package solver

import (
	// "fmt"
	"strings"
)

func ParseClue(raw_clue string) StructuredClue {
	raw_clue = strings.Replace(raw_clue, "'", "", -1)
	raw_clue = strings.Replace(raw_clue, " ", "", -1)
	// stack := []*[]interface{}{}
	stack := []*StructuredClue{}
	var active int
	i := 0
	for j, c := range raw_clue {
		if string(c) == "(" {
			i = j
			// stack = append(stack, &[]interface{}{})
			stack = append(stack, &StructuredClue{})
			active = len(stack) - 1
		} else if string(c) == "," {
			if j-i > 1 {
				stack[active].Type = strings.TrimSpace(raw_clue[i+1 : j])
				// *stack[active] = append(*stack[active], strings.TrimSpace(raw_clue[i+1:j]))
			}
			i = j
		} else if string(c) == ")" {
			if j-i > 1 {
				stack[active].Head = strings.TrimSpace(raw_clue[i+1 : j])
				// *stack[active] = append(*stack[active], strings.TrimSpace(raw_clue[i+1:j]))
			}
			i = j
			if len(stack) > 1 {
				stack[active-1].Args = append(stack[active-1].Args, stack[active])
				// *(stack[active-1]) = append(*(stack[active-1]), *stack[active])
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

func (c *StructuredClue) HashString() string {
	result := "("
	result += c.Type + ", "
	result += c.Head + ", "
	for _, s := range c.Args {
		result += (s).HashString() + ", "
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
	result = "('" + c.Type + "', "
	if c.Head != "" {
		result += "'" + c.Head + "', "
	}
	parents := c.Ans[answer]

	for i, sub_clue := range c.Args {
		result += sub_clue.print_with_answer(parents[i]) + ", "
	}
	result += "'" + strings.ToUpper(answer) + "')"
	return result
}
