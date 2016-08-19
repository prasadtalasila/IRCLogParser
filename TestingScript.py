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

'''
	TRY LARGE TIME RANGES ON THE FOLLOWING GRAPHS WITH UTMOST CARE
	WOULD TAKE A LONG TIME
'''
# for x in xrange(1, 13):
# Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createAggregateGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
	# Parser.createChannelsOfNickGraph(log_directory, output_directory, startingDate, x, endingDate, x)
# Parser.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.degreeMessageNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
Parser.degreeNodeNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.svdOnKeywords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.findResponseTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.findConvLength_ConvRefreshTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createGephiTimelapseCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.implementWithIgraphs(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# print "Creating a new output folder"
# print "Creating a new output folder"
# meaningfull_channels = ['#ubuntu.txt']
# print "Creating a new output folder"
# output_dir_degree = output_directory+"degreeNodeNumberCSV/"
# os.system("rm -rf "+output_dir_degree)
# os.system("mkdir "+output_dir_degree)
# i = 0
# for channel_searched in meaningfull_channels:
# 	channel_searched = channel_searched[:-4]
# 	for x in xrange(1, 13):
# 		Parser.degreeNodeNumberCSV(log_directory, channel_searched, output_directory, startingDate, x, endingDate, x)
# 	print x