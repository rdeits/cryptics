import pycryptics.utils.cfg as cfg
from pycryptics.utils.synonyms import cached_synonyms, WORDS
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
        return bool(re.match(pattern, ans[:len(pattern)]))

def valid_words(words):
    return "_".join(words) in WORDS

def lit(s, l, p):
    return tuple(s)

def null(s, l, p):
    return ("",)

def first(s, l, p):
    assert(len(s) == 1)
    return (s[0][0],)

def syn(s, l, p):
    assert(len(s) == 1)
    return tuple(cached_synonyms(s[0], sum(l) + 2))

def top(s, l, p):
    ans = "".join(s)
    words = split_words(ans, l)
    if len(ans) == sum(l) and matches_pattern(ans, p) and valid_words(words):
        return tuple([ans])


TRANSFORMS = {cfg.lit: lit,
              cfg.sub_arg: lit,
              cfg.clue_arg: lit,
              cfg.sub_: null,
              cfg.top: top,
              cfg.syn: syn,
              cfg.first: first}
