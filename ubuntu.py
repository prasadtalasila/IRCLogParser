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

degree_type = ["out_degree", "in_degree", "total_degree"]
presence_type = ["CC", "UU", "CU"]

# ============== INPUT==================
log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

# ============== ANALYSIS =============
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)

degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)

bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
data = [[i for i in range(len(bin_matrix[0]))]]
data.append([sum(i) for i in zip(*bin_matrix)])

truncated_rt, rt_cutoff_time = channel.response_time(log_data, nicks, nick_same_list, config.CUTOFF_PERCENTILE)
conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list, rt_cutoff_time, config.CUTOFF_PERCENTILE)

user.keywords_clusters(log_data, nicks, nick_same_list, output_directory, "keywords")
network.degree_analysis_on_graph(message_number_graph)
hits = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)

# ============== OUTPUT ================
saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph")
saver.draw_nx_graph (hits, output_directory, "hits")
saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph")

saver.save_csv([["response_time_cutoff"], [rt_cutoff_time]], output_directory, "rt_cutoff")
saver.save_csv([["month", "users", "directed_messages"], ["Jan-2013", len(message_number_graph), int(message_number_graph.size('weight'))]], output_directory, "users_messages")

for dtype in degree_type:
    saver.save_csv(degree_anal_message_number[dtype]["formatted_for_csv"], output_directory, dtype)   

saver.save_csv(bin_matrix, output_directory, "MessageNumber_binsize_"+str(config.BIN_LENGTH_MINS))

saver.draw_nx_graph(message_number_graph, output_directory, "mnagg")    

saver.save_csv(conv_len, output_directory, "conv_len")
saver.save_csv(truncated_rt, output_directory, "resp_time")
saver.save_csv(conv_ref_time, output_directory, "conv_ref_time")

# =============== VIZ ===================
message_graph, message_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'message_number_graph.net')
vis.plot_infomap_igraph(message_graph, message_membership, output_directory, "message")
vis.plot_data (data, output_directory, "bins")

conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, output_directory, "conv_len")
resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(truncated_rt, output_directory, "resp_time")
conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, output_directory, "conv_ref_time")
saver.save_csv( [["a","b","c", "MSE"], [conv_len_curve_fit_parameters]], output_directory,"conv_len_curve_fit_parameters")
saver.save_csv( [["a","b","c", "MSE"], [resp_time_curve_fit_parameters]], output_directory,"resp_time_curve_fit_parameters")
saver.save_csv( [["a","b","c", "MSE"], [conv_ref_time_curve_fit_parameters]], output_directory,"conv_ref_time_curve_fit_parameters")

for dtype in degree_type:
    slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number[dtype]["raw_for_vis"], output_directory, channel_name[0] +dtype)
    saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory, dtype+"-curve-fit")

# ============== PRESENCE ACROSS MULTIPLE CHANNELS ==============
# Change analysis to all channels in config
log_data = reader.linux_input(log_directory, ["ALL"], starting_date, ending_date)
nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

saver.save_js_arc(dict_out["CC"]["reducedGraph"], channels_hash, config.OUTPUT_DIRECTORY + "protovis/", "cc.js")

for ptype in presence_type:
    saver.save_csv(dict_out[ptype]["reducedMatrix"],output_directory, "r"+ptype)
    saver.save_net_nx_graph(dict_out[ptype]["graph"], output_directory, "adj"+ptype)
    saver.save_net_nx_graph(dict_out[ptype]["reducedGraph"], output_directory, "radj"+ptype)
    radj_graph, radj_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'radj'+ptype+'.net')
    vis.plot_infomap_igraph(radj_graph, radj_membership, output_directory, "radj"+ptype+"_infomaps-reduced")
    adj_graph, adj_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'adj'+ptype+'.net')
    vis.plot_infomap_igraph(adj_graph, adj_membership, output_directory, "adj"+ptype+"_infomaps-full")

degree_anal_message_number_CC = network.degree_analysis_on_graph(dict_out["CC"]["graph"], directed=False)

saver.save_csv(degree_anal_message_number_CC["degree"]["formatted_for_csv"], output_directory, "CC_degree")
degree_anal_message_number_UU = network.degree_analysis_on_graph(dict_out["UU"]["graph"], directed = False)
saver.save_csv(degree_anal_message_number_UU["degree"]["formatted_for_csv"], output_directory, "UU_degree")
degree_anal_message_number_CU = network.degree_analysis_on_graph(dict_out["CU"]["graph"], directed=False)
saver.save_csv(degree_anal_message_number_CU["degree"]["formatted_for_csv"], output_directory, "CU_degree")

slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number_CC["degree"]["raw_for_vis"], output_directory, "CC_degree_curve_fit")
saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"CC-degree-curve-fit")

slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number_CU["degree"]["raw_for_vis"], output_directory, "CU_degre_curve_fit")
saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"CU-degree-curve-fit")

slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number_UU["degree"]["raw_for_vis"], output_directory, "UU_degree_curve_fit")
saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"UU-degree-curve-fit")

# ======================== Heatmap =========================
log_data = reader.linux_input(log_directory, ["#kubuntu-devel"], "2013-1-1", "2013-12-31")
nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
saver.save_csv(bin_matrix, output_directory, "heatmap")
vis.matplotlob_csv_heatmap_generator(output_directory +"heatmap.csv", output_directory, "heatmap-plot")

dates = [ ['2013-1-1','2013-1-31'],['2013-5-1','2013-5-30'] ]
cut_offs = [ 0, 10, 20]

# ================= Message Exchange Network  Single Channel =========================
for date in dates:
    starting_date = date[0]
    ending_date = date[1]
    for cutoff in cut_offs:
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff
        log_data = reader.linux_input(log_directory, ["#kubuntu-devel"], starting_date, ending_date)
        nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)


        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, output_directory, "message-exchange-" + starting_date + "-cutoff-" + str(cutoff))

        msg_graph, msg_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + starting_date + "-cutoff-" + str(cutoff) + '.net')

        vis.plot_infomap_igraph(msg_graph, msg_membership, output_directory, "message-exchange-" + starting_date + "-cutoff-" +str(cutoff))
        
# ================= Message Exchange Network Multi Channel =========================

for date in dates:
    starting_date = date[0]
    ending_date = date[1]
    log_data = reader.linux_input(log_directory, ["#kubuntu-devel", "#kubuntu", "#ubuntu-devel"], starting_date, ending_date)
    nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
    for cutoff in cut_offs:
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff

        dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, output_directory, "message-exchange-" + starting_date + "-multi-cutoff-"+str(cutoff))

        msg_graph, msg_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + starting_date + "-multi-cutoff-" + str(cutoff) +".net")
        UC_adjacency_matrix = zip(*dict_out["CU"]["matrix"])

        vis.plot_infomap_igraph(msg_graph, msg_membership, output_directory, "message-exchange-" + starting_date + "-multi-cutoff-"+str(cutoff), aux_data = {"type": "MULTI_CH", "uc_adj": UC_adjacency_matrix, "user_hash": nicks_hash})
