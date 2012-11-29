package main

import (
	// "cryptics/data_gen"
	// "cryptics/load_utils"
	"cryptics/utils"
	"fmt"
)

func main() {
	// data_gen.GenerateNgrams()
	// syns := utils.LoadSynonyms()
	// ngrams, initial_ngrams := utils.LoadNgrams()
	// fmt.Println(syns["big"])
	// fmt.Println(ngrams["cat"])
	// fmt.Println(initial_ngrams["fbsx"])
	// fmt.Println(utils.Anagrams([]byte("pal")))
	// foo := []byte("foo")
	// bar := []byte("bar")
	// baz := []byte("baz")
	// bap := []byte("bap")
	// branching_list := [][][]byte{{foo, bar}, {baz, bap}}
	// fmt.Println(utils.ByteTreeSearch(branching_list, func(foo []byte) bool { return true }))
	fmt.Println(utils.AllLegalSubstrings("aca_tb", 3))
	fmt.Println(utils.AllLegalSubstrings("acatb", 2))
	fmt.Println(utils.AllInsertions("foo", "bar", 1))
	fmt.Println(utils.MatchesPattern("foobar", "f..b.r"))
	fmt.Println(utils.MatchesPattern("foobar", "f..a.r"))
	fmt.Println(utils.MatchesPattern("foobar", ""))
	fmt.Println(utils.MatchesPattern("foo", "f..b.r"))
}
