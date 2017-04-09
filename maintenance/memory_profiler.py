import glob
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt

file_name = glob.glob('../test/*.dat')[0]
with open(file_name) as f:
    data = f.readlines()
f.close()

x = []
y = []
x_start = float(data[1:][0].split()[2])

for line in data[1:]:
    x.append(float(line.split()[2]) - x_start)
    y.append(float(line.split()[1]))

plt.plot(x, y)
plt.savefig('../maintenance/memory_consumption.png')