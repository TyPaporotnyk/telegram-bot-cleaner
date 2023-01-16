import unittest

from services import _messages_without_english_words


class TestMessagesToCorrect(unittest.TestCase):

    def test_request_jobs_list(self):
        self.assertEqual(_messages_without_english_words("Hello World"), False)
        self.assertEqual(_messages_without_english_words("Hello World!! HEEE"), False)
        self.assertEqual(_messages_without_english_words("Мир"), True)
        self.assertEqual(_messages_without_english_words("Привет мир"), True)
        self.assertEqual(_messages_without_english_words("Привет!мир"), True)
        self.assertEqual(_messages_without_english_words("Привет!  !! Worlds"), True)
