import Parser

log_directory = "/home/rohan/parser_files/2013/"
channel_name= "#kubuntu-devel" #channel name
output_directory = "/home/rohan/parser_files/Output/"
startingMonth = 11
endingMonth = 12

Parser.createNickChangesGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
Parser.createMessageTimeGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
Parser.createMessageNumberGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)
Parser.createMessageNumberBinsCSV(log_directory, channel_name, output_directory, startingMonth, endingMonth)
Parser.createAggregateGraph(log_directory, channel_name, output_directory, startingMonth, endingMonth)