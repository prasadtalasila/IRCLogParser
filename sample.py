import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker, vis, config, validate
from analysis import network, user, channel, community

log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

# ============== INPUT==================
log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)             
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

# ============== ANALYSIS =============
# message_number_graph_day_list = network.message_number_graph(log_data, nicks, nick_same_list, DAY_BY_DAY_ANALYSIS = True)
#degree_anal_message_numder = network.degree_analysis_on_graph(message_number_graph)
# message_time_graph_list = network.create_message_time_graph(log_data, nicks, nick_same_list)
#out_degree_node_number, in_degree_node_number, total_degree_node_number = network.degreeNodeNumberCSV(log_data, nicks, nick_same_list)
#nick_change_graph_list =  user.nick_change_graph(log_data)
bin_matrix, ans = network.create_message_number_binsCSV(log_data, nicks, nick_same_list)
# conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)
# resp_time = channel.response_time(log_data, nicks, nick_same_list)

# user.keywords_clusters(log_data, nicks, nick_same_list)
# network.degree_analysis_on_message_number(log_data, nicks, nick_same_list)

# adjCC_graph, adjCC_membership = community.infomap_igraph(ig_graph=None, net_file_location="/home/rohan/Desktop/adjCC.net")

# ============== OUTPUT ================
#saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph")
#saver.save_csv(degree_anal_message_numder["out_degree"]["formatted_for_csv"], output_directory, "out_degree")
#saver.save_csv(degree_anal_message_numder["in_degree"]["formatted_for_csv"], output_directory, "in_degree")
#saver.save_csv(degree_anal_message_numder["total_degree"]["formatted_for_csv"], output_directory, "total_degree")
#saver.save_csv(out_degree_node_number, output_directory, "node_out_degree" + starting_date +'-'+ending_date)
#saver.save_csv(in_degree_node_number, output_directory, "node_in_degree"+ starting_date +'-'+ending_date)
#saver.save_csv(total_degree_node_number, output_directory, "node_total_degree"+ starting_date +'-'+ending_date)
saver.save_csv(bin_matrix, output_directory, "Message_number_bins")
# for i in range(len(message_time_graph_list)):
    # saver.draw_nx_graph(message_time_graph_list[i], output_directory, "mtg" + str(i+1))
#saver.draw_nx_graph(message_time_graph, output_directory, "mtgagg")
# saver.save_csv(conv_len, output_directory, "conv_len")
# saver.save_csv(resp_time, output_directory, "resp_time")
# saver.save_csv(conv_ref_time, output_directory, "conv_ref_time")

# =============== VIZ ===================
# conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, 20, output_directory, "conv_len")
# resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(resp_time, 20, output_directory, "resp_time")
# conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, 30, output_directory, "conv_ref_time")
# vis.plot_infomap_igraph(adjCC_graph, adjCC_membership, output_directory, "adjCC_infomaps")
#vis.generate_log_plots(9, out_degree_node_number, channel_name[0] +"OUT"+ starting_date + ending_date, output_directory)

# ============== VALIDATION ==============
# validate.validate_RT_RL_CRT(conv_len_curve_fit_parameters, [[10.5, 10.6], [2.12, 2.32], [0, 0.2], [0, 0.0002]], "conv_len")
# validate.validate_RT_RL_CRT(resp_time_curve_fit_parameters, [[0.3, 10.4], [10.3, 30.4], [-0.002, 0.002], [0, 0.002]], "resp_time")
# validate.validate_RT_RL_CRT(conv_ref_time_curve_fit_parameters, [[10.05, 10.1], [0.1, 0.2], [0.02, 0.04], [0, 0.0002], [9, 11]], "conv_ref_time")


# ============== PRESENCE ACROSS MULTIPLE CHANNELS ==============
# Change analysis to all channels in config
# nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
# dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

# saver.save_csv(dict_out["UU"]["reducedMatrix"],output_directory, "rUU")
# saver.save_csv(dict_out["CC"]["reducedMatrix"],output_directory, "rCC")
# saver.save_csv(dict_out["CU"]["reducedMatrix"],output_directory, "rCU")
