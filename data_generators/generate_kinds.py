from utils.kinds import valid_intermediate, valid_kinds, KINDS
from utils.search import tree_search
import cPickle as pickle
import json

all_kinds = dict([])

for i in range(1, 10):
    potential_kinds = tree_search([], [KINDS] * i,
                       combination_func=lambda s, w: s + [w],
                       member_test=valid_intermediate)
    all_kinds[i] = [k for k in potential_kinds if valid_kinds(k)]
    print i

with open('data/kinds.pck', 'wb') as f:
    pickle.dump(all_kinds, f)

with open('data/kinds.json', 'w') as f:
    json.dump(all_kinds, f, separators=(',', ':'), indent=0)
