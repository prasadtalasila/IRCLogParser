import unittest
import lib.slack.nickTracker as nickTracker
import lib.slack.util as util
import os


class NickTrackerTest(unittest.TestCase):
    
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data = util.load_from_disk(self.current_directory+ "/data/log_data")
        self.nicks1 = util.load_from_disk(self.current_directory+ "/data/nicks1")
        self.nick_same_list1 = util.load_from_disk(self.current_directory+ "/data/nick_same_list1")
        
    def tearDown(self):
        self.current_directory = None
        self.log_data = None
        self.nicks1 = None
        self.nick_same_list1 = None

    def test_nick_tracker(self):
        nicks, nick_same_list = nickTracker.nick_tracker(self.log_data)
        self.assertEqual(nicks, self.nicks1)
        self.assertEqual(nick_same_list, self.nick_same_list1)
        

if __name__ == '__main__':
    unittest.main()
