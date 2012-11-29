package utils

import (
	"regexp"
)

func MatchesPattern(word, pattern string) bool {
	var result bool
	if pattern == "" {
		result = true
	} else {
		pattern = pattern[0:len(word)]
		result, _ = regexp.MatchString(pattern, word)
	}
	return result
}
