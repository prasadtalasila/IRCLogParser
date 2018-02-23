import unittest
from lib.analysis import user
import lib.config as config
from mock import patch
import lib.util as util
import os
import StringIO
import sys


class UserTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data = util.load_from_disk(self.current_directory + "/../../../data/user_test/log_data")
        self.nicks = util.load_from_disk(self.current_directory + "/../../../data/user_test/nicks")
        self.nick_same_list = util.load_from_disk(self.current_directory + "/../../../data/user_test/nick_same_list")


    def tearDown(self):
        self.current_directory = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None


    @patch("lib.config.DEBUGGER", new = True)
    @patch("lib.config.PRINT_WORDS", new = True)
    @patch("lib.config.KEYWORDS_THRESHOLD", new = 0.01)
    @patch("lib.config.KEYWORDS_MIN_WORDS", new = 100)
    def test_keywords(self):
        expected_keywords_filtered = util.load_from_disk(self.current_directory + "/../../../data/user_test/keywords/keywords_filtered")
        expected_user_keyword_freq_dict = util.load_from_disk(self.current_directory + "/../../../data/user_test/user_keyword_freq_dict")
        expected_user_words_dict = util.load_from_disk(self.current_directory + "/../../../data/user_test/keywords/user_words_dict")
        expected_nicks_for_stop_words = util.load_from_disk(self.current_directory + "/../../../data/user_test/keywords/nicks_for_stop_words")
        expected_sorted_keywords_for_channels = util.load_from_disk(self.current_directory + "/../../../data/user_test/keywords/sorted_keywords_for_channels")
        expected_captured_output = util.load_from_disk(self.current_directory +  "/data/user_test/keywords/stdout_captured_output")
        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels = user.keywords(self.log_data , self.nicks, self.nick_same_list)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertEqual(expected_keywords_filtered, keywords_filtered)
        self.assertEqual(expected_user_keyword_freq_dict, user_keyword_freq_dict)
        self.assertEqual(expected_user_words_dict, user_words_dict)
        self.assertEqual(expected_nicks_for_stop_words, nicks_for_stop_words)
        self.assertEqual(expected_sorted_keywords_for_channels, sorted_keywords_for_channels)


if __name__ == '__main__':
    unittest.main()
