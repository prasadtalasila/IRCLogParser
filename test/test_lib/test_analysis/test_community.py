import unittest
from lib.analysis import community
from igraph import clustering
import lib.util as util
import os

current_directory = os.path.dirname(os.path.realpath(__file__))

class CommunityTest(unittest.TestCase):

    def setUp(self):
        self.log_data = util.load_from_disk(current_directory+ "/data/log_data")
        self.nicks_hash = util.load_from_disk(current_directory+ "/data/nicks_hash")

    def tearDown(self):
        self.log_data = None
        self.nicks_hash = None

    def test_infomap_igraph(self):
        message_graph, message_comm = community.infomap_igraph(ig_graph=None, net_file_location= current_directory + '/data/message_number_graph.net')
        expected_result = util.load_from_disk(current_directory + '/data/community')
        
        dis = clustering.compare_communities(message_comm, expected_result) #calculate distance between two communities
        
        assert dis == 0.0
    
    def test_convert_id_name_community(self):
        pass


if __name__ == '__main__':
    unittest.main()
