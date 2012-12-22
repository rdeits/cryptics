package ngrams

import (
	"cryptics/syn_load_utils"
	"encoding/gob"
	"fmt"
	"os"
	"strings"
)

func GenerateNgrams() {
	ngrams := map[int]map[string]bool{}
	initial_ngrams := map[int]map[string]bool{}
	// var skip bool
	var key int
	for word, _ := range syn_load_utils.SYNONYMS {
		if strings.Contains(word, "_") {
			continue
		}
		key = len(word)
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
		// fmt.Println(word, key, initial_ngrams[key], ngrams[key])
	}
	ngrams_file, err := os.Create("data/ngrams.gob")
	// ngrams_file, err := os.Create("../data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer ngrams_file.Close()
	gob.NewEncoder(ngrams_file).Encode(ngrams)

	initial_ngrams_file, err := os.Create("data/initial_ngrams.gob")
	if err != nil {
		fmt.Println(err)
	}
	defer initial_ngrams_file.Close()
	gob.NewEncoder(initial_ngrams_file).Encode(initial_ngrams)
}
