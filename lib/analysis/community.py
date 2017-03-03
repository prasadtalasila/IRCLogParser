import networkx as nx
import igraph
import sys
sys.path.append('../lib')
import config
import vis


def infomap_igraph(nx_graph, net_file_location=None, reduce_graph=False):
    """ 
        Performs igraph-infomap analysis on the nx graph
    
    Args:
        nx_graph(object): networkx graph object
        net_file_location(str): location to load graph from if not mentioned in nx_graph
        reduce_graph(bool): toggle between enable/disable reduction

    Returns:
        nx_graph: networkx graph object
        community.membership: result of infomap community analyis
    """

    if nx_graph is None:
        # give an option of loading a graph from .net file
        nx_graph = igraph.Graph()
        nx_graph = igraph.read(net_file_location, format="pajek")

    if reduce_graph:
        nx_graph = select_top_vertices(nx_graph, "UU")

    community = nx_graph.community_infomap(edge_weights=nx_graph.es["weight"])
    codelength = community.codelength

    print "code-length:", codelength
    print "no. of communities: ", max(community.membership) + 1
    print community

    if config.DEBUGGER:
        for node in nx_graph.vs():
            print str(node.index)+"\t"+str(nx_graph.vs["id"][node.index])
            # print str(node.index)+"\t"+str(id_to_name_map[g.vs["id"][node.index]])

    # http://stackoverflow.com/questions/21976889/plotting-communities-with-python-igraph
    return nx_graph, community.membership



def select_top_vertices(nx_graph, pajek_type, top_channels=None, top_users=None, top_id_for_channels_and_user_graphs=None, top_id_for_user_graphs=None):
    """ 
    Reduces the nx_graph to only include top-nodes
    
    Args:
        nx_graph(object): networkx graph object
        pajek_type(str): UU/CU/CC

    Returns:
        nx_graph: updated (reduced) networkx graph object
    """

    # from reduced hashes, use degree analysis on edglelist to select top-nodes?
    
    '''
    default:
    top_channels = ["#ubuntu-devel", "#ubuntu-bugs", "#ubuntu", "#ubuntu-irc", "#xubuntu-devel", "#ubuntu-classroom", "#launchpad", "#kubuntu-devel", "#ubuntu-quality", "#ubuntu+1", "#ubuntu-release", "#ubuntu-meeting", "#kubuntu", "#ubuntu-locoteams", "#ubuntu-beginners", "#lubuntu", "#ubuntu-motu", "#ubuntu-discuss", "#ubuntu-on-air", "#xubuntu", "#ubuntu-community-team", "#ubuntu-uk", "#ubuntu-server", "#ubuntu-x", "#ubuntu-ops", "#ubuntu-phone", "#ubuntu-arm", "#ubuntu-kernel", "#ubuntu-desktop", "#ubuntu-unity"]
    top_users = ["benonsoftware", "ubottu", "jrib", "OerHeks", "dr_willis", "MoL0ToV", "FloodBot1", "cfhowlett", "dkessel", "DJones", "BluesKaj", "iceroot", "usr13", "bekks", "JoseeAntonioR", "Unit193", "kubine", "ubot2", "micahg", "sterna", "zdobersek", "CrazyLemon", "lynxlynxlynx", "czajkowski", "lifeless", "mlankhorst", "penguin42", "brobostigon", "AlanBell", "popey", "SilverSpace", "ubot5", "xiaoy", "cjohnston", "stgraber", "philipballew", "andol", "waltman", "holstein", "len-1304", "Wizard", "ScottK", "snap-l", "rick_h_", "ricotz", "mhall119", "bkerensa", "jcastro", "pleia2", "Scrimmer", "aleksei`", "[Raiden]", "artus", "ubot-it", "xangua", "jussi", "ikonia", "Pici", "Myrtti", "koegs", "hallyn", "davmor2", "roaksoax", "sarnold", "infinity", "mesquka", "wgrant", "tjaalton", "xnox", "lubotu3", "shadeslayer", "Tm_T", "Riddell", "SergioMeneses", "balloons", "ofan", "dobey", "Laney", "cjwatson", "jtaylor", "slangasek", "bdmurray", "tsimpson", "apw", "hazmat", "tumbleweed", "tgm4883", "gnomefreak", "cyphermox", "mgz", "didrocks", "hplc", "lordievader", "jibel", "seb128", "jodh", "ubot2`", "escott", "smartboyhw", "dholbach"]
    top_id_for_channels_and_user_graphs = ['1000001', '1000003', '1000005', '1000006', '1000007', '1000008', '1000011', '1000012', '1000014', '1000015', '1000017', '1000018', '1000020', '1000021', '1000023', '1000026', '1000027', '1000028', '1000030', '1000031', '1000032', '1000033', '1000034', '1000035', '1000036', '1000044', '1000047', '1000049', '1000050', '1000059', '2', '9', '31', '32', '37', '62', '71', '109', '168', '173', '179', '188', '219', '256', '381', '382', '392', '415', '442', '451', '453', '455', '459', '471', '473', '477', '478', '487', '489', '493', '505', '515', '571', '631', '639', '653', '668', '677', '680', '682', '694', '749', '779', '780', '788', '794', '796', '797', '799', '800', '805', '806', '809', '823', '857', '915', '940', '990', '1273', '1283', '1321', '1324', '1326', '1333', '1343', '1362', '1375', '1386', '1387', '1399', '1418', '1419', '1421', '1425', '1426', '1431', '1531', '1537', '1544', '1546', '1552', '1562', '1564', '1566', '1602', '1681', '1737', '2245', '2334', '2392', '3157', '3186', '4262', '4714', '4774', '4778', '5931', '6286', '8776', '9191']  
    top_id_for_user_graphs = ['2', '9', '31', '32', '37', '62', '71', '109', '168', '173', '179', '188', '219', '256', '381', '382', '392', '415', '442', '451', '453', '455', '459', '471', '473', '477', '478', '487', '489', '493', '505', '515', '571', '631', '639', '653', '668', '677', '680', '682', '694', '749', '779', '780', '788', '794', '796', '797', '799', '800', '805', '806', '809', '823', '857', '915', '940', '990', '1273', '1283', '1321', '1324', '1326', '1333', '1343', '1362', '1375', '1386', '1387', '1399', '1418', '1419', '1421', '1425', '1426', '1431', '1531', '1537', '1544', '1546', '1552', '1562', '1564', '1566', '1602', '1681', '1737', '2245', '2334', '2392', '3157', '3186', '4262', '4714', '4774', '4778', '5931', '6286', '8776', '9191'] 
    '''
    
    def delete_helper(top_parameter):
        nodes_to_delete = []
        for node in nx_graph.vs():
            if node["id"] not in top_parameter:
                nodes_to_delete.append(node.index)
        return nodes_to_delete

    if pajek_type == "CC":
        nodes_to_delete = delete_helper(top_channels)
    elif pajek_type == "CU":
        nodes_to_delete = delete_helper(top_id_for_channels_and_user_graphs) 
    elif pajek_type == "UU":
        nodes_to_delete = delete_helper(top_id_for_user_graphs) 
    else:
        print "ERROR"

    nx_graph.delete_vertices(nodes_to_delete)
    
    return nx_graph