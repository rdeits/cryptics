import cPickle as pickle

with open('ngrams.pck', 'rb') as f:
    NGRAMS = pickle.load(f)

def anagrams(letters, active_set = ['']):
    if len(active_set[0]) == len(letters):
        return active_set
    else:
        new_active_set = []
        for w in active_set:
            for l in set(remaining_letters(letters, w)):
                candidate = w + l
                if candidate in NGRAMS[len(candidate)]:
                    new_active_set.append(candidate)
        if len(new_active_set) == 0:
            return []
        else:
            return anagrams(letters, new_active_set)

def remaining_letters(letters, w):
    for c in set(letters):
        if letters.count(c) > w.count(c):
            yield c
