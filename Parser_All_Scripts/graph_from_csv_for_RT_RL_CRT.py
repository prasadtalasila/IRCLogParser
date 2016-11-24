import matplotlib.pyplot as plt
import csv
import os
import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import mean_squared_error

def generateProbDistFunction(filePath, howManyTopRows):
	import csv
	f = open(filePath, 'rb')
	reader = csv.reader(f)
	# for row in reader:
	#     print row
	topRows = [int(x[1]) for x in list(reader)[:howManyTopRows]]
	total = sum(topRows)
	freq = [x/float(total) for x in topRows]
	return range(0,howManyTopRows), freq

	f.close()

# def generateFitGraphForLogged(filePath, channel_name, startingDate):
#  x_pdf, y_pdf = generateProbDistFunction(filePath, 20)

#  def func(x, a, b, c):
# 	 return a * np.exp(-b * x) + c
#  # print sum(y_pdf)
#  x = np.array(x_pdf)
#  y = np.array(y_pdf)

#  popt, pcov = curve_fit(func, x, y)
#  [a, b, c] = popt
#  mse = mean_squared_error(func(x, *popt), y)
#  print a, b, c, "MSE="+str(mse)
#  # print y
#  # print func(x, *popt)
#  plt.figure()
#  plt.plot(x, y, 'b-', label="Data")
#  plt.plot(x, func(x, *popt), 'r-', label="Fitted Curve")
 
#  axes = plt.gca()
#  axes.set_xlim([0,20])
#  axes.set_ylim([0,1])
#  plt.legend()
#  # plt.show()
#  plt.savefig("/home/rohan/Desktop/Graph/"+filePath.split("/")[-1][:-4]+".png")
#  plt.close()

# print "a * np.exp(-b * x) + c"
# for file in sorted(os.listdir("/home/rohan/Desktop/CL/")):
# 	print "\n",file.split("/")[-1][:-4]
# 	try:
# 		generateFitGraphForLogged("/home/rohan/Desktop/CL/"+file, file.split("_")[0], file.split("_")[1])
# 	except ValueError:
# 		print "[ERROR: Value Error]"





'''IGNORING ZERO'''
def generateFitGraphForLogged(filePath, channel_name, startingDate):
 howManyTopRows = 30
 x_pdf, y_pdf = generateProbDistFunction(filePath, howManyTopRows)

 def func(x, a, b, c):
	 return a * np.exp(-b * x) + c

 first_non_zero_index = -1
 if filter(lambda x: x!=0, y_pdf):
 	first_non_zero_index = y_pdf.index(filter(lambda x: x!=0, y_pdf)[0])

 x = np.array(x_pdf[0: howManyTopRows - first_non_zero_index])
 y = np.array(y_pdf[first_non_zero_index:])

 popt, pcov = curve_fit(func, x, y)
 [a, b, c] = popt
 mse = mean_squared_error(func(x, *popt), y)
 print a, b, c, "x-shift="+str(first_non_zero_index), "MSE="+str(mse)
 plt.figure()
 plt.plot(x, y, 'b-', label="Data")
 plt.plot(x, func(x, *popt), 'r-', label="Fitted Curve")
 
 axes = plt.gca()
 # axes.set_xlim([0 ,20])
 axes.set_ylim([0,1])
 plt.xticks(range(0, 20,5), xrange(first_non_zero_index, howManyTopRows, 5), size='small')
 
 plt.legend()
 # plt.show()
 plt.savefig("/home/rohan/Desktop/Graph/"+filePath.split("/")[-1][:-4]+".png")
 plt.close()

print "a * np.exp(-b * x) + c"
for file in sorted(os.listdir("/home/rohan/Desktop/CRT/")):
	print "\n",file.split("/")[-1][:-4]
	try:
		generateFitGraphForLogged("/home/rohan/Desktop/CRT/"+file, file.split("_")[0], file.split("_")[1])
	except ValueError:
		print "[ERROR: Value Error]"
	except RuntimeError:
		print "No optimal parameter for curve fit"


