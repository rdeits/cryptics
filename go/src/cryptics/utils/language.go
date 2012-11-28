package utils

import (
	"cryptics/load_utils"
	"strings"
)

var SYNONYMS = load_utils.LoadSynonyms()

func Reverse(word string) string {
	ans := []rune(word)
	l := len(word)
	for i, c := range word {
		ans[l-i-1] = c
	}
	return string(ans)
}

func AllLegalSubstrings(word string, length int) map[string]bool {
	subs := map[string]bool{}
	word = strings.ToLower(word)
	if strings.Contains(word, "_") {
		word = strings.Replace(word, "_", "", -1)
		for i := 0; i < len(word)-length+1; i++ {
			s := word[i : i+length]
			if _, ok := SYNONYMS[s]; ok {
				subs[s] = true
			}
		}
	}
	return subs
}
