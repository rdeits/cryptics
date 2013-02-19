package solver

import (
	"cryptics/utils"
	// "fmt"
	"strings"
)

func SolveFactoredClue(clue_str string, phrasing *utils.Phrasing, solved_parts map[string]map[string][]string) StructuredClue {
	clue := ParseClue(clue_str)
	err := clue.Solve(phrasing, solved_parts)
	if err {
		clue = StructuredClue{}
	} else {
		results := map[string][]string{}
		for a, parents := range clue.Ans {
			if utils.AnswerTest(a, phrasing) {
				results[strings.Join(utils.SplitWords(a, (*phrasing).Lengths), "_")] = parents
			}
		}
		clue.Ans = results
	}
	return clue
}
