import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.feature_extraction import text 
# stop_words = text.ENGLISH_STOP_WORDS.union(["hey","hi"])

def correctLastCharCR(inText):#if the last letter of the nick is '\' replace it by 'CR' for example rohan\ becomes rohanCR to avoid complications in nx because of \
 if(inText[len(inText)-1]=='\\'):
  inText = inText[:-1]+'CR'
 return inText

def correctNickFor_(inText):#last letter of nick maybe _ and this produces error in nickmatching
 if(inText and inText[len(inText)-1]=='_'):
  inText = inText[:-1]
 return inText

def createKeyWords(log_directory, channel_name, output_directory, startingMonth, endingMonth):
 
 out_dir_nick_change = output_directory+"key-words/"
 user_words_dict = []
 nick_same_list=[[] for i in range(5000)] #list of list with each list having all the nicks for that particular person


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
   
   print "Analysing ",filePath 
   
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
     
     nick_receiver=''

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
     
     #generating the words written by the sender

     message = rec_list[1:]
     correctedNickReciever = correctNickFor_(nick_receiver)
     if correctedNickReciever in message:
      message.remove(correctedNickReciever)
     # print nick_sender, "XXXXX", ":".join(message), "YYYY"  
     word_list = ":".join(message).split(" ")
     fr = 1
     for dic in user_words_dict:
      if dic['sender'] == nick_sender:
        dic['words'].extend(word_list)
        fr = 0
     if fr:
      user_words_dict.append({'sender':nick_sender, 'words':word_list }) 
 
 count_vect = CountVectorizer(analyzer = 'word', stop_words='english')
 for dictonary in user_words_dict:
  # print dictonary['sender']
  # print dictonary['words']
  matrix = count_vect.fit_transform(dictonary['words'])
  freqs = [(word, matrix.getcol(idx).sum()) for word, idx in count_vect.vocabulary_.items()]
  print dictonary['sender']
  print sorted(freqs, key = lambda x: -x[1])
  print "\n"