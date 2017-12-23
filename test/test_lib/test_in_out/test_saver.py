import unittest
import lib.in_out.saver as saver
import lib.util as util
import lib.config as config
import os
import csv
import json
import networkx as nx

current_directory = os.path.dirname(os.path.realpath(__file__))

class SaverTest(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_check_if_dir_exists(self):
        saver.check_if_dir_exists(current_directory + '/test/')
        assert os.path.exists(os.path.dirname(current_directory + '/test/'))
        os.rmdir(current_directory + '/test/')
        
    def test_draw_nx_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([1,2,3])
        graph.add_edge(1,3)
        
        saver.draw_nx_graph(graph, current_directory, 'nx_graph')
        assert os.path.exists(current_directory + '/nx_graph.svg')
        assert os.path.isfile(current_directory + '/nx_graph.svg')
        
        os.remove(current_directory + '/nx_graph.svg')
    
    def test_save_net_nx_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([1,2,3])
        graph.add_edge(1,3)
        saver.save_net_nx_graph(graph, current_directory, 'test_save_net_nx')
        
        assert os.path.exists(current_directory + '/test_save_net_nx.net')
        assert os.path.isfile(current_directory + '/test_save_net_nx.net')
        
        g = nx.read_pajek(current_directory + '/test_save_net_nx.net')
        assert nx.is_isomorphic(graph, g)
        
        os.remove(current_directory + '/test_save_net_nx.net')
        
    def test_save_csv(self):
        matrix = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        saver.save_csv(matrix, current_directory, 'test_save_csv')
        assert os.path.exists(current_directory + '/test_save_csv.csv')
        assert os.path.isfile(current_directory + '/test_save_csv.csv')
        
        filename = current_directory + '/test_save_csv.csv'
        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            try:
                for row in reader:
                    assert row == [1.0, 2.0, 3.0]
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        
        os.remove(current_directory + '/test_save_csv.csv')
        
    def test_save_js_arc(self):
        with open(current_directory + '/data/save_js') as fh:
            expected_result = fh.readline()
        
        rCC = nx.read_pajek(current_directory + '/data/radjCC.net')
        channels_hash = util.load_from_disk(current_directory + '/data/channels_hash')
        
        saver.save_js_arc(rCC, channels_hash, current_directory, '/save_js')
        
        assert os.path.exists(current_directory + '/save_js')
        assert os.path.isfile(current_directory + '/save_js')
        
        with open(current_directory + '/save_js') as fh:
            dump = fh.readline()
            
        assert expected_result == dump
        
        os.remove(current_directory + '/save_js')
        # remove files copied from lib/protovis
        os.remove(current_directory + '/arc_graph.html')
        os.remove(current_directory + '/ex.css')
        os.remove(current_directory + '/protovis-r3.2.js')
        
if __name__ == '__main__':
    unittest.main()
