package main

import "fmt"

func main() {
	my_map := map[int]int{}
	c := make(chan [2]int)
	xs := []int{1, 1, 2}
	for j := 0; j < 5; j++ {
		for _, x := range xs {
			go double(x, my_map, c)
		}
		for i := 0; i < len(xs); i++ {
			fmt.Println(<-c)
		}
	}
}

func double(x int, my_map map[int]int, c chan [2]int) {
	if y, ok := my_map[x]; ok {
		fmt.Println("cache hit on: ", x)
		c <- [2]int{x, y}
	} else {
		fmt.Println("cache miss on: ", x)
		y := x * 2
		my_map[x] = y
		c <- [2]int{x, y}
	}
}
