# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 09:39:18 2025

@author: farha
"""

import numpy as np
import pandas as pd
import gurobipy as gp
from gurobipy import GRB
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import pickle
import csv
import os
start_time = time.time()


## Network 1
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Sheet3')
#data1= pd.read_excel(r'200users_1_base.xlsx', sheet_name='NetA', engine='openpyxl')
#data2= pd.read_excel(r'200users_1_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
#AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
#AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
#Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)


num_nodes=262

source=263
sink=264
node_expansion_start_node=265



# Create a Gurobi model
m = gp.Model("Network_Dual_LB")


capacities1 = {}
Objective_ValueLB=0
df6={}


# Decision variable: Binary variable indicating if an edge is selected
theta = m.addVars(A.edges, vtype=GRB.CONTINUOUS, name="theta")
pi = m.addVars(A.nodes,  vtype=GRB.CONTINUOUS, name="pi")
mu = m.addVars(A.edges,  vtype=GRB.CONTINUOUS, name="mu")
    
z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    

#Objective function: Min-cut (Dual of max flow)
m.setObjective(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j] for i, j in A.edges), GRB.MINIMIZE)

# Constraints: Ensure connectivity
m.addConstrs(pi[i]-pi[j]+theta[i, j]>=0 for i, j in A.edges)
m.addConstr(pi[sink]-pi[source]>=1)
#m.addConstrs(z[i, j]==0 for i, j in A.edges)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
m.addConstrs(mu[i,j]+z[i,j] - theta[i,j] >= 0 for  i, j in A.edges)

m.addConstrs(z[i,j]==0 for i,j in A.edges)

# Optimize the model
start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
m.optimize()

Objective_Value_Base1= m.objVal

##Network 2
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\NodeExpansionData.xlsx', sheet_name='Sheet1')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet20')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='NodeEx')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet19')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet21')
#data1= pd.read_excel(r'200users_1_base.xlsx', sheet_name='NetA', engine='openpyxl')
#data2= pd.read_excel(r'200users_1_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
#AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
#AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
#Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)


num_nodes=260

source=1
sink=262
node_expansion_start_node=263



# Create a Gurobi model
m = gp.Model("Network_Dual_LB")


capacities1 = {}
Objective_ValueLB=0
df6={}


# Decision variable: Binary variable indicating if an edge is selected
theta = m.addVars(A.edges, vtype=GRB.CONTINUOUS, name="theta")
pi = m.addVars(A.nodes,  vtype=GRB.CONTINUOUS, name="pi")
mu = m.addVars(A.edges,  vtype=GRB.CONTINUOUS, name="mu")
    
z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    

#Objective function: Min-cut (Dual of max flow)
m.setObjective(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j] for i, j in A.edges), GRB.MINIMIZE)

# Constraints: Ensure connectivity
m.addConstrs(pi[i]-pi[j]+theta[i, j]>=0 for i, j in A.edges)
m.addConstr(pi[sink]-pi[source]>=1)
#m.addConstrs(z[i, j]==0 for i, j in A.edges)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
m.addConstrs(mu[i,j]+z[i,j] - theta[i,j] >= 0 for  i, j in A.edges)

m.addConstrs(z[i,j]==0 for i,j in A.edges)

# Optimize the model
start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
m.optimize()

Objective_Value_Base2= m.objVal

##Network 3
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Sheet3')
#data1= pd.read_excel(r'200users_3_base.xlsx', sheet_name='NetA', engine='openpyxl')
#data2= pd.read_excel(r'200users_3_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_3_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_3_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_3_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
#AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
#AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
#Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)
num_nodes=261
num_res_arcs=131
rand_num=num_nodes+num_res_arcs
Total_arcs_A=1178
Com_arcs=num_res_arcs+Total_arcs_A
source=262
sink=263
node_expansion_start_node=264
# Create a Gurobi model
m = gp.Model("Network_Dual_LB")
capacities1 = {}
Objective_ValueLB=0
df6={}
# Decision variable: Binary variable indicating if an edge is selected
theta = m.addVars(A.edges, vtype=GRB.CONTINUOUS, name="theta")
pi = m.addVars(A.nodes,  vtype=GRB.CONTINUOUS, name="pi")
mu = m.addVars(A.edges,  vtype=GRB.CONTINUOUS, name="mu")   
z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    

#Objective function: Min-cut (Dual of max flow)
m.setObjective(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j] for i, j in A.edges), GRB.MINIMIZE)

# Constraints: Ensure connectivity
m.addConstrs(pi[i]-pi[j]+theta[i, j]>=0 for i, j in A.edges)
m.addConstr(pi[sink]-pi[source]>=1)
#m.addConstrs(z[i, j]==0 for i, j in A.edges)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
m.addConstrs(mu[i,j]+z[i,j] - theta[i,j] >= 0 for  i, j in A.edges)
m.addConstrs(z[i,j]==0 for i,j in A.edges)
# Optimize the model
start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
m.optimize()

Objective_Value_Base3= m.objVal

## Network 4
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_4_base\200users_4_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_4_base\200users_4_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_4_base\200users_4_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_4_base\200users_4_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_4_base\200users_4_base.xlsx', sheet_name='Sheet3')
#data1= pd.read_excel(r'200users_4_base.xlsx', sheet_name='NetA',engine='openpyxl')
#data2= pd.read_excel(r'200users_4_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_4_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_4_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_4_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
#AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
#AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
#Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)


num_nodes=261
num_res_arcs=126
rand_num=num_nodes+num_res_arcs
Total_arcs_A=1147
Com_arcs=num_res_arcs+Total_arcs_A
source=262
sink=263
node_expansion_start_node=264
# Create a Gurobi model
m = gp.Model("Network_Dual_LB")
capacities1 = {}
Objective_ValueLB=0
df6={}
# Decision variable: Binary variable indicating if an edge is selected
theta = m.addVars(A.edges, vtype=GRB.CONTINUOUS, name="theta")
pi = m.addVars(A.nodes,  vtype=GRB.CONTINUOUS, name="pi")
mu = m.addVars(A.edges,  vtype=GRB.CONTINUOUS, name="mu")
z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
#Objective function: Min-cut (Dual of max flow)
m.setObjective(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j] for i, j in A.edges), GRB.MINIMIZE)

# Constraints: Ensure connectivity
m.addConstrs(pi[i]-pi[j]+theta[i, j]>=0 for i, j in A.edges)
m.addConstr(pi[sink]-pi[source]>=1)
#m.addConstrs(z[i, j]==0 for i, j in A.edges)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
m.addConstrs(mu[i,j]+z[i,j] - theta[i,j] >= 0 for  i, j in A.edges)
m.addConstrs(z[i,j]==0 for i,j in A.edges)
# Optimize the model
start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
m.optimize()

Objective_Value_Base4= m.objVal


##Network 5
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_5_base\200users_5_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_5_base\200users_5_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_5_base\200users_5_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_5_base\200users_5_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_5_base\200users_5_base.xlsx', sheet_name='Sheet13')
#data1= pd.read_excel(r'200users_5_base.xlsx', sheet_name='NetA', engine='openpyxl')
#data2= pd.read_excel(r'200users_5_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_5_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_5_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_5_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
#AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
#AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
#Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)
num_nodes=262
source=263
sink=264
node_expansion_start_node=265
# Create a Gurobi model
m = gp.Model("Network_Dual_LB")
capacities1 = {}
Objective_ValueLB=0
df6={}

# Decision variable: Binary variable indicating if an edge is selected
theta = m.addVars(A.edges, vtype=GRB.CONTINUOUS, name="theta")
pi = m.addVars(A.nodes,  vtype=GRB.CONTINUOUS, name="pi")
mu = m.addVars(A.edges,  vtype=GRB.CONTINUOUS, name="mu") 
z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
#Objective function: Min-cut (Dual of max flow)
m.setObjective(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j] for i, j in A.edges), GRB.MINIMIZE)
# Constraints: Ensure connectivity
m.addConstrs(pi[i]-pi[j]+theta[i, j]>=0 for i, j in A.edges)
m.addConstr(pi[sink]-pi[source]>=1)
#m.addConstrs(z[i, j]==0 for i, j in A.edges)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
m.addConstrs(mu[i,j]+z[i,j] - theta[i,j] >= 0 for  i, j in A.edges)
m.addConstrs(z[i,j]==0 for i,j in A.edges)
# Optimize the model
start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
m.optimize()
Objective_Value_Base5= m.objVal

result=pd.DataFrame({'Network 1': [Objective_Value_Base1], 'Network 2': [Objective_Value_Base2], 'Network 3':[Objective_Value_Base3],'Network 4':[Objective_Value_Base4],'Network 5':[Objective_Value_Base5]})
f_p='Result.xlsx'
result.to_excel(f_p, index=False)