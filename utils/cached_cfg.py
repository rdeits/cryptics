import cPickle as pickle


def load_clue_structures():
    with open('data/clue_structures.pck', 'rb') as f:
        c = load(f)
    return c


CLUE_STRUCTURES = load_clue_structures()

def convert_indexed_clue(clue, phrases):
    if isinstance(clue, str):
        return clue
    elif isinstance(clue, int):
        return phrases[clue]
    else:
        return tuple([convert_indexed_clue(c) for c in clue])


def cached_clue_structures(phrases):
    for indexed_clue in CLUE_STRUCTURES[len(phrases)]:
        yield convert_indexed_clue(indexed_clue, phrases)
