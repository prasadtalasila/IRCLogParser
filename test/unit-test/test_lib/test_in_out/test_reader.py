import unittest
import os, sys
import datetime
from datetime import datetime as dt
from itertools import islice
from lib.in_out import reader
from lib.in_out.reader import Reader, UbuntuReader, SlackReader, ScummVMReader

class LinuxInputTest(unittest.TestCase):
	
	def test_linux_input(self):
	
		current_directory = os.path.dirname(os.path.realpath(__file__))
		log_data = current_directory+ "/data/log"
		start_date_str = "2013-1-1"
		end_date_str = "2013-1-1"
		channel_name = ["#kubuntu-devel"]
		expected_output={'log_data': '=== Mamarok_ is now known as Mamarok\n', 'auxiliary_data': {'month': 1, 'day': 1, 'channel': '#kubuntu-devel', 'year': 2013}}
		
		log_dir=reader.linux_input(log_data, channel_name, start_date_str, end_date_str)
		self.assertEqual(log_dir.values()[0][10], expected_output)
		
		
class ReaderTest(unittest.TestCase):

	def setUp(self):
	
		self.current_directory = os.path.dirname(os.path.realpath(__file__))
		self.log_data = self.current_directory+ "/data/log"
		self.start_date = dt.strptime("2013-1-1", '%Y-%m-%d')
		self.end_date = dt.strptime("2013-1-1", '%Y-%m-%d')
		self.channel_name = ["#kubuntu-devel"]
		
		self.start_date_2 = dt.strptime("2000-1-1", '%Y-%m-%d')
		self.end_date_2 = dt.strptime("2000-1-1", '%Y-%m-%d')
		self.expected_output1= ('#kubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== LordOfTime is now known as TheLordOfTime\n')
		self.expected_output2= ('#kubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== Mamarok_ is now known as Mamarok\n')
		self.expected_output3= ('#ubuntu-devel', datetime.datetime(2013, 1, 1, 0, 0), '=== nerd is now known as superbot\n')

	def tearDown(self):
	
		self.log_data = None
		self.start_date = None
		self.end_date = None
		self.channel_name= None
		
		self.start_date_2 = None
		self.end_date_2 = None
		self.expected_output1= None
		self.expected_output2= None
		self.expected_output3= None

	def test_build_path(self):
	
		path= Reader()._build_path(self.log_data, self.start_date, self.channel_name[0])
		self.assertEqual(path, self.log_data+"/2013/01/01/#kubuntu-devel.txt")
	
	def test_read_single_channel_log(self):
		
		output= tuple(Reader()._read_single_channel_log(self.log_data, self.channel_name[0], self.start_date, self.end_date))		
		self.assertEqual(output[0], self.expected_output1)
		with self.assertRaises(IOError):
			tuple(Reader()._read_single_channel_log(self.log_data, self.channel_name[0], self.start_date_2, self.end_date_2))

	def test_read_log(self):
	
		output1= tuple(Reader().read_log(self.log_data, self.channel_name, self.start_date, self.end_date))
		self.assertEqual(output1[0], self.expected_output1)
		output2= Reader().read_log(self.log_data, self.channel_name+ ["#ubuntu-devel"], self.start_date, self.end_date)
		output3= Reader().read_log(self.log_data, ["ALL"], self.start_date, self.end_date)
		self.assertIsNone(output2)
		self.assertIsNone(output3)
			

class UbuntuReaderTest(ReaderTest,unittest.TestCase):
	
	def test_read_multi_channel_logs(self):
	
		output= UbuntuReader()._read_multi_channel_logs(self.log_data, self.channel_name+ ["#ubuntu-devel"], self.start_date, self.end_date)		
		output_to_check= []
		for i in islice(output, 0, 2):
			for j in islice(i, 10, 11):
				output_to_check.append(j)		
		
		self.assertEqual(output_to_check[0], self.expected_output2)
		self.assertEqual(output_to_check[1], self.expected_output3)
	
	def test_read_log(self):
		
		output1= UbuntuReader().read_log(self.log_data, ["ALL"], self.start_date, self.end_date)
		output2= tuple(UbuntuReader().read_log(self.log_data, self.channel_name, self.start_date, self.end_date))
		output3= UbuntuReader().read_log(self.log_data, self.channel_name+ ["#ubuntu-devel"], self.start_date, self.end_date)
		output3_to_check=[]
		for i in islice(output3, 0, 2):
			for j in islice(i, 10, 11):
				output3_to_check.append(j)
				
		self.assertIsNone(output1)
		self.assertEqual(output2[0], self.expected_output1)
		self.assertEqual(output3_to_check[0], self.expected_output2)
		self.assertEqual(output3_to_check[1], self.expected_output3)

		
class SlackReaderTest(ReaderTest,unittest.TestCase):

	def test_build_path(self):
	
		path= SlackReader()._build_path(self.log_data, self.start_date, self.channel_name[0])
		self.assertEqual(path, self.log_data+"/2013/#kubuntu-devel.20130101.log")
		
	def test_read_log(self):
	
		self.assertIsNotNone(tuple(SlackReader().read_log(self.log_data, self.start_date, self.end_date)))
		with self.assertRaises(IOError):
			tuple(SlackReader().read_log(self.log_data, self.start_date_2, self.end_date_2))


class TestScummVMReader(ReaderTest, unittest.TestCase):

	def test_read_log(self):
	
		self.assertIsNotNone(tuple(ScummVMReader().read_log(self.log_data, self.start_date, self.end_date)))
		with self.assertRaises(IOError):
			tuple(ScummVMReader().read_log(self.log_data, self.start_date_2, self.end_date_2))

				
if __name__ == '__main__':
    unittest.main()
