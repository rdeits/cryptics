from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def index (server):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'<html>\n'])
    extend_([u'  <head>\n'])
    extend_([u"    <link href='/static/css/crypticweb.css' rel='stylesheet' type='text/css'>\n"])
    extend_([u'    <script type="text/javascript" src="/static/jquery/js/jquery-1.9.1.js"></script>\n'])
    extend_([u'    <script type="text/javascript" src="/static/jquery/js/jquery-ui-1.10.1.custom.min.js"></script>\n'])
    extend_([u'    <script type="text/javascript">var SERVER="', escape_(server, True), u'"</script>\n'])
    extend_([u'    <script type="text/javascript" src="/static/js/client.js"></script>\n'])
    extend_([u'  </head>\n'])
    extend_([u'  <body>\n'])
    extend_([u'    <div class="page">\n'])
    extend_([u'      <div class="header">\n'])
    extend_([u'        <div class="title">\n'])
    extend_([u'          <h1>Cryptic Crossword Clue Solver</h1>\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <div class="info">\n'])
    extend_([u'          <a href="https://github.com/rdeits/cryptics">Source code</a> | <a href="http://blog.robindeits.com/2013/02/11/a-cryptic-crossword-clue-solver/">More information</a><br>\n'])
    extend_([u'        </div>\n'])
    extend_([u'      </div>\n'])
    extend_([u'\n'])
    extend_([u'      <div class="preamble">\n'])
    extend_([u'        <div class="solver_desc">\n'])
    extend_([u'          This is a general tool for solving cryptic (or "British-style") crossword clues.  Run it by entering a cryptic clue along with the answer length (or lengths) in parenthesis. If you know some of the letters in the answer, you can type them in after the lengths, using a single \'.\' for each unknown letter. Here are some examples of clues it can solve correctly:\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <br>\n'])
    extend_([u'\n'])
    extend_([u'        <div id="sample_clues">\n'])
    extend_([u'        </div>\n'])
    extend_([u'        <br>\n'])
    extend_([u'\n'])
    extend_([u'        <div class="solver_desc">\n'])
    extend_([u'          Longer clues take longer to solve. You can help the solver by connecting words which act together with an underscore (\'_\') to from a phrase, as with "rises_and_falls" in the last example.\n'])
    extend_([u'        </div>\n'])
    extend_([u'      </div>\n'])
    extend_([u'\n'])
    extend_([u'      <div id="clue_entry">\n'])
    extend_([u'        <form name="main" method="post" id="clue_form">\n'])
    extend_([u'          <label for="Clue"></label>\n'])
    extend_([u'          <input name="Clue" type="text" id="clue_text" placeholder="Spin broken shingle (7) ..g...."/>\n'])
    extend_([u'          <input type="submit" value="Solve"/>\n'])
    extend_([u'        </form>\n'])
    extend_([u'      </div>\n'])
    extend_([u'\n'])
    extend_([u'      <div id="solution">\n'])
    extend_([u'      </div>\n'])
    extend_([u'    </div>\n'])
    extend_([u'  </body>\n'])
    extend_([u'</html>\n'])

    return self

index = CompiledTemplate(index, 'templates/index.html')
join_ = index._join; escape_ = index._escape

# coding: utf-8
def solver (answers, clue, err_msg):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    if err_msg:
        extend_([u'    ', escape_(err_msg, False), u'\n'])
    else:
        if answers is not None:
            extend_(['    ', u'    <div id="answer_nav">\n'])
            extend_(['    ', u'    <div id="similarities">\n'])
            extend_(['    ', u'    <b>Score</b><br>\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()):
                extend_(['        ', u'    ', escape_("{:.0%}".format(sim), True), u' <br>\n'])
            extend_(['    ', u'    </div>\n'])
            extend_(['    ', u'    <div id="answers">\n'])
            extend_(['    ', u'    <b>Answer</b><br>\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()):
                extend_(['        ', u'    <a href="#ans_header_', escape_(ans, True), u'">', escape_(ans, True), u'</a> <br>\n'])
            extend_(['    ', u'    </div>\n'])
            extend_(['    ', u'    </div>\n'])
            extend_(['    ', u'    <div id="derivations">\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()[:200]):
                extend_(['                ', u'    <div id="ans_header_', escape_(ans, True), u'"><h2>', escape_(ans, True), u': ', escape_("{:.0%}".format(sim), True), u' </h2>\n'])
                for ann in loop.setup(answers.answer_derivations[ans][:5]):
                    extend_(['                    ', u'    ', escape_(ann.derivation(), True), u' <br>\n'])
                    extend_(['                    ', u'    ', escape_(ann.long_derivation(), True), u' <br><br>\n'])
                extend_(['                ', u'    </div>\n'])
            extend_(['    ', u'    </div>\n'])

    return self

solver = CompiledTemplate(solver, 'templates/solver.html')
join_ = solver._join; escape_ = solver._escape

