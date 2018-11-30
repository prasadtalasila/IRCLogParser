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
  
    def reader_object_name(self):
        pass
         
    def reader_object(self, channel_name):
	    pass


class LinuxReaderFactory(ReaderFactory):

    def reader_object_name(self, channel_name):        

        mapping = {'Ubuntu' : '#ubuntu-cat,#ubuntu-es,#ubuntu,#xubuntu,#ubuntu-discuss,#ubuntustudio,#ubuntu-beginners,#lubuntu,#ubuntustudio-devel,#ubuntu-irc,#ubuntu-us-nc,#ubuntu-news,#kubuntu,#ubuntu-motu,#ubuntu-ops,#ubuntu-server,#ubuntu-x,#ubuntu+1,#ubuntu-devel,#kubuntu-devel,#ubuntu-meeting,#ubuntu-translators,#edubuntu,#xubuntu-devel,#ubuntu-us-ca,#ubuntu-ke,#upstart,#ubuntu-kernel,#ubuntu-us-or,#ubuntu-community-team,#ubuntu-quality,#ubuntu-youth,#ubuntu-us-oh,#ubuntu-us-tn,#launchpad,#ubuntu-classroom,#ubuntu-us-pa,#ubuntu-gnome,#ubuntu-gnome-devel,#ubuntu-release,#ubuntu-bugs,#ubuntu-phone,#ubuntu-pl,#ubuntu-app-devel,#ubuntu-uk,#ubuntu-arb,#ubuntu-locoteams,#ubuntu-au,#ubuntu-leadership,#ubuntu-website,#ubuntu-doc,#ubuntu-manual,#ubuntu-learning,#ubuntu-on-air,#ubuntu-nl-mwanzo,#ubuntuone,#bzr,#launchpad-meeting,#launchpad-dev,#juju-dev,#ubuntu-de,#ubuntu-ru,#ubuntu-cn,#ubuntu-mythtv,#ubuntu-ro,#ubuntu-it,#ubuntu-vn,#ubuntu-br,#ubuntu-women-project,#ubuntu-nl,#ubuntu-design,#ubuntu-ie,#ubuntu-desktop,#ubuntu-arm,#maas,#ubuntu-nz,#ubuntu-za,#ubuntu-fi,#ubuntu-mozillateam,#ubuntu-qc,#ubuntu-ca,#ubuntu-pe,#ubuntu-us-mi,#ubuntu-uy,#ubuntu-unity,#ubuntu-dk-moede,#ubuntu-dk,#ubuntu-no,#ubuntu-ph,#ubuntu-my,#ubuntu-cm,#ubuntu-rs,#ubuntu-mk,#ubuntu-tablet,#ubuntu-tv,#ubuntu-it-meeting,#ubuntu-hr,#ubuntu-tr,#ubuntu-accessibility,#ubuntu-se,#ubuntu-ir,#ubuntu-si,#ubuntu-ko,#ubuntu-installer,#ubuntu-cl,#kubuntu-se,#ubuntu-cym,#ubuntu-eg,#ubuntu-tn,#ubuntu-cz,#ubuntu-dz,#ubuntu-us-wa,#ubuntu-ngo,#juju-gui,#ubuntu-classroom-es,#ubuntu-co,#ubuntu-us-ga,#ubuntu-jp,#launchpad-yellow,#ubuntu-papercuts,#ubuntu-us-co,#ubuntu-us-mn,#ubuntu-co-meeting,#ubuntu-ar,#ubuntu-es-locos,#ubuntu-us-fl,#ubuntu-touch,#ubuntu-us-dc,#ubuntu-us-tx,#ubuntu-sa,#ubuntu-bd,#ubuntu-artwork,#ubuntu-il,#ubuntu-fr-l10n,#ubuntu-toolchain,#ubuntu-ports,#ubuntu-zh,#ubuntu-java,#ubuntu-marketing,#ubuntu-us-sc,#ubuntu-eu,#ubuntu-tw,#ubuntu-laptop,#ubuntu-tam,#ubuntu-hk,#ubuntu-pk,#ubuntu-centroamerica,#ubuntu-charlas,#ubuntu-l10n-es,#launchpad-reviews,#ubuntu-us-ar,#ubuntu-cy,#ubuntu-lb,#ubuntu-tour,#ubuntu-for-all,#ubuntu-se-mote,#ubuntu-translators-ru,#ubuntu-pa,#ubuntu-hn,#ubuntu-us-me,#ubuntu-us-md,#ubuntu-sv,#ubuntu-tn-classroom,#ubuntu-tn-meeting', 'Slack' : 'slackware', 'ScummVM' : 'scummvm'}
        reader_name = None
        for key in mapping.keys():  
            if channel_name in mapping[key].split(','):
                reader_name = key
                break        
        return reader_name        
        
    def reader_object(self, channel_name):

        reader = None
        reader_name = self.reader_object_name(channel_name)
        if reader_name == 'Ubuntu':
            reader = UbuntuReader()
        elif reader_name == 'Slack':
            reader = SlackReader()
        elif reader_name == 'ScummVM':
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

        channels_requested = list()
        ubuntu_mapping = {'Ubuntu' : '#ubuntu-cat,#ubuntu-es,#ubuntu,#xubuntu,#ubuntu-discuss,#ubuntustudio,#ubuntu-beginners,#lubuntu,#ubuntustudio-devel,#ubuntu-irc,#ubuntu-us-nc,#ubuntu-news,#kubuntu,#ubuntu-motu,#ubuntu-ops,#ubuntu-server,#ubuntu-x,#ubuntu+1,#ubuntu-devel,#kubuntu-devel,#ubuntu-meeting,#ubuntu-translators,#edubuntu,#xubuntu-devel,#ubuntu-us-ca,#ubuntu-ke,#upstart,#ubuntu-kernel,#ubuntu-us-or,#ubuntu-community-team,#ubuntu-quality,#ubuntu-youth,#ubuntu-us-oh,#ubuntu-us-tn,#launchpad,#ubuntu-classroom,#ubuntu-us-pa,#ubuntu-gnome,#ubuntu-gnome-devel,#ubuntu-release,#ubuntu-bugs,#ubuntu-phone,#ubuntu-pl,#ubuntu-app-devel,#ubuntu-uk,#ubuntu-arb,#ubuntu-locoteams,#ubuntu-au,#ubuntu-leadership,#ubuntu-website,#ubuntu-doc,#ubuntu-manual,#ubuntu-learning,#ubuntu-on-air,#ubuntu-nl-mwanzo,#ubuntuone,#bzr,#launchpad-meeting,#launchpad-dev,#juju-dev,#ubuntu-de,#ubuntu-ru,#ubuntu-cn,#ubuntu-mythtv,#ubuntu-ro,#ubuntu-it,#ubuntu-vn,#ubuntu-br,#ubuntu-women-project,#ubuntu-nl,#ubuntu-design,#ubuntu-ie,#ubuntu-desktop,#ubuntu-arm,#maas,#ubuntu-nz,#ubuntu-za,#ubuntu-fi,#ubuntu-mozillateam,#ubuntu-qc,#ubuntu-ca,#ubuntu-pe,#ubuntu-us-mi,#ubuntu-uy,#ubuntu-unity,#ubuntu-dk-moede,#ubuntu-dk,#ubuntu-no,#ubuntu-ph,#ubuntu-my,#ubuntu-cm,#ubuntu-rs,#ubuntu-mk,#ubuntu-tablet,#ubuntu-tv,#ubuntu-it-meeting,#ubuntu-hr,#ubuntu-tr,#ubuntu-accessibility,#ubuntu-se,#ubuntu-ir,#ubuntu-si,#ubuntu-ko,#ubuntu-installer,#ubuntu-cl,#kubuntu-se,#ubuntu-cym,#ubuntu-eg,#ubuntu-tn,#ubuntu-cz,#ubuntu-dz,#ubuntu-us-wa,#ubuntu-ngo,#juju-gui,#ubuntu-classroom-es,#ubuntu-co,#ubuntu-us-ga,#ubuntu-jp,#launchpad-yellow,#ubuntu-papercuts,#ubuntu-us-co,#ubuntu-us-mn,#ubuntu-co-meeting,#ubuntu-ar,#ubuntu-es-locos,#ubuntu-us-fl,#ubuntu-touch,#ubuntu-us-dc,#ubuntu-us-tx,#ubuntu-sa,#ubuntu-bd,#ubuntu-artwork,#ubuntu-il,#ubuntu-fr-l10n,#ubuntu-toolchain,#ubuntu-ports,#ubuntu-zh,#ubuntu-java,#ubuntu-marketing,#ubuntu-us-sc,#ubuntu-eu,#ubuntu-tw,#ubuntu-laptop,#ubuntu-tam,#ubuntu-hk,#ubuntu-pk,#ubuntu-centroamerica,#ubuntu-charlas,#ubuntu-l10n-es,#launchpad-reviews,#ubuntu-us-ar,#ubuntu-cy,#ubuntu-lb,#ubuntu-tour,#ubuntu-for-all,#ubuntu-se-mote,#ubuntu-translators-ru,#ubuntu-pa,#ubuntu-hn,#ubuntu-us-me,#ubuntu-us-md,#ubuntu-sv,#ubuntu-tn-classroom,#ubuntu-tn-meeting'}
        for channel_name in ubuntu_mapping['Ubuntu'].split(','):
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
