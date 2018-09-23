"""
This is a network utility function that also acts as a wrapper class for the modules
used in IRCLogParser from NetworkX and iGraph
"""

import networkx as nx 


class Graph(object):

    node_dict_factory = dict
    adjlist_outer_dict_factory = dict
    adjlist_inner_dict_factory = dict
    edge_attr_dict_factory = dict


    def to_directed_class(self):
        return nx.DiGraph

    def to_undirected_class(self):
        return nx.Graph

    def __init__(self):
        self.graph = nx.Graph()

    @property
    def adj(self):
        return self.graph.adj

    @property
    def name(self):
        return self.graph.name

    @name.setter
    def name(self, s):
        self.name = s       

    def __str__(self):
        return self.name

    def __iter__(self):
        return self.graph.__iter__()

    def __contains__(self, n):
        return self.graph.__contains__(n)

    def __len__(self):
        return self.graph.__len__()

    def __getitem__(self, n):
        self.graph.__getitem__(n)

    def add_node(self, node_for_adding):
        self.graph.add_node(node_for_adding)

    def add_nodes_from(self, nodes_for_adding, **attr):
        self.graph.add_nodes_from(nodes_for_adding)

    def remove_node(self, n):
        self.graph.remove_node(n)

    def remove_nodes_from(self, nodes):
        self.graph.remove_nodes_from(nodes)

    @property
    def nodes(self):
        return self.graph.nodes()

    def number_of_nodes(self):
        return self.graph.number_of_nodes()

    def had_node(self, n):
        return self.graph.has_node(n)

    def add_edge(self, u_of_edge, v_of_edge, **attr):
        self.graph.add_edge(u_of_edge, v_of_edge)

    def add_edges_from(self, ebunch_to_add, **attr):
        self.graph.add_edges_from(ebunch_to_add)

    def is_directed(self):
        return self.graph.is_directed()

    def is_multigraph(self):
        return self.graph.is_multigraph()

    def update(self, edges=None, nodes=None):
        # self.graph.update(edges=edges, nodes=nodes)
        pass

    def edges(self):
        return self.graph.edges()

    def has_edge(self, u, v):
        return self.graph.has_edge(u, v)

    def neighbors(self, n):
        return self.graph.neighbors(n)

    def adjacency(self):
        # return self.graph.adjacency()
        pass

    @property
    def degree(self):
        return self.graph.degree()    


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