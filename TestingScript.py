import Parser

log_directory = "/home/dhruvie/LOP/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/dhruvie/LOP/Output/"
startingDate = 1
startingMonth = 1
endingDate = 10
endingMonth = 1

'''
	TRY LARGE TIME RANGES ON THE FOLLOWING GRAPHS WITH UTMOST CARE
	WOULD TAKE A LONG TIME
'''

# Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.createAggregateGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createChannelsOfNickGraph(log_directory, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.degreeMessageNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.degreeNodeNumberCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.svdOnKeywords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.findResponseTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.findConvLength_ConvRefreshTime(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.createGephiTimelapseCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
#Parser.implementWithIgraphs(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)