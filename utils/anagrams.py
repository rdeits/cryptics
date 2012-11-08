import cPickle as pickle
import os
import re
from utils.ngrams import NGRAMS


def load_anagrams():
    if os.path.exists('data/anagrams.pck'):
        with open('data/anagrams.pck', 'rb') as f:
            return pickle.load(f)
    else:
        return dict()


ANAGRAMS = load_anagrams()


def remaining_letters(letters, w):
    for c in set(letters):
        if letters.count(c) > w.count(c):
            yield c


def anagrams(letters, active_set=['']):
    letters = re.sub(r'_', '', str(letters))
    if len(active_set[0]) == len(letters):
        return active_set
    else:
        new_active_set = []
        for w in active_set:
            for l in set(remaining_letters(letters, w)):
                candidate = w + l
                if candidate in NGRAMS[len(candidate)]:
                    new_active_set.append(candidate)
        if len(new_active_set) == 0:
            return []
        else:
            return anagrams(letters, new_active_set)


def cached_anagrams(x, length=None):
    x = x.lower().replace('_', '')
    if length and (len(x) > length):
        return []
    if x not in ANAGRAMS:
        ANAGRAMS[x] = anagrams(x)
    return filter(lambda y: y != x, ANAGRAMS[x])
