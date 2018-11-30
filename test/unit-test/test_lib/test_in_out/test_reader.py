import unittest
import os, sys
import datetime
from datetime import datetime as dt
from itertools import islice
from lib.in_out import reader
from lib.in_out.reader import ReaderFactory, LinuxReaderFactory, Reader, UbuntuReader, SlackReader, ScummVMReader


class LinuxInputTest(unittest.TestCase):
	
	def test_linux_input(self):	
	
		current_directory = os.path.dirname(os.path.realpath(__file__))
		log_data = current_directory+ "/data/log"
		start_date_str = "2013-1-1"
		end_date_str = "2013-1-1"
		channel_name = ["#kubuntu-devel", "slackware", "scummvm", "invalid_channel"]
		expected_output_ubuntu = {'log_data': '=== Mamarok_ is now known as Mamarok\n', 'auxiliary_data': {'month': 1, 'day': 1, 'channel': '#kubuntu-devel', 'year': 2013}}
		expected_output_slack = {'log_data': '[00:07:50] <TheM4ch1n3> ah\n', 'auxiliary_data': {'month': 1, 'day': 1, 'channel': 'slackware', 'year': 2013}}
		expected_output_scummvm = {'log_data': 'p0\n', 'auxiliary_data': {'month': 1, 'day': 1, 'channel': 'scummvm', 'year': 2013}}
		
		log_dir = reader.linux_input(log_data, channel_name, start_date_str, end_date_str)
		self.assertEqual(log_dir.values()[0][10], expected_output_ubuntu)
		self.assertEqual(log_dir.values()[0][14], expected_output_slack)
		self.assertEqual(log_dir.values()[0][34], expected_output_scummvm)

class ReaderFactoryTest(unittest.TestCase):
  
    def test_reader_object(self):	    
	    pass


class LinuxReaderFactoryTest(ReaderFactoryTest, unittest.TestCase):

    def test_reader_object(self):    
        
        linuxReader = LinuxReaderFactory()
        self.assertIsInstance(linuxReader.reader_object("#kubuntu-devel"), UbuntuReader)
        self.assertIsInstance(linuxReader.reader_object("slackware"), SlackReader)
        self.assertIsInstance(linuxReader.reader_object("scummvm"), ScummVMReader)


class ReaderTest(unittest.TestCase):

	def setUp(self):
		
		self.current_directory = os.path.dirname(os.path.realpath(__file__))
		self.log_data = self.current_directory+ "/data/log"
		self.start_date = dt.strptime("2013-1-1", '%Y-%m-%d')
		self.end_date = dt.strptime("2013-1-1", '%Y-%m-%d')
		self.channel_name = ["#kubuntu-devel", "slackware", "scummvm"]	
			
		self.start_date_2 = dt.strptime("2000-1-1", '%Y-%m-%d')
		self.end_date_2 = dt.strptime("2000-1-1", '%Y-%m-%d')
		
		self.ubuntu_expected_output_1 = ('#kubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== LordOfTime is now known as TheLordOfTime\n')
		self.ubuntu_expected_output_2 = ('#kubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== Mamarok_ is now known as Mamarok\n')
		self.ubuntu_expected_output_3 = ('#ubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== nerd is now known as superbot\n')
		
		self.slack_expected_output = ('slackware', datetime.datetime(2013, 1, 1, 0, 0), '[00:06:41] Guest86829 (~alejandro@190.250.76.206) left irc: Quit: Lost terminal\n')
		self.scummvm_expected_output = ('scummvm', datetime.datetime(2013, 1, 1, 0, 0), 'ccollections\n')
		
		self.ubuntuReader = UbuntuReader()
		self.slackReader = SlackReader()
		self.scummvmReader = ScummVMReader()

	def tearDown(self):	
	
		self.log_data = None
		self.start_date = None
		self.end_date = None
		self.channel_name= None		
		
		self.start_date_2 = None
		self.end_date_2 = None
		
		self.ubuntu_expected_output_1 = None
		self.ubuntu_expected_output_2 = None
		self.ubuntu_expected_output_3 = None
		
		self.slack_expected_output = None
		self.scummvm_expected_output = None
		
		self.ubuntuReader = None
		self.slackReader = None
		self.scummvmReader = None

	def test_build_path(self):	    
	    pass
	    
	def test_read_single_channel_log(self):		
		pass
		
	def test_read_log(self):	
		pass
					

