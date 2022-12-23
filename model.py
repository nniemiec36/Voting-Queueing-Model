import queueing_tool as qt
import numpy as np
import sys
import csv
import random

SMALL = "SMALL"
AVERAGE = "AVERAGE"
LARGE = "LARGE"

# default
precinct_size = AVERAGE

# setting lambda for different precinct sizes
def set_lambda():
    if precinct_size == SMALL:
        return 0.09615384615
    elif precinct_size == AVERAGE:
        return 1.923076923
    else:
        return 5.769230769

# set turnout
def set_turnout():
    if precinct_size == SMALL:
        return 75
    elif precinct_size == AVERAGE:
        return 1500
    else:
        return 4500

def set_checkin_workers():
    if precinct_size == SMALL:
        return 1
    elif precinct_size == AVERAGE:
        return 5
    else:
        return 15

def set_DRES():
    if precinct_size == SMALL:
        return 1
    elif precinct_size == AVERAGE:
        return 12
    else:
        return 30

# need an adjacency list (or matrix)
# assume that this voting place has
adjacency_list = {0: [1], 1: [2]}
edge_list = {0: {1: 1}, 1: {2: 2}}
# specifies what kind of queue sits on each edge, type 1 and type 2

# create a graph
graph = qt.adjacency2graph(adjacency=adjacency_list, edge_type=edge_list)


def rate(t):
    return l


def arr_f(t):
    return qt.poisson_random_measure(t, rate, l)


def ser_checkin(t):
    return t + np.random.exponential(1.4085)


def ser_voting(t):
    return t + np.random.exponential(4.9905)

l = set_lambda()
turnout = set_turnout()
dre = set_DRES()
checkins = set_checkin_workers()

queue_classes = {1: qt.QueueServer, 2: qt.QueueServer}
queue_args = {
    1: {
        'arrival_f': arr_f,
        'service_f': ser_checkin,
        'num_servers': checkins,
        'AgentFactory': qt.GreedyAgent
    },
    2: {
        'num_servers': dre,
        'service_f': ser_voting
    }
}

runs = []
overalls = []
delay1s = []
delay2s = []
times = []

for i in range(0, 1000):

    queue_network = qt.QueueNetwork(g=graph, max_agents=turnout, q_classes=queue_classes, q_args=queue_args, seed=random.randint(10, 2000))

    # specifies which queue type allows arrivals from outside the system

    queue_network.start_collecting_data()
    queue_network.initialize(edge_type=1)
    queue_network.simulate(t=780)

    data_out = queue_network.get_agent_data()

    runs.append(data_out)

    time_in_system=[]
    delay_1=[]
    delay_2=[]
    overall_delay=[]
    
    for k in data_out.keys():
        #print(k)
        #print(data_out[k])
        #print(len(data_out[k]))
        try:
            if data_out[k][2,0]>=data_out[k][0,0]:
                time_in_system.append(data_out[k][2,0]-data_out[k][0,0])
        except:
            pass
        
        try:
            if data_out[k][0,1]>=data_out[k][0,0]:
                delay_1.append(data_out[k][0,1]-data_out[k][0,0])
        except:
            pass
        
        try:
            if data_out[k][1,1]>=data_out[k][1,0]:
                delay_2.append(data_out[k][1,1]-data_out[k][1,0])
        except:
            pass
        
        try:
            if data_out[k][1,1]>=data_out[k][1,0] and data_out[k][0,1]>=data_out[k][0,0]:
                overall_delay.append((data_out[k][1,1]-data_out[k][1,0])+(data_out[k][0,1]-data_out[k][0,0]))
        except:
            pass
    times.append(time_in_system)
    delay1s.append(delay_1)
    delay2s.append(delay_2)
    overalls.append(overall_delay)   

header = ['Run', 'Key', 'Arrival Time', 'Enter Service Time', 'Departure Time', 'Length of Queue', 'Number of Agents', 'Edge Index of Queue']

filename = 'ave_12_precincts_results.csv'
with open(filename, 'w') as file:
    for header in header:
        file.write(str(header)+', ')
    file.write('\n')
    for n in range(0, len(runs)):
        for k in runs[n].keys():
            for i in runs[n][k]:
                file.write(str(n)+', ')
                file.write(str(k)+', ')
                for j in i:
                    file.write(str(j)+', ')
                file.write('\n')

filename = 'ave_12_precincts_delay1.csv'
with open(filename, 'w') as file:
    for n in range(0, len(delay1s)):
        file.write(str(n)+', ')
        for j in delay1s[n]:
            file.write(str(j)+', ')
        file.write('\n')

filename = 'ave_12_precincts_overall.csv'
with open(filename, 'w') as file:
    for n in range(0, len(overalls)):
        file.write(str(n)+', ')
        for j in overalls[n]:
            file.write(str(j)+', ')
        file.write('\n')

filename = 'ave_12_precincts_delay2.csv'
with open(filename, 'w') as file:
    for n in range(0, len(delay2s)):
        file.write(str(n)+', ')
        for j in delay2s[n]:
            file.write(str(j)+', ')
        file.write('\n')

filename = 'ave_12_precincts_times.csv'
with open(filename, 'w') as file:
    for n in range(0, len(times)):
        file.write(str(n)+', ')
        for j in times[n]:
            file.write(str(j)+', ')
        file.write('\n')