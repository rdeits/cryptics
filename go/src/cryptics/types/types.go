package types

const max_phrase_length = 20

type PhraseKey [max_phrase_length]int

func HashLengths(lengths []int) PhraseKey {
	// In order to store ngrams by phrase length, we need to be able to use tuples of lengths as map keys. This approximates that by converting each slice of ints into a single int. It will break if we ever have phrases of more than <max_phrase_length> words.
	result := PhraseKey{}
	for i, l := range lengths {
		result[i] = l
	}
	return result
}
