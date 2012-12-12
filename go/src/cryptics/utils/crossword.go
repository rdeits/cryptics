package utils

import (
	"cryptics/load_utils"
	// "fmt"
	"regexp"
	// "strings"
)

var SYNONYMS map[string][]string = load_utils.SYNONYMS

type Phrasing struct {
	Lengths []int
	Pattern string
}

func matches_pattern(word, pattern string) bool {
	var result bool
	if pattern == "" {
		result = true
	} else {
		pattern = pattern[0:len(word)]
		result, _ = regexp.MatchString(pattern, word)
	}
	return result
}

func SplitWords(ans string, lengths []int) []string {
	// if strings.TrimSpace(ans) == "" {
	// 	return []string{}
	// }
	j := 0
	words := []string{}
	var stop int
	for _, l := range lengths {
		stop = j + l
		if j >= len(ans) {
			return words
		} else if stop >= len(ans) {
			stop = len(ans)
		}
		words = append(words, ans[j:stop])
		j += l
	}
	return words
}

func PartialAnswerTest(ans string, phrasing *Phrasing) bool {
	// words := SplitWords(ans, (*phrasing).Lengths)
	return len(ans) <= Sum((*phrasing).Lengths) && matches_pattern(ans, (*phrasing).Pattern) && valid_initial_words(ans, (*phrasing).Lengths)
}

func AnswerTest(ans string, phrasing *Phrasing) bool {
	// words := SplitWords(ans, (*phrasing).Lengths)
	return len(ans) == Sum((*phrasing).Lengths) && matches_pattern(ans, (*phrasing).Pattern) && valid_words(ans, (*phrasing).Lengths)
}

func Sum(x []int) int {
	ans := 0
	for j := 0; j < len(x); j++ {
		ans += x[j]
	}
	return ans
}

func valid_initial_words(ans string, lengths []int) bool {
	return load_utils.INITIAL_NGRAMS[HashLengths(lengths)][ans]
	// for _, w := range words {
	// 	if x := NGRAMS.Initial[w]; !x {
	// 		return false
	// 	}
	// }
	// return true
}

func valid_words(ans string, lengths []int) bool {
	return load_utils.NGRAMS[HashLengths(lengths)][ans]
	// for _, w := range words {
	// 	if _, ok := (SYNONYMS)[w]; !ok {
	// 		return false
	// 	}
	// }
	// return true
}
