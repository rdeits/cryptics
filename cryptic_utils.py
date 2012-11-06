

def valid_intermediate(kinds):
    if len(kinds) < 2:
        return True
    if ('_l' in kinds[0] or kinds[0] == 'ins'):
        return False
    if kinds[0] == 'd':
        if '_l' in kinds[1] or kinds[1] == 'ins':
            return False
    if any('_r' in kinds[i] and ('_l' in kinds[i + 1] or kinds[i + 1] == 'ins') for i in range(len(kinds) - 1)):
        return False
    if any(kinds[i] == 'ins' and '_r' in kinds[i + 1] for i in range(len(kinds) - 1)):
        return False
    if kinds[-1] == 'd':
        if '_r' in kinds[-2] or kinds[-2] == 'ins':
            return False
    if kinds.count('ana_l') + kinds.count('ana_r') > 1:
        return False
    if any('_r' in kinds[i] and kinds[i + 1] != 'lit' for i in range(len(kinds) - 1)):
        return False
    if any(kinds[i] != 'lit' and '_l' in kinds[i + 1] for i in range(len(kinds) - 1)):
        return False
    if any('_r' in kinds[i] and '_l' in kinds[i + 2] for i in range(len(kinds) - 2)):
        return False
    if any((('_r' in kinds[i] or kinds[i] == 'ins') and kinds[i + 1] == 'null') or (('_l' in kinds[i + 1] or kinds[i + 1] == 'ins') and kinds[i] == 'null') for i in range(len(kinds) - 1)):
        return False
    return True


def valid_kinds(kinds):
    if (kinds[0] == 'd') == (kinds[-1] == 'd'):
        return False
    if any(k == 'd' for k in kinds[1:-1]):
        return False
    if ('_r' in kinds[-1] or kinds[-1] == 'ins'):
        return False
    if not valid_intermediate(kinds):
        return False
    return True


additional_synonyms = {'siblings': ['sis'], 'four': ['v'], 'one': ['a', 'i'], 'ten': ['x'], 'fifty': ['l']}


def compute_arg_offsets(i, clue):
    kind = clue[i][1]
    if kind[:3] == 'ins':
        arg_offsets = [-1, 1]
        if i > 1 and '_r' in clue[i - 2][1]:
            arg_offsets[0] = -2
        if i < len(clue) - 2 and '_l' in clue[i + 2][1]:
            arg_offsets[1] = 2
        func = kind
    else:
        func, direction = kind.split('_')
        if direction == 'l':
            arg_offsets = [-1]
        else:
            arg_offsets = [1]
    return func, arg_offsets



