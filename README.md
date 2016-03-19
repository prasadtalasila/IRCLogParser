#IRC Log Parser

Import `Parser.py` in your file to use the library functions.

Functions presently implemented are:
- **createNickChangesGraph** - creates a graph which tracks the nick changes of the users, each edge has a time stamp denoting the time at which the nick was changed
- **createMessageTimeGraph** - creates a directed graph where each edge denotes a message sent from a user to another with the stamp denoting the time at which the message was sent.
- **createMessageNumberGraph** - creates a directed graph with each edge having an associated weight which denotes the number of messages exchanged between users for that particular day.
- **createMessageNumberBinsCSV** - creates a CSV file which tracks the number of message exchanged in a channel for 48 bins of half an hour each distributed all over the day aggragated over the year. 
- **createAggregateGraph** - creates a directed graph for a longer frame of time with each node representing an IRC user, and each directed edge has a weight which mentions the number messages sent and recieved by that user in the selected time frame.
- **createChannelsOfNickGraph** - creates a directed graph for each nick, each edge from which points to the IRC Channels that nick has participated in. (Nick changes are tracked here and only the initial nick is shown if a user changed his nick) 

`TestingScript.py` demonstrates the use of these funtions.
