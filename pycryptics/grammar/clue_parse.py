from pycryptics.grammar.cfg import generate_grammar
from pycryptics.grammar.memo_chart import MemoChart
from nltk import parse


def generate_clues(phrases):
    g = generate_grammar(phrases)
    parser = parse.EarleyChartParser(g, chart_class=MemoChart)
    return parser.nbest_parse(phrases)
    # return [clue_from_tree(t) for t in parser.nbest_parse(phrases)]
