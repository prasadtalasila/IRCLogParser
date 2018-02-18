import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
from datetime import date
import lib.slack.util as util
import csv
import numpy as np
import lib.slack.config as config
from itertools import izip_longest as zip_longest
import lib.analysis.user as user


def message_number_graph(log_dict, nicks, nick_same_list, DAY_BY_DAY_ANALYSIS=False):
    """ 
    Creates a directed graph
    with each node representing an IRC user
    and each directed edge has a weight which 
    mentions the number messages sent and recieved by that user 
    in the selected time frame.
    
    Args:
        log_dict (dict): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}
        nicks(list): list of all the nicks
        nick_same_list(list): list of lists mentioning nicks which belong to same users
    Returns:
       message_number_graph (nx graph object)
    """
    message_number_day_list = []
    conversations=[[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]
    aggregate_message_number_graph = nx.DiGraph()  #graph with multiple directed edges between clients used

    G = util.to_graph(nick_same_list)
    conn_comp_list = list(connected_components(G))

    conn_comp_list = util.create_connected_nick_list(conn_comp_list)

    def msg_no_analysis_helper(rec_list, nick_sender, nick, conn_comp_list,conversations,today_conversation):
        for receiver in rec_list:
            if(receiver == nick):
                if(nick_sender != nick):                                 
                    nick_receiver = ''
                    nick_receiver = util.get_nick_sen_rec(config.MAX_EXPECTED_DIFF_NICKS, nick, conn_comp_list, nick_receiver)    

                    if DAY_BY_DAY_ANALYSIS:
                        today_conversation = util.extend_conversation_list(nick_sender, nick_receiver, today_conversation)
                    else:
                        conversations = util.extend_conversation_list(nick_sender, nick_receiver, conversations)

    def message_no_add_egde(message_graph, conversation):
        for index in xrange(config.MAX_EXPECTED_DIFF_NICKS):
            if(len(conversation[index]) == 3 and conversation[index][0] >= config.THRESHOLD_MESSAGE_NUMBER_GRAPH):
                if len(conversation[index][1]) >= config.MINIMUM_NICK_LENGTH and len(conversation[index][2]) >= config.MINIMUM_NICK_LENGTH:
                    message_graph.add_edge(util.get_nick_representative(nicks, nick_same_list, conversation[index][1]), util.get_nick_representative(nicks, nick_same_list, conversation[index][2]), weight=conversation[index][0])
        return message_graph


    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            today_conversation = [[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]
            for line in day_log:
                flag_comma = 0

                if(util.check_if_msg_line (line)):
                    parsed_nick = re.search(r"\<(.*?)\>", line)
                    nick_sender = util.correctLastCharCR(parsed_nick.group(0)[1:-1])
                    nick_receiver = ""      

                    for nick in nicks:
                        rec_list = [e.strip() for e in line.split(':')]
                        rec_list = util.rec_list_splice(rec_list)
                        if not rec_list[2]:
                            break                        
                        rec_list = util.correct_last_char_list(rec_list)       
                        msg_no_analysis_helper(rec_list, nick_sender, nick, conn_comp_list, conversations,today_conversation)

                        if "," in rec_list[1]:
                            flag_comma = 1
                            rec_list_2=[e.strip() for e in rec_list[1].split(',')]
                            for i in xrange(0,len(rec_list_2)):
                                if(rec_list_2[i]):
                                    rec_list_2[i] = util.correctLastCharCR(rec_list_2[i])                            
                            msg_no_analysis_helper(rec_list_2, nick_sender, nick, conn_comp_list, conversations, today_conversation)                

                        if(flag_comma == 0):
                            rec = line[line.find(">")+1:line.find(", ")]
                            rec = rec[1:]
                            rec = util.correctLastCharCR(rec)
                            if(rec == nick):
                                if(nick_sender != nick):                                   
                                    nick_receiver = nick_receiver_from_conn_comp(nick, conn_comp_list)        

            if DAY_BY_DAY_ANALYSIS:
                today_message_number_graph = nx.DiGraph()
                today_message_number_graph = message_no_add_egde(today_message_number_graph, today_conversation)                
                year, month, day = util.get_year_month_day(day_content)
                message_number_day_list.append([today_message_number_graph, year+'-'+month+'-'+day])

    print "\nBuilding graph object with EDGE WEIGHT THRESHOLD:", config.THRESHOLD_MESSAGE_NUMBER_GRAPH

    if not DAY_BY_DAY_ANALYSIS:
        aggregate_message_number_graph = message_no_add_egde(aggregate_message_number_graph, conversations)
        

    if config.DEBUGGER:
        print "========> 30 on " + str(len(conversations)) + " conversations"
        print conversations[:30]

    if DAY_BY_DAY_ANALYSIS:
        return message_number_day_list
    else:
        return aggregate_message_number_graph


def filter_edge_list(edgelist_file_loc, max_hash, how_many_top):
    """
    reduces the edge list by selecting top nodes through degree analysis
    
    Arguments:
        edgelist_file_loc (str): location of the edgelist file
        max_hash (int): max possinle value of the node_hash in edgelist
        how_many_top (int): how many top nodes to select in the new edgeList
    Returns:
        null
    """
    node_list = []
    degrees = [0] * max_hash

    with open(edgelist_file_loc) as f:
        content = f.readlines()
        for line in content:
            a, b = line.split()
            node_list.append(int(a))
            node_list.append(int(b))
            degrees[int(a)] += 1
            degrees[int(b)] += 1

    print "Done Pre Computation"
    print "Max_hash", max(node_list)

    max_hash = max(node_list)
    degrees = np.array(degrees)

    print "========TOP "+str(how_many_top)+" NODES ON BASIS OF DEGREE ========"

    top_nodes = list(degrees.argsort()[::-1])[:how_many_top]
    # print top_nodes
    print "======= UPDATED ADJACENY LIST ON THE BASIS OF ABOVE NODES ======="

    with open(edgelist_file_loc) as f:
        content = f.readlines()
        for line in content:
            a, b = map(int, line.split())
            if a in top_nodes and b in top_nodes:
                print str(a) + "\t" + str(b)

def degree_analysis_on_graph(nx_graph, date=None, directed = True):
    """
    perform degree analysis of input graph object
    
    Arguments:
        nx_graph (nx_object): object to perform analysis on
    Returns:
        null
    """
    
    def nodes_with_degree_populator(degree_values, label): 
        nodes_with_degree = []
        if len(degree_values):
            nodes_with_degree = [[label + str(i), 0, ''] for i in xrange((max(degree_values)+1))]
        else:
            nodes_with_degree = [["NA", 0, "NA"]]

        for degree in degree_values:
            nodes_with_degree[degree][1] += 1

        return nodes_with_degree

    def give_userlist_where_degree_helper(degree_dict, degree):
        key_list = ""
        for key in degree_dict:
            if degree_dict[key] == degree:
                key_list += (str(key) + ", ")
        return key_list

    degree_map = {} # will map a string(eg "out", "in" , "all") to nx_graph.out_degree() etc
    
    def raw_node_append(nodes, raw, degree_type):        
        """
        Args:
            nodes(List) : nodes_with_OUT/IN/TOTAL degree\
            raw(List) : raw_in/out/total
            degree_type(str) : "in" "out" or "all" , basically keys of degree_map          
        Returns:
            raw(List)
            nodes(List)
        """  
        for i in range(1, len(nodes)):
            raw.append(nodes[i][1]) # raw will store the number of nodes with degree 0 in position 1, # of nodes with degree 1 in position 2 etc
            nodes[i][2] = give_userlist_where_degree_helper(degree_map[degree_type], i - 1)
        return raw, nodes
 
    if directed:
        nodes_with_OUT_degree = nodes_with_degree_populator(nx_graph.out_degree().values(), "nodes_w_out_deg")
   
        nodes_with_IN_degree = nodes_with_degree_populator(nx_graph.in_degree().values(), "nodes_w_in_deg")
        nodes_with_TOTAL_degree = nodes_with_degree_populator(nx_graph.degree().values(), "nodes_w_deg")    

        nodes_with_OUT_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_OUT_degree)]) # sum of (number of nodes with degree 1 +number of nodes with degre 2..)

        nodes_with_IN_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_IN_degree)])

        nodes_with_TOTAL_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_TOTAL_degree)])


        raw_out = [str(date)]
        raw_in = [str(date)]
        raw_total = [str(date)]

        degree_map = {"out":nx_graph.out_degree(),"in":nx_graph.in_degree(),"all":nx_graph.degree()}  

        raw_out, nodes_with_OUT_degree = raw_node_append(nodes_with_OUT_degree, raw_out, "out")
        raw_in, nodes_with_IN_degree = raw_node_append(nodes_with_IN_degree, raw_in, "in")
        raw_total, nodes_with_TOTAL_degree = raw_node_append(nodes_with_TOTAL_degree, raw_total, "all")   

        return {
            "out_degree": {
                "formatted_for_csv": nodes_with_OUT_degree,
                "raw_for_vis": raw_out
                },
            "in_degree": {
                "formatted_for_csv": nodes_with_IN_degree,
                "raw_for_vis": raw_in
                },
            "total_degree": {
                "formatted_for_csv": nodes_with_TOTAL_degree,
                "raw_for_vis": raw_total
                }
            }
    # for undirected        
    else:        
        nodes_with_degree_undirected = nodes_with_degree_populator(nx_graph.degree().values(), "nodes_w_deg")
        nodes_with_degree_undirected.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_degree_undirected)])
        raw_degree = [str(date)]
        degree_map = {"all":nx_graph.degree()}
        raw_degree, nodes_with_degree_undirected = raw_node_append(nodes_with_degree_undirected, raw_degree, "all")

        return  {
            "degree":{
                "formatted_for_csv" : nodes_with_degree_undirected,
                "raw_for_vis" : raw_degree
            }   
         }