class UbuntuReaderTest(ReaderTest, unittest.TestCase):
	
    def test_build_path(self):
        path = self.ubuntuReader._build_path(self.log_data, self.start_date, self.channel_name[0])
        self.assertEqual(path, self.log_data+"/2013/01/01/#kubuntu-devel.txt")
        
    def test_read_single_channel_log(self):	
    	
        output = tuple(self.ubuntuReader._read_single_channel_log(self.log_data, self.channel_name[0], self.start_date, self.end_date))		
        self.assertEqual(output[0], self.ubuntu_expected_output_1)
        with self.assertRaises(IOError):
            tuple(self.ubuntuReader._read_single_channel_log(self.log_data, self.channel_name[0], self.start_date_2, self.end_date_2))           
        
    def test_read_multi_channel_logs(self):	
    
        output = self.ubuntuReader._read_multi_channel_logs(self.log_data, [self.channel_name[0], "#ubuntu-devel"], self.start_date, self.end_date)		
        output_to_check = []
        for i in islice(output, 0, 2):
            for j in islice(i, 10, 11):
                output_to_check.append(j)		
		
        self.assertEqual(output_to_check[0], self.ubuntu_expected_output_2)
        self.assertEqual(output_to_check[1], self.ubuntu_expected_output_3)
        
    def test_read_all_channel_logs(self):
         output = self.ubuntuReader._read_all_channel_logs(self.log_data, self.start_date, self.end_date)
         output_to_check = []
         for i in islice(output, 19, 20):
            for j in islice(i, 0, 1):
                output_to_check.append(j)
         self.assertEqual(output_to_check[0], self.ubuntu_expected_output_1)
    	
    def test_read_log(self):
		        
        output1 = self.ubuntuReader.read_log(self.log_data, ["ALL"], self.start_date, self.end_date)
        output2 = tuple(self.ubuntuReader.read_log(self.log_data, [self.channel_name[0]], self.start_date, self.end_date))
        output3 = self.ubuntuReader.read_log(self.log_data, [self.channel_name[0], "#ubuntu-devel"], self.start_date, self.end_date)
        output1_to_check = []
        output3_to_check = []
        
        for i in islice(output1, 19, 20):
            for j in islice(i, 0, 1):
                output1_to_check.append(j)        
        for i in islice(output3, 0, 2):
            for j in islice(i, 10, 11):
                output3_to_check.append(j)		
        
        self.assertEqual(output1_to_check[0], self.ubuntu_expected_output_1)
        self.assertEqual(output2[0], self.ubuntu_expected_output_1)
        self.assertEqual(output3_to_check[0], self.ubuntu_expected_output_2)
        self.assertEqual(output3_to_check[1], self.ubuntu_expected_output_3)

		
class SlackReaderTest(ReaderTest, unittest.TestCase):    
    
    def test_build_path(self):
	
        path = self.slackReader._build_path(self.log_data, self.start_date, self.channel_name[1])
        self.assertEqual(path, self.log_data+"/2013/slackware.20130101.log")
		
    def test_read_single_channel_log(self):
		
        output = tuple(self.slackReader._read_single_channel_log(self.log_data, self.channel_name[1], self.start_date, self.end_date))		
        self.assertEqual(output[0], self.slack_expected_output)
        with self.assertRaises(IOError):
            tuple(self.slackReader._read_single_channel_log(self.log_data, self.channel_name[1], self.start_date_2, self.end_date_2))       	
		
    def test_read_log(self):
	
        self.assertIsNotNone(tuple(self.slackReader.read_log(self.log_data, [self.channel_name[1]], self.start_date, self.end_date)))
        with self.assertRaises(IOError):
            tuple(self.slackReader.read_log(self.log_data, [self.channel_name[1]], self.start_date_2, self.end_date_2))


class ScummVMReaderTest(ReaderTest, unittest.TestCase):
    
    def test_build_path(self):
	
        path = self.scummvmReader._build_path(self.log_data, self.start_date, self.channel_name[2])
        self.assertEqual(path, self.log_data+"/2013/01/01/scummvm.txt")
		
    def test_read_single_channel_log(self):
		
        output = tuple(self.scummvmReader._read_single_channel_log(self.log_data, self.channel_name[2], self.start_date, self.end_date))		
        self.assertEqual(output[0], self.scummvm_expected_output)
        with self.assertRaises(IOError):
            tuple(self.scummvmReader._read_single_channel_log(self.log_data, self.channel_name[2], self.start_date_2, self.end_date_2)) 

    def test_read_log(self):
	
        self.assertIsNotNone(tuple(self.scummvmReader.read_log(self.log_data, [self.channel_name[2]], self.start_date, self.end_date)))
        with self.assertRaises(IOError):
            tuple(self.scummvmReader.read_log(self.log_data, [self.channel_name[2]], self.start_date_2, self.end_date_2))

				
if __name__ == '__main__':
    unittest.main()
    
