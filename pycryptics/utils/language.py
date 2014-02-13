from pycryptics.utils.synonyms import cached_synonyms
from nltk.corpus import wordnet as wn


def semantic_similarity(word1, word2):
    words1 = word1.split('_')
    words2 = word2.split('_')
    if fast_semantic_similarity(word1, word2) == 1:
        return 1
    max_p = 0
    word1_sim = set([])
    for s1 in wn.synsets(word1):
        word1_sim.add(s1)
        word1_sim.update(s1.similar_tos())
        # for st1 in [s1] + s1.similar_tos():
        #     word1_sim.append(st1)

    word2_sim = set([])
    for s2 in wn.synsets(word2):
        word2_sim.add(s2)
        word2_sim.update(s2.similar_tos())

    for st1 in word1_sim:
        for st2 in word2_sim:
            p = wn.wup_similarity(st1, st2)
            if p == 1:
                return p
            if p > max_p:
                max_p = p
    if len(words1) > 1 or len(words2) > 1:
        sub_similarity = .9 * semantic_similarity(words1[-1], words2[-1])
    else:
        sub_similarity = 0
    return max(max_p, sub_similarity)


def fast_semantic_similarity(word1, word2):
    syns1 = cached_synonyms(word1)
    syns1.add(word1)
    syns2 = cached_synonyms(word2)
    syns2.add(word2)
    for s1 in syns1:
        if s1 in syns2:
            return 1
    return 0
