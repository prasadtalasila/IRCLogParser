import unittest
from lib.analysis import user
import networkx as nx
import lib.util as util
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class UserTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks_hash = util.load_from_disk(current_directory+ "/data/nicks_hash")
        self.nick_same_list = util.load_from_disk(current_directory+"/data/nick_same_list")

    def tearDown(self):
        self.log_data = None
        self.nicks_hash = None

    def test_nick_change_graph(self):
        nick_change_graph_list = user.nick_change_graph(self.log_data, True)
        for i in range(len(nick_change_graph_list)):
            expected_nick_change_graph = nx.read_pajek(current_directory + "/data/nick_change_graph_"+str(i)+".net")
            assert nx.is_isomorphic(expected_nick_change_graph, nick_change_graph_list[i])
    
    def test_top_keywords_for_nick(self):
        user_keyword_freq_dict = util.load_from_disk(current_directory+"/data/user_keyword_freq_dict")
        top_keywords, top_keywords_normal_freq = user.top_keywords_for_nick(user_keyword_freq_dict, user_keyword_freq_dict[0]['nick'], 0.01, 100)
        expected_top_keywords = util.load_from_disk(current_directory+"/data/top_keywords")
        expected_top_keywords_normal_freq = util.load_from_disk(current_directory+"/data/top_keywords_normal_freq")

        assert top_keywords == expected_top_keywords
        assert top_keywords_normal_freq == expected_top_keywords_normal_freq
   
    def test_keywords(self):
       pass
        
    def test_keywords_clusters(self):
       pass 

    def test_extended_stop_words(self):
        nicks_for_stop_words = util.load_from_disk(current_directory+"/data/nicks_for_stop_words")
        stop_word_without_apostrophe = util.load_from_disk(current_directory+"/data/stop_word_without_apostrophe")
        stop_words_extended = user.extended_stop_words(nicks_for_stop_words, stop_word_without_apostrophe)
        expected_stop_words_extended = util.load_from_disk(current_directory+"/data/stop_words_extended")
        assert expected_stop_words_extended == stop_words_extended

if __name__ == '__main__':
    unittest.main()
