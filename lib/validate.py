import csv
import sys
sys.path.append('../lib')
from auxiliary.viz import fit_graph_from_csv_for_RT_RL_CRT as fit

def validate_RT_RL(file, range_a, range_b, range_c, range_mse):
	a, b, c, mse = fit.generateFitGraphForLogged(file, "/tmp/")

	if not range_a[0] <= a <= range_a[1]:
		print "[Unexpected Value] a | " + file		

	if not range_b[0] <= b <= range_b[1]:
		print "[Unexpected Value] b | " + file

	if not range_c[0] <= c <= range_c[1]:
		print "[Unexpected Value] c | " + file

	if not range_mse[0] <= mse <= range_mse[1]:
		print "[Unexpected Value] mse | " + file 

def validate_CRT(file, range_a, range_b, range_c, expected_first_non_zero_index, range_mse):
	a, b, c, first_non_zero_index, mse = fit.generateFitGraphForLogged_CRT(file, "/tmp/")

	if not range_a[0] <= a <= range_a[1]:
		print "[Unexpected Value] a | " + file		

	if not range_b[0] <= b <= range_b[1]:
		print "[Unexpected Value] b | " + file

	if not range_c[0] <= c <= range_c[1]:
		print "[Unexpected Value] c | " + file

	if not first_non_zero_index[0] <= expected_first_non_zero_index <= first_non_zero_index[1]:
		print "[Unexpected Value] first_non_zero_index | " + file 

	if not range_mse[0] <= mse <= range_mse[1]:
		print "[Unexpected Value] mse | " + file 