"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(object):

    def __init__(self):
        self.graph = nx.Graph()


class DiGraph(Graph):

    def __init__(self):
        self.digraph = nx.DiGraph()


class MultiDiGraph(MultiGraph, DiGraph):

    def __init__(self):
        self.multidigraph = nx.MultiDiGraph()


def read_pajek(path, encoding='UTF-8'):

    return nx.readwrite.pajek.read_pajek(path, encoding)


def is_isomorphic(G1, G2, node_match=None, edge_match=None):

    return nx.algorithms.isomorphism.is_isomorphic(G1, G2, node_match, edge_match)


def to_agraph(N):

    return nx.drawing.nx_agraph.to_agraph(N)


def connected_components(G):

    return nx.algorithms.components.connected.connected_components(G)


def relabel_nodes(G, mapping, copy=True):

    return nx.relabel.relabel_nodes(G, mapping, copy)


def write_pajek(G, path, encoding='UTF-8'):

    return nx.readwrite.pajek.write_pajek(G, path, encoding)


def hits(G, max_iter=100, tol=1.0e-8, nstart=None, normalized=True):

    return nx.hits(G, max_iter, tol, nstart, normalized)


def node_link_data(G, attrs=None):

    return nx.readwrite.json_graph.node_link_data(G, attrs)