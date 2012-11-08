from utils.cryptics import additional_synonyms


def load_words():
    with open('data/sowpods.txt', 'r') as f:
        return set(w.strip() for w in f.readlines())


WORDS = load_words()
WORDS.update(additional_synonyms.keys())
