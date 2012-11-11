

def load_words():
    with open('data/sowpods.txt', 'r') as f:
        words = set(w.strip() for w in f.readlines())
    return words


WORDS = load_words()
