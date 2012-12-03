package solver

import "strings"

func ParseClue(raw_clue string) []interface{} {
	raw_clue = strings.Replace(raw_clue, "'", "", -1)
	raw_clue = strings.Replace(raw_clue, " ", "", -1)
	stack := []*[]interface{}{}
	var active int
	i := 0
	for j, c := range raw_clue {
		if string(c) == "(" {
			i = j
			stack = append(stack, &[]interface{}{})
			active = len(stack) - 1
		} else if string(c) == "," {
			if j-i > 1 {
				*stack[active] = append(*stack[active], strings.TrimSpace(raw_clue[i+1:j]))
			}
			i = j
		} else if string(c) == ")" {
			if j-i > 1 {
				*stack[active] = append(*stack[active], strings.TrimSpace(raw_clue[i+1:j]))
			}
			i = j
			if len(stack) > 1 {
				*(stack[active-1]) = append(*(stack[active-1]), *stack[active])
				stack = stack[0:active]
			}
			active -= 1
		}
	}
	if active != -1 {
		panic("Mismatched parentheses")
	}
	return *stack[0]
}
