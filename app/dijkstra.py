# -*- coding: utf-8 -*-
import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import networkx as nx
from pyvis.network import Network

st.title('時空間情報処理特論 最終課題')
st.write('学修番号: 21860632')
st.write('氏名: 山口翔大')

stations=['奥多摩','拝島','八王子','京王八王子','立川','橋本','吉祥寺','明大前','新宿','東京','渋谷','東神奈川','川崎','品川']
sidx=list(range(len(stations)))
pos=list([[-10,-10],[-7,-7],[-7,-4],[-6,-5],[-4,-7],[-8,-1],[-1,-8],[2,-5],[5,-5],[14,-2],[5,-2],[8,7],[11,4],[11,1]])

w=[[ 0,51, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [51, 0,11, 0,11, 0, 0, 0, 0, 0, 0, 0, 0, 0],
   [ 0,11, 0, 8,11,12, 0, 0, 0, 0, 0, 0, 0, 0],
   [ 0, 0, 8, 0, 0, 0, 0,35, 0, 0, 0, 0, 0, 0],
   [ 0,11,11, 0, 0, 0,16, 0, 0, 0, 0, 0,41, 0],
   [ 0, 0,12, 0, 0, 0, 0,34, 0, 0, 0,37, 0, 0],
   [ 0, 0, 0, 0,16, 0, 0, 9,15, 0, 0, 0, 0, 0],
   [ 0, 0, 0,35, 0,34, 9, 0, 5, 0, 6, 0, 0, 0],
   [ 0, 0, 0, 0, 0, 0,15, 5, 0,13, 4, 0, 0,20],
   [ 0, 0, 0, 0, 0, 0, 0, 0,13, 0,25,36,16, 7],
   [ 0, 0, 0, 0, 0, 0, 0, 6, 4,25, 0, 0, 0,13],
   [ 0, 0, 0, 0, 0,37, 0, 0, 0,36, 0, 0,10, 0],
   [ 0, 0, 0, 0,41, 0, 0, 0, 0,16, 0,10, 0, 8],
   [ 0, 0, 0, 0, 0, 0, 0, 0,20, 7,13, 0, 8, 0],
  ]

st.write('ダイクストラ法を用いて、奥多摩駅から品川駅間の最短経路を表示します。')
st.write('もし経路の中で通りたくない駅があれば下記で選択して下さい。')

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
   pos=np.array(pos)
   
   for i in range(len(w)):
       w[i].pop(idx)
   w.pop(idx)

G =nx.Graph()
for i in range(len(stations)):
   for j in range(len(stations)):
       if w[i][j]>0:
           G.add_edge(i,j,weight=w[i][j])

start_idx=[i for i,s in enumerate(stations) if s=='奥多摩'][0]
goal_idx=[i for i,s in enumerate(stations) if s=='品川'][0]

path=nx.dijkstra_path(G,start_idx,goal_idx)
length=nx.dijkstra_path_length(G,start_idx,goal_idx)

path_pairs=list()
for i in range(len(path)-1):
   path_pairs.append([path[i],path[i+1]])

st.title(r'最短経路')
'最短経路の合計コストは、 '+str(length)+' [分]です。 (乗り換えに要する時間は含みません。)'

nt=Network("500px","800px",heading='')

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
components.html(source,height=1000,width=1300)
