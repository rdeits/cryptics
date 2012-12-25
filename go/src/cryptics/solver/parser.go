package solver

import (
	// "fmt"
	"strings"
)

var type_to_str = map[int]string{
	ANA:   "ana",
	SUB:   "sub",
	REV:   "rev",
	INS:   "ins",
	TOP:   "top",
	ANA_:  "ana_",
	SUB_:  "sub_",
	INS_:  "ins_",
	REV_:  "rev_",
	LIT:   "lit",
	NULL:  "null",
	DEF:   "d",
	FIRST: "first",
	SYN:   "syn"}

var str_to_type = map[string]int{
	"ana":   ANA,
	"sub":   SUB,
	"rev":   REV,
	"ins":   INS,
	"top":   TOP,
	"ana_":  ANA_,
	"sub_":  SUB_,
	"ins_":  INS_,
	"rev_":  REV_,
	"lit":   LIT,
	"null":  NULL,
	"d":     DEF,
	"first": FIRST,
	"syn":   SYN}

func ParseClue(raw_clue string) StructuredClue {
	raw_clue = strings.Replace(raw_clue, "'", "", -1)
	raw_clue = strings.Replace(raw_clue, " ", "", -1)
	stack := []*StructuredClue{}
	var active int
	i := 0
	for j, c := range raw_clue {
		if string(c) == "(" {
			i = j
			stack = append(stack, &StructuredClue{})
			active = len(stack) - 1
		} else if string(c) == "," {
			if j-i > 1 {
				stack[active].Type = str_to_type[strings.TrimSpace(raw_clue[i+1:j])]
			}
			i = j
		} else if string(c) == ")" {
			if j-i > 1 {
				stack[active].Head = strings.TrimSpace(raw_clue[i+1 : j])
			}
			i = j
			if len(stack) > 1 {
				stack[active-1].Args = append(stack[active-1].Args, stack[active])
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
