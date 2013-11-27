import web
from pycryptics.solve_clue import CrypticClueSolver, split_clue_text
import re

SERVER = "http://cryptic-solver.appspot.com/solve/"

class index:
    def GET(self):
        return render.index(SERVER)


class solve:
    def GET(self, clue):
        clue = clue.strip()
        if clue != "":
            if not re.match(r"[^\(\)]*\([0-9]+ *[,[0-9 ]*]*\)[ \.a-zA-Z]*", clue):
                return render.solver(None, clue, "I don't quite understand the formatting of that clue. Please make sure that the clue is of the form: <br>clue text (length)<br>or<br>clue text (length) pattern<br> as in the examples above.")
            try:
                phrases, lengths, pattern, answer = split_clue_text(clue)
                if sum(lengths) != len(pattern) and pattern != '':
                    print "length mismatch"
                    return render.solver(None, clue, "The length of the pattern must exactly match the number of letters in the answer, or you can just leave it blank. Here are some allowable patterns:<br>(5) ....s<br>(3,2) a.e..<br>(9)<br>")
                assert len(pattern) == 0 or len(pattern) == sum(lengths), "Answer lengths and length of pattern string must match: sum(%s) != %d" % (lengths, len(pattern))
            except Exception as e:
                raise e
                print e
                return render.solver(None, clue, "Something went wrong that I don't know how to handle. Here's python's attempt at an explanation:<br>" + str(e))
            if len(phrases) > 7:
                return render.solver(None, clue, "Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them")
            solver.setup(clue)
            solver.run()
            answers = solver.collect_answers()
            print "returning:", answers
            return render.solver(answers, solver.clue_text, "")
        else:
            return render.solver(None, "", "")

render = web.template.render('pycryptics/crypticweb/templates/')

urls = ('/', 'index',
        '/solve/(.*)', 'solve')


solver = CrypticClueSolver()

app = web.application(urls, globals())
print "Starting up server. Press Ctrl+c to shut down"
app = app.gaerun()
print "Shutting down...."
