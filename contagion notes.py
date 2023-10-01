#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#n = number of banks, which in the full model is taken to be 1000 - an average number of banks in a modern country.
# Each bank is a node.
# A bank has a capital balance = AIB - LIB - qAM - D
# To be liquid 1-phi(AIB - LIB) + qAM - D => 0
# Where phi is the proportion of AIB that have failed.
# Where:

# AIB = Assets interbank and is an incoming edge from another bank
# LIB = Liability interbank and is an outgoing edge to another bank (thus every AIB matches and LIB)
# q = Change in value of illiquid assets, largely due to prevailing economic circumstances.
# AM = Illiquid Assets, suchs as mortgages.
# D = Illiquid Debts, Consumer debts.
# Each is one link with a direction. Total AIB = Total LIB

# [Naturally one banks asset is anothers liability]

# Phi - Proportion of interbank assets that have failed.
# 
# *********************************************************************************************************************

# How to find the sum wieght of a node

# You can use the Graph.degree() method with the weight= keyword like this:

# In [1]: import networkx as nx

# In [2]: G = nx.Graph()

# In [3]: G.add_edge(1,2,weight=7)

# In [4]: G.add_edge(1,3,weight=42)

# In [5]: G.degree(weight='weight') Out[5]: {1: 49, 2: 7, 3: 42}

# In [6]: G.degree(weight='weight').items() Out[6]: [(1, 49), (2, 7), (3, 42)]


# standard imports
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# 3rd party imports


# custom imports

# *********************************************************************************************************************
# Stage 1 - Initialise the Network
# *********************************************************************************************************************

#Initialise grapgh G
G = nx.DiGraph()

# Set number of banks - in the Gai and Kapadia model n=1000 which is an average number of banks in a modern economy
banks = 10

#Set the value modifier for illiquid assets. 1 is neutral.
q = 1

# IB = Interbank Assets : Sum of wieght of in and out edges
# AM = Illiquid assets, such as mortgages
# D = Debt to creditors, ie. credit accounts. 
# Recall that these assets are double booked, thus function as asset or liability dependant on circumstances.

#Iterate through all banks.
#Create nodes labelled by n, with and AM and D of 0 [for later changes] [Not succesfully done yet]
#Give each bank five out edges to other randomly selected banks.
#Link_List is generated in each for banks loop to denoate banks that are not linked to the current bank.

# AIB - LIB = 20% of bank capital
# qAM - D = 80% of bank capital
# Banks are assumed to have 4% Capital Buffer
# Therefore 0.2(AIB-LIB)+0.8(qAM-D)= 104
# AIB and LIB are determined first, by generating the LIB for each bank.

# K = AIB - LIB + AM - D 
# If K=>0 the bank is solvent.
# K=4%


# 80(AM-D) - 20(AIB-LIB) = 104

# AIB-LIB =  Between 10 and -10 if AIB is lambda 5 and LIB is also Lambda 5.

# random.poisson(lam=1.0, size=None)

#Set edges for LIB. 
for bank in range(banks):
    G.add_node(bank, id=bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, bal=0, solv=1)
    
    link_list=[]
    for i in range(banks):
        link_list.append(i)
    
    for link in range(5):       #This model gives every bank 5 creditors. These will be adapted to poisson lamda 5.
                                #HOW TO WE MAKE THE ARRAY WORK IF nLIB is different every time?
                                #While each bank has 5 creditors, it may have more or less debtors.
                                #The total nodes in the graph will be 50.
        while True:
            
            creditor = random.randint(0,banks-1)    #The creditor is a randomly chosen other bank
            
            if creditor!=bank and creditor in link_list:  #Creditor cannot be a) the node bank or b) a current creditor
                break
        
        
        G.add_edge(bank,creditor,weight=2)        #A directed edge is added from the node bank to its creditor
        link_list.remove(creditor)        #Each time a creditor is identified they are removed from the link list
        
    
    
    AIB =  (len((G.in_edges(bank))))
    wAIB = G.in_degree(weight='weight')[bank]
    LIB =  (len((G.out_edges(bank)))) 
    wLIB = G.out_degree(weight='weight')[bank]
    
    IB = wAIB-wLIB
    #D is an normal distribution around 40 - to make up its approx 80% of the assets is a composit of D and AM
    D = int(random.gauss(mu=40.0, sigma=6.0))
    # To ensure equilibrium AM is determined to be the different between the deposits and the IB loans
    # If the bank has favourable IB loans than it has larger deposits to balance it out.
    AM = D-IB
    # Multiple by 1.08 to get an overall approximate 4% capital buffer
    # A is multiplied by 1.08 to approximately account for the 4% capital buffer, 
    # then we add one to ensure all banks aresolvent
    AM*=(1.08)
    AM=int(AM)+1

        
    #formula for solvency condition (solvent if balance >=0)
    balance=wAIB-wLIB+(q*AM)-D
    G.nodes[bank]['solv']=wAIB-wLIB+(q*AM)-D>0
    
    #G.add_node(bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, solv=1)
    G.nodes[bank]['aib']=AIB
    G.nodes[bank]['waib']=wAIB
    G.nodes[bank]['lib']=LIB   
    G.nodes[bank]['wlib']=wLIB
    G.nodes[bank]['ib']=IB
    G.nodes[bank]['am']=AM
    G.nodes[bank]['bal']=balance
    G.nodes[bank]['d']=D

    
