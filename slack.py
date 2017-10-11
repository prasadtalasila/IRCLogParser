from lib.slack.in_out import reader
from lib.in_out import saver
import lib.slack.nickTracker as nickTracker, lib.slack.config as config, lib.vis as vis, lib.validate as validate, lib.slack.util as util
from lib.analysis import network, user, community
from lib.slack.analysis import network, channel
import numpy as np
import networkx as nx
log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

degree_type = ["out_degree", "in_degree", "total_degree"]

# ============== INPUT==================
log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

# ============== ANALYSIS =============
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)

degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)

bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
data = [[i for i in range(len(bin_matrix[0]))]]
data.append([sum(i) for i in zip(*bin_matrix)])

default_cutoff = config.CUTOFF_PERCENTILE
percentiles = [0, 1, 5, 10, 20]

for cutoff in percentiles:
    config.CUTOFF_PERCENTILE = cutoff
    truncated_rt, rt_cutoff_time = channel.response_time(log_data, nicks, nick_same_list, config.CUTOFF_PERCENTILE)
    conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list, rt_cutoff_time, config.CUTOFF_PERCENTILE)
    saver.save_csv(conv_len, output_directory, "conv_len-cutoff-" + str(cutoff))
    saver.save_csv(truncated_rt, output_directory, "resp_time-cutoff-" + str(cutoff))
    saver.save_csv(conv_ref_time, output_directory, "conv_ref_time-cutoff-" + str(cutoff))
    conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, output_directory, "conv_len_cutoff" + str(cutoff))
    resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(truncated_rt, output_directory, "resp_time_cutoff" + str(cutoff))
    conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, output_directory, "conv_ref_time_cutoff" + str(cutoff))
    saver.save_csv( [["a","b","c", "MSE"], [conv_len_curve_fit_parameters]], output_directory,"conv_len_curve_fit_parameters-cutoff-" + str(cutoff))
    saver.save_csv( [["a","b","c", "MSE"], [resp_time_curve_fit_parameters]], output_directory,"resp_time_curve_fit_parameters-cutoff-" + str(cutoff))
    saver.save_csv( [["a","b","c", "MSE"], [conv_ref_time_curve_fit_parameters]], output_directory,"conv_ref_time_curve_fit_parameters-cutoff-"+str(cutoff))

config.CUTOFF_PERCENTILE = default_cutoff #revert back to default

user.keywords_clusters(log_data, nicks, nick_same_list, output_directory, "keywords")
network.degree_analysis_on_graph(message_number_graph)

threshold = config.THRESHOLD_MESSAGE_NUMBER_GRAPH #store original default config
cutoffs = [0, 10, 20]

for cutoff in cutoffs:
    config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff
    msg_graph_experts, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)
    saver.draw_nx_graph (msg_graph_experts, output_directory, "hits-cutoff-"+str(cutoff))

config.THRESHOLD_MESSAGE_NUMBER_GRAPH = threshold #revert to default config

# ============== OUTPUT ================
saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph")
saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph")

saver.save_csv([["response_time_cutoff"], [rt_cutoff_time]], output_directory, "rt_cutoff")
saver.save_csv([["month", "users", "directed_messages"], ["Jan-2013", len(message_number_graph), int(message_number_graph.size('weight'))]], output_directory, "users_messages")

for dtype in degree_type:
    saver.save_csv(degree_anal_message_number[dtype]["formatted_for_csv"], output_directory, dtype)   

saver.save_csv(bin_matrix, output_directory, "MessageNumber_binsize_"+str(config.BIN_LENGTH_MINS)) 

# =============== VIZ ===================
message_graph, message_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'message_number_graph.net')
vis.plot_infomap_igraph(message_graph, message_community.membership, output_directory, "message")
vis.plot_data (data, output_directory, "bins")

for dtype in degree_type:
    slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number[dtype]["raw_for_vis"], output_directory, channel_name[0] +dtype)
    saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory, dtype+"-curve-fit")

"""
# ======================== Heatmap =========================
log_data = reader.linux_input(log_directory, ["#kubuntu-devel"], "2013-1-1", "2013-12-31")
nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
saver.save_csv(bin_matrix, output_directory, "heatmap")
vis.matplotlob_csv_heatmap_generator(output_directory +"heatmap.csv", output_directory, "heatmap-plot")
"""

dates = [ ['2013-1-1','2013-1-31'],['2013-5-1','2013-5-30'] ]
cut_offs = [ 0, 10, 20]

# ================= Message Exchange Network  Single Channel =========================
for date in dates:
    starting_date = date[0]
    ending_date = date[1]
    log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
    nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
    for cutoff in cut_offs:
        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff

        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, output_directory, "message-exchange-" + starting_date + "-cutoff-" + str(cutoff))

        msg_graph, message_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + starting_date + "-cutoff-" + str(cutoff) + '.net')

        vis.plot_infomap_igraph(msg_graph, message_community.membership, output_directory, "message-exchange-" + starting_date + "-cutoff-" +str(cutoff))
