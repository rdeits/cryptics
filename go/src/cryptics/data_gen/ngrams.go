package data_gen

import(
	"io/ioutil"
	"strings"
	"fmt"
	// "encoding/json"
	"os"
)

func GenerateNgrams() {
	content, err := ioutil.ReadFile("/Users/rdeits/Projects/Cryptics/raw_data/sowpods.txt")
	if err != nil{
		fmt.Println(err)
	}
	lines := strings.Split(string(content), "\n")
	ngrams := map[string]bool {}
	initial_ngrams := map[string]bool {}
	for _, word := range(lines) {
		for i := 1; i <= len(word); i++ {
			initial_ngrams[word[0:i]] = true
			for j := 0; j <= len(word) - i; j ++ {
				ngrams[word[j:j+i]] = true
			}
		}
	}
	ngrams_file, err := os.Create("data/ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer ngrams_file.Close()
	for s, _ := range ngrams {
		ngrams_file.WriteString(s + "\n")
	}

	initial_ngrams_file, err := os.Create("data/initial_ngrams.txt")
	if err != nil {
		fmt.Println(err)
	}
	defer initial_ngrams_file.Close()
	for s, _ := range initial_ngrams {
		initial_ngrams_file.WriteString(s + "\n")
	}

	// ngrams_enc := json.NewEncoder(ngrams_file)
	// ngrams_json := []string {}
	// for s, _ := range ngrams {
	// 	ngrams_json = append(ngrams_json, s)
	// }
	// if err := ngrams_enc.Encode(&ngrams_json); err != nil {
	// 	fmt.Println(err)
	// }
	// initial_ngrams_enc := json.NewEncoder(initial_ngrams_file)
	// initial_ngrams_json := []string {}
	// for s, _ := range initial_ngrams {
	// 	initial_ngrams_json = append(initial_ngrams_json, s)
	// }
	// if err := initial_ngrams_enc.Encode(&initial_ngrams_json); err != nil {
	// 	fmt.Println(err)
	// }
}