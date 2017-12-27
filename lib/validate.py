from lib.in_out import saver, reader
from lib import vis, nickTracker
from lib.analysis import network
import numpy as np

def validate_RT_RL_CRT(in_data, ranges, fileName):
    """ 
        Validates the values of curve fit parameters

    Args:
        in_data(list): calculated values of curve fit parameters
        ranges(list of list):  expected values of curve fit parameters
        fileName(str): fileName

    Returns:
       null

    """
    for i in xrange(len(in_data)):
        if not ranges[i][0] <= in_data[i] <= ranges[i][1]:
            errorMessage (i, ranges[i], in_data[i], fileName)


def errorMessage(value_number, expected_range, actual_value, fileName):
    """ 
        Prints error messsage if value not as expected

    Args:
        value_number(int): index of the value in in_data which is not as expected
        expected_range(list): expected values of curve fit parameters
        actual_value(int):  calculated value of curve fit parameters
        fileName(str): fileName

    Returns:
       null

    """
    print "[Unexpected Value] of Arg", value_number, " @", fileName, "| EXPECTED_RANGE:", \
        expected_range, "| GOT:", actual_value
        
        
# Correlational : statistical distribution as illustrated by box plot for degree
def box_plot_for_degree(log_directory, output_directory, channel_name):
    cutoff = 0
    for channel_name_iter in channel_name:
        out_degree_fit_parameters = np.zeros((12, 4))
        in_degree_fit_parameters = np.zeros((12, 4))
        total_degree_fit_parameters = np.zeros((12, 4))
        for month in range(1, 13):
            log_data = reader.linux_input(log_directory, channel_name_iter, "2013-"+str(month)+"-1", "2013-"+str(month)+"-31")
            nicks, nick_same_list = nickTracker.nick_tracker(log_data)

            message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
            degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)

            out_degree_fit_parameters[month-1] = vis.generate_log_plots(degree_anal_message_number["out_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])
            in_degree_fit_parameters[month-1] = vis.generate_log_plots(degree_anal_message_number["in_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])
            total_degree_fit_parameters[month-1] = vis.generate_log_plots(degree_anal_message_number["total_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])

        parameters = ['slope', 'intercept', 'r_square']
        for para_ind in range(len(parameters)):
            vis.box_plot(out_degree_fit_parameters[:, para_ind], output_directory, "out_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            vis.box_plot(in_degree_fit_parameters[:, para_ind], output_directory, "in_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            vis.box_plot(total_degree_fit_parameters[:, para_ind], output_directory, "total_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))

            saver.save_csv([out_degree_fit_parameters[:, para_ind].tolist()], output_directory, "out_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            saver.save_csv([in_degree_fit_parameters[:, para_ind].tolist()], output_directory, "in_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            saver.save_csv([total_degree_fit_parameters[:, para_ind].tolist()], output_directory, "total_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))

def keywords_hits_overlap(log_directory, output_directory, channel_name):
    # Correlational: overlap for keyword digest and HITS
    for month in xrange(1, 13):
        log_data_m1 = reader.linux_input(log_directory, channel_name, "2013-"+str(month)+"-1", "2013-"+str(month)+"-31")
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        message_graph_m1, top_hubs_m1, top_keyword_overlap_m1, top_auth_m1 = network.identify_hubs_and_experts(log_data_m1, nicks_m1, nick_same_list_m1)
        saver.draw_nx_graph(message_graph_m1, output_directory, "expert-month-"+str(month))

        log_data_m2 = reader.linux_input(log_directory, channel_name, "2013-"+str(month+1)+"-1", "2013-"+str(month+1)+"-31")
        nicks_m2, nick_same_list_m2 = nickTracker.nick_tracker(log_data_m1)
        message_graph_m2, top_hubs_m2, top_keyword_overlap_with_score_m2, top_auth_m2 = network.identify_hubs_and_experts(log_data_m2, nicks_m2, nick_same_list_m2)

        print "Top 10 HUBS for Month [HITS]", month, ":", top_hubs_m1
        print "Top 10 HUBS for Month [HITS]", month + 1, ":", top_hubs_m2
        print "Number of common HUBS (from 10) between above 2 months:", len(list(set(top_hubs_m1).intersection(top_hubs_m2)))

        print "Top 10 Experts by keywords for Months", month, ":", top_keyword_overlap_m1
        print "Top 10 Experts by keywords for Months", month + 1, ":", top_keyword_overlap_with_score_m2
        print "Number of common Experts by keywords (from 10) between above 2 months:", len(list(set(top_keyword_overlap_m1).intersection(top_keyword_overlap_with_score_m2)))

        print "Top 10 AUTH for Month [HITS]", month, ":", top_auth_m1
        print "Top 10 AUTH for Month [HITS]", month + 1, ":", top_auth_m2
        print "Number of common AUTH (from 10) between above 2 months:", len(list(set(top_auth_m1).intersection(top_auth_m2)))
        
        print "Number of users common btw HUBS from HITS and Experts by Keywords (from 10) for month", month, ":",  len(list(set(top_keyword_overlap_m1).intersection(top_hubs_m1))) 
        print "Number of users common btw AUTH from HITS and Experts by Keywords (from 10) for month", month, ":",  len(list(set(top_keyword_overlap_m1).intersection(top_auth_m1)))
        print "Number of users common btw HUBS from HITS and AUTH from HITS (from 10) for month", month, ":",  len(list(set(top_hubs_m1).intersection(top_auth_m1)))
        print "Number of users common btw HUBS, HITS and KEYWORDS", month, ":", len(set(list(set(top_keyword_overlap_m1).intersection(top_hubs_m1))).intersection(top_auth_m1))

#Correlational Code-Length

def codelengths(log_directory, output_directory, channel_name):
    codelengths = []
    for month in xrange(1, 13):
        log_data_m1 = reader.linux_input(log_directory, channel_name, "2013-"+str(month)+"-1", "2013-"+str(month)+"-31")
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        message_number_graph_m1 = network.message_number_graph(log_data_m1, nicks_m1, nick_same_list_m1, False)
        try:
            #FOS is a reserved word in igraph and if 'fos' is a username in the nx graph, it generates an error
            saver.save_net_nx_graph(message_number_graph_m1, output_directory, "message-exchange-" + str(month))
            msg_igraph, msg_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + str(month) + '.net')
            codelengths.append(msg_community.codelength)
        except:
            node_labels = message_number_graph_m1.nodes()
            labels = {}
            for label in node_labels:
                if label == "fos":
                    labels[label] = "fos_"
                else:
                    labels[label] = label

            message_number_graph_m1 = nx.relabel_nodes(message_number_graph_m1, labels)
            saver.save_net_nx_graph(message_number_graph_m1, output_directory, "message-exchange-" + str(month))
            print "error in", month

        msg_igraph, msg_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + str(month) + '.net')
        codelengths.append(msg_community.codelength)

    vis.box_plot(codelengths, output_directory, "codelengths2013")
    saver.save_csv([codelengths], output_directory, "codelengths2013")      

#Correlational Activity
def correlational_activity(log_directory, output_directory, channel_name):
    pearson = []
    for month in xrange(1, 12):
        log_data_m1 = reader.linux_input(log_directory, channel_name, "2013-"+str(month)+"-1", "2013-"+str(month)+"-31")
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        bin_matrix_m1, total_messages_m1 = network.message_number_bins_csv(log_data_m1, nicks_m1, nick_same_list_m1)
        monthly_sum_bins_m1 = [sum(i) for i in zip(*bin_matrix_m1)]

        log_data_m2 = reader.linux_input(log_directory, channel_name, "2013-"+str(month+1)+"-1", "2013-"+str(month+1)+"-31")
        nicks_m2, nick_same_list_m2 = nickTracker.nick_tracker(log_data_m2)
        bin_matrix_m2, total_messages_m2 = network.message_number_bins_csv(log_data_m2, nicks_m2, nick_same_list_m2)
        monthly_sum_bins_m2 = [sum(i) for i in zip(*bin_matrix_m2)]
        corr = np.corrcoef(monthly_sum_bins_m1, monthly_sum_bins_m2)[0, 1]

        print "\n----------------------------------"
        print "For months", month, "and", month+1
        print "Bins for M1:", monthly_sum_bins_m1
        print "Bins for M2:", monthly_sum_bins_m2
        print "Pearson correlation:", corr
        pearson.append(corr)

    vis.box_plot(pearson, output_directory, "pearson2013")
    saver.save_csv([pearson], output_directory, "pearson2013")   
