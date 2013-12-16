from nltk.parse.chart import Tree
from pycryptics.utils.transforms import valid_partial_answer


def arg_filter(arg_set):
    if arg_set != [""]:
        return [a for a in arg_set if not a == ""]
    return arg_set


class ClueUnsolvableError(Exception):
    pass


class ClueTree(Tree):
    """
    A tree data structure designed to reflect the CFG structure of a
    cryptic crossword clue, along with all of the mechanisms required
    to solve that clue and explain the answer
    """
    __slots__ = ['_answers', 'constraints']

    def __init__(self, node_or_str, children=None):
        self._answers = None
        self._constraints = None
        super(ClueTree, self).__init__(node_or_str, children)

    def __str__(self):
        child_strs = []
        for child in self:
            child_strs.append(str(child))
        return "({} {})".format(self.node.name, ' '.join(child_strs))

    def __repr__(self):
        return self.__str__()

    def set_constraints(self, constraints):
        self._constraints = constraints
        for c in self:
            if (not isinstance(c, str)) and c._constraints is None:
                c.set_constraints(constraints)

    def solve(self):
        child_answers = [ClueTree.get_answers(c) for c in self]
        for i, s in enumerate(child_answers):
            if isinstance(s, dict):
                child_answers[i] = s.keys()
        if self.node.name == 'top':
            arg_sets = self.make_top_arg_sets(child_answers)
        else:
            arg_sets = self.make_arg_sets(child_answers)
        if self._answers is None:
            self._answers = {}
        for args in arg_sets:
            answers = self.node.apply_rule(arg_filter(args), self._constraints)
            # answers = RULES[self.node](arg_filter(args), self._constraints)
            if answers is None:
                answers = []
            for ans in answers:
                self._answers[ans] = args[:]

    def make_top_arg_sets(self, child_answers):
        target_len = sum(self._constraints.lengths)
        arg_sets = [([], 0, '')]
        for ans_list in child_answers:
            new_arg_sets = []
            for ans in ans_list:
                for s in arg_sets:
                    candidate = (s[0] + [ans], s[1] + len(ans), s[2] + ans)
                    if valid_partial_answer(candidate[2], self._constraints):
                    # if candidate[1] <= target_len:
                        new_arg_sets.append(candidate)
            arg_sets = new_arg_sets
        return [s[0] for s in arg_sets if s[1] == target_len]

    def make_arg_sets(self, child_answers):
        # return itertools.product(*child_answers)
        arg_sets = [[]]
        for ans_list in child_answers:
            new_arg_sets = []
            for ans in ans_list:
                for s in arg_sets:
                    new_arg_sets.append(s + [ans])
            arg_sets = new_arg_sets
        return arg_sets

    @staticmethod
    def get_answers(tree_or_leaf):
        if isinstance(tree_or_leaf, str):
            return [tree_or_leaf]
        else:
            return tree_or_leaf.answers

    @property
    def answers(self):
        if self._answers is None:
            self._answers = {}
            self.solve()
        if self._answers == {}:
            raise ClueUnsolvableError("This clue has no solutions under the given constraints: " + str(self._constraints))
        return self._answers

    def derivation(self, answer):
        if self.node.is_argument:
            return self[0].derivation(self.answers[answer][0])
        result = "(" + self.node.name + " "
        arg_answers = self.answers[answer]
        for i, child in enumerate(self):
            if isinstance(child, basestring):
                result += '"' + child + '"'
            else:
                result += child.derivation(arg_answers[i])
            if i < len(self) - 1:
                result += " "
        if answer != "" and not any(answer == a for a in arg_answers):
            result += " -> " + answer.upper()
        result += ")"
        return result

    def long_derivation(self, answer, score=None):
        result = ""
        arg_answers = [a.encode('ascii', 'replace') for a in self.answers[answer]]
        if len(self) == 0:
            return result
        if len(self) == 1 and answer == arg_answers[0]:
            if isinstance(self[0], ClueTree):
                return self[0].long_derivation(arg_answers[0])
            else:
                return ""
        indicator = None
        for i, child in enumerate(self):
            if isinstance(child, basestring):
                continue
            if child.node.is_indicator:
            # if child.node.endswith('_'):
                indicator = child[0]
            else:
                result += child.long_derivation(arg_answers[i])
        if self.node.name != 'top':
            result += '\n'

        if indicator is not None and self.node.name != 'top':
            result += "'" + indicator + "' means to "
        non_empty_args = ["'" + a + "'" for a in arg_answers if a != ""]
        result += self.node.long_derivation(non_empty_args)
        # if self.node == 'rev':
        #     result += "reverse " + non_empty_args[0]
        # elif self.node == 'sub':
        #     result += "take a substring of " + non_empty_args[0]
        # elif self.node == 'ins':
        #     result += "insert " + non_empty_args[0] + " and " + non_empty_args[1]
        # elif self.node == 'ana':
        #     result += "anagram " + non_empty_args[0]
        # elif self.node == 'syn':
        #     result += "Take a synonym of " + non_empty_args[0]
        # elif self.node == 'first':
        #     result += "Take the first letter of " + non_empty_args[0]
        # elif self.node == 'null':
        #     result += non_empty_args[0] + " is a filler word."
        # elif self.node == 'd':
        #     result += non_empty_args[0] + " is the definition."
        # elif self.node == 'top' and len(non_empty_args) > 1:
        #     result += "\nCombine " + comma_list(map(str.upper, non_empty_args))

        if answer != "" and (self.node.name != 'top' or len(non_empty_args) > 1):
            result += " to get " + answer.upper() + "."

        if self.node.name == 'top' and score is not None:
            result += "\n" + answer.upper() + " matches "
            for child in self:
                if child.node.name == 'd':
                    result += "'" + child[0] + "'"
                    break
            result += " with confidence score {:.0%}.".format(score)
        return result


