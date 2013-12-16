from pycryptics.utils.synonyms import cached_synonyms
from pycryptics.utils.transforms import valid_answer
from pycryptics.utils.clue_funcs import internal_substrings, reverse, anagrams, all_insertions, bigram_filter


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

