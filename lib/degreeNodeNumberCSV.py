import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import csv
import math
import numpy as np
from numpy.random import normal
from scipy.optimize import curve_fit
from scipy import stats
from sklearn.metrics import mean_squared_error
import ext.util

def degreeNodeNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	nodes_with_OUT_degree_per_day = []
	nodes_with_IN_degree_per_day = []
	nodes_with_TOTAL_degree_per_day = []

	max_degree_possible = 1000

	# output_dir_degree = output_directory+"degreeNode/"
	output_dir_degree = output_directory
	output_dir_degree_img = output_dir_degree + "individual-images/"
	output_file_out_degree = output_dir_degree + channel_name+"_out_degree"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".csv"
	output_file_in_degree = output_dir_degree + channel_name+"_in_degree"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".csv"
	output_file_total_degree = output_dir_degree + channel_name+"_total_degree"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".csv"

	# print "Creating a new output folder"
	# os.system("rm -rf "+output_dir_degree)
	# os.system("mkdir "+output_dir_degree)

	if not os.path.exists(os.path.dirname(output_dir_degree)):
		try:
			os.makedirs(os.path.dirname(output_dir_degree))
			# os.system("rm -rf "+output_dir_degree_img)
			os.system("mkdir "+output_dir_degree_img)
			# os.system("rm "+output_file_out_degree)
			os.system("touch "+output_file_out_degree)
			# os.system("rm "+output_file_in_degree)
			os.system("touch "+output_file_in_degree)
			# os.system("rm "+output_file_total_degree)
			os.system("touch "+output_file_total_degree)

		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	for folderiterator in range(startingMonth, endingMonth + 1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name
					
			nicks = [] #list of all the nicknames     	
			'''
				Getting all the nicknames in a list nicks[]
			'''
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks:                       
						nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks)):
				nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
					
			for i in xrange(0,len(nicks)):
				nicks[i]=ext.util.correctLastCharCR(nicks[i])

			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					nick1=ext.util.correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
					nick2=ext.util.correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
					if nick1 not in nicks:
						nicks.append(nick1)
					if nick2 not in nicks:
						nicks.append(nick2)
					
			'''
				Forming list of lists for avoiding nickname duplicacy
			'''
			nick_same_list=[[] for i in range(len(nicks))] #list of list with each list having all the nicks for that particular person
			
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					line1=line[line.find("=")+1:line.find(" is")][3:]
					line2=line[line.find("wn as")+1:line.find("\n")][5:]
					line1=ext.util.correctLastCharCR(line1)
					line2=ext.util.correctLastCharCR(line2)
					for i in range(5000):
						if line1 in nick_same_list[i] or line2 in nick_same_list[i]:
							nick_same_list[i].append(line1)
							nick_same_list[i].append(line2)
							break
						if not nick_same_list[i]:
							nick_same_list[i].append(line1)
							nick_same_list[i].append(line2)
							break

			'''
				Making relation map between client
			'''
			conversations=[[] for i in range(100)] #format of each list [num_messages,sender_nick,receiver_nick]
			for i in xrange(0,100):
				conversations[i].append(0)
			
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var = ext.util.correctLastCharCR(var) 
					for d in range(len(nicks)):
						if var in nick_same_list[d]:
							nick_sender = nick_same_list[d][0]
							break
						else:
							nick_sender=var
							
					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')]
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]:
							break
						for x in xrange(0,len(rec_list)):
							if(rec_list[x]):
								rec_list[x] = ext.util.correctLastCharCR(rec_list[x])
						for z in rec_list:
							if(z==i):
								if(var != i):  
									for d in range(len(nicks)):
										if i in nick_same_list[d]:
											nick_receiver=nick_same_list[d][0]
											break
										else:
											nick_receiver=i
											
									for k in xrange(0,100):
										if (nick_sender in conversations[k] and nick_receiver in conversations[k]):
											if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
												conversations[k][0]=conversations[k][0]+1
												break
										if(len(conversations[k])==1):
											conversations[k].append(nick_sender)
											conversations[k].append(nick_receiver)
											conversations[k][0]=conversations[k][0]+1
											break
								
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for y in xrange(0,len(rec_list_2)):
								if(rec_list_2[y]):
									rec_list_2[y] = ext.util.correctLastCharCR(rec_list_2[y])
							for j in rec_list_2:
								if(j==i):
									if(var != i):   
										for d in range(len(nicks)):
											if i in nick_same_list[d]:
												nick_receiver=nick_same_list[d][0]
												break
											else:
												nick_receiver=i
											
										for k in xrange(0,100):
											if (nick_sender in conversations[k] and nick_receiver in conversations[k]):
												if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
													conversations[k][0]=conversations[k][0]+1
													break
											if(len(conversations[k])==1):
												conversations[k].append(nick_sender)
												conversations[k].append(nick_receiver)
												conversations[k][0]=conversations[k][0]+1
												break

						if(flag_comma == 0):
							rec=line[line.find(">")+1:line.find(", ")][1:]
							rec = ext.util.correctLastCharCR(rec)
							if(rec==i):
								if(var != i):
									for d in range(len(nicks)):
										if i in nick_same_list[d]:
											nick_receiver=nick_same_list[d][0]
											break
										else:
											nick_receiver=i
										
									for k in xrange(0,100):
										if (nick_sender in conversations[k] and nick_receiver in conversations[k]):  
											if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
												conversations[k][0]=conversations[k][0]+1
												break
										if(len(conversations[k])==1):
											conversations[k].append(nick_sender)
											conversations[k].append(nick_receiver)
											conversations[k][0]=conversations[k][0]+1
											break
		
			msg_num_graph = nx.DiGraph()  #graph with multiple directed edges between clients used 

			for y in xrange(0,100):
				if(len(conversations[y])==3):
					msg_num_graph.add_edge(conversations[y][1],conversations[y][2],weight=conversations[y][0])   

			for u,v,d in msg_num_graph.edges(data=True):
							d['label'] = d.get('weight','')
			# output_file=out_dir_msg_num+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_msg_num.png"
			# print "Generated " + output_file
			# A = nx.drawing.nx_agraph.to_agraph(msg_num_graph)
			# A.layout(prog='dot')
			# A.draw(output_file)

			nodes_with_OUT_degree = [0]*max_degree_possible
			nodes_with_IN_degree = [0]*max_degree_possible
			nodes_with_TOTAL_degree = [0]*max_degree_possible

			# print msg_num_graph.out_degree(), msg_num_graph.in_degree(), msg_num_graph.degree()
			# print msg_num_graph.out_degree().values()
			# print msg_num_graph.in_degree().values()
			# print msg_num_graph.degree().values()

			for degree in msg_num_graph.out_degree().values():
				nodes_with_OUT_degree[degree]+=1

			for degree in msg_num_graph.in_degree().values():
				nodes_with_IN_degree[degree]+=1

			for degree in msg_num_graph.degree().values():
				nodes_with_TOTAL_degree[degree]+=1
			

			x_axis_log = [math.log(i) for i in xrange(1, 20)]#ignore degree 0
			y_axis_log = [math.log(i) if i>0 else 0 for i in nodes_with_TOTAL_degree[1:20] ]#ignore degree 0
			#plot1
			plt.plot(x_axis_log, y_axis_log) 
			#plot2
			plt.plot([1,2], [1,2])
			plt.xlabel("log(degree)")
			plt.ylabel("log(no_of_nodes)")

			plt.xticks(x_axis_log, ['log'+str(i) for i in xrange(1, len(x_axis_log))])
			plt.yticks(x_axis_log, ['log'+str(i) for i in xrange(1, len(x_axis_log))])

			plt.legend(['Required', 'y = x'], loc='upper left')

			# Save it in png and svg formats
			plt.savefig(output_dir_degree_img+"/total_out_degree"+str(folderiterator)+"-"+str(fileiterator)+".png")
			plt.close()

			# print "\n"
			nodes_with_OUT_degree.insert(0, sum(nodes_with_OUT_degree))
			nodes_with_OUT_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
			nodes_with_OUT_degree_per_day.append(nodes_with_OUT_degree)

			nodes_with_IN_degree.insert(0, sum(nodes_with_IN_degree))
			nodes_with_IN_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
			nodes_with_IN_degree_per_day.append(nodes_with_IN_degree)

			nodes_with_TOTAL_degree.insert(0, sum(nodes_with_TOTAL_degree))
			nodes_with_TOTAL_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
			nodes_with_TOTAL_degree_per_day.append(nodes_with_TOTAL_degree)

	# print nodes_with_OUT_degree_per_day
	# print nodes_with_IN_degree_per_day
	# print nodes_with_TOTAL_degree_per_day
	
	temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
	temp.insert(0, 'total')
	temp.insert(0, 'out-degree/day>')

	nodes_with_OUT_degree_per_day.insert(0, temp)
	column_wise_OUT = zip(*nodes_with_OUT_degree_per_day)
	with open(output_file_out_degree, 'wb') as myfile:
		wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
		for col in column_wise_OUT:
			wr.writerow(col)

	temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
	temp.insert(0, 'total')
	temp.insert(0, 'in-degree/day>')

	nodes_with_IN_degree_per_day.insert(0, temp)
	column_wise_IN = zip(*nodes_with_IN_degree_per_day)
	with open(output_file_in_degree, 'wb') as myfile2:
		wr = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
		for col in column_wise_IN:
			wr.writerow(col)

	temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
	temp.insert(0, 'total')
	temp.insert(0, 'degree/day>')

	nodes_with_TOTAL_degree_per_day.insert(0, temp)
	column_wise_TOTAL = zip(*nodes_with_TOTAL_degree_per_day)
	with open(output_file_total_degree, 'wb') as myfile3:
		wr = csv.writer(myfile3, quoting=csv.QUOTE_ALL)
		for col in column_wise_TOTAL:
			wr.writerow(col)

	# generateFitGraphOverTime("TOTAL", 10, column_wise_TOTAL, channel_name, startingDate, startingMonth, endingDate, endingMonth, output_dir_degree)
	generateFitGraphOverTime("OUT", 9, column_wise_OUT, channel_name, startingDate, startingMonth, endingDate, endingMonth, output_dir_degree)
	generateFitGraphOverTime("IN", 9, column_wise_IN, channel_name, startingDate, startingMonth, endingDate, endingMonth, output_dir_degree)


