import unittest
from lib.analysis import network, user
from lib.in_out import reader , saver
from lib import nickTracker
import networkx as nx
import lib.util as util
import lib.config as config
import os
import StringIO
import sys
import filecmp
from networkx.algorithms.components.connected import connected_components
from numpy.testing import assert_array_equal

class UserProfileTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.out_dir = self.current_directory + "/data/output/2013/01/user_tracking/"
        self.log_data =  reader.linux_input(self.current_directory + "/data/input/", ["#kubuntu-devel", "#kubuntu",  "#ubuntu-devel"], "2013-1-1", "2013-1-7")

    def tearDown(self):
        self.current_directory = None
        self.out_dir = None
        self.log_data = None

    def test_user_nick_change_tracking(self):
        expected_nicks = util.load_from_disk(self.out_dir + "nicks")
        expected_nick_same_list = util.load_from_disk(self.out_dir + "nick_same_list")

        nicks, nick_same_list = nickTracker.nick_tracker(self.log_data)

        self.assertEqual(expected_nicks, nicks)
        self.assertEqual(expected_nick_same_list, nick_same_list)

    def test_user_to_channel_tracking(self):
        expected_nicks = util.load_from_disk(self.out_dir + "channel_tracking_nicks")
        expected_nick_same_list = util.load_from_disk(self.out_dir + "channel_tracking_nick_same_list")
        expected_channels_for_user = util.load_from_disk(self.out_dir + "channels_for_user")
        expected_nick_channel_dict = util.load_from_disk(self.out_dir + "nick_channel_dict")
        expected_nicks_hash = util.load_from_disk(self.out_dir + "nicks_hash")
        expected_channel_hash = util.load_from_disk(self.out_dir + "channels_hash")

        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(self.log_data, True)

        self.assertEqual(expected_nicks, nicks)
        self.assertEqual(expected_nick_same_list, nick_same_list)
        self.assertEqual(expected_channels_for_user, channels_for_user)
        self.assertEqual(expected_nick_channel_dict, nick_channel_dict)
        self.assertEqual(expected_nicks_hash, nicks_hash)
        self.assertEqual(expected_channel_hash,  channels_hash)

    def test_keyword_digest(self):

        nicks, nick_same_list = nickTracker.nick_tracker(self.log_data)

        user.keywords_clusters(self.log_data, nicks, nick_same_list, "./",  "temp_keywords")

        self.assertTrue(filecmp.cmp(self.out_dir + "temp_keywords.txt", "temp_keywords.txt"))
        os.remove("temp_keywords.txt")

    def test_identify_hubs_and_experts(self):

        expected_top_hub = util.load_from_disk(self.out_dir+ "top_hub")
        expected_top_keyword_overlap = util.load_from_disk(self.out_dir+ "top_keyword_overlap")
        expected_top_auth = util.load_from_disk(self.out_dir+ "top_auth")
        expected_message_graph = util.load_from_disk(self.out_dir + "message_num_graph")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput

        nicks, nick_same_list = nickTracker.nick_tracker(self.log_data)
        message_num_graph, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(self.log_data, nicks, nick_same_list)

        sys.stdout = sys.__stdout__
        capturedOutput.close()

        self.assertEqual(top_hub, expected_top_hub)
        self.assertEqual(top_keyword_overlap, expected_top_keyword_overlap)
        self.assertEqual(top_auth, expected_top_auth)
        self.assertTrue(nx.is_isomorphic(expected_message_graph, message_num_graph))

if __name__ == '__main__':
    unittest.main()
