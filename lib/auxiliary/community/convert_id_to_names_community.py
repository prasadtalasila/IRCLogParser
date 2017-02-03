import numpy as np

def convert_id_name_community(community_txt_file, hash_file_txt, reduced_hash_txt, REDUCED_COMMUNITY)
	max_hash = 1000162
	hash_value = [""]*max_hash

	with open(hash_file_txt) as f:
		content = f.readlines()
		for line in content:
			a, b =  line.split()
			a = int(a)
			hash_value[a] = b

	'''CHANGE COMMUNUITES FROM IDS TO NAME'''
	print "{: >20} {: >1}".format("NAME", "CommunityID")
	print "================================="

	if not REDUCED_COMMUNITY:
		c = 0
		with open(community_txt_file) as f:
			content = f.readlines()
			for line in content:
				a, b =  line.split()
				a = int(a)
				b = int(b)
				if b != c:
					print "---------------------------"
					c+=1
				# print  hash_value[a]+"\t"+str(b)
				print "{: >20} {: >1}".format(hash_value[a], b)

	else:
		'''USED FOR REDUCED COMMUNITIES'''

		top_names = []
		with open(reduced_hash_txt) as f:
			content = f.readlines()
			for line in content:
				a, b =  line.split()
				a = int(a)
				top_names.append(b)


		c = 0
		with open(community_txt_file) as f:
			content = f.readlines()
			for line in content:
				a, b =  line.split()
				a = int(a)
				b = int(b)
				if b != c:
					print "---------------------------"
					c+=1
				if hash_value[a] in top_names:	
					print "{: >20} {: >1}".format(hash_value[a], b)