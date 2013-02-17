from __future__ import division
from pycryptics.utils.language import semantic_similarity
from pycryptics.utils.cfg import generate_clues
from pycryptics.utils.phrasings import phrasings
from pycryptics.utils.synonyms import SYNONYMS
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


class ClueSolutions:
    def __init__(self, anns):
        self.answer_scores = dict()
        self.answer_derivations = dict()
        for ann in anns:
            self.answer_derivations.setdefault(ann.answer, []).append(ann)
        for k, v in self.answer_derivations.items():
            self.answer_scores[k] = max(a.similarity for a in v)

    def sorted_answers(self):
        return sorted([(v, k) for k, v in self.answer_scores.items()], reverse=True)


class CrypticClueSolver(object):
    def __init__(self):
        self.running = False
        self.answers_with_clues = None
        self.clue_text = None
        self.total_phrasings = 0
        self.finished_phrasings = 0
        self.phrasing_clues = 0
        self.finished_phrasing_clues = 0

    @property
    def progress(self):
        if self.total_phrasings == 0 or self.phrasing_clues == 0:
            return None
        return self.finished_phrasings / self.total_phrasings + (self.finished_phrasing_clues / self.phrasing_clues) * 1 / (self.total_phrasings)

    def __enter__(self):
        self.start_go_server()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()
        self.stop_go_server()

    def start_go_server(self):
        self.go_proc = subprocess.Popen(['cryptics'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop_go_server(self):
        try:
            self.go_proc.stdin.write('..\n')
            self.go_proc.wait()
        except IOError:
            self.go_proc.kill()

    def stop(self):
        self.running = False

    def setup(self, clue_text):
        self.clue_text = clue_text

    def run(self):
        self.running = True
        self.clue_text = self.clue_text.encode('ascii', 'ignore')
        all_phrasings, lengths, pattern, answer = parse_clue_text(self.clue_text)
        self.total_phrasings = len(all_phrasings)
        self.finished_phrasings = 0
        self.answers_with_clues = []

        self.go_proc.stdin.write("# %s %s\n" % (lengths, pattern))
        print self.go_proc.stdout.readline()
        for p in all_phrasings:
            if not self.running:
                break
            print p
            for ann_ans in self.solve_phrasing(p):
                self.answers_with_clues.append(ann_ans)
            self.finished_phrasing_clues = 0
            self.finished_phrasings += 1
        if len(self.answers_with_clues) == 0 and pattern.replace('.', '') != "":
            self.answers_with_clues = [PatternAnswer(x, all_phrasings[0]) for x in SYNONYMS.keys() if matches_pattern(x, pattern, lengths)]
        self.answers_with_clues.sort(reverse=True)
        return self.answers_with_clues

    def solve_phrasing(self, phrasing):
        """
        Solve a clue which has been broken down into phrases, like:
        ['initially', 'babies', 'are', 'naked']
        """
        answers_with_clues = []
        possible_clues = list(generate_clues(phrasing))
        self.phrasing_clues = len(possible_clues)
        self.finished_phrasing_clues = 0

        for i, clue in enumerate(possible_clues):
            if not self.running:
                break
            self.go_proc.stdin.write(str(clue) + '\n')
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
            self.finished_phrasing_clues += 1
        return sorted(answers_with_clues, reverse=True)

    def collect_answers(self):
        if self.answers_with_clues is not None:
            return ClueSolutions(self.answers_with_clues)


def matches_pattern(word, pattern, lengths):
    return (tuple(len(x) for x in word.split('_')) == lengths) and re.match("^" + pattern + "$", word)


def split_clue_text(clue_text):
    if '|' not in clue_text:
        clue_text += ' |'
    clue_text = clue_text.lower()
    clue, paren, rest = clue_text.rpartition('(')
    lengths, rest = rest.split(')')
    lengths = lengths.replace('-', ',')
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

if __name__ == '__main__':
    clue = "initially babies are naked (4)"
    with CrypticClueSolver() as solver:
        solver.setup(clue)
        print solver.run()[0]
