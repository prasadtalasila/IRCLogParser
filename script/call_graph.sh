#!/bin/bash

REPO_LINK=https://github.com/davidfraser/pyan/archive/pre-python3.tar.gz
ubuntu_lib="$(pwd)/lib"
slack_lib="$(pwd)/lib/slack"
scummvm_lib="$(pwd)/lib/scummvm"

# download pyan and extract it
wget -v -O pyan.tar.gz $REPO_LINK
tar -xvf ./pyan.tar.gz && mv pyan-pre-python3 pyan


#generate call graph for ubuntu
python ./pyan/pyan.py --dot -c -e -n -g "$ubuntu_lib/analysis/network.py" "$ubuntu_lib/analysis/user.py" "$ubuntu_lib/analysis/channel.py" "$ubuntu_lib/analysis/community.py" \
"$ubuntu_lib/in_out/reader.py" "$ubuntu_lib/in_out/saver.py" "$ubuntu_lib/vis.py" "$ubuntu_lib/util.py" "$ubuntu_lib/config.py" "$ubuntu_lib/nickTracker.py"  > ubuntu.dot 
dot -Gnewrank=true -Tsvg ubuntu.dot >ubuntu.svg

#generate call graph for slack
python ./pyan/pyan.py --dot -c -e -n -g "$slack_lib/analysis/network.py" "$ubuntu_lib/analysis/user.py" "$slack_lib/analysis/channel.py" "$ubuntu_lib/analysis/community.py" \
"$slack_lib/in_out/reader.py" "$ubuntu_lib/in_out/saver.py" "$ubuntu_lib/vis.py" "$slack_lib/util.py" "$ubuntu_lib/config.py" "$slack_lib/nickTracker.py" > slack.dot
dot -Gnewrank=true -Tsvg slack.dot >slack.svg

#generate call graph for scummvm
python ./pyan/pyan.py --dot -c -e -n -g "$ubuntu_lib/analysis/network.py" "$ubuntu_lib/analysis/user.py" "$ubuntu_lib/analysis/channel.py" "$ubuntu_lib/analysis/community.py" \
"$ubuntu_lib/in_out/reader.py" "$ubuntu_lib/in_out/saver.py" "$ubuntu_lib/vis.py" "$ubuntu_lib/util.py" "$scummvm_lib/config.py" "$scummvm_lib/nickTracker.py" > scummvm.dot
dot -Gnewrank=true -Tsvg scummvm.dot >scummvm.svg

#Paste call graphs & dot files

echo "see ubuntu dot file: " && cat ubuntu.dot | curl -F 'clbin=<-' https://clbin.com
echo "see slack dot file: " && cat slack.dot | curl -F 'clbin=<-' https://clbin.com
echo "see scummvm dot file: " && cat scummvm.dot | curl -F 'clbin=<-' https://clbin.com
echo "see ubuntu image:" && curl -F "name=@ubuntu.svg" https://img.vim-cn.com/
echo "see slack image:" && curl -F "name=@slack.svg" https://img.vim-cn.com/
echo "see scummvm image:" && curl -F "name=@scummvm.svg" https://img.vim-cn.com/

#Cleanup
rm pyan.tar.gz
rm -rf pyan
rm *.dot
rm *.svg
