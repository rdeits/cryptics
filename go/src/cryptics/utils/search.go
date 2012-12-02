package utils

import "strings"

func StringTreeSearch(branching_list []map[string]bool, member_test func(string) bool) map[string]bool {
	active_set := map[string]bool{"": true}
	var new_active_set map[string]bool
	var candidate string
	for _, part := range branching_list {
		new_active_set = map[string]bool{}
		for s := range active_set {
			for w := range part {
				candidate = s + w
				candidate = strings.Replace(candidate, "_", "", -1)
				if member_test(candidate) {
					new_active_set[candidate] = true
				}
			}
		}
		active_set = new_active_set
	}
	return active_set
}
