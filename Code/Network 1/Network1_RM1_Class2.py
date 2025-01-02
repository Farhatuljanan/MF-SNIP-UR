# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 19:12:41 2024

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

data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_1_base\200users_1_base.xlsx', sheet_name='Sheet4')
#data1= pd.read_excel(r'200users_1_base.xlsx', sheet_name='NetA', engine='openpyxl')
#data2= pd.read_excel(r'200users_1_base.xlsx', sheet_name='ResAR',engine='openpyxl')
#data3= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Comb',engine='openpyxl')
#data4= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sij',engine='openpyxl')
#data5= pd.read_excel(r'200users_1_base.xlsx', sheet_name='Sheet3',engine='openpyxl')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
Important_nodes_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)

num_nodes=262
num_res_arcs=len(AR.edges)
rand_num=num_nodes+num_res_arcs
Total_arcs_A=len(A.edges)
Com_arcs=num_res_arcs+Total_arcs_A
source=263
sink=264
node_expansion_start_node=265
n=10 #number of scenarios in LB
#n1=100  #sample size for UB
M=5 #Replication numbers for LB
#T=2   #Replication numbers for UB
n1=500 #number of scenarios in UB
T=30
a=list(range(0,num_nodes))
a1=list(range(0,100))
a2=list(range(0,num_res_arcs))
a3=list(range(0,num_nodes))
#Creation of R_{ij} set
arcs=[]
arcs.extend(AR.edges) #Creating a list of restructured arcs
list_of_arcs_R={}  #  Creating of a dict which would create the set R_{ij} based on arc number
for i in a2:
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
for m in a2:
     R[(arcs[m][0],arcs[m][1])].extend(list_of_arcs_R[m]) 
# Convert lists to tuples so that they are iterable
#arc_list1 = {arc: tuple(arc_list) for arc, arc_list in arc_lists.items()} 

# Creation set S_ij

list_of_arcs_S={}
a7=list(range(0,62))
for l1 in a7:
    out_edges = list(A.out_edges(l1+200+265))
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
     
#Creation of V_ij

arcs11=[]
for i in a2:
    arcs12=list(list_of_arcs_R[i])
    for j in list(range(0, len(list_of_arcs_R[i]))):
        edge=arcs12[j]
        if edge not in arcs11:
            arcs11.append(edge)
list_of_arcs_V={}
for i in list(range(0, len(arcs11))):
    all_arc1=[]
    edge=arcs11[i]
    for j in list(range(0, len(list_of_arcs_R))):
        if edge in list_of_arcs_R[j]:
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
random_integers = [random.randint(1, 100) for _ in range(30)]
M1=list(range(0,M))
S=list(range(0,n)) 

# Create a Gurobi model
m = gp.Model("Network_Dual_LB")
elapsed_time_Replica=np.zeros((len(M1),1))
b={}
capacities1 = {}
Objective_ValueLB=np.zeros((len(M1),1))
df6={}
df71={}
#df7={}
unique_edges = A.edges - S_ij.edges
for l in M1:
    seed_value2 = random_integers[(l)]
    np.random.seed(seed_value2)
    #matrix_sequence = [np.random.choice([0,1], size=(1306, len(S))) for _ in range(1)]
    matrix_sequence = [np.random.choice([0,1], size=(num_nodes, len(S))) for _ in range(1)]
    for scenarios in matrix_sequence:
        #print(scenarios)
        b[l]=scenarios
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

#Objective function: Min-cut (Dual of max flow)
    m.setObjective(gp.quicksum((1/len(S))*(gp.quicksum(A[i][j]['Capacity'] *  mu [i, j,s] for i, j in A.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v[i,j,s] for i, j in AR.edges)) for s in S), GRB.MINIMIZE)

