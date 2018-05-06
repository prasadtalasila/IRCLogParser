import logging
import re

from parser_regex import log_regex


class Parser:
    def __init__(self, client):

        # self.nicks maintains a list of current user nicks present \
        # on channels. We will use this heuristic to see nicks mention \
        # in a message. User mention can happen in following ways: \
        # <rohit> bhuvan: or <rohit> bhuvan, kausam, or
        # <rohit> nice work kausam.

        self.nicks = []
        self.regexes = log_regex[client]
        # setup logging
        logging.basicConfig(filename='logger_out.log', level=logging.DEBUG)

    def data_extractor(self, matchObj, groups):
        data = {}
        for category_name, group_no in groups.items():
            data[category_name] = matchObj.group(group_no)

        return data

    def is_nick_change_event(self, line):

        return re.match(self.regexes['nick_change']['regex'], line)

    def parse_nick_change(self, log_line):
        matchObj = re.match(self.regexes['nick_change']['regex'], log_line)

        return self.data_extractor(matchObj, self.regexes['nick_change']['groups'])

    def nick_change_event(self, line):
        data = self.parse_nick_change(line)
        # remove old nick from self.nicks
        if data['old_nick'] in self.nicks:
            self.nicks.remove(data['old_nick'])

        self.nicks.append(data['new_nick'])
        data['type'] = 'NICK_CHANGE'

        return data

    def parse_directed_message(self, line):
        matchObj = re.match(self.regexes['directed_message']['regex'], line)

        return self.data_extractor(matchObj, self.regexes['directed_message']['groups'])

    def parse_undirected_message(self, line):
        matchObj = re.match(self.regexes['undirected_message']['regex'], line)

        return self.data_extractor(matchObj, self.regexes['undirected_message']['groups'])

    def message_event(self, line):

        data = {}
        if re.match(self.regexes['directed_message']['regex'], line):
            data = self.parse_directed_message(line)
            data['receivers'] = data['receivers'].split(',')
            data['type'] = 'DIRECTED_MESSAGE'
        elif re.match(self.regexes['undirected_message']['regex'], line):
            data = self.parse_undirected_message(line)
            data['type'] = 'UNDIRECTED_MESSAGE'
        else:
            logging.exception('Unknown Log Pattern Found')

        return data

    def line_parse(self, line):

        # remove leading and trailing whitespace
        line.strip()

        if self.is_nick_change_event(line):
            return self.nick_change_event(line)
        else:
            return self.message_event(line)

    def parse_log(self, log_line, date, channel_name):

        parse_line = self.line_parse(log_line)
        parse_line['date'] = date
        parse_line['channel'] = channel_name
        return parse_line

    def reset_state(self):
        self.nicks = []
        self.regexes = None