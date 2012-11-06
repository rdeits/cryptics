from __future__ import division
from load_utils import load_words, load_initial_ngrams, load_anagrams, load_synonyms
from language_utils import all_legal_substrings, semantic_similarity, all_insertions, anagrams, matches_pattern
from cryptic_utils import valid_intermediate, valid_kinds, additional_synonyms, compute_arg_offsets
from search import tree_search
import re

WORDS = load_words()
INITIAL_NGRAMS = load_initial_ngrams()
ANAGRAMS = load_anagrams()
SYNONYMS = load_synonyms()
for s in additional_synonyms:
    SYNONYMS[s].update(additional_synonyms[s])

def cached_anagrams(x, length):
    if len(x) > length:
        return ['']
    if x in ANAGRAMS:
        return filter(lambda y: y != x, ANAGRAMS[x])
    else:
        return filter(lambda y: y != x, anagrams(x))


def cached_synonyms(x, length):
    syns = [s for s in SYNONYMS[x.replace(' ', '_')] if len(s) <= length]
    if len(syns) == 0:
        syns = [x]
    return list(syns)

THRESHOLD = 0.5

all_phrases = [
               ['attractive', 'female', 'engraving', 8, ''],
               ['join', 'trio of', 'astronomers', 'in', 'marsh', 6, 'f.....'],
               ['host', 'played in the pool', 'around', 'four', 'finally', (5), 's....'],
               ['spin', 'broken', 'shingle', 7, 'e......'],
               ['initially', 'babies', 'are', 'naked', 4, ''],
               ['tenor', 'and', 'alto', 'upset', 'count', 5, ''],
               ['sat', 'up', 'interrupting', 'siblings', 'balance', 6, ''],
               ['ach cole', 'wrecked', 'something in the ear', 7, ''],
               ['Bottomless', 'sea', 'stormy', 'sea', 'waters', 'surface', 'rises and falls', 7, '']
               ]


FUNCTIONS = {'ana': cached_anagrams, 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': lambda x, l: [''.join(reversed(x))]}

TRANSFORMS = {'lit': lambda x, l: [x.replace(' ', '')],
              'null': lambda x, l: [''],
              'first': lambda x, l: [x[0]],
              'syn': cached_synonyms}

KINDS = ['ana_r', 'ana_l', 'sub_r', 'sub_l', 'ins', 'rev_l', 'rev_l', 'lit', 'd', 'syn', 'first', 'null']


def generate_structured_clues(phrases, length, pattern):
    potential_kinds = tree_search([], [KINDS] * (len(phrases)),
                       combination_func=lambda s, w: s + [w],
                       member_test=valid_intermediate)
    for kinds in potential_kinds:
        if valid_kinds(kinds):
            yield zip(phrases, kinds) + [length, pattern]


def solve_structured_clue(clue):
    pattern = clue.pop()
    length = clue.pop()
    definition, d = clue.pop([x[1] for x in clue].index('d'))
    groups_to_skip = set([])
    answer_subparts = [[] for x in clue]
    while any(s == [] for index, s in enumerate(answer_subparts) if index not in groups_to_skip):
        for i, group in enumerate(clue):
            if answer_subparts[i] != []:
                continue
            phrase, kind = group[:2]
            if kind[:3] in FUNCTIONS:
                func, arg_offsets = compute_arg_offsets(i, clue)
                arg_indices = [i + x for x in arg_offsets]
                groups_to_skip.update(arg_indices)
                if any(answer_subparts[j] == [] for j in arg_indices):
                    continue
                arg_sets = tree_search([],
                                       [answer_subparts[ai] for ai in arg_indices],
                                       combination_func=lambda s, w: s + [w])
                for arg_set in arg_sets:
                    arg_set += [length]
                    answer_subparts[i].extend(list(FUNCTIONS[func](*arg_set)))
                if len(answer_subparts[i]) == 0:
                    return []
            else:
                answer_subparts[i] = TRANSFORMS[kind](phrase, length)
            # elif kind == 'lit':
            #     answer_subparts[i] = [phrase.replace(' ', '')]
            # elif kind == 'null':
            #     answer_subparts[i] = ['']
            # elif kind == 'first':
            #     answer_subparts[i] = [phrase[0]]
            # elif kind == 'syn':
            #     syns = SYNONYMS[phrase.replace(' ', '_')]
            #     if len(syns) == 0:
            #         syns = [phrase]
            #     answer_subparts[i] = list(syns)
    potential_answers = set(tree_search('', answer_subparts,
                                    lambda x: x not in groups_to_skip,
                                    lambda x: len(x) <= length and x in INITIAL_NGRAMS[len(x)] and matches_pattern(x, pattern)))
    answers = [(s, semantic_similarity(s, definition)) for s in potential_answers if s in WORDS and len(s) == length]
    return sorted(answers, key=lambda x: x[1], reverse=True)


def solve_phrases(phrases):
    pattern = phrases.pop()
    length = phrases.pop()
    answers = set([])
    answers_with_clues = []
    for clue in generate_structured_clues(phrases, length, pattern):
        new_answers = solve_structured_clue(clue)
        new_answers = [a for a in new_answers if a not in answers]
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


if __name__ == '__main__':
    for phrases in all_phrases:
        print phrases
        answers = solve_phrases(phrases)[:50]
        for a in answers:
            print a
        print "\n"

