# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:58:21 2024

@author: farha
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 11:33:21 2024

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
data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Reduced_A')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Reduced_AR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Reduced_AuAR')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet22')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Reduced_Nodes_ResArcs')
data6= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='NodeEx')
data7= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet19')
data8= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\NodeExpansionData.xlsx', sheet_name='Sheet1')
data9= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet21')
data10= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Second_tier')
data11= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet12')
data12= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Extra_Arcs_Partial')
data13= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet20')
data14= pd.read_excel(r'D:\PhD Research\First_paper\200users_2_base\200users_2_base.xlsx', sheet_name='Sheet23')

#data1= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Reduced_A',engine='openpyxl')
#data2= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Reduced_AR',engine='openpyxl')
#data3= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Reduced_AuAR',engine='openpyxl')
#data4= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet22',engine='openpyxl')
#data5= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Reduced_Nodes_ResArcs',engine='openpyxl')
#data6= pd.read_excel(r'200users_2_base.xlsx', sheet_name='NodeEx',engine='openpyxl')
#data7= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet19',engine='openpyxl')
#data8= pd.read_excel(r'NodeExpansionData.xlsx', sheet_name='Sheet1',engine='openpyxl')
#data9= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet21',engine='openpyxl')
#data10= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Second_tier',engine='openpyxl')
#data11= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet12',engine='openpyxl')
#data12= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Extra_Arcs_Partial',engine='openpyxl')
#data13= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet20',engine='openpyxl')
#data14= pd.read_excel(r'200users_2_base.xlsx', sheet_name='Sheet23',engine='openpyxl')


