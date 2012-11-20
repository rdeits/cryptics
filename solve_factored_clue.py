from __future__ import division
from utils.language import all_legal_substrings, semantic_similarity, all_insertions, string_reverse
from utils.ngrams import INITIAL_NGRAMS
from utils.anagrams import cached_anagrams
from utils.synonyms import cached_synonyms, WORDS
from utils.cfg import generate_clues
from utils.search import tree_search
from utils.phrasings import phrasings
from utils.crossword import answer_test, partial_answer_test, split_words
import time
import re


class ClueUnsolvableError(Exception):
    def __init__(self, clue):
        self.clue = clue

    def __str__(self):
        print self.clue

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
    lengths, rest = rest.split(')')
    lengths = tuple(int(x) for x in lengths.split(','))
    pattern, answer = rest.split('|')
    pattern = pattern.strip()
    assert len(pattern) == 0 or len(pattern) == sum(lengths), "Answer lengths and length of pattern string must match: sum(%s) != %d" % (lengths, len(pattern))
    clue = re.sub('-', '_', clue)
    clue = re.sub(r'[^a-zA-Z\ _]', '', clue)
    clue = re.sub(r'\ +', ' ', clue)
    phrases = clue.split(' ')
    phrases = [p for p in phrases if p.strip() != '']
    all_phrasings = []
    for p in phrasings(phrases):
        p += [lengths, pattern]
        all_phrasings.append(p)
    return all_phrasings, answer


def solve_phrasing(phrasing, solved_parts=dict()):
    """
    Solve a clue which has been broken down into phrases, like:
    ['initially', 'babies', 'are', 'naked', 4, 'b...']
    """
    pattern = phrasing.pop()
    lengths = phrasing.pop()
    answers = set([])
    answers_with_clues = []
    now = time.time()
    possible_clues = generate_clues(phrasing)
    print time.time() - now

    for i, clue in enumerate(possible_clues):
        d, definition = clue[[x[0] for x in clue].index('d')]
        # print clue
        try:
            new_answers = solve_factored_clue(clue[:], lengths, pattern,
                                              solved_parts)
        except ClueUnsolvableError:
            # Clue was unsolvable, so skip it
            continue
        new_answers = filter(lambda ans: answer_test(ans, lengths, pattern, WORDS), new_answers)
        new_answers = ['_'.join(split_words(a, lengths)) for a in new_answers if a not in answers]
        new_answers = zip(new_answers, [semantic_similarity(a, definition) for a in new_answers])
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


def solve_factored_clue(clue, lengths, pattern, solved_parts=dict()):
    length = sum(lengths)
    if clue in solved_parts:
        result = solved_parts[clue]
    else:
        if clue[0] in TRANSFORMS:
            result = set(TRANSFORMS[clue[0]](clue[1], length))
        elif clue[0] in FUNCTIONS:
            result = set([])
            arg_sets = tree_search([solve_factored_clue(c, lengths, pattern, solved_parts) for c in clue[1:] if c[0] not in HEADS])
            for arg_set in arg_sets:
                arg_set += [length]
                result.update(FUNCTIONS[clue[0]](*arg_set))
        elif clue[0] == 'd':
            result = ['']
        elif clue[0] == 'clue':
            def member_test(x):
                return partial_answer_test(x, lengths, pattern, INITIAL_NGRAMS)
            result = tree_search([map(lambda x: x.replace('_', ''),
                                      solve_factored_clue(c, lengths, pattern, solved_parts)) for c in clue[1:]],
                                 start=[''], member_test=member_test)
        else:
            raise ValueError('Unrecognized clue: %s' % clue)
    solved_parts[clue] = result
    # print clue, result
    if len(result) == 0:
        raise ClueUnsolvableError(clue)
    return result


if __name__ == '__main__':
    # print solve_phrasing(['small_bricks', 'included_among', 'durable_goods', 4, 'l...'])
    # print solve_factored_clue(('clue', ('sub', ('lit', 'significant_ataxia'), ('sub_', 'overshadows')), ('d', 'choral_piece')), (7,), '')
    # print solve_clue_text('small_bricks small_bricks (5, 6)')
    for clue in open('clues/clues.txt', 'r').readlines():
        print solve_clue_text(clue)[:1]
        # break

