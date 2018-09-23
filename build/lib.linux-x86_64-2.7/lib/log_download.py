import datetime
from dateutil.rrule import rrule, DAILY
from datetime import timedelta
from BeautifulSoup import BeautifulSoup
import urllib2 as ulib
import logging
import re
import time
import os

log = logging.getLogger(__name__)

# Global variables
UBUNTU_ENDPOINT = "https://irclogs.ubuntu.com/{}/{month:02d}/{day:02d}"
UBUNTU_CHANNEL_ENDPOINT = "https://irclogs.ubuntu.com/{}/{month:02d}/{day:02d}/%23{channel}"
SCUMMVM_ENDPOINT = "http://www.enderboi.com/log.php?log=scummvm.log.{day:02d}{month}{year}&format=text"        
    

def save_log(log_data, save_dir, dt, name):
    """
    Args:
        log_data      (str) : chat log as text
        save_dir (str) : location of directory to save the log
        dt       (date): date corresponding to the log
        name     (str) : name of the file to be saved
    """
    
    if not (os.path.exists(save_dir) and os.path.isdir(save_dir)):
        log.info("Save Directory does not exist. Creating a new directory {}".format(save_dir))
        os.makedirs(save_dir)
    
    day_dir = os.path.join(save_dir, "{}/{month:02d}/{day:02d}".format(dt.year, month=dt.month, day=dt.day))
    
    if not os.path.isdir(day_dir):
        log.info("Day log directory does not exist. Creating log directory {}".format(day_dir))
        os.makedirs(day_dir)
        
    with open(os.path.join(day_dir, name), "w+") as f:
        f.write(log_data)
        
def send_request(url):
    """
    Args:
        url (str) - address to fetch log from
    
    Returns:
        The response(log) received from the server.
    """
    log.info("Sending request to {}".format(url))
    response = ulib.urlopen(url)
    
    status_code = response.getcode()
    
    if status_code != 200:
        log.warning("Error while sending download request to {} Returned code {}".format(url, status_code))
        return None
    else:
        log.info("Log fetched successfully for {}".format(url))
    
    res = response.read()
    time.sleep(1)
    return res
    

def ubuntu_url(start_date, end_date):
    """
    Args:
        start_date (date object): Starting date from which logs need to be fetched 
        end_date (date object) : Last date for which logs need to be fetched
    Returns:
        Yields channel name, current_date, and url at which log for returned
        channel and current_date is present.
    """
    
    for current_date in rrule(freq=DAILY, dtstart=start_date, until=end_date):
        url = UBUNTU_ENDPOINT.format(current_date.year,month=current_date.month, day=current_date.day)
        
        r = send_request(url)
        soup = BeautifulSoup(r)
        links = soup.findAll(href=re.compile(".txt"))
        
        for link in links:
            channel = link.string
            channel_ = channel[1:]
            
            yield channel, current_date, UBUNTU_CHANNEL_ENDPOINT.format(current_date.year, month=current_date.month, day=current_date.day, channel=channel_)
    
def scummvm_url(start_date, end_date):
    """
    Args:
        start_date (date object): Starting date from which logs need to be fetched 
        end_date (date object) : Last date for which logs need to be fetched
    Returns:
        Yields channel name, current_date, and url at which log for returned
        channel and current_date is present.
    """
    
    for current_date in rrule(freq=DAILY, dtstart=start_date, until=end_date):
                
        yield "#scummvm.txt", current_date, SCUMMVM_ENDPOINT.format(day=current_date.day, month=current_date.strftime('%b'), year=current_date.year)
    
def fetch_logs(start_date, end_date, url_endpoint, save_dir=os.path.join(os.getcwd(),"logs")):
    """
    Args:
        start_date (date object) : Starting date from which logs need to be fetched 
        end_date (date object) : Last date for which logs need to be fetched
        url_endpoint (function object): Function object that retrieves
        url end point where logs for particular date is present.
        save_dir (str) : location where fetched logs needs to be save
    Returns:
    
    
    """
    for name, next_date, url in url_endpoint(start_date, end_date):
        log = send_request(url)
        save_log(log, save_dir, next_date, name)

