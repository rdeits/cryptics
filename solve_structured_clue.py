from __future__ import division
from utils.language import all_legal_substrings, semantic_similarity, all_insertions, matches_pattern, string_reverse
from utils.ngrams import INITIAL_NGRAMS
from utils.words import WORDS
from utils.anagrams import cached_anagrams
from utils.synonyms import cached_synonyms
from utils.cryptics import compute_arg_offsets
from utils.kinds import generate_kinds
from utils.search import tree_search
import re

FUNCTIONS = {'ana': cached_anagrams, 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': string_reverse}

TRANSFORMS = {'lit': lambda x, l: [x.replace(' ', '').lower()],
              'null': lambda x, l: [''],
              'first': lambda x, l: [x[0].lower()],
              'syn': cached_synonyms}


def generate_structured_clues(phrases, length, pattern):
    return (zip(phrases, k) + [length, pattern] for k in generate_kinds(phrases))


def solve_structured_clue(clue):
    pattern = clue.pop()
    length = clue.pop()
    definition, d = clue.pop([x[1] for x in clue].index('d'))
    groups_to_skip = set([])
    answer_subparts = [[] for x in clue]
    count = 0
    while any(s == [] for s in answer_subparts) and count < 2:
        count += 1
        for i, group in enumerate(clue):
            if len(answer_subparts[i]) != 0:
                continue
            phrase, kind = group[:2]
            if kind[:3] in FUNCTIONS:
                func, arg_offsets = compute_arg_offsets(i, clue)
                arg_indices = [i + x for x in arg_offsets]
                groups_to_skip.update(arg_indices)
                if any(len(answer_subparts[j]) == 0 for j in arg_indices):
                    continue
                arg_sets = tree_search([],
                                       [answer_subparts[ai] for ai in arg_indices],
                                       combination_func=lambda s, w: s + [w])
                for arg_set in arg_sets:
                    arg_set += [length]
                    answer_subparts[i].extend(list(FUNCTIONS[func](*arg_set)))
            else:
                answer_subparts[i] = TRANSFORMS[kind](phrase, length)
            if len(answer_subparts[i]) == 0:
                return []
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
        new_answers = solve_structured_clue(clue[:])
        new_answers = [a for a in new_answers if a not in answers]
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


def parse_clue_text(clue_text):
    if '|' not in clue_text:
        clue_text += '| |'
    clue_text = clue_text.lower()
    clue, rest = clue_text.split('(')
    length, rest = rest.split(')')
    length = int(length)
    foo, pattern, answer = rest.split('|')
    pattern = pattern.strip()
    clue = re.sub(r'[^a-zA-Z\ _]', '', clue)
    clue = re.sub(r'\ +', ' ', clue)
    phrases = clue.split(' ')
    phrases = [p for p in phrases if p.strip() != '']
    phrases += [length, pattern]
    return phrases, answer


if __name__ == '__main__':
    for clue_text in open('clues/clues.txt', 'r').readlines():
        if clue_text.startswith('#'):
            continue
        phrases, answer = parse_clue_text(clue_text)
        print "Clue:", phrases
        print "Known answer:", answer
        answers = solve_phrases(phrases)[:15]
        for a in answers:
            print a
        print "\n"
