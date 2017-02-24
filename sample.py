import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker, vis, config, validate
from analysis import network, user, channel

log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

# ============== INPUT==================
log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)              
nicks, nick_same_list = nickTracker.nick_tracker(log_data)


# ============== ANALYSIS =============
# message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)

# nick_change_graph_list =  user.nick_change_graph(log_data)

# conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list)
# resp_time = channel.response_time(log_data, nicks, nick_same_list)

user.keywords_clusters(log_data, nicks, nick_same_list)

# ============== OUTPUT ================
# saver.draw_nx_graph(message_number_graph, output_directory, "message_time_graph")

# for i in range(len(nick_change_graph_list)):
#   saver.draw_nx_graph(nick_change_graph_list[i], output_directory, "nick_change_graph_" + str(i))

# saver.save_csv(conv_len, output_directory, "conv_len")
# saver.save_csv(resp_time, output_directory, "resp_time")
# saver.save_csv(conv_ref_time, output_directory, "conv_ref_time")


# =============== VIZ ===================
# conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, 20, output_directory, "conv_len")
# resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(resp_time, 20, output_directory, "resp_time")
# conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, 30, output_directory, "conv_ref_time")


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