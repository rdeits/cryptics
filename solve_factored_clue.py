from __future__ import division
from utils.language import all_legal_substrings, semantic_similarity, all_insertions, matches_pattern, string_reverse
from utils.ngrams import INITIAL_NGRAMS
from utils.anagrams import cached_anagrams
from utils.synonyms import cached_synonyms, WORDS
from cryptic_cfg import generate_clues
from utils.search import tree_search
from utils.phrasings import phrasings
import re


FUNCTIONS = {'ana': cached_anagrams, 'sub': all_legal_substrings, 'ins': all_insertions, 'rev': string_reverse}

TRANSFORMS = {'lit': lambda x, l: [x.lower()],
              'null': lambda x, l: [''],
              'd': lambda x, l: [''],
              'first': lambda x, l: [x[0].lower()],
              'syn': cached_synonyms}

HEADS = ['ana_', 'sub_', 'ins_', 'rev_']


def solve_clue_text(clue_text):
    """
    Solve a raw clue, like
    Initially babies are naked (4) b... | BARE
    """
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
    """
    Solve a clue which has been broken down into phrases, like:
    ['initially', 'babies', 'are', 'naked', 4, 'b...']
    """
    pattern = phrasing.pop()
    length = phrasing.pop()
    answers = set([])
    answers_with_clues = []
    possible_clues = generate_clues(phrasing)

    def answer_test(ans):
        return ans in WORDS and len(ans) == length and matches_pattern(ans, pattern)
    for i, clue in enumerate(possible_clues):
        d, definition = clue[[x[0] for x in clue].index('d')]
        # print clue
        new_answers = solve_factored_clue(clue[:], length, pattern,
                                          solved_parts)
        new_answers = filter(answer_test, new_answers)
        new_answers = [a for a in new_answers if a not in answers]
        new_answers = zip(new_answers, [semantic_similarity(a, definition) for a in new_answers])
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


def solve_factored_clue(clue, length, pattern, solved_parts=dict()):
    if clue in solved_parts:
        return solved_parts[clue]
    if clue[0] in TRANSFORMS:
        result = set(TRANSFORMS[clue[0]](clue[1], length))
    elif clue[0] in FUNCTIONS:
        result = set([])
        arg_sets = tree_search([[]],
                               [solve_factored_clue(c, length, pattern, solved_parts) for c in clue[1:] if c[0] not in HEADS],
                               combination_func=lambda s, w: s + [w])
        for arg_set in arg_sets:
            arg_set += [length]
            result.update(FUNCTIONS[clue[0]](*arg_set))
    elif clue[0] == 'd':
        result = ['']
    elif clue[0] == 'clue':
        def member_test(x):
            return len(x) <= length and matches_pattern(x, pattern) and x in INITIAL_NGRAMS[length][len(x)]
        result = tree_search([''],
                           [solve_factored_clue(c, length, pattern, solved_parts) for c in clue[1:]],
                           member_test=member_test)
    else:
        import pdb; pdb.set_trace()
    solved_parts[clue] = result
    return result


if __name__ == '__main__':
    print solve_phrasing(['small_bricks', 'included_among', 'durable_goods', 4, 'l...'])
    # for clue in open('clues/clues.txt', 'r').readlines():
    #     print solve_clue_text(clue)[:15]
    #     break

