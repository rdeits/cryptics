from utils.cfg import generate_clues
import cPickle as pickle


def precompute_clues(max_length):
    """
    Precompute all parses up to max_length
    """
    computed_clues = dict()
    for i in range(1, max_length + 1):
        phrases = range(i)
        computed_clues[i] = generate_clues(phrases)
    with open('data/clue_structures.pck', 'w') as f:
        pickle.dump(computed_clues, f)

if __name__ == '__main__':
    precompute_clues(8)