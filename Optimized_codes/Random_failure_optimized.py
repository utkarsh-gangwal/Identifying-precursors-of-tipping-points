# Import all the necessary libraries
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
import joblib
from joblib import Parallel, delayed
from joblib import parallel_backend
import multiprocessing
from multiprocessing import Pool
import multiprocessing
import snap
from datetime import datetime

# Random failures
# Contingency size if the number of nodes to be removed in one step

def robustness_snap(contingencysize):
    global n
    print(n)
    e = int(0.008*(n*(n-1)/2))
    graph = snap.GenRndGnm(snap.PUNGraph, n, e)   # nodes, edges
    largestcluster = n*snap.GetMxSccSz(graph)
    nodes = list(np.arange(n))

    sizeratio = []
    sizeratio.append([0.0,1.0])
    for m in range(contingencysize,n,contingencysize):
        iterable = []
        for j in range(100):
            choice = np.random.choice(nodes, contingencysize, replace=False)
            V = snap.TIntV()
            for i in choice:
                V.Add(i)
            iterable.append(V)

        emptylist = []
        for i in iterable:
            G = snap.ConvertGraph(snap.PUNGraph, graph)
            snap.DelNodes(G, i)
            Numberconnectedcomponents = (n-m)*snap.GetMxSccSz(G)
            emptylist.append([i,Numberconnectedcomponents/largestcluster])

        d = min(list(j for i,j in emptylist))     # d is the minimum value of SCF
        sizeratio.append([m/contingencysize, d])
        b = [x for x,y in emptylist if y==d][0]   # b is the corressponding of d
        snap.DelNodes(graph, b)
        for k in b:
            nodes.remove(k)
    sizeratio.append([math.ceil(n/contingencysize),0.0])
    return sizeratio

net_size = [5000, 6000, 7000, 8000, 9000, 20000, 25000]
folder = "/home/utkarsh/Documents"
g_type = "random"

time_list = []
for size in net_size:
    time = {}
    time['size'] = size
    
    t_present = datetime.now()
    pickle_name = str(size) + g_type +".pkl"
    n = size
    sizes = list(range(14,98,4))
    if __name__ == "__main__":
        p = Pool(48)

        randomvalues = p.map(robustness_snap, sizes)
        p.close()
        save_as_pickled_object(randomvalues, pickle_name)
    t_final = datetime.now()
    time['used'] =t_final-t_present
    time_list.append(time)
print(time_list)
