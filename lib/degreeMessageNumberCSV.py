import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import csv

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText

def degreeMessageNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):
 
 nodes_with_OUT_degree_per_day = []
 nodes_with_IN_degree_per_day = []
 nodes_with_TOTAL_degree_per_day = []

 max_degree_possible = 1000

 output_dir_degree = output_directory+"degreeMessageNumberCSV/"
 
 output_file_out_degree = output_dir_degree + "msg_no_out_degree.csv"
 output_file_in_degree = output_dir_degree + "msg_no_in_degree.csv"
 output_file_total_degree = output_dir_degree + "msg_no_total_degree.csv"


 print "Creating a new output folder"
 os.system("rm -rf "+output_dir_degree)
 os.system("mkdir "+output_dir_degree)

 os.system("rm "+output_file_out_degree)
 os.system("touch "+output_file_out_degree)
 os.system("rm "+output_file_in_degree)
 os.system("touch "+output_file_in_degree)
 os.system("rm "+output_file_total_degree)
 os.system("touch "+output_file_total_degree)

 rem_time= None #remembers the time of the last message of the file parsed before the current file

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
   # output_file_out_degree=out_dir_msg_time+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_msg_time.png"
   # print "Generated " + output_file_out_degree
   # A = nx.drawing.nx_agraph.to_agraph(graph_conversation)
   # A.layout(prog='dot')
   # A.draw(output_file_out_degree)
   nodes_with_OUT_degree = [0]*max_degree_possible
   nodes_with_IN_degree = [0]*max_degree_possible
   nodes_with_TOTAL_degree = [0]*max_degree_possible

   print graph_conversation.out_degree(), graph_conversation.in_degree(), graph_conversation.degree()
   print graph_conversation.out_degree().values()
   print graph_conversation.in_degree().values()
   print graph_conversation.degree().values()

   for degree in graph_conversation.out_degree().values():
    nodes_with_OUT_degree[degree]+=1

   for degree in graph_conversation.in_degree().values():
    nodes_with_IN_degree[degree]+=1

   for degree in graph_conversation.degree().values():
    nodes_with_TOTAL_degree[degree]+=1

   print "\n"
   nodes_with_OUT_degree.insert(0, sum(nodes_with_OUT_degree))
   nodes_with_OUT_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
   nodes_with_OUT_degree_per_day.append(nodes_with_OUT_degree)

   nodes_with_IN_degree.insert(0, sum(nodes_with_IN_degree))
   nodes_with_IN_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
   nodes_with_IN_degree_per_day.append(nodes_with_IN_degree)

   nodes_with_TOTAL_degree.insert(0, sum(nodes_with_TOTAL_degree))
   nodes_with_TOTAL_degree.insert(0, str(folderiterator)+"-"+str(fileiterator))
   nodes_with_TOTAL_degree_per_day.append(nodes_with_TOTAL_degree)

 # print nodes_with_OUT_degree_per_day
 # print nodes_with_IN_degree_per_day
 # print nodes_with_TOTAL_degree_per_day
 
 temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
 temp.insert(0, 'total')
 temp.insert(0, 'out-degree/day>')

 nodes_with_OUT_degree_per_day.insert(0, temp)
 column_wise = zip(*nodes_with_OUT_degree_per_day)
 with open(output_file_out_degree, 'wb') as myfile:
  wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
  for col in column_wise:
   wr.writerow(col)

 temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
 temp.insert(0, 'total')
 temp.insert(0, 'in-degree/day>')

 nodes_with_IN_degree_per_day.insert(0, temp)
 column_wise = zip(*nodes_with_IN_degree_per_day)
 with open(output_file_in_degree, 'wb') as myfile2:
  wr = csv.writer(myfile2, quoting=csv.QUOTE_ALL)
  for col in column_wise:
   wr.writerow(col)

 temp = ['deg'+str(i) for i in xrange(max_degree_possible)]
 temp.insert(0, 'total')
 temp.insert(0, 'degree/day>')

 nodes_with_TOTAL_degree_per_day.insert(0, temp)
 column_wise = zip(*nodes_with_TOTAL_degree_per_day)
 with open(output_file_total_degree, 'wb') as myfile3:
  wr = csv.writer(myfile3, quoting=csv.QUOTE_ALL)
  for col in column_wise:
   wr.writerow(col)

