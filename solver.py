from __future__ import division
import nltk
import re
from load_utils import load_words, load_initial_ngrams, load_synonyms, load_anagrams
from language_utils import semantic_similarity, legal_substrings, AnagramDict



FUNCTIONS = ['syn', 'null', 'sub', 'ana']
WORDS = load_words()
INITIAL_NGRAMS = load_initial_ngrams()
SYNONYMS = load_synonyms()
ANAGRAMS = AnagramDict(load_anagrams())

THRESHOLD = .5


def functional_distribution(word):
    """
    Given a word, return a map from cryptic functions to relative probabilities.

    Currently a stub.
    """
    return {'syn': .4, 'null': .2, 'sub': .3, 'ana': .3}



def wordplay(words, length):
    """
    Tries to do the wordplay part of the clue to get an answer of a given length
    """
    for s in substring_words(''.join(words), length):
        yield s
    for f, answer_list in find_all_function_sets(words, length):
        for a in answer_list:
        # for a in answers_from_functions(f, length):
            if len(a) == length:
                yield a


def answers_from_function(f, w, length, answer_list=['']):
    if f == 'null':
        return answer_list
    else:
        new_answer_list = []
        for s in answer_list:
            if f == 'lit':
                candidate = s + w
                if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                    new_answer_list.append(candidate)
            elif f == 'syn':
                for syn in SYNONYMS[w]:
                    candidate = s + syn
                    if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                        new_answer_list.append(candidate)
            elif f == 'sub':
                for l in range(len(w)):
                    for sub in legal_substrings(w, l + 1):
                        candidate = s + sub
                        if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                            new_answer_list.append(candidate)
            elif f == 'ana':
                for ana in ANAGRAMS[w]:
                    candidate = s + ana
                    if len(candidate) <= length and candidate in INITIAL_NGRAMS[len(candidate)]:
                        new_answer_list.append(candidate)
        return new_answer_list


def find_all_function_sets(remaining_words, length, active_set=[([], [''])]):
    """
    Given an ordered list of wordplay words, return all possible arrangements of the functional use of those words, sorted by descending likelihood.
    """
    if len(remaining_words) == 0:
        return sorted(active_set, key=lambda x: functional_likelihood(x[0]), reverse=True)
    else:
        word = remaining_words[0]
        remaining_words = remaining_words[1:]
        new_active_set = []
        for s, answer_list in active_set:
            for f in FUNCTIONS:
                candidate = s + [(word, f)]
                new_answer_list = answers_from_function(f, word, length, answer_list)
                if len(new_answer_list) > 0:
                    new_active_set.append((candidate, new_answer_list))
        return find_all_function_sets(remaining_words, length,
                                         new_active_set)


def functional_likelihood(s):
    p = 1
    for (word, func) in s:
        p *= functional_distribution(word)[func]
    return p


def substring_words(sentence, length):
    sentence = re.sub(' ', '', sentence)
    for i in range(len(sentence) - length + 1):
        s = sentence[i:i + length]
        if s in WORDS:
            yield s


def solve_cryptic_clue(raw_clue):
    print "\n", raw_clue
    clue, length_str = raw_clue.lower().split('(')
    clue = re.sub(r'[^a-zA-Z\ ]', '', clue)
    words = nltk.tokenize.word_tokenize(clue)
    length_str, ans_str = length_str.split(')')
    length = int(re.sub(r'\)', '', length_str))
    true_answer = ans_str.upper()
    answers = []
    for def_words, clue_words in [(words[0:1], words[1:]),
                                 (words[:2], words[2:]),
                                 (words[-2:], words[:-2]),
                                 (words[-1:], words[:-1])]:
        # print "Trying definition:", def_word
        for candidate in wordplay(clue_words, length):
            similarity = semantic_similarity(candidate, ' '.join(def_words))
            if similarity > THRESHOLD:
                answers.append((candidate, similarity))
        answers = sorted(list(set(answers)), key = lambda x: x[1], reverse=True)
    print answers
    if len(answers) > 0:
        print 'Best guess:', answers[0][0]
        return answers[0][0].lower() == true_answer.strip().lower()
    else:
        print "No solution found"
        return False

if __name__ == '__main__':
    for raw_clue in open('clues.txt', 'r').readlines()[:]:
        if raw_clue[0] != '#':
            solve_cryptic_clue(raw_clue)
