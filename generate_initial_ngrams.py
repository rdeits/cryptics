from nltk.corpus import wordnet as wn
from collections import defaultdict
from utils import WORDS
import cPickle as pickle

initial_ngrams = defaultdict(lambda: set([]))

for word in WORDS:
    for i in range(len(word)):
        initial_ngrams[i+1].add(word[:i+1])

with open('initial_ngrams.pck', 'wb') as f:
    pickle.dump(dict(initial_ngrams), f)

