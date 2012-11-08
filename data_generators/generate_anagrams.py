import cPickle as pickle
from utils.anagrams import anagrams
from utils.words import WORDS

all_anagrams = dict()

i = 0
length = len(WORDS)
for word in WORDS:
    i += 1
    print '%6f' % (float(i) / length)
    all_anagrams[word] = anagrams(word)

with open('data/anagrams.pck', 'wb') as f:
    pickle.dump(all_anagrams, f)
