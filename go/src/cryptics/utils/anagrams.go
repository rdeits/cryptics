package utils

import (
	"cryptics/load_utils"
	"strings"
)

var NGRAMS *load_utils.Ngrams = load_utils.NGRAMS

func remaining_letters(letters []rune, word string) map[rune]bool {
	remaining := map[rune]bool{}
	for _, x := range letters {
		if strings.Count(string(letters), string(x)) > strings.Count(word, string(x)) {
			remaining[x] = true
		}
	}
	return remaining
}

func Anagrams(word string, active_set ...string) []string {
	letters := []rune{}
	if active_set == nil {
		// active_set = [][]byte{{}}
		active_set = []string{""}
		for _, l := range word {
			if string(l) != "_" {
				letters = append(letters, l)
			}
		}
	} else {
		letters = []rune(word)
	}
	if len(active_set[0]) == len(letters) {
		ans := []string{}
		for _, w := range active_set {
			if w != word {
				ans = append(ans, w)
			}
		}
		return ans
	} else {
		new_active_set := []string{}
		for _, w := range active_set {
			for l := range remaining_letters(letters, w) {
				candidate := w + string(l)
				if NGRAMS.All[candidate] {
					new_active_set = append(new_active_set, candidate)
				}
			}
		}
		if len(new_active_set) == 0 {
			return []string{}
		} else {
			return Anagrams(string(letters), new_active_set...)
		}
	}
	panic("Should never get here")
	return []string{}
}
