#This code generates a time-series graph. Such a graph has users on the y axis and msg transmission time on x axis.This means that if there exit 4 users- A,B,C,D. 
#Then if any of these users send a message at time t, then we put a dot infront of that user at time t in the graph.
import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import numpy
import datetime
import time
import pandas as pd

#yofel shadeslayer, yofel pheonixbrd
for iterator in range(2,3):
	for fileiterator in range(1,2):
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
		nicks = [] #list of all the nicknames
		send_time = [] #list of all the times a user sends a message to another user
		conv_time = []
		Numofmsg = []
		channel= "#kubuntu-devel" #channel name
		groups = ['yofel_','phoenix_firebrd', 'shadeslayer'] #first will be assigned UID 50, second 100, third 150 and so on   
		groupsnum = []
		groupsnum.append(50)
		for i in range(0, len(groups)-1):
			groupsnum.append(50+groupsnum[i])

		
#code for getting all the nicknames in a list
		for i in content:
			if(i[0] != '=' and "] <" in i and "> " in i):
				m = re.search(r"\<(.*?)\>", i)
				if m.group(0) not in nicks:                       
					nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list



		for i in xrange(0,len(nicks)):
			nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
				
		for i in xrange(0,len(nicks)):
			if(nicks[i][len(nicks[i])-1]=='\\'):
				nicks[i]=nicks[i][:-1]
				nicks[i]=nicks[i]+'CR'

		for j in content:
			if(j[0]=='=' and "changed the topic of" not in j):
				line1=j[j.find("=")+1:j.find(" is")]
				line2=j[j.find("wn as")+1:j.find("\n")]
				line1=line1[3:]
				line2=line2[5:]
				if(line1[len(line1)-1]=='\\'):
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

		x=[[] for i in range(len(nicks))]
		for line in content:
			if(line[0]=='=' and "changed the topic of" not in line):
				line1=line[line.find("=")+1:line.find(" is")]
				line2=line[line.find("wn as")+1:line.find("\n")]
				line1=line1[3:]
				line2=line2[5:]
				if(line1[len(line1)-1]=='\\'):
					line1=line1[:-1]
					line1=line1 + 'CR' 
				if(line2[len(line2)-1]=='\\'):
					line2=line2[:-1]
					line2=line2 + 'CR'
				for i in range(len(nicks)):
					if line1 in x[i]:
						x[i].append(line1)
						x[i].append(line2)
						break
					if not x[i]:
						x[i].append(line1)
						x[i].append(line2)
						break

		
		

#code for making relation map between clients

		
		for line in content:
			flag_comma = 0
			if(line[0] != '=' and "] <" in line and "> " in line):
				m = re.search(r"\<(.*?)\>", line)
				var = m.group(0)[1:-1]
				if(var[len(var)-1]=='\\'):
					var=var[:-1]
					var=var + 'CR' 
				for d in range(len(nicks)):
					if var in x[d]:
						pehla = x[d][0]
						break
					else:
						pehla=var
						

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
									if i in x[d]:
										second=x[d][0]
										break
									else:
										second=i
							
							
							if pehla in groups and second in groups:
								conv_time.append(line[1:6])       #We store time and index of sender, so that in our graph we can put a mark on that index at that time.
								Numofmsg.append(groupsnum[groups.index(pehla)])

							
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
										if i in x[d]:
											second=x[d][0]
											break
										else:
											second=i
								
								if pehla in groups and second in groups:
									conv_time.append(line[1:6])
									Numofmsg.append(groupsnum[groups.index(pehla)])
								
		

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
									if i in x[d]:
										second=x[d][0]
										break
									else:
										second=i
							
							if pehla in groups and second in groups:
								conv_time.append(line[1:6])
								Numofmsg.append(groupsnum[groups.index(pehla)])


		print(conv_time)
		print(Numofmsg)

		data = {'Time': conv_time, 
								'Message_Sent': Numofmsg}
		df = pd.DataFrame(data, columns = ['Time', 'Message_Sent'])
		df.index = df['Time']
		del df['Time']
		df
		print(df)
		axes = plt.gca()
		axes.set_ylim([0,200])
		df.plot(ax=axes ,style=['o','rx'])
		plt.savefig('time-series.png')
		plt.close()


#Here we have plotted the graph with msg transmission time as x axis and users(A(50),B(100),C(150).....) as y axis.
#User who sends more messages will have a higher density of dots infront of its index.



