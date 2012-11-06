import sys
sys.path.append('..')
import cPickle as pickle
from load_utils import load_words
from language_utils import anagrams

WORDS = load_words()

all_anagrams = dict()

i = 0
length = len(WORDS)
for word in WORDS:
    i += 1
    print '%6f' % (float(i) / length)
    all_anagrams[word] = anagrams(word)

with open('data/anagrams.pck', 'wb') as f:
    pickle.dump(all_anagrams, f)
