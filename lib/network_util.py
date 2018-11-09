"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(nx.Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = nx.Graph()

    @property
    def name(self):
        return self.graph.name

    @name.setter
    def name(self, s):
        self.name = s       

    def add_node(self, node_for_adding):
        self.graph.add_node(node_for_adding)

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.graph.add_nodes_from(nodes_for_adding)


    @property
    def nodes(self):
        return self.graph.nodes()

    def number_of_nodes(self):
        return self.graph.number_of_nodes()

    def has_node(self, n):
        return self.graph.has_node(n)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.graph.add_edge(u_of_edge, v_of_edge)

    def add_edges_from(self, ebunch_to_add, **attr):
        self.graph.add_edges_from(ebunch_to_add)

    def is_directed(self):
        return self.graph.is_directed()

    def is_multigraph(self):
        return self.graph.is_multigraph()

    def edges(self):
        return self.graph.edges()

    def has_edge(self, u, v):
        return self.graph.has_edge(u, v)    


class DiGraph(Graph):

    def __init__(self):
        self.graph = nx.DiGraph()


class MultiGraph(Graph):

    def __init__(self):
        self.graph = nx.MultiGraph()


class MultiDiGraph(MultiGraph, DiGraph):

    def __init__(self):
        self.graph = nx.MultiDiGraph()



def read_pajek(path, encoding='UTF-8'):

    return nx.readwrite.pajek.read_pajek(path, encoding)


def is_isomorphic(G1, G2, node_match=None, edge_match=None):

    return nx.algorithms.isomorphism.is_isomorphic(G1, G2)


def to_agraph(N):

    return nx.drawing.nx_agraph.to_agraph(N)


def connected_components(G):

    return nx.algorithms.components.connected.connected_components(G)


def relabel_nodes(G, mapping, copy=True):

    return nx.relabel.relabel_nodes(G, mapping)


def write_pajek(G, path, encoding='UTF-8'):

    return nx.readwrite.pajek.write_pajek(G, path)


def hits(G, max_iter=100, tol=1.0e-8, nstart=None, normalized=True):

    return nx.hits(G)


def node_link_data(G, attrs=None):

    return nx.readwrite.json_graph.node_link_data(G)
