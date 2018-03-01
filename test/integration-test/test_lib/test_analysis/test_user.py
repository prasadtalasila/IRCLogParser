import unittest
from lib.analysis import user
import lib.config as config
from mock import patch
import lib.util as util
import os
import StringIO
import sys
import filecmp
import networkx as nx

class UserTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = self.current_directory + "/../../../data/test_lib/test_analysis/user_test/"
        self.log_data = util.load_from_disk(self.test_data_dir + "log_data")
        self.nicks = util.load_from_disk(self.test_data_dir + "nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir + "nick_same_list")


    def tearDown(self):
        self.current_directory = None
        self.test_data_dir = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None


    @patch("lib.config.DEBUGGER", new = True)
    @patch("lib.config.PRINT_WORDS", new = True)
    @patch("lib.config.KEYWORDS_THRESHOLD", new = 0.01)
    @patch("lib.config.KEYWORDS_MIN_WORDS", new = 100)
    def test_keywords(self):
        expected_keywords_filtered = util.load_from_disk(self.test_data_dir + "keywords/keywords_filtered")
        expected_user_keyword_freq_dict = util.load_from_disk(self.test_data_dir + "user_keyword_freq_dict")
        expected_user_words_dict = util.load_from_disk(self.test_data_dir + "keywords/user_words_dict")
        expected_nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "keywords/nicks_for_stop_words")
        expected_sorted_keywords_for_channels = util.load_from_disk(self.test_data_dir + "keywords/sorted_keywords_for_channels")
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


    @patch("lib.analysis.user.time", autospec = True)
    @patch("lib.config.ENABLE_SVD", new = False)
    @patch("lib.config.ENABLE_ELBOW_METHOD_FOR_K", new = False)
    @patch("lib.config.NUMBER_OF_CLUSTERS", new = 11)
    @patch("lib.config.SHOW_N_WORDS_PER_CLUSTER", new = 10)
    @patch("lib.config.CHECK_K_TILL", new = 20)
    def test_keywords_clusters(self, mock_time):

        mock_time.return_value = 0
        expected_captured_output = util.load_from_disk( self.test_data_dir + "stdout_captured_output_keywords_clusters");

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        user.keywords_clusters(self.log_data, self.nicks, self.nick_same_list, self.current_directory ,"temp_output_keywords_clusters")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertTrue(filecmp.cmp(self.test_data_dir + "output_keywords_clusters.txt", self.current_directory + "/temp_output_keywords_clusters.txt"))
        os.remove(self.current_directory + "/temp_output_keywords_clusters.txt")

    @unittest.expectedFailure
    @patch("lib.config.ENABLE_SVD", new = True)
    @patch("lib.config.ENABLE_ELBOW_METHOD_FOR_K", new = True)
    @patch("lib.config.NUMBER_OF_CLUSTERS", new = 11)
    @patch("lib.config.SHOW_N_WORDS_PER_CLUSTER", new = 10)
    @patch("lib.config.CHECK_K_TILL", new = 20)
    def test_keywords_clusters_expected_failure(self, mock_time):
        mock_time.return_value = 0
        expected_captured_output = util.load_from_disk( self.test_data_dir + "stdout_captured_output_keywords_clusters");

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        user.keywords_clusters(self.log_data, self.nicks, self.nick_same_list, self.current_directory ,"temp_output_keywords_clusters")
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_captured_output, output)
        self.assertTrue(filecmp.cmp(self.test_data_dir + "output_keywords_clusters.txt", self.current_directory + "/temp_output_keywords_clusters.txt"))
        os.remove(self.current_directory + "/temp_output_keywords_clusters.txt")



    def test_nick_change_graph(self):
        expected_nick_change_graph_list = util.load_from_disk(self.test_data_dir + "nick_change_graph_list")
        expected_aggregate_nick_change_graph = util.load_from_disk(self.test_data_dir + "aggregate_nick_change_graph")

        nick_change_graph_list = user.nick_change_graph(self.log_data, True)

        aggregate_nick_change_graph = user.nick_change_graph(self.log_data, False)

        for i in xrange(len(nick_change_graph_list)):
            self.assertTrue(nx.is_isomorphic(expected_nick_change_graph_list[i], nick_change_graph_list[i]))

        self.assertTrue(nx.is_isomorphic(expected_aggregate_nick_change_graph, aggregate_nick_change_graph))



if __name__ == '__main__':
    unittest.main()
