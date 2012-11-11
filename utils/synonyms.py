import cPickle as pickle
from collections import defaultdict
import json

def load_synonyms():
    with open('data/synonyms.pck', 'rb') as f:
        syns = defaultdict(lambda: [])
        syns.update(pickle.load(f))
        return syns

def load_abbreviations():
    with open('data/abbreviations.json', 'r') as f:
        abbrevs = json.load(f)
    return abbrevs

SYNONYMS = load_synonyms()
ABBREVIATIONS = load_abbreviations()

for s in additional_synonyms:
    SYNONYMS[s].extend(additional_synonyms[s])
for s in ABBREVIATIONS:
    SYNONYMS[s].extend(ABBREVIATIONS[s])


def cached_synonyms(x, length=None):
    x = x.lower()
    syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
    return list(syns)
