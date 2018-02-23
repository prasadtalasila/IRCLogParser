import os
import unittest

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objs as go
from ddt import ddt, data, unpack
from mock import patch

from lib import vis, util


def mock_exponential_curve_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def mock_generate_probability_distribution(data):
    topRows = [int(x[1]) for x in data]
    total = sum(topRows)
    freq = [x/float(total) for x in topRows]
    return range(0, len(data)), freq

@ddt
class VisTest(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = current_dir + "/../../data/test_lib/"

    def tearDown(self):
        self.test_data_dir = None

    @data(([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [1, 0, 1, 0]))
    @unpack
    @patch("lib.config.USE_PYPLOT", 1)
    def test_calc_plot_linear_fit_use_pylpot(self, x_in, y_in, expected_result):
        output = vis.calc_plot_linear_fit(x_in, y_in, self.test_data_dir, "linear_plot_test")
        # remove the image generated from plot function
        os.remove(self.test_data_dir + '/linear_plot_test.png')
        assert np.allclose(output, expected_result)

    @data(([0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5], [1, 0, 1, 0]))
    @unpack
    @patch("lib.config.USE_PYPLOT", 0)
    def test_calc_plot_linear_fit_use_pylpot(self, x_in, y_in, expected_result):
        output = vis.calc_plot_linear_fit(x_in, y_in, self.test_data_dir, "linear_plot_test")
        # remove the image generated from plot function
        os.remove(self.test_data_dir + '/linear_plot_test.png')
        assert np.allclose(output, expected_result)

        output = vis.calc_plot_linear_fit(None, None, self.test_data_dir, "linear_plot_test")
        expected_output = -1, -1, -1, -1
        self.assertEqual(output, expected_output)

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

    def test_generate_probability_distribution(self):
        x, freq = vis.generate_probability_distribution(None)
        self.assertEqual(x, -1)
        self.assertEqual(freq, -1)

    @patch("lib.vis.generate_probability_distribution", autospec=True)
    @patch("lib.util.exponential_curve_func", autospec = True)
    @patch("lib.vis.curve_fit", autospec=True)
    def test_exponential_curve_fit_and_plot(self, mock_curve_fit, mock_curve_func, mock_probability_distribution):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_len")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_len_fit")
        mock_curve_fit.return_value = util.load_from_disk(self.test_data_dir+ "/vis/curve_fit")
        mock_curve_func.side_effect = mock_exponential_curve_func
        mock_probability_distribution.side_effect = mock_generate_probability_distribution

        output = vis.exponential_curve_fit_and_plot(data, self.test_data_dir, "exponential_plot_test")
        os.remove(self.test_data_dir + '/exponential_plot_test.png')
        assert np.allclose(output, expected_result)

    @patch("lib.vis.generate_probability_distribution", autospec=True)
    @patch("lib.util.exponential_curve_func", autospec = True)
    @patch("lib.vis.curve_fit", autospec=True)
    def test_exponential_curve_fit_and_plot_x_shifted(self, mock_curve_fit, mock_curve_func, mock_probability_distribution):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time_fit_params")
        mock_curve_fit.return_value = util.load_from_disk(self.test_data_dir + "/vis/curve_fit_x_shifted")
        mock_curve_func.side_effect = mock_exponential_curve_func
        mock_probability_distribution.side_effect = mock_generate_probability_distribution

        output = vis.exponential_curve_fit_and_plot_x_shifted(data, self.test_data_dir, "exponential_plot_test_shifted")
        # delete the plot created
        os.remove(self.test_data_dir + '/exponential_plot_test_shifted.png')
        assert np.allclose(output, expected_result)
    
    @patch("lib.config.DEBUGGER",1)
    @patch("igraph.plot",autospec=True)
    def test_plot_infomap_igraph_no_edges(self,mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir+'/vis/message_graph')
        membership = util.load_from_disk(self.test_data_dir+'/vis/membership')
        igraph = util.load_from_disk(self.test_data_dir+'/vis/igraph')
        
        # test infomap plotting with edges not shown
        vis.plot_infomap_igraph(message_graph,membership, self.test_data_dir, "message", show_edges=False)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))
        
        # check infomap generation with None membership
        vis.plot_infomap_igraph(message_graph,None, self.test_data_dir, "message")
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))
        
    @patch("lib.config.DEBUGGER",1)
    @patch("igraph.plot",autospec=True)
    def test_plot_infomap_igraph_show_edges(self,mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir+'/vis/message_graph')
        membership = util.load_from_disk(self.test_data_dir+'/vis/membership')
        igraph = util.load_from_disk(self.test_data_dir+'/vis/igraph')
        
        # test for infomap generation with edges
        vis.plot_infomap_igraph(message_graph,membership, self.test_data_dir, "message", show_edges=True)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))
        
    @patch("lib.config.DEBUGGER",1)
    @patch("igraph.plot",autospec=True)
    def test_plot_infomap_igraph_aux_data(self,mock_igraph_plot):
        message_graph = util.load_from_disk(self.test_data_dir+'vis/message_exchange_graph')
        membership = util.load_from_disk(self.test_data_dir+'vis/message_exchange_graph_membership')
        igraph = util.load_from_disk(self.test_data_dir+'vis/message_exchange_igraph')
        aux = util.load_from_disk(self.test_data_dir+'vis/aux_data')
        
        # test for infomap generation with auxiliary data
        vis.plot_infomap_igraph(message_graph,membership, self.test_data_dir, "message", aux_data = aux)
        self.assertTrue(mock_igraph_plot.call_args[0][0].isomorphic_vf2(igraph))

    @patch("lib.vis.calc_plot_linear_fit", autospec=True)
    def test_generate_log_plots(self, mock_calc_plot):
        data = util.load_from_disk(self.test_data_dir + "/vis/degree_msg_number")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/out_degree_analysis")
        mock_calc_plot.return_value = util.load_from_disk(self.test_data_dir + "vis/calc_plot_data")
        output = vis.generate_log_plots(data, self.test_data_dir, "log_plot_test")
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
        vis.generate_group_bar_charts(y_values, x_values, trace_headers, self.test_data_dir, 'test_group_bar_chart')
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

        vis.csv_heatmap_generator_plotly(self.test_data_dir + "/vis/", self.test_data_dir, "plotly_heatmap_test")
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
