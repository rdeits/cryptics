from utils.synonyms import cached_synonyms
from nltk.corpus import wordnet as wn


def semantic_similarity(word1, word2):
    if fast_semantic_similarity(word1, word2) == 1:
        return 1
    max_p = 0
    for s1 in wn.synsets(word1):
        for st1 in [s1] + s1.similar_tos():
            for s2 in wn.synsets(word2):
                for st2 in [s2] + s2.similar_tos():
                    p = wn.wup_similarity(st1, st2)
                    if p == 1:
                        return p
                    if p > max_p:
                        max_p = p
    return max_p


def fast_semantic_similarity(word1, word2):
    syns1 = cached_synonyms(word1)
    syns1.append(word1)
    syns2 = cached_synonyms(word2)
    syns2.append(word2)
    for s1 in syns1:
        if s1 in syns2:
            return 1
    return 0
