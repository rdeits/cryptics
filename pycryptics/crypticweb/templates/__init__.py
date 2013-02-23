from web.template import CompiledTemplate, ForLoop, TemplateResult


# coding: utf-8
def index (answers, clue, err_msg):
    __lineoffset__ = -4
    loop = ForLoop()
    self = TemplateResult(); extend_ = self.extend
    extend_([u'\n'])
    extend_([u"<link href='/static/crypticweb.css' rel='stylesheet' type='text/css'>\n"])
    extend_([u'\n'])
    extend_([u'<h1><a href="/">Cryptic Crossword Clue Solver</a></h1>\n'])
    extend_([u'<a href="https://github.com/rdeits/cryptics">Source code</a><br>\n'])
    extend_([u'This is a general tool for solving cryptic (or "British-style") crossword clues.  Run it by entering a cryptic clue along with the answer length (or lengths) in parenthesis. If you know some of the letters in the answer, you can type them in after the lengths, using a single \'.\' for each unknown letter. Here are some examples of clues it can solve correctly:<br><br>\n'])
    extend_([u'\n'])
    extend_([u'<a href="/solve/Spin%20broken%20shingle%20(7)">Spin broken shingle (7)</a><br>\n'])
    extend_([u'ENGLISH<br>\n'])
    extend_([u'<a href="/solve/Be%20aware%20of%20nerd\'s%20flip-flop%20(4)%20k...">Be aware of nerd\'s flip-flop (4) k...</a><br>\n'])
    extend_([u'KNOW<br>\n'])
    extend_([u'<a href="/solve/Stirs,%20spilling%20soda%20(4)%20.d..">Stirs, spilling soda (4) .d..</a><br>\n'])
    extend_([u'ADOS<br>\n'])
    extend_([u'<a href="/solve/Male%20done%20mixing%20drink%20(8)">Male done mixing drink (8)</a><br>\n'])
    extend_([u'LEMONADE<br>\n'])
    extend_([u'<a href="/solve/Bottomless%20sea,%20stormy%20sea%20-%20waters\'%20surface%20rises_and_falls%20(7)%20s.es...">Bottomless sea, stormy sea - waters\' surface rises_and_falls (7) s.es...</a><br>\n'])
    extend_([u'SEESAWS<br>\n'])
    extend_([u'<br>\n'])
    extend_([u'\n'])
    extend_([u'Longer clues take longer to solve. You can help the solver by connecting words which act together with an underscore (\'_\') to from a phrase, as with "rises_and_falls" in the last example.\n'])
    extend_([u'\n'])
    extend_([u'<form name="main" method="post" id="clue_form">\n'])
    extend_([u'        <label for="Clue">Clue</label>\n'])
    extend_([u'        <input name="Clue" type="text" id="Clue" placeholder="Spin broken shingle (7) ..g...." value="', escape_(clue, True), u'" size="100"/>\n'])
    extend_([u'        <input type="submit" value="Solve"/>\n'])
    extend_([u'        <input type="submit" formaction="/halt" value="Halt"/>\n'])
    extend_([u'</form>\n'])
    extend_([u'\n'])
    extend_([u'<div id="solution">\n'])
    if err_msg:
        extend_(['        ', u'    ', escape_(err_msg, False), u'\n'])
    else:
        if answers is not None:
            extend_(['            ', u'    <div id="answer_nav">\n'])
            extend_(['            ', u'    <div id="similarities">\n'])
            extend_(['            ', u'    <b>Score</b><br>\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()):
                extend_(['                ', u'    ', escape_("{:.2g}".format(sim), True), u' <br>\n'])
            extend_(['            ', u'    </div>\n'])
            extend_(['            ', u'    <div id="answers">\n'])
            extend_(['            ', u'    <b>Answer</b><br>\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()):
                extend_(['                ', u'    <a href="#ans_header_', escape_(ans, True), u'">', escape_(ans, True), u'</a> <br>\n'])
            extend_(['            ', u'    </div>\n'])
            extend_(['            ', u'    </div>\n'])
            extend_(['            ', u'    <div id="derivations">\n'])
            for (sim, ans) in loop.setup(answers.sorted_answers()[:200]):
                extend_(['                        ', u'    <span class="answer_header" id="ans_header_', escape_(ans, True), u'">', escape_(ans, True), u': ', escape_(sim, True), u' </span> <br>\n'])
                for ann in loop.setup(answers.answer_derivations[ans][:5]):
                    extend_(['                            ', u'    ', escape_(ann, True), u' <br>\n'])
            extend_(['            ', u'    </div>\n'])
    extend_([u'</div>\n'])

    return self

index = CompiledTemplate(index, 'templates/index.html')
join_ = index._join; escape_ = index._escape

