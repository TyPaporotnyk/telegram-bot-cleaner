import unittest

from services import _messages_without_english_words


class TestMessagesToCorrect(unittest.TestCase):

    def test_messages_without_english(self):
        self.assertEqual(_messages_without_english_words("Hello World"), False)
        self.assertEqual(_messages_without_english_words("Hello, World!"), False)
        self.assertEqual(_messages_without_english_words("Привет"), True)
        self.assertEqual(_messages_without_english_words("Привет мир"), True)
        self.assertEqual(_messages_without_english_words("Привет, мир!"), True)
        self.assertEqual(_messages_without_english_words("Привет, World!"), True)
        self.assertEqual(_messages_without_english_words(",!"), False)
