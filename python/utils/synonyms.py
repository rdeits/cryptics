import cPickle as pickle


def load_synonyms():
    with open('data/synonyms.pck', 'rb') as f:
        syns = pickle.load(f)
        return syns


SYNONYMS = load_synonyms()
WORDS = SYNONYMS.keys()


def cached_synonyms(x, length=None):
    x = x.lower()
    if x in SYNONYMS:
        syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
        return list(syns)
    else:
        return []
