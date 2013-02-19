import nltk.parse as parse
import nltk.grammar as grammar
from pycryptics.grammar.memo_chart import MemoChart

top = grammar.Nonterminal('top')
bar = grammar.Nonterminal('bar')
baz = grammar.Nonterminal('baz')
foo = grammar.Nonterminal('foo')

prods = [grammar.Production(top, [bar]), grammar.Production(top, [baz]), grammar.Production(bar, [foo]), grammar.Production(baz, [foo]), grammar.Production(foo, ['foo'])]

g = grammar.ContextFreeGrammar(top, prods)

parser = parse.EarleyChartParser(g, trace=True, chart_class=MemoChart)

p = parser.nbest_parse(['foo'])
print p
print p[0][0][0]
print p[1][0][0]
print "==", p[0][0][0] == p[1][0][0]
print "is", p[0][0][0] is p[1][0][0]
