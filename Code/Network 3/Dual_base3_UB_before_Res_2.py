# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 01:34:38 2024

@author: fjanan
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
Final_interdiction={}

file_path_pickle ='z_values_base3_Heu_ModCap_2(n_40,m_5)_B_20.pkl' ## Interdiction plan with Budget 20

# Load the dictionary from the pickle file
with open(file_path_pickle, 'rb') as pickle_file:
    Interdiction_Values = pickle.load(pickle_file)

file_path_pickle ='z_values_base3_Heu_ModCap_2(n_40,m_5)_B_40.pkl' ## Interdiction plan with Budget 40

# Load the dictionary from the pickle file
with open(file_path_pickle, 'rb') as pickle_file:
    Interdiction_Values1 = pickle.load(pickle_file)

file_path_pickle ='z_values_base3_Heu_ModCap_2(n_40,m_5)_B_60.pkl' ## Interdiction plan with Budget 60

# Load the dictionary from the pickle file
with open(file_path_pickle, 'rb') as pickle_file:
    Interdiction_Values2 = pickle.load(pickle_file)


a_in=list(range(0,5))
for i in a_in:
    Final_interdiction[i]=Interdiction_Values[i]
    Final_interdiction[i+5]=Interdiction_Values1[i]
    Final_interdiction[i+10]=Interdiction_Values2[i]

data1= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='NetA')
data2= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='ResAR')
data3= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Comb')
data4= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Sij')
data5= pd.read_excel(r'D:\PhD Research\First_paper\200users_3_base\200users_3_base.xlsx', sheet_name='Sheet4')
A = nx.from_pandas_edgelist(data1, 'Source', 'Target', ['Tau','Resource','Capacity'], create_using=nx.DiGraph)
AR = nx.from_pandas_edgelist(data2, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
AuAR = nx.from_pandas_edgelist(data3, 'Source', 'Target', ['Capacity'], create_using=nx.DiGraph)
S_ij=nx.from_pandas_edgelist(data4, 'Source', 'Target', create_using=nx.DiGraph)
Important_nodes_random_gen= nx.from_pandas_edgelist(data5, 'Source', 'Target', create_using=nx.DiGraph)


n=2
n1=500
M=15
T=30
No_LB=list(range(0,1))
No_UB=list(range(0,M))
# Create a Gurobi model
num_nodes=261
num_res_arcs=131
rand_num=num_nodes+num_res_arcs
Total_arcs_A=1178
Com_arcs=num_res_arcs+Total_arcs_A
source=262
sink=263
node_expansion_start_node=264

a=list(range(0,num_nodes))
a1=list(range(0,100))
a2=list(range(0,num_res_arcs))
a3=list(range(0,num_nodes))
#a6=list(range(0,260))


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
# Creation set S_ij

list_of_arcs_S={}
a7=list(range(0,len(S_ij.edges)))
for l1 in a7:
    out_edges = list(A.out_edges(l1+200+node_expansion_start_node))
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

UpperBound=np.zeros((M,1))
S3=list(range(0,T))



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
for arc in arcs11:
      V[arc] = [] 
      
for m in list(range(0, len(arcs11))):
     V[(arcs11[m][0],arcs11[m][1])].extend(list_of_arcs_V[m]) 

S4=list(range(0,n1))  
#elapsed_time_Replica_UB=np.zeros((len(S3),1))
a={}
  
unique_edges = A.edges - S_ij.edges  
a4=list(range(0,n1))
elapsed_time_Replica = np.zeros((len(S3),len(No_UB)))
Objective_Value=np.zeros((len(S3),len(No_UB)))

# Generate a list of random integers
seed_value = 2
random.seed(seed_value)
random_integers_UB = [random.randint(1, 100) for _ in range(300)]
random_integers_UB1 = np.zeros((len(S3),len(No_UB)))
aR=0
for i in No_UB:
    for j in S3:
        random_integers_UB1[j][i]=random_integers_UB[aR+j]
    aR=aR+T

for iUB in No_UB:
  inderdiction = {}
  df3=pd.DataFrame(Final_interdiction[iUB])
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
    
    matrix_sequence = [np.random.choice([0,1], size=(num_nodes, len(S4))) for _ in range(1)]

     #   print(row)
    for scenarios in matrix_sequence:
        #print(scenarios)
        a[l]=scenarios
    # out of sample
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
    rand_a_b={}
    #selecting specific scenario and assigning a_{ij} and b_{ij} to the arcs of network AuAR and then adding the constraints
    for s in S4:  
       selected_column2 = a[l][:,s]
       rand_a_b[s] = selected_column2.tolist()
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
       #for i, j in AR.edges:
               #H[c][d]['sum']=gp.quicksum(G[p][q]['Capacity'] for p, q in arc_lists[(c, d)])    
          # m1.addConstrs(phi1[i, j, s] >= alpha1[k,l,s] for k, l in R[(i,j)])
       m1.addConstrs(mu1[p,q,s]+alpha1[p,q,s]  - theta1[p,q,s] >= 0 for  p, q in A.edges)
       #m1.addConstrs(delta1[p,q,s]-AuAR[p][q]['Rand'] * theta1 [p,q,s] >= 0 for p,q in AR.edges)
       m1.addConstrs(gp.quicksum(alpha1[k,l,s] for k,l in S1[(i,j)])>=A[i][j]['Tau'] * alpha1[i,j,s] for i,j in S_ij.edges)

    #m1.addConstrs(v1[i,j,s]<= delta1[i,j,s] for i,j in AR.edges for s in S4)
    #m1.addConstrs(v1[i,j,s]<= phi1[i,j,s] for i,j in AR.edges for s in S4)
   # m1.addConstrs(v1[i,j,s]>= delta1[i,j,s] + phi1[i,j,s] - 1 for i,j in AR.edges for  s in S4)
    start_time_Replica=time.time()
    # Optimize the model
    m1.optimize()
    end_time_Replica=time.time() 
    elapsed_time_Replica[l][iUB]=end_time_Replica - start_time_Replica
    Objective_Value[l][iUB]= m1.objVal
Obj=np.zeros((1,15))
Obj1=np.zeros((1,3))
Obj[0, :] = np.mean(Objective_Value, axis=0)
# Find the minimum values for the specified ranges
Obj1[0, 0] = np.min(Obj[0, :5])    # Minimum of columns 0 to 4
Obj1[0, 1] = np.min(Obj[0, 5:10])  # Minimum of columns 5 to 9
Obj1[0, 2] = np.min(Obj[0, 10:15])
ElapTimeUB_M1=pd.DataFrame(elapsed_time_Replica)
file_path = 'elapTimeUB_Base3_MF_SNIP_UR_beofore_restruc_2(B_20_40_60).xlsx'
#ElapTimeUB_M1.to_excel(file_path, index=False)
Ob_UB_M1=pd.DataFrame(Obj1)
file_path = 'ObjUB_Base3_MF_SNIP_UR_beofore_restruc_2(B_20_40_60).xlsx'
Ob_UB_M1.to_excel(file_path, index=False)

