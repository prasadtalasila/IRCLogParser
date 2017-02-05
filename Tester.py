import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker
from analysis import network

log_directory="/home/rohan/parser_files/YearlyLogFiles/2013/"
channel_name="#kubuntu-devel"
starting_date = 1
starting_month = 1
ending_date = 31
ending_month = 1

#input
log_data = reader.linux_input(log_directory, channel_name, starting_date, starting_month, ending_date, ending_month)                
nicks, nick_same_list = nickTracker.nick_tracker(log_data)


#analysis
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)


#output
saver.draw_nx_graph(message_number_graph, "/home/rohan/Desktop", "message_time_graph")
