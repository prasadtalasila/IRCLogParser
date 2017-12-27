import unittest
import lib.util as util
import lib.config as config
import commands
import subprocess
import os
import networkx as nx
from ddt import ddt, data, unpack

current_directory = os.path.dirname(os.path.realpath(__file__))

# maybe try to refactor compare_graphs and compare_graph_outputs of tests.py
def compare_graphs(graph1, graph2):
    if nx.is_isomorphic(graph1, graph2):       
        return True
    return False

@ddt
class UtilTest(unittest.TestCase):

    def setUp(self):
        self.nicks = ['BluesKaj', 'Peace-', 'LordOfTime', 'TheLordOfTime', 'benonsoftware', 'Benny', 'Guest43293', 'rdieter_work', 'rdieter', 'jjesse-home_', 'jjesse-home', 'rdieter1', 'Mamarok', 'Mamarok_', 'G4MBY', 'PaulW2U', 'jussi', 'shadeslayer', 'Tm_T', 'yofel', 'ScottK', 'Quintasan', 'mikhas', 'ubottu', 'Noskcaj', 'Riddell', 'Tonio_', 'Tonio_aw', 'yofel_', 'Quintasan_']
        self.expected_nicks = self.nicks

    def tearDown(self):
        self.nicks = None
        self.expected_nicks = None

    def test_save_to_disk(self):
        util.save_to_disk(self.nicks, current_directory+ "/data/nicksTest")
        status, output = commands.getstatusoutput('cmp '+ current_directory + '/data/nicks '+ current_directory+ '/data/nicksTest')
        subprocess.Popen(['rm', current_directory+ '/data/nicksTest'])
        assert status == 0, "Failure to load from disk."


    def test_load_from_disk(self):
        nicks = util.load_from_disk(current_directory+ "/data/nicks")
        assert nicks == self.expected_nicks, "Failure to load from disk."
    
    @data(("krishna\\", "krishnaCR"))
    @unpack
    def test_correctLastCharCR(self, input_nick, expected_output_nick):       
        self.assertEqual(util.correctLastCharCR(input_nick), expected_output_nick)
    
    @data(("krishna\\", "krishnaCR"))
    @unpack
    def test_correct_nick_for_(self, input_nick, expected_output_nick):       
        self.assertEqual(util.correct_nick_for_("rohan_"),"rohan")
    
    @data((['a','b','c','d'], [('a','b'), ('b','c'), ('c','d')]))
    @unpack
    def test_to_edges(self, input_vertices, expected_output):        
        self.assertListEqual(list(util.to_edges(input_vertices)), expected_output)

    @data(([["krishna","ka","krish"], ["rohit","rohitu","rohita"]], [("krishna","ka"),("ka","krish"),("rohitu","rohit"),("rohita","rohitu")]))
    @unpack
    def test_to_graph(self, same_nick_list, edge_list):
        expected_graph = nx.Graph()
        expected_graph.add_edges_from(edge_list)
        self.assertTrue(compare_graphs(util.to_graph(same_nick_list),expected_graph)) 
    
    @data((0, 2, 0, 1, 3.0))
    @unpack
    def test_exponential_curve_func(self, x, a, b, c, expected_result):
        self.assertEqual(util.exponential_curve_func(x, a, b, c), expected_result)
    
    @data(({"log_data": None, \
        "auxiliary_data": {"channel": None,"year": 2017,"month": 10,"day": 7}
        }, ('2017','10','7')))
    @unpack
    def test_get_year_month_day(self, auxiliary_day_content, expected_output):      
        self.assertEqual(util.get_year_month_day(auxiliary_day_content), expected_output)
    
    @data(("[13:48] <ScottK> shadeslayer: It wasn't empty when I made it.", ['[13','shadeslayer',"It wasn't empty when I made it."]))
    @unpack
    def test_rec_list_splice(self, line, expected_result):
        rec_list = [e.strip() for e in line.split(':')]
        util.rec_list_splice(rec_list)
        self.assertListEqual(rec_list, expected_result)
    
    @data('[11:10] <canci> hi everyone')
    def test_check_if_msg_line(self, line):
        self.assertTrue(util.check_if_msg_line(line))             

    def test_build_graphs(self):
        day_graph, expected_day_graph, aggr_graph, expected_aggr_graph = nx.DiGraph(), nx.DiGraph(), nx.DiGraph(), nx.DiGraph()        
        expected_day_graph.add_edge("krishna", "rohan", weight="11:00")
        expected_aggr_graph.add_edge("krishna", "rohan", weight="2017"+"/" + "10" + "/" + "7" + " - " + "11:00")
        util.build_graphs("krishna","rohan","11:00","2017","10","7",day_graph,aggr_graph)
        self.assertTrue(compare_graphs(day_graph,expected_day_graph))
        self.assertTrue(compare_graphs(aggr_graph,expected_aggr_graph))

    def test_extend_conversation_list(self):
        conversations = [[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]
        util.extend_conversation_list("krishna","rohan",conversations)
        util.extend_conversation_list("krishna","rohan",conversations)
        util.extend_conversation_list("rohan","rohit",conversations)
        self.assertListEqual(conversations[0:2],[[2,"krishna","rohan"],[1,"rohan","rohit"]])
    
    @data(([set(['a','b','c']),set(['e','f','g'])], [['a','b','c'], ['e','f','g']]))
    @unpack
    def test_create_connected_nick_list(self, conn_comp_list, expected_conn_comp_list):
        util.create_connected_nick_list(conn_comp_list)
        # sorted has to be uses as set to list conversion leads to change in ordering
        self.assertEqual((sorted(conn_comp_list[0]),sorted(conn_comp_list[1])),\
                        (sorted(expected_conn_comp_list[0]),sorted(expected_conn_comp_list[1]))) 
    
    @data((["rohan\\","rohit\\","krishna\\"], ["rohanCR","rohitCR","krishnaCR"]))
    @unpack
    def test_correct_last_char_list(self, nick_list, expected_result):       
        self.assertListEqual(util.correct_last_char_list(nick_list), expected_result)
    
    @data(('=== benonsoftware is now known as Benny\n', "=", " is", 3, 'benonsoftware'), \
          ('=== benonsoftware is now known as Benny\n', "wn as", "\n", 5, 'Benny'), \
          ('[13:56] <Dhruv> Rohan, Hi!', ">", ", ", 1, "Rohan"))
    @unpack
    def test_splice_find(self, line, search_param1, search_param2, splice_index, expected_result):
        self.assertEqual(util.splice_find(line, search_param1, search_param2, splice_index), expected_result)
    
    @data((3, "rohano", [["krishna","krish"],["rohan","rohano"],["rohit","rohit101"]], "", "rohan" ), \
          (3, "krish", [["krishna","krish"],["rohan","rohano"],["rohit","rohit101"]], "", "krishna"))
    @unpack
    def test_get_nick_sen_rec(self, iter_range, nick_to_search, conn_comp_list, nick_sen_rec, expected_result):
        self.assertEqual(util.get_nick_sen_rec(iter_range, nick_to_search, conn_comp_list, nick_sen_rec), expected_result)
        self.assertEqual(util.get_nick_sen_rec(3,"krish",conn_comp_list,""),"krishna")
    
    @data((["krishna","krish","rohan","rohit","rohano"], [["krishna","krish"],["rohan","rohano"],["rohit"],[],[]], "Dhruv", "Dhruv"), \
          (["krishna","krish","rohan","rohit","rohano"], [["krishna","krish"],["rohan","rohano"],["rohit"],[],[]], "krish", "krishna"))
    @unpack
    def test_get_nick_representative(self, nicks, nick_same_list, nick_to_compare, expected_result):
        # look at nickTracker.py in that too nick_same_list has size = maxm expected diff nicks
        self.assertEqual(util.get_nick_representative(nicks, nick_same_list, nick_to_compare), expected_result)

    @data(([[1,2,3],[3,1,2],[2,3,1]], 1, False, 2, [[3,1,2], [1,2,3]]), \
          ([[1,2,3],[3,1,2],[2,3,1]], 1, True, 2, [[2,3,1], [1,2,3]]))
    @unpack
    def test_find_top_n_element_after_sorting(self, in_list, index, reverseBool, n, expected_output):
        self.assertListEqual(util.find_top_n_element_after_sorting(in_list, index, reverseBool,n), expected_output)    


if __name__ == '__main__':
    unittest.main()
