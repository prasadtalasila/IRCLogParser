import unittest
import lib.nickTracker as nickTracker
import lib.util as util
import os
import StringIO
import sys
from mock import patch


class NickTrackerTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        self.current_directory = None
    
    @patch("lib.config.MAX_EXPECTED_DIFF_NICKS", new = 5000)
    @patch("lib.config.DEBUGGER", new = True)
    @patch("lib.nickTracker.searchChannel", autospec = True)
    @patch("lib.util.splice_find", autospec = True)
    @patch("lib.util.correctLastCharCR", autospec = True)
    @patch("lib.util.check_if_msg_line", autospec = True)
    def test_nick_tracker(self, mock_check_if_msg_line, mock_correctLastCharCR, mock_splice_find, mock_searchChannel):

        log_data_dat = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/log_data")
        nick_same_list_data = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/nick_same_list")
        correctLastCharCR_data = util.load_from_disk(self.current_directory + "/data/correctLastCharCR_list")
        check_if_msg_line_data = util.load_from_disk(self.current_directory + "/data/check_if_msg_line_list")
        splice_find_data = util.load_from_disk(self.current_directory + "/data/splice_find_list")

        log_data = log_data_dat
        mock_searchChannel.side_effect = util.load_from_disk(self.current_directory + "/data/searchChannel_list1")
        mock_splice_find.side_effect = splice_find_data
        mock_correctLastCharCR.side_effect = correctLastCharCR_data
        mock_check_if_msg_line.side_effect = check_if_msg_line_data

        expected_nicks1 = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/nicks1")
        expected_nick_same_list = nick_same_list_data
        expected_output = util.load_from_disk(self.current_directory + "/data/stdout_nick_tracker1")

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, track_users_on_channels = False)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_nicks1, nicks)
        self.assertEqual(expected_nick_same_list, nick_same_list)
        self.assertEqual(expected_output, output)


        log_data = log_data_dat

        mock_searchChannel.side_effect = util.load_from_disk(self.current_directory + "/data/searchChannel_list2")
        mock_splice_find.side_effect = splice_find_data
        mock_correctLastCharCR.side_effect = correctLastCharCR_data
        mock_check_if_msg_line.side_effect = check_if_msg_line_data

        expected_channels_for_user = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/channels_for_user")
        expected_nick_channel_dict = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/nick_channel_dict")
        expected_nicks_hash = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/nicks_hash")
        expected_channels_hash = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/channels_hash")
        expected_output = util.load_from_disk(self.current_directory + "/data/stdout_nick_tracker2")
        expected_nicks2 = util.load_from_disk(self.current_directory + "/../../data/test_lib/nickTracker/nicks2")
        expected_nick_same_list = nick_same_list_data

        captured_output = StringIO.StringIO()
        sys.stdout = captured_output
        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, track_users_on_channels = True)
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        captured_output.close()

        self.assertEqual(expected_nicks2, nicks)
        self.assertEqual(expected_nick_same_list, nick_same_list)
        self.assertEqual(expected_output, output)
        self.assertEqual(expected_channels_for_user ,channels_for_user)
        self.assertEqual(expected_nick_channel_dict ,nick_channel_dict)
        self.assertEqual(expected_nicks_hash, nicks_hash)
        self.assertEqual(expected_channels_hash, channels_hash)


    def test_searchChannel(self):
        channels = [["#ubuntu",0], ["#kubuntu",0], ["#kubuntu-devel",0], ["#ubuntu-devel",0]]
        self.assertEqual(nickTracker.searchChannel("#kubuntu",channels),1)

if __name__ == '__main__':
    unittest.main()
