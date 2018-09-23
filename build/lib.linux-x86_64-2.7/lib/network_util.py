"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(object):

    def __init__(self):
        self.graph = nx.Graph()

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.graph.add_nodes_from(nodes_for_adding)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.graph.add_edge(u_of_edge, v_of_edge)

    def add_edges_from(self, ebunch_to_add, **attr):
        self.graph.add_edges_from(ebunch_to_add)

    def is_directed(self):
        self.graph.is_directed()

    def is_multigraph(self):
        self.graph.is_multigraph()

    def nodes(self):
        self.graph.nodes()

    def edges(self):
        self.graph.edges()

    @property
    def name(self):
        self.graph.name


class DiGraph(Graph):

    def __init__(self):
        self.digraph = nx.DiGraph()

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.digraph.add_edge(u_of_edge, v_of_edge)

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.digraph.add_nodes_from(nodes_for_adding)

    def is_directed(self):
        self.digraph.is_directed()

    def out_degree(self):
        self.digraph.out_degree()

    @property
    def nodes(self):
        self.digraph.nodes()

    @property
    def edges(self):
        self.digraph.edges()

    @property
    def name(self):
        self.digraph.name


class MultiGraph(Graph):

    def __init__(self):
        self.multigraph = nx.MultiGraph()


class MultiDiGraph(MultiGraph, DiGraph):

    def __init__(self):
        self.multidigraph = nx.MultiDiGraph()

    def add_edge(self, u_for_edge, v_for_edge, key=None, **attr):
        self.multidigraph.add_edge(u_for_edge, v_for_edge)

    def is_directed(self):
        self.multidigraph.is_directed()


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
