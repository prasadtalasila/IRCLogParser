import re
import numpy
from networkx.algorithms.components.connected import connected_components
import lib.slack.util as util
import lib.slack.config as config


def conv_len_conv_refr_time(log_dict, nicks, nick_same_list, rt_cutoff_time, cutoff_percentile):

	""" Calculates the conversation length (CL) that is the length of time for which two users communicate 
	i.e. if a message is not replied to within Response Time(RT), 
	then it is considered as a part of another conversation.
	This function also calculates the conversation refresh time(CRT)
	For a pair of users, this is the time when one conversation ends and another one starts.
	Args:   
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(List) : list of nickname created using nickTracker.py
		nick_same_list :List of same_nick names created using nickTracker.py
		rt_cutoff_time (int) : Response Time (RT) cutoff to be used for CL and CRT calculations
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

	def build_conversation(rec_list, nick, send_time, nick_to_search,
						   nick_receiver, nick_sender, dateadd,
						   conversations, conn_comp_list, line):
		for names in rec_list:
			conversations, nick_receiver, send_time = \
				conv_helper(names, nick, send_time, nick_to_search,
							nick_receiver, nick_sender, dateadd,
							conversations, conn_comp_list, line)
		return  conversations, nick_receiver, send_time

	def conv_helper(rec, nick, send_time, nick_to_search, nick_receiver,
					nick_sender, dateadd, conversations, conn_comp_list, line):
		if(rec == nick):
			send_time.append(line[1:6])
			if(nick_to_search != nick):
				nick_receiver = util.get_nick_sen_rec(len(nicks), nick, conn_comp_list, nick_receiver)
				for i in range(config.MAX_CONVERSATIONS):
					if (nick_sender in conversations[i] and nick_receiver in conversations[i]):
						conversations = conv_append(conversations, i, dateadd, line)
						break
					if(len(conversations[i]) == 0):
						conversations[i].append(nick_sender)
						conversations[i].append(nick_receiver)
						conversations = conv_append(conversations, i, dateadd, line)
						break
		return  conversations, nick_receiver, send_time

	def conv_mat_diff(i,j,conversations):
		"""
		i(int): matrix index for row
		j(int): matrix index for column
		"""
		return (conversations[i][j]-conversations[i][j-1])

	def conv_append(conversations, index, dateadd, line):
		conversations[index].append(config.HOURS_PER_DAY*config.MINS_PER_HOUR*dateadd + int(line[1:6][0:2])*config.MINS_PER_HOUR + int(line[1:6][3:5]))
		return conversations

	def parse_log_lines_for_conv(log_dict, nicks, conn_comp_list, conversations):
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
						nick_sender = util.get_nick_sen_rec(len(nicks), nick_to_search, conn_comp_list, nick_sender)

						for nick in nicks:
							rec_list = [e.strip() for e in line.split(':')]
							util.rec_list_splice(rec_list)
							if not rec_list[2]:
								break
							rec_list = util.correct_last_char_list(rec_list)
							conversations, nick_receiver, send_time = \
								build_conversation(rec_list, nick, send_time,
												   nick_to_search, nick_receiver, nick_sender,
												   dateadd, conversations, conn_comp_list, line)

							if "," in rec_list[2]:
								flag_comma = 1
								rec_list_2 = [e.strip() for e in rec_list[2].split(',')]
								rec_list_2 = util.correct_last_char_list(rec_list_2)
								conversations, nick_receiver, send_time = \
									build_conversation(rec_list_2, nick, send_time,
													   nick_to_search, nick_receiver,
													   nick_sender, dateadd, conversations,
													   conn_comp_list, line)

							if(flag_comma == 0):
								rec = util.splice_find(line, ">", ", ", 1)
								conversations, nick_receiver, send_time	= \
									conv_helper(rec, nick, send_time, nick_to_search,
												nick_receiver, nick_sender, dateadd,
												conversations, conn_comp_list, line)

		return 	conversations, nick_receiver, send_time


	conversations, nick_receiver, send_time = parse_log_lines_for_conv(log_dict, nicks, conn_comp_list, conversations)

	# Consider all cases in which messages are addressed as - (nick1:nick2 or nick1,nick2
	# or nick1,nick2:) and stores their response times in conversations.
	# conversations[i] contains all the response times between userA and userB
	# throughout a chosen time period.

	for i in range(len(conversations)):
		#remove the first two elements from every conversations[i]
		# as they are the UIDS of sender and receiver respectively(and not RTs)
		if(len(conversations[i]) != 0):
			del conversations[i][0:2]

	for i in range(len(conversations)):
		if(len(conversations[i]) != 0):
			first = conversations[i][0]
			# response times are calculated starting from index 2.
			# So now we have all the response times in conversations.
			for j in range(1, len(conversations[i])):
					# We are recording the conversation length in conv and CRT in conv_diff.
					if(conv_mat_diff(i, j, conversations) > rt_cutoff_time):
						conv.append(conversations[i][j-1] - first)

						conv_diff.append(conv_mat_diff(i, j, conversations))
						first = conversations[i][j]
					if(j == (len(conversations[i]) - 1)):
						conv.append(conversations[i][j] - first)
						break
	#To plot CDF we store the CL and CRT values and their number of occurences
	row_cl = build_stat_dist(conv)
	row_crt = build_stat_dist(conv_diff)
	truncated_cl, cl_cutoff_time = truncate_table(row_cl, cutoff_percentile)
	truncated_crt, crt_cutoff_time = truncate_table(row_crt, cutoff_percentile)

	return truncated_cl, truncated_crt




def response_time(log_dict, nicks, nick_same_list, cutoff_percentile):

	""" finds the response time of a message 
	i.e. the best guess for the time at which one can expect a reply for his/her message.

	Args:
		log_dict (str): Dictionary of logs data created using reader.py
		nicks(List) : List of nickname created using nickTracker.py
		nick_same_list :List of same_nick names created using nickTracker.py
		cutoff_percentile (int): Cutoff percentile indicating statistical significance
		
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

	def build_mean_list(conversations, index, mean_list):
		for j in range(2, len(conversations[index])):
			mean_list.append(conversations[index][j])
		return mean_list

	def resp_helper(rec, nick, send_time, nick_to_search, nick_receiver, nick_sender, conversations, conn_comp_list):
		if(rec == nick):
			send_time.append(line[1:6])
			if(nick_to_search != nick):
				nick_receiver = util.get_nick_sen_rec(len(nicks), nick, conn_comp_list, nick_receiver)								
				for i in range(config.MAX_RESPONSE_CONVERSATIONS):
					if (nick_sender in conversations[i] and nick_receiver in conversations[i]): 
						conversations[i].append(line[1:6])
						break
					if(len(conversations[i]) == 0):
						conversations[i].append(nick_sender)
						conversations[i].append(nick_receiver)
						conversations[i].append(line[1:6])
						break		
		return conversations, nick_receiver, send_time				

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
					nick_sender = util.get_nick_sen_rec(len(nicks), nick_to_search, conn_comp_list, nick_sender)					         
					for nick in nicks:
						rec_list = [e.strip() for e in line.split(':')]
						util.rec_list_splice(rec_list)

						if not rec_list[2]:
							break						
						rec_list = util.correct_last_char_list(rec_list)		
						
						for name in rec_list:
							conversations, nick_receiver, send_time = resp_helper(name, nick, send_time, nick_to_search, nick_receiver, nick_sender, conversations, conn_comp_list)							
							
						if "," in rec_list[2]: 
							flag_comma = 1
							rec_list_2 = [e.strip() for e in rec_list[2].split(',')]							
							rec_list_2 = util.correct_last_char_list(rec_list_2)		
								
							for name in rec_list_2:
								conversations, nick_receiver, send_time = resp_helper(name, nick, send_time, nick_to_search, nick_receiver, nick_sender, conversations, conn_comp_list)								

						if(flag_comma == 0):
							rec = util.splice_find(line, ">", ", ",1)							
							conversations, nick_receiver, send_time = resp_helper(rec, nick, send_time, nick_to_search, nick_receiver, nick_sender, conversations, conn_comp_list)						
			
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
					totalmeanstd_list = build_mean_list(conversations, i, totalmeanstd_list)

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
					meanstd_list = build_mean_list(conversations, i, meanstd_list)					
					conversations[i].append(numpy.mean(meanstd_list))
					conversations[i].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
					meanstd_list[:] = []

	graph_cumulative.sort()

	truncated_rt = None
	rt_cutoff_time = None
	if graph_cumulative:
		for i in range(graph_cumulative[len(graph_cumulative)-1] + 1):
			graph_y_axis.append(graph_cumulative.count(i))     # problem when ti=0 count is unexpectedly large
			graph_x_axis.append(i)		

		#Finally storing the RT values along with their frequencies in a csv file; no need to invoke build_stat_dist() function
		rows_rt = zip(graph_x_axis, graph_y_axis)
		truncated_rt, rt_cutoff_time = truncate_table(rows_rt, cutoff_percentile)

		if config.CUTOFF_TIME_STRATEGY == "TWO_SIGMA":
			resp_time, resp_frequency_tuple = zip(*truncated_rt)
			resp_frequency = list(resp_frequency_tuple)
			rt_cutoff_time_frac = numpy.mean(resp_frequency) + 2*numpy.std(resp_frequency)
			rt_cutoff_time = int(numpy.ceil(rt_cutoff_time_frac))


	return truncated_rt, rt_cutoff_time


