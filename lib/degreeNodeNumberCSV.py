import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import csv
import math
import numpy as np
from numpy.random import normal
from scipy.optimize import curve_fit

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText


def degreeNodeNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):

 nodes_with_OUT_degree_per_day = []
 nodes_with_IN_degree_per_day = []
 nodes_with_TOTAL_degree_per_day = []

 max_degree_possible = 1000

 output_dir_degree = output_directory+"degreeNodeNumberCSV/"
 output_dir_degree_img = output_dir_degree + "individual-images/"
 output_file_out_degree = output_dir_degree + "node_no_out_degree.csv"
 output_file_in_degree = output_dir_degree + "node_no_in_degree.csv"
 output_file_total_degree = output_dir_degree + "node_no_total_degree.csv"


 print "Creating a new output folder"
 os.system("rm -rf "+output_dir_degree)
 os.system("mkdir "+output_dir_degree)

 os.system("rm -rf "+output_dir_degree_img)
 os.system("mkdir "+output_dir_degree_img)

 os.system("rm "+output_file_out_degree)
 os.system("touch "+output_file_out_degree)
 os.system("rm "+output_file_in_degree)
 os.system("touch "+output_file_in_degree)
 os.system("rm "+output_file_total_degree)
 os.system("touch "+output_file_total_degree)

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
   # output_file=out_dir_msg_num+channel_name+"_2013_"+str(folderiterator)+"_"+str(fileiterator)+"_msg_num.png"
   # print "Generated " + output_file
   # A = nx.drawing.nx_agraph.to_agraph(msg_num_graph)
   # A.layout(prog='dot')
   # A.draw(output_file)

   nodes_with_OUT_degree = [0]*max_degree_possible
   nodes_with_IN_degree = [0]*max_degree_possible
   nodes_with_TOTAL_degree = [0]*max_degree_possible

   print msg_num_graph.out_degree(), msg_num_graph.in_degree(), msg_num_graph.degree()
   print msg_num_graph.out_degree().values()
   print msg_num_graph.in_degree().values()
   print msg_num_graph.degree().values()

   for degree in msg_num_graph.out_degree().values():
    nodes_with_OUT_degree[degree]+=1

   for degree in msg_num_graph.in_degree().values():
    nodes_with_IN_degree[degree]+=1

   for degree in msg_num_graph.degree().values():
    nodes_with_TOTAL_degree[degree]+=1
   

   x_axis_log = [math.log(i) for i in xrange(1, 20)]#ignore degree 0
   y_axis_log = [math.log(i) if i>0 else 0 for i in nodes_with_TOTAL_degree[1:20] ]#ignore degree 0
   #plot1
   plt.plot(x_axis_log, y_axis_log) 
   #plot2
   plt.plot([1,2], [1,2])
   plt.xlabel("log(degree)")
   plt.ylabel("log(no_of_nodes)")

   plt.xticks(x_axis_log, ['log'+str(i) for i in xrange(1, len(x_axis_log))])
   plt.yticks(x_axis_log, ['log'+str(i) for i in xrange(1, len(x_axis_log))])

   plt.legend(['Required', 'y = x'], loc='upper left')

   # Save it in png and svg formats
   plt.savefig(output_dir_degree_img+"/total_out_degree"+str(folderiterator)+"-"+str(fileiterator)+".png")
   plt.close()

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

 sum_each_row = []
 for row in column_wise[3:]: #ignore degree 0 and text, starting from degree 1
  sum_each_row.append(sum(row[1:]))

 # print sum_each_row
 x_axis_log = [math.log(i) for i in xrange(1, 20)]#ignore degree 0
 y_axis_log = [math.log(i) if i>0 else 0 for i in sum_each_row[1:20] ]#ignore degree 0

 def func(x, a, b):
  return a - b*x
 
 parameter, covariance_matrix = curve_fit(func, x_axis_log, y_axis_log)

 a,b = parameter
 
 print a, b

 x = np.linspace(min(x_axis_log), max(x_axis_log), 1000)

 #plot1
 plt.plot(x_axis_log, y_axis_log, 'rx') 
 #plot2
 plt.plot(x, func(x, *parameter), 'b-', label='fit')
 plt.xlabel("log(degree)")
 plt.ylabel("log(no_of_nodes)")

 plt.xticks(x_axis_log, ['log'+str(i) for i in xrange(1, len(x_axis_log))])
 plt.yticks([math.log(i) for i in xrange(1, 100)], ['log'+str(i) for i in xrange(1, 100)])

 plt.legend(['Data', 'Curve Fit'], loc='upper left')

 # Save it in png and svg formats
 plt.savefig(output_dir_degree+"/total_graph_"+str(startingDate)+"-"+str(startingMonth)+"_"+str(endingDate)+"-"+str(endingMonth)+".png")
 plt.close()

 print output_dir_degree +"/total_graph_"+str(startingDate)+"-"+str(startingMonth)+"_"+str(endingDate)+"-"+str(endingMonth)+".png"