import unittest
import lib.slack.nickTracker as nickTracker
import lib.slack.util as util
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class NickTrackerTest(unittest.TestCase):
    
    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks1 = util.load_from_disk(current_directory+ "/data/nicks1")
        self.nick_same_list1 = util.load_from_disk(current_directory+ "/data/nick_same_list1")
        self.nicks2 = util.load_from_disk(current_directory+ "/data/nicks2")
        self.nick_same_list2 = util.load_from_disk(current_directory+ "/data/nick_same_list2")
        self.channels_for_user = util.load_from_disk(current_directory+ "/data/channels_for_user")
        self.nick_channel_dict = util.load_from_disk(current_directory+ "/data/nick_channel_dict")
        self.nicks_hash = util.load_from_disk(current_directory+ "/data/nicks_hash")
        self.channels_hash = util.load_from_disk(current_directory+ "/data/channels_hash")
        
    def tearDown(self):
        self.log_data = None
        self.nicks1 = None
        self.nick_same_list1 = None

    def test_nick_tracker(self):
        nicks, nick_same_list = nickTracker.nick_tracker(self.log_data, track_users_on_channels = False)
        assert nicks == self.nicks1
        assert nick_same_list == self.nick_same_list1
        
        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(self.log_data, track_users_on_channels = True)
        assert nicks == self.nicks2
        assert nick_same_list == self.nick_same_list2
        assert channels_for_user == self.channels_for_user
        assert nicks_hash == self.nicks_hash
        assert channels_hash == self.channels_hash

if __name__ == '__main__':
    unittest.main()
