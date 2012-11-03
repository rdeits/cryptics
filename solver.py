from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
import re


def substrings(sentence, length):
    sentence = re.sub(' ', '', sentence)
    for i in range(len(sentence) - length + 1):
        yield sentence[i:i + length]


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
        string = re.sub(' ', '', clue.lower())
        for possible_a in possible_answers(words, length):
            if possible_a in string:
                print possible_a


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
