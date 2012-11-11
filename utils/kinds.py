import os
from utils.search import tree_search
import cPickle as pickle

KINDS = ['ana_r', 'ana_l', 'sub_r', 'sub_l', 'ins', 'rev_l', 'rev_r', 'lit', 'd', 'syn', 'first', 'null']


def load_all_kinds():
    if os.path.exists('data/kinds.pck'):
        with open('data/kinds.pck', 'rb') as f:
            return pickle.load(f)
    else:
        return dict()


all_kinds = load_all_kinds()
all_kinds[1] = [['d']]


def check_functions(kinds):
    if ('_l' in kinds[0] or kinds[0] == 'ins'):
        return False
    for i in range(len(kinds) - 1):
        if 'ana_r' == kinds[i] and kinds[i + 1] != 'lit':
            return False
        if 'ana_l' == kinds[i + 1] and kinds[i] != 'lit':
            return False
        if '_r' in kinds[i] and kinds[i + 1] not in ['lit', 'syn']:
            return False
        if '_l' in kinds[i + 1] and kinds[i] not in ['lit', 'syn']:
            return False
        if kinds[i] == 'ins' and kinds[i + 1] == 'ins':
            return False
        if kinds[i] == 'ins' and not ('_r' in kinds[i + 1] or kinds[i + 1] in ['lit', 'syn', 'first']):
            return False
        if kinds[i + 1] == 'ins' and not ('_l' in kinds[i] or kinds[i] in ['lit', 'syn', 'first']):
            return False
    return True


def check_totals(kinds):
    if kinds.count('ana_l') + kinds.count('ana_r') > 1:
        return False
    if any(kinds[i] == 'null' and kinds[i + 1] == 'null' and kinds[i + 2] == 'null' for i in range(len(kinds) - 2)):
        return False
    if all(k == 'null' or k == 'd' for k in kinds):
        return False
    return True


def valid_intermediate(kinds):
    if any(k == 'd' for k in kinds[1:-1]):
        return False
    if len(kinds) < 2:
        return True
    return check_functions(kinds) and check_totals(kinds)
    # if kinds[0] == 'd':
    #     if '_l' in kinds[1] or kinds[1] == 'ins':
    #         return False
    # if any('_r' in kinds[i] and ('_l' in kinds[i + 1] or kinds[i + 1] == 'ins') for i in range(len(kinds) - 1)):
    #     return False
    # if any(kinds[i] == 'ins' and '_r' in kinds[i + 1] for i in range(len(kinds) - 1)):
    #     return False
    # if any(kinds[i] == 'ins' and kinds[i + 1] == 'ins' for i in range(len(kinds) - 1)):
    #     return False
    # if kinds[-1] == 'd':
    #     if '_r' in kinds[-2] or kinds[-2] == 'ins':
    #         return False
    # if any('_r' in kinds[i] and kinds[i + 1] != 'lit' for i in range(len(kinds) - 1)):
    #     return False
    # if any(kinds[i] != 'lit' and '_l' in kinds[i + 1] for i in range(len(kinds) - 1)):
    #     return False
    # if any('_r' in kinds[i] and '_l' in kinds[i + 2] for i in range(len(kinds) - 2)):
    #     return False
    # if any((('_r' in kinds[i] or kinds[i] == 'ins') and kinds[i + 1] == 'null') or (('_l' in kinds[i + 1] or kinds[i + 1] == 'ins') and kinds[i] == 'null') for i in range(len(kinds) - 1)):
    #     return False


def valid_kinds(kinds):
    if (kinds[0] == 'd') == (kinds[-1] == 'd'):
        return False
    if ('_r' in kinds[-1] or kinds[-1] == 'ins'):
        return False
    if not valid_intermediate(kinds):
        return False
    return True


def generate_kinds(phrases):
    if len(phrases) in all_kinds:
        return all_kinds[len(phrases)]
    else:
        print "Warning: very long clue. This may take a very long time. Can you make fewer phrases out of this clue?"
        potential_kinds = tree_search([], [KINDS] * (len(phrases)),
                           combination_func=lambda s, w: s + [w],
                           member_test=valid_intermediate)
        generated_kinds = (k for k in potential_kinds if valid_kinds(k))
        return generated_kinds

