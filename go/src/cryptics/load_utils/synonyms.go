package utils

import (
	"io/ioutil"
	"encoding/json"
	"fmt"
	)

func LoadSynonyms() map[string][]string {
	data, err := ioutil.ReadFile("../data/synonyms.json")
	if err != nil {
		fmt.Println(err)
	}
	var raw_syns interface{}
	err = json.Unmarshal(data, &raw_syns)
	if err != nil {
		fmt.Println(err)
	}
	syns := map[string][]string {}
	for k, v := range raw_syns.(map[string]interface{}) {
		syns[k] = []string {}
		for _, s := range v.([]interface{}) {
			syns[k] = append(syns[k], s.(string))
		}
	}
	return syns
}
