import re
import lib.scummvm.config as config
import lib.util as util
from datetime import date


def nick_tracker(log_dict):
    """ 
        Tracks all nicks and the identifies nicks which point to same user

    Args:
        log_dict(dictionary): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}

    Returns:
       nicks(list): all nicks
       nick_same_list(list): list of lists with each list corresponding to nicks of same user 

    """
    nicks = []  # list of all the nicknames
    nick_same_list = [[] for i in xrange(config.MAX_EXPECTED_DIFF_NICKS)]

    # Getting all the nicknames in a list
    def nick_append(nick, nicks):
        if nick not in nicks:
            nicks.append(nick)
        return nicks

    for day_content_all_channels in log_dict.values():
        # traverse over data of different channels for that day
        for day_content in day_content_all_channels:
            day_logs = day_content["log_data"]

            for day_log in day_logs:
                # use regex to get the string between <> and appended it to the nicks list
                if (util.check_if_msg_line(day_log)):
                    m = re.search(r"\<(.*?)\>", day_log)
                    nick = util.correctLastCharCR(m.group(0)[1:-1])
                    nicks = nick_append(nick, nicks)

            ''' Forming list of lists for avoiding nickname duplicacy '''
            for line in day_logs:
                if ("Nick change:" in line):
                    old_nick = line.split()[3]
                    new_nick = line.split()[5]
                    nicks = nick_append(old_nick, nicks)
                    nicks = nick_append(new_nick, nicks)

                    for i in xrange(config.MAX_EXPECTED_DIFF_NICKS):
                        if old_nick in nick_same_list[i] or new_nick in nick_same_list[i]:
                            if old_nick not in nick_same_list[i]:
                                nick_same_list[i].append(old_nick)
                            if new_nick not in nick_same_list[i]:
                                nick_same_list[i].append(new_nick)
                            break
                        if not nick_same_list[i]:
                            nick_same_list[i].append(old_nick)
                            nick_same_list[i].append(new_nick)
                            break

    for nick in nicks:
        for index in xrange(config.MAX_EXPECTED_DIFF_NICKS):
            if nick in nick_same_list[index]:
                break
            if not nick_same_list[index]:
                nick_same_list[index].append(nick)
                break

    if config.DEBUGGER:
        print "========> 30 on {} nicks".format(len(nicks))
        print nicks[:30]
        print "========> 30 on {} nick_same_list".format(len(nick_same_list))
        print nick_same_list[:30]

    return [nicks, nick_same_list]