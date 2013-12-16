import nltk.grammar as gram
from pycryptics.utils.indicators import INDICATORS
from pycryptics.utils.synonyms import cached_synonyms
from pycryptics.utils.transforms import valid_answer
from pycryptics.utils.clue_funcs import all_legal_substrings, reverse, anagrams, all_insertions

"""
A Context Free Grammar (CFG) to describe allowed substructures of cryptic crossword clues and how to solve each substructure.
"""


class BaseNode:
    """
    Each *Node class is a data structure which represents a single node
    in a parsed cryptic clue tree. That node must have a name, a method for
    applying its wordplay rule, and a (possibly empty) explanation string
    for its long derivation. These classes are just for conveniently
    defining and storing those methods for each type of node, and are
    never meant to be instantiated.
    """
    is_indicator = False
    is_argument = False
    name = "base"
    derivation_string = ""
    __slots__ = []

    @staticmethod
    def apply_rule(filtered_args, constraints):
        return [""]

    @classmethod
    def long_derivation(cls, non_empty_args):
        return cls.derivation_string.format(*non_empty_args)

def comma_list(args):
    result = ""
    for i, a in enumerate(args):
        result += a
        if i < len(args) - 1 and len(args) > 2:
            result += ","
        if i == len(args) - 2:
            result += " and "
        else:
            result += " "
    return result

class TopNode(BaseNode):
    name = 'top'

    @staticmethod
    def apply_rule(filtered_args, constraints):
        ans = "".join(filtered_args)
        is_valid, words = valid_answer(ans, constraints)
        if is_valid:
            return ['_'.join(words)]

    @staticmethod
    def long_derivation(non_empty_args):
        if len(non_empty_args) > 1:
            return "\nCombine " + comma_list(map(str.upper, non_empty_args))
        else:
            return ""

class LitNode(BaseNode):
    name = 'lit'

    @staticmethod
    def apply_rule(s, c):
        return s

class NullNode(BaseNode):
    name = 'null'
    derivation_string = "{} is a filler word"

class DNode(BaseNode):
    name = 'd'
    derivation_string = "{} is the definition"

class SynNode(BaseNode):
    name = 'syn'
    derivation_string = "Take a synonym of {}"

    @staticmethod
    def apply_rule(s, constraints):
        assert(len(s) == 1)
        return cached_synonyms(s[0], sum(constraints.lengths) + 2)

class FirstNode(BaseNode):
    name = 'first'
    derivation_string = "Take the first letter of {}"

    @staticmethod
    def apply_rule(s, c):
        assert(len(s) == 1)
        return [s[0][0]]

class AnaNode(BaseNode):
    name = 'ana'
    derivation_string = "anagram {}"

    @staticmethod
    def apply_rule(s, c):
        return anagrams(s, c)

class SubNode(BaseNode):
    name = 'sub'
    derivation_string = "take a substring of {}"

    @staticmethod
    def apply_rule(s, c):
        return all_legal_substrings(s, c)

class InsNode(BaseNode):
    name = 'ins'
    derivation_string = "insert {} and {}"

    @staticmethod
    def apply_rule(s, c):
        return all_insertions(s, c)

class RevNode(BaseNode):
    name = 'rev'
    derivation_string = "reverse {}"

    @staticmethod
    def apply_rule(s, c):
        return reverse(s, c)

class IndNode(BaseNode):
    is_indicator = True

class AnaIndNode(IndNode):
    name = 'ana_'

class SubIndNode(IndNode):
    name = 'sub_'

class InsIndNode(IndNode):
    name = 'ins_'

class RevIndNode(IndNode):
    name = 'rev_'

class ArgNode(BaseNode):
    is_argument = True

    @staticmethod
    def apply_rule(s, c):
        return s

class ClueArgNode(ArgNode):
    name = 'clue_arg'

class InsArgNode(ArgNode):
    name = 'ins_arg'

class AnaArgNode(ArgNode):
    name = 'ana_arg'

