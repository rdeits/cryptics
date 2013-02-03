from __future__ import division
import pycryptics.utils.cfg as cfg
from pycryptics.utils.transforms import TRANSFORMS
from pycryptics.utils.language import semantic_similarity

RULES = TRANSFORMS

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

class ClueParser():
    def __init__(self, phrases, lengths, pattern, grammar):
        self.phrases = phrases
        self.lengths = lengths
        self.pattern = pattern
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
                                        results = RULES[prod.lhs()](s, self.lengths, self.pattern)
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
    phrases = "brass age ship".split(' ')
    g = cfg.generate_grammar(phrases)

    pc = ClueParser(phrases,(7,),"",g)
    print pc.parsings
    pc.generate_answers()
    print pc.answers