def message_time_graph(log_dict, nicks, nick_same_list, DAY_BY_DAY_ANALYSIS=False):
    """ creates a directed graph where each edge denotes a message sent from a user to another user
    with the stamp denoting the time at which the message was sent

    Args:
        log_dict (dictionary): Dictionary of logs data created using reader.py
        nicks(List) : List of nickname created using nickTracker.py
        nick_same_list(List) :List of same_nick names created using nickTracker.py

    Returns:
       msg_time_graph_list(List): List of message time graphs for different days
       msg_time_aggr_graph: aggregate message time graph where edges are date + time when sender sends a message to receiver
    """  
    msg_time_graph_list = []
    msg_time_aggr_graph = nx.MultiDiGraph()
    G = util.to_graph(nick_same_list)
    conn_comp_list = list(connected_components(G))

    def compare_spliced_nick(nick_to_compare, spliced_nick, nick_name, line):
        if(nick_to_compare == nick_name):
            if(spliced_nick != nick_name):
                nick_receiver = nick_receiver_from_conn_comp(nick_name, conn_comp_list)        
                util.build_graphs(nick_sender, nick_receiver, line[1:6], year, month, day, graph_conversation, msg_time_aggr_graph)             
     
    conn_comp_list = util.create_connected_nick_list(conn_comp_list)

    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            year, month, day = util.get_year_month_day(day_content)
            graph_conversation = nx.MultiDiGraph()  #graph with multiple directed edges between clients used
            for line in day_log:
                flag_comma = 0
                if(util.check_if_msg_line (line)):
                    m = re.search(r"\<(.*?)\>", line)         
                    spliced_nick = util.correctLastCharCR(m.group(0)[1:-1])
                    nick_sender = ""                          
                    nick_sender = util.get_nick_sen_rec(config.MAX_EXPECTED_DIFF_NICKS, spliced_nick, conn_comp_list, nick_sender)

                    for nick_name in nicks:
                        rec_list = [e.strip() for e in line.split(':')]  #receiver list splited about :
                        rec_list = util.rec_list_splice(rec_list)
                        if not rec_list[2]:  #index 0 will contain time 14:02
                            break                        
                        rec_list = util.correct_last_char_list(rec_list)        
                        for nick_to_search in rec_list:
                            if(nick_to_search == nick_name):
                                if(spliced_nick != nick_name):                                    
                                    nick_receiver = ""                                         
                                    nick_receiver = util.get_nick_sen_rec(config.MAX_EXPECTED_DIFF_NICKS, nick_name, conn_comp_list, nick_receiver)                                            
                                    util.build_graphs(nick_sender, nick_receiver, line[1:6], year, month, day, graph_conversation, msg_time_aggr_graph)

                        if "," in rec_list[2]:  #receiver list may of the form <Dhruv> Rohan, Ram :
                            flag_comma = 1
                            rec_list_2 = [e.strip() for e in rec_list[2].split(',')]
                            rec_list_2 = util.correct_last_char_list(rec_list_2)        
                            for nick_to_search in rec_list_2:                              
                                compare_spliced_nick(nick_to_search, spliced_nick, nick_name, line)   

                        if(flag_comma == 0):  #receiver list can be <Dhruv> Rohan, Hi!
                            rec = line[line.find(">") + 1:line.find(", ")]
                            rec = util.correctLastCharCR(rec[1:])                           
                            compare_spliced_nick(rec, spliced_nick, nick_name, line)    

            msg_time_graph_list.append(graph_conversation)

    if DAY_BY_DAY_ANALYSIS:
        return msg_time_graph_list
    else:
        return msg_time_aggr_graph


