import numpy
import datetime
import time
import pandas as pd
import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import sys
import csv

#methods used later for clustering nicks of same user.
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


x=[[] for i in range(7000)] #This value must be incremented from 7000 if need be. We might have more than 7000 users on a channel. If we keep this as 7000
nicks = [] #we will not get all the users. So its better to increment this by certain value and check if the sizeof(L) calculated increases or not. If it 
conv = []#increases then we need to again increment and check for an increase in size(L). However, if size(L) stays the same then 7000 can be used. Same applies to all the other codes.
conv_diff = [] # I would advice on using a different data structure which does not have an upper bound like we do in arrays. 
for iterator in range(1,13):
	for fileiterator in range(1,32):
		if(fileiterator<10):  
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0" 
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"          #Lines 42-53 are for storing every line of a log file in variable called 
		else:                                                             #content
			sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"  
			sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
		if not os.path.exists(sttring):
			continue 
		with open(sttring) as f:
						content = f.readlines()                              
	
		send_time = [] #list of all the times a user sends a message to another user
		picks = []
		channel= "#ubuntu" #channel name
		print(sttring)   
		

		for i in content:
			if(i[0] != '=' and "] <" in i and "> " in i):  #Lines 61-65 are used to store all words between <> in picks.
				m = re.search(r"\<(.*?)\>", i)
				if m.group(0) not in picks:                       
					picks.append(m.group(0))   #used regex to get the string between <> and appended it to the picks list



		for i in xrange(0,len(picks)):
			if picks[i][1:-1] not in nicks:
				nicks.append(picks[i][1:-1])     #Now nicks contains all words with <> removed which earlier picks had.
				
		for i in xrange(0,len(nicks)):
			if(len(nicks[i])!=0 and nicks[i][len(nicks[i])-1]=='\\'):
				nicks[i]=nicks[i][:-1]
				nicks[i]=nicks[i]+'CR'

		for j in content:
			if(j[0]=='=' and "changed the topic of" not in j):
				line1=j[j.find("=")+1:j.find(" is")]
				line2=j[j.find("wn as")+1:j.find("\n")]
				line1=line1[3:]
				line2=line2[5:]                                       #If any nick contains '\' in the end, then we convert that to nicknameCR
				if(len(line1)!=0 and line1[len(line1)-1]=='\\'):
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
			if(line[0]=='=' and "changed the topic of" not in line):   #we dont want the lines in with topic changes to be
				line1=line[line.find("=")+1:line.find(" is")]             #considered
				line2=line[line.find("wn as")+1:line.find("\n")]
				line1=line1[3:]
				line2=line2[5:]
				if(len(line1)!=0 and line1[len(line1)-1]=='\\'):
					line1=line1[:-1]
					line1=line1 + 'CR' 
				if(line2[len(line2)-1]=='\\'):
					line2=line2[:-1]
					line2=line2 + 'CR'
				for i in range(7000):
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


		#Till here we add to x(2-D array of strings) all the nickname changes. E.g. x[i] contains all the nicks of a particular user which he used
		#throughout a year.


for ni in nicks:
	for ind in range(7000):
		if ni in x[ind]:
			break
		if not x[ind]:
			x[ind].append(ni)
			break

#Append all the nicks from nicks array which are not already present in x. These would be the ones who did not change their nicks throughout the
#year.

G = to_graph(x) #function definition is on top
L = list(connected_components(G))

	

for i in range(1,len(L)+1):
	L[i-1] = list(L[i-1])

	# We use connected components algorithm to group all those nick clusters that have atleast one nick common in their clusters. So e.g.
	#Cluster 1- nick1,nick2,nick3,nick4(some nicks of a user) #Cluster 2 -nick5,nick6,nick2,nick7. Then we would get - nick1,nick2,nick3,nick4,nick5,nick6,nick7 and we can safely assume they belong to the same user.

xarr=[[] for i in range(10000)] #This might need to be incremented from 10000 if we have more users. Same logic as the above 7000 one. Applies to all the other codes too.
graph_to_sir = []                ## I would advice on using a different data structure which does not have an upper bound like we do in arrays. 
graph_x_axis = []
graph_y_axis = []
graphx1 =[]
graphy1 =[]
graphx2 =[]
graphy2 =[]

dateadd=-1 #Variable used for response time calculation. Varies from 0-365.
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
						content = f.readlines()                               
		dateadd=dateadd+1
		send_time = [] #list of all the times a user sends a message to another user
		meanstd_list = []
		totalmeanstd_list = []
		x_axis = []
		y_axis = []
		real_y_axis = []
		time_in_min = [[] for i in range(100)]
		channel= "#kubuntu-devel" #channel name
		print(sttring)

		
		
		

