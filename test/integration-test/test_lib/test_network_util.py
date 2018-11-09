import lib.network_util as network_util
import networkx as nx
import unittest
import os
import sys


class NetworkUtilTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        self.current_directory = None

    def test_read_pajek(self):
        expected_graph = nx.read_pajek(self.current_directory + "/data/message_number_graph.net")
        output_graph = network_util.read_pajek(self.current_directory + "/data/message_number_graph.net")

        self.assertTrue(nx.is_isomorphic(expected_graph, output_graph))

    def test_is_isomorphic(self):
        graph = nx.read_pajek(self.current_directory + "/data/message_number_graph.net")

        self.assertTrue(network_util.is_isomorphic(graph, graph))

    def test_to_agraph(self):
        graph = nx.read_pajek(self.current_directory + "/data/message_number_graph.net")

        expected_agraph = nx.nx_agraph.to_agraph(graph)
        output_agraph = network_util.to_agraph(graph)

        self.assertEquals(expected_agraph, output_agraph)

    def test_connected_components(self):
        graph = nx.path_graph(4)
        graph.add_path([10, 11, 12])

        expected_generator = nx.connected_components(graph)
        output_generator = network_util.connected_components(graph)

        self.assertEquals(list(expected_generator), list(output_generator))

    def test_relabel_nodes(self):
        graph = nx.path_graph(3)

        mapping = {0: 'a', 1: 'b', 2: 'c'}

        self.assertEquals(sorted(nx.relabel_nodes(graph, mapping)), sorted(network_util.relabel_nodes(graph, mapping)))

    def test_write_pajek(self):
        graph = nx.path_graph(3)

        path = self.current_directory + "/data/test_write_pajek_output.net"

        network_util.write_pajek(graph, path)

        read_graph = nx.read_pajek(path)

        self.assertTrue(network_util.is_isomorphic(graph, read_graph))

    def test_hits(self):
        graph = nx.path_graph(4)

        expected_tuple1, expected_tuple2 = nx.hits(graph)

        output_tuple1, output_tuple2 = network_util.hits(graph)

        self.assertEquals(expected_tuple1, output_tuple1)
        self.assertEquals(expected_tuple2, output_tuple2)

    def node_link_data(self):
        graph = nx.path_graph(4)

        expected_dict = nx.readwrite.json_graph.node_link_data(graph)
        output_dict = network_util.node_link_data(graph)

        self.assertEquals(expected_dict, output_dict)


    def test_Graph(self):
        graph = network_util.Graph()

        graph.add_node(1)
        graph.add_node(2)
        graph.add_nodes_from([3, 4, 5])
        graph.add_edge(1, 2)
        graph.add_edges_from([(3, 4)])
        graph.name = 'mygraph'
        
        self.assertEqual(graph.name, 'mygraph')
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(4))
        self.assertTrue(graph.has_edge(1, 2))
        self.assertTrue(graph.has_edge(3, 4))
        self.assertFalse(graph.is_directed())
        self.assertFalse(graph.is_multigraph())
        self.assertEqual(list(graph.nodes()), [1, 2, 3, 4, 5])
        self.assertEqual(list(graph.edges()), [(1, 2), (3, 4)])

    
    def test_DiGraph(self):
        graph = network_util.DiGraph()

        graph.add_node(1)
        graph.add_node(2)
        graph.add_nodes_from([3, 4, 5])
        graph.add_edge(1, 2)
        graph.add_edges_from([(3, 4)])
        graph.name = 'mygraph'
        
        self.assertEqual(graph.name, 'mygraph')
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(4))
        self.assertTrue(graph.has_edge(1, 2))
        self.assertTrue(graph.has_edge(3, 4))
        self.assertFalse(graph.is_multigraph())
        self.assertEqual(list(graph.nodes()), [1, 2, 3, 4, 5])
        self.assertEqual(list(graph.edges()), [(1, 2), (3, 4)])
        self.assertNotEqual(graph.is_directed(), False)


    def test_MultiGraph(self):
        graph = network_util.MultiGraph()

        graph.add_node(1)
        graph.add_node(2)
        graph.add_nodes_from([3, 4, 5])
        graph.add_edge(1, 2)
        graph.add_edges_from([(3, 4)])
        graph.name = 'mygraph'
        
        self.assertEqual(graph.name, 'mygraph')
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(4))
        self.assertTrue(graph.has_edge(1, 2))
        self.assertTrue(graph.has_edge(3, 4))
        self.assertTrue(graph.is_multigraph())
        self.assertEqual(list(graph.nodes()), [1, 2, 3, 4, 5])
        self.assertEqual(list(graph.edges()), [(1, 2), (3, 4)])
        self.assertEqual(graph.is_directed(), False)


    def test_MultiDiGraph(self):
        graph = network_util.MultiDiGraph()

        graph.add_node(1)
        graph.add_node(2)
        graph.add_nodes_from([3, 4, 5])
        graph.add_edge(1, 2)
        graph.add_edges_from([(3, 4)])
        graph.name = 'mygraph'
        
        self.assertEqual(graph.name, 'mygraph')
        self.assertTrue(graph.has_node(1))
        self.assertTrue(graph.has_node(4))
        self.assertTrue(graph.has_edge(1, 2))
        self.assertTrue(graph.has_edge(3, 4))
        self.assertTrue(graph.is_multigraph())
        self.assertEqual(list(graph.nodes()), [1, 2, 3, 4, 5])
        self.assertEqual(list(graph.edges()), [(1, 2), (3, 4)])
        self.assertNotEqual(graph.is_directed(), False)
