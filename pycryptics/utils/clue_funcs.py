from __future__ import division
from pycryptics.utils.synonyms import SYNONYMS
import pycryptics.utils.cfg as cfg
from pycryptics.utils.ngrams import NGRAMS
import re


def reverse(s, phrasing):
    assert len(s) == 1
    return tuple(bigram_filter([''.join(reversed(s[0]))], phrasing))

def all_legal_substrings(words, phrasing):
    assert len(words) == 1
    word = words[0].lower().replace('_', "")
    length = sum(phrasing.lengths)
    subs = set([])
    if len(word) <= 1:
        return subs
    if len(word) > length:
        for i in range(1, len(word) - length):
            s = word[i:i+length]
            if s in SYNONYMS:
                subs.add(s)
    for l in range(1, min(len(word), length + 1, 4)):
        subs.add(word[:l])
    subs.add(word[-1:])
    if len(word) > 2:
        subs.add(word[:1] + word[-1:])
        if len(word) % 2 == 0:
            subs.add(word[len(word)//2-1:len(word)//2+1])
            subs.add(word[:len(word)//2-1] + word[len(word)//2+1:])
        else:
            subs.add(word[len(word)//2:len(word)//2+1])
            subs.add(word[:len(word)//2] + word[len(word)//2+1:])
        subs.add(word[1:])
        subs.add(word[:len(word)-1])
        subs.add(word[1:-1])
    return tuple(bigram_filter(subs, phrasing))


def all_insertions(words, phrasing):
    assert len(words) == 2
    word1, word2 = [w.lower().replace('_', "") for w in words]
    results = set([])
    if len(word1) + len(word2) > sum(phrasing.lengths):
        return None
    for j in range(1, len(word2)):
        results.add(word2[:j] + word1 + word2[j:])
    word2, word1 = word1, word2
    for j in range(len(word2)):
        results.add(word2[:j] + word1 + word2[j:])
    return tuple(bigram_filter(results, phrasing))


def remaining_letters(letters, w):
    for c in set(letters):
        if letters.count(c) > w.count(c):
            yield c


def anagrams(letters, phrasing, active_set=['']):
    letters = re.sub(r'_', '', str(letters))
    if len(active_set[0]) == len(letters):
        return filter(lambda x: x != str(letters), active_set)
    else:
        new_active_set = []
        for w in active_set:
            for c in set(remaining_letters(letters, w)):
                candidate = w + c
                if any(candidate in NGRAMS[l] for l in phrasing.lengths):
                    new_active_set.append(candidate)
        if len(new_active_set) == 0:
            return []
        else:
            return anagrams(letters, phrasing, new_active_set)

def valid_anagrams(words, phrasing):
    assert len(words) == 1
    word = words[0].lower().replace('_', '')
    if len(word) > sum(phrasing.lengths):
        return None
    else:
        return tuple([a for a in anagrams(word, phrasing) if a != word])

def bigram_filter(answers, phrasing):
    threshold = len(phrasing.lengths) - 1  # allow violations across word boundaries

    valid_answers = []
    for ans in answers:
        violations = 0
        for i in range(len(ans)-1):
            ok = False
            for l in phrasing.lengths:
                if ans[i:i+2] in NGRAMS[l]:
                    ok = True
                    break
            if not ok:
                violations += 1
        if violations <= threshold:
            valid_answers.append(ans)
    return valid_answers


FUNCTIONS = {cfg.sub: all_legal_substrings,
             cfg.rev: reverse,
             cfg.ana: valid_anagrams,
             cfg.ins: all_insertions}

if __name__ == '__main__':
    from pycryptics.parse_and_solve import Phrasing
    print reverse(['soda'], Phrasing([], [4,], ""))
    print valid_anagrams(['paint'], Phrasing([], [5], ""))