import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def generateProbDistFunction(filePath, howManyTopRows):
	import csv
	f = open(filePath, 'rb')
	reader = csv.reader(f)
	topRows = [int(x[1]) for x in list(reader)[:howManyTopRows]]
	total = sum(topRows)
	freq = [x/float(total) for x in topRows]
	return range(0,howManyTopRows), freq

	f.close()

def generateFitGraphForLogged():
 x_pdf, y_pdf = generateProbDistFunction("/home/rohan/Desktop/#kubuntu-devel_CRT.csv", 20)

 def func(x, a, b, c):
	 return a * np.exp(-b * x) + c
 
 x = np.array(x_pdf[0:10])
 y = np.array(y_pdf[10:20])

 popt, pcov = curve_fit(func, x, y)
 [a, b, c] = popt
 print a, b, c
 plt.figure()
 plt.plot(x, y, 'b-', label="Data")
 plt.plot(x, func(x, *popt), 'r-', label="Fitted Curve")
 
 axes = plt.gca()
 axes.set_xlim([0,20])
 axes.set_ylim([0,1])
 
 plt.legend()
 plt.show()
 # plt.savefig(output_dir_degree+"/"+channel_name+"_"+typeOfDegree+"_graph_"+str(startingDate)+"-"+str(startingMonth)+"_"+str(endingDate)+"-"+str(endingMonth)+".png")
 plt.close()

generateFitGraphForLogged()