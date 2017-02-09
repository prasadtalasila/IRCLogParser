import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker
from analysis import network

log_directory="/media/krishna/Media/ParserIn/"
channel_name="#kubuntu-devel"
starting_date="2013-3-12"
ending_date = "2013-4-14"
#input
log_data = reader.linux_input(log_directory, channel_name, starting_date,ending_date)                
nicks, nick_same_list = nickTracker.nick_tracker(log_data)


#analysis
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)


#output
saver.draw_nx_graph(message_number_graph, "/home/krishna/Desktop","MNG")
