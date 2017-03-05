import re
import numpy
from networkx.algorithms.components.connected import connected_components
import util
import config

def conv_len_conv_refr_time(log_dict, nicks, nick_same_list):

	""" Calculates the conversation length (CL) that is the length of time for which two users communicate 
	i.e. if a message is not replied to within Response Time(RT), 
	then it is considered as a part of another conversation.
	This function also calculates the conversation refresh time(CRT)
	For a pair of users, this is the time when one conversation ends and another one starts.
	Args:   
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(List) : list of nickname created using nickTracker.py
		nick_same_list :List of same_nick names created using nickTracker.py        
	Returns:
		row_cl(zip List): Conversation Length
		row_crt(zip List) :Conversation Refresh time
	   
	""" 
	conv = []
	conv_diff = []  

	G = util.to_graph(nick_same_list)
	conn_comp_list = list(connected_components(G))

	util.create_connected_nick_list(conn_comp_list)

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
			#code for making relation map between clients       
			for line in day_log:
				flag_comma = 0
				if(util.check_if_msg_line (line)):
					nick_sender = ""
					nick_receiver = ""
					m = re.search(r"\<(.*?)\>", line)
					nick_to_search = util.correctLastCharCR(m.group(0)[1:-1])
					for d in range(len(nicks)):                        #E.g. if names are rohan1,rohan2,rohan3...,then var will store rohan1.
						if((d < len(conn_comp_list)) and (nick_to_search in conn_comp_list[d])):
							nick_sender = conn_comp_list[d][0]
							break
						
					for nick in nicks:
						rec_list = [e.strip() for e in line.split(':')]
						util.rec_list_splice(rec_list)						
						if not rec_list[1]:
							break
						#for i in range(len(rec_list)):
							#if(rec_list[i]):
								#rec_list[i] = util.correctLastCharCR(rec_list[i])
						rec_list = util.correct_last_char_list(rec_list)		

						for names in rec_list:
							if(names == nick):
								send_time.append(line[1:6])
								if(nick_to_search != nick):     
									for d in range(len(nicks)):
										if((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):
											nick_receiver = conn_comp_list[d][0]
											break
										
									for i in range(config.MAX_CONVERSATIONS):
										if (nick_sender in conversations[i] and nick_receiver in conversations[i]):
											conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5]))   # We add response times in conversations for every conversation 
											break                                                                     #between userA and userB. If they havent already conversed 
										if(len(conversations[i]) == 0):                                               #before than add time at a new array index and later append to it.
											conversations[i].append(nick_sender)
											conversations[i].append(nick_receiver)
											conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5]))
											break
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2 = [e.strip() for e in rec_list[1].split(',')]
							#for i in range(len(rec_list_2)):
								#if(rec_list_2[i]):
									#rec_list_2[i] = util.correctLastCharCR(rec_list_2[i])
							rec_list_2 = util.correct_last_char_list(rec_list_2)		

							for names in rec_list_2:
								if(names == nick):
									send_time.append(line[1:6])
									if(nick_to_search != nick):
										for d in range(len(nicks)):
											if((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):   #Lines 212-255 consider all cases in which messages are addressed such as - nick1:nick2 or nick1,nick2,
												nick_receiver = conn_comp_list[d][0]                   #or nick1,nick2:
												break
										
										for i in range(config.MAX_CONVERSATIONS):
											if (nick_sender in conversations[i] and nick_receiver in conversations[i]):
												conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5])) 
												break
											if(len(conversations[i]) == 0):
												conversations[i].append(nick_sender)
												conversations[i].append(nick_receiver)
												conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR+int(line[1:6][3:5]))
												break

						if(flag_comma == 0):
							rec = util.correctLastCharCR(line[line.find(">") + 1:line.find(", ")][1:])              

							if(rec == nick):
								send_time.append(line[1:6])
								if(nick_to_search != nick):
									for d in range(len(nicks)):
										if ((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):
											nick_receiver = conn_comp_list[d][0]
											break
									
									for i in range(config.MAX_CONVERSATIONS):
										if (nick_sender in conversations[i] and nick_receiver in conversations[i]): 
											conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR + int(line[1:6][3:5]))
											break
										if(len(conversations[i]) == 0):
											conversations[i].append(nick_sender)
											conversations[i].append(nick_receiver)
											conversations[i].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR + int(line[1:6][3:5]))
											break
		
	#Lines 212-290 consider all cases in which messages are addressed as - (nick1:nick2 or nick1,nick2 or nick1,nick2:) and stores their response times in conversations. conversations[i] contains all the response times between userA and userB throughout an entire year.

	for i in range(len(conversations)):       #Lines 295-297 remove the first two elements from every conversations[i] as they are the UIDS of sender and receiver respectively(and not RTs)
		if(len(conversations[i]) != 0):              # response times are calculated starting from index 2. So now we have all the response times in conversations.
			del conversations[i][0:2]

	for i in range(len(conversations)):
		if(len(conversations[i]) != 0):
			first = conversations[i][0]
			for j in range(1, len(conversations[i])):
					if(conversations[i][j]-conversations[i][j-1] > 9):

						conv.append(conversations[i][j-1] - first)    #We are recording the conversation length in conv and CRT in conv_diff. Here 9 is the average response
																																										#time we have already found before(see parser-RT.py). For every channel this value differs and would have to be changed in the code.
						conv_diff.append(conversations[i][j] - conversations[i][j-1])
						first = conversations[i][j]
					if(j == (len(conversations[i]) - 1)):
						conv.append(conversations[i][j] - first)                    
						break

	for i in range(max(conv)):
		graphx1.append(i)
		graphy1.append(conv.count(i))

	for i in range(max(conv_diff)):
		graphx2.append(i)
		graphy2.append(conv_diff.count(i))

