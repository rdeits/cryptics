package utils

import (
	"io/ioutil"
	"strings"
	"fmt"
	)

func LoadNgrams() (map[string]bool, map[string]bool) {
	ngrams := map[string]bool {}
	initial_ngrams := map[string]bool {}
	raw_ngrams, err := ioutil.ReadFile("data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	ngrams_list := strings.Split(string(raw_ngrams), "\n")
	for _, n := range ngrams_list {
		ngrams[n] = true
	}
	raw_init, err := ioutil.ReadFile("data/initial_ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	init_ngrams_list := strings.Split(string(raw_init), "\n")
	for _, n := range init_ngrams_list {
		initial_ngrams[n] = true
	}
	return ngrams, initial_ngrams
}

