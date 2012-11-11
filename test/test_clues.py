import unittest
from solve_structured_clue import solve_clue_text, parse_clue_text


class TestClues(unittest.TestCase):
    def test_known_clues(self):
        for clue_text in open('clues/known_clues.txt', 'r').readlines():
            phrases, known_answer = parse_clue_text(clue_text)
            answers = solve_clue_text(clue_text)
            print answers[:5]
            self.assertEqual(answers[0][0][0].lower(), known_answer.lower().strip())
