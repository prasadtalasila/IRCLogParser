import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components

import util
import sys
sys.path.append('../lib')
import config



def createAggregateGraph(log_data, nicks, nick_same_list):
    """ Creates a directed graph for a longer time frames 
        with each node representing an IRC user
        and each directed edge has a weight which 
        mentions the number messages sent and recieved by that user 
        in the selected time frame.

    Args:
        log_directory (str): conn_comp_listocation of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        channel_name (str): Channel to be perform analysis on
        output_directory (str): conn_comp_listocation of output directory
        startingDate (int): Date to start the analysis (in conjunction with startingMonth)
        startingMonth (int): Date to start the analysis (in conjunction with startingDate)
        endingDate (int): Date to end the analysis (in conjunction with endingMonth)
        endingMonth (int): Date to end the analysis (in conjunction with endingDate)

    Returns:
       aggregate_graph (nx graph object) 

    """

    conversations=[[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]   
    
    aggregate_graph = nx.DiGraph()  #graph with multiple directed edges between clients used 

    G = util.to_graph(nick_same_list)
    conn_comp_list = list(connected_components(G))

    for i in range(len(conn_comp_list)):
        conn_comp_list[i] = list(conn_comp_list[i])

    for day_content in log_data:
       for line in day_content:
            flag_comma = 0
            if(line[0] != '=' and "] <" in line and "> " in line):
                m = re.search(r"\<(.*?)\>", line)
                var = util.correctLastCharCR(m.group(0)[1:-1])
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

    for index in xrange(config.MAX_EXPECTED_DIFF_NICKS):
        if(len(conversations[index]) == 3):
            aggregate_graph.add_edge(conversations[index][1], conversations[index][2], weight = conversations[index][0]) 

    if config.DEBUGGER:
        print "========> nicks"
        print nicks[:30]
        print "========> nick_same_list"
        print nick_same_list[:30]
        print "========> conversations"
        print conversations[:30]
    
    return aggregate_graph