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
        return bool(re.match(pattern[:len(ans)], ans))

def valid_words(words):
    return "_".join(words) in SYNONYMS

def valid_answer(ans, phrasing):
    if len(ans) != sum(phrasing.lengths) or not matches_pattern(ans, phrasing.pattern) or ans in phrasing.phrases:
        return False, None
    words = split_words(ans, phrasing.lengths)
    return valid_words(words), words

def valid_partial_answer(ans, phrasing):
    if len(ans) > sum(phrasing.lengths):
        return False
    if not matches_pattern(ans, phrasing.pattern):
        return False
    words = split_words(ans, phrasing.lengths)
    for i, word in enumerate(words):
        if word not in INITIAL_NGRAMS[phrasing.lengths[i]]:
            return False
    return True

def lit(s, phrasing):
    return s

def null(s, phrasing):
    return [""]

def first(s, phrasing):
    assert(len(s) == 1)
    return [s[0][0]]

def syn(s, phrasing):
    assert(len(s) == 1)
    return cached_synonyms(s[0], sum(phrasing.lengths) + 2)

def top(s, phrasing):
    ans = "".join(s)
    is_valid, words = valid_answer(ans, phrasing)
    if is_valid:
        return ['_'.join(words)]


TRANSFORMS = {'lit': lit,
              'd': null,
              'null': null,
              'sub_': null,
              'sub_arg': lit,
              'clue_arg': lit,
              'rev_': null,
              'rev_arg': lit,
              'ins_': null,
              'ins_arg': lit,
              'ana_': null,
              'ana_arg': lit,
              'top': top,
              'syn': syn,
              'first': first}
