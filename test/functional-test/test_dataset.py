import unittest
import os
import lib.slack.in_out.reader as reader
import lib.slack.nickTracker as nickTracker
from lib.slack.analysis import network


class DataSetTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data_dir = self.current_directory+"/data/input/slackware/"
        self.start_date = '2013-01-01'
        self.end_date  ='2013-01-08'
        self.expected_result = 137,1754

    def tearDown(self):
        self.current_directory = None
        self.log_data_dir = None
        self.start_date = None
        self.end_date = None
        self.expected_result = None

    def test_dataset(self):
        log_data = reader.linux_input_slack(self.log_data_dir, self.start_date, self.end_date)
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        expected_output = len(message_number_graph), int(message_number_graph.size('weight'))
        self.assertEqual(expected_output, self.expected_result)

if __name__ == '__main__':
    unittest.main()