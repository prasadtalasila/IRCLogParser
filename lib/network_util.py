"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(nx.Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.g = nx.Graph(incoming_graph_data=incoming_graph_data, **attr)
        self.node_dict_factory = ndf = self.node_dict_factory
        self.adjlist_outer_dict_factory = self.adjlist_outer_dict_factory
        self.adjlist_inner_dict_factory = self.adjlist_inner_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory

        self.graph = {}   # dictionary for graph attributes
        self._node = ndf()  # empty node attribute dict
        self._adj = self.adjlist_outer_dict_factory()

    @property
    def name(self):
        return self.g.name

    @name.setter
    def name(self, s):
        self.g.name = s

    @property
    def adj(self):
        return self.g.adj

    @property
    def node(self):
        return self.g.node      

    def add_node(self, node_for_adding, **attr):
        self.g.add_node(node_for_adding, **attr)

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.g.add_nodes_from(nodes_for_adding, **attr)

    def nodes(self):
        return self.g.nodes()

    def has_node(self, n):
        return self.g.has_node(n)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.g.add_edge(u_of_edge, v_of_edge, **attr)

    def add_edges_from(self, ebunch_to_add, **attr):
        self.g.add_edges_from(ebunch_to_add, **attr)

    def is_directed(self):
        return self.g.is_directed()

    def is_multigraph(self):
        return self.g.is_multigraph()

    def edges(self):
        return self.g.edges()

    def has_edge(self, u, v):
        return self.g.has_edge(u, v)    


class DiGraph(Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.g = nx.DiGraph(incoming_graph_data=incoming_graph_data, **attr)
        self.node_dict_factory = ndf = self.node_dict_factory
        self.adjlist_outer_dict_factory = self.adjlist_outer_dict_factory
        self.adjlist_inner_dict_factory = self.adjlist_inner_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory

        self.graph = {}   # dictionary for graph attributes
        self._node = ndf()  # empty node attribute dict
        self._adj = self.adjlist_outer_dict_factory()

    def out_degree(self):
        return self.g.out_degree()

    def in_degree(self):
        return self.g.in_degree()


class MultiGraph(Graph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.g = nx.MultiGraph(incoming_graph_data=incoming_graph_data, **attr)
        self.node_dict_factory = ndf = self.node_dict_factory
        self.adjlist_outer_dict_factory = self.adjlist_outer_dict_factory
        self.adjlist_inner_dict_factory = self.adjlist_inner_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory

        self.graph = {}   # dictionary for graph attributes
        self._node = ndf()  # empty node attribute dict
        self._adj = self.adjlist_outer_dict_factory()


class MultiDiGraph(MultiGraph, DiGraph):

    def __init__(self, incoming_graph_data=None, **attr):
        self.g = nx.MultiDiGraph(incoming_graph_data=incoming_graph_data, **attr)
        self.node_dict_factory = ndf = self.node_dict_factory
        self.adjlist_outer_dict_factory = self.adjlist_outer_dict_factory
        self.adjlist_inner_dict_factory = self.adjlist_inner_dict_factory
        self.edge_attr_dict_factory = self.edge_attr_dict_factory

        self.graph = {}   # dictionary for graph attributes
        self._node = ndf()  # empty node attribute dict
        self._adj = self.adjlist_outer_dict_factory()



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
