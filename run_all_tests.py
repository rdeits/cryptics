from pycryptics.solve_clue import CrypticClueSolver, split_clue_text

with CrypticClueSolver() as solver:
    for clue_text in open('clues/known_clues.txt', 'r').readlines():
        phrases, lengths, pattern, known_answer = split_clue_text(clue_text)
        solver.setup(clue_text)
        answers = solver.run()
        for a in answers[:5]: print a
        assert (answers[0].answer.lower() == known_answer.lower().strip())