# Constraints: Ensure connectivity
    m.addConstrs(pi[i,s]-pi[j,s]+theta[i, j,s]>=0 for i, j in AuAR.edges for s in S)
    m.addConstrs(pi[sink,s]-pi[source,s]>=1 for s in S)
    #m.addConstrs(gp.quicksum(alpha[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges for s in S)
    rand_a_b = {}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    
    arcs_As=[]
    arcs_As1=[]
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S:
        selected_column = b[l][:,s]
        rand_a_b[s] = selected_column.tolist()
        for edge, rand in zip(Important_nodes_random_gen.edges(), rand_a_b[s]):
            Important_nodes_random_gen[edge[0]][edge[1]]['Rand'] = rand
        for p,q in A.edges:
            Edge=(p,q)
            if Edge in Important_nodes_random_gen.edges:
                A[p][q]['Rand']=Important_nodes_random_gen[p][q]['Rand']
            else:
                A[p][q]['Rand']=0
        arc13=[]
        for p,q in Important_nodes_random_gen.edges:
            if (p,q) in arcs11:
                if A[p][q]['Rand']==1:
                      seed_number = p+q
                      random.seed(seed_number)
                      random_restr = random.choice(V[(p,q)])
                      for (r,t) in V[(p,q)]:
                         if (r,t)== random_restr:
                             edge=(r,t)
                             if edge not in arc13:
                                arc13.append(edge)
                             AR[r][t]['Rand']=1
        for p,q in AR.edges:
            if (p,q) not in arc13:
                AR[p][q]['Rand']=0
               #ac=0             
        for p,q in AuAR.edges:
            if (p,q) in Important_nodes_random_gen.edges:
                       #ac=ac+1
                 AuAR[p][q]['Rand']=Important_nodes_random_gen[p][q]['Rand']
            elif (p,q) in arc13:
                 AuAR[p][q]['Rand']=AR[p][q]['Rand']
            else:
                 AuAR[p][q]['Rand']=0
        
        #m.addConstrs(sum(A[k][l]['Rand'] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha[i,j,s] for i,j in S_ij.edges)
       # for r,t in S_ij.edges:
        #        #arcs_As=[]
         # if AuAR[r][t]['Rand']==1:
          #    if A[r][t]['Tau']<=sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
           #        edge=(r,t)
            #       if edge not in arcs_As:
             #           arcs_As.append(edge)
        
       # for r,t in unique_edges:
        #    if AuAR[r][t]['Rand']==1:
         #       edge2=(r,t)
          #      if edge2 not in arcs_As1:
           #       arcs_As1.append(edge2)
           # else:
            #    m.addConstr(alpha[r,t,s]==0) 
        #for r,t in S_ij.edges:
           # if AuAR[r][t]['Rand']==0:
           #     m.addConstr(alpha[r,t,s]==0)
          #  else:
              #  if A[r][t]['Tau']>sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                 #   m.addConstr(alpha[r,t,s]==0)
        m.addConstrs(alpha[i,j,s]<=AuAR[i][j]['Rand'] * z[i,j] for i,j in S_ij.edges)
        m.addConstrs(alpha[i,j,s]==AuAR[i][j]['Rand'] * z[i,j] for i,j in unique_edges)
        m.addConstrs(delta[i,j,s]-AuAR[i][j]['Rand'] * theta [i,j,s] >= 0 for i,j in AR.edges)
        m.addConstrs(mu[i,j,s]+alpha[i,j,s] - theta[i,j,s] >= 0 for  i, j in A.edges)
        for i, j in AR.edges:
               #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
            m.addConstrs(phi[i, j, s] >= alpha[k,l,s] for k, l in R[(i,j)])
    #for i,j in S_ij.edges:
     #   edge1=(i,j)
      #  if edge1 not in arcs_As:
       #     m.addConstr(z[i,j]==0)
    #for i,j in unique_edges:
        #edge3=(i,j)
        #if edge3 not in arcs_As1:
        #    m.addConstr(z[i,j]==0)
    m.addConstrs(v[i,j,s]<= delta[i,j,s] for i,j in AR.edges for s in S)
    m.addConstrs(v[i,j,s]<= phi[i,j,s] for i,j in AR.edges for s in S)
    m.addConstrs(v[i,j,s]>= delta[i,j,s] + phi[i,j,s] - 1 for i,j in AR.edges for  s in S)
    for l1 in a:
        out_edges = list(A.out_edges(l1+node_expansion_start_node))
        target_nodes = [edge[1] for edge in out_edges]
        m.addConstrs(A[i][j]['Tau'] * z[i,j] <= gp.quicksum(gp.quicksum(z[k,l] for k,l in A.out_edges(r)) for r in target_nodes)for i,j in A.in_edges(l1+node_expansion_start_node))
    m.addConstr(gp.quicksum(z[i,j]* A[i][j]['Resource'] for i,j in A.edges) <=60)

