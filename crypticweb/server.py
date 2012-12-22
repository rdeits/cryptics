import web
from web import form
from solve_factored_clue import CrypticClueSolver, split_clue_text
import threading


class index:
    def GET(self):
        # form = myform()
        answers = solver.answers_with_clues
        if answers == []:
            answers = ["Sorry, I couldn't find any answers"]
        elif answers is None:
            answers = [""]
        return render.index(answers[:200], form)

    def POST(self):
        # form = myform()
        if not form.validates():
            return render.index(["Sorry, something went wrong with that clue"], form)
        else:
            # phrases, answer = parse_clue_text(form.d.Clue)
            # answers = solve_phrases(phrases)[:50]
            phrases, lengths, pattern, answer = split_clue_text(form.d.Clue)
            if len(phrases) > 7:
                return render.index(["Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them"], form)
            solver.clue_text = form.d.Clue
            solver_thread = threading.Thread(target=solver.run)
            solver_thread.start()
            solver_thread.join()
            # answers = solve_clue_text(form.d.Clue)
            raise web.seeother('/')


class halt:
    def POST(self):
        print "trying to halt"
        solver.stop()
        raise web.seeother('/')


if __name__ == "__main__":
    render = web.template.render('crypticweb/templates/')

    urls = ('/', 'index',
            '/halt', 'halt')

    myform = form.Form(
        form.Textbox("Clue", size="100"))
    form = myform()
    with CrypticClueSolver() as solver:
        app = web.application(urls, globals())
        app.run()
