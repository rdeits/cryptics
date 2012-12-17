import unittest
from solve_factored_clue import solve_clue_text, parse_clue_text, stop_go_server


class TestClues(unittest.TestCase):
    def test_known_clues(self):
        try:
            for clue_text in open('clues/known_clues.txt', 'r').readlines():
                phrases, known_answer = parse_clue_text(clue_text)
                answers = solve_clue_text(clue_text)
                for a in answers[:5]: print a
                self.assertEqual(answers[0].answer.lower(), known_answer.lower().strip())
        finally:
            stop_go_server()
