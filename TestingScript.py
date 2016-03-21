import Parser

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/"
startingDate = 21
startingMonth = 1
endingDate = 7
endingMonth = 3

# Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)
'''
	TRY LARGE TIME RANGES ON THE FOLLOWING GRAPHS WITH UTMOST CARE
	WOULD TAKE A LONG TIME
'''
# Parser.createAggregateGraph(log_directory, channel_name, startingDate, startingMonth, endingDate, endingMonth)
# Parser.createChannelsOfNickGraph(log_directory, output_directory, startingDate, startingMonth, endingDate, endingMonth)
Parser.createKeyWords(log_directory, channel_name, output_directory, startingDate, startingMonth, endingDate, endingMonth)