import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText


def createNickChangesGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
 
 out_dir_nick_change = output_directory+"nick-changes/"

 print "Creating a new output folder"
 os.system("rm -rf "+out_dir_nick_change)
 os.system("mkdir "+out_dir_nick_change)

 rem_time= None #remembers the time of the last message of the file parsed before the current file

 for folderiterator in range(startingMonth, endingMonth + 1):
  temp1 = "0" if folderiterator < 10 else ""
  for fileiterator in range(1,32):
   temp2 = "0" if fileiterator < 10 else ""
   filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
   if not os.path.exists(filePath):
    if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
     print "[Error] Path "+filePath+" doesn't exist"
    continue 
   with open(filePath) as f:
       content = f.readlines() #contents stores all the lines of the file channel_name
     
   nicks = [] #list of all the nicknames     

   '''
    Getting all the nicknames in a list nicks[]
   '''
   for i in content:
    if(i[0] != '=' and "] <" in i and "> " in i):
     m = re.search(r"\<(.*?)\>", i)
     if m.group(0) not in nicks:                       
      nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

   for i in xrange(0,len(nicks)):
    nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
     
   for i in xrange(0,len(nicks)):
    nicks[i]=correctLastCharCR(nicks[i])

   for line in content:
    if(line[0]=='=' and "changed the topic of" not in line): #excluding the condition when user changes the topic. Search for only nick changes
     nick1=correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
     nick2=correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
     if nick1 not in nicks:
      nicks.append(nick1)
     if nick2 not in nicks:
      nicks.append(nick2)
    
   #print("printing nicks***********************************")
   #print(nicks)
     
   '''
    Forming list of lists for avoiding nickname duplicacy
   '''
   nick_same_list=[[] for i in range(len(nicks))] #list of list with each list having all the nicks for that particular person

   for line in content:
    if(line[0]=='=' and "changed the topic of" not in line):
     line1=line[line.find("=")+1:line.find(" is")][3:]
     line2=line[line.find("wn as")+1:line.find("\n")][5:]
     line1=correctLastCharCR(line1)
     line2=correctLastCharCR(line2)
     for i in range(5000):
      if line1 in nick_same_list[i] or line2 in nick_same_list[i]:
       nick_same_list[i].append(line1)
       nick_same_list[i].append(line2)
       break
      if not nick_same_list[i]:
       nick_same_list[i].append(line1)
       nick_same_list[i].append(line2)
       break

   #print("printing nick_same_list****************************")
   #print(nick_same_list)     

   '''=========================== Plotting the nickname changes graph =========================== '''

   graph_nickchanges=nx.MultiDiGraph()   #using networkx
   y=-1
   for i in content:
    y=y+1
    if(i[0] =='=' and "changed the topic of" not in i):  #excluding the condition when user changes the topic. Search for only nick changes
     nick1=correctLastCharCR(i[i.find("=")+1:i.find(" is")][3:])
     nick2=correctLastCharCR(i[i.find("wn as")+1:i.find("\n")][5:])
     z=y
     while z>=0:
      z=z-1
      if(content[z][0]!='='):
       graph_nickchanges.add_edge(nick1,nick2,weight=content[z][1:6])
       break                             # these lines extract the from-to nicknames and strip them appropriately to make 
     if(z==-1):
      graph_nickchanges.add_edge(nick1,nick2,weight=rem_time)                                            #edge between them  
   
   count=len(content)-1 #setting up the rem_time for next file, by noting the last message sent on that file.
   while(count>=0):
    if(content[count][0]!='='):
     rem_time=content[count][1:6]
     break
    count=count-1

   for u,v,d in graph_nickchanges.edges(data=True):
       d['label'] = d.get('weight','')

   output_file=out_dir_nick_change+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_nick_change.png"
   print "Generated "+ output_file
   A = nx.drawing.nx_agraph.to_agraph(graph_nickchanges)
   A.layout(prog='dot')
   A.draw(output_file) #graphviz helps to convert a dot file to PNG format for visualization
