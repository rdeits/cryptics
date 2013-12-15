from pycryptics.utils.synonyms import cached_synonyms, SYNONYMS
from pycryptics.utils.ngrams import INITIAL_NGRAMS
import re

def split_words(ans, lengths):
    j = 0
    words = []
    stop = 0
    for l in lengths:
        stop = j + l
        if j >= len(ans):
            return words
        elif stop >= len(ans):
            stop = len(ans)
        words.append(ans[j:stop])
        j += l
    return words

def matches_pattern(ans, pattern):
    if pattern == "":
        return True
    else:
        return all(c == pattern[i] or pattern[i] == '.' for i, c in enumerate(ans))

def valid_words(words):
    return "_".join(words) in SYNONYMS

def valid_answer(ans, constraints):
    if len(ans) != sum(constraints.lengths) or not matches_pattern(ans, constraints.pattern) or ans in constraints.phrases:
        return False, None
    words = split_words(ans, constraints.lengths)
    return valid_words(words), words

def valid_partial_answer(ans, constraints):
    if len(ans) > sum(constraints.lengths):
        return False
    if not matches_pattern(ans, constraints.pattern):
        return False
    words = split_words(ans, constraints.lengths)
    for i, word in enumerate(words):
        if word not in INITIAL_NGRAMS[constraints.lengths[i]]:
            return False
    return True

def lit_fun(s, constraints):
    return s

def null_fun(s, constraints):
    return [""]

def first_fun(s, constraints):
    assert(len(s) == 1)
    return [s[0][0]]

def syn_fun(s, constraints):
    assert(len(s) == 1)
    return cached_synonyms(s[0], sum(constraints.lengths) + 2)

def top_fun(s, constraints):
    ans = "".join(s)
    is_valid, words = valid_answer(ans, constraints)
    if is_valid:
        return ['_'.join(words)]


# TRANSFORMS = {'lit': lit,
#               'd': null,
#               'null': null,
#               'sub_': null,
#               'sub_arg': lit,
#               'clue_arg': lit,
#               'rev_': null,
#               'rev_arg': lit,
#               'ins_': null,
#               'ins_arg': lit,
#               'ana_': null,
#               'ana_arg': lit,
#               'top': top,
#               'syn': syn,
#               'first': first}
