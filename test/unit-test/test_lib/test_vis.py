import os
import sys
import unittest
from os import path
from mock import patch
import matplotlib.pyplot as plt
import plotly.plotly as py
import mock as Mock
import numpy as np
import networkx as nx
import plotly.graph_objs as go
from ddt import ddt, data, unpack

from lib import vis, util

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
current_dir = os.path.dirname(os.path.abspath(__file__))


@ddt
class VisTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @data(([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [1, 0, 1, 0]))
    @unpack
    @patch("lib.config.USE_PYPLOT", 1)
    def test_calc_plot_linear_fit_use_pylpot(self, x_in, y_in, expected_result):
        output = vis.calc_plot_linear_fit(x_in, y_in, current_dir, "linear_plot_test")
        # remove the image generated from plot function
        os.remove(current_dir + '/linear_plot_test.png')
        assert np.allclose(output, expected_result)

    @data(([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [1, 0, 1, 0]))
    @unpack
    @patch("lib.config.USE_PYPLOT", 0)
    def test_calc_plot_linear_fit_use_pylpot(self, x_in, y_in, expected_result):
        output = vis.calc_plot_linear_fit(x_in, y_in, current_dir, "linear_plot_test")
        # remove the image generated from plot function
        os.remove(current_dir + '/linear_plot_test.png')
        assert np.allclose(output, expected_result)

        output = vis.calc_plot_linear_fit(None, None, current_dir, "linear_plot_test")
        expected_output = -1, -1, -1, -1
        self.assertEqual(output, expected_output)

    @patch("matplotlib.pyplot.plot", autospec=True)
    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_plot_data(self, mock_savefig, mock_plot):
        data = ([[0, 1, 2, 3, 4, 5, 6, 7, 8], [0, 2, 4, 6, 8, 10, 12, 14, 16]])
        x_data, y_data = (d for d in data)
        x = np.array(x_data)
        y = np.array(y_data)

        vis.plot_data(data, current_dir, 'test')
        np.testing.assert_array_equal(x, mock_plot.call_args[0][0])
        np.testing.assert_array_equal(y, mock_plot.call_args[0][1])
        plt.savefig.assert_called_once_with(current_dir + "/" + "test" + ".png")

    @data(([[0, 5], [1, 10], [2, 5], [3, 7], [4, 3]],
           [float(5) / 30, float(10) / 30, float(5) / 30, float(7) / 30, float(3) / 30], [0, 1, 2, 3, 4]))
    @unpack
    def test_generate_probability_distribution(self, data, expected_freq, expected_x):
        x, freq = vis.generate_probability_distribution(data)
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(freq, expected_freq)

    def test_generate_probability_distribution(self):
        x, freq = vis.generate_probability_distribution(None)
        self.assertEqual(x, -1)
        self.assertEqual(freq, -1)

    @data(
        (util.load_from_disk(current_dir + "/data/conv_len"), util.load_from_disk(current_dir + "/data/conv_len_fit")))
    @unpack
    def test_exponential_curve_fit_and_plot(self, data, expected_result):
        output = vis.exponential_curve_fit_and_plot(data, current_dir, "exponential_plot_test")
        # remove the plot created
        os.remove(current_dir + '/exponential_plot_test.png')
        assert np.allclose(output, expected_result)

    @data((util.load_from_disk(current_dir + "/data/conv_ref_time"),
           util.load_from_disk(current_dir + "/data/conv_ref_time_fit_params")))
    @unpack
    def test_exponential_curve_fit_and_plot_x_shifted(self, data, expected_result):
        output = vis.exponential_curve_fit_and_plot_x_shifted(data, current_dir, "exponential_plot_test_shifted")
        # delete the plot created
        os.remove(current_dir + '/exponential_plot_test_shifted.png')
        assert np.allclose(output, expected_result)
    
    @patch("lib.config.DEBUGGER",1)
    @patch("igraph.plot",autospec=True)
    def test_plot_infomap_igraph_show_edges(self,mock_igraph_plot):
        message_graph = util.load_from_disk(current_dir+'/data/message_graph')
        membership = util.load_from_disk(current_dir+'/data/membership')
        igraph = util.load_from_disk(current_dir+'/data/igraph')
        vis.plot_infomap_igraph(message_graph,membership, current_dir, "message")
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))
       
       
    @data((util.load_from_disk(current_dir + "/data/degree_msg_number"),
           util.load_from_disk(current_dir + "/data/out_degree_analysis")))
    @unpack
    def test_generate_log_plots(self, data, expected_result):
        output = vis.generate_log_plots(data, current_dir, "log_plot_test")
        # delete the plot created
        os.remove(current_dir + '/log_plot_test.png')
        assert np.allclose(output, expected_result)

    @patch("plotly.plotly.image.save_as")
    def test_generate_group_bar_charts(self, mock_py):
        x_values = [
            [5.10114882, 5.0194652482, 4.9908093076],
            [4.5824497358, 4.7083614037, 4.3812775722],
            [2.6839471308, 3.0441476209, 3.6403820447]
        ]
        y_values = ['#kubuntu-devel', '#ubuntu-devel', '#kubuntu']
        trace_headers = ['head1', 'head2', 'head3']
        test_data = [
            go.Bar(
                x=x_values,
                y=y_values[i],
                name=trace_headers[i]
            ) for i in range(len(y_values))
        ]

        layout = go.Layout(barmode='group')
        fig = go.Figure(data=test_data, layout=layout)
        vis.generate_group_bar_charts(y_values, x_values, trace_headers, current_dir, 'test_group_bar_chart')
        assert mock_py.call_count == 1
        self.assertEqual(fig.get('data')[0], mock_py.call_args[0][0].get('data')[0])

    @patch("plotly.plotly.image.save_as")
    def test_csv_heatmap_generator_plotly(self, mock_py):
        test_data = np.array([[5075, 507, 634, 7237, 3421, 7522, 12180, 9635, 7381, 7967, 6224, 2712, 4758, 2704, 1763,
                               1869, 4428, 1680],
                              [1652, 425, 269, 982, 2687, 15318, 3865, 3213, 4411, 6821, 1960, 7007, 883, 4592, 0, 3271,
                               619, 1508],
                              [1578, 924, 409, 1115, 6088, 491, 1923, 10700, 16206, 8690, 1350, 3778, 237, 1095, 20639,
                               2669, 1956, 6015]])

        trace = go.Heatmap(
            z=test_data,
            x=list(range(48)),
            y=list(range(1, 12)),
            colorscale=[
                [0, 'rgb(255, 255, 204)'],
                [0.13, 'rgb(255, 237, 160)'],
                [0.25, 'rgb(254, 217, 118)'],
                [0.38, 'rgb(254, 178, 76)'],
                [0.5, 'rgb(253, 141, 60)'],
                [0.63, 'rgb(252, 78, 42)'],
                [0.75, 'rgb(227, 26, 28)'],
                [0.88, 'rgb(189, 0, 38)'],
                [1.0, 'rgb(128, 0, 38)']
            ]
        )

        final_data = [trace]
        layout = go.Layout(title='HeatMap', width=800, height=640)
        fig = go.Figure(data=final_data, layout=layout)

        vis.csv_heatmap_generator_plotly(current_dir + "/data/", current_dir, "plotly_heatmap_test")
        assert mock_py.call_count == 1
        self.assertTrue(fig.get('layout') == mock_py.call_args[0][0].get('layout'))
        np.testing.assert_array_equal(fig.data[0].get('z'), mock_py.call_args[0][0].data[0].get('z'))

    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_matplotlob_csv_heatmap_generator(self, mock_savefig):
        data = np.array([[5075, 507, 634, 7237, 3421, 7522, 12180, 9635, 7381, 7967, 6224, 2712, 4758, 2704, 1763, 1869,
                          4428, 1680],
                         [1652, 425, 269, 982, 2687, 15318, 3865, 3213, 4411, 6821, 1960, 7007, 883, 4592, 0, 3271, 619,
                          1508],
                         [1578, 924, 409, 1115, 6088, 491, 1923, 10700, 16206, 8690, 1350, 3778, 237, 1095, 20639, 2669,
                          1956, 6015]])
        vis.matplotlob_csv_heatmap_generator(current_dir + "/" + "data/test_heatmap.csv", current_dir,
                                             "csv_heatmap_test")
        plt.savefig.assert_called_once_with(current_dir + "/" + "csv_heatmap_test" + ".png")

    @patch("matplotlib.pyplot.boxplot", autospec=True)
    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_box_plot(self, mock_savefig, mock_boxplot):
        data = [0, 1, 2, 3, 4, 5, 6, 7, 8]

        vis.box_plot(data, current_dir, 'box_plot_test')
        plt.boxplot.assert_called_once_with(data)
        plt.savefig.assert_called_once_with(current_dir + "/" + "box_plot_test" + ".png")


if __name__ == '__main__':
    unittest.main()
