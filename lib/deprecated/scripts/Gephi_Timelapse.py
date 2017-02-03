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

#print(today1[0])

my_sum=0  #ignore this 

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


x=[[] for i in range(5000)]

nicks = [] #list of all the nicknames

for iterator in range(1,13):
	for fileiterator in range(1,32):
		if(fileiterator<10):  
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0" 
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
		else:
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"  
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
		if not os.path.exists(sttring):
			continue 
		with open(sttring) as f:
						content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel   
	
		send_time = [] #list of all the times a user sends a message to another user
		picks = []
		channel= "#kubuntu-devel" #channel name
		#print(sttring)   
		
#code for getting all the nicknames in a list
		for i in content:
			if(i[0] != '=' and "] <" in i and "> " in i):
				m = re.search(r"\<(.*?)\>", i)
				if m.group(0) not in picks:                       
					picks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list



		for i in xrange(0,len(picks)):
			if picks[i][1:-1] not in nicks:
				nicks.append(picks[i][1:-1])     #removed <> from the nicknames
				
		for i in xrange(0,len(nicks)):
			if(nicks[i] and nicks[i][len(nicks[i])-1]=='\\'):
				nicks[i]=nicks[i][:-1]
				nicks[i]=nicks[i]+'CR'

		for j in content:
			if(j[0]=='=' and "changed the topic of" not in j):
				line1=j[j.find("=")+1:j.find(" is")]
				line2=j[j.find("wn as")+1:j.find("\n")]
				line1=line1[3:]
				line2=line2[5:]
				if(line1 and line1[len(line1)-1]=='\\'):
					line1=line1[:-1]
					line1=line1 + 'CR' 
				if(line2[len(line2)-1]=='\\'):
					line2=line2[:-1]
					line2=line2 + 'CR'
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
				if(line1 and line1[len(line1)-1]=='\\'):
					line1=line1[:-1]
					line1=line1 + 'CR' 
				if(line2[len(line2)-1]=='\\'):
					line2=line2[:-1]
					line2=line2 + 'CR'
				for i in range(5000):
					if line1 in x[i] or line2 in x[i]:
						if line1 in x[i] and line2 not in x[i]:
							x[i].append(line2)
							break
						if line2 in x[i] and line1 not in x[i]: 
							x[i].append(line1)
							break
						if line2 in x[i] and line1 in x[i]:
							break  
					if not x[i]:
						x[i].append(line1)
						x[i].append(line2)
						break


		

#print(x)  
for ni in nicks:
	for ind in range(5000):
		if ni in x[ind]:
			break
		if not x[ind]:
			x[ind].append(ni)
			break

#print("*********************x**********************************")
#print(x)


G = to_graph(x)
L = list(connected_components(G))



for i in range(1,len(L)+1):
	L[i-1] = list(L[i-1])

#The explanation for the aforementioned code has already been given in parser-RT.py.

#Lines 190-233 are for the nodes in Gephi. We make sure that all nodes are always present throughout our timelapse. For this reason the appear
#and disappear times for all the nodes are 1 Jan 00:00:01 to 1 Feb 00:00:01 (our timelapse is for a month). If we want our nodes to appear or disappear at some other times
# change their values here itself. Our aim is to store all these tables in a csv file. Gephi imports these node and edge csv 
#files, parses them and produces the timelapse.
createvar = -1
for iterator in range(1,13):
	for fileiterator in range(1,32):
		if(fileiterator<10):  
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0" 
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
		else:
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"  
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
		if not os.path.exists(sttring):
			continue 
		with open(sttring) as f:
						content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel   
		createvar = createvar + 1
		picks_again = []
		channel= "#kubuntu-devel" #channel name
		print(sttring)   
		
#code for getting all the nicknames in a list
		for il in content:
			if(il[0] != '=' and "] <" in il and "> " in il):
				m = re.search(r"\<(.*?)\>", il)
				if m.group(0) not in picks_again:                       
					picks_again.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list
		pakau = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_conversation.png"
		#print(pakau)
		#print(picks_again)
		for nx in picks_again:
			for dk in range(len(nicks)):
				if (dk<len(L) and nx[1:-1] in L[dk]):
					col1.append(str(L[dk][0]))
					col2.append(str(L[dk][0]))
					#col3.append(today1[createvar])
					#col4.append(today2[createvar])
					col3.append("2013-01-01 00:00:01") #Nodes stay throughout the month. Col3 and Col4 are the appear and disappear times.
					col4.append("2013-02-01 00:00:01")
					break
		

rows = zip(col1,col2,col3,col4)    # We store everything in a csv file which we will later import to Gephi. We are Gephi's slaves!
with open('/home/dhruvie/LOP/nodesgephi.csv', 'a+') as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				for ro in rows:
					wr.writerow(ro)
					
