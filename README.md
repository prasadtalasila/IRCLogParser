#IRC Log Parser

The objective of this project is to utilize social network analysis techniques to examine the relationships between actors on the Internet Relay Chat(IRC) social networking service. The IRCLogParser is an application that accepts IRC log files from different channels and parses them to analyse the principles of interaction between IRC users. Study of these interactions on different levels helps us in deriving the local and global communication patterns between users on different channels. Therefore, IRCLogParser draws its inspiration from various fields such as data mining, graph theory and inferential modeling in order to form predictive models that help in understanding certain intricate characteristics of a social network. This involves analyzing graphs with IRC users(nodes) and their connections(edges), to study the details about various network graph properties such as density, size, node centrality, degree, connectedness etc.

![img](https://github.com/prasadtalasila/IRCLogParser/raw/master/Archive/sample_img/kubuntu-devel_4_10_2013_conversation.png)


##Functionality

Import `parser.py` in your file to use the library functions.

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
- **keyWordsCluster_KMeansTFIDF** - Used `createKeyWords` to form clusters of words post TF IDF (optional).

<hr>

## Usage

`module.py` can be used in the command line to run various methods provided by the library.

It has the following parameters:

**Neccessary Arguments**
- `funcPerform` : which method to run / all

**Optional arguments**
- `(-i) --in_directory` : log_directory
- `(-c) --channel` : channel_name
- `(-o) --out_directory` : output_directory
- `(-f) --from` : start_date in dd-mm format
- `(-t) --to` : end_date in dd-mm format


A typical usage of the module is as follows:
`python module.py "nickChange" -f="1-1" -t="31-1"`