import importlib
import logging
import re


class Parser(object):
    def __init__(self, channel):

        # self.nicks maintains a list of current user nicks present \
        # on channels. We will use this heuristic to see nicks mention \
        # in a message. User mention can happen in following ways: \
        # <rohit> bhuvan: or <rohit> bhuvan, kausam, or
        # <rohit> nice work kausam.

        # setup logging
        logging.basicConfig(filename='logger_out.log', level=logging.DEBUG)

        self.nicks = []
        self.channel_name = channel
        regex_module_path = 'lib.in_out.parser.{}'.format(channel)
        try:
            parser_regex = importlib.import_module(regex_module_path)
        except ImportError:
            logging.exception('Unknown Channel Found')
            raise

        self.regexes = parser_regex.log_regex


    def __regex_data_extractor(self, matchObj, groups):
        """
        The function extracts the group information from the matchobject returned from regex matching
        :param matchObj:MatchObjeect generated from regex matching
        :param groups(dict): the tag of the data to be extracted from the regex and the corresponding group number of the regex
        :return: dictionary with the data extracted from regex
        """
        data = {}
        for category_name, group_no in groups.items():
            data[category_name] = matchObj.group(group_no)

        return data

    def __parse_event(self, event_type, log_line):
        """
        The function extracts relevant data from the given log line by matching it against a regular expression.
        :param event_type(str): event type of the log_line, e.g - Nick Change, Directed Message, Undirected Message
        :param log_line(str): log line to be parsed
        :return: a dictionary containing the relevant data extracted from the log_line
        """
        matchObj = re.match(self.regexes[event_type]['regex'], log_line)

        return self.__regex_data_extractor(matchObj, self.regexes[event_type]['groups'])

    def __check_event_type(self, log_line, event_type):
        """
        The function checks if the given log line is of the type of the given event
        :param log_line(str): a line from the log data
        :return (boolean): yes if the log_line is a nick change event otherwise No
        """
        return re.match(self.regexes[event_type]['regex'], log_line)

    def __nick_change_event(self, log_line):
        """
        Parses the log_line to ascertain the old nick and new nick.
        It also updates the nicks list by removing the old nick and adding the new nick of a user
        :param log_line(str): a line from the log data
        :return: a dictionary containing the relevant data extracted from the log_line
        """
        data = self.__parse_event('nick_change', log_line)
        # remove old nick from self.nicks
        if data['old_nick'] in self.nicks:
            self.nicks.remove(data['old_nick'])

        self.nicks.append(data['new_nick'])
        data['type'] = 'NICK_CHANGE'

        return data

    def __message_event(self, log_line):
        """
        Parses the log_line and identifies the Time, Sender, (Receiver) and the message content
        :param log_line(str): a line from the log data
        :return: a dictionary containing the relevant data extracted from the log_line
        """
        data = {}
        if self.__check_event_type(log_line, 'directed_message'):
            data = self.__parse_event('directed_message', log_line)
            data['receivers'] = data['receivers'].split(',')
            data['type'] = 'DIRECTED_MESSAGE'
        elif self.__check_event_type(log_line, 'undirected_message'):
            data = self.__parse_event('undirected_message', log_line)
            data['type'] = 'UNDIRECTED_MESSAGE'
        else:
            logging.exception('Unknown Log Pattern Found')

        return data

    def __line_parse(self, log_line):
        """
        Identifies the action in the log_line (eg: nick change, message etc) and subsequently parses the log_line
        :param log_line: a line from the log data
        :return: a dictionary containing the relevant data extracted from the log_line
        """
        
        # remove leading and trailing whitespace
        log_line.strip()

        if self.__check_event_type(log_line, 'nick_change'):
            return self.__nick_change_event(log_line)
        else:
            return self.__message_event(log_line)

    def parse_log(self, log_line):
        """
        The function to be called by other classes/functions for parsing a given log line.
        :param log_line: a line from the log data
        :return: a dictionary containing the relevant data extracted from the log_line
        """
        parse_line = self.__line_parse(log_line)
        parse_line['channel'] = self.channel_name
        return parse_line

    def reset_state(self):
        """
        Resets the current state of the object
        :return: None
        """
        self.nicks = []
        self.regexes = None