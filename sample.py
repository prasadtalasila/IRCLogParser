from lib.in_out import reader, saver
import lib.nickTracker as nickTracker, lib.config as config, lib.vis as vis, lib.validate as validate, lib.util as util
from lib.analysis import network, channel, user, community
import numpy as np
import networkx as nx
log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

# ============== INPUT==================
log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

# ============== ANALYSIS =============
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
# message_number_graph_day_list = network.message_number_graph(log_data, nicks, nick_same_list, True)
# print int(message_number_graph.size('weight'))
# print util.count_number_of_users_on_channel(nick_same_list)
# degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)
# message_time_graph_list = network.message_time_graph(log_data, nicks, nick_same_list, True)
# message_time_graph = network.message_time_graph(log_data, nicks, nick_same_list, False)
# out_degree_node_number, in_degree_node_number, total_degree_node_number = network.degree_node_number_csv(log_data, nicks, nick_same_list)
# nick_change_graph_list = user.nick_change_graph(log_data, True)
# bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
# data = [[i for i in range(len(bin_matrix[0]))]]
# data.append([sum(i) for i in zip(*bin_matrix)])
# conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)
# resp_time = channel.response_time(log_data, nicks, nick_same_list)

# user.keywords_clusters(log_data, nicks, nick_same_list)
# network.degree_analysis_on_graph(message_number_graph)
# hits = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)

# adjCC_graph, adjCC_membership = community.infomap_igraph(ig_graph=None, net_file_location="/home/rohan/Desktop/adjCC.net")

# ============== OUTPUT ================
#saver.save_net_nx_graph (message_time_graph, output_directory, "message_time_graph")
#saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph")
# saver.draw_nx_graph (hits, output_directory, "hits")
# saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph")

# saver.save_csv(degree_anal_message_number["out_degree"]["formatted_for_csv"], output_directory, "out_degree")
# saver.save_csv(degree_anal_message_number["in_degree"]["formatted_for_csv"], output_directory, "in_degree")
# saver.save_csv(degree_anal_message_number["total_degree"]["formatted_for_csv"], output_directory, "total_degree")
# saver.save_csv(out_degree_node_number, output_directory, "node_out_degree" + starting_date +'-'+ending_date)
# saver.save_csv(in_degree_node_number, output_directory, "node_in_degree"+ starting_date +'-'+ending_date)
# saver.save_csv(total_degree_node_number, output_directory, "node_total_degree"+ starting_date +'-'+ending_date)
# saver.save_csv(bin_matrix, output_directory, "MessageNumber_binsize_"+str(config.BIN_LENGTH_MINS))
# for i in range(len(nick_change_graph_list)):
    # saver.draw_nx_graph(nick_change_graph_list[i], output_directory, "ncg" + str(i+1))

saver.draw_nx_graph(message_number_graph, output_directory, "mnagg")    
# saver.draw_nx_graph(message_time_graph, output_directory, "mtgagg")
# saver.save_csv(conv_len, output_directory, "conv_len")
# saver.save_csv(resp_time, output_directory, "resp_time")
# saver.save_csv(conv_ref_time, output_directory, "conv_ref_time")

# =============== VIZ ===================
#message_graph, message_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'message_number_graph.net')
#vis.plot_infomap_igraph(message_graph, message_membership, output_directory, "message")
# vis.plot_data (data, output_directory, "bins")
#hits_graph, hits_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'hits.net')
#vis.plot_infomap_igraph(hits_graph, hits_membership, output_directory, "hits")

# conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, 20, output_directory, "conv_len")
# resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(resp_time, 20, output_directory, "resp_time")
# conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, 30, output_directory, "conv_ref_time")
# saver.save_csv( [["a","b","c", "MSE"], [conv_len_curve_fit_parameters]], output_directory,"conv_len_curve_fit_parameters")
# saver.save_csv( [["a","b","c", "MSE"], [resp_time_curve_fit_parameters]], output_directory,"resp_time_curve_fit_parameters")
# saver.save_csv( [["a","b","c", "MSE"], [conv_ref_time_curve_fit_parameters]], output_directory,"conv_ref_time_curve_fit_parameters")

# slope,intercept,r_square,mse = vis.generate_log_plots(9, out_degree_node_number, output_directory, channel_name[0] +"OUT"+ starting_date + ending_date)
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"out-degree-curve-fit")

# slope,intercept,r_square,mse = vis.generate_log_plots(9, in_degree_node_number, output_directory, channel_name[0] +"IN"+ starting_date + ending_date)
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"in-degree-curve-fit")

