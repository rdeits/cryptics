from __future__ import division
import nltk
from nltk.corpus import wordnet as wn
import re
import cPickle as pickle
from utils import WORDS
from anagram import anagrams

FUNCTIONS = ['lit', 'syn', 'null', 'first', 'ana']

with open('initial_ngrams.pck', 'rb') as f:
    INITIAL_NGRAMS = pickle.load(f)
THRESHOLD = .5

def functional_distribution(word):
    """
    Given a word, return a map from cryptic functions to relative probabilities.

    Currently a stub.
    """
    return {'lit': .4, 'syn': .4, 'null': .2, 'first': .3, 'ana': .2}

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
    for f in find_all_function_sets(words, length):
        for a in answers_from_functions(f, length):
            if len(a) == length:
                yield a


def possible_word_beginning(s):
    """
    given a set of letters, return whether that set of letters can begin any word in our dictionary (used to prune out bad trees)
    """
    raise NotImplementedError

def answers_from_functions(functions, length, active_set=['']):
    if len(functions) == 0:
        return active_set
    else:
        w, f = functions[0]
        functions = functions[1:]
        new_active_set = []
        if f == 'null':
            new_active_set = active_set
        else:
            for s in active_set:
                if f == 'lit':
                    candidate = s + w
                    if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                        new_active_set.append(candidate)
                elif f == 'syn':
                    for syn in synonyms(w):
                        candidate = s + syn
                        if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                            new_active_set.append(candidate)
                elif f == 'first':
                    candidate = s + w[0]
                    if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                        new_active_set.append(candidate)
                elif f == 'ana':
                    for ana in anagrams(w):
                        candidate = s + ana
                        if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                            new_active_set.append(candidate)
        if len(new_active_set) == 0:
            return []
        else:
            return answers_from_functions(functions, length, new_active_set)


def find_all_function_sets(remaining_words, length, active_set=[[]]):
    """
    Given an ordered list of wordplay words, return all possible arrangements of the functional use of those words, sorted by descending likelihood.
    """
    if len(remaining_words) == 0:
        return sorted(active_set, key=lambda x: functional_likelihood(x), reverse=True)
    else:
        word = remaining_words[0]
        remaining_words = remaining_words[1:]
        new_active_set = []
        for s in active_set:
            for f in FUNCTIONS:
                candidate = s + [(word, f)]
                if len(answers_from_functions(candidate, length)) != 0:
                    new_active_set.append(s + [(word, f)])
        return find_all_function_sets(remaining_words, length,
                                         new_active_set)


def functional_likelihood(s):
    p = 1
    for (word, func) in s:
        p *= functional_distribution(word)[func]
    return p


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
    for raw_clue in open('clues.txt', 'r').readlines()[:]:
        print "\n", raw_clue
        clue, length_str = raw_clue.lower().split('(')
        clue = re.sub(r'[^a-zA-Z\ ]', '', clue)
        words = nltk.tokenize.word_tokenize(clue)
        length_str, ans_str = length_str.split(')')
        length = int(re.sub(r'\)', '', length_str))
        true_answer = ans_str.upper()
        answers = []
        for def_word, clue_words in [(words[0], words[1:]),
                                     (words[-1], words[:-1])]:
            print "Trying definition:", def_word
            for candidate in wordplay(clue_words, length):
                similarity = semantic_similarity(candidate, def_word)
                if similarity > THRESHOLD:
                    answers.append((candidate, similarity))
            print sorted(answers, key = lambda x: x[1], reverse=True)


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
