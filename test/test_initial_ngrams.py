import unittest
from language_utils import INITIAL_NGRAMS


class TestInitialNgrams(unittest.TestCase):
    def test_true(self):
        self.assertTrue('br' in INITIAL_NGRAMS[2])
        self.assertTrue('rock' in INITIAL_NGRAMS[4])

    def test_false(self):
        self.assertFalse('bx' in INITIAL_NGRAMS[2])

if __name__ == '__main__':
    unittest.main()