def message_number_bins_csv(log_dict, nicks, nick_same_list):
    """ creates a CSV file which tracks the number of message exchanged in a channel 
        for 48 bins of half an hour each distributed all over the day 
        aggragated over the year.

    Args:
        log_dict (dictionary): Dictionary of logs data created using reader.py
        nicks(List) : List of nickname created using nickTracker.py
        nick_same_list(List) :List of same_nick names created using nickTracker.p

    Returns:
       null 
    """   
    
    no_of_bins = (config.HOURS_PER_DAY * config.MINS_PER_HOUR) / config.BIN_LENGTH_MINS
    tot_msgs = [0] * no_of_bins
    bin_matrix = []

    def bin_increment(nick_name, messager, nick_spliced, bins, bin_index):
        if(nick_name == messager):
            if(nick_spliced != messager):  
                bins[bin_index] = bins[bin_index] + 1 
            
    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            bins = [0] * no_of_bins

            for line in day_log:
                if(line[0] != '='): 
                    time_in_min = int(line[1:3]) * 60 + int(line[4:6])

                    bin_index = time_in_min / config.BIN_LENGTH_MINS #gives the index of the bin for eg 01:35 in mins is 95 then 95/30 --> 3 , puts it in bin index 3
                    
                    flag_comma = 0 # sometimes messages are sent to users like [22:55] <Rohan> Krishna, i hope we are on track. and sometimes like [22:56] <Krishna> Rohan: Yes it is.  

                    if(line[0] != '=' and "] <" in line and "> " in line):
                        m = re.search(r"\<(.*?)\>", line)
                        nick_spliced = util.correctLastCharCR(m.group(0)[1:-1])
                        
                        for messager in nicks:
                            rec_list = [e.strip() for e in line.split(':')]
                            rec_list = util.rec_list_splice(rec_list)
                            if not rec_list[2]:
                                break                            
                            rec_list = util.correct_last_char_list(rec_list)
                            for nick_name in rec_list:
                                bin_increment(nick_name, messager, nick_spliced, bins, bin_index)                                                                                               
                                            
                            if "," in rec_list[2]: 
                                flag_comma = 1
                                rec_list = [e.strip() for e in rec_list[2].split(',')]                              
                                rec_list = util.correct_last_char_list(rec_list)
                                for nick_name in rec_list:
                                    bin_increment(nick_name, messager, nick_spliced, bins, bin_index)                                            
                        
                            if(flag_comma == 0):
                                rec = line[line.find(">")+1:line.find(", ")][1:]
                                rec = util.correctLastCharCR(rec)
                                bin_increment(rec, messager, nick_spliced, bins, bin_index)                               
                                       

            bin_matrix.append(bins)      
            tot_msgs = [tot_msgs[i] + bins[i] for i in range(len(bins))]
            
    return bin_matrix, sum(tot_msgs)