#The below code similarly is for obtaining the edge csv file which we is imported to gephi later. The difference here
#is that we know when the edges appear. We obtain this from the log file(line[1:6]), we just append :00 to satisfy the hh:mm:ss format, Gephi wants.

createvar_used=-1 
for iterator in range(1,13):
	for fileiterator in range(1,32):
		if(fileiterator<10):  
			sttring="/home/dhruvie/LOP/2006/"+str(iterator)+"/0" 
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
		else:
			sttring="/home/dhruvie/LOP/2006/"+str(iterator)+"/"  
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
		if not os.path.exists(sttring):
			continue 
		with open(sttring) as f:
						content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel   
		createvar_used=createvar_used+1    
		#print(sttring)
		nickplots = [] #nickplots stores all those nicks from nicks[] list that do not have zero in and outdegree in our conversation graph
		indegree = [] #this list stores all the indegree corresponding to a particular nick
		outdegree = [] #this list stores all the outdegree corresponding to a particular nick
		

#  G1 = nx.MultiDiGraph()  
		for line in content:
			flag_comma = 0
			if(line[0] != '=' and "] <" in line and "> " in line):
				m = re.search(r"\<(.*?)\>", line)
				var = m.group(0)[1:-1]
				if(var[len(var)-1]=='\\'):
					var=var[:-1]
					var=var + 'CR' 
				for d in range(len(nicks)):
					if (d<len(L) and var in L[d]):
						pehla = L[d][0]
						break
						

				for i in nicks:
					data=[e.strip() for e in line.split(':')]
					data[1]=data[1][data[1].find(">")+1:len(data[1])]
					data[1]=data[1][1:]
					if not data[1]:
						break
					for ik in xrange(0,len(data)):
						if(data[ik] and data[ik][len(data[ik])-1]=='\\'):
							data[ik]=data[ik][:-1]
							data[ik]=data[ik] + 'CR'
					for z in data:
						if(z==i):
							send_time.append(line[1:6])
							if(var != i):  
								for d in range(len(nicks)):
									if i in L[d]:
										second=L[d][0]
										break
								col_edge1.append(pehla)
								col_edge2.append(second)   #We are going to add all these columns in a csv file for Gephi's use.
								col_edge3.append("Directed")
								col_edge4.append(1.0)
								col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
								col_edge6.append(today2[createvar_used])
								my_sum=my_sum+1

	#       G1.add_edge(pehla,second,weight=line[1:6])
								if pehla not in nickplots:
									nickplots.append(pehla)  
								if second not in nickplots: #Right time to append to nickplots.
									nickplots.append(second) 
							
					if "," in data[1]: 
						flag_comma = 1
						data1=[e.strip() for e in data[1].split(',')]
						for ij in xrange(0,len(data1)):
							if(data1[ij] and data1[ij][len(data1[ij])-1]=='\\'):
								data1[ij]=data1[ij][:-1]
								data1[ij]=data1[ij] + 'CR'
						for j in data1:
							if(j==i):
								send_time.append(line[1:6])
								if(var != i):  
									for d in range(len(nicks)):
										if i in L[d]:
											second=L[d][0]
											break
									col_edge1.append(pehla)
									col_edge2.append(second)
									col_edge3.append("Directed")
									col_edge4.append(1.0)
									col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
									col_edge6.append(today2[createvar_used])              
									my_sum=my_sum+1
		#       G1.add_edge(pehla,second,weight=line[1:6])  
									if pehla not in nickplots:
										nickplots.append(pehla)   
									if second not in nickplots:
										nickplots.append(second) 

					if(flag_comma == 0):
						search2=line[line.find(">")+1:line.find(", ")] 
						search2=search2[1:]
						if(search2[len(search2)-1]=='\\'):
							search2=search2[:-1]
							search2=search2 + 'CR' 
						if(search2==i):
							send_time.append(line[1:6])
							if(var != i):
								for d in range(len(nicks)):
									if i in L[d]:
										second=L[d][0]
										break
								col_edge1.append(pehla)
								col_edge2.append(second)
								col_edge3.append("Directed")
								col_edge4.append(1.0)
								col_edge5.append(today1[createvar_used]+" "+line[1:6]+":00")
								col_edge6.append(today2[createvar_used]) 
								my_sum=my_sum+1
			#     G1.add_edge(pehla,second,weight=line[1:6])  
								if pehla not in nickplots:
									nickplots.append(pehla)   
								if second not in nickplots:
									nickplots.append(second) 
						
		
		n_brilli=channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_conversation.png"
		print(n_brilli)

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

bitsfc = zip(col_edge1,col_edge2,col_edge3,col_edge4,col_edge5,col_edge6)   
with open('/home/dhruvie/LOP/edgesgephi.csv', 'a+') as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				for rz in bitsfc:
					wr.writerow(rz)  

'''
print(my_sum)  








