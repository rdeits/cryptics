package load_utils

import (
	"fmt"
	"io/ioutil"
	"strings"
)

type Ngrams struct {
	Initial map[string]bool
	All     map[string]bool
}

func LoadNgrams() *Ngrams {
	all_ngrams := map[string]bool{}
	initial_ngrams := map[string]bool{}
	raw_ngrams, err := ioutil.ReadFile("data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	ngrams_list := strings.Split(string(raw_ngrams), "\n")
	for _, n := range ngrams_list {
		all_ngrams[n] = true
	}
	raw_init, err := ioutil.ReadFile("data/initial_ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	init_ngrams_list := strings.Split(string(raw_init), "\n")
	for _, n := range init_ngrams_list {
		initial_ngrams[n] = true
	}
	ngrams := Ngrams{Initial: initial_ngrams, All: all_ngrams}
	return &ngrams
}

var NGRAMS *Ngrams = LoadNgrams()
