package solver

import (
	"cryptics/utils"
)

type transform func(string, int) map[string]bool

var FUNCTIONS map[string]transform = map[string]transform{"ana": func(x string, l int) map[string]bool {
	if len(x) < l {
		return map[string]bool{}
	}
	return utils.Anagrams(x)
}, "sub": utils.AllLegalSubstrings, "rev": utils.Reverse}

var TRANSFORMS map[string]transform = map[string]transform{"lit": func(x string, l int) map[string]bool {
	return map[string]bool{x: true}
}, "null": func(x string, l int) map[string]bool {
	return map[string]bool{}
}, "d": func(x string, l int) map[string]bool {
	return map[string]bool{}
}, "first": func(x string, l int) map[string]bool {
	return map[string]bool{string(x[0]): true}
}, "syn": func(x string, l int) map[string]bool {
	if syns, ok := (*utils.SYNONYMS)[x]; ok {
		if l == 0 {
			panic("Got zero length")
		}
		result := map[string]bool{}
		for _, s := range syns {
			if len(s) <= l {
				result[s] = true
			}
		}
		return result
	}
	return map[string]bool{}
}}

var HEADS []string = []string{"ana_", "sub_", "ins_", "rev_"}

type FactoredClue struct {
	Type string
	Head string
	Args interface{}
}

func SolveFactoredClue(clue FactoredClue, phrasing *utils.Phrasing, solved_parts *map[FactoredClue]map[string]bool) map[string]bool {
	length := utils.Sum((*phrasing).Lengths)
	var result map[string]bool
	if ans, ok := (*solved_parts)[clue]; ok {
		result = ans
	} else {
		if trans, ok := TRANSFORMS[clue.Type]; ok {
			result = trans(clue.Head, length)
		} else if clue_func, ok := FUNCTIONS[clue.Type]; ok {
			result = map[string]bool{}
			for s := range SolveFactoredClue(clue.Args.([1]FactoredClue)[0], phrasing, solved_parts) {
				for r := range clue_func(s, length) {
					result[r] = true
				}
			}
		} else if clue.Type == "ins" {
			result = map[string]bool{}
			sub_clue_1 := clue.Args.([2]FactoredClue)[0]
			sub_clue_2 := clue.Args.([2]FactoredClue)[1]
			for s1 := range SolveFactoredClue(sub_clue_1, phrasing, solved_parts) {
				for s2 := range SolveFactoredClue(sub_clue_2, phrasing, solved_parts) {
					for r := range utils.AllInsertions(s1, s2, length) {
						result[r] = true
					}
				}
			}
		} else if clue.Type == "clue" {
			member_test := func(x string) bool {
				return utils.PartialAnswerTest(x, phrasing)
			}
			sub_answers := []map[string]bool{}
			for _, sub_clue := range clue.Args.([]FactoredClue) {
				sub_answers = append(sub_answers, SolveFactoredClue(sub_clue, phrasing, solved_parts))
			}
			result = utils.StringTreeSearch(sub_answers, member_test)
		} else {
			panic("Unrecognized clue type")
		}
	}
	(*solved_parts)[clue] = result
	return result
}
