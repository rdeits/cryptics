package utils

import (
	// "cryptics/load_utils"
	"strings"
	)

func remaining_letters(letters string, word string) map[byte]bool {
	remaining := map[byte]bool {}
	for _, x := range letters {
		if strings.Count(letters, string(x)) > strings.Count(word, string(x)) {
			remaining[byte(x)] = true
		}
	}
	return remaining
}

func Anagrams(word string) map[byte]bool {
	return remaining_letters("foob", "fo")
}
