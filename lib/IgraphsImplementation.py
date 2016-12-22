#We do the same operations usually performed with networkx, but this time with python-igraphs. Igraphs is useful as it can achieve various things that networkx cant. It can also write a graph in various diffent formats useful for tools such as Infomaps and Gephi.

import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import igraph
from igraph import *

def remove_values_from_list(the_list, val):
	return [value for value in the_list if value != val]

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


def implementWithIgraphs(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):

	nick_same_list=[[] for i in range(5000)]
	nicks = [] #list of all the nicknames

	conversations=[[] for i in range(5000)]
	for i in xrange(0,5000):
		conversations[i].append(0)

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
			send_time = [] #list of all the times a user sends a message to another user
			nicks_for_the_day = []
			channel= "#kubuntu-devel" #channel name
			
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
		L[i-1] = [i]+L[i-1]

	#print(L)
	#Uptil here we have all the nicks of the same user clustered together.

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
							content = f.readlines() #contents stores all the lines of the file channel_name 
			print(filePath)
		
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var=correctLastCharCR(var)
					for d in range(len(nicks)):
						if var in L[d]:
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
										
									for rt in xrange(0,5000):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
											if (nick_sender == conversations[rt][1] and nick_receiver == conversations[rt][2]):
												conversations[rt][0]=conversations[rt][0]+1
												break
										if(len(conversations[rt])==1):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt][0]=conversations[rt][0]+1
											break
							
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
										
										for rt in xrange(0,5000):
											if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
												if (nick_sender == conversations[rt][1] and nick_receiver == conversations[rt][2]):
													conversations[rt][0]=conversations[rt][0]+1
													break
											if(len(conversations[rt])==1):
												conversations[rt].append(nick_sender)
												conversations[rt].append(nick_receiver)
												conversations[rt][0]=conversations[rt][0]+1
												break

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
									
									for rt in xrange(0,5000):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]): 
											if (nick_sender == conversations[rt][1] and nick_receiver == conversations[rt][2]):
												conversations[rt][0]=conversations[rt][0]+1
												break
										if(len(conversations[rt])==1):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt][0]=conversations[rt][0]+1
											break
						
	G = Graph(directed=True)  #graph with multiple directed edges between clients used 
	#Notice how the syntax changes with python-igraphs as compared to networkx.

	vertex1=[]
	edge1=[]
	for fin in xrange(0,5000):
		if(len(conversations[fin])==3):
			if(str(conversations[fin][1]) not in vertex1):
				G.add_vertex(str(conversations[fin][1]))
				vertex1.append(str(conversations[fin][1]))
			if(str(conversations[fin][2]) not in vertex1):
				G.add_vertex(str(conversations[fin][2]))
				vertex1.append(str(conversations[fin][2]))  #vertex1 contains the vertex names.
			edge1.append(conversations[fin][0])          #edge1 contains the edge weights
			G.add_edge(str(conversations[fin][1]),str(conversations[fin][2]))  

	G.vs['name'] = vertex1
	G.es['label'] = edge1       #Here we add all the labels like color,name,id,weights etc that we want in our graph
	G.es['weight'] = edge1
	G.vs['id'] = G.vs['name']
	G.es['width'] = edge1

	#print(vertex1)
	#print(conversations)
	#G.write_adjacency("adja_wholeyear.csv",sep=',') #Igraphs has a simple function for printing the adjacency matrix of a graph to a csv file.
	
	G.write_pajek("checkpajek.net")  #writes a graph in pajek format.
	plot(G, "checkgraph.png",edge_width=rescale(edge1,out_range=(1, 15)),layout = G.layout_fruchterman_reingold(), edge_arrow_size=0.5, vertex_size=8)
'''
#Remember to indent everything by one space below this

n_brilli=channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_fourth.png"
print("Here I am")
G.es.select(weight=1).delete()
print(edge1)
edge1 = remove_values_from_list(edge1, 1)
print(edge1)

#we can delete edges with certain weights like 1 in above case. We can delete a list of vertices as shown below. We can append edges too.
#Everything is quite flexible with python-igraphs

list_ver=["124","137","81","199","1","38","198","139","185","146","109","91","254","82","70","111","420","223","327","214","4"]
G.delete_vertices(list_ver)
edge1.append(1)
G.add_edge("196","460") 
edge1.append(1) 
G.add_edge("460","196") 
edge1.append(1) 
G.add_edge("151","259")
edge1.append(1)
G.add_edge("259","151")
edge1.append(1)
G.add_edge("338","121")
m_brilli = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_pajek_patanahi.net"
'''

'''
#We can give different colors to specific vertices as shown below. color is an attribute for both vertex and edge.
G.vs[39]['color'] = 'green'
G.vs[38]['color'] = 'green'
G.vs[27]['color'] = 'cyan'
G.vs[6]['color'] = 'cyan'
G.vs[43]['color'] = 'blue'
G.vs[42]['color'] = 'blue'
G.vs[26]['color'] = 'orange'
G.vs[20]['color'] = 'orange'
#plot(G, n_brilli,edge_width=rescale(edge1,out_range=(1, 15)),layout = G.layout_fruchterman_reingold(), edge_arrow_size=0.5, vertex_size=8)
m_brilli = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_pajek_patanahi.net"


print("\n")
#print(n_brilli)


#G.write_pajek(m_brilli)


#print(G.es['weight'])
cl = G.community_infomap(edge_weights=G.es['weight'])     #igraphs has its own community detection infomaps function.
printingt(cl)
cl.es.select(weight=1).delete()
#print(max(cl.membership))
		
#Z=cl.subgraph(0)      # We can get subgraphs of a graph and work on it too.
#print(Z)


#Z.write_pajek("Zkapajek.net")
#SCL=Z.community_infomap(edge_weights=Z.es['weight'],trials=10)
#print(SCL)

#print(max(SCL.membership))
#sys.exit(1)
#print(G.modularity(cl.membership,weights=edge1))
#print("modularity")
#print(cl.modularity)


#We can get the modularity value of a graph and then also plot it as shown below. Igraph also offers various different layouts. Its exciting to play
#around with them to get a better idea of them.

color_list = ['blue','red','green','cyan','pink','orange','grey']
layout1 = G.layout("lgl")


plot(cl, "graph_Janurrr_subgraph_lgl_final_last.png", edge_width=rescale(G.es['weight'],out_range=(1, 15)), layout=layout1, edge_arrow_size=0.5,
			vertex_color=[color_list[x] for x in cl.membership],
			vertex_size=25)


'''