import nltk.grammar as gram
import pycryptics.grammar.nodes as nd
from pycryptics.utils.indicators import INDICATORS

"""
A Context Free Grammar (CFG) to describe allowed substructures of cryptic crossword clues and how to solve each substructure.
"""

# The basic wordplay transforms
top = gram.Nonterminal(nd.TopNode)
lit = gram.Nonterminal(nd.LitNode)
d = gram.Nonterminal(nd.DNode)
syn = gram.Nonterminal(nd.SynNode)
first = gram.Nonterminal(nd.FirstNode)
null = gram.Nonterminal(nd.NullNode)

# Clue functions
ana = gram.Nonterminal(nd.AnaNode)
sub = gram.Nonterminal(nd.SubNode)
sub_init = gram.Nonterminal(nd.SubInitNode)
sub_final = gram.Nonterminal(nd.SubFinalNode)
ins = gram.Nonterminal(nd.InsNode)
rev = gram.Nonterminal(nd.RevNode)

# ana_, rev_, etc. are anagram/reversal/etc indicators,
# so they produce no text in the wordplay output
ana_ = gram.Nonterminal(nd.AnaIndNode)
sub_ = gram.Nonterminal(nd.SubIndNode)
sub_init_ = gram.Nonterminal(nd.SubInitIndNode)
sub_final_ = gram.Nonterminal(nd.SubFinalIndNode)
ins_ = gram.Nonterminal(nd.InsIndNode)
rev_ = gram.Nonterminal(nd.RevIndNode)
ind_nodes = [nd.AnaIndNode, nd.SubIndNode, nd.SubFinalIndNode, nd.SubInitIndNode, nd.InsIndNode, nd.RevIndNode]

# All the *_arg elements just exist to make the production rules more clear
# so they just pass their inputs literally
clue_arg = gram.Nonterminal(nd.ClueArgNode)
ins_arg = gram.Nonterminal(nd.InsArgNode)
ana_arg = gram.Nonterminal(nd.AnaArgNode)
sub_arg = gram.Nonterminal(nd.SubArgNode)
rev_arg = gram.Nonterminal(nd.RevArgNode)

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
                tags = [lit, d, syn, first, ana_, sub_, sub_init_, sub_final_, rev_]
        for t in tags:
            prods.append(gram.Production(t, [p]))
    return gram.ContextFreeGrammar(top, base_prods + prods)
