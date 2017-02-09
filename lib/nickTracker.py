import re
import config
import util
from datetime import date
nicks = []  # list of all the nicknames
nick_same_list = [[] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]  

def nick_tracker(log_dict):
    """ 
        Tracks all nicks and the identifies nicks which point to same user

    Args:
        log_dict(dictionary): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}

    Returns:
       nicks(list): all nicks
       nick_same_list(list): list of lists with each list corresponding to nicks of same user 

    """

    #Getting all the nicknames in a list
    for day_content in log_dict.values():
        day_log = day_content["log_data"]
        
        for i in day_log:
            # use regex to get the string between <> and appended it to the nicks list
            if(i[0] != '=' and "] <" in i and "> " in i):
                m = re.search(r"\<(.*?)\>", i)
                nick = util.correctLastCharCR(m.group(0)[1:-1])
                if nick not in nicks:
                    nicks.append(nick)

        for line in day_log:
            if(line[0] == '=' and "changed the topic of" not in line):
                old_nick = util.correctLastCharCR(line[line.find("=") + 1:line.find(" is")][3:])
                new_nick = util.correctLastCharCR(line[line.find("wn as") + 1:line.find("\n")][5:])
                if old_nick not in nicks:
                    nicks.append(old_nick)
                if new_nick not in nicks:
                    nicks.append(new_nick)

        ''' Forming list of lists for avoiding nickname duplicacy '''
        for line in day_log:
            if(line[0] == '=' and "changed the topic of" not in line):
                old_nick = util.correctLastCharCR(line[line.find("=") + 1:line.find(" is")][3:])
                new_nick = util.correctLastCharCR(line[line.find("wn as") + 1:line.find("\n")][5:])
                for i in range(config.MAX_EXPECTED_DIFF_NICKS):
                    if old_nick in nick_same_list[i] or new_nick in nick_same_list[i]:
                        if old_nick not in nick_same_list[i]:
                            nick_same_list[i].append(old_nick)
                        if new_nick not in nick_same_list[i]:
                            nick_same_list[i].append(new_nick)
                        break
                    if not nick_same_list[i]:
                        if old_nick not in nick_same_list[i]:
                            nick_same_list[i].append(old_nick)
                        if new_nick not in nick_same_list[i]:
                            nick_same_list[i].append(new_nick)
                        break
    for nick in nicks:
        for index in range(config.MAX_EXPECTED_DIFF_NICKS):
            if nick in nick_same_list[index]:
                break
            if not nick_same_list[index]:
                nick_same_list[index].append(nick)
                break

    return nicks, nick_same_list