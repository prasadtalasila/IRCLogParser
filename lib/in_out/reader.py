import os
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import lib.config as config
import datetime
import collections
from collections import defaultdict
from dateutil.rrule import rrule, DAILY
import logging
import ConfigParser

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
    logs = defaultdict(list)
    linuxreaderfactory = LinuxReaderFactory()
    
    #splitting starting date and ending date
    (starting_year, starting_month, starting_day) = [int(x) for x in starting_date.split('-')]
    (ending_year, ending_month, ending_day) = [int(x) for x in ending_date.split('-')]

    start_date = datetime.date(starting_year, starting_month, starting_day)
    end_date = datetime.date(ending_year, ending_month, ending_day)

    for channel_name in channels_requested:            
        reader = linuxreaderfactory.reader_object(channel_name)
        logging_data = [log_directory, channel_name, start_date, end_date]
        linux_input_logging(reader, logging_data, logs);
        
    return collections.OrderedDict(sorted(logs.items()))
	    	    
    
def linux_input_logging(reader, logging_data, logs):
    
        log_directory = logging_data[0]
        channel_name = logging_data[1]
        start_date = logging_data[2]
        end_date = logging_data[3]

        if reader == None:
            logging.warn("Invalid channel name {}".format(channel_name))
            return

        for channel, date, log in reader.read_log(log_directory, [channel_name], start_date, end_date):
            date_key = date		
            value = {
		            "log_data": log,
		            "auxiliary_data": {
		                    "channel": channel,
		                    "year": date.year,
		                    "month": date.month,
		                    "day": date.day
		                }
		        }
            logs[date_key].append(value)

class ReaderFactory:
  
    def reader_object_name(self, mapping):
        pass
         
    def reader_object(self, channel_name):
	    pass


class MappingParser(ConfigParser.ConfigParser):
    
    def as_dict(self):        
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        
        return d


class LinuxReaderFactory(ReaderFactory):

    def reader_object_name(self, channel_name, mapping):        

        reader_name = None
        for key in mapping['Channels'].keys():                
            if channel_name in mapping['Channels'][key].split(','):
                reader_name = key
                break
        
        return reader_name        
        
    def reader_object(self, channel_name):

        parser = MappingParser()
        parser.read('channel_reader_mapping.ini')
        mapping= parser.as_dict()
        print(mapping)
        reader = None
        reader_name = self.reader_object_name(channel_name, mapping)
        if reader_name == 'ubuntu':
            reader = UbuntuReader()
        elif reader_name == 'slack':
            reader = SlackReader()
        elif reader_name == 'scummvm':
            reader = ScummVMReader()
        
        return reader


class Reader:

    def __init(self):
        pass
       
    def _build_path(self, log_directory, current_date, channel):
        pass

    def __read_single_channel_log(self, reader, logging_data):

        log_directory = logging_data[0]
        channel = logging_data[1]
        start_date = logging_data[2]
        end_date = logging_data[3]

        one_day = datetime.timedelta(1)
        current_date = start_date
        
        while current_date <= end_date:
            log_path = reader._build_path(log_directory, current_date, channel)
            
            if not os.path.exists(log_path):
                logging.warn("No Logs found at {}".format(log_path))
                raise IOError("Path " + log_path + " doesn't exist")
                continue
                
            with open(log_path, 'r') as f:
                    
                for line in f:
                    yield (channel, current_date, line)
            
            current_date = current_date + one_day
        
    def __read_log(self, reader, logging_data):

        log_directory = logging_data[0]
        channels = logging_data[1]
        start_date = logging_data[2]
        end_date = logging_data[3]

        if len(channels) != 1 or "ALL" in channels:
            logging.warn("This Reader class doesnot support multi channel \
                        log read. If you wish to read ubuntu logs use \
                        UbuntuReader or else extend this class to create\
                        a subclass with multi channel read support")
            return
        
        return reader._read_single_channel_log(log_directory, channels[0], start_date, end_date)        
    

class UbuntuReader(Reader, object):

    def __init__(self):
        pass
        
    def _build_path(self, log_directory, current_date, channel):
        path = "{}/{}/{}.txt".format(log_directory, current_date.strftime("%Y/%m/%d"), channel)
        return path    

    def _read_single_channel_log(self, log_directory, channel, start_date, end_date):
        return super(UbuntuReader, self)._Reader__read_single_channel_log(self, [log_directory, channel, start_date, end_date])
              
    def _read_multi_channel_logs(self, log_directory, channels, start_date, end_date):
        for i in range(len(channels)):
            yield self._read_single_channel_log(log_directory, channels[i], start_date, end_date)
        
    def _read_all_channel_logs(self, log_directory, start_date, end_date):   

        channels_requested=list()        
        parser = MappingParser()
        parser.read('channel_reader_mapping.ini')
        mapping= parser.as_dict()
        for channel_name in mapping['Channels']['ubuntu'].split(','):
            channels_requested.append(channel_name)
            
        return self._read_multi_channel_logs(log_directory, channels_requested, start_date, end_date)        
        
    def read_log(self,log_directory, channels, start_date, end_date):

        if len(channels) == 1 and channels[0] == "ALL":
            return self._read_all_channel_logs(log_directory, start_date, end_date)
        elif len(channels) == 1:
            return self._read_single_channel_log(log_directory, channels[0], start_date, end_date)
        else:
            return self._read_multi_channel_logs(log_directory, channels, start_date, end_date)
       
       
class SlackReader(Reader, object):

    def __init__(self):
       pass

    def _build_path(self, log_directory, current_date, channel):
        path = "{}/{}/{}.{}.log".format(log_directory, current_date.strftime("%Y"), channel,current_date.strftime("%Y%m%d"))
        return path

    def _read_single_channel_log(self, log_directory, channel, start_date, end_date): 
        return super(SlackReader, self)._Reader__read_single_channel_log(self, [log_directory, channel, start_date, end_date])
                
    def read_log(self, log_directory, channels, start_date, end_date):        
        return super(SlackReader, self)._Reader__read_log(self, [log_directory, channels, start_date, end_date])
    
    
class ScummVMReader(Reader, object):

    def __init__(self):
        pass
        
    def _build_path(self, log_directory, current_date, channel):
        path = "{}/{}/{}.txt".format(log_directory, current_date.strftime("%Y/%m/%d"), channel)
        return path  

    def _read_single_channel_log(self, log_directory, channel, start_date, end_date):        
        return super(ScummVMReader, self)._Reader__read_single_channel_log(self, [log_directory, channel, start_date, end_date])
            
    def read_log(self, log_directory, channels, start_date, end_date):    
        return super(ScummVMReader, self)._Reader__read_log(self, [log_directory, channels, start_date, end_date])
