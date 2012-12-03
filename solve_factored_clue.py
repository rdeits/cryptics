from __future__ import division
from utils.language import semantic_similarity
from utils.cached_cfg import generate_cached_clues as generate_clues
from utils.phrasings import phrasings
from utils.crossword import split_words
import subprocess
import time
import re

global go_proc
go_proc = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def stop_go_server():
    global go_proc
    go_proc.stdin.write('.\n')
    go_proc.wait()


def solve_clue_text(clue_text):
    """
    Solve a raw clue, like
    Initially babies are naked (4) b... | BARE
    """
    clue_text = clue_text.encode('ascii', 'ignore')
    print "solving clue text"
    print clue_text
    # solved_parts = dict()
    all_phrasings, answer = parse_clue_text(clue_text)
    answers = set([])
    answers_with_clues = []

    go_proc.stdin.write("# %s %s\n" % (all_phrasings[0][-2], all_phrasings[0][-1]))
    print go_proc.stdout.readline()
    for p in all_phrasings:
        print p
        for ans, clue in solve_phrasing(p, go_proc):
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
    phrases = [p for p in phrases if p.strip() != '' and p.strip() != '_']
    all_phrasings = []
    for p in phrasings(phrases):
        p += [lengths, pattern]
        all_phrasings.append(p)
    return all_phrasings, answer


def solve_phrasing(phrasing, go_proc):
    """
    Solve a clue which has been broken down into phrases, like:
    ['initially', 'babies', 'are', 'naked', 4, 'b...']
    """
    pattern = phrasing.pop()
    lengths = phrasing.pop()
    answers = set([])
    answers_with_clues = []
    # now = time.time()
    possible_clues = generate_clues(phrasing)
    # print time.time() - now

    for i, clue in enumerate(possible_clues):
        d, definition = clue[[x[0] for x in clue].index('d')]
        go_proc.stdin.write(str(clue) + '\n')
        result = go_proc.stdout.readline()
        new_answers = eval(result)
        new_answers = ['_'.join(split_words(a, lengths)) for a in new_answers if a not in answers]
        new_answers = zip(new_answers, [semantic_similarity(a, definition) for a in new_answers])
        answers.update(new_answers)
        answers_with_clues.extend(zip(new_answers, [clue] * len(new_answers)))
    return sorted(answers_with_clues, key=lambda x: x[0][1], reverse=True)


if __name__ == '__main__':
    # print solve_phrasing(['small_bricks', 'included_among', 'durable_goods', 4, 'l...'])
    # print solve_factored_clue(('clue', ('sub', ('lit', 'significant_ataxia'), ('sub_', 'overshadows')), ('d', 'choral_piece')), (7,), '')
    print solve_clue_text(u'initially babies are naked (4)')
    # for clue in open('clues/clues.txt', 'r').readlines():
    #     print solve_clue_text(clue)[:1]
        # break
    stop_go_server()

