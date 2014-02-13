from pycryptics.utils.synonyms import cached_synonyms, SYNONYMS
from pycryptics.utils.ngrams import INITIAL_NGRAMS

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
    if len(ans) != sum(constraints.lengths) or not matches_pattern(ans, constraints.pattern) or ans in constraints.phrases or any(x.startswith(ans) for x in constraints.phrases) or any(ans ==x for p in constraints.phrases for x in p.split('_')):
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
