import unittest
from lib.slack.analysis import network
import networkx as nx
import lib.slack.util as util
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class NetworkTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks = util.load_from_disk(current_directory+ "/data/nicks")
        self.nick_same_list = util.load_from_disk(current_directory+ "/data/nick_same_list")

    def tearDown(self):
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    def test_identify_hubs_and_experts(self):
        message_graph, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(self.log_data, self.nicks, self.nick_same_list)
        expected_message_graph = util.load_from_disk(current_directory+ "/data/message_graph")
        expected_top_hub = util.load_from_disk(current_directory+ "/data/top_hub")
        expected_top_keyword_overlap = util.load_from_disk(current_directory+ "/data/top_keyword_overlap")
        expected_top_auth = util.load_from_disk(current_directory+ "/data/top_auth")
        
        assert top_hub == expected_top_hub
        assert top_keyword_overlap == expected_top_keyword_overlap
        assert top_auth == expected_top_auth
        assert nx.is_isomorphic(message_graph, expected_message_graph)

if __name__ == '__main__':
    unittest.main()
