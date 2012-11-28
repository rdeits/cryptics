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
	} else {
		for l := 1; l < min(len(word)-1, length, 3)+1; l++ {
			new_subs := legal_substrings(word, length)
			for s := range new_subs {
				subs[s] = true
			}
		}
	}
	return subs
}

func legal_substrings(word string, length int) map[string]bool {
	result := map[string]bool{}
	result[word[0:length]] = true
	result[word[len(word)-length:len(word)]] = true
	if (len(word)%2 == 0) && (length == 2) {
		result[word[len(word)/2-1:len(word)/2+1]] = true
	} else if length == 2 {
		result[word[0:length/2]+word[len(word)-length/2:len(word)]] = true
	} else if (len(word)%2 == 1) && (length == 1 || length == 3) {
		result[word[len(word)/2-length/2:len(word)/2+length/2+1]] = true
	}
	return result
}

func min(x ...int) int {
	result := x[0]
	for _, y := range x[1:len(x)] {
		if y < result {
			result = y
		}
	}
	return result
}