#To plot CDF we store the CL and CRT values and their number of occurences as shown above.

	row_cl = zip(graphx1, graphy1)
	row_crt = zip(graphx2, graphy2)
	
	return row_cl, row_crt

def response_time(log_dict, nicks, nick_same_list):

	""" finds the response time of a message 
	i.e. the best guess for the time at which one can expect a reply for his/her message.

	Args:
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(List) : List of nickname created using nickTracker.py
		nick_same_list :List of same_nick names created using nickTracker.py
		output_directory (str): Location of output directory
		
	Returns:
	   rows_RT(zip List): Response Time (This refers to the response
		time of a message i.e. the best guess for the time at
		which one can expect a reply for his/her message)

	"""
	G = util.to_graph(nick_same_list)
	conn_comp_list = list(connected_components(G))

	util.create_connected_nick_list(conn_comp_list)
	
	graph_cumulative = []
	graph_x_axis = []
	graph_y_axis = []

	for day_content_all_channels in log_dict.values():
		for day_content in day_content_all_channels:
			day_log = day_content["log_data"]

			send_time = []  #list of all the times a user sends a message to another user
			meanstd_list = []
			totalmeanstd_list = []
			x_axis = []
			y_axis = []
			real_y_axis = []             
			conversations = [[] for i in range(config.MAX_RESPONSE_CONVERSATIONS)]

			#code for making relation map between clients       
			for line in day_log:
				flag_comma = 0
				if(util.check_if_msg_line (line)):
					nick_sender = ""
					nick_receiver = ""
					m = re.search(r"\<(.*?)\>", line)
					nick_to_search = util.correctLastCharCR(m.group(0)[1:-1])
					for d in range(len(nicks)):
						if((d < len(conn_comp_list)) and (nick_to_search in conn_comp_list[d])):
							nick_sender = conn_comp_list[d][0]
							break           
					for nick in nicks:
						rec_list = [e.strip() for e in line.split(':')]
						util.rec_list_splice(rec_list)

						if not rec_list[1]:
							break
						#for i in range(len(rec_list)):
							#if(rec_list[i]):
								#rec_list[i] = util.correctLastCharCR(rec_list[i])
						rec_list = util.correct_last_char_list(rec_list)		

						for name in rec_list:
							if(name == nick):
								send_time.append(line[1:6])
								if(nick_to_search != nick):  
									for d in range(len(nicks)):
										if((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):
											nick_receiver = conn_comp_list[d][0]
											break
										
									for i in range(config.MAX_RESPONSE_CONVERSATIONS):                                      
										if (nick_sender in conversations[i] and nick_receiver in conversations[i]):
											conversations[i].append(line[1:6])
											break
										if(len(conversations[i]) == 0):
											conversations[i].append(nick_sender)
											conversations[i].append(nick_receiver)
											conversations[i].append(line[1:6])
											break
							
						if "," in rec_list[1]: 
							flag_comma = 1
							rec_list_2 = [e.strip() for e in rec_list[1].split(',')]
							#for i in range(len(rec_list_2)):
								#if(rec_list_2[i]):
									#rec_list_2[i] = util.correctLastCharCR(rec_list_2[i])
							rec_list_2 = util.correct_last_char_list(rec_list_2)		
									
							for name in rec_list_2:
								if(name == nick):
									send_time.append(line[1:6])
									if(nick_to_search != nick):   
										for d in range(len(nicks)):
											if((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):
												nick_receiver = conn_comp_list[d][0]
												break
										
										for i in range(config.MAX_RESPONSE_CONVERSATIONS):
											if (nick_sender in conversations[i] and nick_receiver in conversations[i]):
												conversations[i].append(line[1:6]) 
												break
											if(len(conversations[i]) == 0):
												conversations[i].append(nick_sender)
												conversations[i].append(nick_receiver)
												conversations[i].append(line[1:6])
												break

						if(flag_comma == 0):
							rec = util.correctLastCharCR(line[line.find(">") + 1:line.find(", ")][1:])                   
							if(rec == nick):
								send_time.append(line[1:6])
								if(nick_to_search != nick):
									for d in range(len(nicks)):
										if ((d < len(conn_comp_list)) and (nick in conn_comp_list[d])):
											nick_receiver = conn_comp_list[d][0]
											break
									
									for i in range(config.MAX_RESPONSE_CONVERSATIONS):
										if (nick_sender in conversations[i] and nick_receiver in conversations[i]): 
											conversations[i].append(line[1:6])
											break
										if(len(conversations[i]) == 0):
											conversations[i].append(nick_sender)
											conversations[i].append(nick_receiver)
											conversations[i].append(line[1:6])
											break
			
			for i in range(config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[i]) != 0):  
					for j in range(2, len(conversations[i]) - 1):
						conversations[i][j]=(int(conversations[i][j+1][0:2])*config.MINS_PER_HOUR+int(conversations[i][j+1][3:5])) - (int(conversations[i][j][0:2])*config.MINS_PER_HOUR+int(conversations[i][j][3:5]))
	
			for i in range(config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[i]) != 0): 
					if(len(conversations[i]) == 3):
						conversations[i][2] = int(conversations[i][2][0:2])*config.MINS_PER_HOUR+int(conversations[i][2][3:5])     
					else: 
						del conversations[i][-1]

		#Explanation provided in parser-CL+CRT.py
			for i in range(config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[i]) != 0):
					for j in range(2, len(conversations[i])):
						totalmeanstd_list.append(conversations[i][j])

			if(len(totalmeanstd_list) != 0):
				for i in range(max(totalmeanstd_list) + 1):
					x_axis.append(i)

				for i in x_axis:
					y_axis.append(float(totalmeanstd_list.count(i)) / float(len(totalmeanstd_list)))
				
				#finding the probability of each RT to occur=No. of occurence/total occurences.
				real_y_axis.append(y_axis[0])
				for i in range(len(y_axis)):
					real_y_axis.append(float(real_y_axis[i-1]) + float(y_axis[i]))
			
			#to find cumulative just go on adding the current value to previously cumulated value till sum becomes 1 for last entry.
			for i in range(len(totalmeanstd_list)):
				graph_cumulative.append(totalmeanstd_list[i])

			if len(totalmeanstd_list) > 0:
				totalmeanstd_list.append(numpy.mean(totalmeanstd_list))
				totalmeanstd_list.append(numpy.mean(totalmeanstd_list)+2*numpy.std(totalmeanstd_list))
		
			for i in range(config.MAX_RESPONSE_CONVERSATIONS):
				if(len(conversations[i]) != 0):
					for j in range(2, len(conversations[i])):
						meanstd_list.append(conversations[i][j])
					conversations[i].append(numpy.mean(meanstd_list))
					conversations[i].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
					meanstd_list[:] = []

	graph_cumulative.sort()

	for i in range(graph_cumulative[len(graph_cumulative)-1] + 1):
		graph_y_axis.append(graph_cumulative.count(i))     # problem when ti=0 count is unexpectedly large
		graph_x_axis.append(i)
	

#Finally storing the RT values along with their frequencies in a csv file. 
	rows_rt = zip(graph_x_axis, graph_y_axis)

	return rows_rt
