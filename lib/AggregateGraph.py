import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import sys
import ext.util


def createAggregateGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	""" Creates a directed graph for a longer time frames 
		with each node representing an IRC user
		and each directed edge has a weight which 
		mentions the number messages sent and recieved by that user 
		in the selected time frame.

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        channel_name (str): Channel to be perform analysis on
        output_directory (str): Location of output directory
        startingDate (int): Date to start the analysis (in conjunction with startingMonth)
        startingMonth (int): Date to start the analysis (in conjunction with startingDate)
        endingDate (int): Date to end the analysis (in conjunction with endingMonth)
        endingMonth (int): Date to end the analysis (in conjunction with endingDate)

    Returns:
       null 

    """
	MAX_EXPECTED_DIFF_NICKS = 5000

	nick_same_list=[[] for i in range(MAX_EXPECTED_DIFF_NICKS)]  

	conversations=[[] for i in range(MAX_EXPECTED_DIFF_NICKS)]   
	for i in xrange(0,MAX_EXPECTED_DIFF_NICKS):
		conversations[i].append(0)

	nicks = [] #list of all the nicknames
	aggregate_graph = nx.DiGraph()  #graph with multiple directed edges between clients used 

	if not os.path.exists(os.path.dirname(output_directory)):
		try:
			os.makedirs(os.path.dirname(output_directory))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise
				
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
		
			nicks_for_the_day = []
			print "Working on " + filePath 
			
			'''Getting all the nicknames in a list'''
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks_for_the_day:                       
						nicks_for_the_day.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks_for_the_day)):
				if nicks_for_the_day[i][1:-1] not in nicks:
					nicks.append(nicks_for_the_day[i][1:-1])     #removed <> from the nicknames
					
			for i in xrange(0,len(nicks)):
				nicks[i] = ext.util.correctLastCharCR(nicks[i])
			
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					nick1=line[line.find("=")+1:line.find(" is")]
					nick2=line[line.find("wn as")+1:line.find("\n")]
					nick1=nick1[3:]
					nick2=nick2[5:]
					nick1=ext.util.correctLastCharCR(nick1)
					nick2=ext.util.correctLastCharCR(nick2)
					if nick1 not in nicks:
						nicks.append(nick1)
					if nick2 not in nicks:
						nicks.append(nick2)
				
			
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					line1=line[line.find("=")+1:line.find(" is")]
					line2=line[line.find("wn as")+1:line.find("\n")]
					line1=line1[3:]
					line2=line2[5:]
					line1=ext.util.correctLastCharCR(line1)
					line2=ext.util.correctLastCharCR(line2)
					for i in range(MAX_EXPECTED_DIFF_NICKS):
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

	for ni in nicks:
		for ind in range(MAX_EXPECTED_DIFF_NICKS):
			if ni in nick_same_list[ind]:
				break
			if not nick_same_list[ind]:
				nick_same_list[ind].append(ni)
				break

	G = ext.util.to_graph(nick_same_list)
	L = list(connected_components(G))

	for i in range(1,len(L)+1):
		L[i-1] = list(L[i-1])

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

			print(filePath)
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m=re.search(r"\<(.*?)\>", line)
					var=m.group(0)[1:-1]
					var=ext.util.correctLastCharCR(var)
					for d in range(MAX_EXPECTED_DIFF_NICKS):
						if ((d < len(L)) and (var in L[d])):  #change nick_same_list to L because L is the main list of all users and nicks now
							nick_sender = L[d][0]
							break
						
					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')]
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]:
							break
						for k in xrange(0,len(rec_list)):
							if(rec_list[k]):
								rec_list[k]=ext.util.correctLastCharCR(rec_list[k])
						for z in rec_list:
							if(z==i):
								if(var != i):  
									for d in range(MAX_EXPECTED_DIFF_NICKS):
										if ((d<len(L)) and (i in L[d])):
											nick_receiver=L[d][0]
											break
								
									for r in xrange(0,MAX_EXPECTED_DIFF_NICKS):
										if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
											if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
												conversations[r][0]=conversations[r][0]+1
												break
										if(len(conversations[r])==1):
											conversations[r].append(nick_sender)
											conversations[r].append(nick_receiver)
											conversations[r][0]=conversations[r][0]+1
											break
								
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for ij in xrange(0,len(rec_list_2)):                       #changed variable from i to ij as i has been used above. We are in nested for loop. Same variables name will overlap.
								if(rec_list_2[ij]):
									rec_list_2[ij] = ext.util.correctLastCharCR(rec_list_2[ij])
							for j in rec_list_2:
								if(j==i):
									if(var != i):  
										for d in range(MAX_EXPECTED_DIFF_NICKS):
											if i in L[d]:
												nick_receiver=L[d][0]
												break
												
										for r in xrange(0,MAX_EXPECTED_DIFF_NICKS):
											if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
												if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
													conversations[r][0]=conversations[r][0]+1
													break
											if(len(conversations[r])==1):
												conversations[r].append(nick_sender)
												conversations[r].append(nick_receiver)
												conversations[r][0]=conversations[r][0]+1
												break

						if(flag_comma == 0):
							rec=line[line.find(">")+1:line.find(", ")]
							rec=rec[1:]
							rec = ext.util.correctLastCharCR(rec) 
							if(rec==i):
								if(var != i):
									for d in range(MAX_EXPECTED_DIFF_NICKS):
										if i in L[d]:
											nick_receiver=L[d][0]
											break
											
									for r in xrange(0,MAX_EXPECTED_DIFF_NICKS):
										if (nick_sender in conversations[r] and nick_receiver in conversations[r]): 
											if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
												conversations[r][0]=conversations[r][0]+1
												break
										if(len(conversations[r])==1):
											conversations[r].append(nick_sender)
											conversations[r].append(nick_receiver)
											conversations[r][0]=conversations[r][0]+1
											break

			for index in xrange(0,MAX_EXPECTED_DIFF_NICKS):
				if(len(conversations[index])==3):
					aggregate_graph.add_edge(conversations[index][1],conversations[index][2],weight=conversations[index][0])  

	# print("========> nicks")
	# print(nicks)
	# print("========> nick_same_list")
	# print(nick_same_list)
	# print("========> conversations")
	# print(conversations)
	
	for u,v,d in aggregate_graph.edges(data=True):
		d['label'] = d.get('weight','')

	output_file=output_directory+channel_name+"_2013_"+str(startingMonth)+"_"+str(endingMonth)+"_aggregategraph.png"
	print "Generating "+output_file
	print "Please wait ...."

	A = nx.nx_agraph.to_agraph(aggregate_graph)
	A.layout(prog='dot')
	A.draw(output_file)
	print("Done Generating")
