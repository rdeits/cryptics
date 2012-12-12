package utils

import (
	"fmt"
	"strings"
)

func Reverse(words []string, lengths []int) map[string]bool {
	if len(words) > 1 {
		panic("Word must be [1]string: " + fmt.Sprint(words))
	}
	word := strings.ToLower(words[0])
	ans := []rune(word)
	l := len(word)
	for i, c := range word {
		ans[l-i-1] = c
	}
	return map[string]bool{string(ans): true}
}

func AllLegalSubstrings(words []string, lengths []int) map[string]bool {
	if len(words) > 1 {
		panic("Word must be [1]string")
	}
	length := Sum(lengths)
	subs := map[string]bool{}
	word := strings.ToLower(words[0])
	if strings.Contains(word, "_") {
		word = strings.Replace(word, "_", "", -1)
		for i := 0; i < len(word)-length+1; i++ {
			s := word[i : i+length]
			if _, ok := (SYNONYMS)[s]; ok {
				subs[s] = true
			}
		}
	} else {
		for l := 1; l < min(len(word), length+1, 4); l++ {
			new_subs := legal_substrings(word, l)
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
	result[word[len(word)-length:]] = true
	if (len(word)%2 == 0) && (length == 2) {
		result[word[len(word)/2-1:len(word)/2+1]] = true
	}
	if length == 2 {
		result[string(word[0])+string(word[len(word)-1])] = true
	} else if (len(word)%2 == 1) && (length == 1 || length == 3) {
		result[word[len(word)/2-length/2:len(word)/2+length/2+1]] = true
	}
	return result
}

func min(x ...int) int {
	result := x[0]
	for _, y := range x[1:] {
		if y < result {
			result = y
		}
	}
	return result
}

func AllInsertions(words []string, lengths []int) map[string]bool {
	if len(words) > 2 {
		panic("Word must be [1]string")
	}
	word1 := strings.Replace(words[0], "_", "", -1)
	word2 := strings.Replace(words[1], "_", "", -1)
	result := map[string]bool{}
	if word1 == "" || word2 == "" {
		result[word1+word2] = true
	}
	w0, w1 := word1, word2
	for j := 0; j < len(w1); j++ {
		result[w1[0:j]+w0+w1[j:]] = true
	}
	w1, w0 = word1, word2
	for j := 0; j < len(w1); j++ {
		result[w1[0:j]+w0+w1[j:]] = true
	}
	return result
}