A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource', 'Capacity'], create_using=nx.DiGraph)
A_full = nx.from_pandas_edgelist(data8, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
S_ij_full=nx.from_pandas_edgelist(data7, 'Source', 'Target', create_using=nx.DiGraph)
Important_nodes_ResArcs_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)
Important_nodes_ResArcs_random_gen_full= nx.from_pandas_edgelist(data9, 'Source', 'Target', create_using=nx.DiGraph)
Important_nodes_random_gen_full= nx.from_pandas_edgelist(data14, 'Source', 'Target', create_using=nx.DiGraph)
AuAR_full = nx.from_pandas_edgelist(data6, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
Second_Tier=nx.from_pandas_edgelist(data10, 'Source', 'Target', create_using=nx.DiGraph)
Lowest_tier_nodes= nx.from_pandas_edgelist(data11, 'Source', 'Target', create_using=nx.DiGraph)
Extra_Arcs_Partial= nx.from_pandas_edgelist(data12, 'Source', 'Target', create_using=nx.DiGraph)
AR_full = nx.from_pandas_edgelist(data13, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)

num_nodes=260
num_res_arcs=130
rand_num=num_nodes+num_res_arcs
Total_arcs_A=1176
Com_arcs=num_res_arcs+Total_arcs_A
source=1
sink=262
node_expansion_start_node=263
nodes_Sij=len(S_ij.edges)
nodes_Sij_Full=len(S_ij_full.edges)
n=10 #sample size for LB

M=25 #Replication numbers for LB

a=list(range(0,num_nodes))
a1=list(range(0,100))
a2=list(range(0,num_res_arcs))
a3=list(range(0,num_nodes))
a4=list(range(0,len(AR.edges)))
a5=list(range(0,len(S_ij_full.edges)))

#Creation of R_{ij} set
arcs=[]
arcs.extend(AR.edges) #Creating a list of restructured arcs
list_of_arcs_R={}  #  Creating of a dict which would create the set R_{ij} based on arc number
for i in a4:
       out_edges1 = list(A.out_edges(arcs[i][0]))
       target_nodes1 = [edge[1] for edge in out_edges1]
       in_edges2 = list(A.in_edges(arcs[i][1]))
       target_nodes2 = [edge[0] for edge in in_edges2]
       all_arcs = []
       for node in target_nodes1:
           set_of_arcs=list(A.out_edges(node))
           c= list(range(0,len(set_of_arcs)))
           for k in c:
             all_arcs.append(set_of_arcs[k])
       for node in target_nodes2:
           set_of_arcs1=list(A.in_edges(node))
           d= list(range(0,len(set_of_arcs1)))
           for l in d:
               all_arcs.append(set_of_arcs1[l])
       # Loop through the target nodes
       list_of_arcs_R[i]=all_arcs   
R = {}
# Assign a list of arcs to each arc
for arc in arcs:
      R[arc] = []
# Add lists of arcs to each arc
for m in a4:
     R[(arcs[m][0],arcs[m][1])].extend(list_of_arcs_R[m]) 
# Convert lists to tuples so that they are iterable
#arc_list1 = {arc: tuple(arc_list) for arc, arc_list in arc_lists.items()} 

# Creation set S_ij

list_of_arcs_S={}
a7=list(range(0,nodes_Sij))
for l1 in a7:
    out_edges = list(A.out_edges(l1+228+node_expansion_start_node))
    target_nodes = [edge[1] for edge in out_edges]
    all_arcs1=[]
    for node in target_nodes:
        set_arcs=list(A.out_edges(node))
        d=list(range(0,len(set_arcs)))
        for l in d:
            all_arcs1.append(set_arcs[l])
    list_of_arcs_S[l1]=all_arcs1
S1={}
arcs1=[]
arcs1.extend(S_ij.edges)
for arc in arcs1:
    S1[arc]=[]     
for m in a7:
     S1[(arcs1[m][0],arcs1[m][1])].extend(list_of_arcs_S[m])  
list_of_arcs_S_full={}
a7_full=list(range(0,nodes_Sij_Full))
for l1 in a7_full:
    out_edges_full = list(A_full.out_edges(l1+200+node_expansion_start_node))
    target_nodes_full = [edge[1] for edge in out_edges_full]
    all_arcs1_full=[]
    for node in target_nodes_full:
        set_arcs_full=list(A_full.out_edges(node))
        d=list(range(0,len(set_arcs_full)))
        for l in d:
            all_arcs1_full.append(set_arcs_full[l])
    list_of_arcs_S_full[l1]=all_arcs1_full
S1_full={}
arcs1_full=[]
arcs1_full.extend(S_ij_full.edges)
for arc in arcs1_full:
    S1_full[arc]=[]     
for m in a7_full:
     S1_full[(arcs1_full[m][0],arcs1_full[m][1])].extend(list_of_arcs_S_full[m])  

#Creation of V_ij
arcs=[]
arcs.extend(AR_full.edges) #Creating a list of restructured arcs
list_of_arcs_R_full={}  #  Creating of a dict which would create the set R_{ij} based on arc number
for i in a2:
       out_edges1 = list(A_full.out_edges(arcs[i][0]))
       target_nodes1 = [edge[1] for edge in out_edges1]
       in_edges2 = list(A_full.in_edges(arcs[i][1]))
       target_nodes2 = [edge[0] for edge in in_edges2]
       all_arcs = []
       for node in target_nodes1:
           set_of_arcs=list(A_full.out_edges(node))
           c= list(range(0,len(set_of_arcs)))
           for k in c:
             all_arcs.append(set_of_arcs[k])
       for node in target_nodes2:
           set_of_arcs1=list(A_full.in_edges(node))
           d= list(range(0,len(set_of_arcs1)))
           for l in d:
               all_arcs.append(set_of_arcs1[l])
       # Loop through the target nodes
       list_of_arcs_R_full[i]=all_arcs  
arcs11=[]
for i in a2:
    arcs12=list(list_of_arcs_R_full[i])
    for j in list(range(0, len(list_of_arcs_R_full[i]))):
        edge=arcs12[j]
        if edge not in arcs11:
            arcs11.append(edge)
list_of_arcs_V={}
for i in list(range(0, len(arcs11))):
    all_arc1=[]
    edge=arcs11[i]
    for j in list(range(0, len(list_of_arcs_R_full))):
        if edge in list_of_arcs_R_full[j]:
            all_arc1.append(arcs[j])
    list_of_arcs_V[i]=all_arc1   
V = {}
# Assign a list of arcs to each arc
for arc in arcs11:
      V[arc] = [] 
      
for m in list(range(0, len(arcs11))):
     V[(arcs11[m][0],arcs11[m][1])].extend(list_of_arcs_V[m]) 

# Generate a list of random integers using seed number
seed_value = 1
random.seed(seed_value)
# Generate a list of random integers
random_integers = [random.randint(1, 100) for _ in range(100)]
M1=list(range(0,M))
S=list(range(0,n)) 

#Cap Modification
a7=list(range(0,len(Extra_Arcs_Partial.edges)))
list_of_arcs_U={}
for l1 in a7:
    out_edges = list(A_full.out_edges(l1+200+node_expansion_start_node))
    target_nodes = [edge[1] for edge in out_edges]
    all_arcs1=[]
    for node in target_nodes:
        set_arcs=list(A_full.out_edges(node))
        d=list(range(0,len(set_arcs)))
        for l in d:
            all_arcs1.append(set_arcs[l])
    list_of_arcs_U[l1]=all_arcs1
U1={}
arcs1=[]
arcs1.extend(Extra_Arcs_Partial.edges)
for arc in arcs1:
    U1[arc]=[]     
for m in a7:
     U1[(arcs1[m][0],arcs1[m][1])].extend(list_of_arcs_U[m])          
for i,j in Extra_Arcs_Partial.edges:
    A[i][j]['Capacity']=sum(A_full[p][q]['Capacity'] for p,q in U1[(i,j)]) 

# Generate a list of random integers using seed number
seed_value = 1
random.seed(seed_value)
# Generate a list of random integers
random_integers = [random.randint(1, 100) for _ in range(100)]
M1=list(range(0,M))
S=list(range(0,n)) 

#Cap Modification
a7=list(range(0,len(Extra_Arcs_Partial.edges)))
list_of_arcs_U={}
for l1 in a7:
    out_edges = list(A_full.out_edges(l1+200+node_expansion_start_node))
    target_nodes = [edge[1] for edge in out_edges]
    all_arcs1=[]
    for node in target_nodes:
        set_arcs=list(A_full.out_edges(node))
        d=list(range(0,len(set_arcs)))
        for l in d:
            all_arcs1.append(set_arcs[l])
    list_of_arcs_U[l1]=all_arcs1



# Create a Gurobi model
#m = gp.Model("Network_Dual_LB")
elapsed_time_Replica=np.zeros((len(M1),1))
b={}
capacities1 = {}
Objective_ValueLB=np.zeros((len(M1),1))
df6={}
df71={}
df9={}
unique_edges = A.edges - S_ij.edges
unique_edges1 = A.edges - S_ij_full.edges
unique_edges_full = A_full.edges - A.edges
second_tier_nodes=S_ij_full.edges-S_ij.edges
Arcs_Common=A.edges-Extra_Arcs_Partial.edges
for l in M1:
    seed_value2 = random_integers[(l)]
    np.random.seed(seed_value2)
    #matrix_sequence = [np.random.choice([0,1], size=(1306, len(S))) for _ in range(1)]
    matrix_sequence = [np.random.choice([0,1], size=(num_nodes, len(S))) for _ in range(1)]
    for scenarios in matrix_sequence:
        #print(scenarios)
        b[l]=scenarios
    rand_a_b = {}
    m_side = gp.Model("Cap_extra")
    u_extra = m_side.addVars(Extra_Arcs_Partial.edges, S, vtype=GRB.CONTINUOUS, name="u_extra")
    m_side.setObjective(2,GRB.MINIMIZE)

    for s in S:
       selected_column = b[l][:,s]
       rand_a_b[s] = selected_column.tolist()
       for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
           Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
       for p,q in A_full.edges:
           Edge=(p,q)
           if Edge in Important_nodes_random_gen_full.edges:
               A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           else:
               A_full[p][q]['Rand']=0
       arc13=[]
       for p,q in Important_nodes_random_gen_full.edges:
           if (p,q) in arcs11:
               if A_full[p][q]['Rand']==1:
                     seed_number = p+q
                     random.seed(seed_number)
                     random_restr = random.choice(V[(p,q)])
                     for (r,t) in V[(p,q)]:
                        if (r,t)== random_restr:
                            edge=(r,t)
                            if edge not in arc13:
                               arc13.append(edge)
                            AR_full[r][t]['Rand']=1
       for p,q in AR_full.edges:
           if (p,q) not in arc13:
               AR_full[p][q]['Rand']=0
              #ac=0             
       for p,q in AuAR_full.edges:
           if (p,q) in Important_nodes_random_gen_full.edges:
                      #ac=ac+1
                AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           elif (p,q) in arc13:
                AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
           else:
                AuAR_full[p][q]['Rand']=0
       for p,q in AuAR.edges:
           Edge=(p,q)
           if Edge in AuAR_full.edges:
               AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
           else:
               AuAR[p][q]['Rand']=0
       list_of_arcs_UR={}
       for l3 in a7:
           node_in=l3+200+node_expansion_start_node
           if node_in in AR_full.nodes:
             out_edges = list(AR_full.out_edges(l3+200+node_expansion_start_node))
             target_nodes=[]
             for p,q in out_edges:
                if AuAR_full[p][q]['Rand']==1:
                   edge=(p,q)
                   target_nodes.append(edge[1])
             all_arcs1=[]
             for node in target_nodes:
               set_arcs=list(A_full.out_edges(node))
               d=list(range(0,len(set_arcs)))
               for l2 in d:
                   all_arcs1.append(set_arcs[l2])
                   
             list_of_arcs_UR[l3]=all_arcs1
           else:
               list_of_arcs_UR[l3]=[] 
       UR={}
       arcs1=[]
       arcs1.extend(Extra_Arcs_Partial.edges)
       for arc in arcs1:
           UR[arc]=[]     
       for m2 in a7:
            UR[(arcs1[m2][0],arcs1[m2][1])].extend(list_of_arcs_UR[m2])     
       for i,j in Extra_Arcs_Partial.edges:
           cap_sum=0
           for p,q in UR[(i,j)]:
               if (p,q) not in U1[(i,j)]:
                   cap_sum=cap_sum+A_full[p][q]['Capacity']
           m_side.addConstr(u_extra[i,j,s]==A[i][j]['Capacity']+cap_sum)
                   
    m_side.optimize()
    m_side.setParam("OutputFlag", 1)
    value={}
    for s in S:
       for i,j in Extra_Arcs_Partial.edges:
                # Access the value of the variable with indices i, j, k
             value[(i, j, s)] = u_extra[i, j, s].X  
    #V_list = [u_extra[i,j,s].X for i,j in Extra_Arcs_Partial.edges for s in S]
    #values_list = list(value.values())
    
    m = gp.Model("Network_Dual_LB")
    start_time_Replica=time.time()
# Decision variable: Binary variable indicating if an edge is selected
    theta = m.addVars(AuAR.edges, S, vtype=GRB.CONTINUOUS, name="theta")
    pi = m.addVars(AuAR.nodes, S, vtype=GRB.CONTINUOUS, name="pi")
    mu = m.addVars(A.edges, S,  vtype=GRB.CONTINUOUS, name="mu")
    delta = m.addVars(AR.edges, S, vtype=GRB.CONTINUOUS, name="delta")
    phi = m.addVars(AR.edges, S, vtype=GRB.CONTINUOUS, name="phi")
    v = m.addVars(AR.edges, S,  vtype=GRB.CONTINUOUS, name="v")
    z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    alpha= m.addVars(A.edges, S, vtype=GRB.BINARY, name="alpha")
    alpha1= m.addVars(Lowest_tier_nodes.edges, S, vtype=GRB.BINARY, name="alpha")
    z1= m.addVars(Lowest_tier_nodes.edges, vtype=GRB.BINARY, name="z1")
#Objective function: Min-cut (Dual of max flow)
    #m.setObjective(gp.quicksum((1/len(S))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in A.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S), GRB.MINIMIZE)
    m.setObjective(gp.quicksum((1/len(S))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in Arcs_Common)+ gp.quicksum(value[(i,j,s)] *  mu [i, j,s] for i, j in Extra_Arcs_Partial.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S), GRB.MINIMIZE)

# Constraints: Ensure connectivity
    m.addConstrs(pi[i,s]-pi[j,s]+theta[i, j,s]>=0 for i, j in AuAR.edges for s in S)
    m.addConstrs(pi[sink,s]-pi[source,s]>=1 for s in S)
    m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
    m.addConstrs(gp.quicksum(alpha1[k,l,s] for k,l in S1_full[(i,j)])>=A_full[i][j]['Tau'] * alpha[i,j,s] for i,j in Second_Tier.edges for s in S)
    rand_a_b = {}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    
    arcs_As=[]
    arcs_As1=[]
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S:
        selected_column = b[l][:,s]
        rand_a_b[s] = selected_column.tolist()
        for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
            Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
        for p,q in A_full.edges:
            Edge=(p,q)
            if Edge in Important_nodes_random_gen_full.edges:
                A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            else:
                A_full[p][q]['Rand']=0
        arc13=[]
        for p,q in Important_nodes_random_gen_full.edges:
            if (p,q) in arcs11:
                if A_full[p][q]['Rand']==1:
                      seed_number = p+q
                      random.seed(seed_number)
                      random_restr = random.choice(V[(p,q)])
                      for (r,t) in V[(p,q)]:
                         if (r,t)== random_restr:
                             edge=(r,t)
                             if edge not in arc13:
                                arc13.append(edge)
                             AR_full[r][t]['Rand']=1
        for p,q in AR_full.edges:
            if (p,q) not in arc13:
                AR_full[p][q]['Rand']=0
               #ac=0             
        for p,q in AuAR_full.edges:
            if (p,q) in Important_nodes_random_gen_full.edges:
                       #ac=ac+1
                 AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            elif (p,q) in arc13:
                 AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
            else:
                 AuAR_full[p][q]['Rand']=0
        for p,q in AuAR.edges:
            Edge=(p,q)
            if Edge in AuAR_full.edges:
                AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
            else:
                AuAR[p][q]['Rand']=0
        c={}
        d=0
        for p,q in second_tier_nodes:
            if  A_full[p][q]['Tau']>sum(AuAR_full[p1][q1]['Rand'] for p1,q1 in S1_full[(p,q)]):
                AuAR[p][q]['Rand']=0
        for r,t in S_ij.edges:
                #arcs_As=[]
          if AuAR[r][t]['Rand']==1:
              if A[r][t]['Tau']<=sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                   edge=(r,t)
                   if edge not in arcs_As:
                        arcs_As.append(edge)
                        c[d]=arcs_As
                        d=d+1
        for r,t in unique_edges:
            if AuAR[r][t]['Rand']==1:
                edge2=(r,t)
                if edge2 not in arcs_As1:
                  arcs_As1.append(edge2)
            else:
                m.addConstr(alpha[r,t,s]==0) 
        for p,q in Lowest_tier_nodes.edges:
              if AuAR_full[p][q]['Rand']==0:
                    m.addConstr(alpha1[p,q,s]==0)
                
        for r,t in S_ij_full.edges:
            if AuAR[r][t]['Rand']==0:
                m.addConstr(alpha[r,t,s]==0)
            else:
                if A_full[r][t]['Tau']>sum(AuAR_full[r1][t1]['Rand'] for r1,t1 in S1_full[(r,t)]):
                   m.addConstr(alpha[r,t,s]==0)
        m.addConstrs(alpha[i,j,s]<=AuAR[i][j]['Rand'] * z[i,j] for i,j in S_ij_full.edges)
        m.addConstrs(alpha[i,j,s]==AuAR[i][j]['Rand'] * z[i,j] for i,j in unique_edges1)
        m.addConstrs(alpha1[i,j,s]==AuAR_full[i][j]['Rand'] * z1[i,j] for i,j in Lowest_tier_nodes.edges)
        #m.addConstrs(alpha[i,j,s]>= (beta[i,j,s] + AuAR[i][j]['Rand'] * z[i,j] -1) for i,j in S_ij.edges)
        m.addConstrs(delta[i,j,s]-AuAR[i][j]['Rand'] * theta [i,j,s] >= 0 for i,j in AR.edges)
        m.addConstrs(mu[i,j,s]+ alpha[i,j,s] - theta[i,j,s] >= 0 for  i, j in A.edges)
        for i, j in AR.edges:
                #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
            m.addConstrs(phi[i, j, s] >= alpha[k,l,s] for k, l in R[(i,j)])
    for i,j in S_ij.edges:
         edge1=(i,j)
         if edge1 not in arcs_As:
            m.addConstr(z[i,j]==0)
    for i,j in unique_edges:
         edge3=(i,j)
         if edge3 not in arcs_As1:
             m.addConstr(z[i,j]==0)
    m.addConstrs(v[i,j,s]<= delta[i,j,s] for i,j in AR.edges for s in S)
    m.addConstrs(v[i,j,s]<= phi[i,j,s] for i,j in AR.edges for s in S)
    m.addConstrs(v[i,j,s]>= delta[i,j,s] + phi[i,j,s] - 1 for i,j in AR.edges for  s in S)
    for l1 in a5:
         out_edges = list(A.out_edges(l1+200+node_expansion_start_node))
         target_nodes = [edge[1] for edge in out_edges]
         m.addConstrs(A[i][j]['Tau'] * z[i,j] <= gp.quicksum(gp.quicksum(z[k,l] for k,l in A.out_edges(r)) for r in target_nodes) for i,j in A.in_edges(l1+200+node_expansion_start_node))
    for i,j in Second_Tier.edges:
         edge=(i,j)
         if edge in A_full.edges:
             #print("Yes")
             m.addConstr(A_full[i][j]['Tau']* z[i,j] <=gp.quicksum(z1[p,q] for p,q in S1_full[(i,j)]) )
     #m.addConstr(gp.quicksum(z[i,j]* A[i][j]['Resource'] for i,j in A.edges) <=60)
    m.addConstr(gp.quicksum(z[i,j]* A[i][j]['Resource'] for i,j in A.edges)+ 2* gp.quicksum(z1[p,q] for p,q in Lowest_tier_nodes.edges) <=60)

 # Optimize the model
    start_time_Replica=time.time()
 # Optimize the model
     #m.setParam("Heuristics", .3)
    m.setParam("Heuristics", .4)
    m.setParam("MIPFocus", 3)
    m.setParam("Cuts", 2)
    m.optimize()
    end_time_Replica=time.time() 
    elapsed_time_Replica[l]=end_time_Replica - start_time_Replica
    Objective_ValueLB[l]= m.objVal
    z_values = {i: z[i].X for i in z}
    z1_values = {i: z1[i].X for i in z1}
    # Creating a DataFrame from the decision variable values
    df6[l] = pd.DataFrame(list(z_values.items()), columns=['Variable', 'Value'])
    #df6[:,l]=z_values
    #df6[l].to_excel('decision_variable_values(l).xlsx', index=False)
    interdiction_lowest=[]
    interdiction_lowest.extend(A_full.edges)
    df8={}
    for arc in interdiction_lowest:
      df8[arc]=[]    
    for i,j in A_full.edges:
       edge=(i,j)
       if edge in A.edges:
         df8[edge]=z_values[(i,j)]
       else:
         if edge in Lowest_tier_nodes.edges:
            df8[edge]=z1_values[(i,j)]
         else:
             df8[edge]=0
    df9[l]=pd.DataFrame(list(df8.items()), columns=['Variable', 'Value'])

ElapTime1=pd.DataFrame(elapsed_time_Replica)
file_path = 'elapsed time_base2_HM_2(n_10,m_5).xlsx'
#ElapTime1.to_excel(file_path, index=False)



combined_df = pd.concat(df9.values(), axis=1)

# Specify the Excel file path
excel_file_path = 'combined_base1_HM_2(n_10,m_5).xlsx'
#combined_df.to_excel(excel_file_path, index=False)

# Writing the DataFrame to an Excel file

Objec= pd.DataFrame(Objective_ValueLB)

# Specify the Excel file path
#excel_file_path1 = 'Obj_valueLB_base1_Heu_ModCap_1(n_10,m_5).xlsx'

# Save the DataFrame to an Excel file
#Objec.to_excel(excel_file_path1, index=False)


# Your dictionary
#Specify the file path
file_path_pickle = 'z_values_base1_Stability_HM_10(25)_Class2.pkl'

 #Save the dictionary to a pickle file
with open(file_path_pickle, 'wb') as pickle_file:
   pickle.dump(df9, pickle_file)

n1=5000 #out of sample
n2=n      #in sample

T=1
No_LB=list(range(0,1))
No_UB=list(range(0,M))

num_nodes=260
num_res_arcs=130
rand_num=num_nodes+num_res_arcs
Total_arcs_A=1176
Com_arcs=num_res_arcs+Total_arcs_A
source=1
sink=262
node_expansion_start_node=263
nodes_Sij=len(S_ij.edges)
nodes_Sij_Full=len(S_ij_full.edges)

a=list(range(0,num_nodes))
a1=list(range(0,100))
a2=list(range(0,num_res_arcs))
a3=list(range(0,num_nodes))
a4=list(range(0,len(AR.edges)))
a5=list(range(0,len(S_ij_full.edges)))
#Creation of R_{ij} set
arcs=[]
arcs.extend(AR.edges) #Creating a list of restructured arcs
list_of_arcs_R={}  #  Creating of a dict which would create the set R_{ij} based on arc number
for i in a4:
       out_edges1 = list(A.out_edges(arcs[i][0]))
       target_nodes1 = [edge[1] for edge in out_edges1]
       in_edges2 = list(A.in_edges(arcs[i][1]))
       target_nodes2 = [edge[0] for edge in in_edges2]
       all_arcs = []
       for node in target_nodes1:
           set_of_arcs=list(A.out_edges(node))
           c= list(range(0,len(set_of_arcs)))
           for k in c:
             all_arcs.append(set_of_arcs[k])
       for node in target_nodes2:
           set_of_arcs1=list(A.in_edges(node))
           d= list(range(0,len(set_of_arcs1)))
           for l in d:
               all_arcs.append(set_of_arcs1[l])
       # Loop through the target nodes
       list_of_arcs_R[i]=all_arcs   
R = {}
# Assign a list of arcs to each arc
for arc in arcs:
      R[arc] = []
# Add lists of arcs to each arc
for m in a4:
     R[(arcs[m][0],arcs[m][1])].extend(list_of_arcs_R[m]) 
# Convert lists to tuples so that they are iterable
#arc_list1 = {arc: tuple(arc_list) for arc, arc_list in arc_lists.items()} 

# Creation set S_ij

list_of_arcs_S={}
a7=list(range(0,nodes_Sij))
for l1 in a7:
    out_edges = list(A.out_edges(l1+228+node_expansion_start_node))
    target_nodes = [edge[1] for edge in out_edges]
    all_arcs1=[]
    for node in target_nodes:
        set_arcs=list(A.out_edges(node))
        d=list(range(0,len(set_arcs)))
        for l in d:
            all_arcs1.append(set_arcs[l])
    list_of_arcs_S[l1]=all_arcs1
S1={}
arcs1=[]
arcs1.extend(S_ij.edges)
for arc in arcs1:
    S1[arc]=[]     
for m in a7:
     S1[(arcs1[m][0],arcs1[m][1])].extend(list_of_arcs_S[m])  
list_of_arcs_S_full={}
a7_full=list(range(0,nodes_Sij_Full))
for l1 in a7_full:
    out_edges_full = list(A_full.out_edges(l1+200+node_expansion_start_node))
    target_nodes_full = [edge[1] for edge in out_edges_full]
    all_arcs1_full=[]
    for node in target_nodes_full:
        set_arcs_full=list(A_full.out_edges(node))
        d=list(range(0,len(set_arcs_full)))
        for l in d:
            all_arcs1_full.append(set_arcs_full[l])
    list_of_arcs_S_full[l1]=all_arcs1_full
S1_full={}
arcs1_full=[]
arcs1_full.extend(S_ij_full.edges)
for arc in arcs1_full:
    S1_full[arc]=[]     
for m in a7_full:
     S1_full[(arcs1_full[m][0],arcs1_full[m][1])].extend(list_of_arcs_S_full[m])  
# Generate a list of random integers using seed number


#Cap Modification
a7=list(range(0,len(Extra_Arcs_Partial.edges)))
list_of_arcs_U={}
for l1 in a7:
    out_edges = list(A_full.out_edges(l1+200+node_expansion_start_node))
    target_nodes = [edge[1] for edge in out_edges]
    all_arcs1=[]
    for node in target_nodes:
        set_arcs=list(A_full.out_edges(node))
        d=list(range(0,len(set_arcs)))
        for l in d:
            all_arcs1.append(set_arcs[l])
    list_of_arcs_U[l1]=all_arcs1
U1={}
arcs1=[]
arcs1.extend(Extra_Arcs_Partial.edges)
for arc in arcs1:
    U1[arc]=[]     
for m in a7:
     U1[(arcs1[m][0],arcs1[m][1])].extend(list_of_arcs_U[m])          



# Create a Gurobi model
#m = gp.Model("Network_Dual_LB")

b={}
capacities1 = {}

df6={}
df71={}
df9={}
unique_edges = A.edges - S_ij.edges
unique_edges1 = A.edges - S_ij_full.edges
unique_edges_full = A_full.edges - A.edges
second_tier_nodes=S_ij_full.edges-S_ij.edges
Arcs_Common=A.edges-Extra_Arcs_Partial.edges


UpperBound=np.zeros((M,1))
S3=list(range(0,T))

#file_path_pickle ='z_values_base1_Stability_Heu_prac_1.pkl'
#file_path_pickle = r'C:/Users/fjanan/Downloads/Research Code/200users_1_base\z_values_base1_AM_1(n,10_m,5).pkl'

# Load the dictionary from the pickle file
with open(file_path_pickle, 'rb') as pickle_file:
    Interdiction_Values = pickle.load(pickle_file)

#file_path_pickle ='z_values_base1_HeuCap_Stability_1(n_40,m_9_16).pkl'
#with open(file_path_pickle, 'rb') as pickle_file:
 #   Interdiction_Values1 = pickle.load(pickle_file)
#file_path_pickle ='z_values_base1_HeuCap_Stability_1(n_40,m_17_25).pkl'
#with open(file_path_pickle, 'rb') as pickle_file:
 #   Interdiction_Values2 = pickle.load(pickle_file)
#for iUB in No_UB:
Final_interdiction={}
a_in=list(range(0,M))
for i in a_in:
    Final_interdiction[i]=Interdiction_Values[i]
   # Final_interdiction[8+i]=Interdiction_Values1[i]
#a_in=list(range(0,9))
#for i in a_in:
 #   Final_interdiction[16+i]=Interdiction_Values2[i]
S4=list(range(0,n1))
#for l in L:

#elapsed_time_Replica_UB=np.zeros((len(S3),1))
a={}
  
unique_edges = A.edges - S_ij.edges  
a4=list(range(0,n1))
elapsed_time_Replica1_out_of_sample = np.zeros((len(S3),len(No_UB)))
Obj_Val_UB_HM_out_of_sample=np.zeros((len(S3),len(No_UB)))
# Generate a list of random integers
#seed_value = 2
#random.seed(seed_value)
#random_integers_UB = [random.randint(1, 100) for _ in range(5)]
#random_integers_UB1 = np.zeros((len(S3),len(No_UB)))
#aR=0

seed_value = 2
random.seed(seed_value)
matrix_sequence = [np.random.choice([0,1], size=(num_nodes, len(S4))) for _ in range(1)]
S5=list(range(0,n2))
elapsed_time_Replica1_in_sample = np.zeros((len(S3),len(No_UB)))
Obj_Val_UB_HM_in_sample=np.zeros((len(S3),len(No_UB)))
seed_value = 1
random.seed(seed_value)
# Generate a list of random integers
random_integers = [random.randint(1, 100) for _ in range(30)]
#for i in No_UB:
 #   for j in S3:
 #       random_integers_UB1[j][i]=random_integers_UB[aR+j]
  #  aR=aR+T
for iUB in No_UB:
  inderdiction = {}
  df3=pd.DataFrame(Final_interdiction[iUB])
  selected_column2 = df3.iloc[:, 1]
  interdiction = selected_column2.tolist()
  for edge, interdict_value in zip(A_full.edges(), interdiction):
          A_full[edge[0]][edge[1]]['Interdict'] = interdict_value
  for i,j in A_full.edges:
      if A_full[i][j] ['Interdict']>=0.5:
          A_full[i][j] ['Interdict']=1
      else: 
          A_full[i][j] ['Interdict']=0  
  for i,j in A.edges:
      if (i,j) in A_full.edges:
            A[i][j] ['Interdict']=A_full[i][j] ['Interdict']
      else: 
            A[i][j] ['Interdict']=0 
  #for i,j in lowest_tier_nodes.edges:
      
#for l in L:  
  b={} 
  a={}
  for l in S3:
    seed_value1 = random_integers[iUB]
    seed_value1_int = int(seed_value1)
    np.random.seed(seed_value1_int)
    #matrix_sequence = [np.random.choice([0,1], size=(1306, len(S4))) for _ in range(1)]
    #matrix_sequence = [np.random.choice([0,1], size=(1046, len(S4))) for _ in range(1)]
    matrix_sequence1 = [np.random.choice([0,1], size=(num_nodes, len(S5))) for _ in range(1)]

    #matrix_sequence=[list_of_arrays]

    # Print the binary matrix
    #for row in binary_matrix:
     #   print(row)
    for scenarios1 in matrix_sequence:
        #print(scenarios)
        b[l]=scenarios1
    for scenarios2 in matrix_sequence1:
        #print(scenarios)
        a[l]=scenarios2
        Objective=0
    rand_a_b = {}
    m_side = gp.Model("Cap_extra")
    u_extra = m_side.addVars(Extra_Arcs_Partial.edges, S4, vtype=GRB.CONTINUOUS, name="u_extra")
    m_side.setObjective(2,GRB.MINIMIZE)

    for s in S4:
       selected_column = b[l][:,s]
       rand_a_b[s] = selected_column.tolist()
       for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
           Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
       for p,q in A_full.edges:
           Edge=(p,q)
           if Edge in Important_nodes_random_gen_full.edges:
               A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           else:
               A_full[p][q]['Rand']=0
       arc13=[]
       for p,q in Important_nodes_random_gen_full.edges:
           if (p,q) in arcs11:
               if A_full[p][q]['Rand']==1:
                     seed_number = p+q
                     random.seed(seed_number)
                     random_restr = random.choice(V[(p,q)])
                     for (r,t) in V[(p,q)]:
                        if (r,t)== random_restr:
                            edge=(r,t)
                            if edge not in arc13:
                               arc13.append(edge)
                            AR_full[r][t]['Rand']=1
       for p,q in AR_full.edges:
           if (p,q) not in arc13:
               AR_full[p][q]['Rand']=0
              #ac=0             
       for p,q in AuAR_full.edges:
           if (p,q) in Important_nodes_random_gen_full.edges:
                      #ac=ac+1
                AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           elif (p,q) in arc13:
                AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
           else:
                AuAR_full[p][q]['Rand']=0
       for p,q in AuAR.edges:
           Edge=(p,q)
           if Edge in AuAR_full.edges:
               AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
           else:
               AuAR[p][q]['Rand']=0
       list_of_arcs_UR={}
       for l3 in a7:
           node_in=l3+200+node_expansion_start_node
           if node_in in AR_full.nodes:
             out_edges = list(AR_full.out_edges(l3+200+node_expansion_start_node))
             target_nodes=[]
             for p,q in out_edges:
                if AuAR_full[p][q]['Rand']==1:
                   edge=(p,q)
                   target_nodes.append(edge[1])
             all_arcs1=[]
             for node in target_nodes:
               set_arcs=list(A_full.out_edges(node))
               d=list(range(0,len(set_arcs)))
               for l2 in d:
                   all_arcs1.append(set_arcs[l2])
                   
             list_of_arcs_UR[l3]=all_arcs1
           else:
               list_of_arcs_UR[l3]=[] 
       UR={}
       arcs1=[]
       arcs1.extend(Extra_Arcs_Partial.edges)
       for arc in arcs1:
           UR[arc]=[]     
       for m2 in a7:
            UR[(arcs1[m2][0],arcs1[m2][1])].extend(list_of_arcs_UR[m2])     
       for i,j in Extra_Arcs_Partial.edges:
           cap_sum=0
           for p,q in UR[(i,j)]:
               if (p,q) not in U1[(i,j)]:
                   cap_sum=cap_sum+A_full[p][q]['Capacity']
           m_side.addConstr(u_extra[i,j,s]==A[i][j]['Capacity']+cap_sum)
                   
    m_side.optimize()
    m_side.setParam("OutputFlag", 1)
    value={}
    for s in S4:
       for i,j in Extra_Arcs_Partial.edges:
                # Access the value of the variable with indices i, j, k
             value[(i, j, s)] = u_extra[i, j, s].X 
    m = gp.Model("Network_Dual_UB")
    start_time_Replica=time.time()
# Decision variable: Binary variable indicating if an edge is selected
    theta = m.addVars(AuAR.edges, S4, vtype=GRB.CONTINUOUS, name="theta")
    pi = m.addVars(AuAR.nodes, S4, vtype=GRB.CONTINUOUS, name="pi")
    mu = m.addVars(A.edges, S4,  vtype=GRB.CONTINUOUS, name="mu")
    delta = m.addVars(AR.edges, S4, vtype=GRB.CONTINUOUS, name="delta")
    phi = m.addVars(AR.edges, S4, vtype=GRB.CONTINUOUS, name="phi")
    v = m.addVars(AR.edges, S4,  vtype=GRB.CONTINUOUS, name="v")
    #z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    alpha= m.addVars(A.edges, S4, vtype=GRB.BINARY, name="alpha")
    alpha1= m.addVars(Lowest_tier_nodes.edges, S4, vtype=GRB.BINARY, name="alpha")
    #z1= m.addVars(Lowest_tier_nodes.edges, vtype=GRB.BINARY, name="z1")
#Objective function: Min-cut (Dual of max flow)
    #m.setObjective(gp.quicksum((1/len(S))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in A.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S), GRB.MINIMIZE)
    m.setObjective(gp.quicksum((1/len(S4))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in Arcs_Common)+ gp.quicksum(value[(i,j,s)] *  mu [i, j,s] for i, j in Extra_Arcs_Partial.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S4), GRB.MINIMIZE)

# Constraints: Ensure connectivity
    m.addConstrs(pi[i,s]-pi[j,s]+theta[i, j,s]>=0 for i, j in AuAR.edges for s in S4)
    m.addConstrs(pi[sink,s]-pi[source,s]>=1 for s in S4)
    m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S4)
    m.addConstrs(gp.quicksum(alpha1[k,l,s] for k,l in S1_full[(i,j)])>=A_full[i][j]['Tau'] * alpha[i,j,s] for i,j in Second_Tier.edges for s in S4)
    rand_a_b = {}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    
    arcs_As=[]
    arcs_As1=[]
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S4:
        selected_column = b[l][:,s]
        rand_a_b[s] = selected_column.tolist()
        for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
            Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
        for p,q in A_full.edges:
            Edge=(p,q)
            if Edge in Important_nodes_random_gen_full.edges:
                A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            else:
                A_full[p][q]['Rand']=0
        arc13=[]
        for p,q in Important_nodes_random_gen_full.edges:
            if (p,q) in arcs11:
                if A_full[p][q]['Rand']==1:
                      seed_number = p+q
                      random.seed(seed_number)
                      random_restr = random.choice(V[(p,q)])
                      for (r,t) in V[(p,q)]:
                         if (r,t)== random_restr:
                             edge=(r,t)
                             if edge not in arc13:
                                arc13.append(edge)
                             AR_full[r][t]['Rand']=1
        for p,q in AR_full.edges:
            if (p,q) not in arc13:
                AR_full[p][q]['Rand']=0
               #ac=0             
        for p,q in AuAR_full.edges:
            if (p,q) in Important_nodes_random_gen_full.edges:
                       #ac=ac+1
                 AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            elif (p,q) in arc13:
                 AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
            else:
                 AuAR_full[p][q]['Rand']=0
        for p,q in AuAR.edges:
            Edge=(p,q)
            if Edge in AuAR_full.edges:
                AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
            else:
                AuAR[p][q]['Rand']=0
        c={}
        d=0
        for p,q in second_tier_nodes:
            if  A_full[p][q]['Tau']>sum(AuAR_full[p1][q1]['Rand'] for p1,q1 in S1_full[(p,q)]):
                AuAR[p][q]['Rand']=0
        for r,t in S_ij.edges:
                #arcs_As=[]
          if AuAR[r][t]['Rand']==1:
              if A[r][t]['Tau']<=sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                   edge=(r,t)
                   if edge not in arcs_As:
                        arcs_As.append(edge)
                        c[d]=arcs_As
                        d=d+1
        for r,t in unique_edges:
            if AuAR[r][t]['Rand']==1:
                edge2=(r,t)
                if edge2 not in arcs_As1:
                  arcs_As1.append(edge2)
            else:
                m.addConstr(alpha[r,t,s]==0) 
        for p,q in Lowest_tier_nodes.edges:
              if AuAR_full[p][q]['Rand']==0:
                    m.addConstr(alpha1[p,q,s]==0)
                
        for r,t in S_ij_full.edges:
            if AuAR[r][t]['Rand']==0:
                m.addConstr(alpha[r,t,s]==0)
            else:
                if A_full[r][t]['Tau']>sum(AuAR_full[r1][t1]['Rand'] for r1,t1 in S1_full[(r,t)]):
                   m.addConstr(alpha[r,t,s]==0)
        m.addConstrs(alpha[i,j,s]<=AuAR[i][j]['Rand'] * A_full[i][j]['Interdict'] for i,j in S_ij_full.edges)
        m.addConstrs(alpha[i,j,s]==AuAR[i][j]['Rand'] * A[i][j]['Interdict'] for i,j in unique_edges1)
        m.addConstrs(alpha1[i,j,s]==AuAR_full[i][j]['Rand'] * A_full[i][j]['Interdict'] for i,j in Lowest_tier_nodes.edges)
        #m.addConstrs(alpha[i,j,s]>= (beta[i,j,s] + AuAR[i][j]['Rand'] * z[i,j] -1) for i,j in S_ij.edges)
        m.addConstrs(delta[i,j,s]-AuAR[i][j]['Rand'] * theta [i,j,s] >= 0 for i,j in AR.edges)
        m.addConstrs(mu[i,j,s]+ alpha[i,j,s] - theta[i,j,s] >= 0 for  i, j in A.edges)
        for i, j in AR.edges:
                #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
            m.addConstrs(phi[i, j, s] >= alpha[k,l,s] for k, l in R[(i,j)])

    m.addConstrs(v[i,j,s]<= delta[i,j,s] for i,j in AR.edges for s in S4)
    m.addConstrs(v[i,j,s]<= phi[i,j,s] for i,j in AR.edges for s in S4)
    m.addConstrs(v[i,j,s]>= delta[i,j,s] + phi[i,j,s] - 1 for i,j in AR.edges for  s in S4)
    
    
     #m.addConstr(gp.quicksum(z[i,j]* A[i][j]['Resource'] for i,j in A.edges) <=60)
    
 # Optimize the model
    start_time_Replica=time.time()
 # Optimize the model
     #m.setParam("Heuristics", .3)
    m.setParam("Heuristics", .4)
    m.setParam("MIPFocus", 3)
    m.setParam("Cuts", 2)
    m.optimize()
   
    end_time_Replica=time.time() 
    elapsed_time_Replica1_out_of_sample[l][iUB]=end_time_Replica - start_time_Replica
    Obj_Val_UB_HM_out_of_sample[l][iUB]= m.objVal
    
    
    #####In Sample
    rand_a_b = {}
    m_side1 = gp.Model("Cap_extra")
    u_extra1 = m_side1.addVars(Extra_Arcs_Partial.edges, S5, vtype=GRB.CONTINUOUS, name="u_extra1")
    m_side1.setObjective(2,GRB.MINIMIZE)

    for s in S5:
       selected_column = a[l][:,s]
       rand_a_b[s] = selected_column.tolist()
       for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
           Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
       for p,q in A_full.edges:
           Edge=(p,q)
           if Edge in Important_nodes_random_gen_full.edges:
               A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           else:
               A_full[p][q]['Rand']=0
       arc13=[]
       for p,q in Important_nodes_random_gen_full.edges:
           if (p,q) in arcs11:
               if A_full[p][q]['Rand']==1:
                     seed_number = p+q
                     random.seed(seed_number)
                     random_restr = random.choice(V[(p,q)])
                     for (r,t) in V[(p,q)]:
                        if (r,t)== random_restr:
                            edge=(r,t)
                            if edge not in arc13:
                               arc13.append(edge)
                            AR_full[r][t]['Rand']=1
       for p,q in AR_full.edges:
           if (p,q) not in arc13:
               AR_full[p][q]['Rand']=0
              #ac=0             
       for p,q in AuAR_full.edges:
           if (p,q) in Important_nodes_random_gen_full.edges:
                      #ac=ac+1
                AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
           elif (p,q) in arc13:
                AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
           else:
                AuAR_full[p][q]['Rand']=0
       for p,q in AuAR.edges:
           Edge=(p,q)
           if Edge in AuAR_full.edges:
               AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
           else:
               AuAR[p][q]['Rand']=0
       list_of_arcs_UR={}
       for l3 in a7:
           node_in=l3+200+node_expansion_start_node
           if node_in in AR_full.nodes:
             out_edges = list(AR_full.out_edges(l3+200+node_expansion_start_node))
             target_nodes=[]
             for p,q in out_edges:
                if AuAR_full[p][q]['Rand']==1:
                   edge=(p,q)
                   target_nodes.append(edge[1])
             all_arcs1=[]
             for node in target_nodes:
               set_arcs=list(A_full.out_edges(node))
               d=list(range(0,len(set_arcs)))
               for l2 in d:
                   all_arcs1.append(set_arcs[l2])
                   
             list_of_arcs_UR[l3]=all_arcs1
           else:
               list_of_arcs_UR[l3]=[] 
       UR={}
       arcs1=[]
       arcs1.extend(Extra_Arcs_Partial.edges)
       for arc in arcs1:
           UR[arc]=[]     
       for m2 in a7:
            UR[(arcs1[m2][0],arcs1[m2][1])].extend(list_of_arcs_UR[m2])     
       for i,j in Extra_Arcs_Partial.edges:
           cap_sum=0
           for p,q in UR[(i,j)]:
               if (p,q) not in U1[(i,j)]:
                   cap_sum=cap_sum+A_full[p][q]['Capacity']
           m_side1.addConstr(u_extra1[i,j,s]==A[i][j]['Capacity']+cap_sum)
                   
    m_side1.optimize()
    m_side1.setParam("OutputFlag", 1)
    value1={}
    for s in S5:
       for i,j in Extra_Arcs_Partial.edges:
                # Access the value of the variable with indices i, j, k
             value1[(i, j, s)] = u_extra1[i, j, s].X 
    m_in = gp.Model("Network_Dual_UB")
    start_time_Replica=time.time()
