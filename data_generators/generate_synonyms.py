import re
import cPickle as pickle
from nltk.corpus import wordnet as wn
import json
import csv


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


def cleanup(clue):
    clue = re.sub('___', '', clue)
    clue = re.sub('"', '', clue)
    clue = re.sub(' ', '_', clue)
    clue = re.sub('-', '_', clue)
    clue = re.sub(r'\ +', ' ', clue)
    clue = re.sub(r'[^a-zA-Z0-9\ _]', '', clue)
    clue = clue.encode('ascii', 'ignore')
    clue = clue.lower().strip()
    return clue

all_synonyms = dict()

with open('raw_data/sowpods.txt', 'r') as f:
    WORDS = set(w.strip() for w in f.readlines())

for word in WORDS:
    syns = list(synonyms(word))
    all_synonyms[word] = syns

with open('raw_data/abbreviations.json', 'r') as f:
    abbrevs = json.load(f)

for s, vals in abbrevs.items():
    all_synonyms.setdefault(s, []).extend(vals)
    for v in vals:
        all_synonyms.setdefault(cleanup(v), []).append(cleanup(s))

with open('raw_data/American.csv', 'rb') as f:
    american = csv.reader(f)
    for answer, clue in american:
        a, c = cleanup(answer), cleanup(clue)
        if a == "" or c == "":
            continue
        all_synonyms.setdefault(a, []).append(c)
        all_synonyms.setdefault(c, []).append(a)

# with open('raw_data/clues.txt', 'rb') as f:
#     clues = csv.reader(f)
#     for answer, clue in clues:
#         a, c = cleanup(answer), cleanup(clue)
#         if a == "" or c == "":
#             continue
#         all_synonyms.setdefault(a, []).append(c)
#         all_synonyms.setdefault(c, []).append(a)


with open('data/synonyms.pck', 'wb') as f:
    pickle.dump(dict(all_synonyms), f)

with open('data/synonyms.json', 'w') as f:
    json.dump(all_synonyms, f, separators=(',', ':'), indent=0)
