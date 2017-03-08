import csv

def freq_analysis_CU(CU_matrix_location):
	# CU_matrix_location = "/home/rohan/Desktop/CU/"
	freq_anal_matrix = [0 for i in range(31)]


	for j in range(1,13):
		filePath = CU_matrix_location+str(j)+"_"+str(j)+"reduced_CU_adjacency_matrix.csv"

		with open(filePath, 'rU') as p:
		    #reads csv into a list of lists
		    csv_list = list(list(rec) for rec in csv.reader(p, delimiter=',')) 

		csv_list_of_list = [[int(float(item)) for item in row] for row in csv_list]

		for row in csv_list_of_list:
			for i in xrange(31):
				freq_anal_matrix[i] += row.count(i)

	print "Analysis on monthly basis for kubuntu-devel for the year 2013\n\
		   For each month we have 30x100 (channel x user matrix), and each entry denotes\
		   The number of days a particular user has been on the channel (for that month)"

	print "FREQ ANAL = ", freq_anal_matrix
	print "TOTAL ENTRIES ANAL =", sum(freq_anal_matrix)
	print "Tabular Format"

	for i in xrange(31):
		print str(i)+"\t"+str(freq_anal_matrix[i])

