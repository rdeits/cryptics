package utils

import "strings"

func Reverse(word string) string {
	ans := []byte(word)
	l := len(word)
	for i, c := range word {
		ans[l-i-1] = c
	}
	return string(ans)
}

func AllLegalSubstrings(word string, length int) {
	subs := map[string]bool {}
	word = strings.ToLower(word)
	if strings.Contains(word, "_"){
		word = strings.Replace(word, "_", "", -1)
		for 
