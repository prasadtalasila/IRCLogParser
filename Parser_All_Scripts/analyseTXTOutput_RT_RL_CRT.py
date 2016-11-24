'''
Monthly RT/CL
'''

# import numpy as np
# with open("/home/rohan/Desktop/Weekly/CL_Values.txt") as myTXT:
# 	file_lines = []
# 	for line in myTXT:
# 		if len(line.strip())>1:
# 			file_lines.append(line.strip())
# 			# print line.strip()


# # print len(file_lines)
# print "[CL] [Monthly2013] [ALL_CHANNELS] [a * np.exp(-b * x) + c]\n"

# i = 0
# while i < len(file_lines):
# 	j = 0
# 	list_a = []
# 	list_b = []
# 	list_c = []

# 	while j < 24:
# 		header = file_lines[i+j]
# 		values = file_lines[i+j+1]

# 		channel, date = header.split(" ")
# 		a, b, c = values.split(" ")

# 		try:
# 			list_a.append(float(a))
# 			list_b.append(float(b))
# 			list_c.append(float(c))
# 		except ValueError:
# 			pass

# 		# print header
# 		# print values
# 		j+=2
# 	# print len(list_a), len(list_b), len(list_c)
# 	# print list_a, list_b, list_c
# 	print channel
# 	print "==========================="
# 	print "Var", "Minimum", "Maximum", "Average"
# 	print "==========================="
# 	print " A ", "{0:.5f}".format(min(list_a)), "{0:.5f}".format(max(list_a)), "{0:.5f}".format(np.average(list_a))
# 	print " B ", "{0:.5f}".format(min(list_b)), "{0:.5f}".format(max(list_b)), "{0:.5f}".format(np.average(list_b))
# 	print " C ", "{0:.5f}".format(min(list_c)), "{0:.5f}".format(max(list_c)), "{0:.5f}".format(np.average(list_c))
# 	print "\n"

# 	i+=24

'''
Monthly CRT
'''
# import numpy as np
# with open("/home/rohan/Desktop/Weekly/CRT.txt") as myTXT:
# 	file_lines = []
# 	for line in myTXT:
# 		if len(line.strip())>1:
# 			file_lines.append(line.strip())


# # print len(file_lines)
# print "[CRT] [Monthly2013] [ALL_CHANNELS] [a * np.exp(-b * x) + c]\n"
# list_a = []
# list_b = []
# list_c = []
# list_shift=[]
# i = 0
# while i < len(file_lines):
# 	j = 0


# 	while j<24:
# 		header = file_lines[i]
# 		values = file_lines[i+j+1]

# 		channel, date = header.split(" ")
# 		# print values.split(" ")

# 		try:
# 			a, b, c, shift = values.split(" ")
# 			list_a.append(float(a))
# 			list_b.append(float(b))
# 			list_c.append(float(c))
# 			list_shift.append(float(shift.split("=")[1]))
# 		except ValueError:
# 			pass
		
# 		j+=2
# 	# print len(list_a), len(list_b), len(list_c), len(list_shift)
# 	# print list_a, list_b, list_c

# 	i+=24
# print channel
# print "==========================="
# print "Var", "Minimum", "Maximum", "Average"
# print "==========================="
# print "  A  ", "{0:.5f}".format(min(list_a)), "{0:.5f}".format(max(list_a)), "{0:.5f}".format(np.average(list_a))
# print "  B  ", "{0:.5f}".format(min(list_b)), "{0:.5f}".format(max(list_b)), "{0:.5f}".format(np.average(list_b))
# print "  C  ", "{0:.5f}".format(min(list_c)), "{0:.5f}".format(max(list_c)), "{0:.5f}".format(np.average(list_c))
# print "shift", "{0:.4f}".format(min(list_shift)), "{0:.4f}".format(max(list_shift)), "{0:.4f}".format(np.average(list_shift))
# print "\n"

'''
Monthly Node
'''


# import numpy as np
# with open("/home/rohan/Desktop/Weekly/degreeNode.txt") as myTXT:
# 	file_lines = []
# 	for line in myTXT:
# 		if len(line.strip())>1:
# 			file_lines.append(line.strip())


# # print len(file_lines)
# print "[Node] [Monthly2013] [ALL_CHANNELS] [a + bx]"
# i = 0
# while i < len(file_lines):
# 	j= 0
# 	list_aI = []
# 	list_bI = []

# 	list_aO = []
# 	list_bO = []
# 	while j<36:

# 		header = file_lines[i+j]
# 		channel = header.split(" ")[0]
# 		IN = file_lines[i+j+1]
# 		OUT = file_lines[i+j+2]

# 		temp, temp2, aI, bI = IN.split(" ")
# 		temp, aO, bO = OUT.split(" ")

# 		# try:
# 		list_aI.append(float(aI))
# 		list_bI.append(float(bI))

# 		list_aO.append(float(aO))
# 		list_bO.append(float(bO))
# 		j+=3

# 	# except ValueError:
# 		# pass


# 		# print header
# 	# print values
# 	# print len(list_aO), len(list_aI)
# 	# # print list_a, list_b, list_c
# 	print channel
# 	print "===================================="
# 	print "Type ", "Var", "Minimum", "Maximum", "Average"
# 	print "===================================="
# 	print " IN  ", " A ", "{0:.4f}".format(min(list_aI)), "{0:.4f}".format(max(list_aI)), "{0:.4f}".format(np.average(list_aI))
# 	print " IN  ", " B ", "{0:.5f}".format(min(list_bI)), "{0:.5f}".format(max(list_bI)), "{0:.5f}".format(np.average(list_bI))

