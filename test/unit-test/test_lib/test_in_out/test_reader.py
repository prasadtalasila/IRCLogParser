import unittest
import lib.in_out.reader as reader
import lib.util as util
import lib.config as config
import os, sys
import StringIO
from mock import patch
import re

current_directory = os.path.dirname(os.path.realpath(__file__))

class ReaderTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.starting_date = "2013-1-1" 
        self.ending_date = "2013-1-31"
        self.channel_name = ["#kubuntu-devel"]

    def tearDown(self):
        self.log_data = None
        self.starting_date = None
        self.ending_date = None


    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input(self):
        expected_capturedOutput = util.load_from_disk(current_directory + "/data/stdout_captured_linux_input")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        log_data = reader.linux_input(current_directory + "/data/log/", self.channel_name, self.starting_date, self.ending_date)
        output = capturedOutput.getvalue()
        capturedOutput.close()
        sys.stdout = sys.__stdout__
        #See https://docs.python.org/2/library/re.html for more details.
        # string 'Working on: /any_valid_path/IRCLogParser/test/unit-test/test_lib/test_in_out/data/log/2013/01/04/#kubuntu-devel.txt\n' is replaced by
        # 'Working on: IRCLogParser/test/unit-test/test_lib/test_in_out/data/log/2013/01/04/#kubuntu-devel.txt\n'
        output = re.sub(r'(?P<begin>.+ )/.+/(?P<constant>IRCLogParser/.+\n)', r'\g<begin>\g<constant>', output)
        self.assertEqual(log_data, self.log_data)
        self.assertEqual(expected_capturedOutput, output)

    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_all_channels(self):
        expected_capturedOutput = util.load_from_disk(current_directory + "/data/stdout_captured_linux_input_all_channels")
        expected_log_data = util.load_from_disk(current_directory + "/data/log_data_for_test_linux_input_all_channels")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        log_data = reader.linux_input(current_directory + "/data/log_to_test_for_all_channels/", ["ALL"], "2013-1-1", "2013-1-1")
        output = capturedOutput.getvalue()
        capturedOutput.close()
        sys.stdout = sys.__stdout__
        
        #See https://docs.python.org/2/library/re.html for more details.
        output = re.sub(r'(?P<begin>.+ )/.+/(?P<constant>IRCLogParser/.+\n)', r'\g<begin>\g<constant>', output)

        self.assertEqual(expected_log_data, log_data)
        self.assertEqual(expected_capturedOutput, output)



    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_invalid_path(self):
        with self.assertRaises(IOError) as ex:
            reader.linux_input("some non existent path/", self.channel_name, self.starting_date, self.starting_date)

        self.assertEqual(str(ex.exception), "Path some non existent path/2013/01/01/ doesn't exist")


    @patch("lib.config.DEBUGGER", new = True)
    def test_linux_input_non_existent_file(self):
        expected_captured_output = util.load_from_disk(current_directory + "/data/stdout_captured_linux_input_non_existent_file")

        capturedOutput = StringIO.StringIO()
        sys.stdout = capturedOutput
        log_data = reader.linux_input(current_directory + "/data/log/", ["some non existent file","#kubuntu-devel"], self.starting_date, self.ending_date)
        output = capturedOutput.getvalue()
        capturedOutput.close()
        sys.stdout = sys.__stdout__

        output = re.sub(r'(?P<begin>.+ )/.+/(?P<constant>IRCLogParser/.+\n)',r'\g<begin>\g<constant>', output)
        self.assertEqual(self.log_data, log_data)
        self.assertEqual(expected_captured_output, output)



if __name__ == '__main__':
    unittest.main()
