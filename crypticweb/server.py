import web
from web import form
from solve_factored_clue import solve_clue_text, stop_go_server

render = web.template.render('crypticweb/templates/')

urls = ('/', 'index')
app = web.application(urls, globals())

myform = form.Form(
    form.Textbox("Clue", size="100"))


class index:
    def GET(self):
        form = myform()
        return render.index([], form)

    def POST(self):
        form = myform()
        if not form.validates():
            return render.index(["Sorry, something went wrong with that clue"], form)
        else:
            # phrases, answer = parse_clue_text(form.d.Clue)
            # answers = solve_phrases(phrases)[:50]
            if len(form.d.Clue.split('(')[0].strip().split(' ')) > 7:
                return render.index("Sorry, I can't reliably handle clues longer than 7 phrases yet. Try grouping some words into phrases by putting an underscore instead of a space between them")
            answers = solve_clue_text(form.d.Clue)
            if answers == []:
                answers = ["Sorry, I couldn't find any answers"]
            return render.index(answers[:200], form)


if __name__ == "__main__":
    try:
        app.run()
    finally:
        stop_go_server()
