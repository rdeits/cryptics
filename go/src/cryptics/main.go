package main

import (
	// "cryptics/data_gen"
	// "cryptics/load_utils"
	"cryptics/solver"
	"cryptics/utils"
	"fmt"
)

func main() {
	// data_gen.GenerateNgrams()

	fmt.Println(solver.ParseClue("((foo, bar)(baz))"))
	fmt.Println(solver.ParseClue("('clue', ('sub', ('lit', 'significant_ataxia'), ('sub_', 'overshadows')), ('d', 'choral_piece'))"))

	fmt.Println(utils.Anagrams([]string{"pal"}, 3))
	fmt.Println(solver.TRANSFORMS["syn"]("cat", 10))
	fmt.Println(solver.SolveFactoredClue([]interface{}{"syn", "cat"}, &utils.Phrasing{Lengths: []int{4}, Pattern: ""}, map[string]map[string]bool{}))
	fmt.Println(solver.SolveFactoredClue(solver.ParseClue("('clue', ('sub', ('lit', 'significant_ataxia'), ('sub_', 'overshadows')), ('d', 'choral_piece'))"), &utils.Phrasing{Lengths: []int{7}, Pattern: ""}, map[string]map[string]bool{}))
}
