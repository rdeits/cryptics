import cPickle as pickle
import os.path


SYNONYMS = dict()

i = 0
while True:
    if os.path.exists('data/synonyms.%02d.pck' % i):
        with open('data/synonyms.%02d.pck' % i, 'rb') as f:
            d = pickle.load(f)
            SYNONYMS.update(d)
        i += 1
    else:
        break

def cached_synonyms(x, length=None):
    x = x.lower()
    if x in SYNONYMS:
        syns = [s for s in SYNONYMS[x] if (not length) or (len(s) <= length)]
        return list(syns)
    else:
        return []
