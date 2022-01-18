# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import networkx as nx
from pyvis.network import Network

st.title('ダイクストラ法')

stations=['東京','品川','渋谷','新宿','新横浜','横浜','小田原']
sidx=list(range(len(stations)))
pos=list([[-4,0],[-1,0],[0,2],[-1,-2],[2,0],[3,-2],[5,0]])

w=[[ 0, 8,16,15, 0, 0, 0],
  [ 8, 0,13,21,10,17, 0],
  [16,13, 0, 0,27, 0,78],
  [15,21, 0, 0, 0,33, 0],
  [ 0,10,27, 0, 0,13,15],
  [ 0,17, 0,33,13, 0,52],
  [ 0, 0,78, 0,15,52, 0],
  ]

# Radio buttonに用いる文字列
stlist=stations[1:-1]
stlist.append('除外しない')
removed_station=st.radio('除外する駅名',stlist)
idx=[i for i,s in enumerate(stations) if s==removed_station]
if not idx:
   pass
else:
   idx=idx[0]
   stations.pop(idx)
   sidx.pop(idx)
   pos.pop(idx)
   pos=np.array(pos) # 後のスライシングのためにnp.arrayにしておく
   
   for i in range(len(w)):
       w[i].pop(idx)
   w.pop(idx)

G =nx.Graph()
for i in range(len(stations)):
   for j in range(len(stations)):
       if w[i][j]>0:
           G.add_edge(i,j,weight=w[i][j])

start_idx=[i for i,s in enumerate(stations) if s=='東京'][0]
goal_idx=[i for i,s in enumerate(stations) if s=='小田原'][0]

path=nx.dijkstra_path(G,start_idx,goal_idx)
length=nx.dijkstra_path_length(G,start_idx,goal_idx)

path_pairs=list()
for i in range(len(path)-1):
   path_pairs.append([path[i],path[i+1]])

st.title(r'東京→小田原駅の最短経路')
'最短経路の合計コストは'+str(length)

nt=Network("500px","700px",heading='')

for i in range(len(stations)):
   nt.add_node(i,label=stations[i],x=int(pos[i][0]*55),y=int(pos[i][1]*60))
for n in nt.nodes:
   n.update({'physics':False})

for pair in G.edges:
   p=list(pair)
   col,wid=('red',10) if p in path_pairs else ('green',1)
   nt.add_edge(p[0],p[1],color=col,width=wid,label=w[p[0]][p[1]])
    
nt.show('test.html')
htmlfile=open('test.html','r',encoding='utf-8')
source=htmlfile.read()
components.html(source,height=800,width=900)
