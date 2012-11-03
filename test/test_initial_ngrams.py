import unittest
from solver import load_ngrams

initial_ngrams = load_ngrams()


class TestInitialNgrams(unittest.TestCase):
    def test_true(self):
        self.assertTrue('br' in initial_ngrams[2])
        self.assertTrue('rock' in initial_ngrams[4])

    def test_false(self):
        self.assertFalse('bx' in initial_ngrams[2])

if __name__ == '__main__':
    unittest.main()