from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
import re

WORDS = set(word.lower() for word in nltk.corpus.words.words())


def functional_distribution(word):
    """
    Given a word, return a map from cryptic functions to relative probabilities.

    Currently a stub.
    """
    return {'lit': .4, 'syn': .4, 'null': .2}

def semantic_similarity(word1, word2):
    max_p = 0
    for s1 in wn.synsets(word1):
        for st1 in [s1] + s1.similar_tos():
            for s2 in wn.synsets(word2):
                for st2 in [s2] + s2.similar_tos():
                    p = wn.wup_similarity(st1, st2)
                    if p > max_p:
                        max_p = p
    return max_p

def wordplay(words, length):
    """
    Tries to do the wordplay part of the clue to get an answer of a given length
    """
    for s in substrings(''.join(words), length):
        yield s


def substrings(sentence, length):
    sentence = re.sub(' ', '', sentence)
    for i in range(len(sentence) - length + 1):
        s = sentence[i:i + length]
        if s in WORDS:
            yield s


def synonyms(word):
    answers = set([])
    for synset in wn.synsets(word):
        all_synsets = synset.similar_tos()
        all_synsets.append(synset)
        for similar_synset in all_synsets:
            for lemma in similar_synset.lemmas:
                if lemma.name != word:
                    answers.add(lemma.name)
    return answers


def possible_answers(words, length):
    answers = set([])
    for word in [words[0], words[-1]]:
        answers.update(synonyms(word))
    return answers


def middle_letters(word):
    if len(word) % 2 == 0:
        return word[len(word) // 2 - 1:len(word) // 2]
    else:
        return word[len(word) // 2]

word_functions = {
    'literal': lambda x: x,
    'first': lambda x: x[0],
    'last': lambda x: x[-1],
    'outside': lambda x: x[0] + x[-1],
    'middle': middle_letters,
    'synonym': synonyms,
    'null': lambda x: ''
    }


def constructed_answers(words):
    if len(words) == 0:
        return ['']
    answers = set([])
    for action in word_functions:
        for substring in constructed_answers(words[1:]):
            answers.add(action(words[0]) + substring)
    return answers


if __name__ == '__main__':
    for raw_clue in open('clues.txt', 'r').readlines():
        print "\n", raw_clue
        clue, length_str = raw_clue.lower().split('(')
        words = nltk.tokenize.word_tokenize(clue)
        length = int(re.sub(r'\)', '', length_str))
        for def_word, clue_words in [(words[0], words[1:]),
                                     (words[-1], words[:-1])]:
            print "Trying definition:", def_word
            for candidate in wordplay(clue_words, length):
                print candidate, semantic_similarity(candidate, def_word)


"""
What can a word do?
* appear literally (1)
* first letter (1)
* last letter (1)
* outside letters (1)
* middle letter(s) (1)
* reverse part of the clue (?)
* appear as a synonym (?, roughly 5, say)
* yield a substring
* do nothing
"""