# Decision variable: Binary variable indicating if an edge is selected
    theta = m_in.addVars(AuAR.edges, S5, vtype=GRB.CONTINUOUS, name="theta")
    pi = m_in.addVars(AuAR.nodes, S5, vtype=GRB.CONTINUOUS, name="pi")
    mu = m_in.addVars(A.edges, S5,  vtype=GRB.CONTINUOUS, name="mu")
    delta = m_in.addVars(AR.edges, S5, vtype=GRB.CONTINUOUS, name="delta")
    phi = m_in.addVars(AR.edges, S5, vtype=GRB.CONTINUOUS, name="phi")
    v = m_in.addVars(AR.edges, S5,  vtype=GRB.CONTINUOUS, name="v")
    #z = m.addVars(A.edges, vtype=GRB.BINARY, name="z")
    alpha= m_in.addVars(A.edges, S5, vtype=GRB.BINARY, name="alpha")
    alpha1= m_in.addVars(Lowest_tier_nodes.edges, S5, vtype=GRB.BINARY, name="alpha")
    #z1= m.addVars(Lowest_tier_nodes.edges, vtype=GRB.BINARY, name="z1")
#Objective function: Min-cut (Dual of max flow)
    #m.setObjective(gp.quicksum((1/len(S))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in A.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S), GRB.MINIMIZE)
    m_in.setObjective(gp.quicksum((1/len(S5))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in Arcs_Common)+ gp.quicksum(value1[(i,j,s)] *  mu [i, j,s] for i, j in Extra_Arcs_Partial.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S5), GRB.MINIMIZE)

