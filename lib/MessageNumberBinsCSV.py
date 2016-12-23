import os.path
import re
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import os
import csv
import ext.util

def createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth):

	output_file = output_directory + channel_name+"_2013_"+str(startingMonth)+"_"+str(endingMonth)+"_output-parser-bins.csv"
	if not os.path.exists(os.path.dirname(output_file)):
		try:
			os.makedirs(os.path.dirname(output_file))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	ans = [ 0 for i in range(48)]

	for folderiterator in range(startingMonth, endingMonth + 1):
		temp1 = "0" if folderiterator < 10 else ""
		for fileiterator in range(startingDate if folderiterator == startingMonth else 1, endingDate + 1 if folderiterator == endingMonth else 32):
			temp2 = "0" if fileiterator < 10 else ""
			filePath=log_directory+temp1+str(folderiterator)+"/"+temp2+str(fileiterator)+"/"+channel_name+".txt"   
			if not os.path.exists(filePath):
				if not((folderiterator==2 and (fileiterator ==29 or fileiterator ==30 or fileiterator ==31)) or ((folderiterator==4 or folderiterator==6 or folderiterator==9 or folderiterator==11) and fileiterator==31 )): 
					print "[Error] Path "+filePath+" doesn't exist"
				continue 
			with open(filePath) as f:
							content = f.readlines() #contents stores all the lines of the file channel_name

			nicks = [] #list of all the nicknames
			bins = []
						
			for i in range(0,48):
				bins.append(0)

			#code for getting all the nicknames in a list
			for i in content:
				if(i[0] != '=' and "] <" in i and "> " in i):
					m = re.search(r"\<(.*?)\>", i)
					if m.group(0) not in nicks:                       
						nicks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list

			for i in xrange(0,len(nicks)):
				nicks[i] = nicks[i][1:-1]     #removed <> from the nicknames
					
			for i in xrange(0,len(nicks)):
				nicks[i]=ext.util.correctLastCharCR(nicks[i])

			for line in content:
				if(line[0]=='=' and "changed the topic of" not in line):
					nick1=ext.util.correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
					nick2=ext.util.correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
					if nick1 not in nicks:
						nicks.append(nick1)
					if nick2 not in nicks:
						nicks.append(nick2)
			
			for line in content:
				if(line[0] != '='): 
					time_in_min=int(line[1:3])*60+int(line[4:6])
					if(time_in_min < int(line[1:3])*60+30):
						bin_index=int(line[1:3])*2 
					else:
						bin_index=int(line[1:3])*2+1
					flag_comma = 0
					if(line[0] != '=' and "] <" in line and "> " in line):
						m = re.search(r"\<(.*?)\>", line)
						var = m.group(0)[1:-1]
						var = ext.util.correctLastCharCR(var) 

						for i in nicks:
							rec_list=[e.strip() for e in line.split(':')]
							rec_list[1]=rec_list[1][rec_list[1].find(">")+1:len(rec_list[1])]
							rec_list[1]=rec_list[1][1:]
							if not rec_list[1]:
								break
							for k in xrange(0,len(rec_list)):
								if(rec_list[k]):
									rec_list[k] = ext.util.correctLastCharCR(rec_list[k])
							for z in rec_list:
								if(z==i):
									if(var != i):  
										bins[bin_index]=bins[bin_index]+1
											
							if "," in rec_list[1]: 
								flag_comma = 1
								rec_list_2=[e.strip() for e in rec_list[1].split(',')]
								for x in xrange(0,len(rec_list_2)):
									if(rec_list_2[x]):
										rec_list_2[x] = ext.util.correctLastCharCR(rec_list_2[x])
								for j in rec_list_2:
									if(j==i):
										if(var != i):  
											bins[bin_index]=bins[bin_index]+1
						
							if(flag_comma == 0):
								rec=line[line.find(">")+1:line.find(", ")] 
								rec=rec[1:]
								rec = ext.util.correctLastCharCR(rec) 
								if(rec==i):
									if(var != i):
										bins[bin_index]=bins[bin_index]+1
					
			# print "Working on "+filePath
			# print bins
			# print bins
			with open(output_file, 'a+') as myfile:
							wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
							wr.writerow(bins)
							ans = [ans[i] + bins[i] for i in range(len(bins))]

	print sum(ans)