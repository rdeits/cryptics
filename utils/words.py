import json


def load_words():
    with open('data/sowpods.txt', 'r') as f:
        words = set(w.strip() for w in f.readlines())
    with open('data/abbreviations.json', 'r') as f:
        for key, val in json.load(f).iteritems():
            words.add(key)
            words.update(val)
    return words


WORDS = load_words()
