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


def findResponseTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):

 out_dir_msg_num = output_directory+"RT/"
 nick_same_list=[[] for i in range(7000)]
 nicks = [] #list of all the nicknames
 conv = []
 conv_diff = []
 # print "Creating a new output folder"
 # os.system("rm -rf "+out_dir_msg_num)
 # os.system("mkdir "+out_dir_msg_num)

 for folderiterator in range(startingMonth, endingMonth + 1):
  temp1 = "0" if folderiterator < 10 else ""
  for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate if folderiterator == endingMonth else 32):
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



 G = to_graph(nick_same_list)
 L = connected_components(G)

 

 for i in range(1,len(L)+1):
  L[i-1] = [i]+L[i-1]



 graph_to_sir = []
 graph_x_axis = []
 graph_y_axis = []
 graphx1 =[]
 graphy1 =[]
 graphx2 =[]
 graphy2 =[]
 #2,3
 dateadd=-1
 
 for folderiterator in range(startingMonth, endingMonth + 1):
  temp1 = "0" if folderiterator < 10 else ""
  for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate if folderiterator == endingMonth else 32):
   temp2 = "0" if fileiterator < 10 else ""
   filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
   if not os.path.exists(filePath):
    if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
     print "[Error] Path "+filePath+" doesn't exist"
    continue 
   with open(filePath) as f:
       content = f.readlines() #contents stores all the lines of the file channel_name  dateadd=dateadd+1
   send_time = [] #list of all the times a user sends a message to another user
   meanstd_list = []
   totalmeanstd_list = []
   x_axis = []
   y_axis = []
   real_y_axis = []
   time_in_min = [[] for i in range(1000)]
   
   print(filePath)

   conversations=[[] for i in range(200)]   

  

 #code for making relation map between clients


  

  
   for line in content:
    flag_comma = 0
    if(line[0] != '=' and "] <" in line and "> " in line):
     m = re.search(r"\<(.*?)\>", line)
     var = m.group(0)[1:-1]
     var=correctLastCharCR(var)
     for d in range(len(nicks)):
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
        rec_list[ik]=correctLastCharCR(rec_list[ik])
      for z in rec_list:
       if(z==i):
        send_time.append(line[1:6])
        if(var != i):  
         for d in range(len(nicks)):
          if((d<len(L)) and (i in L[d])):
           nick_receiver=L[d][0]
           break
          
         for rt in xrange(0,200):
          if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
           conversations[rt].append(line[1:6])
           break
          if(len(conversations[rt])==0):
           conversations[rt].append(nick_sender)
           conversations[rt].append(nick_receiver)
           conversations[rt].append(line[1:6])
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
           if((d<len(L)) and (i in L[d])):
            nick_receiver=L[d][0]
            break
          
          for rt in xrange(0,200):
           if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]):
            conversations[rt].append(line[1:6]) 
            break
           if(len(conversations[rt])==0):
            conversations[rt].append(nick_sender)
            conversations[rt].append(nick_receiver)
            conversations[rt].append(line[1:6])
            break

      if(flag_comma == 0):
       rec=line[line.find(">")+1:line.find(", ")] 
       rec=rec[1:]
       rec=correctLastCharCR(rec)
       if(rec==i):
        send_time.append(line[1:6])
        if(var != i):
         for d in range(len(nicks)):
          if ((d<len(L)) and (i in L[d])):
           nick_receiver=L[d][0]
           break
         
         for rt in xrange(0,200):
          if (nick_sender in conversations[rt] and nick_receiver in conversations[rt]): 
           conversations[rt].append(line[1:6])
           break
          if(len(conversations[rt])==0):
           conversations[rt].append(nick_sender)
           conversations[rt].append(nick_receiver)
           conversations[rt].append(line[1:6])
           break
  


     
   for index in range(0,200):
    if(len(conversations[index])!=0):  
     for index1 in range(2,len(conversations[index])-1):
      conversations[index][index1]=(int(conversations[index][index1+1][0:2])*60+int(conversations[index][index1+1][3:5])) - (int(conversations[index][index1][0:2])*60+int(conversations[index][index1][3:5]))
 

  
   for index in range(0,200):
    if(len(conversations[index])!=0): 
     if(len(conversations[index])==3):
      conversations[index][2] = int(conversations[index][2][0:2])*60+int(conversations[index][2][3:5])     
     else: 
      del conversations[index][-1]

  
  #Explanation provided in parser-CL+CRT.py

   for index in range(0,200):
    if(len(conversations[index])!=0):
     for index1 in range(2,len(conversations[index])):
      totalmeanstd_list.append(conversations[index][index1])

   if(len(totalmeanstd_list)!=0):

    for iy in range(0, max(totalmeanstd_list)+1):
     x_axis.append(iy)

   

    for ui in x_axis:
     y_axis.append(float(totalmeanstd_list.count(ui))/float(len(totalmeanstd_list)))
   #finding the probability of each RT to occur=No. of occurence/total occurences.


    real_y_axis.append(y_axis[0])
    for ix in range(1, len(y_axis)):
     real_y_axis.append(float(real_y_axis[ix-1])+float(y_axis[ix]))
#to find cumulative just go on adding the current value to previously cumulated value till sum becomes 1 for last entry.
   for hi in range(0,len(totalmeanstd_list)):
    graph_to_sir.append(totalmeanstd_list[hi])


   totalmeanstd_list.append(numpy.mean(totalmeanstd_list))
   totalmeanstd_list.append(numpy.mean(totalmeanstd_list)+2*numpy.std(totalmeanstd_list))

  
  
   for index in range(0,200):
    if(len(conversations[index])!=0):
     for index1 in range(2,len(conversations[index])):
      meanstd_list.append(conversations[index][index1])
     conversations[index].append(numpy.mean(meanstd_list))
     conversations[index].append(numpy.mean(meanstd_list)+(2*numpy.std(meanstd_list)))
     meanstd_list[:] = []

  

  #print("Conversation RT Info")
  #print(conversations)
 
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


 # print(graph_y_axis)
#print(graph_x_axis)
#print(len(graph_y_axis))
#print(len(graph_x_axis))

#Finally storing the RT values along with their frequencies in a csv file. 
 rows = zip(graph_x_axis,graph_y_axis)
 filename=out_dir_msg_num+channel_name+"_"+str(startingMonth)+"-"+str(startingDate)+"_"+str(endingMonth)+"-"+str(endingDate)+"_RT.csv"
 with open(filename, 'a+') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for row in rows:
      wr.writerow(row)



