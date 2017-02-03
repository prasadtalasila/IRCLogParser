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
import ext.util

def findConvLength_ConvRefreshTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	""" Calculates the conversation length that is the length of time for which two users communicate 
	i.e. if a message is not replied to within RT, 
	then it is considered as a part of another conversation.
	This function also calculates the conversation refresh time. 
	For a pair of users, this is the time when one conversation ends and another one starts.

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
	nick_same_list=[[] for i in range(7000)]
	nicks = [] #list of all the nicknames
	conv = []
	conv_diff = []
	
	# out_dir_msg_num = output_directory+"CL/"
	out_dir_msg_num = output_directory
	if not os.path.exists(os.path.dirname(out_dir_msg_num)):
		try:
			os.makedirs(os.path.dirname(out_dir_msg_num))
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
					
			send_time = [] #list of all the times a user sends a message to another user
			nicks_for_the_day = []
			
			print(filePath)   
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
						nicks[i]=ext.util.correctLastCharCR(nicks[i])

			for j in content:
				if(j[0]=='=' and "changed the topic of" not in j):
					line1=j[j.find("=")+1:j.find(" is")]
					line2=j[j.find("wn as")+1:j.find("\n")]
					line1=line1[3:]
					line2=line2[5:]
					if(len(line1)!=0):
						line1=ext.util.correctLastCharCR(line1)
						
					if(len(line2)!=0):
						line2=ext.util.correctLastCharCR(line2)
						
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
						line1=ext.util.correctLastCharCR(line1)
						
					if(len(line2)!=0):
						line2=ext.util.correctLastCharCR(line2)
						
					for i in range(7000):
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
		for ind in range(7000):
			if ni in nick_same_list[ind]:
				break
			if not nick_same_list[ind]:
				nick_same_list[ind].append(ni)
				break

	G = ext.util.to_graph(nick_same_list)
	L = list(connected_components(G))

	for i in range(1,len(L)+1):
                L[i-1] = list(L[i-1])

	# We use connected components algorithm to group all those nick clusters that have atleast one nick common in their clusters. So e.g.
	#Cluster 1- nick1,nick2,nick3,nick4(some nicks of a user) #Cluster 2 -nick5,nick6,nick2,nick7. Then we would get - nick1,nick2,nick3,nick4,nick5,nick6,nick7 and we can safely assume they belong to the same user.

	conversations=[[] for i in range(10000)] #This might need to be incremented from 10000 if we have more users. Same logic as the above 7000 one. Applies to all the other codes too.
	graph_to_sir = []                ## I would advice on using a different data structure which does not have an upper bound like we do in arrays. 
	graph_x_axis = []
	graph_y_axis = []
	graphx1 =[]
	graphy1 =[]
	graphx2 =[]
	graphy2 =[]

	dateadd=-1 #Variable used for response time calculation. Varies from 0-365.
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
			dateadd=dateadd+1
			send_time = [] #list of all the times a user sends a message to another user
			meanstd_list = []
			totalmeanstd_list = []
			x_axis = []
			y_axis = []
			real_y_axis = []
			time_in_min = [[] for i in range(1000)]
			
			print(filePath)

			#code for making relation map between clients		
			for line in content:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					var = m.group(0)[1:-1]
					var=ext.util.correctLastCharCR(var)
					for d in range(len(nicks)):                              #E.g. if names are rohan1,rohan2,rohan3...,then var will store rohan1.
						if((d < len(L)) and (var in L[d])):
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
								rec_list[ik]=ext.util.correctLastCharCR(rec_list[ik])

						for z in rec_list:
							if(z==i):
								send_time.append(line[1:6])
								if(var != i): 	
									for d in range(len(nicks)):
										if((d<len(L)) and (i in L[d])):
											nick_receiver=L[d][0]
											break
										
									for rt in xrange(0,10000):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
											conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5])) # We add response times in conversations for every conversation 
											break                                                                     #between userA and userB. If they havent already conversed 
										if(len(conversations[rt])==0):                                            #before than add time at a new array index and later append to it.
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
											break
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for ij in xrange(0,len(rec_list_2)):
								if(rec_list_2[ij]):
									rec_list_2[ij]=ext.util.correctLastCharCR(rec_list_2[ij])

							for j in rec_list_2:
								if(j==i):
									send_time.append(line[1:6])
									if(var != i): 	
										for d in range(len(nicks)):
											if((d<len(L)) and (i in L[d])):   #Lines 212-255 consider all cases in which messages are addressed such as - nick1:nick2 or nick1,nick2,
												nick_receiver=L[d][0]                   #or nick1,nick2:
												break
										
										for rt in xrange(0,10000):
											if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
												conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5])) 
												break
											if(len(conversations[rt])==0):
												conversations[rt].append(nick_sender)
												conversations[rt].append(nick_receiver)
												conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
												break

						if(flag_comma == 0):
							rec=line[line.find(">")+1:line.find(", ")] 
							rec=rec[1:]
							rec=ext.util.correctLastCharCR(rec)
								
							if(rec==i):
								send_time.append(line[1:6])
								if(var != i):
									for d in range(len(nicks)):
										if ((d<len(L)) and (i in L[d])):
											nick_receiver=L[d][0]
											break
									
									for rt in xrange(0,10000):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):	
											conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
											break
										if(len(conversations[rt])==0):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(24*60*dateadd + int(line[1:6][0:2])*60+int(line[1:6][3:5]))
											break
		
	#Lines 212-290 consider all cases in which messages are addressed as - (nick1:nick2 or nick1,nick2 or nick1,nick2:) and stores their response times in conversations. conversations[i] contains all the response times between userA and userB throughout an entire year.

	for ty in range(0,len(conversations)):       #Lines 295-297 remove the first two elements from every conversations[i] as they are the UIDS of sender and receiver respectively(and not RTs) 
		if(len(conversations[ty])!=0):              # response times are calculated starting from index 2. So now we have all the response times in conversations.
			del conversations[ty][0:2]

	for fg in range(0,len(conversations)):
		if(len(conversations[fg])!=0):
			first=conversations[fg][0]
			for gh in range(1,len(conversations[fg])):
					if(conversations[fg][gh]-conversations[fg][gh-1]>9):
					
						conv.append(conversations[fg][gh-1]-first)    #We are recording the conversation length in conv and CRT in conv_diff. Here 9 is the average response
																																										#time we have already found before(see parser-RT.py). For every channel this value differs and would have to be changed in the code.
						conv_diff.append(conversations[fg][gh]-conversations[fg][gh-1])
						first=conversations[fg][gh]
					if(gh==(len(conversations[fg])-1)):
						conv.append(conversations[fg][gh]-first)					
						break

	for op in range(0,max(conv)):
		graphx1.append(op)
		graphy1.append(conv.count(op))

	for po in range(0,max(conv_diff)):
		graphx2.append(po)
		graphy2.append(conv_diff.count(po))

#To plot CDF we store the CL and CRT values and their number of occurences as shown above.

	row_cl = zip(graphx1,graphy1)
	filename1= out_dir_msg_num+channel_name+"_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+"_CL.csv"
	with open(filename1, 'a+') as myfile:
					wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
					for row in row_cl:
						wr.writerow(row)

	row_crt = zip(graphx2,graphy2)
	filename2= out_dir_msg_num+channel_name+"_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+"_CRT.csv"
	with open(filename2, 'a+') as myfile:
					wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
					for row in row_crt:
						wr.writerow(row)

#These values are then written to conv_length and conv_diff csv files.

#The below commented out code is for finding the RT(the 9 value which we used above for finding CRT and CL.) #Refer to parser-RT.py. Of note is that for finding RT
#we do not append conversations like we did above. Instead we append the time in the format (eg. 10:15) straight from the log file(value between [] when the message is sent).
'''
		for ing in range(0,100):
			if(len(conversations[ing])!=0):                 #These lines convert the time from 10:15 format to 615 seconds format. This is simpler for subtraction
				for ing1 in range(2,len(conversations[ing])):
					time_in_min[ing].append(int(conversations[ing][ing1][0:2])*60+int(conversations[ing][ing1][3:5]))
			
			
		for index in range(0,100):
			if(len(conversations[index])!=0):             #These lines subtract the consecutive time values to get the response times for a conversation.
				for index1 in range(2,len(conversations[index])-1):
					conversations[index][index1]=(int(conversations[index][index1+1][0:2])*60+int(conversations[index][index1+1][3:5])) - (int(conversations[index][index1][0:2])*60+int(conversations[index][index1][3:5]))
	

		for index in range(0,100):        #if there are only 3 elements in conversations[i] -uid1,uid2,time, then we make convert time to seconds format.
			if(len(conversations[index])!=0): 
				if(len(conversations[index])==3):                
					conversations[index][2] = int(conversations[index][2][0:2])*60+int(conversations[index][2][3:5])     
				else: 
					del conversations[index][-1]             #else we delete the last element from every conversations[i] since we dont need it after subtraction operation.
																																						#i.e we remove xi as x(i)-x(i-1) has already been recorded at i-1 index.
		print(conversations) 
		
		for index in range(0,100):
			if(len(conversations[index])!=0):
				for index1 in range(2,len(conversations[index])):        #we append all values after subtraction operation without the UIDs. Thats why second for
					totalmeanstd_list.append(conversations[index][index1])  # loop starts with 2. 0 and 1 index are UIDs. Values are appended to totalmean_std.

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
			if(len(conversations[index])!=0):
				for index1 in range(2,len(conversations[index])):   #Again we are appending mean and std values for RTs of a conversation between two users.
					meanstd_list.append(conversations[index][index1])   #This time appending to conversations.
				conversations[index].append(numpy.mean(meanstd_list))
				conversations[index].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
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
