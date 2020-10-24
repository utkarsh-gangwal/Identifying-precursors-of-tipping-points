import numpy as np
import pandas as pd
import itertools
import random
import operator
import math

avg_values = []
for j in range(len(values[0])):
    scf = 0.0
    for i in range(len(values)):
        scf += values[i][j][1]
    avg_values.append([j, scf/len(values)])
#print(avg_values)

#################### Deviation in slope #######################
avg_values_log = np.log(np.array(avg_values)[1:-1])     # 1st and last values not considered as there is a 0
#print(avg_values_log)

slope = []
for i in range(1, len(avg_values_log)):
    temp = (avg_values_log[i][1]-avg_values_log[i-1][1])/(avg_values_log[i][0]-avg_values_log[i-1][0])
    slope.append([i, abs(temp)])
#print(slope)

deviation = []
for i in range(1, len(slope)):
    temp = slope[i][1] - slope[i-1][1]
    deviation.append([i+1, temp])
#print(deviation)

############ Deviation in Largest Cluster ######################
deviation_size = []
for i in range(1, len(avg_values)):
    temp = avg_values[i][1]-avg_values[i-1][1]
    deviation_size.append([i, abs(temp)])
#print(deviation_size)
