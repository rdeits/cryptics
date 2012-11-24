package utils

import (
	"cryptics/load_utils"
	"strings"
	)

var NGRAMS load_utils.Ngrams = load_utils.NGRAMS

func remaining_letters(letters []byte, word []byte) map[byte]bool {
	remaining := map[byte]bool {}
	for _, x := range letters {
		if strings.Count(string(letters), string(x)) > strings.Count(string(word), string(x)) {
			remaining[byte(x)] = true
		}
	}
	return remaining
}

func Anagrams(word []byte, active_set ...[]byte) [][]byte  {
	letters := []byte {}
	if active_set == nil {
		active_set = [][]byte{{}}
		for _, l := range word {
			if string(l) != "_" {
				letters = append(letters, l)
			}
		}
	} else {
		letters = word
	}
	if len(active_set[0]) == len(letters) {
		ans := [][]byte {}
		for _, w := range active_set {
			if string(w) != string(word) {
				ans = append(ans, w)
			}
		}
		return ans
	} else {
		new_active_set := [][]byte {}
		for _, w := range active_set {
			for l := range remaining_letters(letters, w) {
				candidate := append(w, l)
				if NGRAMS.All[string(candidate)] {
					new_active_set = append(new_active_set, candidate)
				}
			}
		}
		if len(new_active_set) == 0 {
			return [][]byte {}
		} else {
			return Anagrams(letters, new_active_set...)
		}
	}
	panic("Should never get here")
	return [][]byte{}
}
