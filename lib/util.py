import networkx as nx
import numpy as np


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