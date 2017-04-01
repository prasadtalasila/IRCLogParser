import networkx as nx
import numpy as np
import igraph
import sys
sys.path.append('../lib')
import config
import vis


def infomap_igraph(ig_graph, net_file_location=None, reduce_graph=False):
    """ 
        Performs igraph-infomap analysis on the nx graph
    
    Args:
        ig_graph(object): igraph graph object
        net_file_location(str): location to load graph from if not mentioned in ig_graph
        reduce_graph(bool): toggle between enable/disable reduction

    Returns:
        ig_graph: igraph object
        community.membership: result of infomap community analyis
    """

    if ig_graph is None:
        # give an option of loading a graph from .net file
        ig_graph = igraph.Graph()
        ig_graph = igraph.read(net_file_location, format="pajek")

    if reduce_graph:
        ig_graph = select_top_vertices(ig_graph, "UU")

    community = ig_graph.community_infomap(edge_weights=ig_graph.es["weight"])
    codelength = community.codelength

    print "code-length:", codelength
    print "no. of communities: ", max(community.membership) + 1
    print community

    if config.DEBUGGER:
        for node in ig_graph.vs():
            print str(node.index)+"\t"+str(ig_graph.vs["id"][node.index])
            # print str(node.index)+"\t"+str(id_to_name_map[g.vs["id"][node.index]])

    # http://stackoverflow.com/questions/21976889/plotting-communities-with-python-igraph
    return ig_graph, community.membership


def select_top_vertices(ig_graph, pajek_type, top_channels=None, top_users=None, top_id_for_channels_and_user_graphs=None, top_id_for_user_graphs=None):
    """ 
    Reduces the ig_graph to only include top-nodes
    
    Args:
        ig_graph(object): igraph graph object
        pajek_type(str): UU/CU/CC

    Returns:
        ig_graph: updated (reduced) igraph graph object
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
        for node in ig_graph.vs():
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

    ig_graph.delete_vertices(nodes_to_delete)
    
    return ig_graph


def convert_id_name_community(max_hash, community_txt_file, hash_file_txt, reduced_hash_txt, reduced_community):
    """ 
    Converts communites from their ID representation to name for easier understanding
    
    Args:
        max_hash(int): max possible hash value
        community_txt_file(str): location fo the file having community analysis
        hash_file_txt(str): location fo the file having the non-reduced nick_hash
        reduced_hash_txt(str): location fo the file having the reduced nick_hash
        reduced_community(bool): switch b/w reduced and non reduced communities
    
    Returns:
        null
    """
    hash_value = [""]*max_hash

    with open(hash_file_txt) as f:
        content = f.readlines()
        for line in content:
            a, b = line.split()
            hash_value[int(a)] = b

    '''CHANGE COMMUNUITES FROM IDS TO NAME'''
    print "{: >20} {: >1}".format("NAME", "CommunityID")
    print "================================="

    if not reduced_community:
        c = 0
        with open(community_txt_file) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                b = int(b)
                if b != c:
                    print "---------------------------"
                    c += 1
                # print  hash_value[a]+"\t"+str(b)
                print "{: >20} {: >1}".format(hash_value[a], b)

    else:
        '''USED FOR REDUCED COMMUNITIES'''
        top_names = []
        with open(reduced_hash_txt) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                top_names.append(b)

        c = 0
        with open(community_txt_file) as f:
            content = f.readlines()
            for line in content:
                a, b = line.split()
                a = int(a)
                b = int(b)
                if b != c:
                    print "---------------------------"
                    c += 1
                if hash_value[a] in top_names:
                    print "{: >20} {: >1}".format(hash_value[a], b)