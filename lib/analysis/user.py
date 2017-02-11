import networkx as nx
import util
import config

def nick_change_graph(log_dict):

	""" creates a graph which tracks the nick changes of the users
	where each edge has a time stamp denoting the time 
	at which the nick was changed by the user

    Args:
        log_dict (str): Dictionary of logs created using reader.py    

    Returns:
       list of the day_to_day nick changes if config.DAY_BY_DAY_ANALYSIS=True or else an aggregate nick change graph for the 
       given time period.
    """   	

	rem_time = None #remembers the time of the last message of the file parsed before the current file
	nick_change_day_list = []
	aggregate_nick_change_graph = nx.MultiDiGraph() # graph for nick changes in the whole time span (not day to day)
	
	for day_content_all_channels in log_dict.values():		
		
		for day_content in day_content_all_channels:			
				day_log = day_content["log_data"]					
				
				today_nick_change_graph = nx.MultiDiGraph()   #using networkx
				current_line_no = -1
				
				for line in day_log:
					current_line_no = current_line_no + 1
					
					if(line[0] == '=' and "changed the topic of" not in line):  #excluding the condition when user changes the topic. Search for only nick changes
						nick1 = util.correctLastCharCR(line[line.find("=")+1:line.find(" is")][3:])
						nick2 = util.correctLastCharCR(line[line.find("wn as")+1:line.find("\n")][5:])
						earlier_line_no = current_line_no

						while earlier_line_no >= 0: #to find the line just before "=="" so as to find time of Nick Change
							earlier_line_no = earlier_line_no - 1
							if(day_log[earlier_line_no][0] != '='):								
								today_nick_change_graph.add_edge(nick1, nick2, weight=day_log[earlier_line_no][1:6])
								year, month, day = str(day_content["auxiliary_data"]["year"]), str(day_content["auxiliary_data"]["month"]),str(day_content["auxiliary_data"]["day"])
								aggregate_nick_change_graph.add_edge(nick1, nick2, 
									weight=year+"/" + month+ "/" + day + " - "+day_log[earlier_line_no][1:6])
								break

						if(earlier_line_no == -1):
							today_nick_change_graph.add_edge(nick1, nick2, weight=rem_time)                                              
							aggregate_nick_change_graph.add_edge(nick1, nick2, weight = rem_time)
				
				count = len(day_log) - 1 #setting up the rem_time for next file, by noting the last message sent on that file.
				
				while(count >= 0):
					if(day_log[count][0] != '='):
						rem_time = day_log[count][1:6]
						break
					count = count-1
				
				nick_change_day_list.append(today_nick_change_graph)	
						
	if config.DAY_BY_DAY_ANALYSIS:
		return nick_change_day_list
	else:
		return aggregate_nick_change_graph
			