import unittest
from solve_structured_clue import parse_clue_text, solve_phrases


class TestClues(unittest.TestCase):
    def test_known_clues(self):
        for clue_text in open('clues/known_clues.txt', 'r').readlines():
            phrases, known_answer = parse_clue_text(clue_text)
            print clue_text
            print phrases
            answer = solve_phrases(phrases)[0][0][0]
            self.assertEqual(answer.lower(), known_answer.lower().strip())
