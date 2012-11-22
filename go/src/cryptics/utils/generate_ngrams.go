package main

import(
	"io/ioutil"
	"strings"
	"fmt"
	"encoding/json"
	"os"
)


// func readLines(path string) (lines []string, err error) {
// 	var (
// 		file *os.File
// 		part []byte
// 		prefix bool
// 	)
// 	if file, err = os.Open(path); err != nil {
// 		return
// 	}
// 	defer file.Close()

// 	reader := bufio.NewReader(file)
// 	buffer := bytes.NewBuffer(make([]byte, 0))

// 	for {
// 		if part, prefix, err = reader.ReadLine(); err != nil {
// 			break
// 		}
// 		buffer.Write(part)
// 		if !prefix {
// 			lines = append(lines, buffer.String())
// 			buffer.Reset()
// 		}
// 	}
// 	if err == io.EOF {
// 		err = nil
// 	}
// 	return
// }




func main() {
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
	ngrams_file, err := os.Create("ngrams.json")
	if err != nil {
		fmt.Println(err)
	}
	defer ngrams_file.Close()

	initial_ngrams_file, err := os.Create("initial_ngrams.json")
	if err != nil {
		fmt.Println(err)
	}
	defer initial_ngrams_file.Close()

	ngrams_enc := json.NewEncoder(ngrams_file)
	ngrams_json := []string {}
	for s, _ := range ngrams {
		ngrams_json = append(ngrams_json, s)
	}
	if err := ngrams_enc.Encode(&ngrams_json); err != nil {
		fmt.Println(err)
	}
	initial_ngrams_enc := json.NewEncoder(initial_ngrams_file)
	initial_ngrams_json := []string {}
	for s, _ := range initial_ngrams {
		initial_ngrams_json = append(initial_ngrams_json, s)
	}
	if err := initial_ngrams_enc.Encode(&initial_ngrams_json); err != nil {
		fmt.Println(err)
	}
	// const jsonStream = `
	// 	{"Name": ["Ed"]}
	// 	{"Name": ["Sam"]}
	// 	{"Name": ["Ed"]}
	// 	{"Name": ["Sam"]}
	// 	{"Name": ["Ed"]}
	// `
	// type Message struct {
	// 	Name []string
	// }
	// // const jsonStream = `{"foo":["ofo", "oof"]}`
	// // type Anagrams struct {
	// // 	Word string
	// // 	Anas []string
	// // }
	// dec := json.NewDecoder(strings.NewReader(jsonStream))
	// for {
	// 	var a Message
	// 	if err := dec.Decode(&a); err == io.EOF {
	// 		break
	// 	}
	// 	fmt.Printf("%s\n", a.Name)
	// 	// fmt.Println(a.Word)
	// 	// fmt.Println(a.Anas)
	// }
}