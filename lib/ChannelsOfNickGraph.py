import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText and inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText

def searchChannel(channel, channel_list):
 ans = -1
 i = 0
 for c_tuple in channel_list:
  if c_tuple[0] == channel:
   ans = i
   break
  i+=1 

 return ans

def createChannelsOfNickGraph(log_directory, output_directory, startingDate, startingMonth, endingDate, endingMonth):
 nick_channel_dict = []
 # nicks = []
 nick_same_list=[[] for i in range(100000)] #list of list with each list having all the nicks for that particular person
 out_dir_channel_user_time = output_directory+"channel-nick/"

 nicks_hash = []
 channels_hash = []
 users_on_channel = {}


 print "Creating a new output folder"
 os.system("rm -rf "+out_dir_channel_user_time)
 os.system("mkdir "+out_dir_channel_user_time)

 for folderiterator in range(startingMonth, endingMonth + 1):
  temp1 = "0" if folderiterator < 10 else ""
  for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate if folderiterator == endingMonth else 32):
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
     
     print "Working on " + filePath

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
      nicks[i] = correctLastCharCR(nicks[i])

     for line in content:
      if(line[0]=='=' and "changed the topic of" not in line):
       nick1=correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
       nick2=correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
       if nick1 not in nicks:
        nicks.append(nick1)
       if nick2 not in nicks:
        nicks.append(nick2)
      
     ''' Forming list of lists for avoiding nickname duplicacy '''  
     for line in content:
      if(line[0]=='=' and "changed the topic of" not in line):
       line1=line[line.find("=")+1:line.find(" is")][3:]
       line2=line[line.find("wn as")+1:line.find("\n")][5:]
       line1=correctLastCharCR(line1)
       line2=correctLastCharCR(line2)
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
 # print nick_same_list
 print nick_channel_dict
 
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

 print len(nicks_hash)
 print len(channels_hash)
 
 channel_user_graph = nx.Graph()

 for adjlist in nick_channel_dict:
  for channel in adjlist['channels']:
   channel_user_graph.add_edge(nicks_hash.index(adjlist['nickname']) ,channels_hash.index(channel[0]), weight=channel[1])
   # print nicks_hash.index(adjlist['nickname']),adjlist['nickname'], channels_hash.index(channel[0]),channel[0], channel[1]
   if users_on_channel.has_key(channel[0]):
    if adjlist['nickname'] not in users_on_channel[channel[0]]:
     users_on_channel[channel[0]].append(adjlist['nickname'])
   else:
    users_on_channel[channel[0]] = [adjlist['nickname']]

 CU_adjacency_matrix = nx.adjacency_matrix(channel_user_graph) #channel-user adj matrix
 print CU_adjacency_matrix
 print users_on_channel #used for channel-channel graph

 '''adj matrix for channel-channel'''

 CC_adjacency_matrix = [[0]*len(channels_hash) for i in xrange(0,  len(channels_hash))]

 # print len(channels_hash), len(users_on_channel.keys())
 for i in xrange(0, len(users_on_channel.keys())):
  for j in xrange(i+1, len(users_on_channel.keys())):
   common_users = list(set(users_on_channel[users_on_channel.keys()[i]]) & set(users_on_channel[users_on_channel.keys()[j]]))
   # print users_on_channel.keys()[i], users_on_channel.keys()[j], common_users
   CC_adjacency_matrix[i][j] = len(common_users)
   CC_adjacency_matrix[j][i] = len(common_users)

 print CC_adjacency_matrix #channel-user adj matrix
