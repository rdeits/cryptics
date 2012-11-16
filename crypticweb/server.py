import web
from web import form
from solve_factored_clue import solve_clue_text

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
            answers = solve_clue_text(form.d.Clue)[:50]
            if answers == []:
                answers = ["Sorry, I couldn't find any answers"]
            return render.index(answers, form)

if __name__=="__main__":
    app.run()
