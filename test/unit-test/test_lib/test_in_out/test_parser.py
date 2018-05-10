import logging
import unittest

from mock import patch

import lib.in_out.parser as parser


class UbuntuParserTest(unittest.TestCase):

    def setUp(self):
        self.UbuntuParser = parser.Parser('ubuntu')

    def tearDown(self):
        self.UbuntuParser = None

    def test_parse_log_nick_change(self):
        log_line = '=== bhuvan is now known as bhuvan_gupta ==='
        expected_result = {
            'old_nick': 'bhuvan',
            'new_nick': 'bhuvan_gupta',
            'type':     'NICK_CHANGE',
            'channel':  'ubuntu'
        }
        expected_output = self.UbuntuParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.UbuntuParser.nicks, ['bhuvan_gupta'])

        log_line = '=== bhuvan_gupta is now known as gupta_bhuvan ==='
        expected_result = {
            'old_nick': 'bhuvan_gupta',
            'new_nick': 'gupta_bhuvan',
            'type': 'NICK_CHANGE',
            'channel': 'ubuntu'
        }
        expected_output = self.UbuntuParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.UbuntuParser.nicks, ['gupta_bhuvan'])

        self.UbuntuParser.reset_state()
        self.assertFalse(self.UbuntuParser.nicks)

    def test_parse_log_directed_message(self):
        log_line = '[00:22] <foo> bar: I have an interface in ifconfigwo'
        expected_result = {
            'channel': 'ubuntu',
            'message': 'I have an interface in ifconfigwo',
            'receivers': ['bar'],
            'sender_nick': 'foo',
            'time': '00:22',
            'type': 'DIRECTED_MESSAGE'
        }
        expected_output = self.UbuntuParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)

    def test_parse_log_undirected_message(self):
        data = '[00:22] <foo> I will design a new parser module'
        expected_result = {
            'message': 'I will design a new parser module',
            'sender_nick': 'foo',
            'time': '00:22',
            'type': 'UNDIRECTED_MESSAGE',
            'channel': 'ubuntu'
        }
        expected_output = self.UbuntuParser.parse_log(data)
        self.assertEqual(expected_output, expected_result)

    @patch('logging.exception', autospec=True)
    def test_parse_log_unknown_format(self, mock_logging):
        data = 'This must go haywire'
        a = self.UbuntuParser.parse_log(data)
        logging.exception.assert_called_once_with('Unknown Log Pattern Found')


class SlackParserTest(unittest.TestCase):

    def setUp(self):
        self.SlackParser = parser.Parser('slack')

    def tearDown(self):
        self.SlackParser = None

    def test_parse_log_nick_change(self):
        log_line = '[00:18:00] Nick change: bhuvan -> bhuvan_gupta'
        expected_result = {
            'old_nick': 'bhuvan',
            'new_nick': 'bhuvan_gupta',
            'type': 'NICK_CHANGE',
            'channel': 'slack'
        }
        expected_output = self.SlackParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.SlackParser.nicks, ['bhuvan_gupta'])

        log_line = '[00:18:00] Nick change: bhuvan_gupta -> gupta_bhuvan'
        expected_result = {
            'old_nick': 'bhuvan_gupta',
            'new_nick': 'gupta_bhuvan',
            'type': 'NICK_CHANGE',
            'channel': 'slack'
        }
        expected_output = self.SlackParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.SlackParser.nicks, ['gupta_bhuvan'])

        self.SlackParser.reset_state()
        self.assertFalse(self.SlackParser.nicks)

    def test_parse_log_directed_message(self):
        log_line = '[00:22:12] <foo> bar: I have an interface in ifconfigwo'
        expected_result = {
            'channel': 'slack',
            'message': 'I have an interface in ifconfigwo',
            'receivers': ['bar'],
            'sender_nick': 'foo',
            'time': '00:22:12',
            'type': 'DIRECTED_MESSAGE'
        }
        expected_output = self.SlackParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)

    def test_parse_log_undirected_message(self):
        data = '[00:22:45] <foo> I will design a new parser module'
        expected_result = {
            'message': 'I will design a new parser module',
            'sender_nick': 'foo',
            'time': '00:22:45',
            'type': 'UNDIRECTED_MESSAGE',
            'channel': 'slack'
        }
        expected_output = self.SlackParser.parse_log(data)
        self.assertEqual(expected_output, expected_result)

    @patch('logging.exception', autospec=True)
    def test_parse_log_unknown_format(self, mock_logging):
        data = 'This must go haywire'
        a = self.SlackParser.parse_log(data)
        logging.exception.assert_called_once_with('Unknown Log Pattern Found')


class ScummvmParserTest(unittest.TestCase):

    def setUp(self):
        self.ScummvmParser = parser.Parser('scummvm')

    def tearDown(self):
        self.ScummvmParser = None

    def test_parse_log_nick_change(self):
        log_line = '[00:18] Nick change: bhuvan -> bhuvan_gupta'
        expected_result = {
            'old_nick': 'bhuvan',
            'new_nick': 'bhuvan_gupta',
            'type': 'NICK_CHANGE',
            'channel': 'scummvm'
        }
        expected_output = self.ScummvmParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.ScummvmParser.nicks, ['bhuvan_gupta'])

        log_line = '[00:18] Nick change: bhuvan_gupta -> gupta_bhuvan'
        expected_result = {
            'old_nick': 'bhuvan_gupta',
            'new_nick': 'gupta_bhuvan',
            'type': 'NICK_CHANGE',
            'channel': 'scummvm'
        }
        expected_output = self.ScummvmParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)
        self.assertEqual(self.ScummvmParser.nicks, ['gupta_bhuvan'])

        self.ScummvmParser.reset_state()
        self.assertFalse(self.ScummvmParser.nicks)

    def test_parse_log_directed_message(self):
        log_line = '[00:22] <foo> bar: I have an interface in ifconfigwo'
        expected_result = {
            'channel': 'scummvm',
            'message': 'I have an interface in ifconfigwo',
            'receivers': ['bar'],
            'sender_nick': 'foo',
            'time': '00:22',
            'type': 'DIRECTED_MESSAGE'
        }
        expected_output = self.ScummvmParser.parse_log(log_line)
        self.assertEqual(expected_output, expected_result)

    def test_parse_log_undirected_message(self):
        data = '[00:22] <foo> I will design a new parser module'
        expected_result = {
            'message': 'I will design a new parser module',
            'sender_nick': 'foo',
            'time': '00:22',
            'type': 'UNDIRECTED_MESSAGE',
            'channel': 'scummvm'
        }
        expected_output = self.ScummvmParser.parse_log(data)
        self.assertEqual(expected_output, expected_result)

    @patch('logging.exception', autospec=True)
    def test_parse_log_unknown_format(self, mock_logging):
        data = 'This must go haywire'
        a = self.ScummvmParser.parse_log(data)
        logging.exception.assert_called_once_with('Unknown Log Pattern Found')
        

if __name__ == '__main__':
    unittest.main()