# Constraints: Ensure connectivity
    m_in.addConstrs(pi[i,s]-pi[j,s]+theta[i, j,s]>=0 for i, j in AuAR.edges for s in S5)
    m_in.addConstrs(pi[sink,s]-pi[source,s]>=1 for s in S5)
    m_in.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S5)
    m_in.addConstrs(gp.quicksum(alpha1[k,l,s] for k,l in S1_full[(i,j)])>=A_full[i][j]['Tau'] * alpha[i,j,s] for i,j in Second_Tier.edges for s in S5)
    rand_a_b = {}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    
    arcs_As=[]
    arcs_As1=[]
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S5:
        selected_column = a[l][:,s]
        rand_a_b[s] = selected_column.tolist()
        for edge, rand in zip(Important_nodes_random_gen_full.edges(), rand_a_b[s]):
            Important_nodes_random_gen_full[edge[0]][edge[1]]['Rand'] = rand
        for p,q in A_full.edges:
            Edge=(p,q)
            if Edge in Important_nodes_random_gen_full.edges:
                A_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            else:
                A_full[p][q]['Rand']=0
        arc13=[]
        for p,q in Important_nodes_random_gen_full.edges:
            if (p,q) in arcs11:
                if A_full[p][q]['Rand']==1:
                      seed_number = p+q
                      random.seed(seed_number)
                      random_restr = random.choice(V[(p,q)])
                      for (r,t) in V[(p,q)]:
                         if (r,t)== random_restr:
                             edge=(r,t)
                             if edge not in arc13:
                                arc13.append(edge)
                             AR_full[r][t]['Rand']=1
        for p,q in AR_full.edges:
            if (p,q) not in arc13:
                AR_full[p][q]['Rand']=0
               #ac=0             
        for p,q in AuAR_full.edges:
            if (p,q) in Important_nodes_random_gen_full.edges:
                       #ac=ac+1
                 AuAR_full[p][q]['Rand']=Important_nodes_random_gen_full[p][q]['Rand']
            elif (p,q) in arc13:
                 AuAR_full[p][q]['Rand']=AR_full[p][q]['Rand']
            else:
                 AuAR_full[p][q]['Rand']=0
        for p,q in AuAR.edges:
            Edge=(p,q)
            if Edge in AuAR_full.edges:
                AuAR[p][q]['Rand']=AuAR_full[p][q]['Rand']
            else:
                AuAR[p][q]['Rand']=0
        c={}
        d=0
        for p,q in second_tier_nodes:
            if  A_full[p][q]['Tau']>sum(AuAR_full[p1][q1]['Rand'] for p1,q1 in S1_full[(p,q)]):
                AuAR[p][q]['Rand']=0
        for r,t in S_ij.edges:
                #arcs_As=[]
          if AuAR[r][t]['Rand']==1:
              if A[r][t]['Tau']<=sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                   edge=(r,t)
                   if edge not in arcs_As:
                        arcs_As.append(edge)
                        c[d]=arcs_As
                        d=d+1
        for r,t in unique_edges:
            if AuAR[r][t]['Rand']==1:
                edge2=(r,t)
                if edge2 not in arcs_As1:
                  arcs_As1.append(edge2)
            else:
                m_in.addConstr(alpha[r,t,s]==0) 
        for p,q in Lowest_tier_nodes.edges:
              if AuAR_full[p][q]['Rand']==0:
                    m_in.addConstr(alpha1[p,q,s]==0)
                
        for r,t in S_ij_full.edges:
            if AuAR[r][t]['Rand']==0:
                m_in.addConstr(alpha[r,t,s]==0)
            else:
                if A_full[r][t]['Tau']>sum(AuAR_full[r1][t1]['Rand'] for r1,t1 in S1_full[(r,t)]):
                   m_in.addConstr(alpha[r,t,s]==0)
        m_in.addConstrs(alpha[i,j,s]<=AuAR[i][j]['Rand'] * A_full[i][j]['Interdict'] for i,j in S_ij_full.edges)
        m_in.addConstrs(alpha[i,j,s]==AuAR[i][j]['Rand'] * A[i][j]['Interdict'] for i,j in unique_edges1)
        m_in.addConstrs(alpha1[i,j,s]==AuAR_full[i][j]['Rand'] * A_full[i][j]['Interdict'] for i,j in Lowest_tier_nodes.edges)
        #m.addConstrs(alpha[i,j,s]>= (beta[i,j,s] + AuAR[i][j]['Rand'] * z[i,j] -1) for i,j in S_ij.edges)
        m_in.addConstrs(delta[i,j,s]-AuAR[i][j]['Rand'] * theta [i,j,s] >= 0 for i,j in AR.edges)
        m_in.addConstrs(mu[i,j,s]+ alpha[i,j,s] - theta[i,j,s] >= 0 for  i, j in A.edges)
        for i, j in AR.edges:
                #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
            m_in.addConstrs(phi[i, j, s] >= alpha[k,l,s] for k, l in R[(i,j)])

    m_in.addConstrs(v[i,j,s]<= delta[i,j,s] for i,j in AR.edges for s in S5)
    m_in.addConstrs(v[i,j,s]<= phi[i,j,s] for i,j in AR.edges for s in S5)
    m_in.addConstrs(v[i,j,s]>= delta[i,j,s] + phi[i,j,s] - 1 for i,j in AR.edges for  s in S5)
    
    
     #m.addConstr(gp.quicksum(z[i,j]* A[i][j]['Resource'] for i,j in A.edges) <=60)
    
 # Optimize the model
    start_time_Replica=time.time()
 # Optimize the model
     #m.setParam("Heuristics", .3)
    m_in.setParam("Heuristics", .4)
    m_in.setParam("MIPFocus", 3)
    m_in.setParam("Cuts", 2)
    m_in.optimize()
   
    end_time_Replica=time.time() 
    elapsed_time_Replica1_in_sample[l][iUB]=end_time_Replica - start_time_Replica
    Obj_Val_UB_HM_in_sample[l][iUB]= m_in.objVal

  end_time_UB = time.time()
  
