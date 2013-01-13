package solver

import "cryptics/utils"

type transform func(string, int) map[string][]string

var TRANSFORMS = map[int]transform{
	LIT: func(x string, l int) map[string][]string {
		return map[string][]string{x: []string{}}
	},
	NULL: func(x string, l int) map[string][]string {
		return map[string][]string{"": []string{}}
	},
	FIRST: func(x string, l int) map[string][]string {
		return map[string][]string{string(x[0]): []string{}}
	},
	SYN: func(x string, l int) map[string][]string {
		if syns, ok := (utils.SYNONYMS)[x]; ok {
			if l == 0 {
				panic("Got zero length")
			}
			result := map[string][]string{}
			for _, s := range syns {
				if len(s) <= l+2 { // Don't allow ridiculously long synonyms
					result[s] = []string{}
				}
			}
			return result
		}
		return map[string][]string{}
	}}
