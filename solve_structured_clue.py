from __future__ import division
from utils.language import all_legal_substrings, semantic_similarity, all_insertions, matches_pattern, string_reverse
from utils.ngrams import INITIAL_NGRAMS
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
              'first': lambda x, l: [x[0].lower()],
              'syn': cached_synonyms}


def generate_structured_clues(phrases, length, pattern):
    return (zip(phrases, k) + [length, pattern] for k in generate_kinds(phrases))


def find_skipped_groups(clue):
    groups_to_skip = set([])
    for i, group in enumerate(clue):
        phrase, kind = group
        if kind[:3] in FUNCTIONS:
            func, arg_offsets = compute_arg_offsets(i, clue)
            arg_indices = [i + x for x in arg_offsets]
            groups_to_skip.update(arg_indices)
    return groups_to_skip


def solve_structured_clue(clue):
    pattern = clue.pop()
    length = clue.pop()
    definition, d = clue.pop([x[1] for x in clue].index('d'))
    if len(clue) == 0:
        # this must be just a regular crossword clue (no wordplay)
        answers = [(s, semantic_similarity(s, definition)) for s in cached_synonyms(definition) if len(s) == length and matches_pattern(s, pattern)]
        return sorted(answers, key=lambda x: x[1], reverse=True)
    groups_to_skip = find_skipped_groups(clue)
    answer_subparts = [set([]) for x in clue]
    groups_added = 0
    active_set = set([''])
    count = 0
    while any(len(s) == 0 for s in answer_subparts) and count < 2:
        count += 1
        for i, group in enumerate(clue):
            if len(answer_subparts[i]) == 0:
                phrase, kind = group
                if kind[:3] in FUNCTIONS:
                    func, arg_offsets = compute_arg_offsets(i, clue)
                    arg_indices = [i + x for x in arg_offsets]
                    if any(len(answer_subparts[j]) == 0 for j in arg_indices):
                        continue
                    arg_sets = tree_search([[]],
                                           [answer_subparts[ai] for ai in arg_indices],
                                           combination_func=lambda s, w: s + [w])
                    for arg_set in arg_sets:
                        arg_set += [length]
                        answer_subparts[i].update(list(FUNCTIONS[func](*arg_set)))
                else:
                    answer_subparts[i] = set(TRANSFORMS[kind](phrase, length))
                if len(answer_subparts[i]) == 0:
                    return []
            # print "index and subparts", i, answer_subparts
            if all(len(s) > 0 for s in answer_subparts[:i + 1]) and i not in groups_to_skip:
                if i >= groups_added:
                    print "updating"
                    print "current active set:", active_set
                    print "branching list:", answer_subparts[groups_added:i+1]
                    active_set = set(tree_search(active_set, answer_subparts[groups_added:i + 1], lambda x: (x + groups_added) not in groups_to_skip, lambda x: len(x) <= length and x in INITIAL_NGRAMS[length][len(x)] and matches_pattern(x, pattern)))
                    print "new active set:", active_set
                    groups_added = i + 1
                if len(active_set) == 0:
                    return []

    # wordplay_answers = set(tree_search([''], answer_subparts,
    #                                 lambda x: x not in groups_to_skip,
    #                                 lambda x: len(x) <= length and x in INITIAL_NGRAMS[len(x)] and matches_pattern(x, pattern)))
    wordplay_answers = active_set
    answers = [(s, semantic_similarity(s, definition)) for s in wordplay_answers if s in WORDS and len(s) == length]
    return sorted(answers, key=lambda x: x[1], reverse=True)


def solve_phrasing(phrasing):
    pattern = phrasing.pop()
    length = phrasing.pop()
    answers = set([])
    answers_with_clues = []
    for clue in generate_structured_clues(phrasing, length, pattern):
        print clue
        new_answers = solve_structured_clue(clue[:])
        new_answers = [a for a in new_answers if a not in answers]
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
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


def solve_clue_text(clue_text):
    all_phrasings, answer = parse_clue_text(clue_text)
    answers = set([])
    answers_with_clues = []
    for p in all_phrasings:
        print p
        for ans, clue in solve_phrasing(p):
            if ans not in answers:
                answers.add(ans)
                answers_with_clues.append((ans, clue))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


if __name__ == '__main__':
    print solve_structured_clue([('bottomless', 'sub_r'), ('sea', 'lit'), ('stormy', 'ana_r'), ('sea', 'lit'), ('waters', 'lit'), ('surface', 'sub_l'), ('rises_and_falls', 'd'), 7, 's..s...'])
    # print solve_phrasing(['bottomless', 'sea', 'stormy', 'sea', 'waters', 'surface', 'rises_and_falls', 7, 's..s...'])
    # for clue in open('clues/clues.txt', 'r').readlines():
    #     print solve_clue_text(clue)[:15]
    #     break
