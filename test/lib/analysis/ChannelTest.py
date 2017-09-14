import unittest
from lib.analysis import channel
import lib.util as util

class ChannelTest(unittest.TestCase):

    @staticmethod
    def test_conv_len_conv_refr_time():
        log_data = util.load_from_disk("data/log_data")
        nicks = util.load_from_disk("data/nicks")
        nick_same_list = util.load_from_disk("data/nick_same_list")
        expected_conv_len = util.load_from_disk("data/conv_len")
        expected_conv_ref_time = util.load_from_disk("data/conv_ref_time")

        conv_len, conv_ref_time = \
            channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)

        assert conv_len == expected_conv_len, \
            "Error in computing conversation length correctly."
        assert conv_ref_time == expected_conv_ref_time, \
                "Error in computing conversation refresh time correctly."


    @staticmethod
    def test_response_time():
        log_data = util.load_from_disk("data/log_data")
        nicks = util.load_from_disk("data/nicks")
        nick_same_list = util.load_from_disk("data/nick_same_list")
        expected_resp_time = util.load_from_disk("data/resp_time")

        resp_time = channel.response_time(log_data, nicks, nick_same_list)

        assert resp_time == expected_resp_time, \
                "Error in computing response time correctly."


    @staticmethod
    def test_truncate_table_with_short_table():
        resp_time = [(0, 9), (1, 12), (2, 3), (3, 1), (4, 1), (5, 5), (6, 0), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 0), (13, 0), (14, 1), (15, 0), (16, 0), (17, 1), (18, 0), (19, 0), (20, 1)]
        expected_cutoff_time = 14
        cutoff_percentile = 5
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"

        cutoff_percentile = 1
        expected_cutoff_time = 17
        truncated_table, cutoff_time = channel.truncate_table(resp_time, cutoff_percentile)
        assert cutoff_time == expected_cutoff_time, \
                "Error in computing percentile cutoff value"


    @staticmethod
    def test_truncate_table_with_long_table():
        resp_time = util.load_from_disk("data/resp_time")

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


if __name__ == '__main__':
    unittest.main()
