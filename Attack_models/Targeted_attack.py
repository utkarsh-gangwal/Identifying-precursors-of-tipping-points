# Import libraries
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

# Targeted attack model in which the degree is calculated only once
def degreerobustness(contingencysize, graph):   
    original_graph = graph.copy()
    largestcluster = max(nx.connected_component_subgraphs(original_graph), key=len)
    deg = list(original_graph.degree())
    sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)
      
    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, original_graph.number_of_nodes(), contingencysize):
        ivalues = sorted_deg[i-contingencysize:i]
        disruptednodes = [i[0] for i in ivalues]
        graph.remove_nodes_from(disruptednodes)
        
        Numberconnectedcomponents = max(nx.connected_component_subgraphs(graph), key=len)
        sizeratio_deg.append([i/contingencysize, len(Numberconnectedcomponents)/len(largestcluster)])
    sizeratio_deg.append([math.ceil(original_graph.number_of_nodes()/contingencysize), 0.0])
    return sizeratio_deg

# Targeted attack model in which the degree is calculated at every step
def degreerobustness_updated(contingencysize, graph): 
    original_graph = graph.copy()
    largestcluster = max(nx.connected_component_subgraphs(original_graph), key=len)
    
    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, original_graph.number_of_nodes(), contingencysize):
        deg = list(graph.degree())
        sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)
        ivalues = sorted_deg[0:contingencysize]
        disruptednodes = [i[0] for i in ivalues]
        graph.remove_nodes_from(disruptednodes)
        
        Numberconnectedcomponents = max(nx.connected_component_subgraphs(graph), key=len)
        sizeratio_deg.append([i/contingencysize, len(Numberconnectedcomponents)/len(largestcluster)])
    sizeratio_deg.append([math.ceil(original_graph.number_of_nodes()/contingencysize), 0.0])
    return sizeratio_deg

# Targeted attack model in which probability of attack is directly proportional to the degree
def probabilisticmodel(contingencysize, graph): 
    original_graph = graph.copy()
    largestcluster = max(nx.connected_component_subgraphs(original_graph), key=len)
    
    sizeratio_deg = []
    sizeratio_deg.append([0.0, 1.0])
    for i in range(contingencysize, original_graph.number_of_nodes(), contingencysize):
        deg = list(graph.degree())
        node_list = [j[0] for j in deg]
        weight = [j[1] for j in deg]
        
        if len(node_list) - weight.count(0) >= contingencysize:
            p = [k/sum(weight) for k in weight]
            disruptednodes = list(np.random.choice(node_list, contingencysize, replace=False, p = p))
        else:
            sorted_deg = sorted(deg, key=lambda c: (c[1],c[0]), reverse = True)
            ivalues = sorted_deg[0:contingencysize]
            disruptednodes = [i[0] for i in ivalues]

        graph.remove_nodes_from(disruptednodes)       
        Numberconnectedcomponents = max(nx.connected_component_subgraphs(graph), key=len)
        sizeratio_deg.append([i/contingencysize, len(Numberconnectedcomponents)/len(largestcluster)])
    sizeratio_deg.append([math.ceil(original_graph.number_of_nodes()/contingencysize), 0.0])
    return sizeratio_deg
