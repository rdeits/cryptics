from __future__ import division
from utils.language import semantic_similarity
from utils.cfg import generate_clues
from utils.phrasings import phrasings
from utils.synonyms import SYNONYMS
import subprocess
import re


class AnnotatedAnswer:
    def __init__(self, ans, clue):
        self.answer = ans
        self.clue = clue
        d, self._definition, null = clue[[x[0] for x in clue].index('d')]
        self.similarity = semantic_similarity(self.answer, self._definition)

    def __cmp__(self, other):
        return cmp((self.similarity, self.answer), (other.similarity, other.answer))

    def __str__(self):
        return str([self.answer, self.similarity, self.clue])


class PatternAnswer(AnnotatedAnswer):
    def __init__(self, ans, phrasing):
        self.answer = ans
        self.similarity = max(semantic_similarity(ans, phrasing[0]),
                              semantic_similarity(ans, phrasing[-1]))
        self.clue = "???"


class CrypticClueSolver(object):
    def __init__(self):
        self.running = False
        self.answers_with_clues = None
        self.clue_text = None

    def __enter__(self):
        self.start_go_server()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.stop_go_server()

    def start_go_server(self):
        self.go_proc = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop_go_server(self):
        self.go_proc.stdin.write('..\n')
        self.go_proc.wait()

    def stop(self):
        self.running = False

    def run(self):
        self.running = True
        self.clue_text = self.clue_text.encode('ascii', 'ignore')
        # solved_parts = dict()
        all_phrasings, lengths, pattern, answer = parse_clue_text(self.clue_text)
        # all_phrasings, answer = parse_clue_text(self.clue_text)
        self.answers_with_clues = []

        self.go_proc.stdin.write("# %s %s\n" % (lengths, pattern))
        print self.go_proc.stdout.readline()
        for p in all_phrasings:
            if not self.running:
                self.stop_go_server()
                self.start_go_server()
                break
            print p
            for ann_ans in self.solve_phrasing(p):
                self.answers_with_clues.append(ann_ans)
            # if len(self.answers_with_clues) > 0 and self.answers_with_clues[0].similarity == 1:
            #     break
        if len(self.answers_with_clues) == 0:
            self.answers_with_clues = [PatternAnswer(x, all_phrasings[0]) for x in SYNONYMS.keys() if re.match("^" + pattern + "$", x)]
        self.answers_with_clues.sort(reverse=True)
        return self.answers_with_clues

    def solve_phrasing(self, phrasing):
        """
        Solve a clue which has been broken down into phrases, like:
        ['initially', 'babies', 'are', 'naked', 4, 'b...']
        """
        answers_with_clues = []
        possible_clues = list(generate_clues(phrasing))

        for i, clue in enumerate(possible_clues):
            self.go_proc.stdin.write(str(clue) + '\n')
        self.go_proc.stdin.write('.\n')
        for i, x in enumerate(possible_clues):
            result = self.go_proc.stdout.readline()
            while result.strip() != ".":
                clue = eval(result)
                result = self.go_proc.stdout.readline()
                if clue == []:
                    continue
                answer = clue[-1].lower()
                if answer in phrasing or any(x.startswith(answer) for x in phrasing):
                    continue
                answers_with_clues.append(AnnotatedAnswer(answer, clue))
        return sorted(answers_with_clues, reverse=True)


def split_clue_text(clue_text):
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
    return phrases, lengths, pattern, answer


def parse_clue_text(clue_text):
    phrases, lengths, pattern, answer = split_clue_text(clue_text)
    return phrasings(phrases), lengths, pattern, answer
