import unittest
from lib.analysis import user
import lib.util as util
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class UserTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks_hash = util.load_from_disk(current_directory+ "/data/nicks_hash")

    def tearDown(self):
        self.log_data = None
        self.nicks_hash = None

    def test_nick_change_graph(self):
        pass
    
    def test_top_keywords_for_nick(self):
        pass
    
    def test_keywords(self):
        pass
        
    def test_keywords_clusters(self):
        pass
        
    def test_extended_stop_words(self):
        pass

if __name__ == '__main__':
    unittest.main()
