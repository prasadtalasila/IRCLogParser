#We do the same operations usually performed with networkx, but this time with python-igraphs. Igraphs is useful as it can achieve various things that networkx cant. It can also write a graph in various diffent formats useful for tools such as Infomaps and Gephi.

import os.path
import re
import networkx as nx
from networkx.algorithms.components.connected import connected_components
import numpy as np
import matplotlib.pyplot as plt
import pylab
import pygraphviz as pygraphviz
import igraph
from igraph import *

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

def to_graph(l):
    G = nx.Graph()
    for part in l:
        # each sublist is a bunch of nodes
        G.add_nodes_from(part)
        # it also imlies a number of edges:
        G.add_edges_from(to_edges(part))
    return G

def to_edges(l):
    """ 
        treat `l` as a Graph and returns it's edges 
        to_edges(['a','b','c','d']) -> [(a,b), (b,c),(c,d)]
    """
    it = iter(l)
    last = next(it)

    for current in it:
        yield last, current
        last = current    


x=[[] for i in range(500)]
nicks = [] #list of all the nicknames

xarr=[[] for i in range(5000)]
for i in xrange(0,5000):
 xarr[i].append(0)


for iterator in range(1,13):
 for fileiterator in range(1,32):
  if(fileiterator<10):  
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0" 
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
  else:
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"  
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
  if not os.path.exists(sttring):
   continue 
  with open(sttring) as f:
      content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel   
 
  send_time = [] #list of all the times a user sends a message to another user
  picks = []
  channel= "#kubuntu-devel" #channel name
   
  
#code for getting all the nicknames in a list
  for i in content:
   if(i[0] != '=' and "] <" in i and "> " in i):
    m = re.search(r"\<(.*?)\>", i)
    if m.group(0) not in picks:                       
     picks.append(m.group(0))   #used regex to get the string between <> and appended it to the nicks list



  for i in xrange(0,len(picks)):
   if picks[i][1:-1] not in nicks:
    nicks.append(picks[i][1:-1])     #removed <> from the nicknames
    
  for i in xrange(0,len(nicks)):
   if(nicks[i][len(nicks[i])-1]=='\\'):
    nicks[i]=nicks[i][:-1]
    nicks[i]=nicks[i]+'CR'

  for j in content:
   if(j[0]=='=' and "changed the topic of" not in j):
    line1=j[j.find("=")+1:j.find(" is")]
    line2=j[j.find("wn as")+1:j.find("\n")]
    line1=line1[3:]
    line2=line2[5:]
    if(line1[len(line1)-1]=='\\'):
     line1=line1[:-1]
     line1=line1 + 'CR' 
    if(line2[len(line2)-1]=='\\'):
     line2=line2[:-1]
     line2=line2 + 'CR'
    if line1 not in nicks:
     nicks.append(line1)
    if line2 not in nicks:
     nicks.append(line2)
   
  
  
    
 #code for forming list of lists for avoiding nickname duplicacy

  
  for line in content:
   if(line[0]=='=' and "changed the topic of" not in line):
    line1=line[line.find("=")+1:line.find(" is")]
    line2=line[line.find("wn as")+1:line.find("\n")]
    line1=line1[3:]
    line2=line2[5:]
    if(line1[len(line1)-1]=='\\'):
     line1=line1[:-1]
     line1=line1 + 'CR' 
    if(line2[len(line2)-1]=='\\'):
     line2=line2[:-1]
     line2=line2 + 'CR'
    for i in range(500):
     if line1 in x[i] or line2 in x[i]:
      if line1 in x[i] and line2 not in x[i]:
       x[i].append(line2)
       break
      if line2 in x[i] and line1 not in x[i]: 
       x[i].append(line1)
       break
      if line2 in x[i] and line1 in x[i]:
       break  
     if not x[i]:
      x[i].append(line1)
      x[i].append(line2)
      break


  

#print(x)  
for ni in nicks:
 for ind in range(500):
  if ni in x[ind]:
   break
  if not x[ind]:
   x[ind].append(ni)
   break

#print("*********************x**********************************")
#print(x)


G = to_graph(x)
L = connected_components(G)

 