def build_stat_dist(number_list):
	"""
	Summarize a list into a statistical distribution.
	An empty input list generates an empty output list.

	Args:
		number_list (List): List containing positive integers

	Returns:
	   rows_table(zip List): A tuple with two items in each element,
	   in the (number, frequency) format
	"""
	# check for an empty input list
	if not number_list:
		return []

	graph_x = []
	graph_y = []
	for i in range(max(number_list)+1):
		graph_x.append(i)
		graph_y.append(number_list.count(i))

	#print zip(graph_x, graph_y)
	return zip(graph_x, graph_y)


def truncate_table(table, cutoff_percentile):

	"""
	The calculations of conversation characteristics, namely RT, CL and CRT, are
	based on the cutoff values estimated for RT and CL. This generic function takes
	a two column table and truncates the same to a required percentile value. Usually
	the RT followed by CL tables are processed through this function.
	cutoff_percentile (float) : Cutoff indicating the statistical significance of
	observations on conversation characteristics. The value is expressed as a
	floating point number.

	Args:
		table (zip List): List containing 2-tuple elements, ex: [(0,10),(1,5)]

	Returns:
   		truncated_table (zip List): A truncated version of table provided as input
   		argument. The table is truncated to the level of statistical significance
   		mentioned in the cutoff_percentile parameter.
   		cutoff_time (int): Cutoff time value corresponding to the chosen level of
   		statistical significance.

	"""
	truncated_table = None
	cutoff_time = None
	if table:
		times, values = zip(*table)
		total_value = 0
		for value in values:
			total_value = total_value + value

		index = 0
		cutoff_index = 0
		cumulative_value = 0
		while (index < len(values)):
			if (values[index] != 0):
				cumulative_value = cumulative_value + values[index]
				if (cumulative_value <= (1-cutoff_percentile/100.0) * total_value):
					cutoff_index = index
				else:
					break
			index = index + 1

		#slice counts the number of elements, which will be one greater than the index
		truncated_table = zip(times[:cutoff_index+1], values[:cutoff_index+1])
		cutoff_time = times[cutoff_index]

	return truncated_table, cutoff_time
