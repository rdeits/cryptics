import re
import msgpack
from nltk.corpus import wordnet as wn
# from nltk.tag import pos_tag
import json
import csv
import en


def synonyms(word):
    word = re.sub(r'\ ', '_', word)
    answers = set([])
    for synset in wn.synsets(word):
        all_synsets = synset.similar_tos()
        all_synsets.append(synset)
        for similar_synset in all_synsets:
            for lemma in similar_synset.lemmas():
                candidate = correct_form(lemma.name(), word).lower()
                if candidate != word and candidate != "" and not any(c in word.split('_') for c in candidate.split('_')) and not any(c in candidate.split('_') for c in word.split('_')):
                    answers.add(candidate)
    return answers


def correct_form(ans, word):
    if "_" in ans:
        return ans
    # print "correcting", ans, "to match", word
    if en.verb.infinitive(word):
        if en.verb.infinitive(ans):
            return en.verb.conjugate(ans, en.verb.tense(word))
        else:
            return ans
    else:
        if en.is_noun(word):
            return en.noun.singular(ans)
        else:
            return ans


def cleanup(clue):
    if '___' in clue:
        return ""
    clue = re.sub('"', '', clue)
    clue = re.sub(' ', '_', clue)
    clue = re.sub('-', '_', clue)
    clue = re.sub(r'\ +', ' ', clue)
    clue = re.sub(r'[^a-zA-Z0-9\ _]', '', clue)
    clue = clue.encode('ascii', 'ignore')
    clue = clue.lower().strip().strip('_')
    return clue


def main():
    all_synonyms = dict()

    # with open('raw_data/sowpods.txt', 'r') as f:
    #     WORDS = set(w.strip() for w in f.readlines())

    with open('raw_data/UKACD.txt', 'r') as f:
        while True:
            line = f.readline()
            if line[0] == "-":
                break
        WORDS = set(map(cleanup, f.readlines()))

    i = 0
    for word in WORDS:
        if i % 1000 == 0:
            print i, "/", len(WORDS)
        i += 1
        word = word.lower()
        syns = map(cleanup, list(synonyms(word)))
        all_synonyms[word] = syns
        # if syns:
        #     print word, syns
    print "loaded sowpods"

    with open('raw_data/bigrams.txt', 'r') as f:
        for line in f.readlines():
            words, count = line.split('\t')
            if int(count) < 5:
                continue
            if re.search(r'[^a-zA-Z0-9 -_]', words) or re.search(r'0[A-Z]+\.0', words):
                continue
            words = cleanup(words)
            all_synonyms.setdefault(words, []).extend(map(cleanup, list(synonyms(words))))
    print "loaded bigrams"

    with open('raw_data/abbreviations.json', 'r') as f:
        abbrevs = json.load(f)

    for s, vals in abbrevs.items():
        all_synonyms.setdefault(s, []).extend(vals)
        for v in vals:
            all_synonyms.setdefault(cleanup(v), []).append(cleanup(s))
    print "loaded abbreviations"

    with open('raw_data/American.csv', 'rb') as f:
        american = csv.reader(f)
        for answer, clue in american:
            a, c = cleanup(answer), cleanup(clue)
            if a == "" or c == "":
                continue
            all_synonyms.setdefault(a, []).append(c)
            all_synonyms.setdefault(c, []).append(a)
    print "loaded American.csv"

    for k, v in all_synonyms.items():
        all_synonyms[k] = list(set(v))
    print 'removed duplicates'

    with open('data/synonyms.msgpack', 'w') as f:
        msgpack.dump(all_synonyms, f)

    with open('data/synonyms.json', 'w') as f:
        json.dump(all_synonyms, f, separators=(',', ':'), indent=0)

if __name__ == '__main__':
    main()