'''-------------------------------helper function to gen graph-------------------'''
def generateFitGraphOverTime(typeOfDegree, filter_val, column_wise, channel_name, startingDate, startingMonth, endingDate, endingMonth, output_dir_degree):
	sum_each_row = []
	for row in column_wise[3:]: #ignore degree 0 and text, starting from degree 1
		sum_each_row.append(sum(row[1:]))

	# print sum_each_row
	x_axis_log = [math.log(i) for i in xrange(1, filter_val)]#ignore degree 0
	y_axis_log = [math.log(i) if i>0 else 0 for i in sum_each_row[1:filter_val] ]#ignore degree 0

	# get x and y vectors
	x = np.array(x_axis_log)
	y = np.array(y_axis_log)
	
	'''WAY TWO OF REGRESSION'''
	slope, intercept, r_value, p_value, std_err = stats.linregress(x_axis_log,y_axis_log)
	line = [slope*xi+intercept for xi in x_axis_log]

	print str(typeOfDegree)+"\t"+str(slope)+"\t"+str(intercept)+"\t"+str(r_value**2)+"\t"+str(mean_squared_error(y, line))
	# import plotly.plotly as py
	# py.sign_in('rohangoel963', 'vh6le8no26')
	# import plotly.graph_objs as go

	# trace1 = go.Scatter(
	#                   x=x, 
	#                   y=y, 
	#                   mode='lines',
	#                   marker=go.Marker(color='rgb(255, 127, 14)'),
	#                   name='Data'
	#                   )

	# trace2 = go.Scatter(
	#                   x=x, 
	#                   y=line, 
	#                   mode='lines',
	#                   marker=go.Marker(color='rgb(31, 119, 180)'),
	#                   name='Fit'
	#                   )

	# layout = go.Layout(
	#                 title='DegreeNode',
	#                 # plot_bgcolor='rgb(229, 229, 229)',
	#                   xaxis=go.XAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)'),
	#                   # yaxis=go.YAxis(zerolinecolor='rgb(255,255,255)', gridcolor='rgb(255,255,255)')
	#                 )

	# data = [trace1, trace2]
	# fig = go.Figure(data=data, layout=layout)

	# py.image.save_as(fig, typeOfDegree+"temp.png")

	'''END'''

	#graph config
	axes = plt.gca()
	axes.set_xlim([0,3])
	axes.set_ylim([0,6])
	plt.xlabel("log(degree)")
	plt.ylabel("log(no_of_nodes)")

	# fit with np.polyfit
	m, b = np.polyfit(x, y, 1)

	plt.plot(x, y, '-')
	plt.plot(x, m*x + b, '-')
	plt.legend(['Data', 'Fit'], loc='upper right')
	plt.savefig(output_dir_degree+"/"+channel_name+"_"+typeOfDegree+"_graph_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".png")
	plt.close()

	# print typeOfDegree, b, m

	# # Save it in png and svg formats
	# plt.savefig(output_dir_degree+"/"+channel_name+"_"+typeOfDegree+"_graph_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".png")
	# plt.close()

	# print output_dir_degree +"/"+channel_name+"_"+typeOfDegree+"_graph_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+".png"