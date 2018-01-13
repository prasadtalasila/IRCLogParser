import os
import sys
import unittest
from os import path

import matplotlib.pyplot as plt

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib import vis, util
from ddt import ddt, data, unpack
import numpy as np
from mock import patch

current_dir = os.path.dirname(os.path.abspath(__file__))

@ddt
class VisTest(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    @data(([0,1,2,3,4,5], [0,1,2,3,4,5], [1,0,1,0]))
    @unpack
    def test_calc_plot_linear_fit(self, x_in, y_in, expected_result):
        
        output = vis.calc_plot_linear_fit(x_in, y_in, current_dir, "linear_plot_test")

        #remove the image generated from plot function
        os.remove(current_dir + '/linear_plot_test.png')
        
        assert np.allclose(output, expected_result)

    @patch("matplotlib.pyplot.plot", autospec = True)
    @patch("matplotlib.pyplot.savefig", autospec = True)
    def test_plot_data(self,mock_savefig,mock_plot):
        data = ([[0,1,2,3,4,5,6,7,8],[0,2,4,6,8,10,12,14,16]])
        x_data, y_data = (d for d in data)
        x = np.array(x_data)
        y = np.array(y_data)

        vis.plot_data(data,current_dir,'test')
        np.testing.assert_array_equal(x, mock_plot.call_args[0][0])
        np.testing.assert_array_equal(y, mock_plot.call_args[0][1])
        plt.savefig.assert_called_once_with(current_dir + "/" + "test" + ".png")

    @data(([ [0,5], [1,10], [2,5], [3,7], [4,3] ], [float(5)/30, float(10)/30, float(5)/30, float(7)/30, float(3)/30], [0, 1, 2, 3, 4]))
    @unpack
    def test_generate_probability_distribution(self, data, expected_freq, expected_x):
        
        x, freq = vis.generate_probability_distribution(data)
        
        self.assertAlmostEqual(x, expected_x)
        self.assertAlmostEqual(freq, expected_freq)
    
    @data((util.load_from_disk(current_dir + "/data/conv_len"), util.load_from_disk(current_dir + "/data/conv_len_fit")))
    @unpack
    def test_exponential_curve_fit_and_plot(self, data, expected_result):
        
        output = vis.exponential_curve_fit_and_plot(data, current_dir, "exponential_plot_test")
        
        #remove the plot created
        os.remove(current_dir + '/exponential_plot_test.png')
        
        assert np.allclose(output, expected_result)
    
    @data((util.load_from_disk(current_dir + "/data/conv_ref_time"), util.load_from_disk(current_dir + "/data/conv_ref_time_fit_params")))
    @unpack
    def test_exponential_curve_fit_and_plot_x_shifted(self, data, expected_result):
    
        output = vis.exponential_curve_fit_and_plot_x_shifted(data, current_dir, "exponential_plot_test_shifted")
        
        #delete the plot created
        os.remove(current_dir + '/exponential_plot_test_shifted.png')
        
        assert np.allclose(output, expected_result)
    
    @data((util.load_from_disk(current_dir + "/data/degree_msg_number"), util.load_from_disk(current_dir + "/data/out_degree_analysis")))
    @unpack
    def test_generate_log_plots(self, data, expected_result):
        
        output = vis.generate_log_plots(data, current_dir, "log_plot_test")
        
        #delete the plot created
        os.remove(current_dir + '/log_plot_test.png')
        
        assert np.allclose(output, expected_result)
        
        
if __name__ == '__main__':
    unittest.main()
