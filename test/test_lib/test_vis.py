import unittest
import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from lib import vis
from lib import config

current_dir = os.path.dirname(os.path.abspath(__file__))

class VisTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_calc_plot_linear_fit(self):
        x_in = [0,1,2,3,4,5]
        y_in = [0,1,2,3,4,5]
        
        slope, intercept, r_value, mse = vis.calc_plot_linear_fit(x_in, y_in, current_dir, "linear_plot_test")
        os.remove(current_dir + '/linear_plot_test.png')
        assert slope == 1 and intercept == 0 and mse == 0
        
    def test_generate_probability_distribution(self):
        
        data = [ [0,5], [1,10], [2,5], [3,7], [4,3] ]
        expected_freq = [float(5)/30, float(10)/30, float(5)/30, float(7)/30, float(3)/30]
        expected_x = [0, 1, 2, 3, 4]
        
        x, freq = vis.generate_probability_distribution(data)
        
        assert x == expected_x
        assert freq == expected_freq

if __name__ == '__main__':
    unittest.main()

