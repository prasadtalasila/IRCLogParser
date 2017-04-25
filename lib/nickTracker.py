import re
import lib.config as config
import lib.util as util
from datetime import date

def nick_tracker(log_dict, track_users_on_channels = False):
    """ 
        Tracks all nicks and the identifies nicks which point to same user

    Args:
        log_dict(dictionary): with key as dateTime.date object and value as {"data":datalist,"channel_name":channels name}

    Returns:
       nicks(list): all nicks
       nick_same_list(list): list of lists with each list corresponding to nicks of same user 

    """
    nicks = []  # list of all the nicknames
    nick_same_list = [[] for i in range(config.MAX_EXPECTED_DIFF_NICKS)]  
    nick_channel_dict = []
    channels_for_user = []
    nicks_hash = []
    channels_hash = []

    #Getting all the nicknames in a list

    def nick_append(nick, nicks, nicks_today_on_this_channel, track_users_on_channels):
        if track_users_on_channels and (nick not in nicks_today_on_this_channel):
            nicks_today_on_this_channel.append(nick) #not nicks as there are same nicks spread across multiple channels
            nicks.append(nick)
        elif nick not in nicks:
            nicks.append(nick)
        return nicks, nicks_today_on_this_channel


    for day_content_all_channels in log_dict.values():
        #traverse over data of different channels for that day
        
        channels_for_user_day = {}#empty for next day usage

        for day_content in day_content_all_channels:
            
            day_log = day_content["log_data"]
            channel_name = day_content["auxiliary_data"]["channel"]
            nicks_today_on_this_channel = []

            for i in day_log:
                # use regex to get the string between <> and appended it to the nicks list
                if(util.check_if_msg_line (i)):
                    m = re.search(r"\<(.*?)\>", i)
                    nick = util.correctLastCharCR(m.group(0)[1:-1])
                    nicks, nicks_today_on_this_channel = nick_append(nick, nicks, nicks_today_on_this_channel, track_users_on_channels)
                    
            ''' Forming list of lists for avoiding nickname duplicacy '''
            for line in day_log:
                if("Nick change:" in line):
                    old_nick = line.split()[3]
                    new_nick = line.split()[5]
                    nicks, nicks_today_on_this_channel = nick_append(old_nick, nicks, nicks_today_on_this_channel, track_users_on_channels)                
                    nicks, nicks_today_on_this_channel = nick_append(new_nick, nicks, nicks_today_on_this_channel, track_users_on_channels)    
                    
                        #nicks.append(new_nick)
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

            if track_users_on_channels:
                '''
                    Creating list of dictionaries nick_channel_dict of the format : 
                        [{'nickname':'rohan', 'channels':['[#abc', 0],['#bcd', 0]]},{}]
                '''
                considered_nicks = []
                if config.DEBUGGER:
                    print "Analysis on", (str(day_content["auxiliary_data"]["day"]) + "-" + str(day_content["auxiliary_data"]["month"])), channel_name
                
                for user in nicks_today_on_this_channel: 
                    f = 1
                    for nick_tuple in nick_same_list:
                        if user in nick_tuple:
                            user_nick = nick_tuple[0]
                            f = 0
                            break
                    if f:
                        user_nick = user

                    '''for channels of user on a day'''
                    if channels_for_user_day.has_key(user_nick) and channel_name not in channels_for_user_day[user_nick]:
                        channels_for_user_day[user_nick].append(channel_name)
                    else:
                        channels_for_user_day[user_nick] = [channel_name]

                    flag = 1
                    for dictionary in nick_channel_dict:
                        if dictionary['nickname'] == user_nick and user_nick not in considered_nicks:
                            index = searchChannel(channel_name, dictionary['channels'])
                            if index == -1:
                                dictionary['channels'].append([channel_name,1])
                            else:
                                dictionary['channels'][index][1]+=1
                            flag = 0
                            considered_nicks.append(user_nick)
                            break
                    if flag:
                        nick_channel_dict.append({'nickname':user_nick, 'channels': [[channel_name, 1]]})
                        considered_nicks.append(user_nick)

        channels_for_user.append(channels_for_user_day)
        

    for nick in nicks:
        for index in range(config.MAX_EXPECTED_DIFF_NICKS):
            if nick in nick_same_list[index]:
                break
            if not nick_same_list[index]:
                nick_same_list[index].append(nick)
                break

    if config.DEBUGGER:
        print "========> 30 on " + str(len(nicks)) + " nicks"
        print nicks[:30]
        print "========> 30 on " + str(len(nick_same_list)) + " nick_same_list"
        print nick_same_list[:30]

    if not track_users_on_channels:
        return [nicks, nick_same_list]

    else:
        for dicts in nick_channel_dict:
            nick = dicts['nickname']
            if nick not in nicks_hash:
                nicks_hash.append(nick)

            for channel in dicts['channels']:
                if channel[0] not in channels_hash:
                    channels_hash.append(channel[0])
        
        return [nicks, nick_same_list, channels_for_user, nick_channel_dict, nicks_hash, channels_hash]


def searchChannel(channel, channel_list):
    ans = -1
    i = 0
    for c_tuple in channel_list:
        if c_tuple[0] == channel:
            ans = i
            break
        i += 1 
    return ans
