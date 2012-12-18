package solver

import "cryptics/utils"

type transform func(string, int) map[string][]string

var TRANSFORMS map[string]transform = map[string]transform{
	"lit": func(x string, l int) map[string][]string {
		return map[string][]string{x: []string{}}
	},
	"null": func(x string, l int) map[string][]string {
		return map[string][]string{"": []string{}}
	},
	"d": func(x string, l int) map[string][]string {
		return map[string][]string{"": []string{}}
	},
	"first": func(x string, l int) map[string][]string {
		return map[string][]string{string(x[0]): []string{}}
	},
	"syn": func(x string, l int) map[string][]string {
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
