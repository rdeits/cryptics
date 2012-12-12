package solver

import (
	"cryptics/utils"
	"fmt"
)

type transform func(string, int) map[string][]string
type clue_function func([]string, int) map[string]bool

// type SolvedClue struct {
// 	Clue    string
// 	Answers map[string]bool
// }

// func string_hash(clue []interface{}) string {
// 	result := "("
// 	for _, c := range clue {
// 		switch v := c.(type) {
// 		case string:
// 			result += v + ", "
// 		default:
// 			result += string_hash(c.([]interface{})) + ", "
// 		}
// 	}
// 	result += ")"
// 	return result
// }

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
	clue.Solve(phrasing, solved_parts, map_c)
	fmt.Println("solution candidates:", clue.Ans)
	results := map[string][]string{}
	for a, parents := range clue.Ans {
		if utils.AnswerTest(a, phrasing) {
			results[a] = parents
		}
	}
	clue.Ans = results
	fmt.Println(clue.Args[0].Ans)
	ans_c <- clue
	// candidates, _ := solve_partial_clue(clue, phrasing, solved_parts, map_c)
	// // fmt.Println(candidates)
	// results := map[string]bool{}
	// for a := range candidates {
	// 	if utils.AnswerTest(a, phrasing) {
	// 		results[a] = true
	// 	}
	// }
	// ans_c <- SolvedClue{Clue: clue_str, Answers: results}
}

type StructuredClue struct {
	Type string
	Head string
	Args []*StructuredClue
	Ans  map[string][]string // each answer to this clue is a key in the map and each value is the slice of sub-answers to each clue in Args
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
	fmt.Println("Trying to solve:", clue.HashString())
	ans, ok := solved_parts[clue.HashString()]
	clue.Ans = map[string][]string{}
	var sub_clue *StructuredClue
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
			for i, sub_clue := range clue.Args {
				fmt.Println("working on sub clue", sub_clue)
				fmt.Println("before solving", clue.Args[i].Ans)
				err = sub_clue.Solve(phrasing, solved_parts, map_c)
				fmt.Println("after solving", clue.Args[i].Ans)
				fmt.Println("sub clue", sub_clue)
				fmt.Println("sub answers", sub_clue.Ans)
				if err {
					<-map_c
					solved_parts[clue.HashString()] = clue.Ans
					map_c <- true
					fmt.Println(sub_clue, "unsolvable")
					return true
				}
				new_args_set = [][]string{}
				fmt.Println("args set", args_set)
				for _, args := range args_set {
					fmt.Println("in loop")
					sub_answers = sub_clue.Ans
					for sub_ans, _ := range sub_answers {
						fmt.Println("args", sub_ans)
						args = append(args, sub_ans)
						new_args_set = append(new_args_set, args)
						fmt.Println("new args set", new_args_set)
					}
				}
				args_set = new_args_set
			}
			for _, args := range args_set {
				for sub_ans := range clue_func(filter_empty_strings(args), length) {
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
					fmt.Println(sub_clue, "unsolvable")
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
	fmt.Println("returning", clue.Ans)
	if len(clue.Ans) == 1 && blank_ans && (clue.Type != "null" && clue.Type != "d" && !HEADS[clue.Type]) {
		return true
	} else {
		return false
	}
	return false
}

// func solve_partial_clue(clue []interface{}, phrasing *utils.Phrasing, solved_parts map[string]map[string]bool, map_c chan bool) (map[string]bool, bool) {
// 	length := utils.Sum((*phrasing).Lengths)
// 	var result map[string]bool
// 	var sub_answers map[string]bool
// 	var err bool
// 	var sub_ans string
// 	var s []string
// 	// fmt.Println("Trying to solve:", clue)
// 	// <-map_c
// 	ans, ok := solved_parts[string_hash(clue)]
// 	// map_c <- true
// 	if ok {
// 		result = ans
// 		// fmt.Println("Cache hit")
// 	} else {
// 		// fmt.Println("Cache miss")
// 		trans, trans_ok := TRANSFORMS[clue[0].(string)]
// 		clue_func, func_ok := FUNCTIONS[clue[0].(string)]
// 		if trans_ok {
// 			result = trans(clue[1].(string), length)
// 		} else if func_ok {
// 			result = map[string]bool{}
// 			active_set := [][]string{{}}
// 			var new_active_set [][]string
// 			var sub_clue []interface{}
// 			for _, sub_part := range clue[1:len(clue)] {
// 				sub_clue = sub_part.([]interface{})
// 				if _, ok := HEADS[sub_clue[0].(string)]; ok {
// 					continue
// 				}
// 				new_active_set = [][]string{}
// 				for _, s = range active_set {
// 					sub_answers, err = solve_partial_clue(sub_clue, phrasing, solved_parts, map_c)
// 					if err {
// 						<-map_c
// 						(solved_parts)[string_hash(clue)] = result
// 						map_c <- true
// 						return result, true
// 					}
// 					for sub_ans = range sub_answers {
// 						new_active_set = append(new_active_set, append(s, sub_ans))
// 					}
// 				}
// 				active_set = new_active_set
// 			}
// 			for _, arg_set := range active_set {
// 				for sub_ans = range clue_func(arg_set, length) {
// 					result[sub_ans] = true
// 				}
// 			}
// 		} else if clue[0].(string) == "clue" {
// 			member_test := func(x string) bool {
// 				return utils.PartialAnswerTest(x, phrasing)
// 			}
// 			all_sub_answers := []map[string]bool{}
// 			var sub_clue []interface{}
// 			for _, sub_part := range clue[1:len(clue)] {
// 				sub_clue = sub_part.([]interface{})
// 				sub_answers, err = solve_partial_clue(sub_clue, phrasing, solved_parts, map_c)
// 				all_sub_answers = append(all_sub_answers, sub_answers)
// 				if err {
// 					<-map_c
// 					(solved_parts)[string_hash(clue)] = result
// 					map_c <- true
// 					return result, true
// 				}
// 			}
// 			result = utils.StringTreeSearch(all_sub_answers, member_test)
// 		} else {
// 			// fmt.Println("Got this clue type: ", clue[0])
// 			panic("Unrecognized clue type")
// 		}
// 	}
// 	// solved_parts[string_hash(clue)] = result
// 	<-map_c
// 	solved_parts[string_hash(clue)] = result
// 	map_c <- true
// 	// map_c <- SolvedClue{Clue: string_hash(clue), Answers: result}
// 	if len(result) == 1 && result[""] == true && (clue[0].(string) != "null" && clue[0].(string) != "d") {
// 		return result, true
// 	} else {
// 		return result, false
// 	}
// 	// fmt.Println("Returning: ", result, " for clue: ", clue)
// 	return result, false
// }
