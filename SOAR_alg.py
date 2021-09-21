

# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 23:54:59 2021

@author: Segal Raz
"""
import networkx as nx
import math
import numpy as np
import time

def phi(g,node,l,i):
    if i<0:
        return math.inf
    if i==0:
        return g.nodes[node]['l'+str(l)]['k'+str(i)]['red']['val']
    return min(g.nodes[node]['l'+str(l)]['k'+str(i)]['red']['val'],g.nodes[node]['l'+str(l)]['k'+str(i)]['blue']['val'])

def bestPartition(g,node, neighbour, l, i,col):
    tmp=[]
    
    for j in range(0,i+1):
        #print('phi'+str(j)+':'+str(phi(g,neighbour, 1 if col=='blue' else (l+1),j)))
        #print('nphi '+str(i-j)+' :' +str(g.nodes[node]['l'+str(l)]['k'+str(i-j)][col]['val']))
        tmp.append(g.nodes[node]['l'+str(l)]['k'+str()][col]['val']+phi(g,neighbour, 1 if col=='blue' else (l+1),i-j))
    #print("bestPartition: "+str(tmp))
    return [min(tmp),np.argmin(tmp)]

def nodeLoad(g,node):
    neighborsList= list(g.neighbors(node))
    load=0
    workers=[]
    for n in neighborsList:
        if g.nodes[n]['type']=='w':
            load=load+1
            workers.append(n)
    return [load,workers]

def mCost(graph,l,i,Y,X,color):
    tmp=[]
    # if color == 'blue':
    #     i=i-1
    for j in range(0,i+1):
        tmp.append(Y['l'+str(l)]['k'+str(i-j)][color]+X['l'+str(1 if color=='blue' else (l+1))]['k'+str(j)])
    #print("bestPartition: "+str(tmp))
    return min(tmp)

def mSplit(graph,l,i,Y,X,color):
    tmp=[]
    # if color == 'blue':
    #     i=i-1
    for j in range(0,i+1):
        #print('phi'+str(j)+':'+str(phi(g,neighbour, 1 if col=='blue' else (l+1),j)))
        #print('nphi '+str(i-j)+' :' +str(g.nodes[node]['l'+str(l)]['k'+str(i-j)][col]['val']))
        tmp.append(Y['l'+str(l)]['k'+str(i-j)][color]+X['l'+str(1 if color=='blue' else (l+1))]['k'+str(j)])
    # print("bestPartition: "+str(tmp))
    return np.argmin(tmp)
    
    
def nodeRun(graph,node,root,k,Avilabilty):
        load=graph.nodes[node]['load']
        n=[x for x in list(graph.neighbors(node))]
        # print('nodeRun node:'+str(node))
        try:
            p=list(nx.all_simple_paths(graph, source=root, target=node))[0]
        except:
            p=[1]
        
        p.reverse()
        depth=len(p)-1
        att={ node : {'m'+str(c):{'l'+str(d): {'k'+str(j):{'red':0,'blue':0} for j in range(0,k+1)}  for d in range(0,depth+1) }for c in range(0,len(n))}}
        att[node]['minSend']={'l'+str(d): {'k'+str(j):0 for j in range(0,k+1)}  for d in range(0,depth+1) }
        att[node]['node']=node
        att[node]['children']=[]
        att[node]['color']='red'
        nx.set_node_attributes(graph,att)
        
        
        if not n:
            # print("leaf: "+str(node)+" load:"+str(load))
            for d in range(0,depth+1):
                rate=0
                for i in range(1,d+1):
                    # print(i)
                    rate=rate+1/(graph.edges[(p[i],p[i-1])]['Wieght'])
                graph.nodes[node]['minSend']['l'+str(d)]['k'+str(0)]=rate*load
                for i in range(1,k+1):
                    if Avilabilty[int(node)]:
                        graph.nodes[node]['minSend']['l'+str(d)]['k'+str(i)]=rate
                    else:
                        graph.nodes[node]['minSend']['l'+str(d)]['k'+str(i)]=rate*load
                    
        else: 
            first=True  
            for neighbour in n:
                graph.nodes[node]['children'].append(neighbour)
                # print("(n.index(neighbour) "+str(n.index(neighbour)))
                if first:
                    for d in range(0,depth+1):  
                        rate=0
                        for i in range(1,d+1):
                            rate=rate+1/(graph.edges[(p[i],p[i-1])]['Wieght'])
                            
                        graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['red']=graph.nodes[neighbour]['minSend']['l'+str(d+1)]['k'+str(0)]+rate*load
                        graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['blue']=math.inf
                        for i in range(1,k+1):
                            # graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['red']['partition'][neighbour]=i
                            # graph.nodes[node]['l'+str(d)]['k'+str(i)]['blue']['partition'][neighbour]=i-1
                            graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['red']=graph.nodes[neighbour]['minSend']['l'+str(d+1)]['k'+str(i)]+rate*load
                            if Avilabilty[int(node)]:
                                graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['blue']=graph.nodes[neighbour]['minSend']['l'+str(1)]['k'+str(i-1)]+rate
                            else:
                                graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['blue']=math.inf
                    first=False
                else:
                    # tmpNode=copy.deepcopy(graph.nodes[node])
                    for d in range(0,depth+1):
                            
                        PreviosYm=graph.nodes[node]['m'+str(n.index(neighbour)-1)] #easyFix
                        Xm=graph.nodes[neighbour]['minSend']
                        graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['red']=mCost(graph,d,0,PreviosYm,Xm,'red')
                        graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['blue']=math.inf
                        # graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(1)]['red']=mCost(graph,d,1,PreviosYm,Xm,'red')
                        # graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(1)]['blue']=graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(0)]['red']
                        for i in range(1,k+1):
                            PreviosYm=graph.nodes[node]['m'+str(n.index(neighbour)-1)]
                            Xm=graph.nodes[neighbour]['minSend']
                            graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['red']=mCost(graph,d,i,PreviosYm,Xm,'red')
                            if Avilabilty[int(node)]:
                                graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['blue']=mCost(graph,d,i,PreviosYm,Xm,'blue') #hardFix
                            else:
                                graph.nodes[node]['m'+str(n.index(neighbour))]['l'+str(d)]['k'+str(i)]['blue']=math.inf
                            # tmp=bestPartition(graph,node, neighbour, d, i,'red')
                            # # print('node:'+str(node)+' d: '+str(d)+' i: '+str(i)+' tmpred:'+str(tmp))
                            
                            # tmpNode['l'+str(d)]['k'+str(i)]['red']['val']=tmp[0]
                            # tmpNode['l'+str(d)]['k'+str(i)]['red']['partition'][neighbour]=tmp[1]
                            # tmp=bestPartition(graph,node, neighbour, d, i,'blue')
                            # # print('node:'+str(node)+' d: '+str(d)+' i: '+str(i)+' tmpblue:'+str(tmp))
                            # tmpNode['l'+str(d)]['k'+str(i)]['blue']['val']=tmp[0]
                            # tmpNode['l'+str(d)]['k'+str(i)]['blue']['partition'][neighbour]=tmp[1]
                            
                            
                    # att={node: tmpNode}
                    # nx.set_node_attributes(graph,att)
            for d in range(0,depth+1):
                graph.nodes[node]['minSend']['l'+str(d)]['k'+str(0)]=graph.nodes[node]['m'+str(len(n)-1)]['l'+str(d)]['k'+str(0)]['red']
                for i in range(1,k+1):
                    graph.nodes[node]['minSend']['l'+str(d)]['k'+str(i)]=min(graph.nodes[node]['m'+str(len(n)-1)]['l'+str(d)]['k'+str(i)]['red'],graph.nodes[node]['m'+str(len(n)-1)]['l'+str(d)]['k'+str(i)]['blue'])



def gather(g,root,k,Avilabilty):
    # start_time = time.time()
    # g=nx.balanced_tree(deg,h,create_using=nx.DiGraph)
    
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
                # print(node)
                nodeRun(g,node,root,k,Avilabilty)
    
    # print("Running time: "+str(time.time()-start_time))
    return g



def color(g,node,root,d,k):
    if node==root:
        for n in g.nodes:
                g.nodes[n]['color']='red'

    children=g.nodes[node]['children']
    # d=nx.shortest_path_length(g,root,node)
    if children == [] and k>0:
        g.nodes[node]['color']='blue'
        return
    if k>0:
         # print('this node:',node)
         if g.nodes[node]['m'+str(len(children)-1)]['l'+str(d)]['k'+str(k)]['blue']<g.nodes[node]['m'+str(len(children)-1)]['l'+str(d)]['k'+str(k)]['red']:
             g.nodes[node]['color']='blue'
             d=0
             # k=k-1
         for c in children[::-1]:
             if c==children[0]:
                if g.nodes[node]['color']=='blue':
                    # print('this node:',node,'l:',d,'k:',k,'color:',g.nodes[node]['color'],'child:',c,'j:',k-1)
                    color(g,c,root,d+1,k-1)       
                else:
                    # print('this node:',node,'l:',d,'k:',k,'color:',g.nodes[node]['color'],'child:',c,'j:',k)
                    color(g,c,root,d+1,k) 
             else:
                 PreviosYm=g.nodes[node]['m'+str(children.index(c)-1)]
                 Xm=g.nodes[c]['minSend']
                 if g.nodes[node]['color'] == 'blue':
                     j=mSplit(g,d+1,k,PreviosYm,Xm, g.nodes[node]['color'])
                     color(g,c,root,d+1,j)
                     k=k-j
                 
                 else:
                     j=mSplit(g,d,k,PreviosYm,Xm, g.nodes[node]['color'])
                     color(g,c,root,d+1,j)
                     k=k-j
                 # print('this node:',node,'l:',d,'k:',k,'color:',g.nodes[node]['color'],'child:',c,'j:',j)
                 # print('PreviosYm',PreviosYm,'xm',Xm)
                
                 
    if(node==root):
        #gr.nodes[node]['color']='green'
        b=[]
        for n in g.nodes():
            if g.nodes[n]['color']=='blue':
                b.append(n)
        print("Blue nodes: "+str(b))
        return b
    
    
def messageCount(g,root):
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
            rate=1/g.edges[(perent,node)]['Wieght']
            if g.nodes[node]['color']=='blue':
                att={(perent,node):{'mesageCount':1}}
            else:
                children=list(g.out_edges(nbunch=node))
                if children:
                    s=0
                    for c in children:
                       s=s+ g.edges[c]['mesageCount']
                    att={(perent,node):{'mesageCount':s}}
                else:
                    att={(perent,node):{'mesageCount':g.nodes[node]['load']}}
            nx.set_edge_attributes(g,att)

