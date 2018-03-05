import unittest
from lib.analysis import channel
import lib.util as util
import os
from mock import patch


class ChannelTest(unittest.TestCase):

    def setUp(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = current_directory + "/../../../data/test_lib/test_analysis/"
        self.log_data = util.load_from_disk(self.test_data_dir+ "/channel/log_data")
        self.nicks = util.load_from_disk(self.test_data_dir+ "/channel/nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir+ "/channel/nick_same_list")
        self.to_graph = util.load_from_disk(self.test_data_dir + "/channel/to_graph")
        self.connected_nick_list = util.load_from_disk(self.test_data_dir + "/channel/connected_nick_list")

    def tearDown(self):
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    def mock_create_connected_nick_list(self,conn_comp_list):
        for i in range(len(conn_comp_list)):
            conn_comp_list[i] = list(conn_comp_list[i])
        return conn_comp_list

    def mock_get_nick_sen_rec(self, iter_range, nick_to_search, conn_comp_list, nick_sen_rec):
        for i in xrange(iter_range):
            if (i < len(conn_comp_list)) and (nick_to_search in conn_comp_list[i]):
                nick_sen_rec = conn_comp_list[i][0]
                break
        return nick_sen_rec

    def mock_correctLastCharCR(self,inText):
        if len(inText) > 1 and inText[len(inText) - 1] == '\\':
            inText = inText[:-1] + 'CR'
        return inText

    def mock_correct_last_char_list(self,rec_list):
        for i in xrange(len(rec_list)):
            if rec_list[i]:
                rec_list[i] = self.mock_correctLastCharCR(rec_list[i])
        return rec_list

    def mock_rec_list_splice(self,rec_list):
        rec_list[1] = rec_list[1][rec_list[1].find(">") + 1:len(rec_list[1])][1:]
        return rec_list

    def mock_check_if_msg_line(self,line):
        return (line[0] != '=' and "] <" in line and "> " in line)

    def mock_splice_find(self,line, search_param1, search_param2, splice_index):
        return self.mock_correctLastCharCR(line[line.find(search_param1) + 1:line.find(search_param2)][splice_index:])

    @patch("lib.analysis.channel.truncate_table", autospec=True)
    @patch("lib.analysis.channel.build_stat_dist")
    @patch("lib.util.splice_find", autospec=True)
    @patch("lib.util.check_if_msg_line", autospec=True)
    @patch("lib.util.rec_list_splice", autospec=True)
    @patch("lib.util.correctLastCharCR", autospec=True)
    @patch("lib.util.correct_last_char_list", autospec=True)
    @patch("lib.util.get_nick_sen_rec", autospec=True)
    @patch("lib.util.create_connected_nick_list", autospec=True)
    @patch("lib.util.to_graph", autospec=True)
    def test_conv_len_conv_refr_time(self,mock_to_graph, mock_connected_nick_list, mock_nick_sen,\
                                     mock_correct_last_char_list,mock_correct_last_char_CR, mock_rec_list_splice,\
                                     mock_msg_line,mock_splice_find, mock_stat_dist, mock_truncate_table):
        mock_to_graph.return_value = self.to_graph
        mock_connected_nick_list.side_effect = self.mock_create_connected_nick_list
        mock_nick_sen.side_effect = self.mock_get_nick_sen_rec
        mock_correct_last_char_list.side_effect = self.mock_correct_last_char_list
        mock_correct_last_char_CR.side_effect = self.mock_correctLastCharCR
        mock_rec_list_splice.side_effect = self.mock_rec_list_splice
        mock_msg_line.side_effect = self.mock_check_if_msg_line
        mock_splice_find.side_effect = self.mock_splice_find
        mock_truncate_table.side_effect = [util.load_from_disk(self.test_data_dir + "/channel/truncate_cl"),
                                           util.load_from_disk(self.test_data_dir + "/channel/truncate_crt")]
        rt_cutoff_time = 1
        cutoff_percentile = 0
        expected_conv_len = util.load_from_disk(self.test_data_dir + "/channel/conv_len")
        expected_conv_ref_time = util.load_from_disk(self.test_data_dir+ "/channel/conv_ref_time")

        conv_len, conv_ref_time = \
            channel.conv_len_conv_refr_time(self.log_data, self.nicks, self.nick_same_list,
                                            rt_cutoff_time, cutoff_percentile)

        assert conv_len == expected_conv_len, \
            "Error in computing conversation length correctly."
        assert conv_ref_time == expected_conv_ref_time, \
                "Error in computing conversation refresh time correctly."

    @patch("lib.analysis.channel.truncate_table", autospec=True)
    @patch("lib.analysis.channel.build_stat_dist")
    @patch("lib.util.splice_find", autospec=True)
    @patch("lib.util.check_if_msg_line", autospec=True)
    @patch("lib.util.rec_list_splice",autospec=True)
    @patch("lib.util.correctLastCharCR",autospec=True)
    @patch("lib.util.correct_last_char_list", autospec=True)
    @patch("lib.util.get_nick_sen_rec", autospec=True)
    @patch("lib.util.create_connected_nick_list", autospec=True)
    @patch("lib.util.to_graph", autospec=True)
    def test_response_time_low_cutoff_percentile(self,mock_to_graph, mock_connected_nick_list, mock_nick_sen,\
                                     mock_correct_last_char_list,mock_correct_last_char_CR, mock_rec_list_splice,\
                                     mock_msg_line,mock_splice_find, mock_stat_dist, mock_truncate_table):

        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"
        mock_to_graph.return_value = self.to_graph
        mock_connected_nick_list.side_effect = self.mock_create_connected_nick_list
        mock_nick_sen.side_effect = self.mock_get_nick_sen_rec
        mock_correct_last_char_list.side_effect = self.mock_correct_last_char_list
        mock_correct_last_char_CR.side_effect = self.mock_correctLastCharCR
        mock_rec_list_splice.side_effect = self.mock_rec_list_splice
        mock_msg_line.side_effect = self.mock_check_if_msg_line
        mock_splice_find.side_effect = self.mock_splice_find
        mock_truncate_table.side_effect = [util.load_from_disk(self.test_data_dir + "/channel/rt_low_0_percent"),
                                           util.load_from_disk(self.test_data_dir + "/channel/rt_low_1_percent")]

        cutoff_percentile = 0.0
        expected_resp_time = util.load_from_disk(self.test_data_dir+ "/channel/resp_time")
        expected_cutoff_time = 1
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 0% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 0% cutoff percentile."

        cutoff_percentile = 1.0
        expected_resp_time = util.load_from_disk(self.test_data_dir+ "/channel/truncated_rt_1percent")
        expected_cutoff_time = 1
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 1% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 1% cutoff percentile."

    @patch("lib.analysis.channel.truncate_table", autospec=True)
    @patch("lib.analysis.channel.build_stat_dist")
    @patch("lib.util.splice_find", autospec=True)
    @patch("lib.util.check_if_msg_line", autospec=True)
    @patch("lib.util.rec_list_splice",autospec=True)
    @patch("lib.util.correctLastCharCR",autospec=True)
    @patch("lib.util.correct_last_char_list", autospec=True)
    @patch("lib.util.get_nick_sen_rec", autospec=True)
    @patch("lib.util.create_connected_nick_list", autospec=True)
    @patch("lib.util.to_graph", autospec=True)
    def test_response_time_high_cutoff_percentile(self,mock_to_graph, mock_connected_nick_list, mock_nick_sen,\
                                     mock_correct_last_char_list,mock_correct_last_char_CR, mock_rec_list_splice,\
                                     mock_msg_line,mock_splice_find, mock_stat_dist, mock_truncate_table):

        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"
        mock_to_graph.return_value = self.to_graph
        mock_connected_nick_list.side_effect = self.mock_create_connected_nick_list
        mock_nick_sen.side_effect = self.mock_get_nick_sen_rec
        mock_correct_last_char_list.side_effect = self.mock_correct_last_char_list
        mock_correct_last_char_CR.side_effect = self.mock_correctLastCharCR
        mock_rec_list_splice.side_effect = self.mock_rec_list_splice
        mock_msg_line.side_effect = self.mock_check_if_msg_line
        mock_splice_find.side_effect = self.mock_splice_find
        mock_truncate_table.side_effect = [util.load_from_disk(self.test_data_dir + "/channel/rt_high_5_percent"),
                                           util.load_from_disk(self.test_data_dir + "/channel/rt_high_10_percent")]

        cutoff_percentile = 5.0
        expected_resp_time = util.load_from_disk(self.test_data_dir+ "/channel/truncated_rt_5percent")
        expected_cutoff_time = 2
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 5% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 5% cutoff percentile."

        cutoff_percentile = 10.0
        expected_resp_time = util.load_from_disk(self.test_data_dir+ "/channel/truncated_rt_10percent")
        expected_cutoff_time = 3
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 10% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 10% cutoff percentile."

    def test_truncate_table_with_short_table(self):
        resp_time = [(0, 9), (1, 12), (2, 3), (3, 1), (4, 1), (5, 5), (6, 0), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 0), (13, 0), (14, 1), (15, 0), (16, 0), (17, 1), (18, 0), (19, 0), (20, 1)]
        expected_cutoff_time = 14
        cutoff_percentile = 5.0
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

        cutoff_percentile = 1.0
        expected_cutoff_time = 17
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

    def test_truncate_table_with_long_table(self):
        resp_time = util.load_from_disk(self.test_data_dir+ "/channel/resp_time")

        expected_cutoff_time = 989
        cutoff_percentile = 5
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

        cutoff_percentile = 1
        expected_cutoff_time = 1436
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

    def test_build_stat_dist(self):
        assert channel.build_stat_dist([]) == [], "Unable to handle empty list"
        number_list = [0, 9, 1, 0, 6, 3, 0, 0, 0, 0, 0, 13, 1, 0, 15, 6, 0, 0, 0, 0, 0, 0, 3, 7, 0, 7, 3, 0, 0]
        expected_stat_dist = [(0, 17), (1, 2), (2, 0), (3, 3), (4, 0), (5, 0), (6, 2), (7, 2), (8, 0), (9, 1), (10, 0), (11, 0), (12, 0), (13, 1), (14, 0), (15, 1)]

        stat_dist = channel.build_stat_dist(number_list)
        assert stat_dist == expected_stat_dist, "Incorrect result"


if __name__ == '__main__':
    unittest.main()