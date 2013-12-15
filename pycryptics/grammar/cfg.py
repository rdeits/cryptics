import nltk.grammar as gram
from pycryptics.utils.indicators import INDICATORS
from pycryptics.utils.transforms import lit_fun, null_fun, top_fun, syn_fun, first_fun
from pycryptics.utils.clue_funcs import all_legal_substrings, reverse, anagrams, all_insertions

"""
A Context Free Grammar (CFG) to describe allowed structures of cryptic crossword clues.
"""

RULES = {}

# The basic wordplay transforms
top = gram.Nonterminal('top')
RULES['top'] = top_fun
lit = gram.Nonterminal('lit')
RULES['lit'] = lit_fun
d = gram.Nonterminal('d')
RULES['d'] = null_fun
syn = gram.Nonterminal('syn')
RULES['syn'] = syn_fun
first = gram.Nonterminal('first')
RULES['first'] = first_fun
null = gram.Nonterminal('null')
RULES['null'] = null_fun

# Clue functions
ana = gram.Nonterminal('ana')
RULES['ana'] = anagrams
sub = gram.Nonterminal('sub')
RULES['sub'] = all_legal_substrings
ins = gram.Nonterminal('ins')
RULES['ins'] = all_insertions
rev = gram.Nonterminal('rev')
RULES['rev'] = reverse

# ana_, rev_, etc. are anagram/reversal/etc indicators,
# so they produce no text in the wordplay output
ana_ = gram.Nonterminal('ana_')
RULES['ana_'] = null_fun
sub_ = gram.Nonterminal('sub_')
RULES['sub_'] = null_fun
ins_ = gram.Nonterminal('ins_')
RULES['ins_'] = null_fun
rev_ = gram.Nonterminal('rev_')
RULES['rev_'] = null_fun

# All the *_arg elements just exist to make the production rules more clear
# so they just pass their inputs literally
clue_arg = gram.Nonterminal('clue_arg')
RULES['clue_arg'] = lit_fun
ins_arg = gram.Nonterminal('ins_arg')
RULES['ins_arg'] = lit_fun
ana_arg = gram.Nonterminal('ana_arg')
RULES['ana_arg'] = lit_fun
sub_arg = gram.Nonterminal('sub_arg')
RULES['sub_arg'] = lit_fun
rev_arg = gram.Nonterminal('rev_arg')
RULES['rev_arg'] = lit_fun

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
            for kind in INDICATORS:
                if any(w == p or (len(w) > 5 and abs(len(w) - len(p)) <= 3 and p.startswith(w[:-3])) for w in INDICATORS[kind]):
                    tags.append(gram.Nonterminal(kind))
                    found = True
            if not found:
                # tags = word_tags
                tags = [lit, d, syn, first, ana_, sub_, rev_]
        for t in tags:
            prods.append(gram.Production(t, [p]))
    return gram.ContextFreeGrammar(top, base_prods + prods)
