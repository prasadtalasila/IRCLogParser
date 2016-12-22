import Parser
import glob
import os
import sys

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/"
startingDate = 1
startingMonth = 1
endingDate = 31
endingMonth = 1

x = 1

# for x in xrange(1, 13):
# Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# 	# print "Month:", x
# 	Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingDate, x, endingDate, x)
# Parser.createAggregateGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createChannelsOfNickGraph(log_directory, output_directory, startingDate, x, endingDate, x)
# Parser.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.degreeMessageNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.degreeNodeNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.KMeansTFIDF(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.fuzzyCMeans(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.findResponseTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.findConvLength_ConvRefreshTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createGephiTimelapseCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.implementWithIgraphs(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)


# "Runner for RT/RL/CRT Characterisitics"

# gap = 14
# meaningfull_channels = ['#kubuntu-devel.txt']
# # meaningfull_channels = ['#ubuntu-cn.txt', '#ubuntu-it.txt', '#ubuntu-touch.txt', '#ubuntu-uk.txt', '#ubuntu-br.txt', '#ubuntu-si.txt', '#ubuntu-unity.txt', '#kubuntu-devel.txt', '#ubuntu-desktop.txt', '#ubuntu-za.txt', '#ubuntu-ru.txt', '#juju-dev.txt', '#ubuntu-devel.txt', '#ubuntu-de.txt', '#kubuntu.txt', '#ubuntu-server.txt', '#xubuntu.txt', '#ubuntu-hr.txt', '#juju-gui.txt', '#ubuntu-es.txt', '#ubuntu-se.txt', '#ubuntu-quality.txt', '#ubuntu-pl.txt', '#xubuntu-devel.txt', '#ubuntu-ko.txt', '#ubuntu-app-devel.txt', '#ubuntu-meeting.txt', '#ubuntu-release.txt', '#ubuntu-no.txt', '#ubuntu-nl.txt', '#lubuntu.txt', '#ubuntu+1.txt', '#ubuntu-us-mi.txt', '#ubuntustudio.txt', '#ubuntu-kernel.txt']
# print "Creating a new output folder"
# output_dir_degree = output_directory+"CL/"
# os.system("rm -rf "+output_dir_degree)
# os.system("mkdir "+output_dir_degree)

# from datetime import date, datetime, timedelta

# def datespan(startDate, endDate, delta=timedelta(days=1)):
#     currentDate = startDate
#     while currentDate < endDate:
#         yield currentDate
#         currentDate += delta

# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[:-4]
# 	for day in datespan(date(2013, startingMonth, startingDate), date(2013, endingMonth, endingDate), delta=timedelta(days=gap)):
# 		print "\n", channel_searched, str(day.day)+"-"+str(day.month), ":",str((day+timedelta(gap)).day)+"-"+ str((day+timedelta(gap)).month)
# 		Parser.findResponseTime(log_directory, channel_searched, output_directory, day.day,  day.month,(day+timedelta(gap)).day,  (day+timedelta(gap)).month)		
# 	# i+=1


# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[:-4]
# 	for x in xrange(1, 13, 6):
# 		# print x
# 		print "\n", channel_searched, str(startingDate)+"-"+str(x), ":",str(endingDate)+"-"+ str(x+5)
# 		Parser.findConvLength_ConvRefreshTime(log_directory, channel_searched, output_directory, startingDate, x, endingDate, x+5)
# 	print x


# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[:-4]
# 	for x in xrange(1, 13, 2):
# 		# print x
# 		print "\n", channel_searched, str(startingDate)+"-"+str(x), ":",str(endingDate)+"-"+ str(x+1)
# 		Parser.findConvLength_ConvRefreshTime(log_directory, channel_searched, output_directory, startingDate, x, endingDate, x+1)
# # 	print x



# "NO OF USERS/MESSAGES" 

# # meaningfull_channels = [('#ubuntu.txt', 1511040), ('#ubuntu-cn.txt', 561818), ('#ubuntu-it.txt', 323776), ('#ubuntu-touch.txt', 270968), ('#ubuntu-uk.txt', 188089), ('#ubuntu-br.txt', 156714), ('#ubuntu-si.txt', 152977), ('#ubuntu-unity.txt', 142062), ('#kubuntu-devel.txt', 132959)]
# meaningfull_channels = [('#kubuntu-devel.txt', "")]
# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[0][:-4]
# 	print channel_searched
# 	# print "Number of Messages \t Number of users"
# 	# for x in xrange(1, 13):
# 		# print x
# 		# print "\n", channel_searched, str(startingDate)+"-"+str(x), ":",str(endingDate)+"-"+ str(x)
# 	Parser.createKeyWords(log_directory, channel_searched, output_directory, startingDate, 1, endingDate, 12)
# # 	print x



# "NO. OF Direct messages"

# # meaningfull_channels = [('#ubuntu.txt', 1511040), ('#ubuntu-cn.txt', 561818), ('#ubuntu-it.txt', 323776), ('#ubuntu-touch.txt', 270968), ('#ubuntu-uk.txt', 188089), ('#ubuntu-br.txt', 156714), ('#ubuntu-si.txt', 152977), ('#ubuntu-unity.txt', 142062), ('#kubuntu-devel.txt', 132959)]
# meaningfull_channels = [('#ubuntu-devel.txt', ""), ('#kubuntu.txt', "")]
# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[0][:-4]
# 	print channel_searched
# 	# print "Number of Messages \t Number of users"
# 	# for x in xrange(1, 13):
# 		# print x
# 		# print "\n", channel_searched, str(startingDate)+"-"+str(x), ":",str(endingDate)+"-"+ str(x)
# 	Parser.createMessageNumberBinsCSV(log_directory, channel_searched, output_directory, startingDate, 1, endingDate, 12)
# # 	print x



# "degreeNODE"

# meaningfull_channels = [('#ubuntu.txt', 1511040), ('#ubuntu-cn.txt', 561818), ('#ubuntu-it.txt', 323776), ('#ubuntu-touch.txt', 270968), ('#ubuntu-uk.txt', 188089), ('#ubuntu-br.txt', 156714), ('#ubuntu-si.txt', 152977), ('#ubuntu-unity.txt', 142062), ('#kubuntu-devel.txt', 132959)]
# meaningfull_channels = [('#kubuntu.txt', ""), ('#ubuntu-devel.txt', "")]
# print "degree"+"\t"+"slope"+"\tintercept\t"+"R**2"+"\t"+"MSE"
# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[0][:-4]
# 	print "\n", channel_searched
# 	# print "Number of Messages \t Number of users"
# 	for x in xrange(1, 13):
# 		print "Month=", x
# 		# print "\n", channel_searched, str(startingDate)+"-"+str(x), ":",str(endingDate)+"-"+ str(x)
# 		Parser.degreeNodeNumberCSV(log_directory, channel_searched, output_directory, startingDate, x, endingDate, x)
# # 	print x