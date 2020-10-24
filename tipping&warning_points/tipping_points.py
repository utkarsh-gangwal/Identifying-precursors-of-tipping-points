import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import itertools
import random
import operator
import math
import pickle
%matplotlib inline
get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = [20, 20]

avg_values = []
for j in range(len(values[0])):
    scf = 0.0
    for i in range(len(values)):
        scf += values[i][j][1]
    avg_values.append([j, scf/len(values)])

#################### Deviation in slope #######################
avg_values_log = np.log(np.array(avg_values)[1:-1])     # 1st and last values not considered as there is a 0

slope = []
for i in range(1, len(avg_values_log)):
    temp = (avg_values_log[i][1]-avg_values_log[i-1][1])/(avg_values_log[i][0]-avg_values_log[i-1][0])
    slope.append([i, abs(temp)])

deviation = []
for i in range(1, len(slope)):
    temp = slope[i][1] - slope[i-1][1]
    deviation.append([i+1, temp])

############ Deviation in Largest Cluster ######################
deviation_size = []
for i in range(1, len(avg_values)):
    temp = avg_values[i][1]-avg_values[i-1][1]
    deviation_size.append([i, abs(temp)])

################################################################

scf_values = [avg_values]
l_val = log_c(scf_values)
target = l_val

x = 0
x1 = target[x][0][0]
y1 = target[x][0][1]
x2 = target[x][len(target[x])-1][0]
y2 = target[x][len(target[x])-1][1]

get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams['figure.figsize'] = [15, 15]
plt.close('all')
fig = plt.figure()
ax1 = plt.subplot2grid((4,4), (0,1), colspan=2, rowspan=2)  # topleft
ax2 = plt.subplot2grid((4,4), (2,0), colspan=2, rowspan=2)  # bottom left
ax3 = plt.subplot2grid((4,4), (2,2), colspan=2, rowspan=2)  # bottom right
plt.tight_layout(pad = 6)
fig.suptitle('Tipping Point', fontsize = 34)

ax1.loglog(np.array(scf_values[x])[:,0],np.array(scf_values[x])[:,1],color = 'b')
ax1.scatter(np.array(scf_values[x])[:,0],np.array(scf_values[x])[:,1],s = 100,marker='x')
m = (target[x][0][1]-target[x][len(target[x])-1][1])/(target[x][0][0]-target[x][len(target[x])-1][0])
max = 0
for j in range(1,len(l_val[x])):
    c = l_val[x][j][1]-m*(l_val[x][j][0])
    if(c>max):
        max = c
        z = l_val[x][j]
warning_point = round(10**z[0])

l = []
for i in deviation_size:
    if i[0] >= warning_point:
        l.append(i[1])
a = np.max(l)
t = [x for x,y in deviation_size if y==a]
for i in t:
    t = i

ax1.scatter(int(round(10**z[0])),10**z[1],s = 100,color = 'orange')
ax1.scatter(t, avg_values[t][1], s = 100, color = 'r')

ax1.axvspan(0.9, int(round(10**z[0])), alpha=0.2, color='green')
ax1.axvspan(int(round(10**z[0])), t, alpha=0.2, color='orange')
ax1.axvspan(t, 350,alpha=0.2, color='red')
ax1.set_xlim(left = 0.9)
ax1.set_xlim(right = 350)

ax1.set_xlabel('Time', fontsize = '20')
ax1.set_ylabel('Functionality', fontsize = '20')
ax1.tick_params(axis='both', labelsize = 'xx-large', direction='out', length=6, width=2)
ax1.spines['top'].set_linewidth(1.5)
ax1.spines['right'].set_linewidth(1.5)
ax1.spines['bottom'].set_linewidth(1.5)
ax1.spines['left'].set_linewidth(1.5)
ax1.grid(True,which="both",ls="-")



ax2.plot(np.array(deviation)[:,0],np.array(deviation)[:,1], color = 'b')
ax2.scatter(deviation[int(round(10**z[0]))-2][0], deviation[int(round(10**z[0]))-2][1], s = 80, color = 'orange')
ax2.scatter(t, deviation[t-2][1], s = 80, color = 'r')

ax2.set_xlabel('Time', fontsize = '20')
ax2.set_ylabel('Deviation in Slope', fontsize = '20')
ax2.tick_params(axis='both', labelsize = 'xx-large', direction='out', length=6, width=2)
ax2.spines['top'].set_linewidth(1.5)
ax2.spines['right'].set_linewidth(1.5)
ax2.spines['bottom'].set_linewidth(1.5)
ax2.spines['left'].set_linewidth(1.5)
ax2.grid(True,which="both",ls="-")



ax3.plot(np.array(deviation_size)[:,0],np.array(deviation_size)[:,1], color = 'b')
#ax3.scatter(np.array(deviation_size)[:,0],np.array(deviation_size)[:,1], s = 20, marker='o', color = 'b', alpha = 0.3)
ax3.scatter(int(round(10**z[0]))-1, deviation_size[int(round(10**z[0]))-1][1], s = 80, color = 'orange')
#ax3.annotate((int(round(10**z[0])), round(deviation_size[int(round(10**z[0]))-1][1], 5)), (int(round(10**z[0]))-1, deviation_size[int(round(10**z[0]))-1][1]), fontsize = 14, ha='center')
ax3.scatter(t, deviation_size[t-1][1], s = 80, color = 'r')
#ax3.annotate((t, round(deviation_size[t-1][1], 5)), (t, deviation_size[t-1][1]), fontsize = 14, ha='center')

ax3.set_xlabel('Time', fontsize = '20')
ax3.set_ylabel('Deviation in largest component', fontsize = '20')
ax3.tick_params(axis='both', labelsize = 'xx-large', direction='out', length=6, width=2)
ax3.spines['top'].set_linewidth(1.5)
ax3.spines['right'].set_linewidth(1.5)
ax3.spines['bottom'].set_linewidth(1.5)
ax3.spines['left'].set_linewidth(1.5)
ax3.grid(True,which="both",ls="-")
plt.show()
