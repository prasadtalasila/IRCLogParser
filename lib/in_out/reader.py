import os
import sys
sys.path.append('../lib')
import config

def linux_input(log_directory, channel_name, starting_date, starting_month, ending_date, ending_month):
    """  
        reads the IRC-Logs files in linux environment

    Args:
        log_directory (str): Location of the logs (Assumed to be arranged in directory structure as : <year>/<month>/<day>/<log-file-for-channel>.txt)
        channel_name (str): Channel to be perform analysis on
        starting_date (int): Date to start the analysis (in conjunction with starting_month)
        starting_month (int): Date to start the analysis (in conjunction with starting_date)
        ending_date (int): Date to end the analysis (in conjunction with ending_month)
        ending_month (int): Date to end the analysis (in conjunction with ending_date)

    Returns:
        content (log_data) : list of lists contaning log data for every day

    """
    log_data = []
    for folder_iterator in range(starting_month, ending_month + 1):
        extra0 = "0" if folder_iterator < 10 else ""
        for file_iterator in range(starting_date if folder_iterator == starting_month else 1, ending_date + 1 if folder_iterator == ending_month else 32):
            extra0_2 = "0" if file_iterator < 10 else ""
            file_path = log_directory + extra0 + \
                str(folder_iterator) + "/" + extra0_2 + \
                str(file_iterator) + "/" + channel_name + ".txt"
            if not os.path.exists(file_path):
                if not((folder_iterator == 2 and (file_iterator == 29 or file_iterator == 30 or file_iterator == 31)) or ((folder_iterator == 4 or folder_iterator == 6 or folder_iterator == 9 or folder_iterator == 11) and file_iterator == 31)):
                    print "[Error | io/linuxInput] Path " + file_path + " doesn't exist"
                continue
            with open(file_path) as f:
                # contents stores all the lines of the file channel_name
                if config.DEBUGGER:
                    print "Working on: " + file_path
                log_data.append(f.readlines())
               
    return log_data
