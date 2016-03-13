import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import numpy
import datetime
import time
import pandas as pd
#added some new libraries
rem_time= None
for iterator in range(1,5):
 for fileiterator in range(1,5):
  if(fileiterator<10):	
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0"	
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
  else:
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"	
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
  if not os.path.exists(sttring):
   continue 
  with open(sttring) as f:
      content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel
  	
  nicks = [] #list of all the nicknames
  send_time = [] #list of all the times a user sends a message to another user
  nickplots = [] #nickplots stores all those nicks from nicks[] list that do not have zero in and outdegree in our conversation graph
  indegree = [] #this list stores all the indegree corresponding to a particular nick
  outdegree = [] #this list stores all the outdegree corresponding to a particular nick
  channel= "#kubuntu-devel" #channel name
    	
  
#code for getting all the nicknames in a list
  for i in content:
   if(i[0] != '=' and "] <" in i and "> " in i):
    m = re.search(r"\<(.*?)\>", i)
    if m.group(0) not in nicks:                       
     nicks.append(m.group(0))  	#used regex to get the string between <> and appended it to the nicks list



  for i in xrange(0,len(nicks)):
   nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
    
  for i in xrange(0,len(nicks)):
   if(nicks[i][len(nicks[i])-1]=='\\'):
    nicks[i]=nicks[i][:-1]
    nicks[i]=nicks[i]+'CR'

  for j in content:
   if(j[0]=='=' and "changed the topic of" not in j):
    line1=j[j.find("=")+1:j.find(" is")]
    line2=j[j.find("wn as")+1:j.find("\n")]
    line1=line1[3:]
    line2=line2[5:]
    if(line1[len(line1)-1]=='\\'):
     line1=line1[:-1]
     line1=line1 + 'CR' 
    if(line2[len(line2)-1]=='\\'):
     line2=line2[:-1]
     line2=line2 + 'CR'
    if line1 not in nicks:
     nicks.append(line1)
    if line2 not in nicks:
     nicks.append(line2)
   
  #print("printing nicks***********************************")
  #print(nicks)
    
 #code for forming list of lists for avoiding nickname duplicacy

  x=[[] for i in range(len(nicks))]
  for line in content:
   if(line[0]=='=' and "changed the topic of" not in line):
    line1=line[line.find("=")+1:line.find(" is")]
    line2=line[line.find("wn as")+1:line.find("\n")]
    line1=line1[3:]
    line2=line2[5:]
    if(line1[len(line1)-1]=='\\'):
     line1=line1[:-1]
     line1=line1 + 'CR' 
    if(line2[len(line2)-1]=='\\'):
     line2=line2[:-1]
     line2=line2 + 'CR'
    for i in range(len(nicks)):
     if line1 in x[i]:
      x[i].append(line1)
      x[i].append(line2)
      break
     if not x[i]:
      x[i].append(line1)
      x[i].append(line2)
      break

  #print("printing x****************************")
  #print(x)   	



#code for plotting the nickname changes

  G1=nx.MultiDiGraph()   #using networkx
  y=-1
  for i in content:
   y=y+1
   if(i[0] =='=' and "changed the topic of" not in i):                                #scan every line which starts with ===
    line1=i[i.find("=")+1:i.find(" is")]
    line2=i[i.find("wn as")+1:i.find("\n")]
    line1=line1[3:]
    line2=line2[5:]
    if(line1[len(line1)-1]=='\\'):
     line1=line1[:-1]
     line1=line1 + 'CR' 
    if(line2[len(line2)-1]=='\\'):
     line2=line2[:-1]
     line2=line2 + 'CR'
    z=y
    while z>=0:
     z=z-1
     if(content[z][0]!='='):
      G1.add_edge(line1,line2,weight=content[z][1:6])
      break                             # these lines extract the from-to nicknames and strip them appropriately to make 
    if(z==-1):
     G1.add_edge(line1,line2,weight=rem_time)                                            #edge between them  
  
  count=len(content)-1
  while(count>=0):
   if(content[count][0]!='='):
    rem_time=content[count][1:6]
    break
   count=count-1
  

  
  
  
  for u,v,d in G1.edges(data=True):
      d['label'] = d.get('weight','')

  brilliant=channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_nickchanges.png"
  print(brilliant)
  A = nx.to_agraph(G1)
  A.layout(prog='dot')
  A.draw(brilliant)                      #graphviz helps to convert a dot file to PNG format for visualization
  

