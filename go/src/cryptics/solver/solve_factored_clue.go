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
