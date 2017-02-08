import os
import sys
sys.path.append('../lib')
import config
from datetime import date

def linux_input(log_directory, channel_name, starting_date, ending_date):
    """  
        reads the IRC-Logs files in linux environment

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        here log_directory will have the directory where all the folders 2013 2014 2015 etc are stored
        channel_name (str): Channel to be perform analysis on
        starting_date(str): Starting date in the format yyyy-mm-dd
        ending_date(str)  : Ending date in the format yyyy-mm-dd

    Returns:
        logs (dict) : dictionary with key(str) as 'yyyy-mm-dd' and value as another dictionary {"data":day_data,"channel":channel_name}

    """

    #splitting starting date and ending date
    (starting_year,starting_month,starting_day) = [int(x) for x in starting_date.split('-')]
    (ending_year,ending_month,ending_day) = [int(x) for x in ending_date.split('-')]
    logs={} 
    for year_iterator in range(starting_year,ending_year+1):  
        for month_iterator in range(starting_month if year_iterator == starting_year else 1, ending_month + 1 if year_iterator == ending_year else 13):
            extra0 = "0" if month_iterator < 10 else ""        
            for day_iterator in range(starting_day if (month_iterator == starting_month and year_iterator == starting_year) else 1, ending_day + 1 if (month_iterator == ending_month and year_iterator==ending_year) else 32):
                extra0_2 = "0" if day_iterator < 10 else ""
                file_path = log_directory+str(year_iterator)+"/"+extra0 + \
                    str(month_iterator) + "/" + extra0_2 + \
                    str(day_iterator) + "/" + channel_name + ".txt"
                if not os.path.exists(file_path):
                    if not((month_iterator == 2 and (day_iterator == 29 or day_iterator == 30 or day_iterator == 31)) or ((month_iterator == 4 or month_iterator == 6 or month_iterator == 9 or month_iterator == 11) and day_iterator == 31)):
                        print "[Error | io/linuxInput] Path " + file_path + " doesn't exist"
                    continue
                with open(file_path) as f:
                    """ day_data stores all the lines of the file channel_name """
                    if config.DEBUGGER:
                        print "Working on: " + file_path
                    day_data=f.readlines()             
                date_key = date(year_iterator,month_iterator,day_iterator)                
                logs[date_key]={"data":day_data , "channel":channel_name} 
    return logs       
    

