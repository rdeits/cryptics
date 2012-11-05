import nltk
import cPickle as pickle

with open('data/initial_ngrams.pck', 'rb') as f:
    INITIAL_NGRAMS = pickle.load(f)
with open('data/ngrams.pck', 'rb') as f:
    NGRAMS = pickle.load(f)

with open('data/sowpods.txt', 'r') as f:
    WORDS = set(f.readlines())

