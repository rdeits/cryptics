import cPickle as pickle


def load_initial_ngrams():
    with open('data/initial_ngrams.pck', 'rb') as f:
        initial_ngrams = pickle.load(f)
        initial_ngrams[0] = ['']
        return initial_ngrams


def load_ngrams():
    with open('data/ngrams.pck', 'rb') as f:
        return pickle.load(f)

INITIAL_NGRAMS = load_initial_ngrams()
NGRAMS = load_ngrams()
