import os
import unittest

import matplotlib.pyplot as plt
import numpy as np
from ddt import ddt, data, unpack
from mock import patch

from lib import vis, util


@ddt
class VisTest(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = current_dir + "/../../data/test_lib/"

    def tearDown(self):
        self.test_data_dir = None

    def mock_exponential_curve_func(self,x, a, b, c):
        return a * np.exp(-b * x) + c

    def mock_generate_probability_distribution(self, data):
        topRows = [int(x[1]) for x in data]
        total = sum(topRows)
        freq = [x / float(total) for x in topRows]
        return range(0, len(data)), freq

    @data(([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [1, 0, 1, 0]))
    @unpack
    def test_calc_plot_linear_fit(self, x_in, y_in, expected_result):
        expected_output = vis.calc_plot_linear_fit(x_in, y_in, self.test_data_dir, "linear_plot_test")
        # remove the image generated from plot function
        os.remove(self.test_data_dir + '/linear_plot_test.png')
        self.assertTrue(np.allclose(expected_output, expected_result))

        expected_output = vis.calc_plot_linear_fit(None, None, self.test_data_dir, "linear_plot_test")
        expected_result = -1, -1, -1, -1
        self.assertEqual(expected_output, expected_result)

    @patch("matplotlib.pyplot.plot", autospec=True)
    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_plot_data(self, mock_savefig, mock_plot):
        data = ([[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 2, 4, 6, 8, 10, 12, 14, 16]])
        x_data, y_data = (d for d in data)
        x = np.array(x_data)
        y = np.array(y_data)

        vis.plot_data(data, self.test_data_dir, 'test')
        np.testing.assert_array_equal(x, mock_plot.call_args[0][0])
        np.testing.assert_array_equal(y, mock_plot.call_args[0][1])
        plt.savefig.assert_called_once_with(self.test_data_dir + "/" + "test" + ".png")

    @data(([[0, 5], [1, 10], [2, 5], [3, 7], [4, 3]],
           [float(5) / 30, float(10) / 30, float(5) / 30, float(7) / 30, float(3) / 30], [0, 1, 2, 3, 4]))
    @unpack
    def test_generate_probability_distribution(self, data, expected_freq, expected_x):
        x, freq = vis.generate_probability_distribution(data)
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(freq, expected_freq)

    def test_generate_probability_distribution_no_data(self):
        x, freq = vis.generate_probability_distribution(None)
        self.assertEqual(x, -1)
        self.assertEqual(freq, -1)

    @patch("lib.vis.generate_probability_distribution", autospec=True)
    @patch("lib.util.exponential_curve_func", autospec=True)
    @patch("lib.vis.curve_fit", autospec=True)
    def test_exponential_curve_fit_and_plot(self, mock_curve_fit, mock_curve_func, mock_probability_distribution):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_len")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_len_fit")
        mock_curve_fit.return_value = util.load_from_disk(self.test_data_dir + "/vis/curve_fit")
        mock_curve_func.side_effect = self.mock_exponential_curve_func
        mock_probability_distribution.side_effect = self.mock_generate_probability_distribution

        expected_output = vis.exponential_curve_fit_and_plot(data, self.test_data_dir, "exponential_plot_test")
        os.remove(self.test_data_dir + '/exponential_plot_test.png')
        self.assertTrue(np.allclose(expected_output, expected_result))

    @patch("lib.vis.generate_probability_distribution", autospec=True)
    @patch("lib.util.exponential_curve_func", autospec=True)
    @patch("lib.vis.curve_fit", autospec=True)
    def test_exponential_curve_fit_and_plot_x_shifted(self, mock_curve_fit, mock_curve_func,
                                                      mock_probability_distribution):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time_fit_params")
        mock_curve_fit.return_value = util.load_from_disk(self.test_data_dir + "/vis/curve_fit_x_shifted")
        mock_curve_func.side_effect = self.mock_exponential_curve_func
        mock_probability_distribution.side_effect = self.mock_generate_probability_distribution

        expected_output = vis.exponential_curve_fit_and_plot_x_shifted(data, self.test_data_dir, "exponential_plot_test_shifted")
        # delete the plot created
        os.remove(self.test_data_dir + '/exponential_plot_test_shifted.png')
        self.assertTrue(np.allclose(expected_output, expected_result))

    @patch("lib.config.DEBUGGER", 1)
    @patch("igraph.plot", autospec=True)
    def test_plot_infomap_igraph_no_edges(self, mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir + '/vis/message_graph')
        membership = util.load_from_disk(self.test_data_dir + '/vis/membership')
        igraph = util.load_from_disk(self.test_data_dir + '/vis/igraph')

        # test infomap plotting with edges not shown
        vis.plot_infomap_igraph(message_graph, membership, self.test_data_dir, "message", show_edges=False)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))

        # check infomap generation with None membership
        vis.plot_infomap_igraph(message_graph, None, self.test_data_dir, "message")
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))

    @patch("lib.config.DEBUGGER", 1)
    @patch("igraph.plot", autospec=True)
    def test_plot_infomap_igraph_show_edges(self, mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir + '/vis/message_graph')
        membership = util.load_from_disk(self.test_data_dir + '/vis/membership')
        igraph = util.load_from_disk(self.test_data_dir + '/vis/igraph')

        # test for infomap generation with edges
        vis.plot_infomap_igraph(message_graph, membership, self.test_data_dir, "message", show_edges=True)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))

    @patch("lib.config.DEBUGGER", 1)
    @patch("igraph.plot", autospec=True)
    def test_plot_infomap_igraph_aux_data(self, mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir + 'vis/message_exchange_graph')
        membership = util.load_from_disk(self.test_data_dir + 'vis/message_exchange_graph_membership')
        igraph = util.load_from_disk(self.test_data_dir + 'vis/message_exchange_igraph')
        aux = util.load_from_disk(self.test_data_dir + 'vis/aux_data')

        # test for infomap generation with auxiliary data
        vis.plot_infomap_igraph(message_graph, membership, self.test_data_dir, "message", aux_data=aux)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))

    @patch("lib.vis.calc_plot_linear_fit", autospec=True)
    def test_generate_log_plots(self, mock_calc_plot):
        data = util.load_from_disk(self.test_data_dir + "/vis/degree_msg_number")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/out_degree_analysis")
        mock_calc_plot.return_value = util.load_from_disk(self.test_data_dir + "vis/calc_plot_data")
        expected_output = vis.generate_log_plots(data, self.test_data_dir, "log_plot_test")
        self.assertTrue(np.allclose(expected_output, expected_result))

    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_matplotlob_csv_heatmap_generator(self, mock_savefig):
        data = np.array([[5075, 507, 634, 7237, 3421, 7522, 12180, 9635, 7381, 7967, 6224, 2712, 4758, 2704, 1763, 1869,
                          4428, 1680],
                         [1652, 425, 269, 982, 2687, 15318, 3865, 3213, 4411, 6821, 1960, 7007, 883, 4592, 0, 3271, 619,
                          1508],
                         [1578, 924, 409, 1115, 6088, 491, 1923, 10700, 16206, 8690, 1350, 3778, 237, 1095, 20639, 2669,
                          1956, 6015]])
        vis.matplotlob_csv_heatmap_generator(self.test_data_dir + "/" + "vis/test_heatmap.csv", self.test_data_dir,
                                             "csv_heatmap_test")
        plt.savefig.assert_called_once_with(self.test_data_dir + "/" + "csv_heatmap_test" + ".png")

    @patch("matplotlib.pyplot.boxplot", autospec=True)
    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_box_plot(self, mock_savefig, mock_boxplot):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        vis.box_plot(data, self.test_data_dir, 'box_plot_test')
        plt.boxplot.assert_called_once_with(data)
        plt.savefig.assert_called_once_with(self.test_data_dir + "/" + "box_plot_test" + ".png")


if __name__ == '__main__':
    unittest.main()
