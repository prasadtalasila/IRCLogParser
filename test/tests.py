import unittest
import os
import sys
import csv
import pickle
import json
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib.analysis import network, user, channel
from lib.nickTracker import nick_tracker
from ddt import ddt, data, unpack
from lib import config
from in_out import reader
import networkx as nx
current_dir = os.path.dirname(__file__)

log_directory = os.path.join(current_dir, 'data/input/')
expected_output_directory = os.path.join(current_dir, 'data/output/')
channel_name = config.CHANNEL_NAME
log_for_jan = reader.linux_input(log_directory, channel_name, "2013-1-1", "2013-1-31")
nicks_for_jan, nick_same_list_for_jan = nick_tracker(log_for_jan)
log_for_aug = reader.linux_input(log_directory, channel_name, "2013-8-1", "2013-8-31")
nicks_for_aug, nick_same_list_for_aug = nick_tracker(log_for_aug)

def update_expected_output_directory(log_data):
    key = log_data.keys()[0]  #get any key as months and year will be same since log_data has monthly data
    global expected_output_directory
    expected_output_directory = os.path.join(current_dir, 'data/output/' + str(key.year)+'/')
    month = key.month
    temp = str(month)
    if (month < 10):
        temp = '0' + str(month)
    expected_output_directory += temp +'/'


def compare_graph_outputs(generated_output, stored_output_file_name):
    expected_output = nx.read_gpickle(expected_output_directory+stored_output_file_name)
    if(nx.is_isomorphic(generated_output, expected_output)):
        return True
    return False


