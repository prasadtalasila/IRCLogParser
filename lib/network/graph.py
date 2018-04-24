import networkx as nx

class BaseGraph():

    def __init__(self):
        # to do here
        pass

    def graph_add_node(self, n, attr_dict=None, **attr):
        self.graph_obj.add_node(n, attr_dict=None, **attr)

    def graph_add_nodes_from(self, nodes, **attr):
        self.graph_obj.add_nodes_from(nodes, **attr)

    def graph_remove_node(self, n):
        self.graph_obj.remove_node(n)

    def graph_add_edge(self,u, v, attr_dict=None, **attr):
        self.graph_obj.add_edge(u, v, attr_dict=None, **attr)

    def graph_add_edges_from(self, ebunch, attr_dict=None, **attr):
        self.graph_obj.add_edges_from(ebunch, attr_dict=None, **attr)

    def graph_remove_edge(self, u, v):
        self.graph_obj.remove_edge(u, v)

    def graph_remove_edges_from(self, ebunch):
        self.graph_obj.remove_edges_from(ebunch)

class Nodes():

    def __init__(self):
        # to do here
        pass

    def graph_relabel_nodes(self,G, mapping, copy=True):
        self.graph_obj.graph_relabel_nodes(G, mapping, copy=True)

class Graph(BaseGraph, Nodes):

    def __init__(self):
        # to do here
        self.graph_obj = nx.Graph

class MultiGraph(BaseGraph, Nodes):

    def __init__(self):
        # to do here
        self.graph_obj = nx.MultiGraph

class MultiDiGraph(BaseGraph, Nodes):

    def __init__(self):
        # to do here
        self.graph_obj = nx.MultiDiGraph