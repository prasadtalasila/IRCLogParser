import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np

def matplotlob_csv_heatmap_generator(csv_file):
	#This piece of code can be used as a script for generating heatmaps, if we do not want to use plotly that is.
	
	column_labels = map(str,range(1,32))
	row_labels = map(str,range(1,49))
	
	data = genfromtxt(csv_file, delimiter=',')
	print(data)
	
	fig, ax = plt.subplots(figsize=(10,10))
	heatmap = ax.pcolor(data, cmap=plt.cm.Reds)

	cbar = plt.colorbar(heatmap)

	# put the major ticks at the middle of each cell
	#ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	#ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

	# want a more natural, table-like display
	ax.invert_yaxis()
	ax.xaxis.tick_top()

	#ax.set_xticklabels(row_labels, minor=False)
	#ax.set_yticklabels(column_labels, minor=False)
	plt.show()