class SubArgNode(ArgNode):
    name = 'sub_arg'

class RevArgNode(ArgNode):
    name = 'rev_arg'


# The basic wordplay transforms
top = gram.Nonterminal(TopNode)
lit = gram.Nonterminal(LitNode)
d = gram.Nonterminal(DNode)
syn = gram.Nonterminal(SynNode)
first = gram.Nonterminal(FirstNode)
null = gram.Nonterminal(NullNode)

# Clue functions
ana = gram.Nonterminal(AnaNode)
sub = gram.Nonterminal(SubNode)
ins = gram.Nonterminal(InsNode)
rev = gram.Nonterminal(RevNode)

# ana_, rev_, etc. are anagram/reversal/etc indicators,
# so they produce no text in the wordplay output
ana_ = gram.Nonterminal(AnaIndNode)
sub_ = gram.Nonterminal(SubIndNode)
ins_ = gram.Nonterminal(InsIndNode)
rev_ = gram.Nonterminal(RevIndNode)

# All the *_arg elements just exist to make the production rules more clear
# so they just pass their inputs literally
clue_arg = gram.Nonterminal(ClueArgNode)
ins_arg = gram.Nonterminal(InsArgNode)
ana_arg = gram.Nonterminal(AnaArgNode)
sub_arg = gram.Nonterminal(SubArgNode)
rev_arg = gram.Nonterminal(RevArgNode)

production_rules = {
    ins: [[ins_arg, ins_, ins_arg], [ins_arg, ins_arg, ins_]],
    ana: [[ana_arg, ana_], [ana_, ana_arg]],
    sub: [[sub_arg, sub_], [sub_, sub_arg]],
    rev: [[rev_arg, rev_], [rev_, rev_arg]],
    clue_arg: [[lit], [syn], [first], [null], [ana], [sub], [ins], [rev]],
    ins_arg: [[lit], [ana], [syn], [sub], [first], [rev]],
    ana_arg: [[lit]],
    sub_arg: [[lit], [syn], [rev]],
    rev_arg: [[lit], [syn]],
    top: [[clue_arg, d],
          [clue_arg, clue_arg, d],
          [clue_arg, clue_arg, clue_arg, d],
          [d, clue_arg],
          [d, clue_arg, clue_arg],
          [d, clue_arg, clue_arg, clue_arg],
          ]
    }

additional_clue_rules = [[sub_] + [first] * i for i in range(3, 8)] + [[first] * i + [sub_] for i in range(3, 8)]
for r in additional_clue_rules:
    production_rules[top].append(r + [d])
    production_rules[top].append([d] + r)

base_prods = []
for n, rules in production_rules.items():
    for r in rules:
        base_prods.append(gram.Production(n, r))

known_functions = {'in': [ins_, lit, null, sub_],
                   'a': [lit, syn, null],
                   'is': [null, lit],
                   'for': [null, syn],
                   'large': [first, syn],
                   'primarily': [sub_],
                   'and': [null, lit],
                   'of': [null],
                   'on': [ins_, null, lit, syn],
                   'with': [null, ins_]}


def generate_grammar(phrases):
    prods = []
    for p in phrases:
        if p in known_functions:
            tags = known_functions[p]
        else:
            found = False
            tags = [lit, d, syn, first]
            ind_nodes = {'ana_': AnaIndNode,
                         'ins_': InsIndNode,
                         'rev_': RevIndNode,
                         'sub_': SubIndNode}
            for kind in INDICATORS:
                if any(w == p or (len(w) > 5 and abs(len(w) - len(p)) <= 3 and p.startswith(w[:-3])) for w in INDICATORS[kind]):
                    tags.append(gram.Nonterminal(ind_nodes[kind]))
                    found = True
            if not found:
                # tags = word_tags
                tags = [lit, d, syn, first, ana_, sub_, rev_]
        for t in tags:
            prods.append(gram.Production(t, [p]))
    return gram.ContextFreeGrammar(top, base_prods + prods)
