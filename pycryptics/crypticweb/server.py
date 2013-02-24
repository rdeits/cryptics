import web
from web import form
from pycryptics.solve_clue import CrypticClueSolver, split_clue_text
import webbrowser
# from fake_solve_clue import FakeCrypticClueSolver as CrypticClueSolver
# from fake_solve_clue import split_clue_text


class index:
    def GET(self):
        raise web.seeother('/solve/')
        # return render.index(None, form.d.Clue, "")


class solve:
    def GET(self, clue):
        if clue.strip() != "":
            # try:
            phrases, lengths, pattern, answer = split_clue_text(clue)
            if sum(lengths) != len(pattern) and pattern != '':
                print "length mismatch"
                return render.index(None, clue, "The length of the pattern must exactly match the number of letters in the answer, or you can just leave it blank. Here are some allowable patterns:<br>(5) ....s<br>(3,2) a.e..<br>(9)<br>")
            assert len(pattern) == 0 or len(pattern) == sum(lengths), "Answer lengths and length of pattern string must match: sum(%s) != %d" % (lengths, len(pattern))
            # except Exception as e:
            #     raise e
            #     print e
            #     return render.index(None, clue, "Something went wrong that I don't know how to handle. Here's python's attempt at an explanation:<br>" + str(e))
            if len(phrases) > 7:
                return render.index(None, clue, "Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them")
            solver.setup(clue)
            solver.run()
            answers = solver.collect_answers()
            print "returning:", answers
            return render.index(answers, solver.clue_text, "")
        else:
            return render.index(None, "", "")

    def POST(self, clue):
        if not form.validates():
            return render.index(None, form.d.Clue, "I don't quite understand the formatting of that clue. Please make sure that the clue is of the form: Clue Text (Length) Pattern, as in the examples above.")
        raise web.seeother('/solve/'+form.d.Clue.replace('?', ''))

class halt:
    def POST(self):
        print "trying to halt"
        solver.stop()
        raise web.seeother('/')

if __name__ == '__main__':
    render = web.template.render('pycryptics/crypticweb/templates/')

    urls = ('/', 'index',
            '/solve/(.*)', 'solve',
            '/halt', 'halt')

    vclue = form.regexp(r"[^\(\)]*\([0-9 ]*[,[0-9 ]]*\)[ \.a-zA-Z]*", "invalid clue format")
    myform = form.Form(
        form.Textbox("Clue", vclue, size="100"))
    form = myform()

    solver = CrypticClueSolver()

    app = web.application(urls, globals())
    print "Starting up server. Press Ctrl+c to shut down"
    # t = threading.Thread(target=app.run)
    # t.start()
    webbrowser.open("http://localhost:8080", new=2)
    app.run()
    # t.join()
    print "Shutting down...."
