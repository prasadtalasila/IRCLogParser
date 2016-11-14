import csv
import numpy as np

with open('1_1reduced_CU_adjacency_matrix.csv', 'rb') as f:
    reader = csv.reader(f)
    temp = list(reader)


my_matrix = []
for line in temp:
	my_matrix.append(map(float, line))

# print my_matrix


original_row_order = [""]*30
original_column_order = [""]*100

with open("reducedHash.txt") as f:
	content = f.readlines()
	for line in content:
		a, b =  line.split()
		a = int(a)
		if b[0] == "#":
			original_row_order[a] = b
		else:
			original_column_order[a] = b

print len(original_row_order)
print len(original_column_order)

required_row_order = []
required_column_order = []

with open("updatedCUcommunity_withNamesofNodesREDUCED") as f:
	content = f.readlines()
	for line in content:
		a, b =  line.split()
		if a[0] == "#":
			required_row_order.append(a)
		else:
			required_column_order.append(a)

for name in original_row_order:
	if name not in required_row_order:
		required_row_order.append(name)


for name in original_column_order:
	if name not in required_column_order:
		required_column_order.append(name)

print len(required_row_order)
print len(required_column_order)

print required_row_order
print required_column_order

old_matrix = np.array(my_matrix)

new_matrix = np.empty((len(required_row_order), len(required_column_order)))
new_matrix[:]=-1

'''RE ARRANGE MATRIX ACCORING TO COMM'''

'''ROWS'''
for i in range(len(required_row_order)):
	new_matrix[i,:] = old_matrix[original_row_order.index(required_row_order[i]),:]

'''COLUMNS'''
for i in range(len(required_column_order)):
	new_matrix[:, i] = old_matrix[:,original_column_order.index(required_column_order[i])]


np.savetxt("foo.csv", new_matrix, delimiter=",")