import Parser

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/"
startingMonth = 1
endingMonth = 2

# Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
# Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
# Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
# Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingMonth, endingMonth)
'''
	TRY LARGE TIME RANGES ON THE FOLLOWING GRAPHS WITH UTMOST CARE
	WOULD TAKE A LONG TIME
'''
# Parser.createAggregateGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
# Parser.createChannelsOfNickGraph(log_directory, output_directory, startingMonth, endingMonth)
Parser.createKeyWords(log_directory, channel_name, output_directory, startingMonth, endingMonth)