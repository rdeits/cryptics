import nltk
from nltk.corpus import wordnet as wn


def substrings(sentence, length):
    pass


def possible_answers(clue, length):
    words = nltk.tokenize.word_tokenize(clue)
    for word in [words[0], words[-1]]:
        for synset in wn.synsets(word):
            for similar_synset in synset.similar_tos():
                for lemma in similar_synset.lemmas:
                    if len(lemma.name) == length:
                        yield lemma.name


if __name__ == '__main__':
    clue = "Stylish Arab leader described"
    length = 4
    print list(possible_answers(clue, length))
