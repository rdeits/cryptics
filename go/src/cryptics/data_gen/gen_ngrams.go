package data_gen

import (
	"cryptics/utils"
	"fmt"
	"os"
)

func GenerateNgrams() {
	ngrams := map[string]bool{}
	initial_ngrams := map[string]bool{}
	var skip bool
	for word, _ := range utils.SYNONYMS {
		skip = false
		for _, c := range word {
			if string(c) == "_" {
				skip = true
				break
			}
		}
		if skip {
			continue
		}
		for i := 1; i <= len(word); i++ {
			initial_ngrams[word[0:i]] = true
			for j := 0; j <= len(word)-i; j++ {
				ngrams[word[j:j+i]] = true
			}
		}
	}
	ngrams_file, err := os.Create("../data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer ngrams_file.Close()
	for s, _ := range ngrams {
		ngrams_file.WriteString(s + "\n")
	}

	initial_ngrams_file, err := os.Create("../data/initial_ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer initial_ngrams_file.Close()
	for s, _ := range initial_ngrams {
		initial_ngrams_file.WriteString(s + "\n")
	}
}
