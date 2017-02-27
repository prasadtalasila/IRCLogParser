import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
from datetime import date
import util
import csv
import sys
import numpy as np
sys.path.append('../lib')
import config

def message_number_graph(log_dict, nicks, nick_same_list):
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

    conversations=[[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]       
    message_number_graph = nx.DiGraph()  #graph with multiple directed edges between clients used    

    G = util.to_graph(nick_same_list)
    conn_comp_list = list(connected_components(G))

    for i in range(len(conn_comp_list)):
        conn_comp_list[i] = list(conn_comp_list[i])

    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            for line in day_log:
                flag_comma = 0
                if(line[0] != '=' and "] <" in line and "> " in line):
                    m = re.search(r"\<(.*?)\>", line)
                    var = util.correctLastCharCR(m.group(0)[1:-1])
                    nick_sender = ""
                    nick_receiver = ""
                    for d in range(config.MAX_EXPECTED_DIFF_NICKS):
                        if ((d < len(conn_comp_list)) and (var in conn_comp_list[d])):  #change nick_same_list to conn_comp_list because conn_comp_list is the main list of all users and nicks now
                            nick_sender = conn_comp_list[d][0]
                            break
                        
                    for i in nicks:
                        rec_list = [e.strip() for e in line.split(':')]
                        rec_list[1] = rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
                        rec_list[1] = rec_list[1][1:]
                        if not rec_list[1]:
                            break
                        for k in xrange(len(rec_list)):
                            if(rec_list[k]):
                                rec_list[k] = util.correctLastCharCR(rec_list[k])
                        for z in rec_list:
                            if(z == i):
                                if(var != i):  
                                    for d in range(config.MAX_EXPECTED_DIFF_NICKS):
                                        if ((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
                                            nick_receiver=conn_comp_list[d][0]
                                            break
                                
                                    for r in xrange(0,config.MAX_EXPECTED_DIFF_NICKS):
                                        if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
                                            if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
                                                conversations[r][0]=conversations[r][0]+1
                                                break
                                        if(len(conversations[r])==1):
                                            conversations[r].append(nick_sender)
                                            conversations[r].append(nick_receiver)
                                            conversations[r][0]=conversations[r][0]+1
                                            break
                                
                        if "," in rec_list[1]: 
                            flag_comma = 1
                            rec_list_2=[e.strip() for e in rec_list[1].split(',')]
                            for ij in xrange(0,len(rec_list_2)):                       #changed variable from i to ij as i has been used above. We are in nested for loop. Same variables name will overlap.
                                if(rec_list_2[ij]):
                                    rec_list_2[ij] = util.correctLastCharCR(rec_list_2[ij])
                            for j in rec_list_2:
                                if(j==i):
                                    if(var != i):  
                                        for d in range(config.MAX_EXPECTED_DIFF_NICKS):
                                            if i in conn_comp_list[d]:
                                                nick_receiver=conn_comp_list[d][0]
                                                break
                                                
                                        for r in xrange(0,config.MAX_EXPECTED_DIFF_NICKS):
                                            if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
                                                if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
                                                    conversations[r][0]=conversations[r][0]+1
                                                    break
                                            if(len(conversations[r])==1):
                                                conversations[r].append(nick_sender)
                                                conversations[r].append(nick_receiver)
                                                conversations[r][0]=conversations[r][0]+1
                                                break

                        if(flag_comma == 0):
                            rec=line[line.find(">")+1:line.find(", ")]
                            rec=rec[1:]
                            rec = util.correctLastCharCR(rec) 
                            if(rec==i):
                                if(var != i):
                                    for d in range(config.MAX_EXPECTED_DIFF_NICKS):
                                        if i in conn_comp_list[d]:
                                            nick_receiver=conn_comp_list[d][0]
                                            break
                                            
                                    for r in xrange(0,config.MAX_EXPECTED_DIFF_NICKS):
                                        if (nick_sender in conversations[r] and nick_receiver in conversations[r]): 
                                            if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
                                                conversations[r][0]=conversations[r][0] + 1
                                                break
                                        if(len(conversations[r])==1):
                                            conversations[r].append(nick_sender)
                                            conversations[r].append(nick_receiver)
                                            conversations[r][0]=conversations[r][0]+ 1
                                            break

    
    print "\nBuilding graph object with EDGE WEIGHT THRESHOLD:", config.THRESHOLD_MESSAGE_NUMBER_GRAPH                                        

    for index in xrange(config.MAX_EXPECTED_DIFF_NICKS):
        if(len(conversations[index]) == 3 and conversations[index][0] >= config.THRESHOLD_MESSAGE_NUMBER_GRAPH):
            if len(conversations[index][1]) >= config.MINIMUM_NICK_LENGTH and len(conversations[index][2]) >= config.MINIMUM_NICK_LENGTH:
                message_number_graph.add_edge(conversations[index][1], conversations[index][2], weight = conversations[index][0]) 

    if config.DEBUGGER:
        print "========> 30 on " + str(len(conversations)) + " conversations"
        print conversations[:30]
    
    return message_number_graph


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
    
    #====================== CHANNEL_USER ============================
    channel_user_graph = nx.Graph()
    CU_adjacency_matrix = [[0]*len(nicks_hash) for i in xrange(0,  len(channels_hash))]
    
    for adjlist in nick_channel_dict:
        for channel in adjlist['channels']:
            
            if channel[1] > config.FILTER_FOR_CHANNEL_USER_GRAPH:
                # print str(nicks_hash.index(adjlist['nickname']))+"\t"+str(config.STARTING_HASH_CHANNEL +channels_hash.index(channel[0]))
                channel_user_graph.add_edge(nicks_hash.index(adjlist['nickname']),
                    (config.STARTING_HASH_CHANNEL + channels_hash.index(channel[0])),
                    weight=channel[1])
                
                full_presence_graph.add_edge(nicks_hash.index(adjlist['nickname']), 
                    (config.STARTING_HASH_CHANNEL + channels_hash.index(channel[0])),
                    weight=channel[1])

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
    CC_adjacency_matrix = [[0]*len(channels_hash) for i in xrange(0,  len(channels_hash))]

    for i in xrange(0, len(channels_hash)):
        for j in xrange(i+1, len(channels_hash)):
            common_users = list(set(users_on_channel[channels_hash[i]]) & set(users_on_channel[channels_hash[j]]))
            # print users_on_channel.keys()[i], users_on_channel.keys()[j], common_users
            CC_adjacency_matrix[i][j] = len(common_users)
            CC_adjacency_matrix[j][i] = len(common_users)
            if len(common_users) > config.FILTER_FOR_CHANNEL_CHANNEL_GRAPH:
                full_presence_graph.add_edge(str(config.STARTING_HASH_CHANNEL + i) ,str(config.STARTING_HASH_CHANNEL + j), weight=len(common_users))
                full_presence_graph.add_edge(str(config.STARTING_HASH_CHANNEL + j) ,str(config.STARTING_HASH_CHANNEL + i), weight=len(common_users))
                # "Uncomment for directed version"
                # print str(channels_hash.index(users_on_channel.keys()[i]))+"\t"+str(channels_hash.index(users_on_channel.keys()[j]))
                # print str(channels_hash.index(users_on_channel.keys()[j]))+"\t"+str(channels_hash.index(users_on_channel.keys()[i]))
                # print channels_hash[i],channels_hash[j]
                channel_channel_graph.add_edge(str(config.STARTING_HASH_CHANNEL + i) ,str(config.STARTING_HASH_CHANNEL + j), weight=len(common_users))
    
    presence_graph_and_matrix["CC"]["matrix"] = CC_adjacency_matrix
    presence_graph_and_matrix["CC"]["graph"] = channel_channel_graph  
    print "CC Adjacency Matrix Generated"
    
    #====================== USER_USER ============================
    user_user_graph = nx.Graph()
    UU_adjacency_matrix = [[0]*len(nicks_hash) for i in xrange(0,  len(nicks_hash))]

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
                user_user_graph.add_edge(i, j, weight= UU_adjacency_matrix[i][j])
                full_presence_graph.add_edge(i, j, weight= UU_adjacency_matrix[i][j])
                full_presence_graph.add_edge(j, i, weight= UU_adjacency_matrix[i][j])

    presence_graph_and_matrix["CU"]["matrix"] = UU_adjacency_matrix
    presence_graph_and_matrix["CU"]["graph"] = user_user_graph  
    print "UU Adjacency Matrix Generated"

    #=========================================================================
    if config.GENERATE_DEGREE_ANAL:

        max_degree_possible = config.CHANNEL_USER_MAX_DEG

        nodes_with_OUT_degree = [0]*max_degree_possible
        nodes_with_IN_degree = [0]*max_degree_possible
        nodes_with_TOTAL_degree = [0]*max_degree_possible
        
        # print full_presence_graph.out_degree().values()
        for degree in full_presence_graph.out_degree().values():
            if not degree < max_degree_possible:
                print "===error", degree
            nodes_with_OUT_degree[degree] += 1

        for degree in full_presence_graph.in_degree().values():
            if not degree < max_degree_possible:
                print "===error", degree
            nodes_with_IN_degree[degree] += 1

        for degree in full_presence_graph.degree().values():
            if not degree < max_degree_possible:
                print "===error", degree
            nodes_with_TOTAL_degree[degree] += 1

        print "========= OUT DEGREE ======="
        for i in xrange(max_degree_possible):
            print "deg"+str(i)+'\t'+str(nodes_with_OUT_degree[i])

        print "========= IN DEGREE ======="
        for i in xrange(max_degree_possible):
            print "deg"+str(i)+'\t'+str(nodes_with_IN_degree[i])

        print "========= TOTAL DEGREE ======="
        for i in xrange(max_degree_possible):
            print "deg"+str(i)+'\t'+str(nodes_with_TOTAL_degree[i])

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

    #filter out top <how_many_top_channels> indices
    top_indices_channels = sorted(range(len(sum_for_each_channel)), key=lambda i: sum_for_each_channel[i], reverse=True)[:how_many_top_channels]
    indices_to_delete_channels = list(set([i for i in xrange(0, len(channels_hash))]) - set(top_indices_channels))

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
    top_indices_users = sorted(range(len(sum_for_each_user)), key=lambda i: sum_for_each_user[i], reverse=True)[:how_many_top_users]
    indices_to_delete_users = list(set([i for i in xrange(0, len(nicks_hash))]) - set(top_indices_users))

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
            print str(config.STARTING_HASH_CHANNEL +i)+"\t"+reduced_channel_hash[i]

    return presence_graph_and_matrix, full_presence_graph


def degree_analysis_on_graph(nx_graph):
    """
        perform degree analysis of input graph object

    Arguments:
        nx_graph (nx_object): object to perform analysis on

    Returns:
        null
    """

    nodes_with_OUT_degree = [["nodes_w_out_deg" + str(i), 0, ''] for i in xrange((max(nx_graph.out_degree().values())+1))]
    nodes_with_IN_degree = [["nodes_w_in_deg" + str(i), 0, ''] for i in xrange((max(nx_graph.in_degree().values())+1))]
    nodes_with_TOTAL_degree = [["nodes_w_deg" + str(i), 0, ''] for i in xrange((max(nx_graph.degree().values())+1))]

    if config.DEBUGGER:
        print nx_graph.out_degree()
        print nx_graph.in_degree()
        print nx_graph.degree()

        print nx_graph.out_degree().values()
        print nx_graph.in_degree().values()
        print nx_graph.degree().values()

    for degree in nx_graph.out_degree().values():
        nodes_with_OUT_degree[degree][1] += 1

    for degree in nx_graph.in_degree().values():
        nodes_with_IN_degree[degree][1] += 1

    for degree in nx_graph.degree().values():
        nodes_with_TOTAL_degree[degree][1] += 1

    def give_userlist_where_degree(degree_dict, degree):
        key_list = ""
        for key in degree_dict:
            if degree_dict[key] == degree:
                key_list+= (key + ", ")
        return key_list

    nodes_with_OUT_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_OUT_degree)])
    nodes_with_IN_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_IN_degree)])
    nodes_with_TOTAL_degree.insert(0, ["total_nodes", sum(data[1] for data in nodes_with_TOTAL_degree)])

    raw_out = []
    raw_in = []
    raw_total = []

    for i in range(1, len(nodes_with_OUT_degree)):
        raw_out.append(nodes_with_OUT_degree[i][1])
        nodes_with_OUT_degree[i][2] = give_userlist_where_degree(nx_graph.out_degree(), i - 1)

    for i in range(1, len(nodes_with_IN_degree)):
        raw_in.append(nodes_with_IN_degree[i][1])
        nodes_with_IN_degree[i][2] = give_userlist_where_degree(nx_graph.in_degree(), i - 1)

    for i in range(1, len(nodes_with_TOTAL_degree)):
        raw_total.append(nodes_with_TOTAL_degree[i][1])
        nodes_with_TOTAL_degree[i][2] = give_userlist_where_degree(nx_graph.degree(), i - 1)

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

