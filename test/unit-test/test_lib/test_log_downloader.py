import unittest
import lib.log_download as log_download
from dateutil.rrule import rrule, DAILY
import os
import datetime
import mock
import StringIO
import sys, shutil


def mock_url_endpoint(start_date, end_date):
    for current_date in rrule(freq=DAILY, dtstart=start_date, until=end_date):
        yield "kubuntu", current_date, "www.google.com"

 
class UtilTest(unittest.TestCase):
    def setUp(self):
        self.current_directory = os.path.dirname(os.path.realpath(__file__))

    def tearDown(self):
        self.current_directory = None
    
    def test_save_log(self):
    
        dt = datetime.datetime(2016,1,1)
        save_dir = os.path.join(self.current_directory, 'logs')
        day_dir = os.path.join(save_dir, "{}/{month:02d}/{day:02d}".format(dt.year,\
                             month=dt.month, day=dt.day))
        log = "log save test"
        name = "test.txt"
        
        log_download.save_log(log, save_dir, dt, name)
        
        with open(os.path.join(day_dir, name), 'r') as f:
                expected_out = f.read()
        
        self.assertTrue(os.path.isdir(day_dir))
        self.assertTrue(os.path.isdir(save_dir))
        self.assertTrue(os.path.isfile(os.path.join(day_dir, name)))
        self.assertEqual(expected_out, log)
        shutil.rmtree(save_dir)
    
    @mock.patch('lib.log_download.ulib.urlopen')
    @mock.patch('lib.log_download.time.sleep')
    def test_send_request_status_ok(self, mock_sleep, mock_urlopen):
        url = "http://www.google.com"
        mock_response = mock_urlopen.response
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response
        log_download.send_request(url)
        
        mock_response.read.assert_called_once()
        mock_urlopen.assert_called_once_with(url)
        mock_sleep.assert_called_once_with(1)
        
    @mock.patch('lib.log_download.ulib.urlopen')
    def test_send_request_status_error(self, mock_urlopen):
        url = "http://www.google.com"
        mock_response = mock_urlopen.response
        mock_response.getcode.return_value = 404
        mock_urlopen.return_value = mock_response
        response = log_download.send_request(url)
        
        self.assertTrue(response is None)
        mock_urlopen.assert_called_once_with(url)
        
    @mock.patch('lib.log_download.send_request')
    @mock.patch('lib.log_download.BeautifulSoup')
    def test_ubuntu_url(self, mock_BeautifulSoup, mock_send_request):
        start_date = datetime.datetime(2016,1,1)
        end_date = datetime.datetime(2016,1,2)
        
        soup = mock_BeautifulSoup.soup
        link = mock_BeautifulSoup.link
        mock_send_request.return_value = "Request Sent!!"
        mock_BeautifulSoup.return_value = soup
        soup.findAll.return_value = [link]
        link.string = "#kubuntu.txt"
        
        gen = log_download.ubuntu_url(start_date, end_date)
        
        self.assertEqual(next(gen), ("#kubuntu.txt", datetime.datetime(2016,1,1),\
                         "https://irclogs.ubuntu.com/2016/01/01/%23kubuntu.txt"))
        self.assertEqual(next(gen), ("#kubuntu.txt", datetime.datetime(2016,1,2), \
                        "https://irclogs.ubuntu.com/2016/01/02/%23kubuntu.txt"))
        
        
    def test_scummvm_url(self):
        start_date = datetime.datetime(2016,1,1)
        end_date = datetime.datetime(2016,1,2)
        
        gen = log_download.scummvm_url(start_date, end_date)
        
        self.assertEqual(next(gen), ("#scummvm.txt", datetime.datetime(2016,1,1),\
             "http://www.enderboi.com/log.php?log=scummvm.log.01Jan2016&format=text"))
        self.assertEqual(next(gen), ("#scummvm.txt", datetime.datetime(2016,1,2),\
            "http://www.enderboi.com/log.php?log=scummvm.log.02Jan2016&format=text"))
        
    @mock.patch('lib.log_download.send_request')
    @mock.patch('lib.log_download.save_log')
    def test_fetch_logs(self, mock_save_log, mock_send_request):
        start_date = datetime.datetime(2016,1,1)
        end_date = datetime.datetime(2016,1,2)
        save_dir = os.path.join(self.current_directory, "logs")
        log = "testing fetch logs"
        expected_args_list = iter([(log, save_dir, start_date, "kubuntu"), (log, save_dir, end_date, "kubuntu")])
        
        mock_send_request.return_value = log
        
        log_download.fetch_logs(start_date, end_date, mock_url_endpoint, save_dir=save_dir)
        
        for call in mock_save_log.call_args_list:
            args, kwargs = call
            self.assertEqual(args, next(expected_args_list))
       

if __name__ == '__main__':
    unittest.main()
