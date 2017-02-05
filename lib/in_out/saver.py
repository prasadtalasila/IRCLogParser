import networkx as nx
import os

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

    output_file = output_directory + "/" + output_file_name + ".png"
    print "Generating " + output_file
    print "Please wait ...."

    A = nx.nx_agraph.to_agraph(nx_graph)
    A.layout(prog='dot')
    A.draw(output_file)

    print "Done Generating" + output_file
