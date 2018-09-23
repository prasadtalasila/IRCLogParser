import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import lib.slack.config as config
from datetime import date
import collections
from collections import defaultdict

def linux_input_slack(log_directory, starting_date, ending_date):
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

    def check_if_path_is_valid(work_path):
        if not os.path.exists(work_path):
           raise IOError("Path " + work_path + " doesn't exist")

        return  os.listdir(work_path)

    #splitting starting date and ending date
    (starting_year, starting_month, starting_day) = [int(x) for x in starting_date.split('-')]
    (ending_year, ending_month, ending_day) = [int(x) for x in ending_date.split('-')]

    logs = defaultdict(list)

    #enter year folder
    for year_iterator in range(starting_year, ending_year + 1):
        work_path = log_directory+str(year_iterator)+"/"
        file_list = check_if_path_is_valid(work_path)
        #select month
        for month_iterator in range(starting_month if year_iterator == starting_year else 1, ending_month + 1 if year_iterator == ending_year else 13):
            extra0 = "0" if month_iterator < 10 else ""
            #select day
            for day_iterator in range(starting_day if (month_iterator == starting_month and year_iterator == starting_year) else 1, ending_day + 1 if (month_iterator == ending_month and year_iterator==ending_year) else 32):
                extra0_2 = "0" if day_iterator < 10 else ""
                slack_file = "slackware." + str(year_iterator) + str(extra0) + str(month_iterator) + str(extra0_2) + str(day_iterator) + ".log"
                file_path = work_path + slack_file
                if slack_file not in file_list:
                    print "[Error | io/linuxInput] File " + file_path + " doesn't exist"
                    continue

                with open(file_path) as f:
                    """ day_data stores all the lines of the file channel_name """
                    if config.DEBUGGER:
                        print "Working on: " + file_path

                    day_data = f.readlines()

                date_key = date(year_iterator, month_iterator, day_iterator)
                value = {
                    "log_data": day_data,
                    "auxiliary_data": {
                            "channel": "slackware",
                            "year": year_iterator,
                            "month": month_iterator,
                            "day": day_iterator
                        }
                    }

                logs[date_key].append(value)

    return collections.OrderedDict(sorted(logs.items()))
