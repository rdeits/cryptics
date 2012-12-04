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
	solved_parts := map[string]map[string]bool{}
	var solved_clue solver.SolvedClue
	stdin := bufio.NewReader(os.Stdin)
	var clue string
	ans_c := make(chan solver.SolvedClue)
	map_c := make(chan solver.SolvedClue)
	go UpdateMap(solved_parts, map_c)
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
				fmt.Println(solver.FormatAnswers(solved_clue))
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
			solved_parts = map[string]map[string]bool{}
			phrasing = utils.Phrasing{Lengths: lengths, Pattern: pattern}
			fmt.Println(phrasing)
		} else {
			num_clues += 1
			go solver.SolveFactoredClue(clue, &phrasing, solved_parts, ans_c, map_c)
			// fmt.Println(solver.FormatAnswers(solver.SolveFactoredClue(solver.ParseClue(clue), &phrasing, solved_parts)))
		}
	}
}

func UpdateMap(solved_parts map[string]map[string]bool, c chan solver.SolvedClue) {
	var solved_clue solver.SolvedClue
	for {
		solved_clue = <-c
		solved_parts[solved_clue.Clue] = solved_clue.Answers
	}
}
