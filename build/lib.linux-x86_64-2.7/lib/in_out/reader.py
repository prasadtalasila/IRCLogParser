import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import lib.config as config
import datetime
import collections
from collections import defaultdict

def linux_input(log_directory, channels_requested, starting_date, ending_date):
    """  
        reads the IRC-Logs files in linux environment

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        here log_directory will have the directory where all the folders 2013 2014 2015 etc are stored
        channels_requested (list): list of channels to be perform analysis on OR one element list ["ALL"] to perform analyis on all channels in the folder
        starting_date(str): Starting date in the format yyyy-mm-dd
        ending_date(str)  : Ending date in the format yyyy-mm-dd

    Returns:
        logs (dict) : dictionary with key(str) as 'yyyy-mm-dd' and value as another dictionary {"data":day_data,"channel":channel_name}

    """
    def check_if_path_and_file_is_valid(work_path, channels_requested):
        if not os.path.exists(work_path):
            raise IOError("Path " + work_path + " doesn't exist")

        all_channels = set()
        for channel in os.listdir(work_path):
            all_channels.add(channel[:-4])
        #if user has passed the channels_requested argument as "ALL", we make the channels_requested equal to all the available channels in work_path directory
        if len(channels_requested) == 1 and channels_requested[0] == "ALL":
            return list(all_channels)

        channel_list = []

        for channel in channels_requested:
            if channel not in all_channels:
                print "[Error | io/linuxInput] Channel " + work_path + channel + ".txt doesn't exist"
            else:
                channel_list.append(channel)
        return channel_list


    #splitting starting date and ending date
    (starting_year, starting_month, starting_day) = [int(x) for x in starting_date.split('-')]
    (ending_year, ending_month, ending_day) = [int(x) for x in ending_date.split('-')]
    current_date = datetime.date(starting_year, starting_month, starting_day)
    ending_date = datetime.date(ending_year, ending_month, ending_day)
    logs = defaultdict(list)
    one_day = datetime.timedelta(1)
    while (current_date <= ending_date):
        #select relevant channels
        work_path = log_directory + current_date.strftime("%Y/%m/%d") + "/"
        channel_list = check_if_path_and_file_is_valid(work_path, channels_requested)

        for channel_name in channel_list:
            file_path = work_path + channel_name + ".txt"
            with open(file_path) as f:
                """ day_data stores all the lines of the file channel_name """
                if config.DEBUGGER:
                    print "Working on: " + file_path

                day_data = f.readlines()

            date_key = current_date
            value = {
                "log_data": day_data,
                "auxiliary_data": {
                        "channel": channel_name,
                        "year": current_date.year,
                        "month": current_date.month,
                        "day": current_date.day
                    }
                }

            logs[date_key].append(value)
        current_date += one_day

    return collections.OrderedDict(sorted(logs.items()))
