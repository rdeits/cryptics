import pycryptics.utils.cfg as cfg
from pycryptics.utils.synonyms import cached_synonyms, SYNONYMS
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
    return "_".join(words) in SYNONYMS

def valid_answer(ans, phrasing):
    words = split_words(ans, phrasing.lengths)
    return len(ans) == sum(phrasing.lengths) and matches_pattern(ans, phrasing.pattern) and valid_words(words) and not ans in phrasing.phrases

def lit(s, phrasing):
    return tuple(s)

def null(s, phrasing):
    return ("",)

def first(s, phrasing):
    assert(len(s) == 1)
    return (s[0][0],)

def syn(s, phrasing):
    assert(len(s) == 1)
    return tuple(cached_synonyms(s[0], sum(phrasing.lengths) + 2))

def top(s, phrasing):
    ans = "".join(s)
    if valid_answer(ans, phrasing):
        return tuple(['_'.join(split_words(ans, phrasing.lengths))])
    else:
        return None


TRANSFORMS = {cfg.lit: lit,
              cfg.sub_: null,
              # cfg.sub_arg: lit,
              # cfg.clue_arg: lit,
              cfg.rev_: null,
              # cfg.rev_arg: lit,
              cfg.ins_: null,
              # cfg.ins_arg: lit,
              cfg.ana_: null,
              # cfg.ana_arg: lit,
              cfg.top: top,
              cfg.syn: syn,
              cfg.first: first}