#code for making relation map between clients


		

		
		for line in content:
			flag_comma = 0
			if(line[0] != '=' and "] <" in line and "> " in line):
				m = re.search(r"\<(.*?)\>", line)
				var = m.group(0)[1:-1]
				if(var[len(var)-1]=='\\'):
					var=var[:-1]
					var=var + 'CR'                                          #Lines 198-209 make var equal to the first array element of the sender's nick cluster.
				for d in range(len(nicks)):                              #E.g. if names are rohan1,rohan2,rohan3...,then var will store rohan1.
					if((d < len(L)) and (var in L[d])):
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
									if((d<len(L)) and (i in L[d])):
										second=L[d][0]
										break
										
								for rt in xrange(0,10000):
									if (pehla in xarr[rt] and second in xarr[rt]):
										xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5])) # We add response times in xarr for every conversation 
										break                                                                     #between userA and userB. If they havent already conversed 
									if(len(xarr[rt])==0):                                            #before than add time at a new array index and later append to it.
										xarr[rt].append(pehla)
										xarr[rt].append(second)
										xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
										break
							
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
										if((d<len(L)) and (i in L[d])):   #Lines 212-255 consider all cases in which messages are addressed such as - nick1:nick2 or nick1,nick2,
											second=L[d][0]                   #or nick1,nick2:
											break
										
									for rt in xrange(0,10000):
										if (pehla in xarr[rt] and second in xarr[rt]):
											xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5])) 
											break
										if(len(xarr[rt])==0):
											xarr[rt].append(pehla)
											xarr[rt].append(second)
											xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
											break

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
									if ((d<len(L)) and (i in L[d])):
										second=L[d][0]
										break
									
								for rt in xrange(0,10000):
									if (pehla in xarr[rt] and second in xarr[rt]): 
										xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
										break
									if(len(xarr[rt])==0):
										xarr[rt].append(pehla)
										xarr[rt].append(second)
										xarr[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
										break
		
#Lines 212-290 consider all cases in which messages are addressed as - (nick1:nick2 or nick1,nick2 or nick1,nick2:) and stores their response times in xarr. xarr[i] contains all the response times between userA and userB throughout an entire year.



for ty in range(0,len(xarr)):       #Lines 295-297 remove the first two elements from every xarr[i] as they are the UIDS of sender and receiver respectively(and not RTs) 
	if(len(xarr[ty])!=0):              # response times are calculated starting from index 2. So now we have all the response times in xarr.
		del xarr[ty][0:2]


for fg in range(0,len(xarr)):
	if(len(xarr[fg])!=0):
		first=xarr[fg][0]
		for gh in range(1,len(xarr[fg])):
				if(xarr[fg][gh]-xarr[fg][gh-1]>9):
					
					conv.append(xarr[fg][gh-1]-first)    #We are recording the conversation length in conv and CRT in conv_diff. Here 9 is the average response
																																										#time we have already found before(see parser-RT.py). For every channel this value differs and would have to be changed in the code.
					conv_diff.append(xarr[fg][gh]-xarr[fg][gh-1])
					first=xarr[fg][gh]
				if(gh==(len(xarr[fg])-1)):
					
					conv.append(xarr[fg][gh]-first)
					
					break



for op in range(0,max(conv)):
	graphx1.append(op)
	graphy1.append(conv.count(op))

for po in range(0,max(conv_diff)):
	graphx2.append(po)
	graphy2.append(conv_diff.count(po))

#To plot CDF we store the CL and CRT values and their number of occurences as shown above.


rowt = zip(graphx1,graphy1)
with open('/home/dhruvie/LOP/conv_length_recal_aaj.csv', 'a+') as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				for row in rowt:
					wr.writerow(row)




roww = zip(graphx2,graphy2)
with open('/home/dhruvie/LOP/conv_diff_recal_aaj.csv', 'a+') as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				for row in roww:
					wr.writerow(row)


#These values are then written to conv_length and conv_diff csv files.

#The below commented out code is for finding the RT(the 9 value which we used above for finding CRT and CL.) #Refer to parser-RT.py. Of note is that for finding RT
#we do not append xarr like we did above. Instead we append the time in the format (eg. 10:15) straight from the log file(value between [] when the message is sent).
'''
		for ing in range(0,100):
			if(len(xarr[ing])!=0):                 #These lines convert the time from 10:15 format to 615 seconds format. This is simpler for subtraction
				for ing1 in range(2,len(xarr[ing])):
					time_in_min[ing].append(int(xarr[ing][ing1][0:2])*60+int(xarr[ing][ing1][3:5]))
			
			
		for index in range(0,100):
			if(len(xarr[index])!=0):             #These lines subtract the consecutive time values to get the response times for a conversation.
				for index1 in range(2,len(xarr[index])-1):
					xarr[index][index1]=(int(xarr[index][index1+1][0:2])*60+int(xarr[index][index1+1][3:5])) - (int(xarr[index][index1][0:2])*60+int(xarr[index][index1][3:5]))
	

		
		for index in range(0,100):        #if there are only 3 elements in xarr[i] -uid1,uid2,time, then we make convert time to seconds format.
			if(len(xarr[index])!=0): 
				if(len(xarr[index])==3):                
					xarr[index][2] = int(xarr[index][2][0:2])*60+int(xarr[index][2][3:5])     
				else: 
					del xarr[index][-1]             #else we delete the last element from every xarr[i] since we dont need it after subtraction operation.
																																						#i.e we remove xi as x(i)-x(i-1) has already been recorded at i-1 index.
		print(xarr) 
		

		for index in range(0,100):
			if(len(xarr[index])!=0):
				for index1 in range(2,len(xarr[index])):        #we append all values after subtraction operation without the UIDs. Thats why second for
					totalmeanstd_list.append(xarr[index][index1])  # loop starts with 2. 0 and 1 index are UIDs. Values are appended to totalmean_std.

		if(len(totalmeanstd_list)!=0):  

			for iy in range(0, max(totalmeanstd_list)+1):
				x_axis.append(iy)

			

			for ui in x_axis:
				y_axis.append(float(totalmeanstd_list.count(ui))/float(len(totalmeanstd_list)))
			


			real_y_axis.append(y_axis[0])
			for ix in range(1, len(y_axis)):
				real_y_axis.append(float(real_y_axis[ix-1])+float(y_axis[ix]))

			



'''
'''
			data = {'Response time': x_axis, 
									'CDF': real_y_axis}
			df = pd.DataFrame(data, columns = ['Response time', 'CDF'])
			df.index = df['Response time']
			del df['Response time']
			df
																																																		#Here we plot the response time and CDF using pandas library.
			axes = plt.gca()
			#axes.set_xlim([0,300])
			axes.set_ylim([0,1.2])
			df.plot(ax=axes)
			name = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_response_time_CDF.pdf"
			#plt.show()
			plt.savefig(name)
			plt.close()
			
'''
'''
		for hi in range(0,len(totalmeanstd_list)):
			graph_to_sir.append(totalmeanstd_list[hi])


		totalmeanstd_list.append(numpy.mean(totalmeanstd_list))     #Here we are basically appending the mean and std values for RTs just for timepass
		totalmeanstd_list.append(numpy.mean(totalmeanstd_list)+2*numpy.std(totalmeanstd_list))

		
		
		for index in range(0,100):
			if(len(xarr[index])!=0):
				for index1 in range(2,len(xarr[index])):   #Again we are appending mean and std values for RTs of a conversation between two users.
					meanstd_list.append(xarr[index][index1])   #This time appending to xarr.
				xarr[index].append(numpy.mean(meanstd_list))
				xarr[index].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
				meanstd_list[:] = []

		#Ignore the part below this. Its wrong.
		#____________________________________________________________________________________________________________________________________________
		for fina in range(0,100):
			if(len(xarr[fina])!=0):
				calc = time_in_min[fina][0] + xarr[fina][len(xarr[fina])-1]
				for somet in range(0,len(time_in_min[fina])):
					if (time_in_min[fina][somet] > calc):
						subtr = time_in_min[fina][somet-1] - time_in_min[fina][0]
						xarr[fina].append(subtr)
						break
					else:
						subtr = time_in_min[fina][len(time_in_min[fina])-1] - time_in_min[fina][0]
						xarr[fina].append(subtr)
						break

		#print("Conversation RT Info")
		#print(xarr)
	
		#print("Total Response-Time")
		#print(totalmeanstd_list)
		#print("\n\n")
		
#print("grpahs to graph_to_sir")  
#print(graph_to_sir)

graph_to_sir.sort()
#print(graph_to_sir)


for ti in range(0,graph_to_sir[len(graph_to_sir)-1]+1):
	graph_y_axis.append(graph_to_sir.count(ti))
	graph_x_axis.append(ti)


#print(graph_y_axis)
#print(graph_x_axis)
#print(len(graph_y_axis))
#print(len(graph_x_axis))

rows = zip(graph_x_axis,graph_y_axis)         #Storing the RT values and their frequencies in csv file.
with open('/home/dhruvie/LOP/graphforsir2.csv', 'a+') as myfile:
				wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
				for row in rows:
					wr.writerow(row)


'''

