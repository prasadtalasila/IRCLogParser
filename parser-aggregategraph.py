import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz

x=[[] for i in range(5000)]

xarr=[[] for i in range(5000)]
for i in xrange(0,5000):
 xarr[i].append(0)

nicks = [] #list of all the nicknames
G = nx.DiGraph()  #graph with multiple directed edges between clients used 

for iterator in range(1,13):
 for fileiterator in range(1,32):
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
 
  send_time = [] #list of all the times a user sends a message to another user
  picks = []
  channel= "#kubuntu-devel" #channel name
  print(sttring)  	
  
#code for getting all the nicknames in a list
  for i in content:
   if(i[0] != '=' and "] <" in i and "> " in i):
    m = re.search(r"\<(.*?)\>", i)
    if m.group(0) not in picks:                       
     picks.append(m.group(0))  	#used regex to get the string between <> and appended it to the nicks list



  for i in xrange(0,len(picks)):
   if picks[i][1:-1] not in nicks:
    nicks.append(picks[i][1:-1])     #removed <> from the nicknames
    
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
   
  
  
    
 #code for forming list of lists for avoiding nickname duplicacy

  
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
    for i in range(5000):
     if line1 in x[i] or line2 in x[i]:
      x[i].append(line1)
      x[i].append(line2)
      break
     if not x[i]:
      x[i].append(line1)
      x[i].append(line2)
      break

  
  

#code for making relation map between clients


  
  for line in content:
   flag_comma = 0
   if(line[0] != '=' and "] <" in line and "> " in line):
    m = re.search(r"\<(.*?)\>", line)
    var = m.group(0)[1:-1]
    if(var[len(var)-1]=='\\'):
     var=var[:-1]
     var=var + 'CR' 
    for d in range(5000):
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
        for d in range(5000):
         if i in x[d]:
       	  second=x[d][0]
       	  break
         else:
       	  second=i
          
        for rt in xrange(0,5000):
         if (pehla in xarr[rt] and second in xarr[rt]):
          if (pehla == xarr[rt][1] and second == xarr[rt][2]):
           xarr[rt][0]=xarr[rt][0]+1
           break
         if(len(xarr[rt])==1):
          xarr[rt].append(pehla)
          xarr[rt].append(second)
          xarr[rt][0]=xarr[rt][0]+1
          break
       
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
         for d in range(5000):
          if i in x[d]:
       	   second=x[d][0]
       	   break
          else:
       	   second=i
       	  
         for rt in xrange(0,5000):
          if (pehla in xarr[rt] and second in xarr[rt]):
           if (pehla == xarr[rt][1] and second == xarr[rt][2]):
            xarr[rt][0]=xarr[rt][0]+1
            break
          if(len(xarr[rt])==1):
           xarr[rt].append(pehla)
           xarr[rt].append(second)
           xarr[rt][0]=xarr[rt][0]+1
           break

     if(flag_comma == 0):
      search2=line[line.find(">")+1:line.find(", ")] 
      search2=search2[1:]
      if(search2[len(search2)-1]=='\\'):
       search2=search2[:-1]
       search2=search2 + 'CR' 
      if(search2==i):
       send_time.append(line[1:6])
       if(var != i):
        for d in range(5000):
         if i in x[d]:
       	  second=x[d][0]
       	  break
         else:
       	  second=i
       	 
        for rt in xrange(0,5000):
         if (pehla in xarr[rt] and second in xarr[rt]):	
          if (pehla == xarr[rt][1] and second == xarr[rt][2]):
           xarr[rt][0]=xarr[rt][0]+1
           break
         if(len(xarr[rt])==1):
          xarr[rt].append(pehla)
          xarr[rt].append(second)
          xarr[rt][0]=xarr[rt][0]+1
          break
      
 
  

  for fin in xrange(0,5000):
   if(len(xarr[fin])==3):
    G.add_edge(xarr[fin][1],xarr[fin][2],weight=xarr[fin][0])	 


print("*******nicksssssssssssss")
print(nicks)
print("*******xxxxxxxxx")
print(x)
print("*xaaaaaaaaaaaaaarrr")
print(xarr)

for u,v,d in G.edges(data=True):
    d['label'] = d.get('weight','')
n_brilli=channel+"_2013_aggregategraph.png"
print(n_brilli)
A = nx.to_agraph(G)
A.layout(prog='dot')
A.draw(n_brilli)
print("Done.")

  









