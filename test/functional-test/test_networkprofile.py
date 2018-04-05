import os
import unittest

import networkx as nx
import numpy as np
from igraph.clustering import compare_communities

import lib.config as config
import lib.nickTracker as nickTracker
import lib.util as util
import lib.vis as vis
from lib.analysis import network, channel, community
from lib.in_out import reader, saver


class NetworkProfileTest(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data_dir = self.current_directory + "/data/input/"
        self.start_date = '2013-01-01'
        self.end_date = '2013-01-08'

    def tearDown(self):
        self.current_directory = None
        self.log_data_dir = None
        self.start_date = None
        self.end_date = None

    def test_presence_networks(self):
        log_data = reader.linux_input(self.log_data_dir, ["ALL"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/presence_graph_dict')
        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
        expected_output, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user,
                                                                             nick_channel_dict, nicks_hash, channels_hash)
        edge_types = ['CC', 'UU', 'CU']
        for edge_type in edge_types:
            self.assertTrue(nx.is_isomorphic(expected_output[edge_type]['graph'], expected_result[edge_type]['graph']))
            self.assertTrue(nx.is_isomorphic(expected_output[edge_type]['reducedGraph'], expected_result[edge_type]['reducedGraph']))
            expected_output[edge_type].pop('graph')
            expected_output[edge_type].pop('reducedGraph')
            expected_result[edge_type].pop('graph')
            expected_result[edge_type].pop('reducedGraph')
        np.testing.assert_equal(expected_output, expected_result)

    def test_message_exchange_network(self):
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/degree_anal_message_number_graph_kubuntu-devel')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        expected_output = network.degree_analysis_on_graph(message_number_graph)
        self.assertEqual(expected_result, expected_output)

    def test_reduced_networks_cutoff_0(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 0
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_0')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result, expected_output))

    def test_reduced_networks_cutoff_10(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 10
        print "10 default:{} config{}".format(default_config, config.THRESHOLD_MESSAGE_NUMBER_GRAPH)
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_10')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result, expected_output))

    def test_reduced_networks_cutoff_20(self):
        default_config = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 20
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_number_graph_cutoff_20')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
        expected_output = network.message_number_graph(log_data, nicks, nick_same_list, False)
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_config
        self.assertTrue(nx.is_isomorphic(expected_result, expected_output))

    def test_degree_distribution_message_exchange_network(self):
        degree_type = ["out_degree", "in_degree", "total_degree"]
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/message_exchange_network_curve_fit')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)
        expected_output = {}
        for dtype in degree_type:
            expected_output[dtype] = vis.generate_log_plots(degree_anal_message_number[dtype]["raw_for_vis"],
                                                            self.current_directory, "#kubuntu-devel" + dtype)
            os.remove(self.current_directory + "/#kubuntu-devel" + dtype + ".png")
        self.assertEqual(expected_result, expected_output)

    def test_degree_distribution_multi_channel(self):
        log_data = reader.linux_input(self.log_data_dir, ["ALL"], self.start_date, self.end_date)
        expected_result_CC_degree_curve_fit = util.load_from_disk(self.current_directory + '/data/output/CC_degree_curve_fit')
        expected_result_CU_degree_curve_fit = util.load_from_disk(self.current_directory + '/data/output/CU_degree_curve_fit')
        expected_result_UU_degree_curve_fit = util.load_from_disk(self.current_directory + '/data/output/UU_degree_curve_fit')

        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
        dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user,
                                                                      nick_channel_dict, nicks_hash, channels_hash)
        degree_anal_message_number_CC = network.degree_analysis_on_graph(dict_out["CC"]["graph"], directed=False)
        degree_anal_message_number_UU = network.degree_analysis_on_graph(dict_out["UU"]["graph"], directed=False)
        degree_anal_message_number_CU = network.degree_analysis_on_graph(dict_out["CU"]["graph"], directed=False)

        Y = degree_anal_message_number_CU["degree"]["raw_for_vis"][1:]
        data = [(i, Y[i]) for i in range(len(Y))]
        CU_truncated, cutoff = channel.truncate_table(data, 0.5)
        CU_T = [data[1] for data in list(CU_truncated)]
        expected_output_CC_degree_curve_fit = vis.generate_log_plots(degree_anal_message_number_CC["degree"]["raw_for_vis"],
                                                                    self.current_directory, "CC_degree_curve_fit")

        expected_output_CU_degree_curve_fit = vis.generate_log_plots(CU_T, self.current_directory,
                                                                     "CU_degree_curve_fit")

        expected_output_UU_degree_curve_fit = vis.generate_log_plots(degree_anal_message_number_UU["degree"]["raw_for_vis"],
                                                                    self.current_directory, "UU_degree_curve_fit")
        os.remove(self.current_directory + "/CC_degree_curve_fit" + ".png")
        os.remove(self.current_directory + "/CU_degree_curve_fit" + ".png")
        os.remove(self.current_directory + "/UU_degree_curve_fit" + ".png")

        self.assertEqual(expected_result_CC_degree_curve_fit, expected_output_CC_degree_curve_fit)
        self.assertEqual(expected_result_CU_degree_curve_fit, expected_output_CU_degree_curve_fit)
        self.assertEqual(expected_result_UU_degree_curve_fit, expected_output_UU_degree_curve_fit)

    def test_community_analysis_single_channel_cutoff_0(self):
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/community_analysis_single_channel_cutoff_0')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        default_cutoff = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 0
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, self.current_directory, "message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH))

        expected_output = community.infomap_igraph(ig_graph=None,net_file_location=self.current_directory + "/message-exchange-"
                                                                                       + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')

        os.remove(self.current_directory + "/message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_cutoff

        self.assertTrue(expected_result[0].isomorphic(expected_output[0]))
        self.assertEqual(compare_communities(expected_result[1],expected_output[1]),0)

    def test_community_analysis_single_channel_cutoff_10(self):
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/community_analysis_single_channel_cutoff_10')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        default_cutoff = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 10
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, self.current_directory,"message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH))

        expected_output = community.infomap_igraph(ig_graph=None,net_file_location=self.current_directory + "/message-exchange-"
                                                                     + self.start_date + "-cutoff-" + str( config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')
        os.remove(self.current_directory + "/message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_cutoff

        self.assertTrue(expected_result[0].isomorphic(expected_output[0]))
        self.assertEqual(compare_communities(expected_result[1],expected_output[1]),0)

    def test_community_analysis_single_channel_cutoff_20(self):
        log_data = reader.linux_input(self.log_data_dir, ["#kubuntu-devel"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/community_analysis_single_channel_cutoff_20')
        nicks, nick_same_list = nickTracker.nick_tracker(log_data)
        default_cutoff = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 20
        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, self.current_directory,"message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH))

        expected_output = community.infomap_igraph(ig_graph=None, net_file_location=self.current_directory + "/message-exchange-"
                                                                     + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')
        os.remove(self.current_directory + "/message-exchange-" + self.start_date + "-cutoff-" + str(config.THRESHOLD_MESSAGE_NUMBER_GRAPH) + '.net')
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = default_cutoff

        self.assertTrue(expected_result[0].isomorphic(expected_output[0]))
        self.assertEqual(compare_communities(expected_result[1],expected_output[1]),0)

    def test_community_analysis_multi_channel(self):
        log_data = reader.linux_input(self.log_data_dir, ["ALL"], self.start_date, self.end_date)
        expected_result = util.load_from_disk(self.current_directory + '/data/output/community_analysis_multi_channel')
        nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
        dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user,
                                                                      nick_channel_dict, nicks_hash, channels_hash)

        presence_type = ["CC", "UU", "CU"]
        expected_output = {ptype: {} for ptype in presence_type}
        for ptype in presence_type:
            saver.save_net_nx_graph(dict_out[ptype]["graph"], self.current_directory, "adj" + ptype)
            saver.save_net_nx_graph(dict_out[ptype]["reducedGraph"], self.current_directory, "radj" + ptype)
            expected_output[ptype]['adj'] = community.infomap_igraph(ig_graph=None,
                                                                     net_file_location=self.current_directory + '/adj' + ptype + '.net')
            expected_output[ptype]['radj'] = community.infomap_igraph(ig_graph=None,
                                                                      net_file_location=self.current_directory + '/radj' + ptype + '.net')

            os.remove(self.current_directory + '/adj' + ptype + '.net')
            os.remove(self.current_directory + '/radj' + ptype + '.net')

            self.assertTrue(expected_result[ptype]['adj'][0].isomorphic(expected_output[ptype]['adj'][0]))
            self.assertEqual(compare_communities(expected_output[ptype]['adj'][1], expected_result[ptype]['adj'][1]), 0)
            self.assertTrue(expected_result[ptype]['radj'][0].isomorphic(expected_output[ptype]['radj'][0]))
            self.assertEqual(compare_communities(expected_output[ptype]['radj'][1], expected_result[ptype]['radj'][1]),0)


if __name__ == '__main__':
    unittest.main()