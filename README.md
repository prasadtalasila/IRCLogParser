#IRC Log Parser

[![Code Climate](https://codeclimate.com/github/prasadtalasila/IRCLogParser/badges/gpa.svg)](https://codeclimate.com/github/prasadtalasila/IRCLogParser)    


The objective of this project is to utilize social network analysis techniques to examine the relationships between actors on the Internet Relay Chat(IRC) social networking service. The IRCLogParser is an application that accepts IRC log files from different channels and parses them to analyse the principles of interaction between IRC users. Study of these interactions on different levels helps us in deriving the local and global communication patterns between users on different channels. Therefore, IRCLogParser draws its inspiration from various fields such as data mining, graph theory and inferential modeling in order to form predictive models that help in understanding certain intricate characteristics of a social network. This involves analyzing graphs with IRC users(nodes) and their connections(edges), to study the details about various network graph properties such as density, size, node centrality, degree, connectedness etc.

![img](https://github.com/prasadtalasila/IRCLogParser/raw/master/archive/sample_img/kubuntu-devel_4_10_2013_conversation.png)


## Usage

Import `parser.py` in your file to use the library functions.

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

## Documentation

You can view the documentation for IRCLogParser by [clicking here](http://rohangoel96.github.io/IRCLogParser).
