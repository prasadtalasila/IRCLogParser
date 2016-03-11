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


def createAggregateGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth):
 nick_same_list=[[] for i in range(5000)]

 conversations=[[] for i in range(5000)]
 for i in xrange(0,5000):
  conversations[i].append(0)

 nicks = [] #list of all the nicknames
 aggregate_graph = nx.DiGraph()  #graph with multiple directed edges between clients used 

 for folderiterator in range(startingMonth, endingMonth+1):
  temp1 = "0" if folderiterator < 10 else ""
  for fileiterator in range(1,32):
   temp2 = "0" if fileiterator < 10 else ""
   filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
   if not os.path.exists(filePath):
    if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
     print "[Error] Path "+filePath+" doesn't exist"
    continue 
   with open(filePath) as f:
       content = f.readlines() #contents stores all the lines of the file channel_name                             #contents stores all the lines of the file kubunutu-devel   
  
   nicks_for_the_day = []
   print "Working on " + filePath 
   
   '''Getting all the nicknames in a list'''
   for i in content:
    if(i[0] != '=' and "] <" in i and "> " in i):
     m = re.search(r"\<(.*?)\>", i)
     if m.group(0) not in nicks_for_the_day:                       
      nicks_for_the_day.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

   for i in xrange(0,len(nicks_for_the_day)):
    if nicks_for_the_day[i][1:-1] not in nicks:
     nicks.append(nicks_for_the_day[i][1:-1])     #removed <> from the nicknames
     
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
       nick_same_list[i].append(line1)
       nick_same_list[i].append(line2)
       break
      if not nick_same_list[i]:
       nick_same_list[i].append(line1)
       nick_same_list[i].append(line2)
       break

   '''Making relation map between clients'''
   for line in content:
    flag_comma = 0
    if(line[0] != '=' and "] <" in line and "> " in line):
     m=re.search(r"\<(.*?)\>", line)
     var=m.group(0)[1:-1]
     var=correctLastCharCR(var)
     for d in range(5000):
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
      for k in xrange(0,len(rec_list)):
       if(rec_list[k]):
        rec_list[k]=correctLastCharCR(rec_list[k])
      for z in rec_list:
       if(z==i):
        if(var != i):  
         for d in range(5000):
          if i in nick_same_list[d]:
           nick_receiver=nick_same_list[d][0]
           break
          else:
           nick_receiver=i
           
         for r in xrange(0,5000):
          if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
           if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
            conversations[r][0]=conversations[r][0]+1
            break
          if(len(conversations[r])==1):
           conversations[r].append(nick_sender)
           conversations[r].append(nick_receiver)
           conversations[r][0]=conversations[r][0]+1
           break
        
      if "," in rec_list[1]: 
       flag_comma = 1
       rec_list_2=[e.strip() for e in rec_list[1].split(',')]
       for i in xrange(0,len(rec_list_2)):
        if(rec_list_2[i]):
         rec_list_2[i] = correctLastCharCR(rec_list_2[i])
       for j in rec_list_2:
        if(j==i):
         if(var != i):  
          for d in range(5000):
           if i in nick_same_list[d]:
            nick_receiver=nick_same_list[d][0]
            break
           else:
            nick_receiver=i
           
          for r in xrange(0,5000):
           if (nick_sender in conversations[r] and nick_receiver in conversations[r]):
            if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
             conversations[r][0]=conversations[r][0]+1
             break
           if(len(conversations[r])==1):
            conversations[r].append(nick_sender)
            conversations[r].append(nick_receiver)
            conversations[r][0]=conversations[r][0]+1
            break

      if(flag_comma == 0):
       rec=line[line.find(">")+1:line.find(", ")][1:]
       rec = correctLastCharCR(rec) 
       if(rec==i):
        if(var != i):
         for d in range(5000):
          if i in nick_same_list[d]:
           nick_receiver=nick_same_list[d][0]
           break
          else:
           nick_receiver=i
          
         for r in xrange(0,5000):
          if (nick_sender in conversations[r] and nick_receiver in conversations[r]): 
           if (nick_sender == conversations[r][1] and nick_receiver == conversations[r][2]):
            conversations[r][0]=conversations[r][0]+1
            break
          if(len(conversations[r])==1):
           conversations[r].append(nick_sender)
           conversations[r].append(nick_receiver)
           conversations[r][0]=conversations[r][0]+1
           break

   for index in xrange(0,5000):
    if(len(conversations[index])==3):
     aggregate_graph.add_edge(conversations[index][1],conversations[index][2],weight=conversations[index][0])  

 # print("========> nicks")
 # print(nicks)
 # print("========> nick_same_list")
 # print(nick_same_list)
 # print("========> conversations")
 # print(conversations)

 for u,v,d in aggregate_graph.edges(data=True):
     d['label'] = d.get('weight','')

 output_file=output_directory+channel_name+"_2013_"+str(startingMonth)+"_"+str(endingMonth)+"_aggregategraph.png"
 print "Generating "+output_file
 print "Please wait ...."

 A = nx.drawing.nx_agraph.to_agraph(aggregate_graph)
 A.layout(prog='dot')
 A.draw(output_file)
 print("Done Generating")