#code for making relation map between clients



  G = nx.MultiDiGraph()  #graph with multiple directed edges between clients used
  for line in content:
   flag_comma = 0
   if(line[0] != '=' and "] <" in line and "> " in line):
    m = re.search(r"\<(.*?)\>", line)
    var = m.group(0)[1:-1]
    if(var[len(var)-1]=='\\'):
     var=var[:-1]
     var=var + 'CR' 
    for d in range(len(nicks)):
     if var in x[d]:
      pehla = x[d][0]
      break
     else:
   	  pehla=var
      

    for i in nicks:
     data=[e.strip() for e in line.split(':')]
     data[1]=data[1][data[1].find(">")+1:len(data[1])]
     data[1]=data[1][1:]
     if not data[1]:
      break
     for ik in xrange(0,len(data)):
      if(data[ik] and data[ik][len(data[ik])-1]=='\\'):
       data[ik]=data[ik][:-1]
       data[ik]=data[ik] + 'CR'
     for z in data:
      if(z==i):
       send_time.append(line[1:6])
       if(var != i): 	
        for d in range(len(nicks)):
         if i in x[d]:
       	  second=x[d][0]
       	  break
         else:
       	  second=i
          
        G.add_edge(pehla,second,weight=line[1:6])	 
       
     if "," in data[1]: 
      flag_comma = 1
      data1=[e.strip() for e in data[1].split(',')]
      for ij in xrange(0,len(data1)):
       if(data1[ij] and data1[ij][len(data1[ij])-1]=='\\'):
        data1[ij]=data1[ij][:-1]
        data1[ij]=data1[ij] + 'CR'
      for j in data1:
       if(j==i):
        send_time.append(line[1:6])
        if(var != i): 	
         for d in range(len(nicks)):
          if i in x[d]:
       	   second=x[d][0]
       	   break
          else:
       	   second=i
       	  
         G.add_edge(pehla,second,weight=line[1:6])	 

     if(flag_comma == 0):
      search2=line[line.find(">")+1:line.find(", ")] 
      search2=search2[1:]
      if(search2[len(search2)-1]=='\\'):
       search2=search2[:-1]
       search2=search2 + 'CR' 
      if(search2==i):
       send_time.append(line[1:6])
       if(var != i):
        for d in range(len(nicks)):
         if i in x[d]:
       	  second=x[d][0]
       	  break
         else:
       	  second=i
       	 
        G.add_edge(pehla,second,weight=line[1:6])	 
      
    


  for u,v,d in G.edges(data=True):
      d['label'] = d.get('weight','')

#scan through the nicks list and for which nick the in and out degrees are not null add them to nickplots along with the in and out degrees
  for ni in nicks:
   if(bool(G.in_degree(ni)) is not False and bool(G.out_degree(ni)) is not False):
    nickplots.append(ni)
    indegree.append(G.in_degree(ni))
    outdegree.append(G.out_degree(ni))
  
#if indegree and outdegree list is not zero then plot the bar graphs using pandas library as shown below
  if(len(indegree)!=0 and len(outdegree)!=0):
   data = {'Nick': nickplots, #x axis
         'Indegree': indegree} #y axis
   df = pd.DataFrame(data, columns = ['Nick', 'Indegree'])
   df.index = df['Nick']
   del df['Nick']
   df  #these 3 lines remove the first column that has serial number
   print(df)
   axes = plt.gca()
   axes.set_ylim([0,200])
   df.plot(kind='bar', ax=axes)
   name1 = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_indegree.png"
   plt.savefig(name1)
   plt.close()

  #same thing for outdegree
   data = {'Nick': nickplots, 
         'Indegree': outdegree}
   df = pd.DataFrame(data, columns = ['Nick', 'Indegree'])
   df.index = df['Nick']
   del df['Nick']
   df
   print(df)
   axes = plt.gca()
   axes.set_ylim([0,200])
   df.plot(kind='bar', ax=axes)
   name2 = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_outdegree.png"
   plt.savefig(name2)
   plt.close()





  n_brilli=channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_conversation.png"
  print(n_brilli)
  A = nx.to_agraph(G)
  A.layout(prog='dot')
  A.draw(n_brilli)
  

  








