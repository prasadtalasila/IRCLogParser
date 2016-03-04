import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/simpledirected/"

startingMonth = 11
endingMonth = 12

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText

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
   if(line[0]=='=' and "changed the topic of" not in line):
    nick1=correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
    nick2=correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
    if nick1 not in nicks:
     nicks.append(nick1)
    if nick2 not in nicks:
     nicks.append(nick2)
    
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

  '''
   Making relation map between client
  '''
  conversations=[[] for i in range(100)] #format of each list [num_messages,sender_nick,receiver_nick]

  for i in xrange(0,100):
   conversations[i].append(0)
  
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
   	  nick_sender=var
      
    for i in nicks:
     rec_list=[e.strip() for e in line.split(':')]
     rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
     rec_list[1]=rec_list[1][1:]
     if not rec_list[1]:
      break
     for x in xrange(0,len(rec_list)):
      if(rec_list[x]):
       rec_list[x] = correctLastCharCR(rec_list[x])
     for z in rec_list:
      if(z==i):
       if(var != i): 	
        for d in range(len(nicks)):
         if i in nick_same_list[d]:
       	  nick_receiver=nick_same_list[d][0]
       	  break
         else:
       	  nick_receiver=i
          
        for k in xrange(0,100):
         if (nick_sender in conversations[k] and nick_receiver in conversations[k]):
          if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
           conversations[k][0]=conversations[k][0]+1
           break
         if(len(conversations[k])==1):
          conversations[k].append(nick_sender)
          conversations[k].append(nick_receiver)
          conversations[k][0]=conversations[k][0]+1
          break
       
     if "," in rec_list[1]: 
      flag_comma = 1
      rec_list_2=[e.strip() for e in rec_list[1].split(',')]
      for y in xrange(0,len(rec_list_2)):
       if(rec_list_2[y]):
        rec_list_2[y] = correctLastCharCR(rec_list_2[y])
      for j in rec_list_2:
       if(j==i):
        if(var != i): 	
         for d in range(len(nicks)):
          if i in nick_same_list[d]:
       	   nick_receiver=nick_same_list[d][0]
       	   break
          else:
       	   nick_receiver=i
       	  
         for k in xrange(0,100):
          if (nick_sender in conversations[k] and nick_receiver in conversations[k]):
           if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
            conversations[k][0]=conversations[k][0]+1
            break
          if(len(conversations[k])==1):
           conversations[k].append(nick_sender)
           conversations[k].append(nick_receiver)
           conversations[k][0]=conversations[k][0]+1
           break

     if(flag_comma == 0):
      rec=line[line.find(">")+1:line.find(", ")][1:]
      rec = correctLastCharCR(rec)
      if(rec==i):
       if(var != i):
        for d in range(len(nicks)):
         if i in nick_same_list[d]:
       	  nick_receiver=nick_same_list[d][0]
       	  break
         else:
       	  nick_receiver=i
       	 
        for k in xrange(0,100):
         if (nick_sender in conversations[k] and nick_receiver in conversations[k]):	
          if (nick_sender == conversations[k][1] and nick_receiver == conversations[k][2]):
           conversations[k][0]=conversations[k][0]+1
           break
         if(len(conversations[k])==1):
          conversations[k].append(nick_sender)
          conversations[k].append(nick_receiver)
          conversations[k][0]=conversations[k][0]+1
          break
 
  msg_num_graph = nx.DiGraph()  #graph with multiple directed edges between clients used 

  for y in xrange(0,100):
   if(len(conversations[y])==3):
    msg_num_graph.add_edge(conversations[y][1],conversations[y][2],weight=conversations[y][0])	 

  for u,v,d in msg_num_graph.edges(data=True):
      d['label'] = d.get('weight','')
  output_file=output_directory+channel_name+"_"+str(fileiterator)+"_"+str(folderiterator)+"_2013_simpledirectedgraph.png"
  print "Generated " + output_file
  A = nx.drawing.nx_agraph.to_agraph(msg_num_graph)
  A.layout(prog='dot')
  A.draw(output_file)