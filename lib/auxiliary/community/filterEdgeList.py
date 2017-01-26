# from  more_itertools import unique_everseen
# from collections import OrderedDict
import numpy as np

def filterEdgeList(edgeList, how_many_in_new_adjaceny)
	max_hash = 16000
	max_degree_possible = 10000

	my_list = []
	degrees = [0]*max_hash
	with open(edgeList) as f:
		content = f.readlines()
		for line in content:
			a, b =  line.split()
			my_list.append(int(a))
			my_list.append(int(b))
			degrees[int(a)]+=1
			degrees[int(b)]+=1

	# print my_list
	print "done pre comp"
	print "max_hash", max(my_list)

	max_hash = max(my_list)

	# print "======DEGREE====="

	# print "NODE\tDEGREE"
	# for i in range(max_hash):
	# 	print str(i)+"\t"+str(degrees[i])

	# nodes_with_TOTAL_degree = [0]*max_degree_possible
	# print "======DEGREE ANALYSIS======="
	# for degree in degrees:
	# 	nodes_with_TOTAL_degree[degree]+=1

	# print "========= TOTAL DEGREE ======="
	# for i in xrange(max_degree_possible):
	# 	print "deg"+str(i)+'\t'+str(nodes_with_TOTAL_degree[i])

	degrees = np.array(degrees)

	print "========TOP "+str(how_many_in_new_adjaceny)+" NODES ON BASIS OF DEGREE ========"

	top_nodes = list(degrees.argsort()[::-1])[:how_many_in_new_adjaceny]

	print top_nodes

	print "=======UPDATED ADJACENY LIST ON THE BASIS OF ABOVE NODES======="

	with open(edgeList) as f:
		content = f.readlines()
		for line in content:
			a, b =  map(int,line.split())
			if a in top_nodes and b in top_nodes:
				print str(a)+"\t"+str(b)