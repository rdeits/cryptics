from __future__ import division
from utils.language import semantic_similarity
from utils.cfg import generate_clues
from utils.phrasings import phrasings
import subprocess
import re

global go_proc
go_proc = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)


def stop_go_server():
    global go_proc
    go_proc.stdin.write('..\n')
    go_proc.wait()


class AnnotatedAnswer:
    def __init__(self, ans, clue):
        self.answer = ans
        self.clue = clue
        d, self.definition, null = clue[[x[0] for x in clue].index('d')]
        self.similarity = semantic_similarity(self.answer, self.definition)

    def __cmp__(self, other):
        return cmp((self.similarity, self.answer), (other.similarity, other.answer))

    def __str__(self):
        return str([self.answer, self.similarity, self.clue])


def solve_clue_text(clue_text):
    """
    Solve a raw clue, like
    Initially babies are naked (4) b... | BARE
    """
    clue_text = clue_text.encode('ascii', 'ignore')
    # solved_parts = dict()
    all_phrasings, answer = parse_clue_text(clue_text)
    answers_with_clues = []

    go_proc.stdin.write("# %s %s\n" % (all_phrasings[0][-2], all_phrasings[0][-1]))
    print go_proc.stdout.readline()
    for p in all_phrasings:
        print p
        for ann_ans in solve_phrasing(p, go_proc):
            answers_with_clues.append(ann_ans)
        answers_with_clues.sort(reverse=True)
        if len(answers_with_clues) > 0 and answers_with_clues[0].similarity > 0.85:
            return answers_with_clues
    return answers_with_clues


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
    clue = re.sub(r'[^a-zA-Z\ _0-9]', '', clue)
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
    answers_with_clues = []
    possible_clues = list(generate_clues(phrasing))

    for i, clue in enumerate(possible_clues):
        # print clue
        go_proc.stdin.write(str(clue) + '\n')
    go_proc.stdin.write('.\n')
    for i, x in enumerate(possible_clues):
        result = go_proc.stdout.readline()
        while result.strip() != ".":
            clue = eval(result)
            result = go_proc.stdout.readline()
            if clue == []:
                continue
            answer = clue[-1].lower()
            if answer in phrasing:
                continue
            answers_with_clues.append(AnnotatedAnswer(answer, clue))
    return sorted(answers_with_clues, reverse=True)


if __name__ == '__main__':
    # print solve_clue_text(u'spin broken shingle (7)')
    print solve_clue_text(u'youth climbing with ultimately good cheer (10) .d.......t')
    print solve_clue_text(u'youth climbing with ultimately good cheer (10) .d.......t')
    print solve_clue_text(u'youth climbing with ultimately good cheer (10) .d.......t')
    # for clue in open('clues/clues.txt', 'r').readlines():
    #     print solve_clue_text(clue)[:1]
        # break
    stop_go_server()

