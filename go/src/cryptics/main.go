package main

import (
	"bufio"
	"cryptics/solver"
	"cryptics/utils"
	"fmt"
	"os"
	"runtime"
	"strings"
)

func main() {
	runtime.GOMAXPROCS(runtime.NumCPU())
	var phrasing utils.Phrasing
	// var num_clues int
	var l int
	var clue string
	solved_parts := map[string]map[string][]string{}
	stdin := bufio.NewReader(os.Stdin)
	for {
		clue, _ = stdin.ReadString('\n')
		clue = strings.TrimSpace(clue)
		if clue == "" {
			continue
		} else if clue == ".." {
			break
		} else if string(clue[0]) == "#" {
			// num_clues = 0
			parts := strings.Split(clue, "(")
			parts = strings.Split(parts[1], ")")
			lengths_str := parts[0]
			lengths := []int{}
			lengths_strs := strings.Split(lengths_str, ",")
			for _, c := range lengths_strs {
				if strings.TrimSpace(c) == "" {
					continue
				}
				fmt.Sscanf(c, "%d", &l)
				lengths = append(lengths, int(l))
			}
			pattern := strings.TrimSpace(parts[1])
			solved_parts = map[string]map[string][]string{}
			phrasing = utils.Phrasing{Lengths: lengths, Pattern: pattern}
			fmt.Println(phrasing)
		} else {
			solved_clue := solver.SolveFactoredClue(clue, &phrasing, solved_parts)
			for _, a := range solved_clue.FormatAnswers() {
				fmt.Println(a)
			}
			fmt.Println(".")
		}
	}
}