for i in range(1,len(L)+1):
 L[i-1] = [i]+L[i-1]

#print(L)
 
#Uptil here we have all the nicks of the same user clustered together.

for iterator in range(1,2):
 for fileiterator in range(1,32):
  if(fileiterator<10):  
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/0" 
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt"
  else:
   sttring="/home/dhruvie/LOP/2013/"+str(iterator)+"/"  
   sttring=sttring+str(fileiterator)+"/#kubuntu-devel.txt" 
  if not os.path.exists(sttring):
   continue 
  with open(sttring) as f:
      content = f.readlines()                               #contents stores all the lines of the file kubunutu-devel   
  print(sttring)
  
  for line in content:
   flag_comma = 0
   if(line[0] != '=' and "] <" in line and "> " in line):
    m = re.search(r"\<(.*?)\>", line)
    var = m.group(0)[1:-1]
    if(var[len(var)-1]=='\\'):
     var=var[:-1]
     var=var + 'CR' 
    for d in range(len(nicks)):
     if var in L[d]:
      pehla = L[d][0]
      break
      

    for i in nicks:
     data=[e.strip() for e in line.split(':')]
     data[1]=data[1][data[1].find(">")+1:len(data[1])]
     data[1]=data[1][1:]
     if not data[1]:
      break
     for ik in xrange(0,len(data)):
      if(data[ik] and data[ik][len(data[ik])-1]=='\\'):
       data[ik]=data[ik][:-1]
       data[ik]=data[ik] + 'CR'
     for z in data:
      if(z==i):
       send_time.append(line[1:6])
       if(var != i):  
        for d in range(len(nicks)):
         if i in L[d]:
          second=L[d][0]
          break
          
        for rt in xrange(0,5000):
         if (pehla in xarr[rt] and second in xarr[rt]):
          if (pehla == xarr[rt][1] and second == xarr[rt][2]):
           xarr[rt][0]=xarr[rt][0]+1
           break
         if(len(xarr[rt])==1):
          xarr[rt].append(pehla)
          xarr[rt].append(second)
          xarr[rt][0]=xarr[rt][0]+1
          break
       
     if "," in data[1]: 
      flag_comma = 1
      data1=[e.strip() for e in data[1].split(',')]
      for ij in xrange(0,len(data1)):
       if(data1[ij] and data1[ij][len(data1[ij])-1]=='\\'):
        data1[ij]=data1[ij][:-1]
        data1[ij]=data1[ij] + 'CR'
      for j in data1:
       if(j==i):
        send_time.append(line[1:6])
        if(var != i):   
         for d in range(len(nicks)):
          if i in L[d]:
           second=L[d][0]
           break
          
         for rt in xrange(0,5000):
          if (pehla in xarr[rt] and second in xarr[rt]):
           if (pehla == xarr[rt][1] and second == xarr[rt][2]):
            xarr[rt][0]=xarr[rt][0]+1
            break
          if(len(xarr[rt])==1):
           xarr[rt].append(pehla)
           xarr[rt].append(second)
           xarr[rt][0]=xarr[rt][0]+1
           break

     if(flag_comma == 0):
      search2=line[line.find(">")+1:line.find(", ")] 
      search2=search2[1:]
      if(search2[len(search2)-1]=='\\'):
       search2=search2[:-1]
       search2=search2 + 'CR' 
      if(search2==i):
       send_time.append(line[1:6])
       if(var != i):
        for d in range(len(nicks)):
         if i in L[d]:
          second=L[d][0]
          break
         
        for rt in xrange(0,5000):
         if (pehla in xarr[rt] and second in xarr[rt]): 
          if (pehla == xarr[rt][1] and second == xarr[rt][2]):
           xarr[rt][0]=xarr[rt][0]+1
           break
         if(len(xarr[rt])==1):
          xarr[rt].append(pehla)
          xarr[rt].append(second)
          xarr[rt][0]=xarr[rt][0]+1
          break
      
  
G = Graph(directed=True)  #graph with multiple directed edges between clients used 

#Notice how the syntax changes with python-igraphs as compared to networkx.

