package main

import (
	"cryptics/data_gen"
	"cryptics/utils"
	"fmt"
	)

func main() {
	data_gen.GenerateNgrams()
	syns := utils.LoadSynonyms()
	ngrams, initial_ngrams := utils.LoadNgrams()
	fmt.Println(syns["big"])
	fmt.Println(ngrams["cat"])
	fmt.Println(initial_ngrams["fbsx"])
}