# Optimize the model
    start_time_Replica=time.time()
# Optimize the model
    #m.setParam("Heuristics", .3)
    m.optimize()
    end_time_Replica=time.time() 
    elapsed_time_Replica[l]=end_time_Replica - start_time_Replica
    Objective_ValueLB[l]= m.objVal
    z_values = {i: z[i].X for i in z}
   
    # Creating a DataFrame from the decision variable values
    df6[l] = pd.DataFrame(list(z_values.items()), columns=['Variable', 'Value'])
    #df6[:,l]=z_values
    #df6[l].to_excel('decision_variable_values(l).xlsx', index=False)

ElapTime1=pd.DataFrame(elapsed_time_Replica)
file_path = 'elapsed time_base1_AM1_2(n,10_m,5).xlsx'
#ElapTime1.to_excel(file_path, index=False)
mean_time=np.mean(elapsed_time_Replica)
max_time=np.max(elapsed_time_Replica)
min_time=np.min(elapsed_time_Replica)
LB=np.mean(Objective_ValueLB)

combined_df = pd.concat(df6.values(), axis=1)

# Specify the Excel file path
excel_file_path = 'combined_base1_AM1_2(n,10_m,5).xlsx'
#combined_df.to_excel(excel_file_path, index=False)

# Writing the DataFrame to an Excel file

Objec= pd.DataFrame(Objective_ValueLB)

# Specify the Excel file path
excel_file_path1 = 'Obj_valueLB_base1_AM1_2(n,10_m,5).xlsx'

# Save the DataFrame to an Excel file
#Objec.to_excel(excel_file_path1, index=False)


# Your dictionary
# Specify the file path
file_path_pickle = 'z_values_base1_AM1_prac.pkl'

# Save the dictionary to a pickle file
with open(file_path_pickle, 'wb') as pickle_file:
    pickle.dump(df6, pickle_file)


No_LB=list(range(0,1))
No_UB=list(range(0,M))
# Create a Gurobi model

UpperBound=np.zeros((M,1))
S3=list(range(0,T))

# Load the dictionary from the pickle file
with open(file_path_pickle, 'rb') as pickle_file:
    Interdiction_Values = pickle.load(pickle_file)

#for iUB in No_UB:

S4=list(range(0,n1))
#for l in L:

#elapsed_time_Replica_UB=np.zeros((len(S3),1))
a={}
  
unique_edges = A.edges - S_ij.edges  
a4=list(range(0,n1))
elapsed_time_Replica1 = np.zeros((len(S3),len(No_UB)))
Objective_Value_UB=np.zeros((len(S3),len(No_UB)))
# Generate a list of random integers
seed_value = 2
random.seed(seed_value)
random_integers_UB = [random.randint(1, 100) for _ in range(900)]
random_integers_UB1 = np.zeros((len(S3),len(No_UB)))
aR=0
for i in No_UB:
    for j in S3:
        random_integers_UB1[j][i]=random_integers_UB[aR+j]
    aR=aR+T
