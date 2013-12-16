import nltk.grammar as gram
from pycryptics.utils.indicators import INDICATORS
from pycryptics.utils.synonyms import cached_synonyms
from pycryptics.utils.transforms import valid_answer
from pycryptics.utils.clue_funcs import internal_substrings, reverse, anagrams, all_insertions, bigram_filter

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
    derivation_string = "{} is a filler word."

class DNode(BaseNode):
    name = 'd'
    derivation_string = "{} is the definition."

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
        return internal_substrings(s, c)

class SubInitNode(BaseNode):
    name = 'sub_init'
    derivation_string = "take an initial substring of {}"

    @staticmethod
    def apply_rule(words, constraints):
        assert len(words) == 1
        word = words[0].lower().replace('_', "")
        length = sum(constraints.lengths)
        subs = set([])
        if len(word) <= 1:
            return subs
        for l in range(1, min(len(word), length + 1, 4)):
            subs.add(word[:l])
        if len(word) > 2:
            subs.add(word[:len(word)-1])
        return bigram_filter(subs, constraints)

class SubFinalNode(BaseNode):
    name = 'sub_final'
    derivation_string = "take a final substring of {}"

    @staticmethod
    def apply_rule(words, constraints):
        assert len(words) == 1
        word = words[0].lower().replace('_', "")
        subs = set([])
        if len(word) <= 1:
            return subs
        subs.add(word[1:])
        subs.add(word[-1:])
        return bigram_filter(subs, constraints)

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

class SubInitIndNode(IndNode):
    name = 'sub_init_'

class SubFinalIndNode(IndNode):
    name = 'sub_final_'

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
sub_init = gram.Nonterminal(SubInitNode)
sub_final = gram.Nonterminal(SubFinalNode)
ins = gram.Nonterminal(InsNode)
rev = gram.Nonterminal(RevNode)

# ana_, rev_, etc. are anagram/reversal/etc indicators,
# so they produce no text in the wordplay output
ana_ = gram.Nonterminal(AnaIndNode)
sub_ = gram.Nonterminal(SubIndNode)
sub_init_ = gram.Nonterminal(SubInitIndNode)
sub_final_ = gram.Nonterminal(SubFinalIndNode)
ins_ = gram.Nonterminal(InsIndNode)
rev_ = gram.Nonterminal(RevIndNode)
ind_nodes = [AnaIndNode, SubIndNode, SubFinalIndNode, SubInitIndNode, InsIndNode, RevIndNode]

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
    sub_init: [[sub_arg, sub_init_], [sub_init_, sub_arg]],
    sub_final: [[sub_arg, sub_final_], [sub_final_, sub_arg]],
    rev: [[rev_arg, rev_], [rev_, rev_arg]],
    clue_arg: [[lit], [syn], [first], [null], [ana], [sub], [ins], [rev], [sub_init], [sub_final]],
    ins_arg: [[lit], [ana], [syn], [sub], [sub_init], [sub_final], [first], [rev]],
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

additional_clue_rules = [[sub_init_] + [first] * i for i in range(3, 8)] + [[first] * i + [sub_init_] for i in range(3, 8)]
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
                   'primarily': [sub_init_],
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
            for ind in ind_nodes:
                if any(w == p or (len(w) > 5 and abs(len(w) - len(p)) <= 3 and p.startswith(w[:-3])) for w in INDICATORS[ind.name]):
                    tags.append(gram.Nonterminal(ind))
                    found = True
            if not found:
                # tags = word_tags
                tags = [lit, d, syn, first, ana_, sub_, sub_init_, sub_final_, rev_]
        for t in tags:
            prods.append(gram.Production(t, [p]))
    return gram.ContextFreeGrammar(top, base_prods + prods)
