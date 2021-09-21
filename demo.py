# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:07:41 2021

@author: Segal Raz
"""
import argparse
import SOAR_alg as soar
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout



def Add_InNetwork_Capacity(g):
   for node in g.nodes:
       att={node:{'Jobs':{'number':0,'list':[]}}}
       att[node]['color']='red'
       nx.set_node_attributes(g,att)
def AvalbiltyCalc(g,cap):
    avalbilty=[]
    for node in g.nodes:
        if g.nodes[node]['Jobs']['number'] < cap:
            avalbilty.append(True)
        else:
            avalbilty.append(False)
    return avalbilty
def wieghtFunction(func,i):
    if func == 'linear':
        return 1+i
    if func == 'power':
        return 1.5**i
    if func == 'uniform':
        return 1

def AddWieghtToEges(g,root,func):
    l=list (nx.all_pairs_dijkstra_path_length(g))
    rootIndex=list(g.nodes).index(root)
    depth=max(l[rootIndex][1].values())
    r={}
    for i in range(0,depth+1):
        r[i]=[]
    for node in g.nodes():
        r[l[rootIndex][1][node]].append(node)
    
    # for node in r[3]:    
    #     nodeRun(g,node,0,2)
    #     print(node)
    # for node in r[2]:    
    #     nodeRun(g,node,0,2)
    #     print(node)
        
    for i in range(0,depth+1):
        # print('i: '+str(i))
        for node in r[depth-i]: 
            # if g.nodes[node]['type'] == 's':
            #     # print(node)
            if node == root:
                return
            perent=list(g.in_edges(nbunch=node))[0][0]
            att={(perent,node):{'Wieght': wieghtFunction(func, i)}}
            nx.set_edge_attributes(g,att)
            
def JobColor(g,root,k,loadfile):
    # leafL=leafList(g)
    nodeList,load =readLoad(loadfile)
    addLoad(g,load,nodeList)
    AddWieghtToEges(g,root,'uniform')
    Add_InNetwork_Capacity(g)
    avalabilty=AvalbiltyCalc(g,1)
    soar.gather(g,root,k,avalabilty)
    coloring=soar.color(g,root,root,0,k)
    return [g,coloring]

def addLoad(g,load,nodesList):
    for n in g.nodes:
        if int(n) in nodesList:
            att={ n : {'load':int(load[nodesList.index(int(n))])}}
        else:
            att={ n : {'load':0}}
        nx.set_node_attributes(g,att)
        
def main():
    parser = argparse.ArgumentParser(description='SOAR Running example')
    parser.add_argument('-t', help='Tree adjaceny list txt file', required=True)
    parser.add_argument('-l', help='Load list', required=True)
    parser.add_argument('-k', help='Number of blue nodes to place', type=int ,required=True)
    args = parser.parse_args()
    treeFile=args.t#'Test_Tree.txt'
    loadFile=args.l#'load.txt'
    k=args.k
    g = nx.read_adjlist(treeFile, create_using=nx.DiGraph)

    r=[n for n,d in g.in_degree() if d==0]
    g,color=JobColor(g,r[0],k,loadFile)
    NXdraw(g,'0',1)
  

def readLoad(file):
     f = open(file, "r")
     lines= f.readlines()
     node = []
     load = []
     for line in lines:
         line=line.replace('\n','')
         n,l=line.split(' ')
         node.append(int(n))
         load.append(int(l))
     return node,load
 
def colorMap(gr,cap):
        color_map = []
        for node in gr.nodes:
            if gr.nodes[node]['color']=='blue':
                color_map.append((0, 0, 1-(0.25/cap)*gr.nodes[node]['Jobs']['number']))
            else:
                color_map.append(gr.nodes[node]['color'])
        return color_map
    
def NXdraw(g,root,cap):
    # Walg.messageCount(g,root)
    # SumMessage,BottleNeck=NetworkUtiliztion(g)
    # plt.title('number of Utilization: '+str(SumMessage)+' ,bottle neck: '+str(BottleNeck))
    labels = nx.get_node_attributes(g, 'load') 
    # nx.draw(g,pos=graphviz_layout(g, prog="dot"),with_labels=True)
    # nx.draw(g,pos=graphviz_layout(g, prog="dot"),labels=labels)
    nx.draw(g,pos=graphviz_layout(g, prog='dot'),node_color=colorMap(g,cap),labels=labels)
    edge_labels={}
    # for e in g.edges:
    #     edge_labels[e]={'e':e,'w':g.edges[e]['Wieght'],'m':g.edges[e]['mesageCount']}
    # edge_labels = nx.get_edge_attributes(g,'Wieght')
    pos=graphviz_layout(g,prog='dot')
    nx.draw_networkx_edge_labels(g, pos, edge_labels = edge_labels,rotate=False)

if __name__== "__main__":
    main()