#     print ("Bank: ",bank, "AIB: ",AIB,"WAIB: ",wAIB, "LIB: ", LIB, "WLIB: ", wLIB, "Balance: ",IB)
#     print("G.in_degree: ",G.in_degree[bank])
#     print("G.out_degree: ",G.out_degree[bank])    


# print("G.in_degree(weight='weight'): ",G.in_degree(weight='weight'))

# for bank in range(banks):
#     print(G.nodes[bank]['id'],G.in_degree(weight='weight')[bank])  #This returned a weight.

# # Print the nodes and edges:
# print()
# # print("Name:", G.nodes[name])
# print("Nodes:", G.nodes)
# print("Edges", G.edges)

#To check out its number of nodes or edges, 
# use the number_of_nodes() and number_of_edges() methods.
# print()
# print("Number of nodes = ", G.number_of_nodes())
# print("Number of edges = ", G.number_of_edges())        
# print()

     
      
#G.add_node(bank, id=bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, bal=0, solv=1)



for bank in range(banks):
    print ("Bank:",G.nodes[bank]['id'], "AIB:",G.nodes[bank]['aib'],"wAIB:",G.nodes[bank]['waib'], "LIB:", G.nodes[bank]['lib'],
           "wLIB:",G.nodes[bank]['wlib'], "IB:",G.nodes[bank]['ib'], "\tAM:", G.nodes[bank]['am'], "\tD:", G.nodes[bank]['d'], 
           "\tbalance:", G.nodes[bank]['bal'], "\tsolv:",G.nodes[bank]['solv'])


#Draw the graph

pos = nx.spring_layout(G)
nx.draw(G, pos,node_size=100)

labels = nx.get_node_attributes(G, "id")

nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color="white")

plt.show()


# *********************************************************************************************************************
# Stage 2 - Set bank 0 to fail due to extraneous cause
# *********************************************************************************************************************

# Set the bank that will fail

first_default = 0

# Set its out edges to 0, its am and d to 0.

for v, w in G.edges:
    if w==first_default:
        G.edges[v,w]["weight"]=0

AIB =  (len((G.in_edges(first_default))))
wAIB = G.in_degree(weight='weight')[first_default]
LIB =  (len((G.out_edges(first_default)))) 
wLIB = G.out_degree(weight='weight')[first_default]
AM = 0
D = 0

        
IB = wAIB-wLIB

G.nodes[first_default]['aib'] = AIB
G.nodes[first_default]['waib'] = wAIB
G.nodes[first_default]['lib'] = LIB
G.nodes[first_default]['wlib'] = wLIB
G.nodes[first_default]['ib'] = IB
G.nodes[first_default]['am']=AM
G.nodes[first_default]['d']=D

balance=wAIB-wLIB+(q*AM)-D
G.nodes[first_default]['bal']=balance
G.nodes[first_default]['solv']=wAIB-wLIB+(q*AM)-D>0

# Re-evaluate all the other banks.

for bank in range(banks):
    AIB =  (len((G.in_edges(bank))))
    wAIB = G.in_degree(weight='weight')[bank]
    LIB =  (len((G.out_edges(bank)))) 
    wLIB = G.out_degree(weight='weight')[bank]
    IB = wAIB-wLIB
    
    G.nodes[bank]['aib']=AIB
    G.nodes[bank]['waib']=wAIB
    G.nodes[bank]['lib']=LIB   
    G.nodes[bank]['wlib']=wLIB
    G.nodes[bank]['ib']=IB
    
    balance=wAIB-wLIB+(q*AM)-D
    G.nodes[bank]['bal']=balance
    G.nodes[bank]['solv']=wAIB-wLIB+(q*AM)-D>0
    
    print ("Bank:",G.nodes[bank]['id'], "AIB:",G.nodes[bank]['aib'],"wAIB:",G.nodes[bank]['waib'], "LIB:", G.nodes[bank]['lib'],
           "wLIB:",G.nodes[bank]['wlib'], "IB:",G.nodes[bank]['ib'], "\tAM:", G.nodes[bank]['am'], "\tD:", G.nodes[bank]['d'], 
           "\tbalance:", G.nodes[bank]['bal'], "\tsolv:",G.nodes[bank]['solv'])
        
    
    #Draw the graph

