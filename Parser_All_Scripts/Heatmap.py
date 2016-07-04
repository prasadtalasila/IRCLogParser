#This piece of code can be used as a script for generating heatmaps, if we do not want to use plotly that is.
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np
#col=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
#column_labels = col
#row=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46','47','48']
#row_labels = row
data = genfromtxt('/home/dhruvie/Final_HM.csv', delimiter=',')
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

