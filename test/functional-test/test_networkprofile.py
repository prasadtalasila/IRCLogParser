import unittest
import os
import networkx as nx
import numpy as np
import lib.in_out.reader as reader
import lib.nickTracker as nickTracker
import lib.util as util
import lib.config as config
from lib.analysis import network


class NetworkProfileTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data_dir = self.current_directory+"/data/input/"
        self.start_date = '2013-01-01'
        self.end_date = '2013-01-08'

    def tearDown(self):
        self.current_directory = None
        self.log_data_dir = None
        self.start_date = None
        self.end_date = None

    def test_presence_networks(self):
        log_data = reader.linux_input(self.log_data_dir, ["ALL"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/presence_graph_dict')
        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
        expected_output, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user,
                                                                  nick_channel_dict, nicks_hash, channels_hash)
        edge_types = ['CC', 'UU', 'CU']
        for edge_type in edge_types:
            self.assertTrue(nx.is_isomorphic(expected_output[edge_type]['graph'], expected_result[edge_type]['graph']))
            self.assertTrue(nx.is_isomorphic(expected_output[edge_type]['reducedGraph'], expected_result[edge_type]['reducedGraph']))
            expected_output[edge_type].pop('graph')
            expected_output[edge_type].pop('reducedGraph')
            expected_result[edge_type].pop('graph')
            expected_result[edge_type].pop('reducedGraph')
        np.testing.assert_equal(expected_output,expected_result)

    def test_message_exchange_network(self):
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/degree_anal_message_number_graph_kubuntu-devel')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        expected_output = network.degree_analysis_on_graph(message_number_graph)
        self.assertEqual(expected_result,expected_output)

    def test_reduced_networks_cutoff_0(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 0
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_0')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result,expected_output))

    def test_reduced_networks_cutoff_10(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 10
        print "10 default:{} config{}".format(default_config, config.THRESHOLD_MESSAGE_NUMBER_GRAPH)
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_10')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result,expected_output))

    def test_reduced_networks_cutoff_20(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 20
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_20')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result,expected_output))


if __name__ == '__main__':
    unittest.main()