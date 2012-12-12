package main

import (
	// "cryptics/data_gen"
	// "cryptics/load_utils"
	"bufio"
	"cryptics/solver"
	"cryptics/utils"
	"fmt"
	// "io/ioutil"
	"os"
	"runtime"
	"strings"
)

func main() {
	runtime.GOMAXPROCS(8)
	var phrasing utils.Phrasing
	var pattern string
	var lengths []int
	var l int
	var num_clues int
	solved_parts := map[string]map[string][]string{}
	stdin := bufio.NewReader(os.Stdin)
	var clue string
	var solved_clue solver.StructuredClue
	ans_c := make(chan solver.StructuredClue)
	map_c := make(chan bool, 1)
	map_c <- true
	for {
		clue, _ = stdin.ReadString('\n')
		clue = strings.TrimSpace(clue)
		if clue == "" {
			continue
		} else if clue == ".." {
			break
		} else if clue == "." {
			for i := 0; i < num_clues; i++ {
				solved_clue = <-ans_c
				answers := solved_clue.FormatAnswers()
				if len(answers) > 0 {
					for _, a := range solved_clue.FormatAnswers() {
						fmt.Println(a)
					}
				} else {
					fmt.Println("[]")
				}
			}
			num_clues = 0
		} else if string(clue[0]) == "#" {
			num_clues = 0
			parts := strings.Split(clue, "(")
			parts = strings.Split(parts[1], ")")
			lengths_str := parts[0]
			lengths = []int{}
			lengths_strs := strings.Split(lengths_str, ",")
			for _, c := range lengths_strs {
				if strings.TrimSpace(c) == "" {
					continue
				}
				fmt.Sscanf(c, "%d", &l)
				lengths = append(lengths, int(l))
			}
			pattern = strings.TrimSpace(parts[1])
			solved_parts = map[string]map[string][]string{}
			phrasing = utils.Phrasing{Lengths: lengths, Pattern: pattern}
			fmt.Println(phrasing)
		} else {
			num_clues += 1
			go solver.SolveFactoredClue(clue, &phrasing, solved_parts, ans_c, map_c)
			// fmt.Println(solver.FormatAnswers(solver.SolveFactoredClue(solver.ParseClue(clue), &phrasing, solved_parts)))
		}
	}
}
