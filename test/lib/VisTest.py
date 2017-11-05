import unittest
import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib import vis
from lib import config
from ddt import ddt, data, unpack

current_dir = os.path.dirname(os.path.abspath(__file__))

@ddt
class VisTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    @data(([0,1,2,3,4,5], [0,1,2,3,4,5], (1,0,0)))
    @unpack
    def test_calc_plot_linear_fit(self, x_in, y_in, expected_result):
        
        slope, intercept, r_value, mse = vis.calc_plot_linear_fit(x_in, y_in, current_dir, "linear_plot_test")
        expected_slope, expected_intercept, expected_mse = expected_result
        
        #remove the image generated from plot function
        os.remove('linear_plot_test.png')
        
        assert slope == expected_slope and intercept == expected_intercept and mse == expected_mse
    
    @data(([ [0,5], [1,10], [2,5], [3,7], [4,3] ], [float(5)/30, float(10)/30, float(5)/30, float(7)/30, float(3)/30], [0, 1, 2, 3, 4]))
    @unpack
    def test_generate_probability_distribution(self, data, expected_freq, expected_x):
        
        x, freq = vis.generate_probability_distribution(data)
        
        assert x == expected_x
        assert freq == expected_freq
    
    @data(())
    @unpack
    def test_exponential_curve_fit_and_plot(self, data, expected_result):
        
        a, b, c, mse = vis.exponential_curve_fit_and_plot(data, current_dir, "exponential_plot_test")
        
        #remove the plot created
        os.remove('exponential_plot_test.png')
        
        ex_a, ex_b, ex_c, ex_mse = expected_result
        
        assert a == ex_a
        assert b == ex_b
        assert c == ex_c
        assert mse == ex_mse
    
    @data
    @unpack
    def test_exponential_curve_fit_and_plot_x_shifted(self, data, expected_result):
    
        a, b, c, mse, first_non_zero_index = vis.exponential_curve_fit_and_plot(data, current_dir, "exponential_plot_test")
        
        #delete the plot created
        os.remove('exponential_plot_test.png')
        
        ex_a, ex_b, ex_c, ex_mse, ex_first_non_zero_index = expected_result
        
        assert a == ex_a
        assert b == ex_b
        assert c == ex_c
        assert mse == ex_mse
        assert first_non_zero_index == ex_first_non_zero_index
    
    @data
    @unpack
    def test_generate_log_plots(self, data, expected_result):
        
        slope,intercept,r_square,mse = vis.generate_log_plots(data, current_dir, "log_plot_test")
        
        #delete the plot created
        os.remove('log_plot_test.png')
        
        expected_slope, expected_mse, expected_r_sqaure, expected_mse = expected_results
        
        assert slope == expected_slope
        assert intercept == expected_intercept
        assert r_sqaure == expected_r_square
        assert mse == expected_mse
        
        
if __name__ == '__main__':
    unittest.main()

