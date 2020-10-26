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

##################################################################

# Targeted attack model in which degree of nodes is computed once
def degreerobustness_snap(contingencysize):
    global n
    print(n)
    e = int(0.008*(n*(n-1)/2))
    graph = snap.GenRndGnm(snap.PUNGraph, n, e)   # nodes, edges
    largestcluster = n*snap.GetMxSccSz(graph)
    deg = {}
    for NI in graph.Nodes():
        DegCentr = snap.GetDegreeCentr(graph, NI.GetId())
        deg[NI.GetId()] = DegCentr
    deg = [(k, v) for k, v in deg.items()]
    sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)

    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, n, contingencysize):
        ivalues = sorted_deg[i-contingencysize:i]
        V = snap.TIntV()
        for j in ivalues:
            V.Add(j[0])
        snap.DelNodes(graph, V)
        Numberconnectedcomponents = (n-i)*snap.GetMxSccSz(graph)
        sizeratio_deg.append([i/contingencysize, Numberconnectedcomponents/largestcluster])
    sizeratio_deg.append([math.ceil(n/contingencysize),0.0])
    return sizeratio_deg

net_size = [5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000]
folder = "/home/utkarsh/Documents"
g_type = "targeted_model1"

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

        targetedvalues = p.map(degreerobustness_snap, sizes)
        p.close()
        save_as_pickled_object(targetedvalues, pickle_name)
    t_final = datetime.now()
    time['used'] =t_final-t_present
    time_list.append(time)
    
print(time_list)

##################################################################

# Targeted attack model in which degree of nodes is at every step
def degreerobustness_updated_snap(contingencysize):
    global n
    print(n)
    e = int(0.008*(n*(n-1)/2))
    graph = snap.GenRndGnm(snap.PUNGraph, n, e)   # nodes, edges
    largestcluster = n*snap.GetMxSccSz(graph)
    
    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, n, contingencysize):
        deg = {}
        for NI in graph.Nodes():
            DegCentr = snap.GetDegreeCentr(graph, NI.GetId())
            deg[NI.GetId()] = DegCentr
        deg = [(k, v) for k, v in deg.items()]
        sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)

        ivalues = sorted_deg[0:contingencysize]
        V = snap.TIntV()
        for j in ivalues:
            V.Add(j[0])
        snap.DelNodes(graph, V)
        Numberconnectedcomponents =(n-i)*snap.GetMxSccSz(graph)
        sizeratio_deg.append([i/contingencysize, Numberconnectedcomponents/largestcluster])
    sizeratio_deg.append([math.ceil(n/contingencysize),0.0])
    return sizeratio_deg
    
net_size = [5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000]
folder = "/home/utkarsh/Documents"
g_type = "targeted_model2"

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

        #randomvalues = Parallel(n_jobs = 24, verbose = 50)(delayed(robustness_snap)(i) for i in tqdm(sizes))
        targetedvalues_updated = p.map(degreerobustness_updated_snap, sizes)
        p.close()
        save_as_pickled_object(targetedvalues_updated, pickle_name)
    t_final = datetime.now()
    time['used'] =t_final-t_present
    time_list.append(time)
    
print(time_list)

##################################################################

# Targeted attack model in which the probability of failure is proportional to the degree
def probabilistic_snap(contingencysize):
    global n
    print(n)
    e = int(0.008*(n*(n-1)/2))
    graph = snap.GenRndGnm(snap.PUNGraph, n, e)   # nodes, edges
    largestcluster = n*snap.GetMxSccSz(graph)
    
    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, n, contingencysize):
        deg = {}
        for NI in graph.Nodes():
            DegCentr = snap.GetDegreeCentr(graph, NI.GetId())
            deg[NI.GetId()] = DegCentr
        deg = [(k, v*(n-1-(i-contingencysize))) for k, v in deg.items()]
        node_list = [j[0] for j in deg]
        weight = [j[1] for j in deg]

        if len(node_list) - weight.count(0) >= contingencysize:
            p = [k/sum(weight) for k in weight]
            choice = np.random.choice(node_list, contingencysize, replace=False, p = p)
            V = snap.TIntV()
            for j in choice:
                V.Add(j)
        else:
            sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)
            ivalues = sorted_deg[0:contingencysize]
            V = snap.TIntV()
            for j in ivalues:
                V.Add(j[0])
        snap.DelNodes(graph, V)
        Numberconnectedcomponents = (n-i)*snap.GetMxSccSz(graph)
        sizeratio_deg.append([i/contingencysize, Numberconnectedcomponents/largestcluster])
    sizeratio_deg.append([math.ceil(n/contingencysize),0.0])
    return sizeratio_deg
    
net_size = [5000, 6000, 7000, 8000, 9000, 10000, 15000, 20000, 25000]
folder = "/home/utkarsh/Documents"
g_type = "probalistic"

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

        #randomvalues = Parallel(n_jobs = 24, verbose = 50)(delayed(robustness_snap)(i) for i in tqdm(sizes))
        probabilistic = p.map(probabilistic_snap, sizes)
        p.close()
        save_as_pickled_object(probabilistic, pickle_name)
    t_final = datetime.now()
    time['used'] =t_final-t_present
    time_list.append(time)
    
print(time_list)
