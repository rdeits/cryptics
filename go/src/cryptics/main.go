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
	"strings"
)

func main() {
	var phrasing utils.Phrasing
	var pattern string
	var lengths []int
	var l int
	var solved_parts map[string]map[string]bool
	fmt.Println("running")
	stdin := bufio.NewReader(os.Stdin)
	var clue string
	for {
		clue, _ = stdin.ReadString('\n')
		clue = strings.TrimSpace(clue)
		if clue == "" {
			continue
		} else if clue == "." {
			break
		} else if string(clue[0]) == "#" {
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
			solved_parts = map[string]map[string]bool{}
			phrasing = utils.Phrasing{Lengths: lengths, Pattern: pattern}
			fmt.Println(phrasing)
		} else {
			fmt.Println(solver.FormatAnswers(solver.SolveFactoredClue(solver.ParseClue(clue), &phrasing, solved_parts)))
		}
	}
}
