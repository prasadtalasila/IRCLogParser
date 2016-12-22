import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os

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


def createMessageTimeGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	out_dir_msg_time = output_directory+"message-time/"

	print "Creating a new output folder"
	os.system("rm -rf "+out_dir_msg_time)
	os.system("mkdir "+out_dir_msg_time)

	rem_time= None #remembers the time of the last message of the file parsed before the current file
	nick_same_list=[[] for i in range(5000)]  #x
	nicks = [] #list of all the nicknames     

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
			'''
				Getting all the nicknames in a list nicks[]
			'''
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks_for_the_day:                       
						nicks_for_the_day.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks_for_the_day)):
				if nicks_for_the_day[i][1:-1] not in nicks:
					nicks.append(nicks_for_the_day[i][1:-1])     #removed <> from the nicknames
					
			for i in xrange(0,len(nicks)):
				nicks[i] = correctLastCharCR(nicks[i])
			
			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					nick1=line[line.find("=")+1:line.find(" is")]
					nick2=line[line.find("wn as")+1:line.find("\n")]
					nick1=nick1[3:]
					nick2=nick2[5:]
					nick1=correctLastCharCR(nick1)
					nick2=correctLastCharCR(nick2)
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
					line1=correctLastCharCR(line1)
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

	for ni in nicks:
		for ind in range(5000):
			if ni in nick_same_list[ind]:
				break
			if not nick_same_list[ind]:
				nick_same_list[ind].append(ni)
				break

	G = to_graph(nick_same_list)
	L = connected_components(G)

	for i in range(1,len(L)+1):
		L[i-1] = [str(i)]+L[i-1]

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

			'''=========================== Plotting the conversation graph =========================== '''
			graph_conversation = nx.MultiDiGraph()  #graph with multiple directed edges between clients used
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var = correctLastCharCR(var)
					for d in range(5000):
						if ((d < len(L)) and (var in L[d])): 
							nick_sender = L[d][0]
							break

					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')] #receiver list splited about :
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]: #index 0 will contain time 14:02
							break
						for k in xrange(0,len(rec_list)):
							if(rec_list[k]): #checking for \
								rec_list[k] = correctLastCharCR(rec_list[k])
						for z in rec_list:
							if(z==i):
								if(var != i):  
									for d in range(5000):
										if ((d < len(L)) and (i in L[d])): 
											nick_receiver=L[d][0]
											break
									graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])  
								
						if "," in rec_list[1]: #receiver list may of the form <Dhruv> Rohan, Ram :
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for y in xrange(0,len(rec_list_2)):
								if(rec_list_2[y]): #checking for \
									rec_list_2[y]=correctLastCharCR(rec_list_2[y])
							for j in rec_list_2:
								if(j==i):
									if(var != i):   
										for d in range(5000):
											if i in L[d]:
												nick_receiver=L[d][0]
												break
										graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])   

						if(flag_comma == 0): #receiver list can be <Dhruv> Rohan, Hi!
							rec=line[line.find(">")+1:line.find(", ")] 
							rec=rec[1:]
							rec=correctLastCharCR(rec)
							if(rec==i):
								if(var != i):
									for d in range(5000):
										if i in L[d]:
											nick_receiver=L[d][0]
											break
									graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])  
							
			for u,v,d in graph_conversation.edges(data=True):
				d['label'] = d.get('weight','')
			output_file=out_dir_msg_time+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_msg_time.png"
			print "Generated " + output_file
			A = nx.to_agraph(graph_conversation)
			A.layout(prog='dot')
			A.draw(output_file)