def create_message_time_graph(log_dict, nicks, nick_same_list):
    """ creates a directed graph where each edge denotes a message sent from a user to another user
    with the stamp denoting the time at which the message was sent

    Args:
        log_dict (dictionary): Dictionary of logs data created using reader.py
        nicks(List) : List of nickname created using nickTracker.py
        nick_same_list(List) :List of same_nick names created using nickTracker.py

    Returns:
       msg_time_list(List): List of message time graphs for different days
       msg_aggr_graph: aggregate message time graph where edges are date + time when sender sends a message to receiver
    """    
    msg_time_list = []
    msg_aggr_graph = nx.MultiDiGraph()
    G = util.to_graph(nick_same_list)
    conn_comp_list = list(connected_components(G))

    for i in range(len(conn_comp_list)):
        conn_comp_list[i] = list(conn_comp_list[i])

    for day_content_all_channels in log_dict.values():
        for day_content in day_content_all_channels:
            day_log = day_content["log_data"]
            year, month, day = str(day_content["auxiliary_data"]["year"]), str(day_content["auxiliary_data"]["month"]), str(day_content["auxiliary_data"]["day"])       
            graph_conversation = nx.MultiDiGraph()  #graph with multiple directed edges between clients used
            for line in day_log:
                flag_comma = 0
                if(line[0] != '=' and "] <" in line and "> " in line):
                    m = re.search(r"\<(.*?)\>", line)         
                    spliced_nick = util.correctLastCharCR(m.group(0)[1:-1])
                    for i in range(config.MAX_EXPECTED_DIFF_NICKS):
                        if ((i < len(conn_comp_list)) and (spliced_nick in conn_comp_list[i])):
                            nick_sender = conn_comp_list[i][0]
                            break

                    for nick_name in nicks:
                        rec_list = [e.strip() for e in line.split(':')]  #receiver list splited about :
                        rec_list[1] = rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])][1:]                    
                        if not rec_list[1]:  #index 0 will contain time 14:02
                            break
                        for i in range(len(rec_list)):
                            if(rec_list[i]):  #checking for \
                                rec_list[i] = util.correctLastCharCR(rec_list[i])
                        for nick_to_search in rec_list:
                            if(nick_to_search == nick_name):
                                if(spliced_nick != nick_name):
                                    for i in range(config.MAX_EXPECTED_DIFF_NICKS):
                                        if ((i < len(conn_comp_list)) and (nick_name in conn_comp_list[i])):
                                            nick_receiver = conn_comp_list[i][0]
                                            break
                                    graph_conversation.add_edge(nick_sender, nick_receiver, weight=line[1:6])
                                    msg_aggr_graph.add_edge(nick_sender, nick_receiver, weight=year+"/" + month + "/" + day + " - " + line[1:6])

                        if "," in rec_list[1]:  #receiver list may of the form <Dhruv> Rohan, Ram :
                            flag_comma = 1
                            rec_list_2 = [e.strip() for e in rec_list[1].split(',')]
                            for i in range(len(rec_list_2)):
                                if(rec_list_2[i]):  #checking for \
                                    rec_list_2[i] = util.correctLastCharCR(rec_list_2[i])
                            for nick_to_search in rec_list_2:
                                if(nick_to_search == nick_name):
                                    if(spliced_nick != nick_name):
                                        for i in range(config.MAX_EXPECTED_DIFF_NICKS):
                                            if nick_name in conn_comp_list[i]:
                                                nick_receiver = conn_comp_list[i][0]
                                                break
                                        graph_conversation.add_edge(nick_sender, nick_receiver, weight=line[1:6])
                                        msg_aggr_graph.add_edge(nick_sender, nick_receiver, weight=year+"/" + month + "/" + day + " - " + line[1:6])

                        if(flag_comma == 0):  #receiver list can be <Dhruv> Rohan, Hi!
                            rec = line[line.find(">") + 1:line.find(", ")]
                            rec = util.correctLastCharCR(rec[1:])
                            if(rec == nick_name):
                                if(spliced_nick != nick_name):
                                    for i in range(config.MAX_EXPECTED_DIFF_NICKS):
                                        if nick_name in conn_comp_list[i]:
                                            nick_receiver = conn_comp_list[i][0]
                                            break
                                    graph_conversation.add_edge(nick_sender, nick_receiver, weight=line[1:6])
                                    msg_aggr_graph.add_edge(nick_sender, nick_receiver, weight=year+"/" + month + "/" + day + " - " + line[1:6])

            msg_time_list.append(graph_conversation)

    if config.DAY_BY_DAY_ANALYSIS:
        return msg_time_list
    else:
        return msg_aggr_graph
