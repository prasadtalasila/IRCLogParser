import networkx as nx
import numpy as np
<<<<<<< HEAD
import igraph
=======
import config
>>>>>>> 320ffc0b9c9476488e4f9d44738780d1f6a8b880

def correctLastCharCR(inText):#
    """ if the last letter of the nick is '\\' replace it by 'CR'
        for example rohan\ becomes rohanCR
        to avoid complications in nx because of the special char '\\'

    Args:
        inText (str): input nick, checked for '\\' at last position

    Returns:
        str: updated string with '\\' replaced by CR (if it exists) 

    """
    if(len(inText) > 1 and inText[len(inText)-1]=='\\'):
        inText = inText[:-1]+'CR'
    return inText

def correct_nick_for_(inText):
    """
        last letter of nick maybe _ and this produces error in nickmatching
    Args:
        inText (str): input nick, checked for '_' at last position

    Returns:
        str: updated string with '_'  removed 
    """
    
    if(inText and inText[len(inText)-1] == '_'):
        inText = inText[:-1]
    return inText

def to_graph(l):
    G = nx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G


def to_edges(l):
    """ A generator which
        takes a graph and returns it's edges | for
        example : to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]

        Args:
            l (list): graph object to be converted to edge_list

        Returns:
            str: edge list of the inputted graph object
    """
    it = iter(l)
    last = next(it)
    for current in it:
        yield last, current
        last = current  


def exponential_curve_func(x, a, b, c):
    return a * np.exp(-b * x) + c

def get_year_month_day(day_content):
    """ A generator which
        takes a day_content and gives the associated year, month and date associated with it       

        Args:
        day_content(dictionary)=
                    {
                    "log_data": day_data, 
                    "auxiliary_data": {
                            "channel": channel_name,
                            "year": year_iterator,
                            "month": month_iterator,
                            "day": day_iterator
                            }
                    }

        Returns:
            str:year, str:month, str:day
    """
    year, month, day = str(day_content["auxiliary_data"]["year"]), str(day_content["auxiliary_data"]["month"]), str(day_content["auxiliary_data"]["day"])
    return year, month, day

<<<<<<< HEAD

def rec_list_splice(rec_list):
    rec_list[1] = rec_list[1][rec_list[1].find(">") + 1:len(rec_list[1])][1:]

=======
def check_if_msg_line (line):
    return (line[0] != '=' and "] <" in line and "> " in line)

def rec_list_splice(rec_list):
    rec_list[1] = rec_list[1][rec_list[1].find(">") + 1:len(rec_list[1])][1:]
>>>>>>> 320ffc0b9c9476488e4f9d44738780d1f6a8b880

def build_graphs(nick_sender, nick_receiver, time, year, month, day, day_graph, aggr_graph):
    """    
        Args:
            nick_sender(str): person who has sent the message
            nick_receiver(str): person who receives the message
            time(str): time when message is sent
            year(str): year  when message is sent
            month(str): month  when message is sent
            day(str): day when message is sent
            day_graph(networkx directed graph): a single days graph to which we add edges
            aggr_graph(networkx directed graph): a whole time spans aggregate graph to which we add edges

        Returns:
            None
    """
    day_graph.add_edge(nick_sender, nick_receiver, weight=time)
    aggr_graph.add_edge(nick_sender, nick_receiver, weight=year+"/" + month + "/" + day + " - " + time)
        

def HACK_convert_nx_igraph(nx_graph):
    nx.write_pajek(nx_graph, "/tmp/rohan.net")
    ig_graph = igraph.Graph()
    ig_graph = igraph.read("/tmp/rohan.net", format="pajek")
    return ig_graph


def extend_conversation_list(nick_sender, nick_receiver, conversation):
    """ A functions that takes the nick_sender and nick_reciver and add them
        the conversation list and increase the weight.
        Args:
            nick_sender : nick of user sending a message
            nick_receiver: nick of user to whom message is being send_time
            conversation: list of nick_sender's and nick_reciever along with number of time message shared btw them
        Returns:
            conversation (list): list containg all the nick between whom messages have been shared
    """
    for i in xrange(0,config.MAX_EXPECTED_DIFF_NICKS):
        if (nick_sender in conversation[i] and nick_receiver in conversation[i]):
            if (nick_sender == conversation[i][1] and nick_receiver == conversation[i][2]):
                conversation[i][0] += 1
                break
        if(len(conversation[i])==1):
            conversation[i].append(nick_sender)
            conversation[i].append(nick_receiver)
            conversation[i][0]=conversation[i][0]+ 1
            break
    return conversation
