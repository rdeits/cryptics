from __future__ import division
import re

def semantic_similarity(foo, bar):
    return 1

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

def split_clue_text(clue_text):
    if '|' not in clue_text:
        clue_text += ' |'
    clue_text = clue_text.lower()
    clue, rest = clue_text.split('(')
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


class FakeCrypticClueSolver(CrypticClueSolver):
    def __init__(self):
        self.running = False
        self.answers_with_clues = None
        self.clue_text = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def setup(self, clue_text):
        self.clue_text = clue_text

    def run(self):
        self.answers_with_clues = [
['bare', 1, ('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')],
['bare', 1, ('top', ('sub', ('sub_', 'initially', ''), ('syn', 'babies', 'BABE'), 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')],
['bare', 1, ('top', ('null', 'initially', ''), ('first', 'babies', 'B'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'BARE')],
['nude', 0.675, ('top', ('d', 'initially_babies', ''), ('null', 'are', ''), ('syn', 'naked', ''), 'NUDE')],
['nude', 0.675, ('top', ('d', 'initially_babies', ''), ('sub', ''), 'NUDE')],
['evil', 0.6, ('top', ('d', 'initially_babies', ''), ('rev', ''), 'EVIL')],
['bare', 0.5625, ('top', ('d', 'initially_babies_are', ''), ('syn', 'naked', ''), 'BARE')],
['open', 0.5, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('sub', ('sub_', 'are', ''), ('syn', 'naked', 'OPEN'), 'OPEN'), 'OPEN')],
['open', 0.5, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('null', 'are', ''), ('syn', 'naked', 'OPEN'), 'OPEN')],
['open', 0.5, ('top', ('d', 'initially', ''), ('null', 'babies_are', ''), ('syn', 'naked', ''), 'OPEN')],
['open', 0.5, ('top', ('d', 'initially', ''), ('sub', ''), 'OPEN')],
['live', 0.5, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('sub', ('syn', 'are', ''), ('sub_', 'naked', 'LIVE'), 'LIVE'), 'LIVE')],
['live', 0.5, ('top', ('null', 'initially', ''), ('null', 'babies', ''), ('syn', 'are', 'LIVE'), ('d', 'naked', ''), 'LIVE')],
['live', 0.5, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('syn', 'are', 'LIVE'), ('null', 'naked', ''), 'LIVE')],
['live', 0.5, ('top', ('d', 'initially', ''), ('sub', ''), ('null', 'naked', 'LIVE'), 'LIVE')],
['live', 0.5, ('top', ('null', 'initially', ''), ('sub', ('sub_', 'babies', ''), ('syn', 'are', 'LIVE'), 'LIVE'), ('d', 'naked', ''), 'LIVE')],
['live', 0.5, ('top', ('null', 'initially_babies', ''), ('syn', 'are', ''), ('d', 'naked', 'LIVE'), 'LIVE')],
['live', 0.5, ('top', ('sub', ''), ('d', 'naked', 'LIVE'), 'LIVE')],
['bear', 0.5, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('ana', ('lit', 'are', 'ARE'), ('ana_', 'naked', ''), 'EAR'), 'BEAR')],
['bear', 0.5, ('top', ('sub', ('sub_', 'initially', ''), ('syn', 'babies', 'BABE'), 'BE'), ('syn', 'are', 'AR'), ('d', 'naked', ''), 'BEAR')],
['open', 0.45, ('top', ('d', 'initially_babies_are', ''), ('syn', 'naked', ''), 'OPEN')],
['open', 0.4235294117647059, ('top', ('d', 'initially_babies', ''), ('null', 'are', ''), ('syn', 'naked', ''), 'OPEN')],
['open', 0.4235294117647059, ('top', ('d', 'initially_babies', ''), ('sub', ''), 'OPEN')],
['earn', 0.4, ('top', ('d', 'initially', ''), ('ana', ('ana_', 'babies', ''), ('lit', 'are', 'ARE'), 'EAR'), ('first', 'naked', 'N'), 'EARN')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('lit', 'are', 'ARE'), ('null', 'naked', ''), 'BARE')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('sub', ('sub_', 'are', ''), ('syn', 'naked', 'BARE'), 'BARE'), 'BARE')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('sub', ('sub_', 'are', ''), ('syn', 'naked', 'BARE'), 'ARE'), 'BARE')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('null', 'are', ''), ('syn', 'naked', 'BARE'), 'BARE')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('null', 'babies_are', ''), ('syn', 'naked', ''), 'BARE')],
['bare', 0.4, ('top', ('d', 'initially', ''), ('sub', ''), 'BARE')],
['bake', 0.4, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('sub', ('sub_', 'are', ''), ('lit', 'naked', 'NAKED'), 'AKE'), 'BAKE')],
['bare', 0.36000000000000004, ('top', ('d', 'initially_babies', ''), ('null', 'are', ''), ('syn', 'naked', ''), 'BARE')],
['bare', 0.36000000000000004, ('top', ('d', 'initially_babies', ''), ('sub', ''), 'BARE')],
['ally', 0.2857142857142857, ('top', ('sub', ('lit', 'initially', 'INITIALLY'), ('sub_', 'babies', ''), 'ALLY'), ('null', 'are', ''), ('d', 'naked', ''), 'ALLY')],
['ally', 0.2857142857142857, ('top', ('sub', 'ALLY'), ('d', 'naked', ''), 'ALLY')],
['ally', 0.2857142857142857, ('top', ('sub', ('lit', 'initially_babies', 'INITIALLY_BABIES'), ('sub_', 'are', ''), 'ALLY'), ('d', 'naked', ''), 'ALLY')],
['nude', 0.2571428571428571, ('top', ('d', 'initially_babies_are', ''), ('syn', 'naked', ''), 'NUDE')],
['live', 0.2571428571428571, ('top', ('d', 'initially_babies', ''), ('sub', 'LIVE'), 'LIVE')],
['live', 0.2571428571428571, ('top', ('d', 'initially_babies', ''), ('syn', 'are', ''), ('null', 'naked', 'LIVE'), 'LIVE')],
['ally', 0.2571428571428571, ('top', ('sub', 'ALLY'), ('d', 'are_naked', ''), 'ALLY')],
['yare', 0, ('top', ('sub', ('lit', 'initially', 'INITIALLY'), ('sub_', 'babies', ''), 'Y'), ('lit', 'are', 'ARE'), ('d', 'naked', ''), 'YARE')],
['rena', 0, ('top', ('d', 'initially', ''), ('sub', ('sub_', 'babies', ''), ('lit', 'are_naked', 'ARE_NAKED'), 'RENA'), 'RENA')],
['rean', 0, ('top', ('d', 'initially', ''), ('ana', ('ana_', 'babies', ''), ('lit', 'are', 'ARE'), 'REA'), ('first', 'naked', 'N'), 'REAN')],
['nude', 0, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('sub', ('sub_', 'are', ''), ('syn', 'naked', 'NUDE'), 'NUDE'), 'NUDE')],
['nude', 0, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('null', 'are', ''), ('syn', 'naked', 'NUDE'), 'NUDE')],
['nude', 0, ('top', ('d', 'initially', ''), ('null', 'babies_are', ''), ('syn', 'naked', ''), 'NUDE')],
['nude', 0, ('top', ('d', 'initially', ''), ('sub', ''), 'NUDE')],
['lait', 0, ('top', ('sub', ('rev', ('lit', 'initially', 'INITIALLY'), ('rev_', 'babies', ''), 'YLLAITINI'), ('sub_', 'are', ''), 'LAIT'), ('d', 'naked', ''), 'LAIT')],
['iyar', 0, ('top', ('sub', ('lit', 'initially', 'INITIALLY'), ('sub_', 'babies', ''), 'IY'), ('syn', 'are', 'AR'), ('d', 'naked', ''), 'IYAR')],
['irae', 0, ('top', ('first', 'initially', 'I'), ('ana', ('ana_', 'babies', ''), ('lit', 'are', 'ARE'), 'RAE'), ('d', 'naked', ''), 'IRAE')],
['inia', 0, ('top', ('sub', ('lit', 'initially', 'INITIALLY'), ('sub_', 'babies', ''), 'INI'), ('first', 'are', 'A'), ('d', 'naked', ''), 'INIA')],
['evil', 0, ('top', ('null', 'initially', ''), ('rev', ('rev_', 'babies', ''), ('syn', 'are', 'LIVE'), 'EVIL'), ('d', 'naked', ''), 'EVIL')],
['evil', 0, ('top', ('d', 'initially', ''), ('rev', ('rev_', 'babies', ''), ('syn', 'are', 'LIVE'), 'EVIL'), ('null', 'naked', ''), 'EVIL')],
['evil', 0, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('rev', ('syn', 'are', 'LIVE'), ('rev_', 'naked', ''), 'EVIL'), 'EVIL')],
['evil', 0, ('top', ('sub', ('sub_', 'initially', ''), ('rev', ('rev_', 'babies', ''), ('syn', 'are', 'LIVE'), 'EVIL'), 'EVIL'), ('d', 'naked', ''), 'EVIL')],
['evil', 0, ('top', ('d', 'initially', ''), ('sub', ('sub_', 'babies', ''), ('rev', ('syn', 'are', ''), ('rev_', 'naked', 'LIVE'), 'EVIL'), 'EVIL'), 'EVIL')],
['evil', 0, ('top', ('d', 'initially', ''), ('sub', ('rev', ('rev_', 'babies', ''), ('syn', 'are', 'LIVE'), 'EVIL'), ('sub_', 'naked', ''), 'EVIL'), 'EVIL')],
['dean', 0, ('top', ('d', 'initially', ''), ('sub', ('sub_', 'babies', ''), ('rev', ('rev_', 'are', ''), ('lit', 'naked', 'NAKED'), 'DEKAN'), 'DEAN'), 'DEAN')],
['brea', 0, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('ana', ('lit', 'are', 'ARE'), ('ana_', 'naked', ''), 'REA'), 'BREA')],
['braw', 0, ('top', ('d', 'initially', ''), ('sub', ('lit', 'babies', ''), ('sub_', 'are', 'BABIES'), 'B'), ('syn', 'naked', 'RAW'), 'BRAW')],
['braw', 0, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('null', 'are', ''), ('syn', 'naked', 'RAW'), 'BRAW')],
['braw', 0, ('top', ('d', 'initially', ''), ('sub', ('syn', 'babies', 'BABE'), ('sub_', 'are', ''), 'B'), ('syn', 'naked', 'RAW'), 'BRAW')],
['braw', 0, ('top', ('d', 'initially', ''), ('first', 'babies_are', 'B'), ('syn', 'naked', 'RAW'), 'BRAW')],
['brae', 0, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('ana', ('lit', 'are', 'ARE'), ('ana_', 'naked', ''), 'RAE'), 'BRAE')],
['barn', 0, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('syn', 'are', 'AR'), ('first', 'naked', 'N'), 'BARN')],
['baer', 0, ('top', ('d', 'initially', ''), ('first', 'babies', 'B'), ('ana', ('lit', 'are', 'ARE'), ('ana_', 'naked', ''), 'AER'), 'BAER')],
['babe', 0, ('top', ('null', 'initially', ''), ('syn', 'babies', 'BABE'), ('null', 'are', ''), ('d', 'naked', ''), 'BABE')],
['babe', 0, ('top', ('d', 'initially', ''), ('sub', ('syn', 'babies', ''), ('sub_', 'are', 'BABE'), 'BABE'), ('null', 'naked', ''), 'BABE')],
['babe', 0, ('top', ('d', 'initially', ''), ('syn', 'babies', 'BABE'), ('null', 'are', ''), ('null', 'naked', ''), 'BABE')],
['babe', 0, ('top', ('null', 'initially', ''), ('sub', ('syn', 'babies', ''), ('sub_', 'are', 'BABE'), 'BABE'), ('d', 'naked', ''), 'BABE')],
['babe', 0, ('top', ('sub', ('sub_', 'initially', ''), ('syn', 'babies', 'BABE'), 'BABE'), ('null', 'are', ''), ('d', 'naked', ''), 'BABE')],
['babe', 0, ('top', ('null', 'initially', ''), ('syn', 'babies', 'BABE'), ('d', 'are_naked', ''), 'BABE')],
['babe', 0, ('top', ('sub', 'BABE'), ('d', 'are_naked', ''), 'BABE')],
['babe', 0, ('top', ('d', 'initially', ''), ('syn', 'babies', 'BABE'), ('null', 'are_naked', ''), 'BABE')],
['babe', 0, ('top', ('d', 'initially', 'BABE'), ('sub', ''), 'BABE')],
['baba', 0, ('top', ('sub', ('sub_', 'initially', ''), ('syn', 'babies', 'BABE'), 'BAB'), ('first', 'are', 'A'), ('d', 'naked', ''), 'BABA')],
['baba', 0, ('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'BAB'), ('first', 'are', 'A'), ('d', 'naked', ''), 'BABA')],
['aked', 0, ('top', ('d', 'initially', ''), ('null', 'babies', ''), ('sub', ('sub_', 'are', ''), ('lit', 'naked', 'NAKED'), 'AKED'), 'AKED')],
['aked', 0, ('top', ('d', 'initially', ''), ('sub', ('sub_', 'babies', ''), ('lit', 'are_naked', 'ARE_NAKED'), 'AKED'), 'AKED')],
['aked', 0, ('top', ('d', 'initially', ''), ('sub', ''), 'AKED')],
['aked', 0, ('top', ('d', 'initially_babies', ''), ('sub', ''), 'AKED')],
['abie', 0, ('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies', 'BABIES'), 'ABIE'), ('null', 'are', ''), ('d', 'naked', ''), 'ABIE')],
['abie', 0, ('top', ('d', 'initially', 'ABIE'), ('sub', ''), ('null', 'naked', ''), 'ABIE')],
['abie', 0, ('top', ('null', 'initially', ''), ('sub', ('lit', 'babies', 'BABIES'), ('sub_', 'are', ''), 'ABIE'), ('d', 'naked', ''), 'ABIE')],
['abie', 0, ('top', ('sub', ''), ('d', 'are_naked', 'ABIE'), 'ABIE')],
['abie', 0, ('top', ('d', 'initially', ''), ('sub', 'ABIE'), 'ABIE')],
['abie', 0, ('top', ('sub', ('sub_', 'initially', ''), ('lit', 'babies_are', 'BABIES_ARE'), 'ABIE'), ('d', 'naked', ''), 'ABIE')],
['abie', 0, ('top', ('d', 'initially', ''), ('sub', ('lit', 'babies_are', ''), ('sub_', 'naked', 'BABIES_ARE'), 'ABIE'), 'ABIE')],
['abie', 0, ('top', ('sub', ('lit', 'initially_babies', 'INITIALLY_BABIES'), ('sub_', 'are', ''), 'ABIE'), ('d', 'naked', ''), 'ABIE')]]
        for i, a in enumerate(self.answers_with_clues):
            self.answers_with_clues[i] = AnnotatedAnswer(a[0], a[-1])
