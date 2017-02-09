import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker
from analysis import network
from lib import config

log_directory = config.LOG_DIRECTORY
channel_name = config.CHANNEL_NAME
starting_date= config.STARTING_DATE
ending_date = config.ENDING_DATE
output_directory = config.OUTPUT_DIRECTORY

#input
log_data = reader.linux_input(log_directory, channel_name, starting_date, ending_date)                
nicks, nick_same_list = nickTracker.nick_tracker(log_data)

#analysis
message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)


#output
saver.draw_nx_graph(message_number_graph, output_directory, "message_time_graph")
