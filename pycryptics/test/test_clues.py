import unittest
import time
from pycryptics.solve_clue import CrypticClueSolver, split_clue_text


class TestClues(unittest.TestCase):
    def test_timed_clues(self):
        with CrypticClueSolver() as solver:
            solver.quiet = True
            start = time.time()
            for clue_text in open('clues/known_clues.txt', 'r').readlines():
                print "\n========================================"
                print clue_text
                phrases, lengths, pattern, known_answer = split_clue_text(clue_text)
                solver.setup(clue_text)
                answers = solver.run()
                print answers[0].long_derivation()
                # for a in answers[:5]:
                #     print a
                self.assertEqual(answers[0].answer.lower(), known_answer.lower().strip())
            print "\n========================================"
            print "Finished timed set in {:.1f} seconds".format(time.time() - start)

    def test_more_clues(self):
        with CrypticClueSolver() as solver:
            solver.quiet = True
            for clue_text in open('clues/more_known_clues.txt', 'r').readlines():
                print "\n========================================"
                print clue_text
                phrases, lengths, pattern, known_answer = split_clue_text(clue_text)
                solver.setup(clue_text)
                answers = solver.run()
                print answers[0].long_derivation()
                # for a in answers[:5]:
                #     print a
                self.assertEqual(answers[0].answer.lower(), known_answer.lower().strip())
