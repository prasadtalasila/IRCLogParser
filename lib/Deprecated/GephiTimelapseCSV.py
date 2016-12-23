#This code is useful if one wants to plot the timelapse or the dynamic variations of a graph over a specific time interval using Gephi.
#Our final output would be a Node and an Edge CSV file. We would import these files to Gephi, generate a time frame, and then eventually the required
#timelapse. Whenever an edge would appear between two nodes in the timelapse, it would mean that a message was sent at some time
#shown in the timelapse. The arrow of the edge would tell us about the sender and receiver nodes.
import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import sys
import datetime
import time
import pandas as pd
import csv
import datetime

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
	if(len(inText) > 1 and inText[len(inText)-1]=='\\'):
		inText = inText[:-1]+'CR'
	return inText

def to_graph(l):
	G = nx.Graph()
	for part in l:
		# each sublist is a bunch of nodes
		G.add_nodes_from(part)
		# it also imlies a number of edges:
		G.add_edges_from(to_edges(part))
	return G

def to_edges(l):
	""" 
					treat `l` as a Graph and returns it's edges 
					to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
	"""
	it = iter(l)
	last = next(it)

	for current in it:
		yield last, current
		last = current    

def createGephiTimelapseCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	"""[Deprecated]
	Produces node and edge csv files that contain information relevant for creating a timelapse of user interactions on Gephi. Most importantly, these csv files contain the node/edge appear and disappear times and can easily be imported into Gephi.
	"""
	today1= []
	today2 =[]
	col1 = []
	col2 = []
	col3 = []
	col4 = []
	col_edge1 = []
	col_edge2 = []
	col_edge3 = []
	col_edge4 = []
	col_edge5 = []
	col_edge6 = []

	for i in range(0,365):
		dt1= datetime.datetime.now() - datetime.timedelta(days=3*365 + 105 - i)

		#We are basically trying to append all the 365 dates into today1 and today2. This is dependent on the day you are writing this code. 105 means
		#I was writing the code after 105 days from 1 Jan 2016. For making the Gephi timelapse work, we need to get the times in the dd-mm-yy h:m:s format
		# My advice would be to try Gephi yourself first and then come back to the code.
		today1.append(dt1.strftime('%Y-%m-%d'))
		dt2= datetime.datetime.now() - datetime.timedelta(days=3*365 + 105 - i) 
	
		today2.append(dt2.strftime('%Y-%m-%d'))

	#for xv in range(len(today1)):        #If we want our graphs to simply change on a daily basis then we can append 00:00:01 to appear time. This means that irrespective
	#today1[xv]= today1[xv] + " 00:00:01" #of when an edge appears on a particular day, the edge will appear throughout 00:00:01 to 23:59:59 of that day.
	# But from the log files we know when an edge appears, so we will use that to make out timelapse more meaningful and precise. 
	for xz in range(len(today2)):
		today2[xz]= today2[xz] + " 23:59:59" #However once an edge appears, it only disappears when the day ends i.e. 23:59:59. We can change this as per our wish.

	nick_same_list=[[] for i in range(5000)]

	nicks = [] #list of all the nicknames
	my_sum = 0

	for folderiterator in range(startingMonth, endingMonth+1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name                             #contents stores all the lines of the file kubunutu-devel   
	
			send_time = [] #list of all the times a user sends a message to another user
			nicks_for_the_day = []
			
			print(filePath+ "For Nicks")
		
			#code for getting all the nicknames in a list
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks_for_the_day:                       
						nicks_for_the_day.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks_for_the_day)):
				if nicks_for_the_day[i][1:-1] not in nicks:
					nicks.append(nicks_for_the_day[i][1:-1])     #removed <> from the nicknames
				
			for i in xrange(0,len(nicks)):
				if(len(nicks[i])!=0):
						nicks[i]=correctLastCharCR(nicks[i])

			for j in content:
				if(j[0]=='=' and "changed the topic of" not in j):
					line1=j[j.find("=")+1:j.find(" is")]
					line2=j[j.find("wn as")+1:j.find("\n")]
					line1=line1[3:]
					line2=line2[5:]
					if(len(line1)!=0):
						line1=correctLastCharCR(line1)
						
					if(len(line2)!=0):
						line2=correctLastCharCR(line2)
					if line1 not in nicks:
						nicks.append(line1)
					if line2 not in nicks:
						nicks.append(line2)
			
			#code for forming list of lists for avoiding nickname duplicacy
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					line1=line[line.find("=")+1:line.find(" is")]
					line2=line[line.find("wn as")+1:line.find("\n")]
					line1=line1[3:]
					line2=line2[5:]
					if(len(line1)!=0):
						line1=correctLastCharCR(line1)
						
					if(len(line2)!=0):
						line2=correctLastCharCR(line2)
					for i in range(5000):
						if line1 in nick_same_list[i] or line2 in nick_same_list[i]:
							if line1 in nick_same_list[i] and line2 not in nick_same_list[i]:
								nick_same_list[i].append(line2)
								break
							if line2 in nick_same_list[i] and line1 not in nick_same_list[i]: 
								nick_same_list[i].append(line1)
								break
							if line2 in nick_same_list[i] and line1 in nick_same_list[i]:
								break  
						if not nick_same_list[i]:
							nick_same_list[i].append(line1)
							nick_same_list[i].append(line2)
							break
	#print(x)  
	for ni in nicks:
		for ind in range(5000):
			if ni in nick_same_list[ind]:
				break
			if not nick_same_list[ind]:
				nick_same_list[ind].append(ni)
				break

	#print("*********************x**********************************")
	#print(nick_same_list)

	G = to_graph(nick_same_list)
	L = connected_components(G)

	for i in range(1,len(L)+1):
		L[i-1] = [str(i)]+L[i-1]

	#The explanation for the aforementioned code has already been given in parser-RT.py.

	#Lines 190-233 are for the nodes in Gephi. We make sure that all nodes are always present throughout our timelapse. For this reason the appear
	#and disappear times for all the nodes are 1 Jan 00:00:01 to 1 Feb 00:00:01 (our timelapse is for a month). If we want our nodes to appear or disappear at some other times
	# change their values here itself. Our aim is to store all these tables in a csv file. Gephi imports these node and edge csv 
	#files, parses them and produces the timelapse.
	createvar = -1
	
	for folderiterator in range(startingMonth, endingMonth+1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name                             #contents stores all the lines of the file kubunutu-devel   
			createvar = createvar + 1
			nicks_for_the_day_2 = []
			print(filePath+ "For Nodes")
			
			#code for getting all the nicknames in a list
			for il in content:
				if(il[0] != '=' and "] <" in il and "> " in il):
					m = re.search(r"\<(.*?)\>", il)
					if m.group(0) not in nicks_for_the_day_2:                       
						nicks_for_the_day_2.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list
				
			for nx in nicks_for_the_day_2:
				for dk in range(len(nicks)):
					if (dk<len(L) and nx[1:-1] in L[dk]):
						col1.append(str(L[dk][0]))
						col2.append(str(L[dk][0]))
						#col3.append(today1[createvar])
						#col4.append(today2[createvar])
						col3.append("2013-01-01 00:00:01") #Nodes stay throughout the month. Col3 and Col4 are the appear and disappear times. Hardcode them ;)
						col4.append("2013-02-01 00:00:01")
						break
		
	rows = zip(col1,col2,col3,col4)   	# We store everything in a csv file which we will later import to Gephi. We are Gephi's slaves!
	with open('/home/dhruvie/LOP/nodesgephi_unchained.csv', 'a+') as myfile:
					wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
					for ro in rows:
						wr.writerow(ro)
					
	#The below code similarly is for obtaining the edge csv file which we is imported to gephi later. The difference here
	#is that we know when the edges appear. We obtain this from the log file(line[1:6]), we just append :00 to satisfy the hh:mm:ss format, Gephi wants.

	createvar_used=-1 
	
	for folderiterator in range(startingMonth, endingMonth+1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name                             #contents stores all the lines of the file kubunutu-devel   
			createvar_used=createvar_used+1    
			print(filePath+ "For Edges")
			nickplots = [] #nickplots stores all those nicks from nicks[] list that do not have zero in and outdegree in our conversation graph
			indegree = [] #this list stores all the indegree corresponding to a particular nick
			outdegree = [] #this list stores all the outdegree corresponding to a particular nick
		
	#  G1 = nx.MultiDiGraph()  
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var=correctLastCharCR(var)
					for d in range(len(nicks)):
						if (d<len(L) and var in L[d]):
							nick_sender = L[d][0]
							break
						
					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')]
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]:
							break
						for ik in xrange(0,len(rec_list)):
							if(rec_list[ik]):
								rec_list[ik]=correctLastCharCR(rec_list[ik])
						for z in rec_list:
							if(z==i):
								send_time.append(line[1:6])
								if(var != i): 	
									for d in range(len(nicks)):
										if i in L[d]:
											nick_receiver=L[d][0]
											break
									col_edge1.append(nick_sender)
									col_edge2.append(nick_receiver)			#We are going to add all these columns in a csv file for Gephi's use.
									col_edge3.append("Directed")
									col_edge4.append(1.0)
									col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
									col_edge6.append(today2[createvar_used])
									my_sum=my_sum+1

		#       G1.add_edge(nick_sender,nick_receiver,weight=line[1:6])
									if nick_sender not in nickplots:
										nickplots.append(nick_sender)	 
									if nick_receiver not in nickplots:	#Right time to append to nickplots.
										nickplots.append(nick_receiver) 
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for ij in xrange(0,len(rec_list_2)):
								if(rec_list_2[ij]):
									rec_list_2[ij]=correctLastCharCR(rec_list_2[ij])
							for j in rec_list_2:
								if(j==i):
									send_time.append(line[1:6])
									if(var != i): 	
										for d in range(len(nicks)):
											if i in L[d]:
												nick_receiver=L[d][0]
												break
										col_edge1.append(nick_sender)
										col_edge2.append(nick_receiver)
										col_edge3.append("Directed")
										col_edge4.append(1.0)
										col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
										col_edge6.append(today2[createvar_used])           	  
										my_sum=my_sum+1
									# G1.add_edge(nick_sender,nick_receiver,weight=line[1:6])	 
										if nick_sender not in nickplots:
											nickplots.append(nick_sender)   
										if nick_receiver not in nickplots:
											nickplots.append(nick_receiver) 

						if(flag_comma == 0):
							rec=line[line.find(">")+1:line.find(", ")] 
							rec=rec[1:]
							rec=correctLastCharCR(rec)
							if(rec==i):
								send_time.append(line[1:6])
								if(var != i):
									for d in range(len(nicks)):
										if i in L[d]:
											nick_receiver=L[d][0]
											break
									col_edge1.append(nick_sender)
									col_edge2.append(nick_receiver)
									col_edge3.append("Directed")
									col_edge4.append(1.0)
									col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
									col_edge6.append(today2[createvar_used]) 
									my_sum=my_sum+1
								# G1.add_edge(nick_sender,nick_receiver,weight=line[1:6])	 
									if nick_sender not in nickplots:
										nickplots.append(nick_sender)   
									if nick_receiver not in nickplots:
										nickplots.append(nick_receiver) 
						
	edge_rows = zip(col_edge1,col_edge2,col_edge3,col_edge4,col_edge5,col_edge6)   
	with open('/home/dhruvie/LOP/edgesgephi_unchained.csv', 'a+') as myfile:
					wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
					for rz in edge_rows:
						wr.writerow(rz)  

			#The below code is for plotting the indegree and outdegree versus time. The code is self-explanatory. Pandas library is utilized.
'''
		for u,v,d in G1.edges(data=True):
						d['label'] = d.get('weight','')

		for ui in nickplots:
			indegree.append(G1.in_degree(ui))
			outdegree.append(G1.out_degree(ui))

#if indegree and outdegree list is not zero then plot the bar graphs using pandas library as shown below
		if(len(indegree)!=0 and len(outdegree)!=0):
			data = {'Nick': nickplots, #x axis
									'Indegree': indegree} #y axis
			df = pd.DataFrame(data, columns = ['Nick', 'Indegree'])
			df.index = df['Nick']
			del df['Nick']
			df  #these 3 lines remove the first column that has serial number
		# print(df)
			axes = plt.gca()
			axes.set_ylim([0,200])
			df.plot(kind='bar', ax=axes)
			name1 = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_indegree.png"
			plt.savefig(name1)
			plt.close()

		#same thing for outdegree
			data = {'Nick': nickplots, 
									'Indegree': outdegree}
			df = pd.DataFrame(data, columns = ['Nick', 'Indegree'])
			df.index = df['Nick']
			del df['Nick']
			df
	#  print(df)
			axes = plt.gca()
			axes.set_ylim([0,200])
			df.plot(kind='bar', ax=axes)
			name2 = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_outdegree.png"
			plt.savefig(name2)
			plt.close()
'''
'''  A = nx.to_agraph(G1)
		A.layout(prog='dot')
		A.draw(n_brilli)
'''