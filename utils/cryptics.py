

additional_synonyms = {'siblings': ['sis'], 'four': ['v'], 'one': ['a', 'i'], 'ten': ['x'], 'fifty': ['l'], 'lego': ['small_bricks'], 'graduate': ['ba'], 'manchu': [], 'rearguard': [], 'somber': ['grave']}


def is_func_argument(i, clue):
    """
    Returns True if clue sub-part i is the argument of a directional function (like 'ana_r' or 'sub_l').

    We do this because insertion always happens after other functions have been resolved.
    """
    return (i > 0 and '_r' in clue[i - 1][1]) or (i < len(clue) - 1 and '_l' in clue[i + 1][1])


def compute_arg_offsets(i, clue):
    kind = clue[i][1]
    if kind[:3] == 'ins':
        arg_offsets = [-1, 1]
        if is_func_argument(i - 1, clue):
        # if i > 1 and '_r' in clue[i - 2][1]:
            arg_offsets[0] = -2
        if is_func_argument(i + 1, clue):
        # if i < len(clue) - 2 and '_l' in clue[i + 2][1]:
            arg_offsets[1] = 2
        func = kind
    else:
        func, direction = kind.split('_')
        if direction == 'l':
            arg_offsets = [-1]
        else:
            arg_offsets = [1]
    return func, arg_offsets

