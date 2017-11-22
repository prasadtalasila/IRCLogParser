from __future__ import print_function
from lib.slack.in_out import reader
from lib.in_out import saver
import lib.slack.nickTracker as nickTracker, lib.slack.config as config, lib.vis as vis, lib.validate as validate, lib.slack.util as util
from lib.analysis import user, community
from lib.slack.analysis import network, channel
import numpy as np
import networkx as nx
import gc
import datetime

log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date = config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

exec_times_file = open(output_directory + "execution_times.txt", 'w')

degree_type = ["out_degree", "in_degree", "total_degree"]

print("begin at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# ============== INPUT==================
log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
nicks, nick_same_list = nickTracker.nick_tracker(log_data)
print("reading log files completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# ============== MESSAGE BINS HEATMAP =============
bin_matrix, total_messages = network.message_number_bins_csv(log_data, nicks, nick_same_list)
data = [[i for i in range(len(bin_matrix[0]))]]
data.append([sum(i) for i in zip(*bin_matrix)])
saver.save_csv(bin_matrix, output_directory, "MessageNumber_binsize_"+str(config.BIN_LENGTH_MINS)) 
vis.plot_data (data, output_directory, "bins")

print("msg bins completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()
del bin_matrix, total_messages, data
gc.collect()

print("msg bins gc completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# ============== CONVERSATION CHARACTERISTICS =============
default_cutoff = config.CUTOFF_PERCENTILE
#percentiles = [0, 1, 5, 10, 20]
percentiles = [1]

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
    saver.save_csv([["response_time_cutoff"], [rt_cutoff_time]], output_directory, "rt_cutoff-" + str(cutoff))
    print("work for cutoff = ", cutoff, "completed at: ", datetime.datetime.now(), file=exec_times_file)

config.CUTOFF_PERCENTILE = default_cutoff #revert back to default

del truncated_rt, rt_cutoff_time, conv_len, conv_ref_time
del conv_len_curve_fit_parameters, resp_time_curve_fit_parameters, conv_ref_time_curve_fit_parameters
gc.collect()
print("conversation characteristics gc completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# ============== MESSAGE EXCHANGE GRAPH ANALYSIS =============
threshold = config.THRESHOLD_MESSAGE_NUMBER_GRAPH
config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 0

message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
print("msg exchange graph with cutoff=0 generated at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

saver.save_csv([["month", "users", "directed_messages"], ["Jan-2013", len(message_number_graph), int(message_number_graph.size('weight'))]], output_directory, "users_messages")

degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)
print("msg exchange graph node degree analysis completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

for dtype in degree_type:
    saver.save_csv(degree_anal_message_number[dtype]["formatted_for_csv"], output_directory, dtype)   
    slope,intercept,r_square,mse = vis.generate_log_plots(degree_anal_message_number[dtype]["raw_for_vis"], 
								output_directory, "slackware-" +dtype)
    saver.save_csv( [["Y","K","R^2", "MSE"], [slope,intercept,r_square,mse]], output_directory, dtype+"-curve-fit")

print("msg exchange graph node degree analysis saved at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

del message_number_graph, degree_anal_message_number
del slope,intercept,r_square,mse
gc.collect()
print("msg exchange with cutoff=0 gc completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# create a smaller message exchange graph for visualization
config.THRESHOLD_MESSAGE_NUMBER_GRAPH = 20
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph")
print("msg exchange graph with cutoff=20 generated at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

saver.save_net_nx_graph (message_number_graph, output_directory, "message_number_graph_cutoff_20")
print("msg exchange graph saved at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

saver.draw_nx_graph(message_number_graph, output_directory, "message_number_graph_cutoff_20")
print("msg exchange graph plot completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

config.THRESHOLD_MESSAGE_NUMBER_GRAPH = threshold

del message_number_graph, threshold
gc.collect()
print("msg exchange with cutoff=20 gc completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()


# ============== EXPERT IDENTIFICATION USING HITS AND TF-IDF  =============
user.keywords_clusters(log_data, nicks, nick_same_list, output_directory, "keywords")
print("TF-IDF keyword clusters completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()

threshold = config.THRESHOLD_MESSAGE_NUMBER_GRAPH #store original default config
cutoffs = [10]
#cutoffs = [0, 10, 20]

for cutoff in cutoffs:
    config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff
    msg_graph_experts, top_hub, top_keyword_overlap, top_auth = network.identify_hubs_and_experts(log_data, nicks, nick_same_list)
    print("creation of HITS graph with cutoff =",cutoff, "completed at: ", datetime.datetime.now(), file=exec_times_file)
    exec_times_file.flush()

    if cutoff == 10:
        saver.draw_nx_graph (msg_graph_experts, output_directory, "hits-cutoff-"+str(cutoff))
        print("plot of HITS graph with cutoff =",cutoff, "completed at: ", datetime.datetime.now(), file=exec_times_file)
        exec_times_file.flush()

config.THRESHOLD_MESSAGE_NUMBER_GRAPH = threshold #revert to default config

del msg_graph_experts, cutoff
gc.collect()
print("HITS work completed at: ", datetime.datetime.now(), file=exec_times_file)
exec_times_file.flush()



# ============== INFOMAPS COMMUNITY DETECTION ON MESSAGE EXCHANGE GRAPH  =============
# the net file is for message exchange graph with cutoff= 0
# message_graph, message_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + 'message_number_graph.net')
# print("Infomaps CD on message exchange graph completed at: ", datetime.datetime.now(), file=exec_times_file)
# exec_times_file.flush()

# vis.plot_infomap_igraph(message_graph, message_community.membership, output_directory, "msg_infomap")
# print("plot of clusters given by Infomaps CD completed at: ", datetime.datetime.now(), file=exec_times_file)
# exec_times_file.flush()

# del message_graph, message_community
# gc.collect()
# print("gc for expert section completed at: ", datetime.datetime.now(), file=exec_times_file)
# exec_times_file.flush()



# ============== ANALYSIS OF DYNAMIC COMMUNITIES  =============
dates = [ ['2013-1-1','2013-1-31'],['2013-6-1','2013-6-30'] ]
cut_offs = [ 0, 10, 20]

for date in dates:
    print("dynamic community analysis for", starting_date, "started at: ", datetime.datetime.now(), file=exec_times_file)
    exec_times_file.flush()
    starting_date = date[0]
    ending_date = date[1]
    log_data = reader.linux_input_slack(log_directory, starting_date, ending_date)
    nicks, nick_same_list = nickTracker.nick_tracker(log_data, False)
    for cutoff in cut_offs:
        print("dynamic community analysis for", starting_date, "with cutoff=", cutoff, 
		"started at: ", datetime.datetime.now(), file=exec_times_file)
        exec_times_file.flush()

        config.THRESHOLD_MESSAGE_NUMBER_GRAPH = cutoff

        message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
        saver.save_net_nx_graph(message_number_graph, output_directory, "message-exchange-" + starting_date + "-cutoff-" + str(cutoff))
        saver.save_csv([["month", "users", "directed_messages"], ["Jan-2013", len(message_number_graph),
                        int(message_number_graph.size('weight'))]], output_directory, "users_messages-" + starting_date + "-cutoff_"
                        + str(cutoff))
        del message_number_graph
        gc.collect()

        msg_graph, message_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + starting_date + "-cutoff-" + str(cutoff) + '.net')

        if cutoff != 0:
            # be careful; vis.plot_infomap_igraph() takes a long time to complete on large graphs
            print("vis.plot_infomap_igraph() starts for", starting_date, "with cutoff=", cutoff,
                    "at: ", datetime.datetime.now(), file=exec_times_file)
            exec_times_file.flush()
            vis.plot_infomap_igraph(msg_graph, message_community.membership, output_directory, "message-exchange-" + starting_date + 
					"-cutoff-" +str(cutoff))
            print("vis.plot_infomap_igraph() ends for", starting_date, "with cutoff=", cutoff,
                    "at: ", datetime.datetime.now(), file=exec_times_file)
            exec_times_file.flush()

        del msg_graph, message_community
        gc.collect()
        print("dynamic community analysis for", starting_date, "with cutoff=", cutoff, 
		"completed at: ", datetime.datetime.now(), file=exec_times_file)
        exec_times_file.flush()

    del log_data, nicks, nick_same_list
    gc.collect()
    print("dynamic community analysis for", starting_date, "completed at: ", datetime.datetime.now(), file=exec_times_file)
    exec_times_file.flush()
    


exec_times_file.close()
