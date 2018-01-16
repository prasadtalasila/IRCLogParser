import networkx as nx
import numpy as np
import igraph
import sys
import lib.config as config
import lib.vis as vis


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
