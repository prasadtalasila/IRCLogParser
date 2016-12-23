import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import ext.util

def searchChannel(channel, channel_list):
	ans = -1
	i = 0
	for c_tuple in channel_list:
		if c_tuple[0] == channel:
			ans = i
			break
		i+=1 
	return ans

def createChannelsOfNickGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
	nick_channel_dict = []
	nick_same_list=[[] for i in range(100000)] #list of list with each list having all the nicks for that particular person

	nicks_hash = []
	channels_hash = []
	users_on_channel = {}
	channel_for_users_for_all_days = []
	channel_for_user_for_the_day = {}

	# out_dir_channel_user_time = output_directory+"channel-nick/"
	out_dir_channel_user_time = output_directory
	if not os.path.exists(os.path.dirname(out_dir_channel_user_time)):
		try:
			os.makedirs(os.path.dirname(out_dir_channel_user_time))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	for folderiterator in range(startingMonth, endingMonth + 1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			if not ((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )):
				for channel_searched in os.listdir(log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"):
					channel_searched = channel_searched[:-4]
					filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_searched+".txt"   
					if not os.path.exists(filePath):
						print "[Error] Path "+filePath+" doesn't exist"
						continue 
					with open(filePath) as f:
						content = f.readlines() #contents stores all the lines of the file channel_searched
					
					#print "Working on " + filePath

					nicks = [] #list of all the nicknames     

					'''Getting all the nicknames in a list'''
					for i in content:
						if(i[0] != '=' and "] <" in i and "> " in i):
							m = re.search(r"\<(.*?)\>", i)
							if m.group(0) not in nicks:                       
								nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

					for i in xrange(0,len(nicks)):
						nicks[i] = nicks[i][1:-1]   #removed <> from the nicknames
							
					for i in xrange(0,len(nicks)):
						nicks[i] = ext.util.correctLastCharCR(nicks[i])

					for line in content:
						if(line[0]=='=' and "changed the topic of" not in line):
							nick1=ext.util.correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
							nick2=ext.util.correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
							if nick1 not in nicks:
								nicks.append(nick1)
							if nick2 not in nicks:
								nicks.append(nick2)
						
					''' Forming list of lists for avoiding nickname duplicacy '''  
					for line in content:
						if(line[0]=='=' and "changed the topic of" not in line):
							line1=line[line.find("=")+1:line.find(" is")][3:]
							line2=line[line.find("wn as")+1:line.find("\n")][5:]
							line1=ext.util.correctLastCharCR(line1)
							line2=ext.util.correctLastCharCR(line2)
							for i in range(5000):
								if line1 in nick_same_list[i] or line2 in nick_same_list[i]:
									if line1 not in nick_same_list[i]:
										nick_same_list[i].append(line1)
									if line2 not in nick_same_list[i]:
										nick_same_list[i].append(line2)
									break
								if not nick_same_list[i]:
									if line1 not in nick_same_list[i]:
										nick_same_list[i].append(line1)
									if line2 not in nick_same_list[i]:
										nick_same_list[i].append(line2)
									break

					'''
						Creating list of dictionaries nick_channel_dict of the format : [{'nickname':'rohan', 'channels':['[#abc', 0],['#bcd', 0]]},{}]
					# '''
					# print nicks
					done = []
					for d in range(len(nicks)): 
						var = nicks[d]
						f = 1
						for x in nick_same_list:
							if var in x:
								user_nick = x[0]
								f = 0
								break
						if f:
							user_nick = var

						'''for channels of user on a day'''
						# print channel_searched, user_nick
						if channel_for_user_for_the_day.has_key(user_nick) and channel_searched not in channel_for_user_for_the_day[user_nick]:
							channel_for_user_for_the_day[user_nick].append(channel_searched)
						else:
							channel_for_user_for_the_day[user_nick] = [channel_searched]

						# print user_nick
						flag = 1
						for dictionary in nick_channel_dict:
							if dictionary['nickname'] == user_nick and user_nick not in done:
								# print user_nick, done
								# if channel_searched not in dictionary['channels']:
								index = searchChannel(channel_searched, dictionary['channels'])
								if index == -1:
									dictionary['channels'].append([channel_searched,1])
								else:
									dictionary['channels'][index][1]+=1
								flag = 0
								done.append(user_nick)
								break
						if flag:
							nick_channel_dict.append({'nickname':user_nick, 'channels': [[channel_searched, 1]]})
							done.append(user_nick)

				# print "checking", fileiterator, folderiterator
				# print channel_for_user_for_the_day
				channel_for_users_for_all_days.append(channel_for_user_for_the_day)
				channel_for_user_for_the_day = {}#empty for next day usage

	# print nick_same_list
	# print nick_channel_dict
	
	# myGraph = nx.DiGraph()
	# for dicts in nick_channel_dict:
	#  # print dicts
	#  # no_of_channels = 0
	#  nick = dicts['nickname']
	#  if nick not in nicks_hash:
	#   nicks_hash.append(nick)

	#  for channel in dicts['channels']:
	#   if channel[1] > 20:
	#    myGraph.add_edge(nick ,channel[0],weight=channel[1])
	#   if channel[0] not in channels_hash:
	#    channels_hash.append(channel[0])
	#   # no_of_channels+=1
	#   # print dicts

	# for u,v,d in myGraph.edges(data=True):
	#  d['label'] = d.get('weight','')

	# output_file=out_dir_channel_user_time+"_channels-of-nick-graph.png"
	# print "Generating "+output_file

	# A = nx.drawing.nx_agraph.to_agraph(myGraph)
	# A.layout(prog='dot')
	# A.draw(output_file) 

	'''!!!!!!!!!!!! Reptition if use above!!!!!!!!!!!!!!!!! '''

	for dicts in nick_channel_dict:
		nick = dicts['nickname']
		if nick not in nicks_hash:
			nicks_hash.append(nick)

		for channel in dicts['channels']:
			if channel[0] not in channels_hash:
				channels_hash.append(channel[0])

	# print len(nicks_hash)
	# print len(channels_hash)
	
	channel_user_graph = nx.Graph()
	# # myGraph = nx.DiGraph() #directed

	CU_adjacency_matrix = [[0]*len(nicks_hash) for i in xrange(0,  len(channels_hash))]
	temp2 = []
	for adjlist in nick_channel_dict:
		for channel in adjlist['channels']:
			# channel_user_graph.add_edge(nicks_hash.index(adjlist['nickname']) ,(1000000+channels_hash.index(channel[0])), weight=channel[1])
	#   # print nicks_hash.index(adjlist['nickname']),adjlist['nickname'], channels_hash.index(channel[0]),channel[0], channel[1]
			# CU_adjacency_matrix[channels_hash.index(channel[0])][nicks_hash.index(adjlist['nickname'])] = channel[1]
			# print adjlist['nickname'], channel[0]
			# channel_user_graph.add_edge(adjlist['nickname'], channel[0], weight=int(channel[1]))
	#   # if channel[1] > 25 :
	#    # print str(nicks_hash.index(adjlist['nickname']))+"\t"+str(1000000+channels_hash.index(channel[0]))
			if users_on_channel.has_key(channel[0]):
				if adjlist['nickname'] not in users_on_channel[channel[0]]:
					users_on_channel[channel[0]].append(adjlist['nickname'])
			else:
				users_on_channel[channel[0]] = [adjlist['nickname']]

	# # # CU_adjacency_matrix = nx.adjacency_matrix(channel_user_graph) #channel-user adj matrix
	
	# # # print "CU Adj Matrix", CU_adjacency_matrix  #channel-user adj matrix
	# # # print users_on_channel #used for channel-channel graph
	# # # print "Saving CU Adjacency Matrix"
	# # # np.savetxt(output_directory+"/CU_adjacency_matrix_"+str(startingMonth)+"_"+str(endingMonth)+"_.csv", CU_adjacency_matrix, delimiter=",")
	print "Reduced CU Adjacency Matrix will be saved"
	nx.write_pajek(channel_user_graph, "adjCU.net")
	print "saved CU .net"
	# channel_channel_graph = nx.Graph()

	# '''adj matrix for channel-channel'''

	# CC_adjacency_matrix = [[0]*len(channels_hash) for i in xrange(0,  len(channels_hash))]

	# print len(channels_hash), len(users_on_channel.keys())
	# for i in xrange(0, len(channels_hash)):
	#  for j in xrange(i+1, len(channels_hash)):
	#   common_users = list(set(users_on_channel[channels_hash[i]]) & set(users_on_channel[channels_hash[j]]))
	#   # print channels_hash[i]
	#   # print users_on_channel.keys()[i], users_on_channel.keys()[j], common_users
	#   # CC_adjacency_matrix[i][j] = len(common_users)
	#   # CC_adjacency_matrix[j][i] = len(common_users)
	#   # if len(common_users) > 0:
	#   	# myGraph.add_edge(users_on_channel.keys()[i] ,users_on_channel.keys()[j], weight=len(common_users))
	#   	# myGraph.add_edge(users_on_channel.keys()[j] ,users_on_channel.keys()[i], weight=len(common_users))
	#   if len(common_users) > 0:
	#   	# print str(channels_hash.index(users_on_channel.keys()[i]))+"\t"+str(channels_hash.index(users_on_channel.keys()[j]))
	#   # "Uncomment for directed version"
	#   # print str(channels_hash.index(users_on_channel.keys()[j]))+"\t"+str(channels_hash.index(users_on_channel.keys()[i]))
	#   	# print channels_hash[i],channels_hash[j]
	#   	channel_channel_graph.add_edge(channels_hash[i] ,channels_hash[j], weight=len(common_users))

	# # print "CC Adj Matrix", CC_adjacency_matrix #channel-channel adj matrix
	# # print "Saving CC Adjacency Matrix"
	# # # np.savetxt(output_directory+"/CC_adjacency_matrix_"+str(startingMonth)+"_"+str(endingMonth)+"_.csv", CC_adjacency_matrix, delimiter=",")
	# # # print "Done!"
	# print "Reduced CC Adjacency Matrix will be saved"
	# nx.write_pajek(channel_channel_graph, "adjCC.net")
	# print "saved CC .net"
	user_user_graph = nx.Graph()

	# '''adj matrix for user-user'''
	UU_adjacency_matrix = [[0]*len(nicks_hash) for i in xrange(0,  len(nicks_hash))]

	# # print channel_for_users_for_all_days
	for user_channel_dict in channel_for_users_for_all_days:
	#  # user_channel_dict format : {nick : [channels on that day], }
		for i in xrange(0, len(user_channel_dict.keys())):
			for j in xrange(i+1, len(user_channel_dict.keys())):
				common_channels_on_that_day = list(set(user_channel_dict[user_channel_dict.keys()[i]]) & set(user_channel_dict[user_channel_dict.keys()[j]]))
	#    # print "common_channels_on_that_day"
	#    # print user_channel_dict.keys()[i], user_channel_dict.keys()[j], common_channels_on_that_day
				user1 = user_channel_dict.keys()[i]
				user2 = user_channel_dict.keys()[j]
				no_of_common_channels_day = len(common_channels_on_that_day)

				# if not user_user_graph.has_edge(user1, user2):
				#  user_user_graph.add_edge(user1 ,user2, weight=0)
				#  user_user_graph.add_edge(user2 ,user1, weight=0)
					
				# user_user_graph[user1][user2]['weight'] += no_of_common_channels_day
				# user_user_graph[user2][user1]['weight'] += no_of_common_channels_day

				# print str(nicks_hash.index(user1))+"\t"+str(nicks_hash.index(user2))
	#    # "Uncomment for directed version"
	#    # print str(nicks_hash.index(user2))+"\t"+str(nicks_hash.index(user1))
				
	#    # print user1, user2
				UU_adjacency_matrix[nicks_hash.index(user1)][nicks_hash.index(user2)] += no_of_common_channels_day
				UU_adjacency_matrix[nicks_hash.index(user2)][nicks_hash.index(user1)] += no_of_common_channels_day

	for i in range(len(nicks_hash)):
		for j in range(i):
			if UU_adjacency_matrix[i][j] > 0:
				# print str(i)+'\t'+str(j)
				user_user_graph.add_edge(i ,j, weight=UU_adjacency_matrix[i][j])

	# print "UU Adj Matrix", UU_adjacency_matrix #user-user matrix
	# print "Saving UU Adjacency Matrix"
	# np.savetxt(output_directory+"/UU_adjacency_matrix_"+str(startingMonth)+"_"+str(endingMonth)+"_.csv", UU_adjacency_matrix, delimiter=",")
	print "Reduced UU Adjacency Matrix will be saved"
	nx.write_pajek(user_user_graph, "adjUU.net")
	print "saved UU .net"

	# output_file=out_dir_channel_user_time+"_channels-of-nick-graph.png"
	# print "Generating "+output_file
	# max_degree_possible = 10000

	# nodes_with_OUT_degree = [0]*max_degree_possible
	# nodes_with_IN_degree = [0]*max_degree_possible
	# nodes_with_TOTAL_degree = [0]*max_degree_possible
	
	# print myGraph.out_degree().values()

	# for degree in myGraph.out_degree().values():
	#  if not degree < max_degree_possible:
	#   print "===error", degree
	#  nodes_with_OUT_degree[degree]+=1

	# for degree in myGraph.in_degree().values():
	#  if not degree < max_degree_possible:
	#   print "===error", degree
	#  nodes_with_IN_degree[degree]+=1

	# for degree in myGraph.degree().values():
	#  if not degree < max_degree_possible:
	#   print "===error", degree
	#  nodes_with_TOTAL_degree[degree]+=1

	# print "========= OUT DEGREE ======="
	# for i in xrange(max_degree_possible):
	#  print "deg"+str(i)+'\t'+str(nodes_with_OUT_degree[i])

	# print "========= IN DEGREE ======="
	# for i in xrange(max_degree_possible):
	#  print "deg"+str(i)+'\t'+str(nodes_with_IN_degree[i])

	# print "========= TOTAL DEGREE ======="
	# for i in xrange(max_degree_possible):
		# print "deg"+str(i)+'\t'+str(nodes_with_TOTAL_degree[i])

	'''
		We have around 20k users and most of them just visit a channel once, 
		hence we filter out the top 100 users
		This inturns reduces the CU and UU matrices
	'''

	'''
		calculate top <how_many_top_users> users
		this is achieved by taking top users from CU matrix on the basis of the column sum (total number of days active on a channel)
	# '''
	# how_many_top_users = 100

	# '''
	#  we also need to filter the channels and are filtered on the basis of row sum of CC matrix
	# '''
	# how_many_top_channels = 30

	# sum_for_each_channel = []
	# for channel_row in CC_adjacency_matrix:
	#  sum_for_each_channel.append(sum(channel_row))

	# #filter out top <how_many_top_channels> indices
	# top_indices_channels = sorted(range(len(sum_for_each_channel)), key=lambda i: sum_for_each_channel[i], reverse=True)[:how_many_top_channels]
	# indices_to_delete_channels = list(set([i for i in xrange(0, len(channels_hash))]) - set(top_indices_channels))

	# temp_channels = np.delete(CC_adjacency_matrix, indices_to_delete_channels, 1) #delete columns
	# reduced_CC_adjacency_matrix = np.delete(temp_channels, indices_to_delete_channels, 0) #delete rows
	# print "Saving Reduced CC Adjacency Matrix"
	# np.savetxt(output_directory+"/"+str(startingMonth)+"_"+str(endingMonth)+"reduced_CC_adjacency_matrix.csv", reduced_CC_adjacency_matrix, delimiter=",")
	# print "Done!"

	# #to calculate sum first take the transpose of CU matrix so users in row
	# UC_adjacency_matrix = zip(*CU_adjacency_matrix)
	# sum_for_each_user = []


	# for user_row in UC_adjacency_matrix:
	#  sum_for_each_user.append(sum(user_row))

	# #filter out top <how_many_top_users> indices
	# top_indices_users = sorted(range(len(sum_for_each_user)), key=lambda i: sum_for_each_user[i], reverse=True)[:how_many_top_users]
	# indices_to_delete_users = list(set([i for i in xrange(0, len(nicks_hash))]) - set(top_indices_users))

	# # print len(top_indices_users), top_indices_users
	# # print len(indices_to_delete_users), indices_to_delete_users

	# #update the nick_hash, channel_hash
	# reduced_nick_hash = np.delete(nicks_hash, indices_to_delete_users)
	# reduced_channel_hash = np.delete(channels_hash, indices_to_delete_channels)


	# #update the CU matrix by deleting particular columns, and rows which are not in top_indices_users, channels
	# temp_user_channel = np.delete(CU_adjacency_matrix, indices_to_delete_users, 1) #delete columns
	# reduced_CU_adjacency_matrix = np.delete(temp_user_channel, indices_to_delete_channels, 0) #delete rows

	# print "Saving Reduced CU Adjacency Matrix"
	# np.savetxt(output_directory+"/"+str(startingMonth)+"_"+str(endingMonth)+"reduced_CU_adjacency_matrix.csv", reduced_CU_adjacency_matrix, delimiter=",")
	# print "Done!"

	# #update the UU matrix by deleting both columns and rows
	# temp_users = np.delete(UU_adjacency_matrix, indices_to_delete_users, 1) #delete columns
	# reduced_UU_adjacency_matrix = np.delete(temp_users, indices_to_delete_users, 0) #delete rows
	# print "Saving Reduced UU Adjacency Matrix"
	# np.savetxt(output_directory+"/"+str(startingMonth)+"_"+str(endingMonth)+"reduced_UU_adjacency_matrix.csv", reduced_UU_adjacency_matrix, delimiter=",")
	# print "Done!"


	# print "=================================================="

	# print "========= REDUCED NICK HASH ========="
	# for i in range(len(reduced_nick_hash)):
	#  print str(i)+"\t"+reduced_nick_hash[i]
	
	# print "========= REDUCED CHANNEL HASH ========="
	# for i in range(len(reduced_channel_hash)):
	#  print str(1000000+i)+"\t"+reduced_channel_hash[i]