import unittest
import lib.in_out.saver as saver
import lib.util as util
import os
import csv
import lib.network_util as nx
import sys
from mock import patch
from errno import EACCES


class SaverTest(unittest.TestCase):
    
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        self.current_directory = None

    def test_check_if_dir_exists(self):
        saver.check_if_dir_exists(self.current_directory + '/test/')
        self.assertTrue(os.path.exists(os.path.dirname(self.current_directory + '/test/')))
        os.rmdir(self.current_directory + '/test/')

    @patch("os.makedirs", autospec = True)
    @patch("os.path.exists", autospec = True)
    def test_check_if_dir_exists_exception(self, mock_path, mock_makedir):
        mock_path.return_value = False
        mock_makedir.side_effect = OSError(EACCES)
        self.assertRaises(OSError, saver.check_if_dir_exists,'test/')
        
    def test_draw_nx_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([1,2,3])
        graph.add_edge(1,3)
        
        saver.draw_nx_graph(graph, self.current_directory, 'nx_graph')
        self.assertTrue(os.path.exists(self.current_directory + '/nx_graph.svg'))
        self.assertTrue(os.path.isfile(self.current_directory + '/nx_graph.svg'))
        
        os.remove(self.current_directory + '/nx_graph.svg')
    
    def test_save_net_nx_graph(self):
        graph = nx.DiGraph()
        graph.add_nodes_from([1,2,3])
        graph.add_edge(1,3)
        saver.save_net_nx_graph(graph, self.current_directory, 'test_save_net_nx')
        
        self.assertTrue(os.path.exists(self.current_directory + '/test_save_net_nx.net'))
        self.assertTrue(os.path.isfile(self.current_directory + '/test_save_net_nx.net'))
        
        g = nx.read_pajek(self.current_directory + '/test_save_net_nx.net')
        self.assertTrue(nx.is_isomorphic(graph, g))
        
        os.remove(self.current_directory + '/test_save_net_nx.net')
        
    def test_save_csv(self):
        matrix = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        saver.save_csv(matrix, self.current_directory, 'test_save_csv')
        self.assertTrue(os.path.exists(self.current_directory + '/test_save_csv.csv'))
        self.assertTrue(os.path.isfile(self.current_directory + '/test_save_csv.csv'))
        
        filename = self.current_directory + '/test_save_csv.csv'
        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
            try:
                for row in reader:
                    self.assertEqual(row, [1.0, 2.0, 3.0])
            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
        
        os.remove(self.current_directory + '/test_save_csv.csv')
        
    def test_save_js_arc(self):
        with open(self.current_directory + '/data/save_js') as fh:
            expected_result = fh.readline()
        
        rCC = nx.read_pajek(self.current_directory + '/data/radjCC.net')
        channels_hash = util.load_from_disk(self.current_directory + '/data/channels_hash')
        
        saver.save_js_arc(rCC, channels_hash, self.current_directory, '/save_js')
        
        self.assertTrue(os.path.exists(self.current_directory + '/save_js'))
        self.assertTrue(os.path.isfile(self.current_directory + '/save_js'))
        
        with open(self.current_directory + '/save_js') as fh:
            dump = fh.readline()
            
        self.assertEqual(expected_result, dump)
        
        os.remove(self.current_directory + '/save_js')
        # remove files copied from lib/protovis
        os.remove(self.current_directory + '/arc_graph.html')
        os.remove(self.current_directory + '/ex.css')
        os.remove(self.current_directory + '/protovis-r3.2.js')
        
if __name__ == '__main__':
    unittest.main()
