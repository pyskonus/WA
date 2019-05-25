from bigraph import Bigraph
import unittest


class TestBigraph(unittest.TestCase):

    def setUp(self):
        self.example = Bigraph()

    def tearDown(self):
        del self.example

    def test__steitem__(self):
        self.example['a'] = {('e', 2), ('c', 2), ('d', 4)}
        self.example['b'] = {('c', 1)}
        self.example['c'] = {('d', 1), ('c', 1)}

        self.assertIsInstance(self.example['a'], list)
        self.assertIsInstance(self.example['c'], list)
        self.assertIsInstance(self.example['b'], list)

        with self.assertRaises(ValueError):
            self.example['d']

    def test__getitem__(self):
        self.example['a'] = {('e', 2), ('c', 2), ('d', 4)}
        self.example['b'] = {('c', 1)}
        self.example['c'] = {('d', 1), ('c', 1)}

        self.assertEqual(set(self.example['a']), {('c', 2), ('e', 2), ('d', 4)})

    def test_get_incentives(self):
        self.example['a'] = {('e', 2), ('c', 2), ('d', 4)}
        self.example['b'] = {('c', 1)}
        self.example['c'] = {('d', 1), ('c', 1)}

        self.assertEqual(self.example.get_incentives('d'), {('c', 1), ('a', 4)})


if __name__ == "__main__":
    unittest.main()