Mean_in_sample=np.mean(Obj_Val_UB_HM_in_sample)
Standard_Deviation_in_sample=np.std(Obj_Val_UB_HM_in_sample)
Mean_out_of_sample=np.mean(Obj_Val_UB_HM_out_of_sample)
Standard_Deviation_out_of_sample=np.std(Obj_Val_UB_HM_out_of_sample)
ElapTimeUB_M1=pd.DataFrame(elapsed_time_Replica1_out_of_sample)
file_path = 'elapTimeUB_Base2_HeuCap_out_of_sample_Class2(n,10_M,25(5000)).xlsx'
#ElapTimeUB_M1.to_excel(file_path, index=False)

Ob_UB_M1=pd.DataFrame(Obj_Val_UB_HM_out_of_sample)
file_path = 'ObjUB_Base2_HeuCap_out_of_sample_Class2(n,10_M,25(5000)).xlsx'
#Ob_UB_M1.to_excel(file_path, index=False)

ElapTimeUB_M1=pd.DataFrame(elapsed_time_Replica1_in_sample)
file_path = 'elapTimeUB_Base2_HeuCap_in_sample_Class2(n,10_M,25).xlsx'
#ElapTimeUB_M1.to_excel(file_path, index=False)

Ob_UB_M1=pd.DataFrame(Obj_Val_UB_HM_in_sample)
file_path = 'ObjUB_Base2_HeuCap_in_sample_Class2(n,10_M,25).xlsx'
#Ob_UB_M1.to_excel(file_path, index=False)

Stability_Tests=pd.DataFrame({'Mean_in_sample': [Mean_in_sample], 'Standard_Deviation_in_sample': [Standard_Deviation_in_sample], 'Mean_out_of_sample':[Mean_out_of_sample],'Standard_Deviation_out_of_sample':[Standard_Deviation_out_of_sample]})
f_p='Stability Tests.xlsx'
Stability_Tests.to_excel(f_p, index=False)  
