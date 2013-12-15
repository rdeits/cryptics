from pycryptics.grammar.cfg import generate_grammar
from pycryptics.grammar.memo_chart import MemoChart
from nltk import parse


def generate_clues(constraints):
    g = generate_grammar(constraints.phrases)
    parser = parse.EarleyChartParser(g, chart_class=MemoChart)
    clues = parser.nbest_parse(constraints.phrases)
    for c in clues:
        c.set_constraints(constraints)
    return clues
