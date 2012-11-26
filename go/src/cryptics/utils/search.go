package utils

import "bytes"

func ByteTreeSearch(branching_list [][][]byte, member_test func([]byte) bool) [][]byte {
	start := [][]byte{[]byte{}}
	active_set := start
	new_active_set := [][]byte{}
	candidate := []byte{}
	for _, part := range branching_list {
		new_active_set = [][]byte{}
		for _, s := range active_set {
			for _, w := range part {
				candidate = bytes.Join([][]byte{s, w}, []byte{})
				if member_test(candidate) {
					new_active_set = append(new_active_set, candidate)
				}
			}
		}
		active_set = new_active_set
	}
	return active_set
}
