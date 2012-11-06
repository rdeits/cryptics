import sys
sys.path.append('..')
import cPickle as pickle
from load_utils import load_words
from language_utils import synonyms

WORDS = load_words()

all_synonyms = dict()

for word in WORDS:
    all_synonyms[word] = synonyms(word)

with open('data/synonyms.pck', 'wb') as f:
    pickle.dump(dict(all_synonyms), f)
