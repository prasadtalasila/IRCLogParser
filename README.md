#IRC Log Parser

Import `Parser.py` in your file to use the library functions.

Functions presently implemented are:
- **createNickChangesGraph** - creates a graph which tracks the nick changes of the users, each edge has a time stamp denoting the time at which the nick was changed
- **createMessageTimeGraph** - creates a directed graph where each edge denotes a message sent from a user to another with the stamp denoting the time at which the message was sent.
- **createMessageNumberGraph** - creates a directed graph with each edge having an associated weight which denotes the number of messages exchanged between users for that particular day.
- **createMessageNumberBinsCSV** - creates a CSV file which tracks the number of message exchanged in a channel for 48 bins of half an hour each distributed all over the day aggragated over the year. 
- **createAggregateGraph** - creates a directed graph for a longer frame of time with each node representing an IRC user, and each directed edge has a weight which mentions the number messages sent and recieved by that user in the selected time frame.
- **createChannelsOfNickGraph** - creates a directed graph for each nick, each edge from which points to the IRC Channels that nick has participated in. (Nick changes are tracked here and only the initial nick is shown if a user changed his nick) 
- **createKeyWords** - outputs the keywords for each user on a particular channel after normalising the frequency and removing the common stop words.
- **degreeMessageNumberCSV** - creates two csv files having no. of nodes with a certain in and out-degree for number of messages respectively
- **degreeNodeNumberCSV** - creates two csv files having no. of nodes with a certain in and out-degree for number of nodes it interacted with, respectively. Also gives graphs for log(degree) vs log(no. of nodes) and tries to find it's equation by crve fitting
- **svdOnKeywords** - uses createKeyWords function and then tries to form clusters by extracting more meaningful keywords. Performs a  Singular Value Decomposition(SVD) after doing a Term Frequency–Inverse Document Frequency(TF-IDF).
- **findResponseTime** - finds the response time of a message i.e. the best guess for the time at which one can expect a reply for his/her message.
- **findConvLength_ConvRefreshTime** - Calculates the conversation length that is the length of time for which two users communicate i.e. if a message is not replied to within RT, then it is considered as a part of another conversation.This function also calculates the conversation refresh time. For a pair of users, this is the time when one conversation ends and another one starts.
- **createGephiTimelapseCSV** - Produces node and edge csv files that contain information relevant for creating a timelapse of user interactions on Gephi. Most importantly, these csv files contain the node/edge appear and disappear times and can easily be imported into Gephi.
- **implementWithIgraphs** - This performs various tasks utilizing the python-igraphs library. Tasks include producing graphs, writing to pajek, obtaining adjacency matrix, community detection, calculating modularity,rescaling edge width, assigning graph attributes such as color etc.

`TestingScript.py` demonstrates the use of these funtions.
