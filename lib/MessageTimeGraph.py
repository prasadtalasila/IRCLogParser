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

def createMessageTimeGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
 
 out_dir_msg_time = output_directory+"message-time/"

 print "Creating a new output folder"
 os.system("rm -rf "+out_dir_msg_time)
 os.system("mkdir "+out_dir_msg_time)

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
    if(line[0]=='=' and "changed the topic of" not in line): #excluding the condition when user changes the topic. Search for only nick changes
     nick1=correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
     nick2=correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
     for i in range(len(nicks)):
      if nick1 in nick_same_list[i]:
       nick_same_list[i].append(nick1)
       nick_same_list[i].append(nick2)
       break
      if not nick_same_list[i]:
       nick_same_list[i].append(nick1)
       nick_same_list[i].append(nick2)
       break

   #print("printing nick_same_list****************************")
   #print(nick_same_list)     


   '''=========================== Plotting the conversation graph =========================== '''

   graph_conversation = nx.MultiDiGraph()  #graph with multiple directed edges between clients used
   for line in content:
    flag_comma = 0
    if(line[0] != '=' and "] <" in line and "> " in line):
     m = re.search(r"\<(.*?)\>", line)
     var = m.group(0)[1:-1]
     var = correctLastCharCR(var)
     for d in range(len(nicks)):
      if var in nick_same_list[d]:
       nick_sender = nick_same_list[d][0]
       break
      else:
       nick_sender = var
       
     for i in nicks:
      rec_list=[e.strip() for e in line.split(':')] #receiver list splited about :
      rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
      rec_list[1]=rec_list[1][1:]
      if not rec_list[1]: #index 0 will contain time 14:02
       break
      for k in xrange(0,len(rec_list)):
       if(rec_list[k]): #checking for \
        rec_list[k] = correctLastCharCR(rec_list[k])
      for z in rec_list:
       if(z==i):
        if(var != i):  
         for d in range(len(nicks)):
          if i in nick_same_list[d]:
           nick_receiver=nick_same_list[d][0]
           break
          else:
           nick_receiver=i
           
         graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])  
        
      if "," in rec_list[1]: #receiver list may of the form <Dhruv> Rohan, Ram :
       flag_comma = 1
       rec_list_2=[e.strip() for e in rec_list[1].split(',')]
       for y in xrange(0,len(rec_list_2)):
        if(rec_list_2[y]): #checking for \
         rec_list_2[y]=correctLastCharCR(rec_list_2[y])
       for j in rec_list_2:
        if(j==i):
         if(var != i):   
          for d in range(len(nicks)):
           if i in nick_same_list[d]:
            nick_receiver=nick_same_list[d][0]
            break
           else:
            nick_receiver=i
           
          graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])   

      if(flag_comma == 0): #receiver list can be <Dhruv> Rohan, Hi!
       rec=line[line.find(">")+1:line.find(", ")] 
       rec=rec[1:]
       rec=correctLastCharCR(rec)
       if(rec==i):
        if(var != i):
         for d in range(len(nicks)):
          if i in nick_same_list[d]:
           nick_receiver=nick_same_list[d][0]
           break
          else:
           nick_receiver=i
          
         graph_conversation.add_edge(nick_sender,nick_receiver,weight=line[1:6])  
       
   for u,v,d in graph_conversation.edges(data=True):
       d['label'] = d.get('weight','')
   output_file=out_dir_msg_time+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_msg_time.png"
   print "Generated " + output_file
   A = nx.drawing.nx_agraph.to_agraph(graph_conversation)
   A.layout(prog='dot')
   A.draw(output_file)
