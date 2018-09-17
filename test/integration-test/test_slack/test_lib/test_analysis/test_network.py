import unittest
from lib.slack.analysis import network
import lib.network_util as nx
import lib.slack.util as util
import lib.slack.config as config 
import os, mock, sys
import StringIO
from numpy.testing import assert_array_equal

    
class NetworkTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = self.current_directory + "/../../../../data/test_slack/test_lib/test_analysis/network_test/"
        self.log_data = util.load_from_disk(self.test_data_dir + "../log_data")
        self.nicks = util.load_from_disk(self.test_data_dir + "../nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir + "../nick_same_list")

    def tearDown(self):
        self.current_directory = None
        self.test_data_dir = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None
        
    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.slack.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.slack.config.DEBUGGER', True)
    def test_message_number_graph(self):
        to_graph_ret = util.load_from_disk(self.test_data_dir + "message_number_graph/to_graph")
        
        conn_list = list(nx.connected_components(to_graph_ret))
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertTrue(nx.is_isomorphic(ret, util.load_from_disk(self.test_data_dir + "message_number_graph/aggregate_message_number_graph")))

    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.slack.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.slack.config.DEBUGGER', True)
    def test_message_number_graph_day_analysis(self):
    
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(self.test_data_dir + "message_number_graph/message_number_day_list")
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertTrue(nx.is_isomorphic(ret[0][0], expected_graph_list[0][0]))
    
    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    def test_message_time_graph(self):
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertTrue(nx.is_isomorphic(ret, util.load_from_disk(self.test_data_dir + "message_time_graph/msg_time_aggr_graph")))

    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    def test_message_time_graph_day_analysis(self):
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(self.test_data_dir + "message_time_graph/msg_time_graph_list")
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertTrue(nx.is_isomorphic(ret[0], expected_graph_list[0]))
        
    @mock.patch('lib.slack.config.HOURS_PER_DAY', 24)
    @mock.patch('lib.slack.config.MINS_PER_HOUR', 60)
    @mock.patch('lib.slack.config.BIN_LENGTH_MINS', 60)
    def test_message_number_bins_csv(self):
        
        bin_matrix_ = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/bin_matrix")
        tot_msgs_ = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/tot_msgs")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        bin_matrix, tot_msgs = network.message_number_bins_csv(self.log_data, self.nicks, self.nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertEqual(bin_matrix, bin_matrix_)
        self.assertEqual(tot_msgs, tot_msgs_)
    
    def test_degree_node_number_csv(self):
        
        out_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/out_degree")
        in_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/in_degree")
        total_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/total_degree")
        
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        out_degree, in_degree, total_degree = network.degree_node_number_csv(self.log_data, self.nicks, self.nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertEqual(out_degree, out_degree_)
        self.assertEqual(in_degree, in_degree_)
        self.assertEqual(total_degree, total_degree_)
    
        
    @mock.patch('lib.slack.config.HOW_MANY_TOP_EXPERTS', 10)
    @mock.patch('lib.slack.config.NUMBER_OF_KEYWORDS_CHANNEL_FOR_OVERLAP', 250)
    @mock.patch('lib.slack.config.DEBUGGER', True)
    def test_identify_hubs_and_experts(self):
    
        top_hub_ = util.load_from_disk(self.test_data_dir + "hits/top_hub")
        top_keyword_overlap_ = util.load_from_disk(self.test_data_dir + "hits/top_keyword_overlap")
        top_auth_ = util.load_from_disk(self.test_data_dir + "hits/top_auth")
        message_graph = util.load_from_disk(self.test_data_dir + "hits/message_graph")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        message_num_graph, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(self.log_data, self.nicks, self.nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertEqual(top_hub, top_hub_)
        self.assertEqual(top_keyword_overlap, top_keyword_overlap_)
        self.assertEqual(top_auth, top_auth_) 
        self.assertTrue(nx.is_isomorphic(message_graph, message_num_graph))

if __name__ == '__main__':
    unittest.main()
