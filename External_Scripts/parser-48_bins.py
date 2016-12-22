import os.path
import re
import numpy as np
import csv

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
  nicks = [] #list of all the nicknames
  send_time = [] #list of all the times a user sends a message to another user
  countit = []
  channel= "#kubuntu-devel" #channel name
    	
  for i in range(0,48):		#We create 48 bins and initialize all of them to 0.
   countit.append(0)

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
   
  
  
  
  for line in content:
   if(line[0] != '='):	
    num1=int(line[1:3])*60+int(line[4:6])
    if(num1 < int(line[1:3])*60+30):
  	 th=int(line[1:3])*2	 #Variable th is crucial as it records the bin which should be incremented when a msg is sent
    else:
   	 th=int(line[1:3])*2+1	#th uses the hour value in the log file to determine the bin index.
    flag_comma = 0
    if(line[0] != '=' and "] <" in line and "> " in line):
     m = re.search(r"\<(.*?)\>", line)
     var = m.group(0)[1:-1]
     if(var[len(var)-1]=='\\'):
      var=var[:-1]
      var=var + 'CR'  

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
        if(var != i): 	
         countit[th]=countit[th]+1
          
        
       
      if "," in data[1]: 
       flag_comma = 1
       data1=[e.strip() for e in data[1].split(',')]
       for ij in xrange(0,len(data1)):
        if(data1[ij] and data1[ij][len(data1[ij])-1]=='\\'):
         data1[ij]=data1[ij][:-1]
         data1[ij]=data1[ij] + 'CR'
       for j in data1:
        if(j==i):
         if(var != i): 	
          countit[th]=countit[th]+1
     
      if(flag_comma == 0):
       search2=line[line.find(">")+1:line.find(", ")] 
       search2=search2[1:]
       if(search2[len(search2)-1]=='\\'):
        search2=search2[:-1]
        search2=search2 + 'CR' 
       if(search2==i):
        if(var != i):
         countit[th]=countit[th]+1
    
  print(sttring)
  print(countit)

  with open('/home/dhruvie/LOP/logs_forsir.csv', 'a+') as myfile:	#We finally write the bin values to a csv file. This file can then be 
      wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)	#imported into plotly to draw heatmaps.
      wr.writerow(countit)



