#!/bin/bash
########################
# Purpose: Create and upload the following
#		a) code profiling information
#		b) code dependency information 
# 
# Author: Prasad Talasila
# Date: 5-December-2017
# Invocation: At the command prompt, 
#		$bash profile.sh
# Dependencies: curl, mprof,sfood,sfood-graph,dot commands need to be available
# Input: python code base of the IRCLogParser project
# Output: graphs showing the code profile and code call sequence
########################

set -e

# perform code profiling
if ! (which mprof && which curl)
then
    echo "tools required for profiling are not installed"
    exit 1
fi

cd test
mprof clean
mprof run python -m unittest -v tests
cd ../profiler
python memory_profiler.py
echo "FOR UPDATED MEMORY CONSUMPTION, see image:"
curl -F "clbin=@memory_consumption.png" https://clbin.com


# generate function call graphs
if ! (which sfood && which sfood-graph && which dot)
then
    echo "tools required for generating function call graphs are not installed"
    exit 1
fi

sfood ../lib/analysis ../lib/analysis/* ../ext ../lib/in_out/* ../lib/config.py ../lib/nickTracker.py ../lib/util.py ../lib/vis.py ../sample.py | sfood-graph | dot -Tpng -Gsize=9,15\! -Gdpi=300 -o call-graph-dependency.png
echo "FOR UPDATED DEPENDENCY, see image:"
curl -F "clbin=@call-graph-dependency.png" https://clbin.com

exit 0
