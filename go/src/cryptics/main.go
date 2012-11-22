package main

import (
	// "cryptics/data_gen"
	"cryptics/utils"
	"fmt"
	)

func main() {
	// data_gen.GenerateNgrams()
	syns := utils.LoadSynonyms()
	fmt.Println(syns["big"])
}