vertex1=[]
edge1=[]
for fin in xrange(0,5000):
 if(len(xarr[fin])==3):
  if(str(xarr[fin][1]) not in vertex1):
   G.add_vertex(str(xarr[fin][1]))
   vertex1.append(str(xarr[fin][1]))
  if(str(xarr[fin][2]) not in vertex1):
   G.add_vertex(str(xarr[fin][2]))
   vertex1.append(str(xarr[fin][2]))  #vertex1 contains the vertex names.
  edge1.append(xarr[fin][0])          #edge1 contains the edge weights
  G.add_edge(str(xarr[fin][1]),str(xarr[fin][2]))  

G.vs['name'] = vertex1
G.es['label'] = edge1       #Here we add all the labels like color,name,id,weights etc that we want in our graph
G.es['weight'] = edge1
G.vs['id'] = G.vs['name']
G.es['width'] = edge1

#print(vertex1)
#print(xarr)
#G.write_adjacency("adja_wholeyear.csv",sep=',') #Igraphs has a simple function for printing the adjacency matrix of a graph to a csv file.
m_brilli = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_pajek_fawad.net"
G.write_pajek(m_brilli)  #writes a graph in pajek format.

'''
n_brilli=channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_fourth.png"
print("Here I am")
G.es.select(weight=1).delete()
print(edge1)
edge1 = remove_values_from_list(edge1, 1)
print(edge1)

#we can delete edges with certain weights like 1 in above case. We can delete a list of vertices as shown below. We can append edges too.
#Everything is quite flexible with python-igraphs

list_ver=["124","137","81","199","1","38","198","139","185","146","109","91","254","82","70","111","420","223","327","214","4"]
G.delete_vertices(list_ver)
edge1.append(1)
G.add_edge("196","460") 
edge1.append(1) 
G.add_edge("460","196") 
edge1.append(1) 
G.add_edge("151","259")
edge1.append(1)
G.add_edge("259","151")
edge1.append(1)
G.add_edge("338","121")
m_brilli = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_pajek_patanahi.net"
'''

'''
#We can give different colors to specific vertices as shown below. color is an attribute for both vertex and edge.
G.vs[39]['color'] = 'green'
G.vs[38]['color'] = 'green'
G.vs[27]['color'] = 'cyan'
G.vs[6]['color'] = 'cyan'
G.vs[43]['color'] = 'blue'
G.vs[42]['color'] = 'blue'
G.vs[26]['color'] = 'orange'
G.vs[20]['color'] = 'orange'
#plot(G, n_brilli,edge_width=rescale(edge1,out_range=(1, 15)),layout = G.layout_fruchterman_reingold(), edge_arrow_size=0.5, vertex_size=8)
m_brilli = channel+"_"+str(fileiterator)+"_"+str(iterator)+"_2013_simpledirectedgraph_pajek_patanahi.net"


print("\n")
#print(n_brilli)


#G.write_pajek(m_brilli)


#print(G.es['weight'])
cl = G.community_infomap(edge_weights=G.es['weight'])     #igraphs has its own community detection infomaps function.
print(cl)
cl.es.select(weight=1).delete()
#print(max(cl.membership))
  
#Z=cl.subgraph(0)      # We can get subgraphs of a graph and work on it too.
#print(Z)


#Z.write_pajek("Zkapajek.net")
#SCL=Z.community_infomap(edge_weights=Z.es['weight'],trials=10)
#print(SCL)

#print(max(SCL.membership))
#sys.exit(1)
#print(G.modularity(cl.membership,weights=edge1))
#print("modularity")
#print(cl.modularity)


#We can get the modularity value of a graph and then also plot it as shown below. Igraph also offers various different layouts. Its exciting to play
#around with them to get a better idea of them.

color_list = ['blue','red','green','cyan','pink','orange','grey']
layout1 = G.layout("lgl")


plot(cl, "graph_Janurrr_subgraph_lgl_final_last.png", edge_width=rescale(G.es['weight'],out_range=(1, 15)), layout=layout1, edge_arrow_size=0.5,
   vertex_color=[color_list[x] for x in cl.membership],
   vertex_size=25)


'''






