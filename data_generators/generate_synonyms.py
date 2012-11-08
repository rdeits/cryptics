import re
import cPickle as pickle
from utils.words import WORDS
from nltk.corpus import wordnet as wn


def synonyms(word):
    word = re.sub(r'\ ', '_', word)
    answers = set([])
    for synset in wn.synsets(word):
        all_synsets = synset.similar_tos()
        all_synsets.append(synset)
        for similar_synset in all_synsets:
            for lemma in similar_synset.lemmas:
                if lemma.name != word:
                    answers.add(lemma.name)
    return answers

all_synonyms = dict()

for word in WORDS:
    all_synonyms[word] = synonyms(word)

with open('data/synonyms.pck', 'wb') as f:
    pickle.dump(dict(all_synonyms), f)