def degree_node_number_csv(log_dict, nicks, nick_same_list):
    """ 
    creates two csv files having no. of nodes with a certain in and out-degree
    for number of nodes it interacted with, respectively.
    Also gives graphs for log(degree) vs log(no. of nodes)
    and tries to find it's equation by curve fitting
    
    Args:
        log_dict (dict): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}
        nicks(list): list of all the nicks
        nick_same_list(list): list of lists mentioning nicks which belong to same users
    Returns:
        out_degree (list)
        in_degree (list)
        total_degree (list)
    """

    msg_num_graph_day_list = message_number_graph(log_dict, nicks, nick_same_list, True)
    degree_analysis_day_list = []

    for day_graph_list in msg_num_graph_day_list:
        day_graph = day_graph_list[0]
        degree_analysis_day_list.append(degree_analysis_on_graph(day_graph, day_graph_list[1]))

    out_degree = []
    in_degree = []
    total_degree = []
    max_in_degree = 0
    max_out_degree = 0
    max_total_degree = 0

    for degree_analysis in degree_analysis_day_list:
        out_degree.append(degree_analysis["out_degree"]["raw_for_vis"])
        in_degree.append(degree_analysis["in_degree"]["raw_for_vis"])
        total_degree.append(degree_analysis["total_degree"]["raw_for_vis"])
        max_out_degree = max(max_out_degree, len(degree_analysis["out_degree"]["raw_for_vis"]))
        max_in_degree = max(max_in_degree, len(degree_analysis["in_degree"]["raw_for_vis"]))
        max_total_degree = max(max_total_degree, len(degree_analysis["total_degree"]["raw_for_vis"]))

    def format_degree_list(degree_list, max_range, degree_type):
        degree_head_row = ["deg"+str(i) for i in range(max_range)]
        degree_head_row.insert(0, degree_type)
        degree_list.insert(0, degree_head_row)
        degree_list = list(zip_longest(*degree_list, fillvalue=0))

        return degree_list

    out_degree = format_degree_list(out_degree, max_out_degree, "out_degree")
    in_degree = format_degree_list(in_degree, max_in_degree, "in_degree")
    total_degree = format_degree_list(total_degree, max_total_degree, "total_degree")

    return out_degree, in_degree, total_degree

