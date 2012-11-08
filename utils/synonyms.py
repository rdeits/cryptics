import cPickle as pickle
from collections import defaultdict
from utils.cryptics import additional_synonyms


def load_synonyms():
    with open('data/synonyms.pck', 'rb') as f:
        syns = defaultdict(lambda: set([]))
        syns.update(pickle.load(f))
        return syns

SYNONYMS = load_synonyms()
for s in additional_synonyms:
    SYNONYMS[s].update(additional_synonyms[s])


def cached_synonyms(x, length=None):
    x = x.lower()
    syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
    return list(syns)
