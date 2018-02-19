import igraph
import lib.config as config


def infomap_igraph(ig_graph, net_file_location=None):
    """ 
        Performs igraph-infomap analysis on the nx graph
    
    Args:
        ig_graph(object): igraph graph object
        net_file_location(str): location to load graph from if not mentioned in ig_graph

    Returns:
        ig_graph: igraph object
        community.membership: result of infomap community analyis
    """

    if ig_graph is None:
        # give an option of loading a graph from .net file
        ig_graph = igraph.read(net_file_location, format="pajek")

    if ig_graph.es:
        community = ig_graph.community_infomap(edge_weights=ig_graph.es["weight"])
        codelength = community.codelength

        print "code-length:", codelength
        print "no. of communities: ", max(community.membership) + 1
        print community

        if config.DEBUGGER:
            for node in ig_graph.vs():
                print str(node.index)+"\t"+str(ig_graph.vs["id"][node.index])

        # http://stackoverflow.com/questions/21976889/plotting-communities-with-python-igraph
        return ig_graph, community

    else:
        return ig_graph, None
