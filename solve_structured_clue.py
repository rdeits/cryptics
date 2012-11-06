from __future__ import division
import sys
from load_utils import load_words, load_initial_ngrams, load_anagrams, load_synonyms
from language_utils import anagrams, synonyms, all_legal_substrings, semantic_similarity, all_insertions, AnagramDict
from search import tree_search

WORDS = load_words()
INITIAL_NGRAMS = load_initial_ngrams()
ANAGRAMS = AnagramDict(load_anagrams())
SYNONYMS = load_synonyms()
SYNONYMS['siblings'].add('sis')

clues = [
[('initially', 'sub', [1]),
('babies', 'arg'),
('are', 'lit'),
('naked', 'd', 4)],
[('tenor', 'first'),
('and', 'null'),
('alto', 'arg'),
('upset', 'ana', [-1]),
('count', 'd', 5)],
[('ach cole', 'arg'),
('wrecked', 'ana', [-1]),
('something in the ear', 'd', 7)],
[('sat', 'arg'),
('up', 'rev', [-1]),
('interrupting', 'ins', [-1, 1]),
('siblings', 'syn'),
('balance', 'd', 6)]]


FUNCTIONS = {'ana': lambda x: ANAGRAMS[x], 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': lambda x: [''.join(reversed(x))]}

def solve_structured_clue(clue):
    definition, d, length = clue.pop([x[1] for x in clue].index('d'))
    groups_to_skip = set([])
    answer_subparts = [[] for x in clue]
    while any(s == [] for index, s in enumerate(answer_subparts) if index not in groups_to_skip):
        for i, group in enumerate(clue):
            phrase, kind = group[:2]
            if len(group) == 3:
                assert kind in FUNCTIONS
                arg_offsets = group[2]
                arg_indices = [i + x for x in arg_offsets]
                groups_to_skip.update(arg_indices)
                if any(answer_subparts[j] == [] for j in arg_indices):
                    continue
                arg_sets = tree_search([],
                                       [map(lambda x: [x], answer_subparts[ai]) for ai in arg_indices])
                for arg_set in arg_sets:
                    answer_subparts[i].extend(list(FUNCTIONS[kind](*arg_set)))
            elif kind == 'lit':
                answer_subparts[i] = [phrase]
            elif kind == 'arg':
                answer_subparts[i] = [phrase]
            elif kind == 'null':
                answer_subparts[i] = ['']
            elif kind == 'first':
                answer_subparts[i] = [phrase[0]]
            elif kind == 'syn':
                syns = SYNONYMS[phrase.replace(' ', '_')]
                answer_subparts[i] = list(syns)
    potential_answers = set(tree_search('', answer_subparts,
                                    lambda x: x not in groups_to_skip,
                                    lambda x: len(x) <= length and x in INITIAL_NGRAMS[len(x)]))
    answers = [(s, semantic_similarity(s, definition)) for s in potential_answers if s in WORDS and len(s) == length]
    return sorted(answers, key=lambda x: x[1], reverse=True)

for clue in clues:
    print clue
    print solve_structured_clue(clue)