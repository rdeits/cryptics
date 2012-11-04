import unittest
import solver

class TestClues(unittest.TestCase):
    def test_known_clues(self):
        for raw_clue in open('test/known_clues.txt', 'r').readlines():
            self.assertTrue(solver.solve_cryptic_clue(raw_clue))
