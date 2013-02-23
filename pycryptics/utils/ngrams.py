import cPickle as pickle
import os.path


INITIAL_NGRAMS = dict()
NGRAMS = dict()
i = 0
while True:
    if os.path.exists('data/ngrams.%02d.pck' % i):
        with open('data/initial_ngrams.%02d.pck' % i, 'rb') as f:
            d = pickle.load(f)
            INITIAL_NGRAMS.update(d)
        with open('data/ngrams.%02d.pck' % i, 'rb') as f:
            d = pickle.load(f)
            NGRAMS.update(d)
        i += 1
    else:
        break
