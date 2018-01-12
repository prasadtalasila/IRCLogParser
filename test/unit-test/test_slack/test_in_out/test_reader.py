import unittest
import lib.slack.in_out.reader as reader
import lib.slack.util as util
import lib.slack.config as config
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class ReaderTest(unittest.TestCase):
    
    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.starting_date = "2013-1-1" 
        self.ending_date = "2013-1-31"
        
        
    def tearDown(self):
        self.log_data = None
        self.starting_date = None
        self.ending_date = None

    def test_nick_tracker(self):
        log_data = reader.linux_input_slack(current_directory + "/data/slackware/", self.starting_date, self.ending_date)
        
        assert log_data == self.log_data
        
if __name__ == '__main__':
    unittest.main()
