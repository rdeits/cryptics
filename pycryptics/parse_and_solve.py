from __future__ import division
import pycryptics.utils.cfg as cfg
from pycryptics.utils.transforms import TRANSFORMS
from pycryptics.utils.clue_funcs import FUNCTIONS
from pycryptics.utils.language import semantic_similarity
from pycryptics.utils.clue_parser import split_clue_text

RULES = TRANSFORMS
RULES.update(FUNCTIONS)

class Phrasing:
    def __init__(self, phrases, lengths, pattern, known_answer=None):
        self.phrases = phrases
        self.lengths = lengths
        self.pattern = pattern
        self.known_answer = known_answer

class AnnotatedAnswer:
    def __init__(self, ans, clue):
        self.answer = ans
        self.clue = clue
        d, (self._definition, null), null = clue[[x[0] for x in clue[1:]].index(cfg.d)+1]
        self.similarity = semantic_similarity(self.answer, self._definition)

    def __cmp__(self, other):
        return cmp((self.similarity, self.answer), (other.similarity, other.answer))

    def __str__(self):
        return str([self.answer, self.similarity, self.clue])

    def __repr__(self):
        return self.__str__()

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

def arg_filter(arg_set):
    return [a for a in arg_set if not a == ""]

class ClueParser():
    def __init__(self, phrasing, grammar):
        self.phrasing = phrasing
        self.lengths = phrasing.lengths
        self.pattern = phrasing.pattern
        self.phrases = phrasing.phrases
        self.grammar = grammar
        self.parsings = set([tuple([(p, (p,)) for p in phrases[:-1]] + [(cfg.d, (phrases[-1], phrases[-1]), ("",))]),
                             tuple([(cfg.d, (phrases[0], phrases[0]), ("",))] + [(p, (p,)) for p in phrases[1:]])])
        self.answers = []
        # self.parsings = [("*HEAD*", [""])] + self.parsings + [("*TAIL*", [""])]

    def generate_answers(self):
        """
        set parsings to the initial parse
        set new_parsings to []
        set finished_parsings to []

        while parsings is not empty:
            for each parsing in parsings:
                if parsing is finished:
                    add it to finished_parsings
                else:
                    for each rule in productions:
                        for each position in parsing:
                            if the rule fits:
                                for each argument:
                                    apply the rule
                                    create answers
                                    if there are any answers:
                                        create the solved factored clue
                                        create a new parsing with the input clues replaced by the solved clue
                                        add the new parsing to new_parsings
            parsings = new_parsings
        """
        self.answers = []
        complete_parsings = set([])
        while len(self.parsings) > 0:
            new_parsings = set([])
            for parsing in self.parsings:
                # print "looking at parsing:", parsing
                if len(parsing) == 1 and parsing[0][0] == cfg.top:
                    # print "parsing is complete"
                    complete_parsings.add(parsing[0])
                else:
                    types = [p[0] for p in parsing]
                    for prod in self.grammar.productions():
                        # print "checking rule:", prod
                        num_args = len(prod.rhs())
                        if prod.lhs() == cfg.top:
                            if num_args != len(parsing):
                                continue
                            else:
                                starts = [0]
                        else:
                            starts = range(len(parsing) - num_args + 1)
                        for pos in starts:
                            # print types[pos:pos+num_args], "?=", prod.rhs()
                            if tuple(types[pos:pos+num_args]) == prod.rhs():
                                arg_sets = [[]]
                                for i in range(num_args):
                                    new_arg_sets = []
                                    for s in arg_sets:
                                        for a in parsing[pos+i][-1]:
                                            new_arg_sets.append(s + [a])
                                    arg_sets = new_arg_sets
                                # print "arg sets:", arg_sets
                                for s in arg_sets:
                                    if prod.lhs() in RULES:
                                        results = RULES[prod.lhs()](arg_filter(s), self.phrasing)
                                        # print "results:", results
                                        if results is not None:
                                            solved_subclue = tuple((prod.lhs(),) + parsing[pos:pos+num_args] + (results,))
                                            new_parsing = parsing[:pos] + (solved_subclue,) + parsing[pos+num_args:]
                                            new_parsings.add(new_parsing)
                                            # print "added new parsing:", new_parsing
            self.parsings = new_parsings
        for p in complete_parsings:
            self.answers.append(AnnotatedAnswer(p[-1][0], p))
        return self.answers


if __name__ == '__main__':
    clue_text = "Stirs, spilling soda (4)"
    phrases, lengths, pattern, answer = split_clue_text(clue_text)
    phrasing = Phrasing(phrases, lengths, pattern, answer)
    g = cfg.generate_grammar(phrases)

    pc = ClueParser(phrasing,g)
    pc.generate_answers()
    print "============================================"
    print ClueSolutions(pc.answers).sorted_answers()
    for a in sorted(pc.answers, key=lambda x: x.similarity, reverse=True):
        print a