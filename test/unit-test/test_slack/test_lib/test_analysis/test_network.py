import unittest
from lib.slack.analysis import network
import networkx as nx
import lib.slack.util as util
import lib.slack.config as config 
import os, mock
from networkx.algorithms.components.connected import connected_components

current_directory = os.path.dirname(os.path.realpath(__file__))

def check_if_msg_line_mock(line):
    
    if line == "[00:06:41] Guest86829 (~alejandro@190.250.76.206) left irc: Quit: Lost terminal\n":
        return False
        
    return True
    
def create_connected_nick_list_mock(conn_comp_list):
    conn_com_list = util.load_from_disk(current_directory+ "/data/conn_comp_list")
    
def correctLastCharCR_mock(nick):
    return nick
    
class NetworkTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks = util.load_from_disk(current_directory+ "/data/nicks")
        self.nick_same_list = util.load_from_disk(current_directory+ "/data/nick_same_list")

    def tearDown(self):
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    @mock.patch('lib.slack.analysis.network.util')
    def test_message_number_graph(self, mock_util):
        log_data = util.load_from_disk(current_directory + "/data/test_msg_log_data")
        nicks = util.load_from_disk(current_directory + "/data/test_msg_nicks")
        nick_same_list = util.load_from_disk(current_directory + "/data/test_msg_nick_same_list")
        to_graph = util.load_from_disk(current_directory + "/data/to_graph")
        
        conn_comp_list = list(connected_components(to_graph))
        
        mock_util.to_graph.return_value = to_graph
        mock_util.check_if_msg_line.side_effect = check_if_msg_line_mock
        mock_util.create_connected_nick_list.side_effect = create_connected_nick_list_mock
        mock_util.correctLastCharCR.side_effect = correctLastCharCR_mock
        
        network.message_number_graph(log_data, nicks, nick_same_list, DAY_BY_DAY_ANALYSIS=False)
        
        mock_util.to_graph.assert_called_once_with(nick_same_list)
        mock_util.create_connected_nick_list.assert_called_once_with(conn_comp_list)
        self.assertEqual(mock_util.check_if_msg_line.call_count, 3)
        self.assertEqual(mock_util.correctLastCharCR.call_count, 6)
        
    def test_filter_edge_list(self):
        pass
        
    def test_degree_analysis_on_graph(self):
        pass
        
    @mock.patch('lib.slack.analysis.network.util')
    def test_message_time_graph(self, mock_util):
        pass
    
    @mock.patch('lib.slack.analysis.network.util')
    def test_message_number_bins_csv(self, mock_util):
        
        log_data = util.load_from_disk(current_directory + "/data/log_data")
        nicks = util.load_from_disk(current_directory + "/data/nicks")
        nick_same_list = util.load_from_disk(current_directory + "/data/nick_same_list")
        
        network.message_number_bins_csv(log_data, nicks, nick_same_list)
    
    @mock.patch('lib.slack.analysis.network.message_number_graph')
    def test_degree_node_number_csv(self, mock_msg_graph):
        
        msg_num_graph_day_list = util.load_from_disk(current_directory + "/data/msg_day_list")
        out_degree_ = util.load_from_disk(current_directory + "/data/out_degree")
        in_degree_ = util.load_from_disk(current_directory + "/data/in_degree")
        total_degree_ = util.load_from_disk(current_directory + "/data/total_degree")
        
        mock_msg_graph.return_value = msg_num_graph_day_list
        
        out_degree, in_degree, total_degree = network.degree_node_number_csv(self.log_data, self.nicks, self.nick_same_list)
        
        mock_msg_graph.assert_called_once_with(self.log_data, self.nicks, self. nick_same_list, True)
        self.assertEqual(out_degree, out_degree_)
        self.assertEqual(in_degree, in_degree_)
        self.assertEqual(total_degree, total_degree_)

    def test_nick_receiver_from_conn_comp(self):
        conn_comp_list = [["Rohit", "rohit", "kaushik"], ["krishna", "krish", "acharya"], ["Rohan", "rohan", "ron"]]
        config.MAX_EXPECTED_DIFF_NICKS = 5000 #mock config variable
        conn_comp_list.extend([[]]*config.MAX_EXPECTED_DIFF_NICKS)
        
        assert network.nick_receiver_from_conn_comp("kaushik", conn_comp_list) == "Rohit"
        assert network.nick_receiver_from_conn_comp("krishna", conn_comp_list) == "krishna"
        assert network.nick_receiver_from_conn_comp("Rohan_goel", conn_comp_list) == ""
        
    @mock.patch('lib.slack.analysis.network.message_number_graph')
    @mock.patch('lib.slack.analysis.network.user.keywords')
    def test_identify_hubs_and_experts(self, mock_keywords, mock_msg_graph):
    
        top_hub_ = util.load_from_disk(current_directory+ "/data/top_hub")
        top_keyword_overlap_ = util.load_from_disk(current_directory+ "/data/top_keyword_overlap")
        top_auth_ = util.load_from_disk(current_directory+ "/data/top_auth")
        message_graph = util.load_from_disk(current_directory+ "/data/message_graph")
        keyword_dict_list = util.load_from_disk(current_directory+ "/data/keyword_dict_list")
        user_keyword_freq_dict = util.load_from_disk(current_directory+"/data/user_keyword_freq_dict")
        user_words_dict_list = util.load_from_disk(current_directory+"/data/user_words_dict_list")
        nicks_for_stop_words = util.load_from_disk(current_directory+"/data/nicks_for_stop_words")
        keywords_for_channels = util.load_from_disk(current_directory+"/data/keywords_for_channels")
        
        # setup mock
        mock_msg_graph.return_value = message_graph
        mock_keywords.return_value = keyword_dict_list, user_keyword_freq_dict, user_words_dict_list, nicks_for_stop_words, keywords_for_channels
        
        message_num_graph, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(self.log_data, self.nicks, self.nick_same_list)
        
        mock_msg_graph.assert_called_once_with(self.log_data, self.nicks, self.nick_same_list)
        mock_keywords.assert_called_once_with(self.log_data, self.nicks, self.nick_same_list)
        self.assertEqual(top_hub, top_hub_)
        self.assertEqual(top_keyword_overlap, top_keyword_overlap_)
        self.assertEqual(top_auth, top_auth_) 
        self.assertTrue(nx.is_isomorphic(message_graph, message_num_graph))

if __name__ == '__main__':
    unittest.main()
