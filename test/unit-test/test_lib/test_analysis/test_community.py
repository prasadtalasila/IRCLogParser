import unittest
from lib.analysis import community
from igraph import clustering,Graph
import lib.util as util
import os


class CommunityTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data = util.load_from_disk(self.current_directory+ "/data/log_data")
        self.nicks_hash = util.load_from_disk(self.current_directory+ "/data/nicks_hash")
        self.sample_igraph = Graph()
        self.sample_igraph.add_vertices(8)

    def tearDown(self):
        self.current_directory = None
        self.log_data = None
        self.nicks_hash = None
        self.sample_igraph = None

    def test_infomap_igraph(self):
        message_graph, message_comm = community.infomap_igraph(ig_graph=None, net_file_location= self.current_directory + '/data/message_number_graph.net')
        expected_result = util.load_from_disk(self.current_directory + '/data/community')
        
        dis = clustering.compare_communities(message_comm, expected_result) #calculate distance between two communities
        
        assert dis == 0.0

    def test_infomap_igraph_no_community(self):

        message_graph, message_comm  = community.infomap_igraph(self.sample_igraph)
        self.assertEqual((message_graph,message_comm),(self.sample_igraph,None))


if __name__ == '__main__':
    unittest.main()
