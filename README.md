# IRCLogParser

[![Build Status](https://travis-ci.org/prasadtalasila/IRCLogParser.svg?branch=dev)](https://travis-ci.org/prasadtalasila/IRCLogParser)
[![Maintainability](https://api.codeclimate.com/v1/badges/211e8675682e2d345d8b/maintainability)](https://codeclimate.com/github/prasadtalasila/IRCLogParser/maintainability)
[![Requirements Status](https://requires.io/github/prasadtalasila/IRCLogParser/requirements.svg?branch=dev)](https://requires.io/github/prasadtalasila/IRCLogParser/requirements/?branch=dev)
[![codecov](https://codecov.io/gh/prasadtalasila/IRCLogParser/branch/dev/graph/badge.svg)](https://codecov.io/gh/prasadtalasila/IRCLogParser)

The objective of this project is to utilize social network analysis techniques to examine the relationships between actors on the Internet Relay Chat(IRC) social networking service. The IRCLogParser is an application that accepts IRC log files from different channels and parses them to analyse the principles of interaction between IRC users. Study of these interactions on different levels helps us in deriving the local and global communication patterns between users on different channels. Therefore, IRCLogParser draws its inspiration from various fields such as data mining, graph theory and inferential modeling in order to form predictive models that help in understanding certain intricate characteristics of a social network. This involves analyzing graphs with IRC users(nodes) and their connections(edges), to study the details about various network graph properties such as density, size, node centrality, degree, connectedness etc.


<img src="https://raw.githubusercontent.com/wiki/prasadtalasila/IRCLogParser/sample_images/kubuntu-devel_4_10_2013_conversation.png" width="400px"></img>
<img src="https://raw.githubusercontent.com/wiki/prasadtalasila/IRCLogParser/sample_images/infomap_CU.png" width="400px"></img>


## Installation

Follow the steps to install dependencies and IRCLogParser library:-
```shell
> git clone https://github.com/prasadtalasila/IRCLogParser.git
> cd IRCLogParser
> sudo script/install
```

Ideally the installation takes not more than 10 minutes.


## Usage

The library's working has been modularised into many modules namely input, analysis, output, visualisation and validation. The [sample.py file](./sample.py) very comprehensively presents how one can use IRCLogParser for parsing and analysis.

A page on typical workflow for using IRCLogParser also exists on the documentation [here](http://prasadtalasila.github.io/IRCLogParser/TypicalUsage.html).

To run and test the sample program, execute in root directory :
`python sample.py`


## Documentation

IRCLogParser uses [Sphinx Python Documentation Generator](http://www.sphinx-doc.org/en/stable/) for generating documentation of the library.
The documentation is auto-generated from the commits made on the [dev](https://github.com/prasadtalasila/IRCLogParser/tree/dev) branch. Please see the [online documentation](http://prasad.talasila.in/IRCLogParser/).




## License

IRCLogParser is available under the [GPL v3.0](./LISENCE.md)
