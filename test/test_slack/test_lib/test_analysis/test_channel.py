import unittest
import sys
import os
sys.path.insert(0,'../../../../')
from lib.slack.analysis import channel
import lib.slack.util as util

current_directory = os.path.dirname(os.path.realpath(__file__))
 
class ChannelTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory + "/data/log_data")
        self.nicks = util.load_from_disk(current_directory + "/data/nicks")
        self.nick_same_list = util.load_from_disk(current_directory + "/data/nick_same_list")

    def tearDown(self):
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    def test_conv_len_conv_refr_time(self):
        rt_cutoff_time = 1
        cutoff_percentile = 0
        expected_conv_len = util.load_from_disk(current_directory + "/data/conv_len")
        expected_conv_ref_time = util.load_from_disk(current_directory + "/data/conv_ref_time")

        conv_len, conv_ref_time = \
            channel.conv_len_conv_refr_time(self.log_data, self.nicks, self.nick_same_list,
                                            rt_cutoff_time, cutoff_percentile)

        assert conv_len == expected_conv_len, \
            "Error in computing conversation length correctly."
        assert conv_ref_time == expected_conv_ref_time, \
                "Error in computing conversation refresh time correctly."


    def test_response_time_low_cutoff_percentile(self):
        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"

        cutoff_percentile = 0.0
        expected_resp_time = util.load_from_disk(current_directory + "/data/resp_time")
        expected_cutoff_time = 2
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 0% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 0% cutoff percentile."

        cutoff_percentile = 1.0
        expected_resp_time = util.load_from_disk(current_directory + "/data/truncated_rt_1percent")
        expected_cutoff_time = 2
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 1% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 1% cutoff percentile."


    def test_response_time_high_cutoff_percentile(self):
        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"

        cutoff_percentile = 5.0
        expected_resp_time = util.load_from_disk(current_directory + "/data/truncated_rt_5percent")
        expected_cutoff_time = 2
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 5% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 5% cutoff percentile."

        cutoff_percentile = 10.0
        expected_resp_time = util.load_from_disk(current_directory + "/data/truncated_rt_10percent")
        expected_cutoff_time = 2
        resp_time, cutoff_time = channel.response_time(self.log_data, self.nicks,
                                          self.nick_same_list, cutoff_percentile)
        assert resp_time == expected_resp_time, \
                "Error in computing response time with 10% cutoff percentile."
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing RT cutoff with 10% cutoff percentile."


    @staticmethod
    def test_truncate_table_with_short_table():
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


    @staticmethod
    def test_truncate_table_with_long_table():
        resp_time = util.load_from_disk(current_directory + "/data/resp_time")

        expected_cutoff_time = 1067
        cutoff_percentile = 5
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

        cutoff_percentile = 1
        expected_cutoff_time = 1172
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

    @staticmethod
    def test_build_stat_dist():
        assert channel.build_stat_dist([]) == [], "Unable to handle empty list"
        number_list = [0, 9, 1, 0, 6, 3, 0, 0, 0, 0, 0, 13, 1, 0, 15, 6, 0, 0, 0, 0, 0, 0, 3, 7, 0, 7, 3, 0, 0]
        expected_stat_dist = [(0, 17), (1, 2), (2, 0), (3, 3), (4, 0), (5, 0), (6, 2), (7, 2), (8, 0), (9, 1), (10, 0), (11, 0), (12, 0), (13, 1), (14, 0), (15, 1)]

        stat_dist = channel.build_stat_dist(number_list)
        assert stat_dist == expected_stat_dist, "Incorrect result"


if __name__ == '__main__':
    unittest.main()
