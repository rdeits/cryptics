package utils

import (
	"cryptics/ngram_load_utils"
	// "fmt"
	"strings"
)

var NGRAMS map[int]map[string]bool = ngram_load_utils.NGRAMS

func Anagrams(words []string, phrasing Phrasing) map[string]bool {
	if len(words) != 1 {
		panic("Word must be [1]string")
	}
	word := strings.ToLower(words[0])
	word = strings.Replace(word, "_", "", -1)
	l := Sum(phrasing.Lengths)
	if len(word) > l {
		return map[string]bool{}
	}

	letters := map[rune]int{}
	for _, c := range word {
		letters[c] += 1
	}

	// a map from partial anagrams to the remaining letters
	active_set := map[string]map[rune]int{"": letters}
	new_active_set := map[string]map[rune]int{}

	for i := 0; i < len(word); i++ {
		new_active_set = map[string]map[rune]int{}
		for w, ls := range active_set {
			for l := range ls {
				candidate := w + string(l)
				valid := true
				for j, w := range SplitWords(candidate, phrasing.Lengths) {
					if !NGRAMS[phrasing.Lengths[j]][w] {
						// fmt.Println("invalid ngrams", w, "for word length", lengths[i])
						valid = false
						break
					}
				}
				if valid {
					new_active_set[candidate] = map[rune]int{}
					for k, v := range ls {
						if k == l && v > 1 {
							new_active_set[candidate][k] = v - 1
						} else if k != l {
							new_active_set[candidate][k] = v
						}
					}
				}
			}
		}
		if len(new_active_set) == 0 {
			return map[string]bool{}
		} else {
			active_set = new_active_set
		}
	}
	ans := map[string]bool{}
	for w := range active_set {
		if w != word {
			ans[w] = true
		}
	}
	return ans
}
