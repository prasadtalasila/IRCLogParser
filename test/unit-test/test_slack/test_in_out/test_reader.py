import unittest
import lib.slack.in_out.reader as reader
import lib.slack.util as util
import lib.slack.config as config
import os, sys
import StringIO
from mock import patch
import re


class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data = util.load_from_disk(self.current_directory+ "/data/log_data")
        self.starting_date = "2013-1-1" 
        self.ending_date = "2013-1-31"


    def tearDown(self):
        self.current_directory = None
        self.log_data = None
        self.starting_date = None
        self.ending_date = None


    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_slack(self):
        expected_captured_output = util.load_from_disk(self.current_directory +"/data/stdout_captured_linux_input_slack")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        log_data = reader.linux_input_slack(self.current_directory + "/data/slackware/", self.starting_date, self.ending_date)
        output = capturedOutput.getvalue()
        capturedOutput.close()
        sys.stdout = sys.__stdout__

        #See https://docs.python.org/2/library/re.html for more details.
        # string 'Working on: /any_valid_path/IRCLogParser/test/unit-test/test_lib/test_in_out/data/log/2013/01/04/#kubuntu-devel.txt\n' is replaced by
        # 'Working on: IRCLogParser/test/unit-test/test_lib/test_in_out/data/log/2013/01/04/#kubuntu-devel.txt\n'
        output = re.sub(r'(?P<begin>.+ )/.+/(?P<constant>IRCLogParser/.+\n)',r'\g<begin>\g<constant>', output)
        self.assertEqual(log_data, self.log_data)
        self.assertEqual(expected_captured_output, output)


    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_invalid_path_slack(self):
        with self.assertRaises(IOError) as ex:
            capturedOutput = StringIO.StringIO()
            sys.stdout = capturedOutput
            reader.linux_input_slack("some non existent path/", self.starting_date, self.starting_date)
            capturedOutput.close()
            sys.stdout = sys.__stdout__

        self.assertEqual(str(ex.exception), "Path some non existent path/2013/ doesn't exist")


    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_non_existent_file_slack(self):
        expected_captured_output = util.load_from_disk(self.current_directory + "/data/stdout_captured_linux_input_slack_non_existent_file")
        expected_log_data = util.load_from_disk(self.current_directory + "/data/log_data_for_test_linux_input_non_existent_file_slack")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        log_data = reader.linux_input_slack(self.current_directory + "/data/slackware_with_missing_files/", "2013-1-1","2013-1-6")
        output = capturedOutput.getvalue()
        capturedOutput.close()
        sys.stdout = sys.__stdout__

        #See https://docs.python.org/2/library/re.html for more details.
        output = re.sub(r'(?P<begin>.+ )/.+/(?P<constant>IRCLogParser/.+\n)',r'\g<begin>\g<constant>', output)
        self.assertEqual(expected_log_data, log_data)
        self.assertEqual(expected_captured_output, output)

if __name__ == '__main__':
    unittest.main()
