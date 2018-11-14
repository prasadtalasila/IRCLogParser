import unittest
from lib.analysis import network
import lib.network_util as nx
import lib.util as util
import lib.config as config
import os, mock
import StringIO
import sys
from lib.network_util import connected_components
from numpy.testing import assert_array_equal


class NetworkIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = self.current_directory + "/../../../data/test_lib/test_analysis/network_test/"
        self.log_data = util.load_from_disk(self.test_data_dir + "log_data")
        self.nicks = util.load_from_disk(self.test_data_dir + "nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir + "nick_same_list")

    def tearDown(self):
        self.current_directory = None
        self.test_data_dir = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    @mock.patch('lib.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.config.DEBUGGER', True)
    def test_message_number_graph(self):

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        graph = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertTrue(nx.is_isomorphic(graph, util.load_from_disk(
            self.test_data_dir + "message_number_graph/aggregate_message_number_graph")))

    @mock.patch('lib.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.config.DEBUGGER', True)
    def test_message_number_graph_day_analysis(self):

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        graph = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(
            self.test_data_dir + "message_number_graph/message_number_day_list")

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertTrue(nx.is_isomorphic(graph[0][0], expected_graph_list[0][0]))
        self.assertTrue(nx.is_isomorphic(graph[1][0], expected_graph_list[1][0]))

    @mock.patch('lib.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    def test_message_time_graph(self):

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        msg_time_aggr_graph = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertTrue(nx.is_isomorphic(msg_time_aggr_graph, util.load_from_disk(
            self.test_data_dir + "message_time_graph/msg_time_aggr_graph")))

    @mock.patch('lib.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    def test_message_time_graph_day_analysis(self):

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        msg_time_aggr_graph = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(
            self.test_data_dir + "message_time_graph/msg_time_graph_list")

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertTrue(nx.is_isomorphic(msg_time_aggr_graph[0], expected_graph_list[0]))
        self.assertTrue(nx.is_isomorphic(msg_time_aggr_graph[1], expected_graph_list[1]))

    @mock.patch('lib.config.HOURS_PER_DAY', 24)
    @mock.patch('lib.config.MINS_PER_HOUR', 60)
    @mock.patch('lib.config.BIN_LENGTH_MINS', 60)
    def test_message_number_bins_csv(self):

        expected_bin_matrix = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/bin_matrix")
        expected_tot_msgs = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/tot_msgs")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        bin_matrix, tot_msgs = network.message_number_bins_csv(self.log_data, self.nicks, self.nick_same_list)

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertEqual(bin_matrix, expected_bin_matrix)
        self.assertEqual(tot_msgs, expected_tot_msgs)

    def test_degree_node_number_csv(self):
        expected_out_degree = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/out_degree")
        expected_in_degree = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/in_degree")
        expected_total_degree = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/total_degree")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        out_degree, in_degree, total_degree = network.degree_node_number_csv(self.log_data, self.nicks,
                                                                             self.nick_same_list)

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertEqual(out_degree, expected_out_degree)
        self.assertEqual(in_degree, expected_in_degree)
        self.assertEqual(total_degree, expected_total_degree)

    @mock.patch('lib.config.HOW_MANY_TOP_EXPERTS', 10)
    @mock.patch('lib.config.NUMBER_OF_KEYWORDS_CHANNEL_FOR_OVERLAP', 250)
    @mock.patch('lib.config.DEBUGGER', True)
    def test_identify_hubs_and_experts(self):
        
        log_data = util.load_from_disk(self.test_data_dir + "hits/log_data")
        nicks = util.load_from_disk(self.test_data_dir + "hits/nicks")
        nick_same_list = util.load_from_disk(self.test_data_dir + "hits/nick_same_list")
        expected_top_hub = util.load_from_disk(self.test_data_dir + "hits/top_hub")
        expected_top_keyword_overlap = util.load_from_disk(self.test_data_dir + "hits/top_keyword_overlap")
        expected_top_auth = util.load_from_disk(self.test_data_dir + "hits/top_auth")
        message_graph = util.load_from_disk(self.test_data_dir + "hits/message_graph")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        message_num_graph, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertEqual(top_hub, expected_top_hub)
        self.assertEqual(top_keyword_overlap, expected_top_keyword_overlap)
        self.assertEqual(top_auth, expected_top_auth)
        self.assertTrue(nx.is_isomorphic(message_graph, message_num_graph))


if __name__ == '__main__':
    unittest.main()
