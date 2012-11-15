import nltk.grammar as cfg
from nltk import parse
from nltk.tree import Tree
from utils.search import tree_search


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

clue_members = [lit, syn, first, null, ana, sub, ins, rev]
ins_members = [lit, ana, syn, sub, first, rev]
ana_members = [lit]
sub_members = [lit, syn, rev]
word_tags = [lit, d, syn, first, null, ana_, sub_, ins_, rev_]

base_clue_rules = []
for i in range(1, 5):
    base_clue_rules.extend(tree_search([[]], [clue_members] * i,
                                  combination_func=lambda s, w: s + [w]))
clue_rules = []
for r in base_clue_rules:
    clue_rules.append(r + [d])
    clue_rules.append([d] + r)

production_rules = {
ins: tree_search([[]],
                 [ins_members, [ins_], ins_members],
                 combination_func=lambda s, w: s + [w]),
ana: [[lit, ana_], [ana_, lit]],
sub: (tree_search([[]],
                 [sub_members, [sub_]],
                 combination_func=lambda s, w: s + [w])
           + tree_search([[]],
                         [[sub_], sub_members],
                         combination_func=lambda s, w: s + [w])),
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
        for t in word_tags:
            prods.append(cfg.Production(t, [p]))
    return cfg.ContextFreeGrammar(clue, base_prods + prods)


def generate_clues(phrases):
    g = generate_grammar(phrases)
    parser = parse.ChartParser(g)
    return [clue_from_tree(t) for t in parser.nbest_parse(phrases)]
