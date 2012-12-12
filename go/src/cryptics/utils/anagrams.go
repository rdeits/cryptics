package utils

import (
	"cryptics/ngram_load_utils"
	// "fmt"
	"strings"
)

var NGRAMS map[int]map[string]bool = ngram_load_utils.NGRAMS

func remaining_letters(letters []rune, word string) map[rune]bool {
	remaining := map[rune]bool{}
	for _, x := range letters {
		if strings.Count(string(letters), string(x)) > strings.Count(word, string(x)) {
			remaining[x] = true
		}
	}
	return remaining
}

func Anagrams(words []string, lengths []int) map[string]bool {
	if len(words) > 1 {
		panic("Word must be [1]string")
	}
	word := strings.ToLower(words[0])
	word = strings.Replace(word, "_", "", -1)
	l := Sum(lengths)
	if len(word) > l {
		return map[string]bool{}
	}
	active_set := map[string]bool{"": true}
	return anagrams_with_active_set(word, lengths, active_set)
}

func anagrams_with_active_set(word string, lengths []int, active_set map[string]bool) map[string]bool {
	letters := []rune(word)
	var valid bool
	var candidate string
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
			candidate = w + string(l)
			valid = true
			for i, w := range SplitWords(candidate, lengths) {
				if !NGRAMS[lengths[i]][w] {
					// fmt.Println("invalid ngrams", w, "for word length", lengths[i])
					valid = false
					break
				}
			}
			if valid {
				new_active_set[candidate] = true
			}
		}
	}
	if len(new_active_set) == 0 {
		return map[string]bool{}
	} else {
		return anagrams_with_active_set(string(letters), lengths, new_active_set)
	}
	panic("Should never get here")
	return map[string]bool{}
}
