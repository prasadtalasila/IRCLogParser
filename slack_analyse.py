from lib.slack.in_out import slackReader as reader
from lib.in_out import saver
import lib.slack.slackNickTracker as nickTracker, lib.slack.slackConfig as config, lib.vis as vis, lib.validate as validate, lib.util as util
from lib.analysis import channel, user, community
from lib.slack.analysis import slackNetwork as network
import numpy as np
import networkx as nx
log_directory = config.LOG_DIRECTORY
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

# ============== INPUT==================
log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

# ============== ANALYSIS =============
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
# message_number_graph_day_list = network.message_number_graph(log_data, nicks, nick_same_list, True)

degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)
# message_time_graph_list = network.message_time_graph(log_data, nicks, nick_same_list, True)
# message_time_graph = network.message_time_graph(log_data, nicks, nick_same_list, False)
#out_degree_node_number, in_degree_node_number, total_degree_node_number = network.degree_node_number_csv(log_data, nicks, nick_same_list)
# nick_change_graph_list = user.nick_change_graph(log_data, True)

bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
data = [[i for i in range(len(bin_matrix[0]))]]
data.append([sum(i) for i in zip(*bin_matrix)])
# conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)
# resp_time = channel.response_time(log_data, nicks, nick_same_list)

# user.keywords_clusters(log_data, nicks, nick_same_list)
# network.degree_analysis_on_graph(message_number_graph)
# hits = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)


# ============== OUTPUT ================
#saver.save_net_nx_graph (message_time_graph, output_directory, "message_time_graph")
saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph")
#saver.draw_nx_graph (hits, output_directory, "hits")
# saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph")

saver.save_csv([["month", "users", "directed_messages"], ["Jan-2013", int(message_number_graph.size('weight')), util.count_number_of_users_on_channel(nick_same_list)]], output_directory, "users_messages")

saver.save_csv(degree_anal_message_number["out_degree"]["formatted_for_csv"], output_directory, "out_degree")
saver.save_csv(degree_anal_message_number["in_degree"]["formatted_for_csv"], output_directory, "in_degree")
saver.save_csv(degree_anal_message_number["total_degree"]["formatted_for_csv"], output_directory, "total_degree")
# saver.save_csv(out_degree_node_number, output_directory, "node_out_degree" + starting_date +'-'+ending_date)
# saver.save_csv(in_degree_node_number, output_directory, "node_in_degree"+ starting_date +'-'+ending_date)
# saver.save_csv(total_degree_node_number, output_directory, "node_total_degree"+ starting_date +'-'+ending_date)

saver.save_csv(bin_matrix, output_directory, "MessageNumber_binsize_"+str(config.BIN_LENGTH_MINS))

# for i in range(len(nick_change_graph_list)):
    # saver.draw_nx_graph(nick_change_graph_list[i], output_directory, "ncg" + str(i+1))

saver.draw_nx_graph(message_number_graph, output_directory, "mnagg")    
# saver.draw_nx_graph(message_time_graph, output_directory, "mtgagg")

	# saver.save_csv(conv_len, output_directory, "conv_len")
	# saver.save_csv(resp_time, output_directory, "resp_time")
	# saver.save_csv(conv_ref_time, output_directory, "conv_ref_time")

# =============== VIZ ===================
message_graph, message_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + '/message_number_graph.net')
vis.plot_infomap_igraph(message_graph, message_membership, output_directory, "message")
vis.plot_data (data, output_directory, "bins")

#hits_graph, hits_membership = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'hits.net')
#vis.plot_infomap_igraph(hits_graph, hits_membership, output_directory, "hits")

# conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, 20, output_directory, "conv_len")
# resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(resp_time, 20, output_directory, "resp_time")
# conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, 30, output_directory, "conv_ref_time")
# saver.save_csv( [["a","b","c", "MSE"], [conv_len_curve_fit_parameters]], output_directory,"conv_len_curve_fit_parameters")
# saver.save_csv( [["a","b","c", "MSE"], [resp_time_curve_fit_parameters]], output_directory,"resp_time_curve_fit_parameters")
# saver.save_csv( [["a","b","c", "MSE"], [conv_ref_time_curve_fit_parameters]], output_directory,"conv_ref_time_curve_fit_parameters")

#### problem with this code #####
# slope,intercept,r_square,mse = vis.generate_log_plots(9, degree_anal_message_number["out_degree"]["raw_for_vis"], output_directory, "OUT")
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"out-degree-curve-fit")

# slope,intercept,r_square,mse = vis.generate_log_plots(9, degree_anal_message_number["in_degree"]["raw_for_vis"], output_directory, "IN")
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"in-degree-curve-fit")

# slope,intercept,r_square,mse = vis.generate_log_plots(9, degree_anal_message_number["total_degree"]["raw_for_vis"], output_directory, "TOTAL")
# saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory,"total-degree-curve-fit")