pos = nx.spring_layout(G)



color_map = []
color_edges =[]

for bank in range(banks):
    if G.nodes[bank]['solv']==False:
        color_map.append('red')
        color_edges.append('red')
    else:
        color_map.append('green')
        color_edges.append('green')



nx.draw(G, pos,node_size=100, edge_color=color_edges, node_color=color_map, with_labels=True)


labels = nx.get_node_attributes(G, "id")

nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color="white")

plt.show()

print (G.nodes[0])
print (G.degree[0])
print (G.out_degree[0])
print (G.in_degree[0])


# *********************************************************************************************************************
# Proof of concept - changing weight of nodes
# *********************************************************************************************************************

#Changing weights of nodes

for v, w in G.edges:
    G.edges[v,w]["weight"]=4
    print(v,w,G.edges[v,w])

#Change nodes with v to 0
for v, w in G.edges:
    if v==0:
        G.edges[v,w]["weight"]=2

for v, w in G.edges:
    print(v,w,G.edges[v,w])

# *********************************************************************************************************************
# Proof of concept - setting attributes, then accessing and changing them.
# *********************************************************************************************************************

#Initialise graph G
G = nx.DiGraph()


print (f"Creating {banks} banks with key qualities.")
for bank in range(banks):
    G.add_node(bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, solv=1)

print("*"*6)    
print("Change AIB of node 3 to 4 and then print")
G.nodes[3]['aib']=4
print (G.nodes[3]['aib'])

print()

print ('*'*6)

print ("Randomly generated aib's between 40 and sixty then print.")

for bank in range(banks):
    G.nodes[bank]['aib']= random.randint(40,60)
    print (bank, G.nodes[bank]['aib'])


# *********************************************************************************************************************
# Stage 3 - Iterate through banks, determining which new banks are insolvent, and update AIB until no further banks
# are insolvent
# *********************************************************************************************************************

# *********************************************************************************************************************
# Stage 4 - Have the entire programme iterate say 10,000 times and record the correlation between average number
# of interbank edges and total network failure rates.
# Other relationship should explored, but this simulates Gai and Kapadi's main finding.
# *********************************************************************************************************************
# TODO: you need to think about where each execution logs to, and then a separate process which inspects the logs
# and sumamarises/monitors a) progress and b) results - file writing, and or the python logger very helpful here.
# you may want to include in your other project
# TODO: multiprocessing.  You want to get your main command down to a single function which can all the config 
# passed to it then executes.
# you can then create a Dataframe of all the config for all the runs, and then use pool to split the dataframe by as 
# many processors on the box and have them all logging separatey, and then a separate process summarising.

# *********************************************************************************************************************
# Stage 5 - Create an interface that allows users to change key variables including:
# - interest rates (which will change relative values of assets)
# - required liquidity
# - balance between liquid and illiquid assets
# - "mean" for poisson distribution (although standard deviation should also be explored)
# - Allows user to 'test' circumstances that provide minal chance of financial catastrophe, ie. learning tool
# *********************************************************************************************************************
# TODO: you can try to create a user interface, but it's probably not the best way.
# instead consider making your main program a function which you can passing all the config for that run.
# then have a csv which has all the config for all your runs. 
# then just have pandas consume, split to multiprocesing, and call the function for you.
# if you had a run ID in the spreadsheet you can correlate your logs with htat, and put it back into spreadsheet.
# universities probably as used to reading a table of config as na interface.

# *********************************************************************************************************************
# Stage 6 - Getting clever.
# Give each bank a range of actions it can take each "turn" of a crisis, such as:
# - interbank loans
# - increasing liquidity
# - supporting struggling neighbours
# - foreclosing on debt.
# Allow the simulation to run until the banks have learned an 'optimal' strategy that results in either:
# - Their individual survival
# - The least damage to the network.
# Record results and publish!
# *********************************************************************************************************************