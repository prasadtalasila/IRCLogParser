import unittest
from lib.slack.analysis import network
import networkx as nx
import lib.slack.util as util
import lib.slack.config as config 
import os, mock, sys
import StringIO
from networkx.algorithms.components.connected import connected_components
from numpy.testing import assert_array_equal

    
class NetworkTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.test_data_dir = self.current_directory + "/../../../../data/test_slack/test_lib/test_analysis/network_test/"
        self.log_data = util.load_from_disk(self.test_data_dir + "../log_data")
        self.nicks = util.load_from_disk(self.test_data_dir + "../nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir + "../nick_same_list")

    def tearDown(self):
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None
        
    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.slack.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.slack.config.DEBUGGER', True)
    @mock.patch('lib.slack.util.to_graph', autospec=True)
    @mock.patch('lib.slack.util.create_connected_nick_list', autospec=True)
    @mock.patch('lib.slack.util.check_if_msg_line', autospec=True)
    @mock.patch('lib.slack.util.get_nick_representative', autospec=True)
    @mock.patch('lib.slack.util.get_year_month_day', autospec=True)
    @mock.patch('lib.slack.util.get_nick_sen_rec', autospec=True)
    @mock.patch('lib.slack.util.correctLastCharCR', autospec=True)
    @mock.patch('lib.slack.util.rec_list_splice', autospec=True)
    def test_message_number_graph(self, mock_rec_list_splice, mock_correctLastCharCR, mock_get_nick_sen_rec, mock_get_year_month_day,\
                         mock_get_nick_representative, mock_check_if_msg_line, mock_create_connected_nick_list, mock_to_graph):
        to_graph_ret = util.load_from_disk(self.test_data_dir + "message_number_graph/to_graph")
        
        conn_list = list(connected_components(to_graph_ret))
        
        mock_to_graph.return_value = to_graph_ret
        mock_rec_list_splice.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/rec_list_splice")
        mock_create_connected_nick_list.return_value = util.load_from_disk(self.test_data_dir + "message_number_graph/conn_comp_list")
        #mock_correct_last_char_list.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/correct_last_char_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/check_if_msg_line")
        mock_correctLastCharCR.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/correctLastCharCR")
        mock_get_nick_sen_rec.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_nick_sen_rec")
        #mock_extend_conversation_list.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/extend_conversation_list")
        mock_get_nick_representative.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_nick_representative")
        mock_get_year_month_day.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_year_month_day")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        mock_to_graph.assert_called_once_with(self.nick_same_list)
        mock_create_connected_nick_list.assert_called_once_with(conn_list)
        self.assertTrue(nx.is_isomorphic(ret, util.load_from_disk(self.test_data_dir + "message_number_graph/aggregate_message_number_graph")))

    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.config.THRESHOLD_MESSAGE_NUMBER_GRAPH', 0)
    @mock.patch('lib.slack.config.MINIMUM_NICK_LENGTH', 3)
    @mock.patch('lib.slack.config.DEBUGGER', True)
    @mock.patch('lib.slack.util.to_graph', autospec=True)
    @mock.patch('lib.slack.util.create_connected_nick_list', autospec=True)
    @mock.patch('lib.slack.util.check_if_msg_line', autospec=True)
    @mock.patch('lib.slack.util.get_nick_representative', autospec=True)
    @mock.patch('lib.slack.util.get_year_month_day', autospec=True)
    @mock.patch('lib.slack.util.get_nick_sen_rec', autospec=True)
    @mock.patch('lib.slack.util.correctLastCharCR', autospec=True)
    @mock.patch('lib.slack.util.rec_list_splice', autospec=True)
    def test_message_number_graph_day_analysis(self, mock_rec_list_splice, mock_correctLastCharCR, mock_get_nick_sen_rec, mock_get_year_month_day,\
                         mock_get_nick_representative, mock_check_if_msg_line, mock_create_connected_nick_list, mock_to_graph):
        to_graph_ret = util.load_from_disk(self.test_data_dir + "message_number_graph/to_graph")
        
        conn_list = list(connected_components(to_graph_ret))
        
        mock_to_graph.return_value = to_graph_ret
        mock_rec_list_splice.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/rec_list_splice")
        mock_create_connected_nick_list.return_value = util.load_from_disk(self.test_data_dir + "message_number_graph/conn_comp_list")
        #mock_correct_last_char_list.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/correct_last_char_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/check_if_msg_line")
        mock_correctLastCharCR.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/correctLastCharCR")
        mock_get_nick_sen_rec.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_nick_sen_rec")
        #mock_extend_conversation_list.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/extend_conversation_list")
        mock_get_nick_representative.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_nick_representative")
        mock_get_year_month_day.side_effect = util.load_from_disk(self.test_data_dir + "message_number_graph/get_year_month_day_DAY_ANALYSIS")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_number_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(self.test_data_dir + "message_number_graph/message_number_day_list")
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        mock_to_graph.assert_called_once_with(self.nick_same_list)
        mock_create_connected_nick_list.assert_called_once_with(conn_list)
        self.assertTrue(nx.is_isomorphic(ret[0][0], expected_graph_list[0][0]))
        
    def test_filter_edge_list(self):
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        network.filter_edge_list(self.test_data_dir +'filter_edge_list_input.txt', 10000, 100)
        sys.stdout = sys.__stdout__
        output = capturedOutput.getvalue()
        f = open(self.test_data_dir +'filter_edge_list_out.txt','r')
        expected_output = f.read()
        f.close()
        capturedOutput.close()
        
        self.assertEqual(output, expected_output)
        
    def test_degree_analysis_on_graph(self):
        directed_graph = util.load_from_disk(self.test_data_dir + 'directed_graph')
        directed_deg_analysis_expected = util.load_from_disk(self.test_data_dir + 'directed_deg_analysis_result')
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        directed_deg_analysis = network.degree_analysis_on_graph(directed_graph)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertEqual(directed_deg_analysis, directed_deg_analysis_expected)
    
    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.util.to_graph', autospec=True)
    @mock.patch('lib.slack.util.create_connected_nick_list', autospec=True)
    @mock.patch('lib.slack.util.check_if_msg_line', autospec=True)
    @mock.patch('lib.slack.util.get_nick_sen_rec', autospec=True)
    @mock.patch('lib.slack.util.get_year_month_day', autospec=True)
    @mock.patch('lib.slack.util.correctLastCharCR', autospec=True)
    @mock.patch('lib.slack.util.rec_list_splice', autospec=True)
    def test_message_time_graph(self, mock_rec_list_splice, mock_correctLastCharCR, mock_get_year_month_day, mock_get_nick_sen_rec, mock_check_if_msg_line, mock_create_connected_nick_list, mock_to_graph):
        to_graph_ret = util.load_from_disk(self.test_data_dir + "message_time_graph/to_graph")
        
        conn_list = list(connected_components(to_graph_ret))
        
        mock_to_graph.return_value = to_graph_ret
        mock_rec_list_splice.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/rec_list_splice")
        mock_create_connected_nick_list.return_value = util.load_from_disk(self.test_data_dir + "message_time_graph/conn_comp_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/check_if_msg_line")
        mock_correctLastCharCR.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/correctLastCharCR")
        mock_get_nick_sen_rec.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/get_nick_sen_rec")
        #mock_correct_last_char_list.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/correct_last_char_list")
        mock_get_year_month_day.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/get_year_month_day")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=False)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        mock_to_graph.assert_called_once_with(self.nick_same_list)
        mock_create_connected_nick_list.assert_called_once_with(conn_list)
        self.assertTrue(nx.is_isomorphic(ret, util.load_from_disk(self.test_data_dir + "message_time_graph/msg_time_aggr_graph")))

    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    @mock.patch('lib.slack.util.to_graph', autospec=True)
    @mock.patch('lib.slack.util.create_connected_nick_list', autospec=True)
    @mock.patch('lib.slack.util.check_if_msg_line', autospec=True)
    @mock.patch('lib.slack.util.get_nick_sen_rec', autospec=True)
    @mock.patch('lib.slack.util.get_year_month_day', autospec=True)
    @mock.patch('lib.slack.util.correctLastCharCR', autospec=True)
    @mock.patch('lib.slack.util.rec_list_splice', autospec=True)
    def test_message_time_graph_day_analysis(self, mock_rec_list_splice, mock_correctLastCharCR, mock_get_year_month_day, mock_get_nick_sen_rec, mock_check_if_msg_line, mock_create_connected_nick_list, mock_to_graph):
        to_graph_ret = util.load_from_disk(self.test_data_dir + "message_time_graph/to_graph")
        
        conn_list = list(connected_components(to_graph_ret))
        
        mock_to_graph.return_value = to_graph_ret
        mock_rec_list_splice.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/rec_list_splice")
        mock_create_connected_nick_list.return_value = util.load_from_disk(self.test_data_dir + "message_time_graph/conn_comp_list")
        mock_check_if_msg_line.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/check_if_msg_line")
        mock_correctLastCharCR.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/correctLastCharCR")
        mock_get_nick_sen_rec.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/get_nick_sen_rec")
        #mock_correct_last_char_list.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/correct_last_char_list")
        mock_get_year_month_day.side_effect = util.load_from_disk(self.test_data_dir + "message_time_graph/get_year_month_day")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        ret = network.message_time_graph(self.log_data, self.nicks, self.nick_same_list, DAY_BY_DAY_ANALYSIS=True)
        expected_graph_list = util.load_from_disk(self.test_data_dir + "message_time_graph/msg_time_graph_list")
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        mock_to_graph.assert_called_once_with(self.nick_same_list)
        mock_create_connected_nick_list.assert_called_once_with(conn_list)
        self.assertTrue(nx.is_isomorphic(ret[0], expected_graph_list[0]))
        
    @mock.patch('lib.slack.config.HOURS_PER_DAY', 24)
    @mock.patch('lib.slack.config.MINS_PER_HOUR', 60)
    @mock.patch('lib.slack.config.BIN_LENGTH_MINS', 60)
    @mock.patch('lib.slack.util', autospec=True)
    def test_message_number_bins_csv(self, mock_util):

        mock_util.correctLastCharCR.side_effect = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/correctLastCharCR")
        mock_util.correct_last_char_list.side_effect = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/correct_last_char_list")
        mock_util.rec_list_splice.side_effect = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/rec_list_splice")
        
        bin_matrix_ = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/bin_matrix")
        tot_msgs_ = util.load_from_disk(self.test_data_dir + "message_number_bins_csv/tot_msgs")
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        bin_matrix, tot_msgs = network.message_number_bins_csv(self.log_data, self.nicks, self.nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        self.assertEqual(bin_matrix, bin_matrix_)
        self.assertEqual(tot_msgs, tot_msgs_)
    
    @mock.patch('lib.slack.analysis.network.message_number_graph')
    def test_degree_node_number_csv(self, mock_msg_graph):
        
        msg_num_graph_day_list = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/msg_day_list")
        out_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/out_degree")
        in_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/in_degree")
        total_degree_ = util.load_from_disk(self.test_data_dir + "degree_node_number_csv/total_degree")
        
        mock_msg_graph.return_value = msg_num_graph_day_list
        
        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        
        out_degree, in_degree, total_degree = network.degree_node_number_csv(self.log_data, self.nicks, self.nick_same_list)
        
        sys.stdout = sys.__stdout__
        capturedOutput.close()
        
        mock_msg_graph.assert_called_once_with(self.log_data, self.nicks, self. nick_same_list, True)
        self.assertEqual(out_degree, out_degree_)
        self.assertEqual(in_degree, in_degree_)
        self.assertEqual(total_degree, total_degree_)
    
    @mock.patch('lib.slack.config.MAX_EXPECTED_DIFF_NICKS', 5000)
    def test_nick_receiver_from_conn_comp(self):
        conn_comp_list = [["Rohit", "rohit", "kaushik"], ["krishna", "krish", "acharya"], ["Rohan", "rohan", "ron"]]
        conn_comp_list.extend([[]]*config.MAX_EXPECTED_DIFF_NICKS)
        
        assert network.nick_receiver_from_conn_comp("kaushik", conn_comp_list) == "Rohit"
        assert network.nick_receiver_from_conn_comp("krishna", conn_comp_list) == "krishna"
        assert network.nick_receiver_from_conn_comp("Rohan_goel", conn_comp_list) == ""
        
    @mock.patch('lib.slack.analysis.network.message_number_graph', autospec=True)
    @mock.patch('lib.slack.analysis.network.user.keywords', autospec=True)
    def test_identify_hubs_and_experts(self, mock_keywords, mock_msg_graph):
    
        top_hub_ = util.load_from_disk(self.test_data_dir + "hits/top_hub")
        top_keyword_overlap_ = util.load_from_disk(self.test_data_dir + "hits/top_keyword_overlap")
        top_auth_ = util.load_from_disk(self.test_data_dir + "hits/top_auth")
        message_graph = util.load_from_disk(self.test_data_dir + "hits/message_graph")
        keyword_dict_list = util.load_from_disk(self.test_data_dir + "hits/keyword_dict_list")
        user_keyword_freq_dict = util.load_from_disk(self.test_data_dir + "hits/user_keyword_freq_dict")
        user_words_dict_list = util.load_from_disk(self.test_data_dir + "hits/user_words_dict_list")
        nicks_for_stop_words = util.load_from_disk(self.test_data_dir + "hits/nicks_for_stop_words")
        keywords_for_channels = util.load_from_disk(self.test_data_dir + "hits/keywords_for_channels")
        
        # setup mock
        mock_msg_graph.return_value = message_graph
        mock_keywords.return_value = keyword_dict_list, user_keyword_freq_dict, user_words_dict_list, nicks_for_stop_words, keywords_for_channels
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
