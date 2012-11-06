from __future__ import division
import sys
from load_utils import load_words, load_initial_ngrams, load_anagrams, load_synonyms
from language_utils import anagrams, synonyms, all_legal_substrings, semantic_similarity, all_insertions, AnagramDict

WORDS = load_words()
INITIAL_NGRAMS = load_initial_ngrams()
ANAGRAMS = AnagramDict(load_anagrams())
SYNONYMS = load_synonyms()

clues = [[('initially', 'sub', [1]),
('babies', 'arg'),
('are', 'lit'),
('naked', 'd')],
[('tenor', 'first'),
('and', 'null'),
('alto', 'arg'),
('upset', 'ana', [-1]),
('count', 'd')],
[('ach cole', 'arg'),
('wrecked', 'ana', [-1]),
('something in the ear', 'd')],
[('sat', 'arg'),
('up', 'rev', [-1]),
('interrupting', 'ins', [-1, 1]),
('siblings', 'syn'),
('balance', 'd')]]


FUNCTIONS = {'ana': lambda x: ANAGRAMS[x], 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': lambda x: reversed(x)}

def solve_structured_clue(clue):
    definition = clue.pop([x[1] for x in clue].index('d'))[0]
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
                arg_sets = [[]]
                for ai in arg_indices:
                    new_arg_sets = []
                    for arg_set in arg_sets:
                        for s in answer_subparts[ai]:
                            new_arg_sets.append(arg_set + [s])
                    arg_sets = new_arg_sets
                for arg_set in arg_sets:
                    answer_subparts[i] = FUNCTIONS[kind](*arg_set)
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
    active_set = ['']
    for i, part in enumerate(answer_subparts):
        if i in groups_to_skip:
            continue
        new_active_set = []
        for s in active_set:
            for w in part:
                candidate = s + w
                if candidate in INITIAL_NGRAMS[len(candidate)]:
                    new_active_set.append(candidate)
        active_set = new_active_set
    answers = [(s, semantic_similarity(s, definition)) for s in active_set if s in WORDS]
    return sorted(answers, key=lambda x: x[1], reverse=True)

for clue in clues:
    print clue
    print solve_structured_clue(clue)