def csv_to_list(csv_path, gen_list, data_in_tuples=True):
    with open(csv_path, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            tup = tuple(int(x) for x in row)
            if (not data_in_tuples):
                tup = list(tup)
            gen_list.append(tup)

def unpickle(filename, expected_output):
    with open(expected_output_directory+filename, 'rb') as f:
        expected_output.extend(pickle.load(f))

def unjson(filename, expected_output):
    with open(expected_output_directory+filename) as f:
        expected_output.append(json.load(f))

@ddt
class test_methods_returning_networkx_graphs(unittest.TestCase):

    def setUp(self):
        pass


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_message_number_graph(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        msg_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)
        self.assertTrue(compare_graph_outputs(msg_number_graph, "message_number_graph.gpickle"), msg=None)


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_msg_time_graph(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        msg_time_graph = network.message_time_graph(log_data, nicks, nick_same_list)
        self.assertTrue(compare_graph_outputs(msg_time_graph, "message_time_graph.gpickle"), msg=None)


    @data(log_for_jan, log_for_aug)
    def test_nick_change_graph(self, log_data):
        update_expected_output_directory(log_data)
        nick_change_graph = user.nick_change_graph(log_data)
        self.assertTrue(compare_graph_outputs(nick_change_graph, "nick_change_graph.gpickle"), msg=None)


    @data(log_for_jan, log_for_aug)
    def test_full_presence_graph(self, log_data):
        update_expected_output_directory(log_data)
        nicks1, nick_same_list1, channels_for_user1, nick_channel_dict1, \
                         nicks_hash1, channels_hash1 = nick_tracker(log_data, True)
        dict_out, graph = network.channel_user_presence_graph_and_csv(nicks1, nick_same_list1, \
                                                                      channels_for_user1, nick_channel_dict1, \
                                                                      nicks_hash1, channels_hash1)
        self.assertTrue(compare_graph_outputs(graph, "full_presence_graph.gpickle"), msg=None)


@ddt
class test_methods_returning_lists(unittest.TestCase):

    def setUp(self):
        pass


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_conv_len_conv_refr_time(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)

        expected_con_len = []
        expected_conv_ref_time = []
        csv_to_list(expected_output_directory+'conv_len.csv', expected_con_len)
        csv_to_list(expected_output_directory+'conv_ref_time.csv', expected_conv_ref_time)

        self.assertListEqual(conv_len, expected_con_len, msg=None)
        self.assertListEqual(conv_ref_time, expected_conv_ref_time, msg=None)


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_response_time_from_channel_lib(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        resp_time = channel.response_time(log_data, nicks, nick_same_list)

        expected_resp_time = []
        csv_to_list(expected_output_directory + 'resp_time.csv', expected_resp_time)
        self.assertListEqual(resp_time, expected_resp_time, msg=None)


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_message_number_bins_csv(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        msg_number_bins_csv, total_msg = network.message_number_bins_csv(log_data, nicks, nick_same_list)

        expected_output = []
        csv_to_list(expected_output_directory + 'message_number_binsize_30.csv', expected_output, False)
        self.assertListEqual(msg_number_bins_csv, expected_output, msg=None)


    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_degree_node_number_csv(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        out_degree, in_degree, total_degree = network.degree_node_number_csv(log_data, \
                                                                             nicks, nick_same_list)

        expected_out_degree = []
        expected_in_degree = []
        expected_total_degree = []

        unpickle('node_in_degree.pkl', expected_in_degree)
        unpickle('node_out_degree.pkl', expected_out_degree)
        unpickle('node_total_degree.pkl', expected_total_degree)

        self.assertListEqual(out_degree, expected_out_degree, msg=None)
        self.assertListEqual(in_degree, expected_in_degree, msg=None)
        self.assertListEqual(total_degree, expected_total_degree, msg=None)


@ddt
class test_methods_performing_intermediate_analysis(unittest.TestCase):

    def setUp(self):
        pass

    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_degree_analysis_on_nodes(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)
        message_time_graph = network.message_time_graph(log_data, nicks, nick_same_list)
        nick_change_graph = user.nick_change_graph(log_data)

        degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)
        degree_anal_message_time = network.degree_analysis_on_graph(message_time_graph)
        degree_anal_nick_change = network.degree_analysis_on_graph(nick_change_graph)

        expected_analysis_msg_number = []
        expected_analysis_msg_time = []
        expected_analysis_nick_change = []

        unjson('degree_anal_message_number.json', expected_analysis_msg_number)
        unjson('degree_anal_message_time.json', expected_analysis_msg_time)
        unjson('degree_anal_nick_change.json', expected_analysis_nick_change)

        self.assertDictEqual(degree_anal_message_number, expected_analysis_msg_number[0], msg=None)
        self.assertDictEqual(degree_anal_message_time, expected_analysis_msg_time[0], msg=None)
        self.assertDictEqual(degree_anal_nick_change, expected_analysis_nick_change[0], msg=None)

    @data((log_for_jan, nicks_for_jan, nick_same_list_for_jan), \
          (log_for_aug, nicks_for_aug, nick_same_list_for_aug))
    @unpack
    def test_keyword_analysis_methods(self, log_data, nicks, nick_same_list):
        update_expected_output_directory(log_data)
        keywords_filtered, user_keyword_freq_dict, user_words_dict, nicks_for_stop_words, keywords_for_channels = \
                           user.keywords(log_data, nicks, nick_same_list);
        expected_keywords_filtered = []
        expected_user_keyword_freq_dict = []
        expected_user_word_dict = []
        expected_nicks_for_stop_words = []

        unjson('keywords_filtered.json', expected_keywords_filtered)
        unjson('user_words_dict.json', expected_user_word_dict)
        unjson('user_keyword_freq_dict.json', expected_user_keyword_freq_dict)
        unjson('nicks_for_stop_words.json', expected_nicks_for_stop_words)

        self.assertListEqual(user_keyword_freq_dict, expected_user_keyword_freq_dict[0], msg=None)
        self.assertListEqual(user_words_dict, expected_user_word_dict[0], msg=None)
        self.assertListEqual(keywords_filtered,expected_keywords_filtered[0])
        self.assertListEqual(nicks_for_stop_words,expected_nicks_for_stop_words[0])