# 	print " OUT ", " A ", "{0:.4f}".format(min(list_aO)), "{0:.4f}".format(max(list_aO)), "{0:.4f}".format(np.average(list_aO))
# 	print " OUT ", " B ", "{0:.5f}".format(min(list_bO)), "{0:.5f}".format(max(list_bO)), "{0:.5f}".format(np.average(list_bO))
# 	print "\n"
# 	i+=36





'''
CL/RT Weekly
'''

import numpy as np
with open("/home/rohan/Desktop/CL[2months].txt") as myTXT:
	file_lines = []
	for line in myTXT:
		if len(line.strip())>1:
			file_lines.append(line.strip())


print len(file_lines)
list_a = []
list_b = []
list_c = []
i = 0
while i < len(file_lines):
	header = file_lines[i]
	values = file_lines[i+1]

	channel, startDate, endDate, typeOfCal = header.split("_")
	a, b, c = values.split(" ")

	try:
		list_a.append(float(a))
		list_b.append(float(b))
		list_c.append(float(c))
	except ValueError:
		pass


	# print header
	# print values
	i+=2

print len(list_a), len(list_b), len(list_c)
# print list_a, list_b, list_c
print "Var", "Minimum", "Maximum", "Average"
print " A ", "{0:.5f}".format(min(list_a)), "{0:.5f}".format(max(list_a)), "{0:.5f}".format(np.average(list_a))
print " B ", "{0:.5f}".format(min(list_b)), "{0:.5f}".format(max(list_b)), "{0:.5f}".format(np.average(list_b))
print " C ", "{0:.5f}".format(min(list_c)), "{0:.5f}".format(max(list_c)), "{0:.5f}".format(np.average(list_c))


'''
CRT Weekly
'''

# import numpy as np
# with open("/home/rohan/Desktop/CRT[2months].txt") as myTXT:
# 	file_lines = []
# 	for line in myTXT:
# 		if len(line.strip())>1:
# 			file_lines.append(line.strip())


# print len(file_lines)
# list_a = []
# list_b = []
# list_c = []
# list_shift=[]
# i = 0
# while i < len(file_lines):
# 	header = file_lines[i]
# 	values = file_lines[i+1]

# 	channel, startDate, endDate, typeOfCal = header.split("_")
# 	# print values.split(" ")

# 	try:
# 		a, b, c, shift = values.split(" ")
# 		list_a.append(float(a))
# 		list_b.append(float(b))
# 		list_c.append(float(c))
# 		list_shift.append(float(shift.split("=")[1]))
# 	except ValueError:
# 		pass


# 	# print header
# 	# print values
# 	i+=2

# print len(list_a), len(list_b), len(list_c), len(list_shift)
# # print list_a, list_b, list_c
# print " Var ", "Minimum", "Maximum", "Average"
# print "  A  ", "{0:.5f}".format(min(list_a)), "{0:.5f}".format(max(list_a)), "{0:.5f}".format(np.average(list_a))
# print "  B  ", "{0:.5f}".format(min(list_b)), "{0:.5f}".format(max(list_b)), "{0:.5f}".format(np.average(list_b))
# print "  C  ", "{0:.5f}".format(min(list_c)), "{0:.5f}".format(max(list_c)), "{0:.5f}".format(np.average(list_c))
# print "shift", "{0:.4f}".format(min(list_shift)), "{0:.4f}".format(max(list_shift)), "{0:.4f}".format(np.average(list_shift))

'''
Degree[weekly]
'''

# import numpy as np
# with open("/home/rohan/Desktop/degreeNode2Months.txt") as myTXT:
# 	file_lines = []
# 	for line in myTXT:
# 		if len(line.strip())>1:
# 			file_lines.append(line.strip())


# print len(file_lines)
# list_aT = []
# list_bT = []

# list_aI = []
# list_bI = []

# list_aO = []
# list_bO = []
# i = 0
# while i < len(file_lines):
# 	header = file_lines[i]
# 	TOTAL = file_lines[i+1]
# 	IN = file_lines[i+2]
# 	OUT = file_lines[i+3]

# 	temp, aT, bT = TOTAL.split(" ")
# 	temp, aI, bI = IN.split(" ")
# 	temp, aO, bO = OUT.split(" ")

# 	# try:
# 	list_aT.append(float(aT))
# 	list_bT.append(float(bT))

# 	list_aI.append(float(aI))
# 	list_bI.append(float(bI))

# 	list_aO.append(float(aO))
# 	list_bO.append(float(bO))

# 	# except ValueError:
# 		# pass


# 	# print header
# 	# print values
# 	i+=4

# print len(list_aT), len(list_aO), len(list_aI)
# # # print list_a, list_b, list_c
# print "Type ", "Var", "Minimum", "Maximum", "Average"
# print "TOTAL", " A ", "{0:.5f}".format(min(list_aT)), "{0:.5f}".format(max(list_aT)), "{0:.5f}".format(np.average(list_aT))
# print "TOTAL", " B ", "{0:.4f}".format(min(list_bT)), "{0:.4f}".format(max(list_bT)), "{0:.4f}".format(np.average(list_bT))

# print " IN  ", " A ", "{0:.5f}".format(min(list_aI)), "{0:.5f}".format(max(list_aI)), "{0:.5f}".format(np.average(list_aI))
# print " IN  ", " B ", "{0:.4f}".format(min(list_bI)), "{0:.4f}".format(max(list_bI)), "{0:.4f}".format(np.average(list_bI))

# print " OUT ", " A ", "{0:.5f}".format(min(list_aO)), "{0:.5f}".format(max(list_aO)), "{0:.5f}".format(np.average(list_aO))
# print " OUT ", " B ", "{0:.4f}".format(min(list_bO)), "{0:.4f}".format(max(list_bO)), "{0:.4f}".format(np.average(list_bO))

