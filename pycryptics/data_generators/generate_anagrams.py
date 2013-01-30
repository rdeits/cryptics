import cPickle as pickle
from utils.anagrams import anagrams
from utils.words import WORDS
import json

all_anagrams = dict()

i = 0
length = len(WORDS)
for word in WORDS:
    i += 1
    print '%6f' % (float(i) / length)
    anas = anagrams(word)
    if len(anas) > 0:
        all_anagrams[word] = anas

with open('data/anagrams.json', 'w') as f:
    json.dump(all_anagrams, f, indent=0, separators=(',', ':'))

with open('data/anagrams.pck', 'wb') as f:
    pickle.dump(all_anagrams, f)
