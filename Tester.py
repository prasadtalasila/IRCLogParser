import sys
sys.path.insert(0, "lib/")
from in_out import reader, saver
import nickTracker
from analysis import network, user, channel
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
# message_number_graph = network.message_number_graph(log_data, nicks, nick_same_list)
#nick_change_graph_list =  user.nick_change_graph(log_data)

#output
# saver.draw_nx_graph(message_number_graph, output_directory, "message_time_graph")
#for i in range(len(nick_change_graph_list)):
#	saver.draw_nx_graph(nick_change_graph_list[i], output_directory, "nick_change_graph_" + str(i))

# Test for Conversation Length and Conversation Refresh Time
CL,CRT = channel.conv_len_conv_refr_time(log_data,nicks,nick_same_list)
saver.save_csv(CL,output_directory,"CL")
saver.save_csv(CRT,output_directory,"CRT")

# Test for Response Time
RT = channel.find_response_time(log_data,nicks,nick_same_list)
saver.save_csv(RT,output_directory,"RT")

'''PRESENCE'''
#Change analysis to all channels
# nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash = nickTracker.nick_tracker(log_data, True)
# dict_out, graph = network.channel_user_presence_graph_and_csv(nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash)

# saver.save_csv(dict_out["UU"]["reducedMatrix"],output_directory, "rUU")
# saver.save_csv(dict_out["CC"]["reducedMatrix"],output_directory, "rCC")
# saver.save_csv(dict_out["CU"]["reducedMatrix"],output_directory, "rCU")