import unittest
from lib.analysis import channel
import lib.util as util
import os


class ChannelTest(unittest.TestCase):

    def setUp(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = current_directory + "/../../../data/test_lib/test_analysis/"
        self.log_data = util.load_from_disk(self.test_data_dir+ "/channel/log_data")
        self.nicks = util.load_from_disk(self.test_data_dir+ "/channel/nicks")
        self.nick_same_list = util.load_from_disk(self.test_data_dir+ "/channel/nick_same_list")

    def tearDown(self):
        self.test_data_dir = None
        self.log_data = None
        self.nicks = None
        self.nick_same_list = None

    def test_conv_len_conv_refr_time(self):
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

    def test_response_time_low_cutoff_percentile(self):
        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"

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

    def test_response_time_high_cutoff_percentile(self):
        # this test assumes config.CUTOFF_TIME_STRATEGY = "TWO_SIGMA"

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

if __name__ == '__main__':
    unittest.main()
