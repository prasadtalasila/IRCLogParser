import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
from datetime import date
import util
import csv
import numpy as np
import config
from itertools import izip_longest as zip_longest
import user


def message_number_graph(log_dict, nicks, nick_same_list, DAY_BY_DAY_ANALYSIS=False):
    """ Creates a directed graph
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

    util.create_connected_nick_list(conn_comp_list)

    def msg_no_analysis_helper(rec_list, corrected_nick, nick, conn_comp_list,conversations,today_conversation):
        for receiver in rec_list:
            if(receiver == nick):
                if(corrected_nick != nick):                                 
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
                    corrected_nick = util.correctLastCharCR(parsed_nick.group(0)[1:-1])
                    nick_sender = ""
                    nick_receiver = ""                    
                    nick_sender = util.get_nick_sen_rec(config.MAX_EXPECTED_DIFF_NICKS, corrected_nick, conn_comp_list, nick_sender)        

                    for nick in nicks:
                        rec_list = [e.strip() for e in line.split(':')]
                        util.rec_list_splice(rec_list)
                        if not rec_list[1]:
                            break                        
                        rec_list = util.correct_last_char_list(rec_list)       
                        msg_no_analysis_helper(rec_list, corrected_nick, nick, conn_comp_list, conversations,today_conversation)

                        if "," in rec_list[1]:
                            flag_comma = 1
                            rec_list_2=[e.strip() for e in rec_list[1].split(',')]
                            for i in xrange(0,len(rec_list_2)):
                                if(rec_list_2[i]):
                                    rec_list_2[i] = util.correctLastCharCR(rec_list_2[i])                            
                            msg_no_analysis_helper(rec_list_2, corrected_nick, nick, conn_comp_list, conversations, today_conversation)                

                        if(flag_comma == 0):
                            rec = line[line.find(">")+1:line.find(", ")]
                            rec = rec[1:]
                            rec = util.correctLastCharCR(rec)
                            if(rec == nick):
                                if(corrected_nick != nick):                                   
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


def channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash):
    """ creates a directed graph for each nick,
    each edge from which points to the IRC Channels that nick has participated in.
    (Nick changes are tracked here and only the initial nick is shown if a user changed his nick)

    Args:
        nicks(list): list of all the nicks
        nick_same_list(list): list of lists mentioning nicks which belong to same users

    Returns:
        presence_graph_and_matrix (dict): contains adjacency matrices and graphs for Acc Auu Acu
        full_presence_graph (nx graph object)
    """

    presence_graph_and_matrix = {
        "CC": {
                "graph": None,
                "matrix": None,
                "reducedMatrix": None
        },
        "CU": {
                "graph": None,
                "matrix": None,
                "reducedMatrix": None
        },
        "UU": {
                "graph": None,
                "matrix": None,
                "reducedMatrix": None
        },
    }

    users_on_channel = {}
    full_presence_graph = nx.DiGraph()  #directed

    def create_adj_matrix(hashed_list1, hashed_list2):
        adj_matrix = [[0] * len(hashed_list1) for i in range(len(hashed_list2))]
        return adj_matrix

    def add_channel_weighted_edge(graph, adjlist, nicks_hash, channels_hash, channel):
        graph.add_edge(nicks_hash.index(adjlist['nickname']), (config.STARTING_HASH_CHANNEL + channels_hash.index(channel[0])), weight=channel[1])
        return graph   
    
    #====================== CHANNEL_USER ============================
    channel_user_graph = nx.Graph()    
    CU_adjacency_matrix = create_adj_matrix(nicks_hash, channels_hash)
    for adjlist in nick_channel_dict:
        for channel in adjlist['channels']:
            
            if channel[1] > config.FILTER_FOR_CHANNEL_USER_GRAPH:
                # print str(nicks_hash.index(adjlist['nickname']))+"\t"+str(config.STARTING_HASH_CHANNEL +channels_hash.index(channel[0]))
                channel_user_graph = add_channel_weighted_edge(channel_user_graph, adjlist, nicks_hash, channels_hash, channel)
                full_presence_graph = add_channel_weighted_edge(full_presence_graph, adjlist, nicks_hash, channels_hash, channel)                

            # print nicks_hash.index(adjlist['nickname']),adjlist['nickname'], channels_hash.index(channel[0]),channel[0], channel[1]
            CU_adjacency_matrix[channels_hash.index(channel[0])][nicks_hash.index(adjlist['nickname'])] = channel[1]
            # print adjlist['nickname'], channel[0]
           
            if users_on_channel.has_key(channel[0]):
                if adjlist['nickname'] not in users_on_channel[channel[0]]:
                    users_on_channel[channel[0]].append(adjlist['nickname'])
            else:
                users_on_channel[channel[0]] = [adjlist['nickname']]
    
    presence_graph_and_matrix["CU"]["matrix"] = CU_adjacency_matrix
    presence_graph_and_matrix["CU"]["graph"] = channel_user_graph  
    print "CU Adjacency Matrix Generated"

    #====================== CHANNEL_CHANNEL ============================
    channel_channel_graph = nx.Graph()    
    CC_adjacency_matrix = create_adj_matrix(channels_hash, channels_hash)

    def add_common_users_weighted_edge(graph, index1, index2, common_users):
        graph.add_edge(str(config.STARTING_HASH_CHANNEL + index1), str(config.STARTING_HASH_CHANNEL + index2), weight=len(common_users))
        return graph

    for i in xrange(0, len(channels_hash)):
        for j in xrange(i+1, len(channels_hash)):
            common_users = list(set(users_on_channel[channels_hash[i]]) & set(users_on_channel[channels_hash[j]]))
            # print users_on_channel.keys()[i], users_on_channel.keys()[j], common_users
            CC_adjacency_matrix[i][j] = len(common_users)
            CC_adjacency_matrix[j][i] = len(common_users)
            if len(common_users) > config.FILTER_FOR_CHANNEL_CHANNEL_GRAPH:
                full_presence_graph = add_common_users_weighted_edge(full_presence_graph, i, j, common_users)
                full_presence_graph = add_common_users_weighted_edge(full_presence_graph, j, i, common_users)
                '''full_presence_graph.add_edge(str(config.STARTING_HASH_CHANNEL + i), str(config.STARTING_HASH_CHANNEL + j), weight=len(common_users))
                full_presence_graph.add_edge(str(config.STARTING_HASH_CHANNEL + j), str(config.STARTING_HASH_CHANNEL + i), weight=len(common_users))'''
                # "Uncomment for directed version"
                # print str(channels_hash.index(users_on_channel.keys()[i]))+"\t"+str(channels_hash.index(users_on_channel.keys()[j]))
                # print str(channels_hash.index(users_on_channel.keys()[j]))+"\t"+str(channels_hash.index(users_on_channel.keys()[i]))
                # print channels_hash[i],channels_hash[j]
                channel_channel_graph = add_common_users_weighted_edge(channel_channel_graph, i , j, common_users)
                '''channel_channel_graph.add_edge(str(config.STARTING_HASH_CHANNEL + i), str(config.STARTING_HASH_CHANNEL + j), weight=len(common_users))'''
    
    presence_graph_and_matrix["CC"]["matrix"] = CC_adjacency_matrix
    presence_graph_and_matrix["CC"]["graph"] = channel_channel_graph
    print "CC Adjacency Matrix Generated"
    
    #====================== USER_USER ============================
    user_user_graph = nx.Graph()   
    UU_adjacency_matrix = create_adj_matrix(nicks_hash, nicks_hash)
    for user_channel_dict in channels_for_user:
        # user_channel_dict format : {nick : [channels on that day], }
        for i in xrange(0, len(user_channel_dict.keys())):
            for j in xrange(i+1, len(user_channel_dict.keys())):
                common_channels_on_that_day = list(set(user_channel_dict[user_channel_dict.keys()[i]]) & set(user_channel_dict[user_channel_dict.keys()[j]]))
                # print user_channel_dict.keys()[i], user_channel_dict.keys()[j], common_channels_on_that_day
                user1 = user_channel_dict.keys()[i]
                user2 = user_channel_dict.keys()[j]
                no_of_common_channels_day = len(common_channels_on_that_day)
                # print str(nicks_hash.index(user1))+"\t"+str(nicks_hash.index(user2))
                # "Uncomment for directed version"
                # print str(nicks_hash.index(user2))+"\t"+str(nicks_hash.index(user1))
                # print user1, user2
                UU_adjacency_matrix[nicks_hash.index(user1)][nicks_hash.index(user2)] += no_of_common_channels_day
                UU_adjacency_matrix[nicks_hash.index(user2)][nicks_hash.index(user1)] += no_of_common_channels_day

    for i in range(len(nicks_hash)):
        for j in range(i):
            if UU_adjacency_matrix[i][j] > config.FILTER_FOR_USER_USER_GRAPH:
                # print str(i)+'\t'+str(j)
                user_user_graph.add_edge(i, j, weight=UU_adjacency_matrix[i][j])
                full_presence_graph.add_edge(i, j, weight=UU_adjacency_matrix[i][j])
                full_presence_graph.add_edge(j, i, weight=UU_adjacency_matrix[i][j])

    presence_graph_and_matrix["UU"]["matrix"] = UU_adjacency_matrix
    presence_graph_and_matrix["UU"]["graph"] = user_user_graph
    print "UU Adjacency Matrix Generated"

    def print_node_degree(nodes, max_degree_possible):
        for i in range(max_degree_possible):
            print "deg"+str(i)+'\t'+str(nodes[i])

    degree_map = {"out": full_presence_graph.out_degree().values(), "in": full_presence_graph.in_degree().values(), "all": full_presence_graph.degree().values()}

    def inc_degree(degree_list, nodes, max_degree_possible):        
        for degree in degree_list:
            if not degree < max_degree_possible:
                print "===error", degree
            nodes[degree] += 1    
        return nodes

    #=========================================================================
    if config.GENERATE_DEGREE_ANAL:

        max_degree_possible = config.CHANNEL_USER_MAX_DEG

        nodes_with_OUT_degree = [0]*max_degree_possible
        nodes_with_IN_degree = [0]*max_degree_possible
        nodes_with_TOTAL_degree = [0]*max_degree_possible
        
        # print full_presence_graph.out_degree().values()

        nodes_with_OUT_degree = inc_degree(degree_map["out"], nodes_with_OUT_degree, max_degree_possible)
        nodes_with_IN_degree = inc_degree(degree_map["in"], nodes_with_IN_degree, max_degree_possible)
        nodes_with_TOTAL_degree = inc_degree(degree_map["all"], nodes_with_TOTAL_degree, max_degree_possible)        

        print "========= OUT DEGREE ======="        
        print_node_degree(nodes_with_OUT_degree, max_degree_possible) 

        print "========= IN DEGREE ======="        
        print_node_degree(nodes_with_IN_degree, max_degree_possible) 

        print "========= TOTAL DEGREE ======="        
        print_node_degree(nodes_with_TOTAL_degree, max_degree_possible) 

    #=========================================================================
    '''
        We have around 20k users and most of them just visit a channel once,
        hence we filter out the top 100 users
        This inturns reduces the CU and UU matrices
    '''

    '''
        calculate top <how_many_top_users> users
        this is achieved by taking top users from CU matrix on the basis of the column sum (total number of days active on a channel)
    # '''
    how_many_top_users = config.FILTER_TOP_USERS

    '''
     we also need to filter the channels and are filtered on the basis of row sum of CC matrix
    '''
    how_many_top_channels = config.FILTER_TOP_CHANNELS

    sum_for_each_channel = []
    for channel_row in CC_adjacency_matrix:
        sum_for_each_channel.append(sum(channel_row))

    def get_top_indices(sum_list, how_many_vals):        
        return sorted(range(len(sum_list)), key=lambda i: sum_list[i], reverse=True)[:how_many_vals]

    def get_indices_to_delete(hash_list, top_indices):
        return list(set([i for i in range(len(hash_list))]) - set(top_indices))

    #filter out top <how_many_top_channels> indices
    top_indices_channels = get_top_indices(sum_for_each_channel, how_many_top_channels)
    indices_to_delete_channels = get_indices_to_delete(channels_hash, top_indices_channels)
   
    temp_channels = np.delete(CC_adjacency_matrix, indices_to_delete_channels, 1) #delete columns
    reduced_CC_adjacency_matrix = np.delete(temp_channels, indices_to_delete_channels, 0) #delete rows
    presence_graph_and_matrix["CC"]["reducedMatrix"] = reduced_CC_adjacency_matrix
    print "Generated Reduced CC Adjacency Matrix"

    #to calculate sum first take the transpose of CU matrix so users in row
    UC_adjacency_matrix = zip(*CU_adjacency_matrix)
    sum_for_each_user = []

    for user_row in UC_adjacency_matrix:
        sum_for_each_user.append(sum(user_row))

    #filter out top <how_many_top_users> indices
    top_indices_users = get_top_indices(sum_for_each_user, how_many_top_users)
    indices_to_delete_users = get_indices_to_delete(nicks_hash, top_indices_users)    

    # print len(top_indices_users), top_indices_users
    # print len(indices_to_delete_users), indices_to_delete_users

    #update the nick_hash, channel_hash
    reduced_nick_hash = np.delete(nicks_hash, indices_to_delete_users)
    reduced_channel_hash = np.delete(channels_hash, indices_to_delete_channels)


    #update the CU matrix by deleting particular columns, and rows which are not in top_indices_users, channels
    temp_user_channel = np.delete(CU_adjacency_matrix, indices_to_delete_users, 1) #delete columns
    reduced_CU_adjacency_matrix = np.delete(temp_user_channel, indices_to_delete_channels, 0) #delete rows

    print "Generated Reduced CU Adjacency Matrix"
    presence_graph_and_matrix["CU"]["reducedMatrix"] = reduced_CU_adjacency_matrix

    #update the UU matrix by deleting both columns and rows
    temp_users = np.delete(UU_adjacency_matrix, indices_to_delete_users, 1) #delete columns
    reduced_UU_adjacency_matrix = np.delete(temp_users, indices_to_delete_users, 0) #delete rows
    print "Generated Reduced UU Adjacency Matrix"
    presence_graph_and_matrix["UU"]["reducedMatrix"] = reduced_UU_adjacency_matrix

    if config.PRINT_CHANNEL_USER_HASH:
        print "=================================================="

        print "========= REDUCED NICK HASH ========="
        for i in range(len(reduced_nick_hash)):
            print str(i)+"\t"+reduced_nick_hash[i]
        
        print "========= REDUCED CHANNEL HASH ========="
        for i in range(len(reduced_channel_hash)):
            print str(config.STARTING_HASH_CHANNEL + i)+"\t"+reduced_channel_hash[i]

    return presence_graph_and_matrix, full_presence_graph


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

def degree_analysis_on_graph(nx_graph, date=None):
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

    nodes_with_OUT_degree = nodes_with_degree_populator(nx_graph.out_degree().values(), "nodes_w_out_deg")
    nodes_with_IN_degree = nodes_with_degree_populator(nx_graph.in_degree().values(), "nodes_w_in_deg")
    nodes_with_TOTAL_degree = nodes_with_degree_populator(nx_graph.degree().values(), "nodes_w_deg")

    def give_userlist_where_degree_helper(degree_dict, degree):
        key_list = ""
        for key in degree_dict:
            if degree_dict[key] == degree:
                key_list += (key + ", ")
        return key_list

    nodes_with_OUT_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_OUT_degree)])
    nodes_with_IN_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_IN_degree)])
    nodes_with_TOTAL_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_TOTAL_degree)])

    raw_out = [str(date)]
    raw_in = [str(date)]
    raw_total = [str(date)]

    degree_map = {"out":nx_graph.out_degree(),"in":nx_graph.in_degree(),"all":nx_graph.degree()}
    
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
            raw.append(nodes[i][1])
            nodes[i][2] = give_userlist_where_degree_helper(degree_map[degree_type], i - 1)
        return raw, nodes

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
     
    util.create_connected_nick_list(conn_comp_list)

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
                        util.rec_list_splice(rec_list)
                        if not rec_list[1]:  #index 0 will contain time 14:02
                            break                        
                        rec_list = util.correct_last_char_list(rec_list)        
                        for nick_to_search in rec_list:
                            if(nick_to_search == nick_name):
                                if(spliced_nick != nick_name):                                    
                                    nick_receiver = ""                                         
                                    nick_receiver = util.get_nick_sen_rec(config.MAX_EXPECTED_DIFF_NICKS, nick_name, conn_comp_list, nick_receiver)                                            
                                    util.build_graphs(nick_sender, nick_receiver, line[1:6], year, month, day, graph_conversation, msg_time_aggr_graph)

                        if "," in rec_list[1]:  #receiver list may of the form <Dhruv> Rohan, Ram :
                            flag_comma = 1
                            rec_list_2 = [e.strip() for e in rec_list[1].split(',')]
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
                            util.rec_list_splice(rec_list)
                            if not rec_list[1]:
                                break                            
                            rec_list = util.correct_last_char_list(rec_list)
                            for nick_name in rec_list:
                                bin_increment(nick_name, messager, nick_spliced, bins, bin_index)                                                                                               
                                            
                            if "," in rec_list[1]: 
                                flag_comma = 1
                                rec_list = [e.strip() for e in rec_list[1].split(',')]                              
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
    """ creates two csv files having no. of nodes with a certain in and out-degree
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

    return message_graph