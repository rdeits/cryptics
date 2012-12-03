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

func Anagrams(words []string, l int) map[string]bool {
	if len(words) > 1 {
		panic("Word must be [1]string")
	}
	word := strings.ToLower(words[0])
	if len(word) > l {
		return map[string]bool{}
	}
	word = strings.Replace(word, "_", "", -1)
	active_set := map[string]bool{"": true}
	return anagrams_with_active_set(word, active_set)
}

func anagrams_with_active_set(word string, active_set map[string]bool) map[string]bool {
	letters := []rune(word)
	for w := range active_set {
		if len(w) == len(letters) {
			ans := map[string]bool{}
			for w := range active_set {
				if w != word {
					ans[w] = true
				}
			}
			return ans
		} else {
			break
		}
	}
	new_active_set := map[string]bool{}
	for w := range active_set {
		for l := range remaining_letters(letters, w) {
			candidate := w + string(l)
			if NGRAMS.All[candidate] {
				new_active_set[candidate] = true
			}
		}
	}
	if len(new_active_set) == 0 {
		return map[string]bool{}
	} else {
		return anagrams_with_active_set(string(letters), new_active_set)
	}
	panic("Should never get here")
	return map[string]bool{}
}
