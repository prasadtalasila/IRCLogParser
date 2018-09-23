import os


def calculate_top_channel(search_dir):
    channel_activity = {}
    subdirs = [x[0] for x in os.walk(search_dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).next()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file_name in files:
                num_lines = sum(1 for line in open(subdir+'/'+file_name))
                if file_name in channel_activity:
                    channel_activity[file_name] += num_lines
                else:
                    channel_activity[file_name] = num_lines                                                                      

    channel_activity_sorted = sorted(channel_activity.items(), key=lambda x: -x[1])
    return channel_activity_sorted

print calculate_top_channel("/home/rohan/parser_files/YearlyLogFiles/2013/")