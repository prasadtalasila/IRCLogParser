import unittest
import sys
from os import path
import networkx as nx
sys.path.insert(0, '../lib')
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib import config, util

# maybe try to refactor compare_graphs and compare_graph_outputs of tests.py
def compare_graphs(graph1, graph2):
    if nx.is_isomorphic(graph1, graph2):       
        return True
    return False

class util_test(unittest.TestCase):
    def test_correctLastCharCR(self):       
        self.assertEqual(util.correctLastCharCR("krishna\\"),"krishnaCR")

    def test_correct_nick_for_(self):       
        self.assertEqual(util.correct_nick_for_("rohan_"),"rohan")

    def test_to_edges(self):        
        self.assertListEqual(list(util.to_edges(['a','b','c','d'])), [('a','b'), ('b','c'), ('c','d')])

    def test_to_graph(self):
        same_nick_list = [["krishna","ka","krish"], ["rohit","rohitu","rohita"]] #each sub list nick is the same person  
        expected_graph = nx.Graph()
        expected_graph.add_edges_from([("krishna","ka"),("ka","krish"),("rohitu","rohit"),("rohita","rohitu")])
        self.assertTrue(compare_graphs(util.to_graph(same_nick_list),expected_graph)) 

    def test_exponential_curve_func(self):
        self.assertEqual(util.exponential_curve_func(0,2,0,1), 3.0)

    def test_get_year_month_day(self):      
        arbitrary_day_content = {"log_data": None, \
        "auxiliary_data": {"channel": None,"year": 2017,"month": 10,"day": 7}
        }
        self.assertEqual(util.get_year_month_day(arbitrary_day_content), ('2017','10','7'))

    def test_rec_list_splice(self):
        line = "[13:48] <ScottK> shadeslayer: It wasn't empty when I made it."
        rec_list = [e.strip() for e in line.split(':')]
        util.rec_list_splice(rec_list)
        self.assertListEqual(rec_list,['[13','shadeslayer',"It wasn't empty when I made it."])

    def test_check_if_msg_line(self):
        self.assertTrue(util.check_if_msg_line('[11:10] <canci> hi everyone'))             

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

    def test_create_connected_nick_list(self):
        expected_conn_comp_list = [['a','b','c'], ['e','f','g']]
        conn_comp_list = [set(['a','b','c']),set(['e','f','g'])]
        util.create_connected_nick_list(conn_comp_list)
        # sorted has to be uses as set to list conversion leads to change in ordering
        self.assertEqual((sorted(conn_comp_list[0]),sorted(conn_comp_list[1])),\
                        (sorted(expected_conn_comp_list[0]),sorted(expected_conn_comp_list[1]))) 

    def test_correct_last_char_list(self):       
        self.assertListEqual(util.correct_last_char_list(["rohan\\","rohit\\","krishna\\"]),["rohanCR","rohitCR","krishnaCR"])

    def test_splice_find(self):
        line1 = '=== benonsoftware is now known as Benny\n'  # this is because on reading using readlines() \n is appended at the end
        self.assertEqual(util.splice_find(line1, "=", " is", 3), 'benonsoftware')
        self.assertEqual(util.splice_find(line1, "wn as", "\n", 5), 'Benny')
        line2 = '[13:56] <Dhruv> Rohan, Hi!'
        self.assertEqual(util.splice_find(line2,">", ", ", 1),"Rohan")      

    def test_get_nick_sen_rec(self):
        conn_comp_list = [["krishna","krish"],["rohan","rohano"],["rohit","rohit101"]]
        self.assertEqual(util.get_nick_sen_rec(3,"rohano",conn_comp_list,""),"rohan")
        self.assertEqual(util.get_nick_sen_rec(3,"krish",conn_comp_list,""),"krishna")

    def test_get_nick_representative(self):
        nicks = ["krishna","krish","rohan","rohit","rohano"]
        nick_same_list=[["krishna","krish"],["rohan","rohano"],["rohit"],[],[]] # look at nickTracker.py in that too nick_same_list has size = maxm expected diff nicks
        self.assertEqual(util.get_nick_representative(nicks,nick_same_list,"Dhruv"),"Dhruv")
        self.assertEqual(util.get_nick_representative(nicks,nick_same_list,"krish"),"krishna")


    def test_find_top_n_element_after_sorting(self):
        in_list = [[1,2,3],[3,1,2],[2,3,1]]
        self.assertListEqual(util.find_top_n_element_after_sorting(in_list, 1, False, 2),[[3,1,2], [1,2,3]])
        self.assertListEqual(util.find_top_n_element_after_sorting(in_list, 1, True, 2), [[2,3,1], [1,2,3]])         

if __name__ == '__main__':
    unittest.main()
