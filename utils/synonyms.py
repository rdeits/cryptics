import cPickle as pickle
from collections import defaultdict
from utils.cryptics import additional_synonyms

def load_synonyms():
    with open('data/synonyms.pck', 'rb') as f:
        syns = defaultdict(lambda: [])
        syns.update(pickle.load(f))
        return syns

def load_abbreviations():
    return dict()

SYNONYMS = load_synonyms()
abbreviations = load_abbreviations()
for s in additional_synonyms:
    SYNONYMS[s].extend(additional_synonyms[s])
for s in abbreviations:
    SYNONYM[s].extend(abbreviations[s])


def cached_synonyms(x, length=None):
    x = x.lower()
    syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
    return list(syns)
