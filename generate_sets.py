from nltk.corpus import wordnet as wn
import nltk
from collections import defaultdict
import cPickle as pickle

WORDS = set(word.lower() for word in nltk.corpus.words.words())
WORDS.update(set(word.lower() for word in nltk.corpus.brown.words()))

def plural(word):
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word[-1] in 'ex' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    return word + 's'

plurals = set([])
for word in WORDS:
    plurals.add(plural(word))
WORDS.update(plurals)

initial_ngrams = defaultdict(lambda: set([]))
ngrams = defaultdict(lambda: set([]))

for word in WORDS:
    for i in range(1, len(word)):
        initial_ngrams[i].add(word[:i])
        for j in range(len(word) - i + 2):
            ngrams[i].add(word[j:j + i])


with open('initial_ngrams.pck', 'wb') as f:
    pickle.dump(dict(initial_ngrams), f)
with open('ngrams.pck', 'wb') as f:
    pickle.dump(dict(ngrams), f)
with open('words.pck', 'wb') as f:
    pickle.dump(WORDS, f)