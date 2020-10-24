import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
import random
import operator
import math
import pickle
import os
from tqdm import tqdm
import sys


def robustness(contingencysize, graph):
    original_graph = graph.copy()
    largestcluster = max(nx.connected_component_subgraphs(original_graph), key=len)
    
    nodes = []
    for q in range(0,original_graph.number_of_nodes()):
        nodes.append(q)
        
    sizeratio = []
    sizeratio.append([0.0,1.0])
    for m in range(contingencysize,original_graph.number_of_nodes(),contingencysize): 
        iterable = []
        for j in range(0,100):
            iterable.append(list(np.random.choice(nodes, contingencysize, replace=False)))      # contingencysize is r in nCr 
        
        emptylist = []
        for i in iterable:
            G = graph.copy()
            G.remove_nodes_from(i)
            Numberconnectedcomponents = max(nx.connected_component_subgraphs(G), key=len)
            emptylist.append([i,len(Numberconnectedcomponents)/len(largestcluster)])
        
        G = graph.copy()
        d = min(list(j for i,j in emptylist))     # d is the minimum value of SCF
        sizeratio.append([m/contingencysize, d])             
        b = [x for x,y in emptylist if y==d][0]   # b is the corressponding of d
        graph.remove_nodes_from(b)                # remove the nodes that cause maximum damage and update the graph
        for k in b:
            nodes.remove(k)                
    sizeratio.append([math.ceil(original_graph.number_of_nodes()/contingencysize),0.0])
    return sizeratio
