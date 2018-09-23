import datetime

import lib.network_util as nx
import numpy as np
from dateutil.relativedelta import relativedelta
from dateutil.rrule import rrule, MONTHLY

from lib import vis, nickTracker, config
from lib.analysis import network, channel, community
from lib.in_out import saver, reader


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
        

def box_plot_for_degree(log_directory, output_directory, channel_name, start_date, end_date):
    """
        Correlational : statistical distribution of curve fit parameters generated for degree distribution. The function
        takes the given time duration and selects one month at a time for generation of a degree distribution sample. Each
        degree distribution sample shall have 3 curve fit parameters namely slope, intercept & r_square. The function collects these parameters
        for all the months of the given time duration. The function produces box plot separately for each parameter.

    Args:
        log_directory(str): path to the location of Logs
        output_directory(str):  path to the location where the results are to be stored
        channel_name(list): channels for which the analysis is to be done.
        start_date(datetime): starting date for the logs to be analysed. This has to be the beginning of the month.
        end_date(datetime): ending date for which the logs are to be analysed. This has to be the end of the month.

    Returns:
       null

    """
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    cutoff = 0
    for channel_name_iter in channel_name:
        out_degree_fit_parameters = np.zeros((12, 4))
        in_degree_fit_parameters = np.zeros((12, 4))
        total_degree_fit_parameters = np.zeros((12, 4))
        for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
            last_day_of_the_month = dt + relativedelta(months=1) - datetime.timedelta(days=1)
        # for month in range(1, 13):
            log_data = reader.linux_input(log_directory, [channel_name_iter], dt.strftime("%Y-%m-%d"),last_day_of_the_month.strftime("%Y-%m-%d"))
            nicks, nick_same_list = nickTracker.nick_tracker(log_data)

            message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list, False)
            degree_anal_message_number = network.degree_analysis_on_graph(message_number_graph)

            out_degree_fit_parameters[dt.month-1] = vis.generate_log_plots(degree_anal_message_number["out_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])
            in_degree_fit_parameters[dt.month-1] = vis.generate_log_plots(degree_anal_message_number["in_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])
            total_degree_fit_parameters[dt.month-1] = vis.generate_log_plots(degree_anal_message_number["total_degree"]["raw_for_vis"], output_directory, channel_name_iter[0])

        parameters = ['slope', 'intercept', 'r_square']
        for para_ind in range(len(parameters)):
            vis.box_plot(out_degree_fit_parameters[:, para_ind], output_directory, "out_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            vis.box_plot(in_degree_fit_parameters[:, para_ind], output_directory, "in_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            vis.box_plot(total_degree_fit_parameters[:, para_ind], output_directory, "total_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))

            saver.save_csv([out_degree_fit_parameters[:, para_ind].tolist()], output_directory, "out_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            saver.save_csv([in_degree_fit_parameters[:, para_ind].tolist()], output_directory, "in_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))
            saver.save_csv([total_degree_fit_parameters[:, para_ind].tolist()], output_directory, "total_degree_"+str(parameters[para_ind])+"_2013_"+channel_name_iter[0]+"_cut_"+str(cutoff))

def keywords_hits_overlap(log_directory, output_directory, channel_name, start_date, end_date):
    """
        The function iterates through the months in the given date range and produces the authorities, top keywords and
        top hubs for the current month and the next month. It also produces the overlap of authorities, top keywords and
        top hubs between the current and the next month.

    Args:
        log_directory(str): path to the location of Logs
        output_directory(str):  path to the location where the results are to be stored
        channel_name(list): channels for which the analysis is to be done
        start_date(datetime): starting date for the logs to be analysed. This has to be the beginning of the month.
        end_date(datetime): ending date for which the logs are to be analysed. This has to be the end of the month.

    Returns:
       null

    """
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        last_day_of_the_month1 = dt + relativedelta(months=1) - datetime.timedelta(days=1)
        log_data_m1 = reader.linux_input(log_directory, channel_name, dt.strftime("%Y-%m-%d"),last_day_of_the_month1.strftime("%Y-%m-%d"))
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        message_graph_m1, top_hubs_m1, top_keyword_overlap_m1, top_auth_m1 = network.identify_hubs_and_experts(log_data_m1, nicks_m1, nick_same_list_m1)
        saver.draw_nx_graph(message_graph_m1, output_directory, "expert-month-"+str(dt.month))

        next_month_dt = dt + relativedelta(months=1)
        last_day_of_the_month2 = next_month_dt + relativedelta(months=1) - datetime.timedelta(days=1)
        log_data_m2 = reader.linux_input(log_directory, channel_name, next_month_dt.strftime("%Y-%m-%d"),last_day_of_the_month2.strftime("%Y-%m-%d"))
        nicks_m2, nick_same_list_m2 = nickTracker.nick_tracker(log_data_m2)
        message_graph_m2, top_hubs_m2, top_keyword_overlap_with_score_m2, top_auth_m2 = network.identify_hubs_and_experts(log_data_m2, nicks_m2, nick_same_list_m2)

        print "Top 10 HUBS for Month [HITS]", dt.month, ":", top_hubs_m1
        print "Top 10 HUBS for Month [HITS]", next_month_dt.month, ":", top_hubs_m2
        print "Number of common HUBS (from 10) between above 2 months:", len(list(set(top_hubs_m1).intersection(top_hubs_m2)))

        print "Top 10 Experts by keywords for Months", dt.month, ":", top_keyword_overlap_m1
        print "Top 10 Experts by keywords for Months", next_month_dt.month, ":", top_keyword_overlap_with_score_m2
        print "Number of common Experts by keywords (from 10) between above 2 months:", len(list(set(top_keyword_overlap_m1).intersection(top_keyword_overlap_with_score_m2)))

        print "Top 10 AUTH for Month [HITS]", dt.month, ":", top_auth_m1
        print "Top 10 AUTH for Month [HITS]", next_month_dt.month, ":", top_auth_m2
        print "Number of common AUTH (from 10) between above 2 months:", len(list(set(top_auth_m1).intersection(top_auth_m2)))
        
        print "Number of users common btw HUBS from HITS and Experts by Keywords (from 10) for month", dt.month, ":",  len(list(set(top_keyword_overlap_m1).intersection(top_hubs_m1)))
        print "Number of users common btw AUTH from HITS and Experts by Keywords (from 10) for month", dt.month, ":",  len(list(set(top_keyword_overlap_m1).intersection(top_auth_m1)))
        print "Number of users common btw HUBS from HITS and AUTH from HITS (from 10) for month", dt.month, ":",  len(list(set(top_hubs_m1).intersection(top_auth_m1)))
        print "Number of users common btw HUBS, HITS and KEYWORDS", dt.month, ":", len(set(list(set(top_keyword_overlap_m1).intersection(top_hubs_m1))).intersection(top_auth_m1))


def codelengths(log_directory, output_directory, channel_name, start_date, end_date):
    """
        The function iterate through the months in the given date range and computes the infomap number. It then plots a
        box plot for the infomap numbers of all the whole months in the given time period.

    Args:
        log_directory(str): path to the location of Logs
        output_directory(str):  path to the location where the results are to be stored
        channel_name(list): channels for which the analysis is to be done
        start_date(datetime): starting date for the logs to be analysed. This has to be the beginning of the month.
        end_date(datetime): ending date for which the logs are to be analysed. This has to be the end of the month.

    Returns:
       null

    """
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    codelengths = []
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        last_day_of_the_month1 = dt + relativedelta(months=1) - datetime.timedelta(days=1)
        log_data_m1 = reader.linux_input(log_directory, channel_name, dt.strftime("%Y-%m-%d"),last_day_of_the_month1.strftime("%Y-%m-%d"))
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        message_number_graph_m1 = network.message_number_graph(log_data_m1, nicks_m1, nick_same_list_m1, False)
        try:
            #FOS is a reserved word in igraph and if 'fos' is a username in the nx graph, it generates an error
            saver.save_net_nx_graph(message_number_graph_m1, output_directory, "message-exchange-" + str(dt.month))
            msg_igraph, msg_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + str(dt.month) + '.net')
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
            saver.save_net_nx_graph(message_number_graph_m1, output_directory, "message-exchange-" + str(dt.month))
            print "error in", dt.month

        msg_igraph, msg_community = community.infomap_igraph(ig_graph=None, net_file_location= output_directory + "message-exchange-" + str(dt.month) + '.net')
        codelengths.append(msg_community.codelength)

    vis.box_plot(codelengths, output_directory, "codelengths2013")
    saver.save_csv([codelengths], output_directory, "codelengths2013")      


def correlational_activity(log_directory, output_directory, channel_name, start_date, end_date):
    """
        The function selects a month in the given date range and creates heatmap bins for the current month and the next
        month. It then calculates the correlational calculates the correlational vectors between the two heatmaps and
        then produces a box plot for all the correlational coefficients of the months in the given date range.

    Args:
        log_directory(str): path to the location of Logs
        output_directory(str):  path to the location where the results are to be stored
        channel_name(list): channels for which the analysis is to be done
        start_date(datetime): starting date for the logs to be analysed. This has to be the beginning of the month.
        end_date(datetime): ending date for which the logs are to be analysed. This has to be the end of the month.

    Returns:
       null

    """
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    pearson = []
    for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
        last_day_of_the_month1 = dt + relativedelta(months=1) - datetime.timedelta(days=1)

        log_data_m1 = reader.linux_input(log_directory, channel_name, dt.strftime("%Y-%m-%d"),last_day_of_the_month1.strftime("%Y-%m-%d"))
        nicks_m1, nick_same_list_m1 = nickTracker.nick_tracker(log_data_m1)
        bin_matrix_m1, total_messages_m1 = network.message_number_bins_csv(log_data_m1, nicks_m1, nick_same_list_m1)
        monthly_sum_bins_m1 = [sum(i) for i in zip(*bin_matrix_m1)]

        next_month_dt = dt + relativedelta(months=1)
        last_day_of_the_month2 = next_month_dt + relativedelta(months=1) - datetime.timedelta(days=1)
        log_data_m2 = reader.linux_input(log_directory, channel_name, next_month_dt.strftime("%Y-%m-%d"),last_day_of_the_month2.strftime("%Y-%m-%d"))
        nicks_m2, nick_same_list_m2 = nickTracker.nick_tracker(log_data_m2)
        bin_matrix_m2, total_messages_m2 = network.message_number_bins_csv(log_data_m2, nicks_m2, nick_same_list_m2)
        monthly_sum_bins_m2 = [sum(i) for i in zip(*bin_matrix_m2)]
        corr = np.corrcoef(monthly_sum_bins_m1, monthly_sum_bins_m2)[0, 1]

        print "\n----------------------------------"
        print "For months", dt.month, "and", dt.month+1
        print "Bins for M1:", monthly_sum_bins_m1
        print "Bins for M2:", monthly_sum_bins_m2
        print "Pearson correlation:", corr
        pearson.append(corr)

    vis.box_plot(pearson, output_directory, "pearson2013")
    saver.save_csv([pearson], output_directory, "pearson2013")   


def correlational_CL_RT_CRT(log_directory, output_directory, start_date, end_date):
    """
        Correlational : statistical distribution as illustrated by box plot for RT, CL, CRT parameters. The function
        takes the given time duration and selects one month at a time for generation of a degree distribution sample. Each
        degree distribution sample shall have 3 curve fit parameters namely a,b & c. The function collects these parameters
        for all the months of the given time duration. The function produces box plot separately for each parameter.


    Args:
        log_directory(str): path to the location of Logs
        output_directory(str):  path to the location where the results are to be stored
        channel_name(list): channels for which the analysis is to be done
        start_date(datetime): starting date for the logs to be analysed. This has to be the beginning of the month.
        end_date(datetime): ending date for which the logs are to be analysed. This has to be the end of the month.

    Returns:
       null

    """
    start_date = datetime.datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date,'%Y-%m-%d')
    percentiles = [0, 1, 5, 10, 20]
    for channel_name_iter in [["#kubuntu-devel"], ["#ubuntu-devel"], ["#kubuntu"]]:
        for cutoff in percentiles:
            conv_len_curve_fit_parameters = np.zeros((12, 4))
            resp_time_curve_fit_parameters = np.zeros((12, 4))
            conv_ref_time_curve_fit_parameters = np.zeros((12, 5))
            for dt in rrule(MONTHLY, dtstart=start_date, until=end_date):
                last_day_of_the_month = dt + relativedelta(months=1) - datetime.timedelta(days=1)

                log_data = reader.linux_input(log_directory, channel_name_iter, dt.strftime("%Y-%m-%d"),last_day_of_the_month.strftime("%Y-%m-%d"))
                nicks, nick_same_list = nickTracker.nick_tracker(log_data)
                default_cutoff = config.CUTOFF_PERCENTILE

                config.CUTOFF_PERCENTILE = cutoff
                truncated_rt, rt_cutoff_time = channel.response_time(log_data, nicks, nick_same_list, config.CUTOFF_PERCENTILE)
                conv_len, conv_ref_time = channel.conv_len_conv_refr_time(log_data, nicks, nick_same_list,
                                                                          rt_cutoff_time, config.CUTOFF_PERCENTILE)
                conv_len_curve_fit_parameters[dt.month - 1] = vis.exponential_curve_fit_and_plot(conv_len, output_directory,
                                                                                              "conv_len_cutoff" + str(cutoff))
                resp_time_curve_fit_parameters[dt.month - 1] = vis.exponential_curve_fit_and_plot(truncated_rt, output_directory,
                                                                                               "resp_time_cutoff" + str(cutoff))
                conv_ref_time_curve_fit_parameters[dt.month - 1] = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time,
                                                                                                             output_directory,
                                                                                                             "conv_ref_time_cutoff" + str(cutoff))

            parameters = ['a', 'b', 'c']
            for para_ind in range(len(parameters)):
                vis.box_plot(conv_len_curve_fit_parameters[:, para_ind], output_directory,
                             "conv_len_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0] + "_cut_" + str(cutoff))
                vis.box_plot(resp_time_curve_fit_parameters[:, para_ind], output_directory,
                             "resp_time_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0] + "_cut_" + str(cutoff))
                vis.box_plot(conv_ref_time_curve_fit_parameters[:, para_ind], output_directory,
                             "conv_refr_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0] + "_cut_" + str(cutoff))

                saver.save_csv([conv_len_curve_fit_parameters[:, para_ind].tolist()], output_directory,
                               "conv_len_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0]
                                + "_cut_" + str(cutoff))
                saver.save_csv([resp_time_curve_fit_parameters[:, para_ind].tolist()], output_directory,
                               "resp_time_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0]
                               + "_cut_" + str(cutoff))
                saver.save_csv([conv_ref_time_curve_fit_parameters[:, para_ind].tolist()], output_directory,
                               "conv_refr_" + str(parameters[para_ind]) + "_2013_" + channel_name_iter[0]
                               + "_cut_" + str(cutoff))

    config.CUTOFF_PERCENTILE = default_cutoff