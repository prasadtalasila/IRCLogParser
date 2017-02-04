import argparse
import Parser
import glob
import os
import sys

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Neccassary Arguments
    parser.add_argument('funcPerform', help='which function / all', type=str)

    # Optional arguments
    parser.add_argument("-i", "--in_directory", help="log_directory", type=str, default="/home/rohan/parser_files/2013/")
    parser.add_argument("-c", "--channel", help="channel_name", type=str, default="#kubuntu-devel")
    parser.add_argument("-o", "--out_directory", help="output_directory", type=str, default="/home/rohan/parser_files/Output/")
    parser.add_argument("-f", "--from", help="start_date : dd-mm", type=str, default="1-1")
    parser.add_argument("-t", "--to", help="end_date : dd-mm", type=str, default="31-1")

    # Parse arguments
    args = parser.parse_args()

    return args

if __name__ == '__main__':
    # Parse the arguments
    args = parseArguments().__dict__

    # Raw print arguments
    print "============================================"
    print "You are running the script with arguments: "
    print "["+args["funcPerform"]+" : "+args["channel"]+" ] "+args["from"]+" : "+args["to"]
    print "IN : "+args["in_directory"]
    print "OUT : " +args["out_directory"]
    print "============================================"

    startingDate, startingMonth = map(int, args["from"].split("-"))
    endingDate, endingMonth = map(int, args["to"].split("-"))
    function_input = args['funcPerform']


    methods = {
        'nickChange': Parser.createNickChangesGraph, 
        'messageTime': Parser.createMessageTimeGraph, 
        'messageNumber': Parser.createMessageNumberGraph,
        'messageNumberBins': Parser.createMessageNumberBinsCSV, 
        'degNodeNumberCSV': Parser.degreeNodeNumberCSV,
        'aggregate': Parser.createAggregateGraph,   
        'channel-nick': Parser.createChannelsOfNickGraph, 
        'keyWords': Parser.keyWordsCluster_KMeansTFIDF,
        'responseTime': Parser.findResponseTime, 
        'convLenRefresh': Parser.findConvLength_ConvRefreshTime,
    }

    attr = {
        "log_directory": args["in_directory"], 
        "channel_name": args["channel"], 
        "output_directory": args["out_directory"], 
        "startingDate": startingDate, 
        "startingMonth": startingMonth, 
        "endingDate": endingDate, 
        "endingMonth": endingMonth
    }

    if function_input in methods.keys():
        ret = methods[function_input](**attr)
    else:
        if function_input == "all" or function_input =="ALL":
            for function in methods.keys():
                methods[function](**attr)
        else:
            print "------- ERROR ---------"
            raise Exception("No such function '" +function_input+ "' defined")