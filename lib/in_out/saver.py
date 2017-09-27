import networkx as nx
import os
import csv
import errno
import sys
from networkx.readwrite import json_graph
import json
sys.path.append('../lib')
import lib.config as config
from shutil import copy2

def check_if_dir_exists(output_directory):
    """ 
        Creates the directory for output if not there

    Args:
        output_directory(str): directory where the output will be saved

    Returns:
       null

    """
    if not os.path.exists(os.path.dirname(output_directory)):
        try:
            os.makedirs(os.path.dirname(output_directory))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def draw_nx_graph(nx_graph, output_directory, output_file_name):
    """ 
        Generates graphs (png image) from networkx graph object

    Args:
        nx_graph(str): networkx graph object to be drawn
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
       null

    """
    
    check_if_dir_exists(output_directory) #create output directory if doesn't exist

    for u, v, d in nx_graph.edges(data=True):
        d['label'] = d.get('weight', '')

    output_file = output_directory + "/" + output_file_name + ".svg"
    if config.DEBUGGER:
        print "Generating", (output_file_name + ".svg")

    A = nx.nx.drawing.nx_agraph.to_agraph(nx_graph)
    A.layout(prog='dot')
    A.draw(output_file)


def save_net_nx_graph(nx_graph, output_directory, output_file_name):
    """ 
        Saves the input graph in pajek (.net) format

    Args:
        nx_graph(str): networkx graph object to be saved
        output_drectory(str): location to save graph
        output_file_name(str): name of the image file to be saved

    Returns:
       null

    """
    if config.DEBUGGER:
        print "Generating", (output_file_name + ".net")
    check_if_dir_exists(output_directory) #create output directory if doesn't exist
    nx.write_pajek(nx_graph, output_directory + "/" + output_file_name +".net")


def save_csv(matrix, output_directory, output_file_name):
    """ 
        Saves the input matrix as a CSV File

    Args:
        matrix(list):  an array containing data to be saved
        output_drectory(str): location to save graph
        output_file_name(str): name of the csv file to be saved

    Returns:
       null

    """
    if config.DEBUGGER:
        print "Generating", (output_file_name + ".csv")
    check_if_dir_exists(output_directory) #create output directory if doesn't exist
    output_file = output_directory + "/" + output_file_name +".csv"
    with open(output_file, 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_NONNUMERIC)
        for col in matrix:
            wr.writerow(col)

def save_js_arc(reduced_CC_graph, channels_hash, output_directory, output_file_name):
    """
        Saves the nx_graph as a js file with variable name communities, it is used in index.html to generate the arc graph

    Args:
        nx_graph: a networkx graph, here it is the reduced community community graph
        channels_hash(dict): list of channel names
        output_drectory(str): location where to save the file
        output_file_name(str): name of the file to be saved
        
    Returns:
       null
        
    """
    check_if_dir_exists(output_directory) #create output directory if doesn't exist
    copy2("../protovis/" + "arc_graph.html", output_directory) #copy required files to output_directory
    copy2("../protovis/" + "ex.css", output_directory)
    copy2("../protovis/" + "protovis-r3.2.js", output_directory)
    jsondict = json_graph.node_link_data(reduced_CC_graph)
    max_weight_val = max(item['weight'] for item in jsondict['links'])
    # the key names in the jsondict_top_channels are kept as the following so that index.html can render it
    jsondict_top_channels = {}
    jsondict_top_channels['nodes'] = [{'nodeName':channels_hash[int(node['id']) - config.STARTING_HASH_CHANNEL]} for node in jsondict['nodes']]
    jsondict_top_channels['links'] = [{'source': link['source'], 'target': link['target'],\
                                    'value': int(link['weight'] * config.EXPANSION_PARAMETER / float(max_weight_val))} for link in jsondict['links']]

    with open(output_directory + output_file_name, 'w') as f:
        f.write("var communities =")
        json.dump(jsondict_top_channels, f)
