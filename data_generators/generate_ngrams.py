import cPickle as pickle
from utils.words import WORDS

initial_ngrams = dict()
ngrams = dict()

for word in WORDS:
    for i in range(1, len(word) + 1):
        initial_ngrams.setdefault(i, set([])).add(word[:i])
        for j in range(len(word) - i + 1):
            ngrams.setdefault(i, set([])).add(word[j: j + i])

with open('data/initial_ngrams.pck', 'wb') as f:
    pickle.dump(dict(initial_ngrams), f)
with open('data/ngrams.pck', 'wb') as f:
    pickle.dump(dict(ngrams), f)
