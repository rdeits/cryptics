import cPickle as pickle
from utils.synonyms import WORDS

initial_ngrams = dict()
ngrams = dict()

for word in WORDS:
    if '_' in word:
        continue
    l = len(word)
    for i in range(len(word) + 1):
        initial_ngrams.setdefault(l, dict()).setdefault(i, set([])).add(word[:i])
        for j in range(len(word) - i + 1):
            ngrams.setdefault(i, set([])).add(word[j: j + i])

with open('data/initial_ngrams.pck', 'wb') as f:
    pickle.dump(dict(initial_ngrams), f)
with open('data/ngrams.pck', 'wb') as f:
    pickle.dump(dict(ngrams), f)
