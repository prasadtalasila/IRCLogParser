import networkx as nx
import re
import numpy
from networkx.algorithms.components.connected import connected_components
import util
import config


def  conv_len_conv_refr_time(log_dict, nicks,nick_same_list):

	""" Calculates the conversation length (CL) that is the length of time for which two users communicate 
	i.e. if a message is not replied to within Response Time(RT), 
	then it is considered as a part of another conversation.
	This function also calculates the conversation refresh time(CRT). 
	For a pair of users, this is the time when one conversation ends and another one starts.
	Args:
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(list) : list of nickname created using nickTracker.py
		nick_same_list :list of same_nick names created using nickTracker.py		
	Returns:
		row_cl(zip list): Conversation Length
		row_crt(zip list) :Conversation Refresh time
	   
	"""	
	conv = []
	conv_diff = []	

	G = util.to_graph(nick_same_list)
	conn_comp_list = list(connected_components(G))

	for i in range(0,len(conn_comp_list)):
		conn_comp_list[i] = list(conn_comp_list[i])

	# We use connected components algorithm to group all those nick clusters that have atleast one nick common in their clusters. So e.g.
	#Cluster 1- nick1,nick2,nick3,nick4(some nicks of a user) #Cluster 2 -nick5,nick6,nick2,nick7. Then we would get - nick1,nick2,nick3,nick4,nick5,nick6,nick7 and we can safely assume they belong to the same user.

	conversations=[[] for i in range(config.MAX_CONVERSATIONS)] #This might need to be incremented from 10000 if we have more users. Same logic as the above 7000 one. Applies to all the other codes too.
											 ## I would advice on using a different data structure which does not have an upper bound like we do in arrays.
	graphx1 =[]
	graphy1 =[]
	graphx2 =[]
	graphy2 =[]

	dateadd = -1 #Variable used for response time calculation. Varies from 0-365.
	for day_content_all_channels in log_dict.values():
		for day_content in day_content_all_channels:
			day_log = day_content["log_data"]

			dateadd = dateadd + 1
			send_time = [] #list of all the times a user sends a message to another user
			meanstd_list = []
			totalmeanstd_list = []
			x_axis = []
			y_axis = []
			real_y_axis = []
			time_in_min = [[] for i in range(config.RESPONSE_TIME_RANGE)]	
			
			#code for making relation map between clients		
			for line in day_log:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):

					m = re.search(r"\<(.*?)\>", line)
					nick_to_search = util.correctLastCharCR(m.group(0)[1:-1])
					for d in range(len(nicks)):                        #E.g. if names are rohan1,rohan2,rohan3...,then var will store rohan1.
						if((d < len(conn_comp_list)) and (nick_to_search in conn_comp_list[d])):
							nick_sender = conn_comp_list[d][0]
							break
						
					for i in nicks:
						rec_list = [e.strip() for e in line.split(':')]
						rec_list[1] = rec_list[1][rec_list[1].find(">") + 1:len(rec_list[1])]
						rec_list[1] = rec_list[1][1:]
						if not rec_list[1]:
							break
						for ik in xrange(0,len(rec_list)):
							if(rec_list[ik]):
								rec_list[ik]=util.correctLastCharCR(rec_list[ik])

						for z in rec_list:
							if(z == i):
								send_time.append(line[1:6])
								if(nick_to_search != i): 	
									for d in range(len(nicks)):
										if((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
											nick_receiver=conn_comp_list[d][0]
											break
										
									for rt in xrange(0,config.MAX_CONVERSATIONS):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
											conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5])) # We add response times in conversations for every conversation 
											break                                                                     #between userA and userB. If they havent already conversed 
										if(len(conversations[rt]) == 0):                                            #before than add time at a new array index and later append to it.
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5]))
											break
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for ij in xrange(0,len(rec_list_2)):
								if(rec_list_2[ij]):
									rec_list_2[ij] = util.correctLastCharCR(rec_list_2[ij])

							for j in rec_list_2:
								if(j == i):
									send_time.append(line[1:6])
									if(nick_to_search != i): 	
										for d in range(len(nicks)):
											if((d<len(conn_comp_list)) and (i in conn_comp_list[d])):   #Lines 212-255 consider all cases in which messages are addressed such as - nick1:nick2 or nick1,nick2,
												nick_receiver=conn_comp_list[d][0]                   #or nick1,nick2:
												break
										
										for rt in xrange(0,config.MAX_CONVERSATIONS):
											if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
												conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5])) 
												break
											if(len(conversations[rt]) == 0):
												conversations[rt].append(nick_sender)
												conversations[rt].append(nick_receiver)
												conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5]))
												break

						if(flag_comma == 0):
							rec = line[line.find(">")+1:line.find(", ")][1:] 							
							rec=util.correctLastCharCR(rec)
								
							if(rec == i):
								send_time.append(line[1:6])
								if(nick_to_search != i):
									for d in range(len(nicks)):
										if ((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
											nick_receiver = conn_comp_list[d][0]
											break
									
									for rt in xrange(0,config.MAX_CONVERSATIONS):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):	
											conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR + int(line[1:6][3:5]))
											break
										if(len(conversations[rt]) == 0):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR + int(line[1:6][3:5]))
											break
		
	#Lines 212-290 consider all cases in which messages are addressed as - (nick1:nick2 or nick1,nick2 or nick1,nick2:) and stores their response times in conversations. conversations[i] contains all the response times between userA and userB throughout an entire year.

	for ty in range(0,len(conversations)):       #Lines 295-297 remove the first two elements from every conversations[i] as they are the UIDS of sender and receiver respectively(and not RTs)
		if(len(conversations[ty]) != 0):              # response times are calculated starting from index 2. So now we have all the response times in conversations.
			del conversations[ty][0:2]

	for fg in range(0,len(conversations)):
		if(len(conversations[fg]) != 0):
			first = conversations[fg][0]
			for gh in range(1,len(conversations[fg])):
					if(conversations[fg][gh]-conversations[fg][gh-1] > 9):
					
						conv.append(conversations[fg][gh-1] - first)    #We are recording the conversation length in conv and CRT in conv_diff. Here 9 is the average response
																																										#time we have already found before(see parser-RT.py). For every channel this value differs and would have to be changed in the code.
						conv_diff.append(conversations[fg][gh] - conversations[fg][gh-1])
						first = conversations[fg][gh]
					if(gh == (len(conversations[fg]) - 1)):
						conv.append(conversations[fg][gh] - first)					
						break

	for op in range(0,max(conv)):
		graphx1.append(op)
		graphy1.append(conv.count(op))

	for po in range(0,max(conv_diff)):
		graphx2.append(po)
		graphy2.append(conv_diff.count(po))

