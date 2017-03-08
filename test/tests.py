import unittest
import os
import sys
from os import path
sys.path.insert(0,'../lib')
sys.path.insert(0,'../in_out')
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from lib.analysis import network
from lib import config, nickTracker
from in_out import reader
import networkx as nx
dir = os.path.dirname(__file__)

log_directory = os.path.join(dir, 'data/input/')
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = os.path.join(dir, 'data/output/')

log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

class test_network_methods(unittest.TestCase):

    def test_msg_number_graph(self):
        msg_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)
        expected_msg_number_graph = nx.read_pajek(output_directory+"message_number_graph.net")
        self.assertTrue(nx.is_isomorphic(msg_number_graph,expected_msg_number_graph), msg="test passed")
