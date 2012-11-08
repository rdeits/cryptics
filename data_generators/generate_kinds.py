from utils.kinds import valid_intermediate, valid_kinds, KINDS
from utils.search import tree_search
import cPickle as pickle

all_kinds = dict([])

for i in range(1, 10):
    potential_kinds = tree_search([], [KINDS] * i,
                       combination_func=lambda s, w: s + [w],
                       member_test=valid_intermediate)
    all_kinds[i] = [k for k in potential_kinds if valid_kinds(k)]
    with open('data/kinds.pck', 'wb') as f:
        print i
        pickle.dump(all_kinds, f)
