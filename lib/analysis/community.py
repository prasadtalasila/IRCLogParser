import networkx as nx
import numpy as np
import igraph
import sys
import lib.config as config
import lib.vis as vis


def infomap_igraph(ig_graph, net_file_location=None):
    """ 
        Performs igraph-infomap analysis on the nx graph
    
    Args:
        ig_graph(object): igraph graph object
        net_file_location(str): location to load graph from if not mentioned in ig_graph
        reduce_graph(bool): toggle between enable/disable reduction

    Returns:
        ig_graph: igraph object
        community.membership: result of infomap community analyis
    """

    if ig_graph is None:
        # give an option of loading a graph from .net file
        ig_graph = igraph.Graph()
        ig_graph = igraph.read(net_file_location, format="pajek")

    if ig_graph.es:
        community = ig_graph.community_infomap(edge_weights=ig_graph.es["weight"])
        codelength = community.codelength

        print "code-length:", codelength
        print "no. of communities: ", max(community.membership) + 1
        print community

        if config.DEBUGGER:
            for node in ig_graph.vs():
                print str(node.index)+"\t"+str(ig_graph.vs["id"][node.index])
                # print str(node.index)+"\t"+str(id_to_name_map[g.vs["id"][node.index]])

        # http://stackoverflow.com/questions/21976889/plotting-communities-with-python-igraph
        return ig_graph, community

    return ig_graph, None


def convert_id_name_community(max_hash, community_txt_file, hash_file_txt, reduced_hash_txt, reduced_community):
    """ 
    Converts communites from their ID representation to name for easier understanding
    
    Args:
        max_hash(int): max possible hash value
        community_txt_file(str): location fo the file having community analysis
        hash_file_txt(str): location fo the file having the non-reduced nick_hash
        reduced_hash_txt(str): location fo the file having the reduced nick_hash
        reduced_community(bool): switch b/w reduced and non reduced communities
    
    Returns:
        null
    """
    hash_value = [""]*max_hash

    with open(hash_file_txt) as f:
        content = f.readlines()
        for line in content:
            a, b = line.split()
            hash_value[int(a)] = b

    '''CHANGE COMMUNUITES FROM IDS TO NAME'''
    print "{: >20} {: >1}".format("NAME", "CommunityID")
    print "================================="

    if not reduced_community:
        c = 0
        with open(community_txt_file) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                b = int(b)
                if b != c:
                    print "---------------------------"
                    c += 1
                # print  hash_value[a]+"\t"+str(b)
                print "{: >20} {: >1}".format(hash_value[a], b)

    else:
        '''USED FOR REDUCED COMMUNITIES'''
        top_names = []
        with open(reduced_hash_txt) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                top_names.append(b)

        c = 0
        with open(community_txt_file) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                b = int(b)
                if b != c:
                    print "---------------------------"
                    c += 1
                if hash_value[a] in top_names:
                    print "{: >20} {: >1}".format(hash_value[a], b)
