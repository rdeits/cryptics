package solver

import (
	"cryptics/utils"
	"fmt"
	"strings"
)

const (
	ANA = iota
	SUB
	REV
	INS
	TOP
	ANA_
	SUB_
	INS_
	REV_
	NULL
	LIT
	DEF
	FIRST
	SYN
)

type clue_function func([]string, utils.Phrasing) map[string]bool

var FUNCTIONS = map[int]clue_function{
	ANA: utils.Anagrams,
	SUB: utils.AllLegalSubstrings,
	REV: utils.Reverse,
	INS: utils.AllInsertions,
	TOP: func(s []string, p utils.Phrasing) map[string]bool {
		return map[string]bool{strings.Join(s, ""): true}
	}}

var HEADS = map[int]bool{ANA_: true, SUB_: true, INS_: true, REV_: true, DEF: true}

type StructuredClue struct {
	Type int
	Head string
	Args []*StructuredClue
	Ans  map[string][]string // each answer to this clue is a key in the map and each value is the slice of sub-answers to each clue in Args that gave that particular answer
}

func (clue *StructuredClue) Solve(phrasing *utils.Phrasing, solved_parts map[string]map[string][]string) (err bool) {
	length := utils.Sum((*phrasing).Lengths)
	// fmt.Println("Trying to solve:", clue.HashString())
	ans, ok := solved_parts[clue.HashString()]
	if ok {
		clue.Ans = ans
	} else {
		clue.Ans = map[string][]string{}
		var sub_clue *StructuredClue
		trans, trans_ok := TRANSFORMS[clue.Type]
		if HEADS[clue.Type] {
			trans = TRANSFORMS[NULL]
			trans_ok = true
		}
		clue_func, func_ok := FUNCTIONS[clue.Type]
		if trans_ok {
			clue.Ans = trans(clue.Head, length)
		} else if func_ok {
			args_set := [][]string{{}}
			new_args_set := [][]string{}
			var candidate []string
			for _, sub_clue = range clue.Args {
				err = sub_clue.Solve(phrasing, solved_parts)
				if err {
					solved_parts[clue.HashString()] = clue.Ans
					return true
				}
				new_args_set = [][]string{}
				for _, args := range args_set {
					for ans := range sub_clue.Ans {
						if clue.Type == TOP {
							candidate = append(args, strings.Replace(ans, "_", "", -1))
							if utils.PartialAnswerTest(strings.Join(candidate, ""), phrasing) {
								new_args_set = append(new_args_set, make([]string, len(candidate)))
								copy(new_args_set[len(new_args_set)-1], candidate)
							}
						} else {
							candidate = append(args, ans)
							new_args_set = append(new_args_set, make([]string, len(candidate)))
							copy(new_args_set[len(new_args_set)-1], candidate)
						}
					}
				}
				if len(new_args_set) > 0 {
					args_set = new_args_set
				} else {
					(solved_parts)[clue.HashString()] = clue.Ans
					return true
				}

			}
			for _, args := range args_set {
				for sub_ans := range clue_func(filter_empty_strings(args), *phrasing) {
					clue.Ans[sub_ans] = args
				}
			}
		} else {
			panic("Unrecognized clue type")
		}
		solved_parts[clue.HashString()] = clue.Ans
	}
	_, blank_ans := clue.Ans[""]
	// fmt.Println("returning", clue.Ans, "for clue", clue.HashString())
	if (len(clue.Ans) == 0 || (len(clue.Ans) == 1 && blank_ans)) && (clue.Type != NULL && !HEADS[clue.Type]) {
		// fmt.Println("err true")
		return true
	}
	return false
}

var skip_types = map[int]bool{ANA_: true, SUB_: true, REV_: true, INS_: true}

func (c *StructuredClue) HashString() string {
	result := "(" + type_to_str[c.Type] + ", " + c.Head + ", "
	for _, sub_clue := range c.Args {
		if !skip_types[sub_clue.Type] {
			result += sub_clue.HashString() + ", "
		} else {
			result += " , "
		}
	}
	result += ")"
	return result
}

func (c *StructuredClue) String() string {
	result := "(" + type_to_str[c.Type] + ", " + c.Head + ", "
	for _, sub_clue := range c.Args {
		result += sub_clue.HashString() + ", "
	}
	result += ")"
	return result
}

func (c *StructuredClue) FormatAnswers() []string {
	var results []string
	var result string
	for ans := range c.Ans {
		result = c.print_with_answer(ans)
		results = append(results, result)
	}
	return results
}

func (c *StructuredClue) print_with_answer(answer string) string {
	var result string
	result = "('" + type_to_str[c.Type] + "', "
	if c.Head != "" {
		result += "'" + c.Head + "', "
	}
	parents := c.Ans[answer]
	if len(parents) > 0 && len(parents) != len(c.Args) {
		panic(fmt.Sprint("Ans map: ", c.Ans, "\nanswer: ", answer, "\nparents: ", parents, "\nclue : ", c.String(), "\nlen(parents)=", len(parents), "\nlen(c.Args)=", len(c.Args)))
	}
	if len(parents) > 0 {
		for i, sub_clue := range c.Args {
			result += sub_clue.print_with_answer(parents[i]) + ", "
		}
	}
	result += "'" + strings.ToUpper(answer) + "')"
	return result
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
