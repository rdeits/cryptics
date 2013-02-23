import cPickle as pickle
from pycryptics.utils.synonyms import SYNONYMS

initial_ngrams = dict()
ngrams = dict()

for word in SYNONYMS:
    if '_' in word:
        continue
    l = len(word)
    for i in range(len(word) + 1):
        initial_ngrams.setdefault(l, set([])).add(word[:i])
        for j in range(len(word) - i + 1):
            ngrams.setdefault(l, set([])).add(word[j: j + i])

for i in initial_ngrams:
    with open('data/initial_ngrams.%02d.pck' % i, 'wb') as f:
        pickle.dump({i: initial_ngrams[i]}, f)
for i in ngrams:
    with open('data/ngrams.%02d.pck' %i, 'wb') as f:
        pickle.dump({i: ngrams[i]}, f)
