import re
from utils.synonyms import cached_synonyms, WORDS
from nltk.corpus import wordnet as wn


def string_reverse(x, length):
    return [''.join(reversed(x))]


def all_legal_substrings(word, length):
    subs = set([])
    word = word.lower()
    if '_' in word:
        word = word.replace('_', '')
        for i in range(len(word) - length + 1):
            s = word[i:i + length]
            if s in WORDS:
                subs.add(s)
    else:
        for l in range(1, min(len(word) - 1, length, 3) + 1):
            subs.update(legal_substrings(word, l))
    return subs


def legal_substrings(word, length):
    result = set([])
    result.add(word[:length])
    result.add(word[-length:])
    if len(word) % 2 == 0 and length == 2:
        result.add(word[:length//2] + word[-length//2:])
        result.add(word[len(word)//2-length//2:len(word)//2+length//2])
    elif len(word) % 2 == 1 and length in [1,3]:
        result.add(word[len(word)//2-length//2:len(word)//2+length//2+1])
    return result


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


def all_insertions(word1, word2, length):
    """
    Try inserting word1 into word2 and vice-versa
    """
    word1 = word1.replace('_', '')
    word2 = word2.replace('_', '')
    if word1 == '' or word2 == '':
        yield word1 + word2
    for w0, w1 in [(word1, word2), (word2, word1)]:
        for j in range(len(w1)):
            yield w1[:j] + w0 + w1[j:]




