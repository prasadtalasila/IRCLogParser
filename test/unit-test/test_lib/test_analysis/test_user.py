import unittest
from lib.analysis import user
import lib.config as config
from lib.in_out import reader, saver
import lib.nickTracker as nickTracker
from mock import patch
import networkx as nx
import lib.util as util
import os
import StringIO
import sys
import filecmp

current_directory = os.path.dirname(os.path.realpath(__file__))
state0 = 0
state1 = 0
def build_graphs_util(nick_sender, nick_receiver, time, year, month, day, day_graph, aggr_graph):
    build_graphs_list = util.load_from_disk(current_directory + "/data/user_test/build_graphs_list")
    day_graph = build_graphs_list[state][0]
    aggr_graph = build_graphs_list[state][1]
    state0 += 1 
def rec_list_splice_util(rec_list):
    rec_list_splice_list = util.load_from_disk(current_directory + "/data/user_test/rec_list_splice_list")
    rec_list[2] = rec_list_splice_list[state1]
    state1 += 1

class UserTest(unittest.TestCase):

    def setUp(self):
        #./data/user_test/log_data has data data for the following configuraton:
        #   STARTING_DATE = "2013-2-1"
        #   ENDING_DATE = "2013-2-15"
        #   CHANNEL_NAME = ["#kubuntu-devel"] 
        self.log_data = util.load_from_disk(current_directory+"/data/user_test/log_data")
        self.nicks_hash = util.load_from_disk(current_directory+ "/data/user_test/nicks_hash")
        self.nick_same_list = util.load_from_disk(current_directory+"/data/user_test/nick_same_list")
        state0 = 0
        state1 = 0

    def tearDown(self):
        self.log_data = None
        self.nicks_hash = None
        self.nick_same_list = None

    @patch("util.splice_find",  autospec = True)
    @patch("util.build_graphs",  autospec = True)
    @patch("util.get_year_month_day",  autospec = True)
    def test_nick_change_graph(self, mock_get_year_month_day,mock_build_graphs, mock_splice_find):
        mock_splice_find.side_effect = util.load_from_disk(current_directory + "/data/user_test/nick_change_graph/splice_find_list")
        mock_build_graphs.side_effect = build_graphs_util 
        nick_change_graph_list = user.nick_change_graph(self.log_data, True)
        expected_nick_change_graph_list = util.load_from_disk(current_directory + "/data/user_test/nick_change_graph_list")
        for i in range(len(nick_change_graph_list)):
            assert nx.is_isomorphic(expected_nick_change_graph_list[i],  nick_change_graph_list[i])
    
    def test_top_keywords_for_nick(self):
        user_keyword_freq_dict = util.load_from_disk(current_directory+"/data/user_test/user_keyword_freq_dict")
        top_keywords, top_keywords_normal_freq = user.top_keywords_for_nick(user_keyword_freq_dict, user_keyword_freq_dict[0]['nick'], 0.01, 100)


        expected_top_keywords = util.load_from_disk(current_directory+"/data/user_test/top_keywords")
        expected_top_keywords_normal_freq = util.load_from_disk(current_directory+"/data/user_test/top_keywords_normal_freq")

        assert top_keywords == expected_top_keywords
        assert top_keywords_normal_freq == expected_top_keywords_normal_freq

    @patch("util.get_nick_representative", autospec = True) 
    @patch("util.check_if_msg_line", autospec = True) 
    @patch("util.correctLastCharCR", autospec = True) 
    @patch("util.correct_last_char_list", autospec = True) 
    @patch("util.splice_find", autospec = True) 
    @patch("util.correct_nick_for_", autospec = True) 
    @patch("util.rec_list_splice", autospec = True) 
    @patch("lib.analysis.user.extended_stop_words", autospec = True) 
    def test_keywords(self, mock_extended_stop_words, mock_rec_list_splice, mock_correct_nick_for_, mock_splice_find, mock_correct_last_char_list, mock_correctLastCharCR, mock_check_if_msg_line, mock_get_nick_representative):
        mock_get_nick_representative.side_effect = util.load_from_disk(current_directory + "/data/user_test/get_nick_representative_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(current_directory + "/data/user_test/check_if_msg_line_list")
        mock_correctLastCharCR.side_effect = util.load_from_disk(current_directory + "/data/user_test/correctLastCharCR_list")
        mock_correct_last_char_list.side_effect = util.load_from_disk(current_directory + "/data/user_test/correct_last_char_list_list")
        mock_splice_find.side_effect = util.load_from_disk(current_directory + "/data/user_test/keywords/splice_find_list")
        mock_correct_nick_for_.side_effect = util.load_from_disk(current_directory + "/data/user_test/correct_nick_for_list")
        mock_rec_list_splice.side_effect = rec_list_splice_util
        mock_extended_stop_words.side_effect = util.load_from_disk(current_directory + "/data/user_test/keywords/extended_stop_words_list")

        keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels = user.keywords(self.log_data , self.nicks_hash, self.nick_same_list) 
        expected_keywords_filtered = util.load_from_disk(current_directory + "/data/user_test/keywords/keywords_filtered")
        expected_user_keyword_freq_dict = util.load_from_disk(current_directory + "/data/user_test/user_keyword_freq_dict")
        expected_user_words_dict = util.load_from_disk(current_directory + "/data/user_test/keywords/user_words_dict") 
        expected_nicks_for_stop_words = util.load_from_disk(current_directory + "/data/user_test/keywords/nicks_for_stop_words")
        expected_sorted_keywords_for_channels = util.load_from_disk(current_directory +"/data/user_test/keywords/sorted_keywords_for_channels") 

        assert expected_keywords_filtered == keywords_filtered
        assert expected_user_keyword_freq_dict == user_keyword_freq_dict
        assert expected_user_words_dict == user_words_dict
        assert expected_nicks_for_stop_words == nicks_for_stop_words
        assert expected_sorted_keywords_for_channels == sorted_keywords_for_channels



    @patch("lib.analysis.user.keywords", autospec = True)
    @patch("lib.analysis.user.extended_stop_words", autospec = True)
    def test_keywords_clusters(self,mock_extended_stop_words, mock_keywords):
        keywords_filtered = util.load_from_disk(current_directory + "/data/user_test/keywords/keywords_filtered")
        user_keyword_freq_dict = util.load_from_disk(current_directory + "/data/user_test/user_keyword_freq_dict")
        user_words_dict = util.load_from_disk(current_directory + "/data/user_test/keywords/user_words_dict") 
        nicks_for_stop_words = util.load_from_disk(current_directory + "/data/user_test/keywords/nicks_for_stop_words")
        sorted_keywords_for_channels = util.load_from_disk(current_directory +"/data/user_test/keywords/sorted_keywords_for_channels") 
        mock_keywords.return_value = keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, sorted_keywords_for_channels
        #/data/user_test/extended_stop_words_list is exclusively used by test_keywords_clusters
        mock_extended_stop_words.side_effect = util.load_from_disk(current_directory + "/data/user_test/extended_stop_words_list")
        
        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        user.keywords_clusters(self.log_data, self.nicks_hash, self.nick_same_list, current_directory + "/data/user_test/","temp_output_keywords_clusters")
        sys.stdout = sys.__stdin__

#        assert expected_captured_output == string
        assert filecmp.cmp(current_directory + "/data/user_test/output_keywords_clusters.txt", current_directory + "/data/user_test/temp_output_keywords_clusters.txt")
        os.remove("data/user_test/temp_output_keywords_clusters.txt")



    def test_extended_stop_words(self):
        nicks_for_stop_words = util.load_from_disk(current_directory+"/data/user_test/keywords/nicks_for_stop_words")
        stop_word_without_apostrophe = util.load_from_disk(current_directory+"/data/user_test/stop_word_without_apostrophe")
        expected_stop_words_extended = util.load_from_disk(current_directory+"/data/user_test/extended_stop_words")

        stop_words_extended = user.extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe)

        assert expected_stop_words_extended == stop_words_extended

if __name__ == '__main__':
    unittest.main()