#To plot CDF we store the CL and CRT values and their number of occurences as shown above.

	row_cl = zip(graphx1,graphy1)
	row_crt = zip(graphx2,graphy2)
	
	return row_cl, row_crt

def find_response_time(log_dict, nicks, nick_same_list):

	""" finds the response time of a message 
	i.e. the best guess for the time at which one can expect a reply for his/her message.

	Args:
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(list) : list of nickname created using nickTracker.py
		nick_same_list :list of same_nick names created using nickTracker.py
		output_directory (str): Location of output directory
		
	Returns:
	   rows_RT(zip list): Response Time (This refers to the response
		time of a message i.e. the best guess for the time at
		which one can expect a reply for his/her message)

	"""
	conv = []
	conv_diff = []
	
	G = util.to_graph(nick_same_list)
	conn_comp_list = list(connected_components(G))

	for i in range(0,len(conn_comp_list)):
		conn_comp_list[i] = list(conn_comp_list[i])
	
	graph_to_sir = []
	graph_x_axis = []
	graph_y_axis = []	
	
	dateadd = -1
	
	for day_content_all_channels in log_dict.values():
		for day_content in day_content_all_channels:
			day_log = day_content["log_data"]   

			send_time = [] #list of all the times a user sends a message to another user
			meanstd_list = []
			totalmeanstd_list = []
			x_axis = []
			y_axis = []
			real_y_axis = []
			time_in_min = [[] for i in range(config.RESPONSE_TIME_RANGE)]	
			conversations=[[] for i in range(config.MAX_RESPONSE_CONVERSATIONS)]   

			#code for making relation map between clients		
			for line in day_log:
				flag_comma = 0
				if(line[0] != '=' and "] <" in line and "> " in line):
					m = re.search(r"\<(.*?)\>", line)
					nick_to_search = util.correctLastCharCR(m.group(0)[1:-1])
					for d in range(len(nicks)):
						if((d < len(conn_comp_list)) and (nick_to_search in conn_comp_list[d])):
							nick_sender = conn_comp_list[d][0]
							break			
					for i in nicks:
						rec_list=[e.strip() for e in line.split(':')]
						rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
						rec_list[1]=rec_list[1][1:]
						if not rec_list[1]:
							break
						for ik in xrange(0,len(rec_list)):
							if(rec_list[ik]):
								rec_list[ik]=util.correctLastCharCR(rec_list[ik])
						for z in rec_list:
							if(z == i):
								send_time.append(line[1:6])
								if(nick_to_search != i):  
									for d in range(len(nicks)):
										if((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
											nick_receiver=conn_comp_list[d][0]
											break
										
									for rt in xrange(0,config.MAX_RESPONSE_CONVERSATIONS):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
											conversations[rt].append(line[1:6])
											break
										if(len(conversations[rt]) == 0):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(line[1:6])
											break
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2=[e.strip() for e in rec_list[1].split(',')]
							for ij in xrange(0,len(rec_list_2)):
								if(rec_list_2[ij]):
									rec_list_2[ij]=util.correctLastCharCR(rec_list_2[ij])
									
							for j in rec_list_2:
								if(j == i):
									send_time.append(line[1:6])
									if(nick_to_search != i):   
										for d in range(len(nicks)):
											if((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
												nick_receiver=conn_comp_list[d][0]
												break
										
										for rt in xrange(0,config.MAX_RESPONSE_CONVERSATIONS):
											if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
												conversations[rt].append(line[1:6]) 
												break
											if(len(conversations[rt]) == 0):
												conversations[rt].append(nick_sender)
												conversations[rt].append(nick_receiver)
												conversations[rt].append(line[1:6])
												break

						if(flag_comma == 0):
							rec=line[line.find(">")+1:line.find(", ")][1:] 							
							rec=util.correctLastCharCR(rec)
							if(rec == i):
								send_time.append(line[1:6])
								if(nick_to_search != i):
									for d in range(len(nicks)):
										if ((d<len(conn_comp_list)) and (i in conn_comp_list[d])):
											nick_receiver=conn_comp_list[d][0]
											break
									
									for rt in xrange(0,config.MAX_RESPONSE_CONVERSATIONS):
										if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]): 
											conversations[rt].append(line[1:6])
											break
										if(len(conversations[rt]) == 0):
											conversations[rt].append(nick_sender)
											conversations[rt].append(nick_receiver)
											conversations[rt].append(line[1:6])
											break
			
			for index in range(0,config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[index]) != 0):  
					for index1 in range(2,len(conversations[index]) - 1):
						conversations[index][index1]=(int(conversations[index][index1+1][0:2])*config.MINS_PER_HOUR+int(conversations[index][index1+1][3:5])) - (int(conversations[index][index1][0:2])*config.MINS_PER_HOUR+int(conversations[index][index1][3:5]))
	
			for index in range(0,config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[index]) != 0): 
					if(len(conversations[index]) == 3):
						conversations[index][2] = int(conversations[index][2][0:2])*config.MINS_PER_HOUR+int(conversations[index][2][3:5])     
					else: 
						del conversations[index][-1]

		#Explanation provided in parser-CL+CRT.py
			for index in range(0,config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[index]) != 0):
					for index1 in range(2,len(conversations[index])):
						totalmeanstd_list.append(conversations[index][index1])

			if(len(totalmeanstd_list) != 0):
				for iy in range(0, max(totalmeanstd_list) + 1):
					x_axis.append(iy)

				for ui in x_axis:
					y_axis.append(float(totalmeanstd_list.count(ui)) / float(len(totalmeanstd_list)))
				
				#finding the probability of each RT to occur=No. of occurence/total occurences.
				real_y_axis.append(y_axis[0])
				for ix in range(1, len(y_axis)):
					real_y_axis.append(float(real_y_axis[ix-1]) + float(y_axis[ix]))
			
			#to find cumulative just go on adding the current value to previously cumulated value till sum becomes 1 for last entry.
			for hi in range(0,len(totalmeanstd_list)):
				graph_to_sir.append(totalmeanstd_list[hi])

			totalmeanstd_list.append(numpy.mean(totalmeanstd_list))
			totalmeanstd_list.append(numpy.mean(totalmeanstd_list)+2*numpy.std(totalmeanstd_list))
		
			for index in range(0,config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[index])!=0):
					for index1 in range(2,len(conversations[index])):
						meanstd_list.append(conversations[index][index1])
					conversations[index].append(numpy.mean(meanstd_list))
					conversations[index].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
					meanstd_list[:] = []

	graph_to_sir.sort()

	for ti in range(0,graph_to_sir[len(graph_to_sir)-1] + 1):
		graph_y_axis.append(graph_to_sir.count(ti))     # problem when ti=0 count is unexpectedly large
		graph_x_axis.append(ti)
	

#Finally storing the RT values along with their frequencies in a csv file. 
	rows_RT = zip(graph_x_axis,graph_y_axis)

	return rows_RT	