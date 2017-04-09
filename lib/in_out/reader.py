import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import lib.config as config
from datetime import date
import collections
from collections import defaultdict

def linux_input(log_directory, channel_list, starting_date, ending_date):
    """  
        reads the IRC-Logs files in linux environment

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        here log_directory will have the directory where all the folders 2013 2014 2015 etc are stored
        channels_list (list): list of channels to be perform analysis on OR one element list ["ALL"] to perform analyis on all channels in the folder
        starting_date(str): Starting date in the format yyyy-mm-dd
        ending_date(str)  : Ending date in the format yyyy-mm-dd

    Returns:
        logs (dict) : dictionary with key(str) as 'yyyy-mm-dd' and value as another dictionary {"data":day_data,"channel":channel_name}

    """

    #splitting starting date and ending date
    (starting_year, starting_month, starting_day) = [int(x) for x in starting_date.split('-')]
    (ending_year, ending_month, ending_day) = [int(x) for x in ending_date.split('-')]
    
    logs = defaultdict(list)
    
    #enter year folder
    for year_iterator in range(starting_year, ending_year + 1):  
        #enter month folders
        for month_iterator in range(starting_month if year_iterator == starting_year else 1, ending_month + 1 if year_iterator == ending_year else 13):
            extra0 = "0" if month_iterator < 10 else ""        
            #enter day folder
            for day_iterator in range(starting_day if (month_iterator == starting_month and year_iterator == starting_year) else 1, ending_day + 1 if (month_iterator == ending_month and year_iterator==ending_year) else 32):
                extra0_2 = "0" if day_iterator < 10 else ""
                work_path = log_directory+str(year_iterator)+"/"+extra0 + \
                    str(month_iterator) + "/" + extra0_2 + \
                    str(day_iterator) + "/"
                #select relevant channels
                if not os.path.exists(work_path):
                    if not((month_iterator == 2 and (day_iterator == 29 or day_iterator == 30 or day_iterator == 31)) or ((month_iterator == 4 or month_iterator == 6 or month_iterator == 9 or month_iterator == 11) and day_iterator == 31)):
                        print "[Error | io/linuxInput] Path", work_path, "doesn't exist"
                else:
                    for channel_searched in os.listdir(work_path):
                        channel_name = channel_searched[:-4]
                        if channel_name in channel_list or (len(channel_list) == 1 and channel_list[0] == "ALL"):
                            file_path = work_path + channel_name + ".txt"
                            if not os.path.exists(file_path):
                                print "[Error | io/linuxInput] Channel " + file_path + " doesn't exist"
                                continue
                            with open(file_path) as f:
                                """ day_data stores all the lines of the file channel_name """
                                if config.DEBUGGER:
                                    print "Working on: " + file_path
                                
                                day_data = f.readlines()             
                            
                            f.close()

                            date_key = date(year_iterator, month_iterator, day_iterator)
                            value = {
                                "log_data": day_data, 
                                "auxiliary_data": {
                                        "channel": channel_name,
                                        "year": year_iterator,
                                        "month": month_iterator,
                                        "day": day_iterator
                                    }
                                }
        
                            logs[date_key].append(value)
                    
    return collections.OrderedDict(sorted(logs.items()))