def nick_receiver_from_conn_comp(nick, conn_comp_list):
    """
        creates nick_receiver from conn_comp_list,
        it is a helper function used in create_message_time_graph and message_number_graph
    """
    nick_receiver = ""
       
    for i in range(config.MAX_EXPECTED_DIFF_NICKS):
        if nick in conn_comp_list[i]:
            nick_receiver = conn_comp_list[i][0]
            break
    return nick_receiver


def identify_hubs_and_experts(log_dict, nicks, nick_same_list):
    """
        uses message_number graph to identify hubs and experts in the network

    Args:
        log_dict (dict): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}
        nicks(list): list of all the nicks
        nick_same_list(list): list of lists mentioning nicks which belong to same users
    """
    message_graph = message_number_graph(log_dict, nicks, nick_same_list)
    hubs, authority_values = nx.hits(message_graph)

    keyword_dict_list, user_keyword_freq_dict, user_words_dict_list, nicks_for_stop_words, keywords_for_channels = user.keywords(log_dict, nicks, nick_same_list)
    if config.DEBUGGER:
        print "========> USERS"
        print user_keyword_freq_dict
        print "========> CHANNELS"
        print keywords_for_channels, len(keywords_for_channels)

    top_keywords_for_channels = []
    for word_tuple in keywords_for_channels[:config.NUMBER_OF_KEYWORDS_CHANNEL_FOR_OVERLAP]:
        top_keywords_for_channels.append(word_tuple[0])

    overlap_word_number = []
    for keyword_tuple in user_keyword_freq_dict:
        keywords_for_user = keyword_tuple['keywords']
        username = keyword_tuple['nick']
        overlapping_keywords = list(set(top_keywords_for_channels).intersection([x[0] for x in keywords_for_user]))
        if len(overlapping_keywords) > 0:
            overlap_word_number.append([username, len(overlapping_keywords)])

    top_hubs_with_score = util.find_top_n_element_after_sorting(hubs.items(), 1, True, config.HOW_MANY_TOP_EXPERTS)
    top_auth_with_score = util.find_top_n_element_after_sorting(authority_values.items(), 1, True, config.HOW_MANY_TOP_EXPERTS)
    top_keyword_overlap_with_score = util.find_top_n_element_after_sorting(overlap_word_number, 1, True, config.HOW_MANY_TOP_EXPERTS)

    print "TOP " + str(config.HOW_MANY_TOP_EXPERTS) + " HUBS\n", top_hubs_with_score
    print "TOP " + str(config.HOW_MANY_TOP_EXPERTS) + " AUTH\n", top_auth_with_score
    print "TOP " + str(config.HOW_MANY_TOP_EXPERTS) + " KEYWORD OVERLAP\n", top_keyword_overlap_with_score

    top_hub = [hub_tuple[0] for hub_tuple in top_hubs_with_score]
    top_auth = [auth_tuple[0] for auth_tuple in top_auth_with_score]
    top_keyword_overlap = [key_overlap_tuple[0] for key_overlap_tuple in top_keyword_overlap_with_score]

    for node_name in message_graph:
        # mark EXPERTS
        message_graph.node[node_name]['style'] = 'filled'
        if node_name in top_auth and node_name in top_keyword_overlap:
            message_graph.node[node_name]['color'] = '#ff000'
        elif node_name in top_auth:
            message_graph.node[node_name]['color'] = '#00ff00'
        elif node_name in top_keyword_overlap:
            message_graph.node[node_name]['color'] = '#0000ff'
        else:
            message_graph.node[node_name]['color'] = '#cccccc'
        # mark HUBS
        if node_name in top_hub:
            message_graph.node[node_name]['shape'] = 'square'

    return message_graph, top_hub, top_keyword_overlap, top_auth
