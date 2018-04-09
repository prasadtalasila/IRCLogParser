import os
import datetime
import logging
from logging.config import fileConfig
import lib.log_download as downloader

lib_directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), "lib")

fileConfig(os.path.join(lib_directory, 'logging_config.ini'))


s_dt = datetime.datetime(2016, 1, 1)
e_dt = datetime.datetime(2017, 1, 1)

downloader.fetch_logs(s_dt, e_dt, downloader.ubuntu_url, save_dir=os.path.join(os.getcwd(),"logs/ubuntu"))
