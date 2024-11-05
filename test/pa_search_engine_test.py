import unittest
import pa_search_engine as pa


class MyTestCase(unittest.TestCase):
    def test_removes_ascii(self):
        word = "As%d^&*(F"

        new_word = pa.sanitize_word(word)

        expected_word = "asdf"
        self.assertEqual(expected_word, new_word)

    def test_parse_empty_line(self):
        line = ""

        parsed = pa.parse_line(line)

        expected_parsed = []
        self.assertEqual(expected_parsed, parsed)

    def test_parse_line_with_non_ascii_words(self):
        line = "%% uhhh 9* 7&&& $$$"

        parsed = pa.parse_line(line)

        expected_parsed = ["uhhh"]
        self.assertEqual(expected_parsed, parsed)

    def test_parse_ascii_line(self):
        line = "hello my name is bella"

        parsed = pa.parse_line(line)

        expected_parsed = ["hello", "my", "name", "is", "bella"]
        self.assertEqual(expected_parsed, parsed)



if __name__ == '__main__':
    unittest.main()
