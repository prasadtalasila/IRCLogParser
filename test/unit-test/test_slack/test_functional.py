import unittest
import sys
from os import path
import networkx as nx
sys.path.insert(0,"../../")
from lib.slack import config, util

class util_test(unittest.TestCase):

    def test_rec_list_splice(self):
        line = "[01:00:49] <Skywise> is it new years yet?"
        rec_list = [e.strip() for e in line.split(':')]
        util.rec_list_splice(rec_list)
        self.assertListEqual(rec_list,['[01', '00', "is it new years yet?"])

    def test_slack_check_if_msg_line(self):
        self.assertTrue(util.check_if_msg_line('[01:02:33] <shonudo> thanks ;'))
        self.assertTrue(util.check_if_msg_line('[01:00:49] <Skywise> is it new years yet?'))         
     

if __name__ == '__main__':
    unittest.main()
