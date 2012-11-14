from __future__ import division
from utils.language import all_legal_substrings, semantic_similarity, all_insertions, matches_pattern, string_reverse
from utils.ngrams import NGRAMS
from utils.anagrams import cached_anagrams
from utils.synonyms import cached_synonyms, WORDS
from utils.cryptics import compute_arg_offsets
from utils.kinds import generate_kinds
from utils.search import tree_search
from utils.phrasings import phrasings
import re



FUNCTIONS = {'ana': cached_anagrams, 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': string_reverse}

TRANSFORMS = {'lit': lambda x, l: [x.replace(' ', '').lower()],
              'null': lambda x, l: [''],
              'd': lambda x, l: [''],
              'first': lambda x, l: [x[0].lower()],
              'syn': cached_synonyms}


def solve_clue_text(clue_text):
    solved_parts = dict()
    all_phrasings, answer = parse_clue_text(clue_text)
    answers = set([])
    answers_with_clues = []
    for p in all_phrasings:
        print p
        for ans, clue in solve_phrasing(p, solved_parts):
            if ans not in answers:
                answers.add(ans)
                answers_with_clues.append((ans, clue))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


def parse_clue_text(clue_text):
    if '|' not in clue_text:
        clue_text += ' |'
    clue_text = clue_text.lower()
    clue, rest = clue_text.split('(')
    length, rest = rest.split(')')
    length = int(length)
    pattern, answer = rest.split('|')
    pattern = pattern.strip()
    clue = re.sub(r'[^a-zA-Z\ _]', '', clue)
    clue = re.sub(r'\ +', ' ', clue)
    phrases = clue.split(' ')
    phrases = [p for p in phrases if p.strip() != '']
    all_phrasings = []
    for p in phrasings(phrases):
        p += [length, pattern]
        all_phrasings.append(p)
    return all_phrasings, answer


def solve_phrasing(phrasing, solved_parts=dict()):
    pattern = phrasing.pop()
    length = phrasing.pop()
    answers = set([])
    answers_with_clues = []
    possible_clues = generate_structured_clues(phrasing, length, pattern)
    for i, clue in enumerate(possible_clues):
        # print clue
        new_answers = solve_structured_clue(clue[:], solved_parts)
        new_answers = [a for a in new_answers if a not in answers]
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


def generate_structured_clues(phrases, length, pattern):
    return [zip(phrases, k) + [length, pattern] for k in generate_kinds(phrases)]


def solve_structured_clue(clue, solved_parts=dict()):
    pattern = clue.pop()
    length = clue.pop()
    definition, d = clue[[x[1] for x in clue].index('d')]
    factored_clue = factor_structured_clue(clue)

    def valid_answer(x):
        return matches_pattern(x, pattern) and len(x) == length and x in WORDS

    wordplay_answers = filter(valid_answer, solve_factored_clue(factored_clue, length, solved_parts))
    answers = [(s, semantic_similarity(s, definition)) for s in wordplay_answers if s in WORDS and len(s) == length]
    return sorted(answers, key=lambda x: x[1], reverse=True)


def factor_structured_clue(clue):
    skip = set([])
    for i, group in enumerate(clue):
        if i in skip:
            continue
        phrase, kind = group[:2]
        if '_r' in kind:
            clue[i] = (phrase, kind[:3], clue[i + 1])
            skip.add(i + 1)
        elif '_l' in kind:
            clue[i] = (phrase, kind[:3], clue[i - 1])
            skip.add(i - 1)
    for i, group in enumerate(clue):
        if i in skip:
            continue
        phrase, kind = group[:2]
        if kind == 'ins':
            if i - 1 in skip:
                arg0 = i - 2
            else:
                arg0 = i - 1
            if i + 1 in skip:
                arg1 = i + 2
            else:
                arg1 = i + 1
            clue[i] = (phrase, kind, clue[arg0], clue[arg1])
            skip.add(arg0)
            skip.add(arg1)
    for i in sorted(skip, reverse=True):
        clue.pop(i)
    return ('cat',) + tuple(clue)


def solve_factored_clue(clue, length, solved_parts=dict()):
    if clue in solved_parts:
        return solved_parts[clue]
    if clue[1] in TRANSFORMS:
        result = set(TRANSFORMS[clue[1]](clue[0], length))
    elif clue[1] in FUNCTIONS:
        result = set([])
        arg_sets = tree_search([[]],
                               [solve_factored_clue(c, length) for c in clue[2:]],
                               combination_func=lambda s, w: s + [w])
        for arg_set in arg_sets:
            arg_set += [length]
            result.update(FUNCTIONS[clue[1]](*arg_set))
    elif clue[1] == 'd':
        result = ['']
    elif clue[0] == 'cat':
        result = tree_search([''],
                           [solve_factored_clue(c, length) for c in clue[1:]],
                           member_test=lambda x: len(x) <= length and x in NGRAMS[len(x)])
    else:
        import pdb; pdb.set_trace()
    solved_parts[clue] = result
    return result




if __name__ == '__main__':
    for clue in open('clues/clues.txt', 'r').readlines():
        print solve_clue_text(clue)[:15]
        break

