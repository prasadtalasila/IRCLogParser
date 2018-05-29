"""
log_regex = {
    event(nick_change, directed_message etc) : {
    'regex' : regex (regular expression against which the match shall be made)
    'groups' : {
        'tag' : group no as in the regular expression
        # https://docs.python.org/2/howto/regex.html#grouping
        }
    }
}
"""

log_regex = {
    'nick_change': {
        'regex': r'^\[\d{2}:\d{2}\] Nick change: (\S*) -> (\S*)',
        'groups': {
            'old_nick': 1,
            'new_nick': 2
        }
    },
    'directed_message': {
        'regex': r'^\[(\d{2}:\d{2})\] \<(\S*)\> (\S*): (.*)',
        'groups': {
            'time': 1,
            'sender_nick': 2,
            'receivers': 3,
            'message': 4
        }
    },
    'undirected_message': {
        'regex': r'^\[(\d{2}:\d{2})\] \<(\S*)\> (.*)',
        'groups': {
            'time': 1,
            'sender_nick': 2,
            'message': 3
        }
    }
}