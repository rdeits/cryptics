from collections import defaultdict
import cPickle as pickle
from utils.words import WORDS

initial_ngrams = defaultdict(lambda: set([]))
ngrams = defaultdict(lambda: set([]))

for word in WORDS:
    for i in range(1, len(word) + 1):
        initial_ngrams[i].add(word[:i])
        for j in range(len(word) - i + 2):
            ngrams[i].add(word[j:j + i])

with open('data/initial_ngrams.pck', 'wb') as f:
    pickle.dump(dict(initial_ngrams), f)
with open('data/ngrams.pck', 'wb') as f:
    pickle.dump(dict(ngrams), f)
