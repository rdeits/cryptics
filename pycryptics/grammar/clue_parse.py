from pycryptics.grammar.cfg import generate_grammar
from pycryptics.grammar.memo_chart import MemoChart
from nltk.parse.chart import Chart
from pycryptics.grammar.clue_tree import ClueTree
from nltk import parse


def generate_clues(constraints):
    g = generate_grammar(constraints.phrases)
    parser = parse.EarleyChartParser(g, chart_class=Chart)
    clues = parser.parse(constraints.phrases, tree_class=ClueTree)
    for c in clues:
        c.set_constraints(constraints)
    return clues
