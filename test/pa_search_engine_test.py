import unittest
import pa_search_engine as pa


class MyTestCase(unittest.TestCase):
    def test_removes_ascii(self):
        word = "As%d^&*(F"

        new_word = pa.sanitize_word(word)

        expected_word = "asdf"
        self.assertEqual(expected_word, new_word)


if __name__ == '__main__':
    unittest.main()