# slope,intercept,r_square,mse = vis.generate_log_plots(9, total_degree_node_number, output_directory, channel_name[0] +"TOTAL"+ starting_date + ending_date)
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"total-degree-curve-fit")

#slope,intercept,r_square,mse = vis.generate_log_plots(9, degree_anal_message_number["out_degree"]["raw_for_vis"], output_directory, channel_name[0] +"TOTAL")
#saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"out-degree-curve-fit-msg")

# ============== VALIDATION ==============
# validate.validate_RT_RL_CRT(conv_len_curve_fit_parameters, [[10.5, 10.6], [2.12, 2.32], [0, 0.2], [0, 0.0002]], "conv_len")
# validate.validate_RT_RL_CRT(resp_time_curve_fit_parameters, [[0.3, 10.4], [10.3, 30.4], [-0.002, 0.002], [0, 0.002]], "resp_time")
# validate.validate_RT_RL_CRT(conv_ref_time_curve_fit_parameters, [[10.05, 10.1], [0.1, 0.2], [0.02, 0.04], [0, 0.0002], [9, 11]], "conv_ref_time")


# ============== PRESENCE ACROSS MULTIPLE CHANNELS ==============
# Change analysis to all channels in config
# log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)
# nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
# dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

# saver.save_csv(dict_out["UU"]["reducedMatrix"],output_directory, "rUU")
# saver.save_csv(dict_out["CC"]["reducedMatrix"],output_directory, "rCC")
# saver.save_csv(dict_out["CU"]["reducedMatrix"],output_directory, "rCU")
# saver.save_net_nx_graph(dict_out["CC"]["graph"], output_directory, "adjCC")
# saver.save_net_nx_graph(dict_out["CU"]["graph"], output_directory, "adjCU")
# saver.save_net_nx_graph(dict_out["UU"]["graph"], output_directory, "adjUU")
# saver.save_net_nx_graph(dict_out["CC"]["reducedGraph"], output_directory, "radjCC")
# saver.save_net_nx_graph(dict_out["CU"]["reducedGraph"], output_directory, "radjCU")
# saver.save_net_nx_graph(dict_out["UU"]["reducedGraph"], output_directory, "radjUU")
# saver.save_js_arc(dict_out["CC"]["reducedGraph"], channels_hash, "lib/protovis/", "cc.js")
# adjCC_graph, adjCC_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'radjCC.net')
# vis.plot_infomap_igraph(adjCC_graph, adjCC_membership, output_directory, "adjCC_infomaps-reduced")

# adjCU_graph, adjCU_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'radjCU.net')
# vis.plot_infomap_igraph(adjCU_graph, adjCU_membership, output_directory, "adjCU_infomaps-reduced")

# adjUU_graph, adjUU_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'radjUU.net')
# vis.plot_infomap_igraph(adjUU_graph, adjUU_membership, output_directory, "adjUU_infomaps-reduced")

# adjCC_graph, adjCC_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'adjCC.net')
# vis.plot_infomap_igraph(adjCC_graph, adjCC_membership, output_directory, "adjCC_infomaps")

# adjCU_graph, adjCU_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'adjCU.net')
# vis.plot_infomap_igraph(adjCU_graph, adjCU_membership, output_directory, "adjCU_infomaps")

# adjUU_graph, adjUU_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'adjUU.net')
# vis.plot_infomap_igraph(adjUU_graph, adjUU_membership, output_directory, "adjUU_infomaps")

# # ======================== Heatmap =========================
# log_data = reader.linux_input(log_directory, ["#kubuntu-devel"], "2013-1-1", "2013-12-31")
# nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
# bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
# saver.save_csv(bin_matrix, output_directory, "heatmap")
# vis.matplotlob_csv_heatmap_generator(output_directory +"heatmap.csv", output_directory, "heatmap-plot");

# ================= Message Exchange Network =========================
# log_data = reader.linux_input(log_directory, ["#kubuntu-devel","#kubuntu","#ubuntu-devel"], starting_date, ending_date)
# nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)

# dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

# message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
# saver.save_net_nx_graph(message_number_graph, output_directory, "message")

# msg_graph, msg_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'message.net')
# UC_adjacency_matrix = zip(*dict_out["CU"]["matrix"])

# msg_membership = []
# for user in UC_adjacency_matrix:
#     ind = user.index(max(user))
#     msg_membership.append(ind)

# vis.plot_infomap_igraph(msg_graph, msg_membership, output_directory, "message-exchange")
