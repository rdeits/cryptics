package ngram_load_utils

import (
	"cryptics/types"
	"encoding/gob"
	"fmt"
	"os"
)

// type Ngrams struct {
// 	Initial map[string]bool
// 	All     map[string]bool
// }

func LoadNgrams() map[types.PhraseKey]map[string]bool {
	var ngrams map[types.PhraseKey]map[string]bool
	raw_ngrams, err := os.Open("data/ngrams.gob")
	if err != nil {
		fmt.Println(err)
	}
	gob.NewDecoder(raw_ngrams).Decode(&ngrams)
	return ngrams
}

func LoadInitialNgrams() map[types.PhraseKey]map[string]bool {
	var initial_ngrams map[types.PhraseKey]map[string]bool
	init_ngrams_file, err := os.Open("data/initial_ngrams.gob")
	if err != nil {
		fmt.Println(err)
	}
	gob.NewDecoder(init_ngrams_file).Decode(&initial_ngrams)
	return initial_ngrams
}

var NGRAMS = LoadNgrams()
var INITIAL_NGRAMS = LoadInitialNgrams()
