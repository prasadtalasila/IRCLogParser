import os
import sys
sys.path.append('../lib')
import config
import numpy as np
from datetime import date

def linux_input(log_directory, channel_name, starting_date, starting_month,starting_year, ending_date, ending_month,ending_year):   

    """  
        reads the IRC-Logs files in linux environment
        important to note : date constructor accpets in the format (yyyy,mm,dd) where each of the elements are integers
    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        here the log_directory stores the location of the directory where all the year folders are stored (ie folder 2013 2014 etc)
        channel_name (str): Channel to be perform analysis on
        starting_date (int): Date to start the analysis (in conjunction with starting_month)
        starting_month (int): Date to start the analysis (in conjunction with starting_date)
        starting_year (int): Date to start the analyis (in conjunction with starting_date and starting_month)
        ending_date (int): Date to end the analysis (in conjunction with ending_month)
        ending_month (int): Date to end the analysis (in conjunction with ending_date)
        ending_year (int): Date to end the analyis (in conjunction with starting_date and starting_month)

    Returns:
       logs : a dictionary with keys as a python date object and value as the data associated with that date
    """
    logs={} 
    for year_iterator in range(starting_year,ending_year+1):  
        for month_iterator in range(starting_month if year_iterator == starting_year else 1, ending_month + 1 if year_iterator == ending_year else 13):
            extra0 = "0" if month_iterator < 10 else ""        
            for day_iterator in range(starting_date if (month_iterator == starting_month and year_iterator == starting_year) else 1, ending_date + 1 if (month_iterator == ending_month and year_iterator==ending_year) else 32):
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
                logs.update({date_key: day_data}) 
    return logs       
    
