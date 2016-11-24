import numpy as np

max_hash = 1000162

hash_value = [""]*max_hash


with open("cuhash.txt") as f:
	content = f.readlines()
	for line in content:
		a, b =  line.split()
		a = int(a)
		hash_value[a] = b

'''CHANGE COMMUNUITES FROM IDS TO NAME'''
print "{: >20} {: >1}".format("NAME", "CommunityID")
print "================================="
# c = 0
# with open("communitiesCU15.txt") as f:
# 	content = f.readlines()
# 	for line in content:
# 		a, b =  line.split()
# 		a = int(a)
# 		b = int(b)
# 		if b != c:
# 			print "---------------------------"
# 			c+=1
# 		# print  hash_value[a]+"\t"+str(b)
# 		print "{: >20} {: >1}".format(hash_value[a], b)







'''USED FOR REDUCED COMMUNITIES'''

top_names = []

with open("reducedHash.txt") as f:
	content = f.readlines()
	for line in content:
		a, b =  line.split()
		a = int(a)
		top_names.append(b)


c = 0
with open("communitiesCU15.txt") as f:
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