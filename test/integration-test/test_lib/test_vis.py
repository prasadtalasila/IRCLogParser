import unittest
import os
import numpy as np
from lib import vis,util
from mock import patch


class VisTest(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.test_data_dir = current_dir + "/../../data/test_lib/"

    def tearDown(self):
        self.test_data_dir = None

    def test_exponential_curve_fit_and_plot(self):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_len")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_len_fit")
        output = vis.exponential_curve_fit_and_plot(data, self.test_data_dir, "exponential_plot_test")
        # remove the plot created
        os.remove(self.test_data_dir + '/exponential_plot_test.png')
        assert np.allclose(output, expected_result)

    def test_exponential_curve_fit_and_plot_x_shifted(self):
        data = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/conv_ref_time_fit_params")
        output = vis.exponential_curve_fit_and_plot_x_shifted(data, self.test_data_dir, "exponential_plot_test_shifted")
        # delete the plot created
        os.remove(self.test_data_dir + '/exponential_plot_test_shifted.png')
        assert np.allclose(output, expected_result)

    @patch("lib.config.USE_PYPLOT",0)
    def test_generate_log_plots(self):
        data = util.load_from_disk(self.test_data_dir + "/vis/degree_msg_number")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/out_degree_analysis")
        output = vis.generate_log_plots(data, self.test_data_dir, "log_plot_test")
        # delete the plot created
        os.remove(self.test_data_dir + '/log_plot_test.png')
        assert np.allclose(output, expected_result)

    @patch("lib.config.USE_PYPLOT",1)
    def test_generate_log_plots_use_pyplot(self):
        data = util.load_from_disk(self.test_data_dir + "/vis/degree_msg_number")
        expected_result = util.load_from_disk(self.test_data_dir + "/vis/out_degree_analysis")
        output = vis.generate_log_plots(data, self.test_data_dir, "log_plot_test")
        # delete the plot created
        os.remove(self.test_data_dir + '/log_plot_test.png')
        assert np.allclose(output, expected_result)

if __name__ == '__main__':
    unittest.main()