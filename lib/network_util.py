"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(nx.Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = nx.Graph(incoming_graph_data=incoming_graph_data, **attr)

    @property
    def name(self):
        return self.graph.name

    @name.setter
    def name(self, s):
        self.graph.name = s

    @property
    def adj(self):
        return self.graph.adj

    @property
    def node(self):
        return self.graph.node      

    def add_node(self, node_for_adding, **attr):
        self.graph.add_node(node_for_adding, **attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.graph.add_nodes_from(nodes_for_adding, **attr)

    def nodes(self):
        return self.graph.nodes()

    def has_node(self, n):
        return self.graph.has_node(n)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.graph.add_edge(u_of_edge, v_of_edge, **attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        self.graph.add_edges_from(ebunch_to_add, **attr)

    def is_directed(self):
        return self.graph.is_directed()

    def is_multigraph(self):
        return self.graph.is_multigraph()

    def edges(self):
        return self.graph.edges()

    def has_edge(self, u, v):
        return self.graph.has_edge(u, v)    


class DiGraph(Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = nx.DiGraph(incoming_graph_data=incoming_graph_data, **attr)

    def out_degree(self):
        return self.graph.out_degree()

    def in_degree(self):
        return self.graph.in_degree()


class MultiGraph(Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = nx.MultiGraph(incoming_graph_data=incoming_graph_data, **attr)


class MultiDiGraph(MultiGraph, DiGraph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.graph = nx.MultiDiGraph(incoming_graph_data=incoming_graph_data, **attr)



def read_pajek(path, encoding='UTF-8'):

    return nx.readwrite.pajek.read_pajek(path, encoding=encoding)


def is_isomorphic(G1, G2, node_match=None, edge_match=None):

    return nx.algorithms.isomorphism.is_isomorphic(G1, G2, node_match=node_match, edge_match=edge_match)


def to_agraph(N):

    return nx.drawing.nx_agraph.to_agraph(N)


def connected_components(G):

    return nx.algorithms.components.connected.connected_components(G)


def relabel_nodes(G, mapping, copy=True):

    return nx.relabel.relabel_nodes(G, mapping, copy=copy)


def write_pajek(G, path, encoding='UTF-8'):

    return nx.readwrite.pajek.write_pajek(G, path, encoding=encoding)


def hits(G, max_iter=100, tol=1.0e-8, nstart=None, normalized=True):

    return nx.hits(G, max_iter=max_iter, tol=tol, nstart=nstart, normalized=normalized)


def node_link_data(G, attrs=None):

    return nx.readwrite.json_graph.node_link_data(G, attrs=attrs)
