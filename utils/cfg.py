import nltk.grammar as cfg
from nltk import parse
from nltk.tree import Tree
from utils.search import tree_search

"""
A Context Free Grammar (CFG) to describe allowed structures of cryptic crossword clues.
"""

clue = cfg.Nonterminal('clue')
lit = cfg.Nonterminal('lit')
d = cfg.Nonterminal('d')
syn = cfg.Nonterminal('syn')
first = cfg.Nonterminal('first')
null = cfg.Nonterminal('null')
ana = cfg.Nonterminal('ana')
sub = cfg.Nonterminal('sub')
ins = cfg.Nonterminal('ins')
rev = cfg.Nonterminal('rev')
ana_ = cfg.Nonterminal('ana_')
sub_ = cfg.Nonterminal('sub_')
ins_ = cfg.Nonterminal('ins_')
rev_ = cfg.Nonterminal('rev_')


known_functions = {
'in': [ins_, lit, null, sub_],
'a': [lit, syn, null],
'strange': [ana_, syn],
'broken': [ana_, syn],
'on_the_way_up': [rev_, syn],
'going_up': [rev_, syn],
'returning': [rev_, syn]}


clue_members = [lit, syn, first, null, ana, sub, ins, rev]
ins_members = [lit, ana, syn, sub, first, rev]
ana_members = [lit]
sub_members = [lit, syn, rev]
rev_members = [lit, syn]
word_tags = [lit, d, syn, first, null, ana_, sub_, ins_, rev_]


def check_clue_totals(clue):
    if clue.count(ana) > 1:
        return False
    if clue.count(null) > 2:
        return False
    if all(c == null for c in clue):
        return False
    if clue.count('ins') > 1:
        return False
    return True

base_clue_rules = []
for i in range(1, 4):
    base_clue_rules.extend(tree_search([clue_members] * i,
                                       member_test=check_clue_totals))
clue_rules = []
for r in base_clue_rules:
    clue_rules.append(r + [d])
    clue_rules.append([d] + r)

production_rules = {
ins: tree_search([ins_members, [ins_], ins_members]),
ana: [[lit, ana_], [ana_, lit]],
sub: (tree_search([sub_members, [sub_]])
           + tree_search([[sub_], sub_members])),
rev: (tree_search([rev_members, [rev_]])
    + tree_search([[rev_], rev_members])),
clue: clue_rules
}

base_prods = []

for n, rules in production_rules.items():
    for r in rules:
        base_prods.append(cfg.Production(n, r))


def clue_from_tree(tree):
    if not isinstance(tree, Tree):
        return tree
    else:
        return tuple([tree.node] + [clue_from_tree(t) for t in tree])


def generate_grammar(phrases):
    prods = []
    for p in phrases:
        if p in known_functions:
            tags = known_functions[p]
        else:
            tags = word_tags
        for t in tags:
            prods.append(cfg.Production(t, [p]))
    return cfg.ContextFreeGrammar(clue, base_prods + prods)


def generate_clues(phrases):
    g = generate_grammar(phrases)
    parser = parse.EarleyChartParser(g)
    return [clue_from_tree(t) for t in parser.nbest_parse(phrases)]
