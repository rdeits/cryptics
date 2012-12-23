import nltk.grammar as cfg
from nltk import parse
from nltk.tree import Tree

"""
A Context Free Grammar (CFG) to describe allowed structures of cryptic crossword clues.
"""

cat = cfg.Nonterminal('cat')
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

clue_arg = cfg.Nonterminal('clue_arg')
clue_members = [lit, syn, first, null, ana, sub, ins, rev]

ins_arg = cfg.Nonterminal('ins_arg')
ins_members = [lit, ana, syn, sub, first, rev]

ana_arg = cfg.Nonterminal('ana_arg')
ana_members = [lit]

sub_arg = cfg.Nonterminal('sub_arg')
sub_members = [lit, syn, rev]

rev_arg = cfg.Nonterminal('rev_arg')
rev_members = [lit, syn]

known_functions = {
'in': [ins_, lit, null, sub_],
'a': [lit, syn, null],
'strange': [ana_, syn],
'broken': [ana_, syn],
'on_the_way_up': [rev_, syn],
'going_up': [rev_, syn],
'returning': [rev_, syn],
'is': [null, lit],
'for': [null, syn],
'large': [first, syn],
'hides': [sub_],
'primarily': [sub_],
'surface': [sub_],
'and': [null, lit]}


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

max_sub_parts = 3
base_clue_rules = [[clue_arg] * i for i in range(max_sub_parts + 1)]

base_clue_rules.extend([[null] + [first] * i for i in range(max_sub_parts + 1, 8)])
base_clue_rules.extend([[first] * i + [null] for i in range(max_sub_parts + 1, 8)])
clue_rules = []
for r in base_clue_rules:
    clue_rules.append(r + [d])
    clue_rules.append([d] + r)

production_rules = {
ins: [[ins_arg, ins_, ins_arg], [ins_arg, ins_arg, ins_]],
ana: [[ana_arg, ana_], [ana_, ana_arg]],
sub: [[sub_arg, sub_], [sub_, sub_arg]],
rev: [[rev_arg, rev_], [rev_, rev_arg]],
cat: clue_rules,
clue_arg: [[i] for i in clue_members],
ins_arg: [[i] for i in ins_members],
ana_arg: [[i] for i in ana_members],
sub_arg: [[i] for i in sub_members],
rev_arg: [[i] for i in rev_members]
}

base_prods = []

for n, rules in production_rules.items():
    for r in rules:
        base_prods.append(cfg.Production(n, r))


def clue_from_tree(tree):
    if not isinstance(tree, Tree):
        return tree
    elif "_arg" in tree.node:
        return clue_from_tree(tree[0])
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
    return cfg.ContextFreeGrammar(cat, base_prods + prods)


def generate_clues(phrases):
    g = generate_grammar(phrases)
    parser = parse.EarleyChartParser(g)
    return [clue_from_tree(t) for t in parser.nbest_parse(phrases)]
