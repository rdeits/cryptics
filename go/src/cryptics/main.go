package main

import (
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
	runtime.GOMAXPROCS(runtime.NumCPU())
	var phrasing utils.Phrasing
	var num_clues int
	var l int
	var clue string
	solved_parts := map[string]map[string][]string{}
	stdin := bufio.NewReader(os.Stdin)
	solved_clues := []solver.StructuredClue{}
	for {
		clue, _ = stdin.ReadString('\n')
		clue = strings.TrimSpace(clue)
		if clue == "" {
			continue
		} else if clue == ".." {
			break
		} else if clue == "." {
			for i := 0; i < num_clues; i++ {
				for _, a := range solved_clues[i].FormatAnswers() {
					fmt.Println(a)
				}
				fmt.Println(".")
			}
			solved_clues = []solver.StructuredClue{}
			num_clues = 0
		} else if string(clue[0]) == "#" {
			num_clues = 0
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
			num_clues += 1
			solved_clue := solver.SolveFactoredClue(clue, &phrasing, solved_parts)
			solved_clues = append(solved_clues, solved_clue)
		}
	}
}
