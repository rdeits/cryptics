import re
from utils.words import WORDS
from utils.synonyms import cached_synonyms
from nltk.corpus import wordnet as wn


def string_reverse(x, length):
    return [''.join(reversed(x))]


def substring_words(sentence, length):
    sentence = re.sub('_', '', sentence).lower()
    for i in range(len(sentence) - length + 1):
        s = sentence[i:i + length]
        if s in WORDS:
            yield s


def all_legal_substrings(word, length):
    word = word.lower()
    subs = []
    for l in range(1, min(len(word) - 1, length) + 1):
        subs.extend(legal_substrings(word, l))
        subs.extend(substring_words(word, l))
    return subs


def legal_substrings(word, length):
    yield word[:length]
    yield word[-length:]
    if len(word) % 2 == 0 and length % 2 == 0:
        yield word[:length//2] + word[-length//2:]
        yield word[len(word)//2-length//2:len(word)//2+length//2]
    elif len(word) % 2 == 1 and length % 2 == 1:
        yield word[len(word)//2-length//2:len(word)//2+length//2+1]


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
    if word1 == '' or word2 == '':
        yield word1 + word2
    for w0, w1 in [(word1, word2), (word2, word1)]:
        for j in range(len(w1)):
            yield w1[:j] + w0 + w1[j:]


def matches_pattern(word, pattern):
    """
    Pattern is a very basic regex, which must have a letter-for-letter mapping with the target string. For example, '.s...a.' is good, but '.s.*a.' will not work.
    """
    if pattern == '':
        return True
    else:
        return bool(re.match(pattern[:len(word)], word))

