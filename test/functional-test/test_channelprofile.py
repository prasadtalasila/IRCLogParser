import unittest
import os
import lib.in_out.reader as reader
import lib.nickTracker as nickTracker
import lib.util as util
import lib.vis as vis
from lib.analysis import network,channel
from mock import patch


class ChannelProfileTest(unittest.TestCase):

    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))
        self.log_data_dir = self.current_directory+"/data/input/"
        self.log_data_kubuntu_devel = reader.linux_input(self.log_data_dir,["#kubuntu-devel"], '2013-01-01', '2013-01-31')
        self.nicks, self.nick_same_list = nickTracker.nick_tracker(self.log_data_kubuntu_devel)

    def tearDown(self):
        self.current_directory = None
        self.log_data_dir = None
        self.log_data_kubuntu_devel = None
        self.nicks = None
        self.nick_same_list = None

    def test_activity_graph(self):
        self.expected_result = util.load_from_disk(self.current_directory+"/data/output/activity_graph")
        bin_matrix, total_messages = network.message_number_bins_csv(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list)
        expected_output = [[i for i in range(len(bin_matrix[0]))]]
        expected_output.append([sum(i) for i in zip(*bin_matrix)])
        self.assertTrue(expected_output,self.expected_result)

    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_conversation_characteristics_cutoff_0(self,mock_savefig):
        cutoff = 0
        expected_result_conv_len = [0.46025248575487415, 1.8745480617100398, 0.0014084453709393393, 1.8113237256968182e-05]
        expected_result_resp_time = [0.26599443483759627, 0.38817554962605116, 0.00012042990450484642, 1.1831364434688785e-05]
        expected_result_conv_ref = [0.004067315269095536, 0.01296093837728012, 1.761952783942606e-05, 5.6259486000435723e-08, 60]

        truncated_rt, rt_cutoff_time = channel.response_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, cutoff)
        conv_len, conv_ref_time = channel.conv_len_conv_refr_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, rt_cutoff_time, cutoff)
        expected_output_conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, self.current_directory, "conv_len_cutoff" + str(cutoff))
        expected_output_resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(truncated_rt, self.current_directory, "resp_time_cutoff" + str(cutoff))
        expected_output_conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, self.current_directory, "conv_ref_time_cutoff" + str(cutoff))
        self.assertTrue(expected_output_conv_len_curve_fit_parameters, expected_result_conv_len)
        self.assertTrue(expected_output_resp_time_curve_fit_parameters, expected_result_resp_time)
        self.assertTrue(expected_output_conv_ref_time_curve_fit_parameters, expected_result_conv_ref)

    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_conversation_characteristics_cutoff_1(self,mock_savefig):
        cutoff = 1
        expected_result_conv_len = [0.45678248067618998, 1.9431782685053713, 0.0030314547153581827, 3.3570362370587976e-05]
        expected_result_resp_time = [0.26876242441433712, 0.38822996056503406, 0.0001355301591146847, 1.4291783519203551e-05]
        expected_result_conv_ref = [0.0031066946048193583, 0.0089793356687177077, 2.3338045062882878e-05, 8.2373085916393017e-08, 66]

        truncated_rt, rt_cutoff_time = channel.response_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, cutoff)
        conv_len, conv_ref_time = channel.conv_len_conv_refr_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, rt_cutoff_time, cutoff)
        expected_output_conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, self.current_directory, "conv_len_cutoff" + str(cutoff))
        expected_output_resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(truncated_rt, self.current_directory, "resp_time_cutoff" + str(cutoff))
        expected_output_conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, self.current_directory, "conv_ref_time_cutoff" + str(cutoff))
        self.assertTrue(expected_output_conv_len_curve_fit_parameters, expected_result_conv_len)
        self.assertTrue(expected_output_resp_time_curve_fit_parameters, expected_result_resp_time)
        self.assertTrue(expected_output_conv_ref_time_curve_fit_parameters, expected_result_conv_ref)

    @patch("matplotlib.pyplot.savefig", autospec=True)
    def test_conversation_characteristics_cutoff_5(self,mock_savefig):
        cutoff = 5
        expected_result_conv_len = [0.44916983849233633, 1.9156349592761313, 0.0048790728866266418, 4.3411589194639429e-05]
        expected_result_resp_time = [0.28001731891457893, 0.38845839930487419, 0.00020016446653020847, 2.896185549800808e-05]
        expected_result_conv_ref = [0.0019379564807119043, 0.0048940078069499857, 4.2070926227686924e-05, 1.7671895171226243e-07, 90]

        truncated_rt, rt_cutoff_time = channel.response_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, cutoff)
        conv_len, conv_ref_time = channel.conv_len_conv_refr_time(self.log_data_kubuntu_devel, self.nicks, self.nick_same_list, rt_cutoff_time, cutoff)
        expected_output_conv_len_curve_fit_parameters = vis.exponential_curve_fit_and_plot(conv_len, self.current_directory, "conv_len_cutoff" + str(cutoff))
        expected_output_resp_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot(truncated_rt, self.current_directory, "resp_time_cutoff" + str(cutoff))
        expected_output_conv_ref_time_curve_fit_parameters = vis.exponential_curve_fit_and_plot_x_shifted(conv_ref_time, self.current_directory, "conv_ref_time_cutoff" + str(cutoff))
        self.assertTrue(expected_output_conv_len_curve_fit_parameters, expected_result_conv_len)
        self.assertTrue(expected_output_resp_time_curve_fit_parameters, expected_result_resp_time)
        self.assertTrue(expected_output_conv_ref_time_curve_fit_parameters, expected_result_conv_ref)


if __name__ == '__main__':
    unittest.main()