for iUB in No_UB:
  inderdiction = {}
  df3=pd.DataFrame(Interdiction_Values[iUB])
  selected_column2 = df3.iloc[:, 1]
  interdiction = selected_column2.tolist()
  for edge, interdict_value in zip(A.edges(), interdiction):
          A[edge[0]][edge[1]]['Interdict'] = interdict_value
  for i,j in A.edges:
      if A[i][j] ['Interdict']>=0.5:
          A[i][j] ['Interdict']=1
      else: 
          A[i][j] ['Interdict']=0  


  S4=list(range(0,n1))
#for l in L:  
  a={} 
  for l in S3:
    seed_value1 = random_integers_UB1[l][iUB]
    seed_value1_int = int(seed_value1)
    np.random.seed(seed_value1_int)
    #matrix_sequence = [np.random.choice([0,1], size=(1306, len(S4))) for _ in range(1)]
    #matrix_sequence = [np.random.choice([0,1], size=(1046, len(S4))) for _ in range(1)]
    matrix_sequence = [np.random.choice([0,1], size=(num_nodes, len(S4))) for _ in range(1)]

    # Print the binary matrix
    #for row in binary_matrix:
     #   print(row)
    for scenarios1 in matrix_sequence:
        #print(scenarios)
        a[l]=scenarios1
        Objective=0
    m1 = gp.Model("Network_Dual_UB")
    start_time_Replica=time.time()
    # Decision variable: Binary variable indicating if an edge is selected
    theta1 = m1.addVars(AuAR.edges, S4, vtype=GRB.CONTINUOUS, name="theta1")
    pi1 = m1.addVars(AuAR.nodes, S4, vtype=GRB.CONTINUOUS, name="pi1")
    mu1 = m1.addVars(A.edges, S4,  vtype=GRB.CONTINUOUS, name="mu1")
    delta1 = m1.addVars(AR.edges, S4, vtype=GRB.CONTINUOUS, name="delta1")
    phi1 = m1.addVars(AR.edges, S4, vtype=GRB.CONTINUOUS, name="phi1")
    v1 = m1.addVars(AR.edges, S4,  vtype=GRB.CONTINUOUS, name="v1")
    alpha1= m1.addVars(A.edges, S4, vtype=GRB.BINARY, name="alpha")
    #Objective function: Min-cut (Dual of max flow)
    m1.setObjective(gp.quicksum((1/len(S4)) * (gp.quicksum(A[i][j]['Capacity'] *  mu1 [i, j,s] for i, j in A.edges)+ gp.quicksum(AR[i][j]['Capacity'] * v1[i,j,s] for i, j in AR.edges)) for s in S4), GRB.MINIMIZE)
    
    # Constraints: Ensure connectivity
    m1.addConstrs(pi1[i,s]-pi1[j,s]+theta1[i, j,s]>=0 for i, j in AuAR.edges for s in S4)
    m1.addConstrs(pi1[sink,s]-pi1[source,s]>=1 for s in S4)
    arcs_As=[]
    arcs_As1=[]
    randm={}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S4:  
       selected_column2 = a[l][:,s]
       randm[s] = selected_column2.tolist()
       for edge, rand in zip(Important_nodes_random_gen.edges(), randm[s]):
           Important_nodes_random_gen[edge[0]][edge[1]]['Rand'] = rand
       for p,q in A.edges:
            Edge=(p,q)
            if Edge in Important_nodes_random_gen.edges:
                A[p][q]['Rand']=Important_nodes_random_gen[p][q]['Rand']
            else:
                A[p][q]['Rand']=0
       arc13=[]
       for p,q in Important_nodes_random_gen.edges:
            if (p,q) in arcs11:
                if A[p][q]['Rand']==1:
                      seed_number = p+q
                      random.seed(seed_number)
                      random_restr = random.choice(V[(p,q)])
                      for (r,t) in V[(p,q)]:
                         if (r,t)== random_restr:
                             edge=(r,t)
                             if edge not in arc13:
                                arc13.append(edge)
                             AR[r][t]['Rand']=1
       for p,q in AR.edges:
            if (p,q) not in arc13:
                AR[p][q]['Rand']=0
               #ac=0             
       for p,q in AuAR.edges:
            if (p,q) in Important_nodes_random_gen.edges:
                       #ac=ac+1
                 AuAR[p][q]['Rand']=Important_nodes_random_gen[p][q]['Rand']
            elif (p,q) in arc13:
                 AuAR[p][q]['Rand']=AR[p][q]['Rand']
            else:
                 AuAR[p][q]['Rand']=0
       
       for r,t in S_ij.edges:
               #arcs_As=[]
         if AuAR[r][t]['Rand']==1:
             if A[r][t]['Tau']<=sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                  edge=(r,t)
                  if edge not in arcs_As:
                       arcs_As.append(edge)
       for r,t in unique_edges:
           if AuAR[r][t]['Rand']==1:
               edge2=(r,t)
               if edge2 not in arcs_As1:
                 arcs_As1.append(edge2)
           else:
               m1.addConstr(alpha1[r,t,s]==0) 
       for r,t in S_ij.edges:
           if AuAR[r][t]['Rand']==0:
               m1.addConstr(alpha1[r,t,s]==0)
           else:
               if A[r][t]['Tau']>sum(AuAR[r1][t1]['Rand'] for r1,t1 in S1[(r,t)]):
                   m1.addConstr(alpha1[r,t,s]==0)
       m1.addConstrs(alpha1[i,j,s]<=AuAR[i][j]['Rand'] * A[i][j]['Interdict'] for i,j in S_ij.edges)
       m1.addConstrs(alpha1[i,j,s]==AuAR[i][j]['Rand'] * A[i][j]['Interdict'] for i,j in unique_edges)
       for i, j in AR.edges:
               #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
           m1.addConstrs(phi1[i, j, s] >= alpha1[k,l,s] for k, l in R[(i,j)])
       m1.addConstrs(mu1[p,q,s]+alpha1[p,q,s]  - theta1[p,q,s] >= 0 for  p, q in A.edges)
       m1.addConstrs(delta1[p,q,s]-AuAR[p][q]['Rand'] * theta1 [p,q,s] >= 0 for p,q in AR.edges)
       m1.addConstrs(gp.quicksum(alpha1[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha1[i,j,s] for i,j in S_ij.edges)

    m1.addConstrs(v1[i,j,s]<= delta1[i,j,s] for i,j in AR.edges for s in S4)
    m1.addConstrs(v1[i,j,s]<= phi1[i,j,s] for i,j in AR.edges for s in S4)
    m1.addConstrs(v1[i,j,s]>= delta1[i,j,s] + phi1[i,j,s] - 1 for i,j in AR.edges for  s in S4)
    start_time_Replica=time.time()
    # Optimize the model
    m1.optimize()
    end_time_Replica=time.time() 
    elapsed_time_Replica1[l][iUB]=end_time_Replica - start_time_Replica
    Objective_Value_UB[l][iUB]= m1.objVal
  UpperBound[iUB]=np.mean(Objective_Value_UB[:,iUB])

  #a[l]= print('Obj: %obj', m1.objVal)

  end_time_UB = time.time()
  
ElapTimeUB_M1=pd.DataFrame(elapsed_time_Replica1)
file_path = 'elapTimeUB_Base1_AM1_Class2(n,10_M,5).xlsx'
#ElapTimeUB_M1.to_excel(file_path, index=False)
Ob_UB_M1=pd.DataFrame(Objective_Value_UB)
file_path = 'ObjUB_Base1_AM1_Class2(n,10_M,5)_check.xlsx'
#Ob_UB_M1.to_excel(file_path, index=False)
UB=np.min(UpperBound)
result=pd.DataFrame({'LB':LB,'UB': [UB], 'Gap':[UB-LB], 'Mean Time': [mean_time], 'Min Time':[min_time],'Max Time':[max_time]})
f_p='Result.xlsx'
result.to_excel(f_p, index=False)
