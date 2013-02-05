from __future__ import division
from pycryptics.utils.transforms import TRANSFORMS
from pycryptics.utils.clue_funcs import FUNCTIONS
from pycryptics.utils.language import semantic_similarity
from pycryptics.utils.clue_parser import split_clue_text
from pycryptics.utils.phrasings import phrasings
from pycryptics.utils.productions import generate_productions
from collections import defaultdict

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
        d, (self._definition, null), null = clue[[x[0] for x in clue[1:]].index('d')+1]
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
    return tuple([a for a in arg_set if not a == ""])

def get_symbol(x):
    if hasattr(x, "symbol"):
        return x.symbol()
    else:
        return x

class ClueParser():
    def __init__(self, phrasing, memo):
        self.memo = memo
        self.phrasing = phrasing
        self.lengths = phrasing.lengths
        self.pattern = phrasing.pattern
        self.phrases = phrasing.phrases
        self.productions = generate_productions(phrasing.phrases)
        self.parsings = set([tuple([(p, (p,)) for p in phrasing.phrases[:-1]] + [('d', (phrasing.phrases[-1], phrasing.phrases[-1]), ("",))]),
                             tuple([('d', (phrasing.phrases[0], phrasing.phrases[0]), ("",))] + [(p, (p,)) for p in phrasing.phrases[1:]])])
        self.answers = []
        # self.prod_arg_map = defaultdict(lambda: [])
        # for prod in self.grammar.productions():
        #     key = tuple([get_symbol(n) for n in prod.rhs()])
        #     self.prod_arg_map[key].append(prod)
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
                dead_end = True
                # print "looking at parsing:", parsing
                if len(parsing) == 1 and parsing[0][0] == 'top':
                    # print "parsing is complete"
                    complete_parsings.add(parsing[0])
                else:
                    # print types
                    rules_to_apply = []
                    for prod in self.productions:
                        for (start, ind_pos, num_args) in prod.locate(parsing):
                            if prod.name == 'top':
                                if start != 0 or num_args != len(parsing):
                                    continue
                            rules_to_apply.append((prod, start, ind_pos, num_args))
                    for (prod, start, ind_pos, num_args) in rules_to_apply:
                        # print "applying rule:", prod
                        arg_sets = [[]]
                        for i in range(num_args):
                            if i == ind_pos:
                                continue
                            new_arg_sets = []
                            for s in arg_sets:
                                for a in parsing[start+i][-1]:
                                    new_arg_sets.append(s + [a])
                            arg_sets = new_arg_sets
                        # print "arg sets:", arg_sets
                        for s in arg_sets:
                            results = self.apply_rule(prod, s)
                            if results is not None:
                                solved_subclue = tuple((prod.name,) + parsing[start:start+num_args] + (results,))
                                new_parsing = parsing[:start] + (solved_subclue,) + parsing[start+num_args:]
                                dead_end = False
                                try:
                                    new_parsings.add(new_parsing)
                                except:
                                    import pdb; pdb.set_trace()
                                # print "added new parsing:", new_parsing
                    # if dead_end:
                    #     print "dead end parsing:", [p[0] for p in parsing]
            self.parsings = new_parsings
        for p in complete_parsings:
            self.answers.append(AnnotatedAnswer(p[-1][0], p))
        return self.answers

    def apply_rule(self, prod, args):
        filtered_args = arg_filter(args)
        memo_key = (prod.name, filtered_args)
        if memo_key in self.memo:
            results = self.memo[memo_key]
        else:
            results = RULES[prod.name](filtered_args, self.phrasing)
            self.memo[memo_key] = results
        return results



def parse_clue_text(clue_text):
    phrases, lengths, pattern, answer = split_clue_text(clue_text)
    return phrasings(phrases), lengths, pattern, answer

def solve_clue_text(clue_text):
    memo = dict([])
    answers = []
    phrasings, lengths, pattern, answer = parse_clue_text(clue_text)
    for p in phrasings:
        print p
        phrasing = Phrasing(p, lengths, pattern, answer)
        # g = cfg.generate_grammar(p)
        pc = ClueParser(phrasing, memo)
        pc.generate_answers()
        answers.extend(pc.answers)
    return sorted(answers, key=lambda x: x.similarity, reverse=True)

if __name__ == '__main__':
    # clue_text = "Initial meetings disappoint Rosemary internally (6)"
    # clue_text = "unsuitable paint smeared (5)"
    clue_text = "you finally beat iowa perfect world (6)"
    answers = solve_clue_text(clue_text)
    print "================================================="
    print ClueSolutions(answers).sorted_answers()
    for a in answers[:10]:
        print a