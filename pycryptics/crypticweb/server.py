import web
from web import form
from solve_clue import CrypticClueSolver, split_clue_text
# from fake_solve_clue import CrypticClueSolver, split_clue_text
# import threading


class index:
    def GET(self):
        answers = solver.collect_answers()
        return render.index(answers, solver.clue_text, "")

    def POST(self):
        if not form.validates():
            return render.index([], "", "Sorry, something went wrong with that clue")
        else:
            phrases, lengths, pattern, answer = split_clue_text(form.d.Clue)
            if len(phrases) > 7:
                return render.index([], form.d.Clue, "Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them")
            solver.setup(form.d.Clue)
            solver.run()
            # solver_thread = threading.Thread(target=solver.run)
            # solver_thread.start()
            # solver_thread.join()
            raise web.seeother('/')


class halt:
    def POST(self):
        print "trying to halt"
        solver.stop()
        raise web.seeother('/')

if __name__ == "__main__":
    render = web.template.render('pycryptics/crypticweb/templates/')

    urls = ('/', 'index',
            '/halt', 'halt')

    myform = form.Form(
        form.Textbox("Clue", size="100"))
    form = myform()
    with CrypticClueSolver() as solver:
        app = web.application(urls, globals())
        print "Starting up server. Press Ctrl+c to shut down"
        app.run()
    print "Shutting down...."
