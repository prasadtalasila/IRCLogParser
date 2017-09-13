#!/bin/bash

apt-get update
apt-get install -y python-setuptools python-dev build-essential
easy_install pip
pip install --upgrade virtualenv
pip install --upgrade pip			#does not upgrade

# install graphviz, igraph and their python bindings
apt-get install -y libxml2-dev build-essential
apt-get install -y libcdt5 libcgraph6 libgd3 libgvc6 libgvpr2 libxaw7 libxmu6 libxt6 fonts-liberation libgraphviz-dev libcgraph6 python-dbg libjs-sphinxdoc
apt-get install -y graphviz graphviz-dev graphviz-doc python-pygraphviz python-pygraphviz-dbg python-pygraphviz-doc 
apt-get install -y libigraph0v5 libigraph0-dev
apt-get install -y python-tk
apt-get install -y python-scipy
apt-get install libcairo2-dev
apt-get install libffi-dev
pip install cairocffi

# install IRCLogParser
pip -v install -e .
