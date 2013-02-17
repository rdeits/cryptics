import web
from web import form
from pycryptics.solve_clue import CrypticClueSolver, split_clue_text
# import re
# from fake_solve_clue import FakeCrypticClueSolver as CrypticClueSolver
from fake_solve_clue import split_clue_text


class index:
    def GET(self):
        raise web.seeother('/solve/')
        # return render.index(None, form.d.Clue, "")


class solve:
    def GET(self, clue):
        try:
            phrases, lengths, pattern, answer = split_clue_text(clue)
        except Exception as e:
            return render.index(None, clue, "Sorry, went wrong that I don't know how to handle. Here's python's attempt at an explanation: " + str(e))
        if len(phrases) > 7:
            return render.index(None, clue, "Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them")
        solver.setup(clue)
        solver.run()
        answers = solver.collect_answers()
        print "returning:", answers
        return render.index(answers, solver.clue_text, "")

    def POST(self, clue):
        if not form.validates():
            return render.index(None, form.d.Clue, "I don't quite understand the formatting of that clue. Please make sure that the clue is of the form: Clue Text (Length) Pattern, as in the examples above.")
        raise web.seeother('/solve/'+form.d.Clue)

class halt:
    def POST(self):
        print "trying to halt"
        solver.stop()
        raise web.seeother('/')

if __name__ == "__main__":
    render = web.template.render('pycryptics/crypticweb/templates/')

    urls = ('/', 'index',
            '/solve/(.*)', 'solve',
            '/halt', 'halt')

    vclue = form.regexp(r"[^\(\)]*\([0-9 ]*[,[0-9 ]]*\)[ \.a-zA-Z]*", "invalid clue format")
    myform = form.Form(
        form.Textbox("Clue", vclue, size="100"))
    form = myform()
    with CrypticClueSolver() as solver:
        app = web.application(urls, globals())
        print "Starting up server. Press Ctrl+c to shut down"
        app.run()
    print "Shutting down...."
