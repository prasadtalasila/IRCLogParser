import unittest
import os
import commands
import subprocess
import igraph
import lib.network_util as nx
import lib.slack.util as util
import lib.slack.config as config
from ddt import ddt, data, unpack
from mock import patch


def mock_to_edges(l):
    it = iter(l)
    last = next(it)
    for current in it:
        yield last, current
        last = current


def mock_correctLastCharCR(inText):
    if(len(inText) > 1 and inText[len(inText)-1]=='\\'):
        inText = inText[:-1]+'CR'
    return inText


@ddt
class UtilTest(unittest.TestCase):

    def setUp(self):
        self.nicks = ['BluesKaj', 'Peace-', 'LordOfTime', 'TheLordOfTime', 'benonsoftware', 'Benny', 'Guest43293', 'rdieter_work', 'rdieter', 'jjesse-home_', 'jjesse-home', 'rdieter1', 'Mamarok', 'Mamarok_', 'G4MBY', 'PaulW2U', 'jussi', 'shadeslayer', 'Tm_T', 'yofel', 'ScottK', 'Quintasan', 'mikhas', 'ubottu', 'Noskcaj', 'Riddell', 'Tonio_', 'Tonio_aw', 'yofel_', 'Quintasan_']
        self.expected_nicks = self.nicks
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        self.nicks = None
        self.expected_nicks = None
        self.current_directory = None

    @data(("ThunderBolt\\", "ThunderBoltCR"))
    @unpack
    def test_correctLastCharCR(self, input_nick, expected_output_nick):
        self.assertEqual(util.correctLastCharCR(input_nick), expected_output_nick)

    @data(("ThunderBolt_", "ThunderBolt"))
    @unpack
    def test_correct_nick_for_(self, input_nick, expected_output_nick):
        self.assertEqual(util.correct_nick_for_(input_nick), expected_output_nick)

    @data(([["ThunderBolt", "ka", "Thunder"], ["paper", "paperu", "papera"]],
           [("ThunderBolt", "ka"), ("ka", "Thunder"), ("paperu", "paper"), ("papera", "paperu")]))
    @unpack
    def test_to_graph(self, same_nick_list, edge_list):
        expected_graph = nx.Graph()
        expected_graph.add_edges_from(edge_list)
        self.assertTrue(nx.is_isomorphic(util.to_graph(same_nick_list), expected_graph))

    @data((['a', 'b', 'c', 'd'], [('a', 'b'), ('b', 'c'), ('c', 'd')]))
    @unpack
    def test_to_edges(self, input_vertices, expected_output):
        self.assertListEqual(list(util.to_edges(input_vertices)), expected_output)

    @data((0, 2, 0, 1, 3.0))
    @unpack
    def test_exponential_curve_func(self, x, a, b, c, expected_result):
        self.assertEqual(util.exponential_curve_func(x, a, b, c), expected_result)

    @data(({"log_data": None,
            "auxiliary_data": {
                "channel": None,
                "year": 2017,
                "month": 10,
                "day": 7}
            },
           ('2017', '10', '7')))
    @unpack
    def test_get_year_month_day(self, auxiliary_day_content, expected_output):
        self.assertEqual(util.get_year_month_day(auxiliary_day_content), expected_output)

    @data(("[13:48] <ScottK> shadeslayer: It wasn't empty when I made it.",
           ['[13', '48] <ScottK> shadeslayer', "t wasn't empty when I made it."]))
    @unpack
    def test_rec_list_splice(self, line, expected_result):
        rec_list = [e.strip() for e in line.split(':')]
        util.rec_list_splice(rec_list)
        self.assertListEqual(rec_list, expected_result)

    @data(('[11:10] <canci> hi everyone','hi everyone'))
    @unpack
    def test_check_if_msg_line(self, line,line2):
        self.assertTrue(util.check_if_msg_line(line))
        self.assertFalse(util.check_if_msg_line(line2))

    def test_build_graphs(self):
        day_graph, expected_day_graph, aggr_graph, expected_aggr_graph = nx.DiGraph(), nx.DiGraph(), nx.DiGraph(), nx.DiGraph()
        expected_day_graph.add_edge("ThunderBolt", "lethifer", weight="11:00")
        expected_aggr_graph.add_edge("ThunderBolt", "lethifer", weight="2017" + "/" + "10" + "/" + "7" + " - " + "11:00")
        util.build_graphs("ThunderBolt", "lethifer", "11:00", "2017", "10", "7", day_graph, aggr_graph)
        self.assertTrue(nx.is_isomorphic(day_graph, expected_day_graph))
        self.assertTrue(nx.is_isomorphic(aggr_graph, expected_aggr_graph))

    def test_HACK_convert_nx_igraph(self):
        test_nx_graph = nx.Graph()
        test_nx_graph.add_nodes_from([1, 3])
        test_nx_graph.add_edges_from([(1, 3), (1, 2)])
        result = util.HACK_convert_nx_igraph(test_nx_graph)
        test_igraph = igraph.Graph()
        test_igraph.add_vertices(3)
        test_igraph.add_edges([(0, 1), (0, 2)])
        self.assertTrue(test_igraph.isomorphic(result))

    def test_extend_conversation_list(self):
        conversations = [[0] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]
        util.extend_conversation_list("ThunderBolt", "lethifer", conversations)
        util.extend_conversation_list("ThunderBolt", "lethifer", conversations)
        util.extend_conversation_list("lethifer", "paper", conversations)
        self.assertListEqual(conversations[0:2], [[2, "ThunderBolt", "lethifer"], [1, "lethifer", "paper"]])

    @data(([set(['a', 'b', 'c']), set(['e', 'f', 'g'])], [['a', 'b', 'c'], ['e', 'f', 'g']]))
    @unpack
    def test_create_connected_nick_list(self, conn_comp_list, expected_conn_comp_list):
        util.create_connected_nick_list(conn_comp_list)
        # sorted has to be uses as set to list conversion leads to change in ordering
        self.assertEqual((sorted(conn_comp_list[0]), sorted(conn_comp_list[1])), \
                         (sorted(expected_conn_comp_list[0]), sorted(expected_conn_comp_list[1])))

    @data((["lethifer\\", "paper\\", "ThunderBolt\\"], ["lethiferCR", "paperCR", "ThunderBoltCR"]))
    @unpack
    @patch("lib.util.correctLastCharCR",autospec = True)
    def test_correct_last_char_list(self, nick_list, expected_result, mock_correctLastChar):
        mock_correctLastChar.side_effect = mock_correctLastCharCR
        self.assertListEqual(util.correct_last_char_list(nick_list), expected_result)

    @data(('=== benonsoftware is now known as Benny\n', "=", " is", 3, 'benonsoftware'), \
          ('=== benonsoftware is now known as Benny\n', "wn as", "\n", 5, 'Benny'), \
          ('[13:56] <Dhruv> lethifer, Hi!', ">", ", ", 1, "lethifer"))
    @unpack
    @patch("lib.util.correctLastCharCR",autospec = True)
    def test_splice_find(self, line, search_param1, search_param2, splice_index, expected_result, mock_correctLastChar):
        mock_correctLastChar.side_effect = mock_correctLastCharCR
        self.assertEqual(util.splice_find(line, search_param1, search_param2, splice_index), expected_result)

    @data((3, "lethifero", [["ThunderBolt", "Thunder"], ["lethifer", "lethifero"], ["paper", "paper101"]], "", "lethifer"), \
          (3, "Thunder", [["ThunderBolt", "Thunder"], ["lethifer", "lethifero"], ["paper", "paper101"]], "", "ThunderBolt"))
    @unpack
    def test_get_nick_sen_rec(self, iter_range, nick_to_search, conn_comp_list, nick_sen_rec, expected_result):
        self.assertEqual(util.get_nick_sen_rec(iter_range, nick_to_search, conn_comp_list, nick_sen_rec),
                         expected_result)
        self.assertEqual(util.get_nick_sen_rec(3, "Thunder", conn_comp_list, ""), "ThunderBolt")

    @data((["ThunderBolt", "Thunder", "lethifer", "paper", "lethifero"],
           [["ThunderBolt", "Thunder"], ["lethifer", "lethifero"], ["paper"], [], []], "toretto", "toretto"), \
          (["ThunderBolt", "Thunder", "lethifer", "paper", "lethifero"],
           [["ThunderBolt", "Thunder"], ["lethifer", "lethifero"], ["paper"], [], []], "Thunder", "ThunderBolt"))
    @unpack
    def test_get_nick_representative(self, nicks, nick_same_list, nick_to_compare, expected_result):
        # look at nickTracker.py in that too nick_same_list has size = maxm expected diff nicks
        self.assertEqual(util.get_nick_representative(nicks, nick_same_list, nick_to_compare), expected_result)

    @data(([[1, 2, 3], [3, 1, 2], [2, 3, 1]], 1, False, 2, [[3, 1, 2], [1, 2, 3]]), \
          ([[1, 2, 3], [3, 1, 2], [2, 3, 1]], 1, True, 2, [[2, 3, 1], [1, 2, 3]]))
    @unpack
    def test_find_top_n_element_after_sorting(self, in_list, index, reverseBool, n, expected_output):
        self.assertListEqual(util.find_top_n_element_after_sorting(in_list, index, reverseBool, n), expected_output)

    @data([['ThunderBolt', 'ThunderBoltBolt', 'Bolt'],
                ['Lethi', 'Lethifer'],
                ['Paper', 'Paperless', 'Paparoni', 'Pepperazi'],
                []])
    def test_count_number_of_users_on_channel(self,data):
        result = util.count_number_of_users_on_channel(data)
        self.assertEqual(result, 3)

    def test_save_to_disk(self):
        util.save_to_disk(self.nicks, self.current_directory + "/data/nicksTest")
        status, output = commands.getstatusoutput('cmp '+ self.current_directory +'/data/nicks '+ self.current_directory+ '/data/nicksTest')
        subprocess.Popen(['rm', self.current_directory + '/data/nicksTest'])
        self.assertEqual(status, 0, "Failure to load from disk.")

    def test_load_from_disk(self):
        nicks = util.load_from_disk(self.current_directory + '/data/nicks')
        self.assertEqual(nicks, self.expected_nicks, "Failure to load from disk.")


if __name__ == '__main__':
    unittest.main()
