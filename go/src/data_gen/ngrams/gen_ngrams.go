package ngrams

import (
	"cryptics/syn_load_utils"
	"cryptics/types"
	"encoding/gob"
	"fmt"
	"os"
	"strings"
)

func GenerateNgrams() {
	ngrams := map[types.PhraseKey]map[string]bool{}
	initial_ngrams := map[types.PhraseKey]map[string]bool{}
	// var skip bool
	var w string
	var lengths []int
	var words []string
	var key types.PhraseKey
	for word, _ := range syn_load_utils.SYNONYMS {
		words = strings.Split(word, "_")
		lengths = []int{}
		for _, w = range words {
			lengths = append(lengths, len(w))
		}
		word = strings.Replace(word, "_", "", -1)
		key = types.HashLengths(lengths)
		// skip = false
		// for _, c := range word {
		// 	if string(c) == "_" {
		// 		skip = true
		// 		break
		// 	}
		// }
		// if skip {
		// 	continue
		// }
		if initial_ngrams[key] == nil {
			initial_ngrams[key] = map[string]bool{}
		}
		if ngrams[key] == nil {
			ngrams[key] = map[string]bool{}
		}
		for i := 1; i <= len(word); i++ {
			initial_ngrams[key][word[0:i]] = true
			for j := 0; j <= len(word)-i; j++ {
				ngrams[key][word[j:j+i]] = true
			}
		}
		fmt.Println(word, key, initial_ngrams[key], ngrams[key])
	}
	ngrams_file, err := os.Create("data/ngrams.gob")
	// ngrams_file, err := os.Create("../data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer ngrams_file.Close()
	gob.NewEncoder(ngrams_file).Encode(ngrams)
	// for s, _ := range ngrams {
	// 	ngrams_file.WriteString(s + "\n")
	// }

	// initial_ngrams_file, err := os.Create("../data/initial_ngrams.txt")
	initial_ngrams_file, err := os.Create("data/initial_ngrams.gob")
	if err != nil {
		fmt.Println(err)
	}
	defer initial_ngrams_file.Close()
	gob.NewEncoder(initial_ngrams_file).Encode(initial_ngrams)
	// for s, _ := range initial_ngrams {
	// 	initial_ngrams_file.WriteString(s + "\n")
	// }
}
