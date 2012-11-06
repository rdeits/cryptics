from nltk.corpus import wordnet as wn
import cPickle as pickle
from collections import defaultdict



def load_initial_ngrams():
    with open('data/initial_ngrams.pck', 'rb') as f:
        initial_ngrams = pickle.load(f)
        initial_ngrams[0] = ['']
        return initial_ngrams


def load_ngrams():
    with open('data/ngrams.pck', 'rb') as f:
        return pickle.load(f)


def load_words():
    with open('data/sowpods.txt', 'r') as f:
        return set(w.strip() for w in f.readlines())


def load_synonyms():
    with open('data/synonyms.pck', 'rb') as f:
        syns = defaultdict(lambda: [])
        syns.update(pickle.load(f))
        return syns

def load_anagrams():
    with open('data/anagrams.pck', 'rb') as f:
        return pickle.load(f)
