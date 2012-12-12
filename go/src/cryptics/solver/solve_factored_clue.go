package solver

import (
	"cryptics/utils"
	"strings"
	// "fmt"
)

type transform func(string, int) map[string][]string
type clue_function func([]string, []int) map[string]bool

var FUNCTIONS map[string]clue_function = map[string]clue_function{"ana": utils.Anagrams, "sub": utils.AllLegalSubstrings, "rev": utils.Reverse, "ins": utils.AllInsertions}

var TRANSFORMS map[string]transform = map[string]transform{"lit": func(x string, l int) map[string][]string {
	return map[string][]string{x: []string{}}
}, "null": func(x string, l int) map[string][]string {
	return map[string][]string{"": []string{}}
}, "d": func(x string, l int) map[string][]string {
	return map[string][]string{"": []string{}}
}, "first": func(x string, l int) map[string][]string {
	return map[string][]string{string(x[0]): []string{}}
}, "syn": func(x string, l int) map[string][]string {
	if syns, ok := (utils.SYNONYMS)[x]; ok {
		if l == 0 {
			panic("Got zero length")
		}
		result := map[string][]string{}
		for _, s := range syns {
			if len(s) <= l {
				result[s] = []string{}
			}
		}
		return result
	}
	return map[string][]string{}
}}

var HEADS = map[string]bool{"ana_": true, "sub_": true, "ins_": true, "rev_": true}

func SolveFactoredClue(clue_str string, phrasing *utils.Phrasing, solved_parts map[string]map[string][]string, ans_c chan StructuredClue, map_c chan bool) {
	clue := ParseClue(clue_str)
	err := clue.Solve(phrasing, solved_parts, map_c)
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
	ans_c <- clue
}

type StructuredClue struct {
	Type string
	Head string
	Args []*StructuredClue
	Ans  map[string][]string // each answer to this clue is a key in the map and each value is the slice of sub-answers to each clue in Args that gave that particular answer
}

func filter_empty_strings(input []string) []string {
	result := []string{}
	for _, s := range input {
		if s != "" {
			result = append(result, s)
		}
	}
	return result
}

func (clue *StructuredClue) Solve(phrasing *utils.Phrasing, solved_parts map[string]map[string][]string, map_c chan bool) (err bool) {
	length := utils.Sum((*phrasing).Lengths)
	var sub_answers map[string][]string
	// fmt.Println("Trying to solve:", clue.HashString())
	<-map_c
	ans, ok := solved_parts[clue.HashString()]
	map_c <- true
	clue.Ans = map[string][]string{}
	var sub_clue *StructuredClue
	var new_args []string
	if ok {
		clue.Ans = ans
	} else {
		trans, trans_ok := TRANSFORMS[clue.Type]
		if HEADS[clue.Type] {
			trans = TRANSFORMS["null"]
			trans_ok = true
		}
		clue_func, func_ok := FUNCTIONS[clue.Type]
		if trans_ok {
			clue.Ans = trans(clue.Head, length)
		} else if func_ok {
			args_set := [][]string{{}}
			new_args_set := [][]string{}
			for _, sub_clue := range clue.Args {
				err = sub_clue.Solve(phrasing, solved_parts, map_c)
				if err {
					<-map_c
					solved_parts[clue.HashString()] = clue.Ans
					map_c <- true
					return true
				}
				new_args_set = [][]string{}
				for _, args := range args_set {
					sub_answers = sub_clue.Ans
					for sub_ans := range sub_answers {
						new_args = append(args, sub_ans)
						new_args_set = append(new_args_set, new_args)
					}
				}
				args_set = new_args_set
			}
			for _, args := range args_set {
				// fmt.Println("function args:", filter_empty_strings(args))
				for sub_ans := range clue_func(filter_empty_strings(args), (*phrasing).Lengths) {
					clue.Ans[sub_ans] = args
				}
			}
		} else if clue.Type == "clue" {
			member_test := func(x string) bool {
				return utils.PartialAnswerTest(x, phrasing)
			}
			all_sub_answers := []map[string][]string{}
			for _, sub_clue = range clue.Args {
				err = sub_clue.Solve(phrasing, solved_parts, map_c)
				if err {
					<-map_c
					(solved_parts)[clue.HashString()] = clue.Ans
					map_c <- true
					return true
				}
				sub_answers = sub_clue.Ans
				all_sub_answers = append(all_sub_answers, sub_answers)
			}
			clue.Ans = utils.StringTreeSearch(all_sub_answers, member_test)
		} else {
			panic("Unrecognized clue type")
		}
	}
	<-map_c
	solved_parts[clue.HashString()] = clue.Ans
	map_c <- true
	_, blank_ans := clue.Ans[""]
	// fmt.Println("returning", clue.Ans, "for clue", clue.HashString())
	if len(clue.Ans) <= 1 && blank_ans && (clue.Type != "null" && clue.Type != "d" && !HEADS[clue.Type]) {
		// fmt.Println("err true")
		return true
	} else {
		// fmt.Println("err false")
		return false
	}
	return false
}
