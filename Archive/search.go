package utils

import (
	// "fmt"
	"strings"
)

func StringTreeSearch(branching_list []map[string][]string, member_test func(string) bool) map[string][]string {
	active_set := [][]string{{}}
	new_active_set := [][]string{}
	var candidate []string
	for _, part := range branching_list {
		new_active_set = [][]string{}
		for _, s := range active_set {
			for w := range part {
				candidate = append(s, strings.Replace(w, "_", "", -1))
				if member_test(strings.Join(candidate, "")) {
					new_active_set = append(new_active_set, candidate)
				}
			}
		}
		active_set = new_active_set
	}
	result := map[string][]string{}
	for _, s := range active_set {
		result[strings.Join(s, "")] = s
	}
	return result
}
