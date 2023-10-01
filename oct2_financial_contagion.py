#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# Financial Contagion Model
#
# Objectives:
# Develop a network model of financial contagion that measures spread after exogenous shock causes one bank to fail.
# Base this model on the 2010 Bank of England Working Paper by Gai and Kapadia
# Allow users to explore this model by changing key variables
# Illustrate the operation of this changes (particularly asset value and liquidity) using Di Graph
# *********************************************************************************************************************
#
# Initial notes
# Gai and Kapadia,"Contagion in financial networks", Bank of England WP 383 (March 2010)
# Defined bank's capital balance as follows:
# k = AIB - LIB + qAM - D
# Such that to be liquid 1-phi(AIB - LIB) + qAM - D => 0
# Variable names in this model are as much as possible matched to those in the Gai and Kapadia model
#
# AIB = Assets interbank and is an incoming edge from another bank
# LIB = Liability interbank and is an outgoing edge to another bank (thus every AIB matches and LIB)
# q = Change in value of illiquid assets, largely due to prevailing economic circumstances.
# AM = Illiquid Assets, suchs as mortgages.
# D = Illiquid Debts, Consumer debts.
# Phi is the proportion of interbank assets that have failed
# liq = Bank liquidity, cash assets that can immediately be drawn down.
#
# solv is a solvency boolean - if s=0 the bank is insolvent
## ie. 1-phi(AIB - LIB) + qAM - D <= 0
#
# We expand the G&K model to include liquidity, a (typically) government mandated quantity of liquid assets
# that act as a buffer against failed interbank loans.
#
# Gai and Kapadia use "n" for the number of banks - we have replaced this with the variable "banks"
# Each bank is a node in a network, where each edge represents and interbank asset/liabilit (dependent on direction)
#
# One the network is randomly generated with nodes "banks", one is chosen to fail due to exogenous reasnons (eg fraud)
# All neighbouring banks are then subject to a risk of failure due to the increase in Phi (proportion of failed AIB)
# Should a neighbouring bank fail, then all its neighbours are subject to the same risk.
# This continues until the network stabalises of the entire financial system collapses.
# *********************************************************************************************************************

# standard imports
import random
import os

# 3rd party imports
import click
import matplotlib.pyplot as plt
import networkx as nx

# custom imports

@click.command()
@click.option('-o', '--img_output_dir', type=str, required=False, default='./static/img', help='Where to put images')
@click.option('-b', '--banks', type=int, required=False,prompt=True,default=10, help='Number of banks')
@click.option('--liq', type=float, required=False,prompt=True,default=0, help='Liquidity default 0; IB edges=2')
@click.option('-q', type=float, required=False,prompt=True,default=1.0, help='Illiquid ROI default is 1.0')
@click.option('-l', '--links_per_bank', type=int, required=False, default=5, help='Number of links per bank')
@click.option('-a', '--am_factor', type=float, required=False, default=1.13, help='AM factor')
@click.option('-v', '--verbose', is_flag=True, required=False, default=False, help='Verbosity')

def main(img_output_dir: str,
         liq: float,
         banks: int,
         q: float,
         links_per_bank: int,
         am_factor: float,
         verbose: bool) -> None:

    """Main Function"""
    # Indentify key variables
        # Number of banks
        # Value of illiquid assets (a multiplier of their approx 40% proportion of the banks assets)
        # Liquidity (as a set value, recalling an interbank loan is worth 2)


    # Cleaning up.
    # Delete previous similations plots, otherwise you will never know what is from this run or the next
    for file in os.listdir(img_output_dir):
        if file.endswith(".png"):
            file_uri = os.path.join(img_output_dir,file)
            print(f'Deleting: {file_uri}')
            os.remove(file_uri)

    # If programme is in verbose mode then an introduction to the code is printed.
    # Outputs tagged as verbose will also only print if you want the fully annotated version of the process.
    if verbose:
        print ("Welcome to the financial contagion simulator.")
        print ()
        print ("This programme simulates what will happen to a network of banks should one bank fail.")
        print ("The consequences of 'financial contagion' - where failure spreads from one bank to another")
        print ("were a central anxiety during the financial crisis of 2008 and a main justification")
        print ("for significant government intervention.")
        print ()
        print ("This simulation is based on the mathematical model developed by Gai and Kapadia")
        print ("Gai and Kapadia,'Contagion in financial networks', Bank of England WP 383 (March 2010)")
        print ("Who define a banks solvency condition as being 1-phi(AIB - LIB) + qAM + L - D <= 0")
        print ("    Where phi is the proportion of links banks that have failed")
        print ("    AIB and LIB interbanks assets and liabilities")
        print ("    AM is illiquid assets (eg. mortgages) multiplied by their current quality q,")
        print ("    L is the banks liquid assets")
        print ("    and D are consumer deposits. ")
        print ()
        print ("Gai and Kapadia's conclusion was that financial networks are stable but fragile")
        print ("- able to withstand exogenous systemic shocks provided there was sufficient interbank assets,")
        print ("However, even with a heavily interconnected network,")
        print ("there would come a tipping point when the whole system collapses.")
        print ()
        print ("This simulation lets you explore this model while adjusting several key variables.")
        print ("It's main objective is to help illustrate the complex concept of financial contagion.")

    print()

    print()
    print ("STAGE 1: INITIALISE THE NETWORK")

    # *****************************************************************************************************************
    # Stage 1 - Initialise the Network
    # *****************************************************************************************************************

    # must have more banks than links
    assert banks > links_per_bank

    # Set value of illiquid assets q. 1 is neutral
    # Set liquidity requirement at 0.

    if verbose:
        print ("Number of banks", banks)
        print ("Asset quality (q) = ", q)
        print ("Liquidity requirement (liq) = ", liq)


    # Initialise graph G
    G = nx.DiGraph()

    # Bank asset structure is (broadly) defined by G&K as follows:
    # |AIB - LIB| = 20% of bank capital
    # |qAM - D| = 80% of bank capital
    # Banks are assumed to have 4% Capital Buffer
    # Therefore 0.2(AIB-LIB)+0.8(qAM-D)= 104
    # AIB and LIB are determined first, by generating the LIB for each bank.

    # Generate nodes - one node per bank
    for bank in range(banks):
        G.add_node(bank, id=bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, bal=0, solv=1, liq=liq)

    # Set edges for LIB.
    for bank in range(banks):

        # Note that storing the variables inside the nodes is not the most efficient means of data handling.
        # It would be better to store them in dataframes then process the iterations
        # Using a DiGraph, however, allows the production of a visual illustration of contagion,
        # allowing users to better understand this difficult concept.

        # all possible debtors
        possible_debtors = list(range(banks))

        # debtor cannot be a) the node bank or b) a current debtor
        possible_debtors.remove(bank) # bank is used as the iterator


        link_counter = 0
        while link_counter < links_per_bank:

            # select a random debtor from possible debtors
            debtor = possible_debtors[random.randint(0,len(possible_debtors)-1)]
            #The debtor is a randomly chosen other bank

            # add edge to the bank index, to the debtor index, with a weight 2
            G.add_edge(bank,debtor,weight=2)
            # A directed edge is added from the node bank to its debtor.
            # Weight is 2 to maintain the average 20:80 structure of bank assets defined by Gai and Kapadia

            # remove the debtor so it can't be used again
            possible_debtors.remove(debtor)
            if verbose:
                print(f'Bank: {bank} added debtor: {debtor} total created links: {link_counter}')

            # increment counter
            link_counter = link_counter + 1

    # loop through again now we have edges
    # all possible debtors
        possible_debtors = list(range(banks))

        # debtor cannot be a) the node bank or b) a current debtor
        possible_debtors.remove(bank) # bank is used as the iterator

        link_counter = 0
        while link_counter < links_per_bank:

            # select a random debtor from possible debtors
            debtor = possible_debtors[random.randint(0,len(possible_debtors)-1)]
            #The debtor is a randomly chosen other bank

            # add edge to the bank index, to the debtor index, with a weight 2
            G.add_edge(bank,debtor,weight=2)
            # A directed edge is added from the node bank to its debtor.
            # Weight is 2 to maintain the average 20:80 structure of bank assets defined by Gai and Kapadia

            # remove the debtor so it can't be used again
            possible_debtors.remove(debtor)
            if verbose:
                print(f'Bank: {bank} added debtor: {debtor} total created links: {link_counter}')

            # increment counter
            link_counter = link_counter + 1

    # loop through again now we have edges
    for bank in range(banks):
        # So at this point this bank has 5 links added as edges
        AIB =  len(G.in_edges(bank)) # how many loans other banks owe i.e (x,you)
        wAIB = G.in_degree(weight='weight')[bank]
        LIB =  len(G.out_edges(bank))
        wLIB = G.out_degree(weight='weight')[bank]
        IB = wAIB-wLIB
        #D is an normal distribution around 40 - to make up its approx 80% of the assets is a composit of D and AM
        D = int(random.gauss(mu=40.0, sigma=6.0))
        # To ensure equilibrium AM is determined to be the different between the deposits and the IB loans
        # If the bank has favourable IB loans than it has larger deposits to compensate it out.
        # This is justifed by market clearence theorems as applied to banking.
        AM = D-IB/2
        # Multiple by the am_factor which allows for a required capital buffer. We are using 1.13 as an approximation
        # representative of state requirements, but users can change this value through the command line.
        AM=int(am_factor*D)

        # IB + AM - D + liq ~ 5
        if verbose:
            print(f'is it ~5 {IB+AM-D+liq}')

        G = set_bank_values(G, bank, AIB, wAIB, q, LIB, wLIB, IB, AM, D, liq)

    # print the output
    if verbose:
        print_banks("INITIAL BANK STATUS",G)
    print (f'Initial number of banks: {banks}')
    print (f'Number of banks insolvent: {count_banks_insolvent(G)}')

    # make the chart
    make_chart("./static/img/banknodes_00_start.png",G)

    # *****************************************************************************************************************
    # Stage 2 - First bank fails due to exogenous factors
    # *****************************************************************************************************************

    # Set the bank that will fail
    first_default = 0
    print()
    print (f"\nSTAGE 2 - BANK {first_default} FAILS DUE TO EXOGENOUS FACTORS")
    # force the first bank bust with a big d_override
    G = process_insolvency(G,first_default,q,d_override=100)

    # *****************************************************************************************************************
    # Stage 3 - Iterate until contagion ceases
    # *****************************************************************************************************************

    print()
    print("STAGE 3: Iterate until contagion ceases")
    print()

    previous_banks_insolvent = 0
    current_banks_insolvent = 1

    i = 1
    while current_banks_insolvent > previous_banks_insolvent:
        previous_banks_insolvent = current_banks_insolvent
        # Re-evaluate all the other banks.
        for bank in range(banks):
            G = evaluate_bank(G,bank,q,liq)
        current_banks_insolvent = count_banks_insolvent(G)
        if verbose:
            print_banks(f"{i:02} POST UPDATE BANK STATUS",G)
        set_banks_insolvent = []
        make_chart(os.path.join(img_output_dir,f'banknodes_{i:02}_post_bank_status.png'),G)
        for bank in range(banks):
            if G.nodes[bank]["solv"] is False:
                process_insolvency(G,bank,q,liq)
                set_banks_insolvent.append(bank)
        print(f'Round: {i:02} Number of banks insolvent: {count_banks_insolvent(G)}')
        print(f'Round: {i:02} set these banks insolvent: {set_banks_insolvent}')

        i = i + 1

def count_banks_insolvent(G: nx.DiGraph) -> bool:
    """Count number of insolvent banks"""
    insolvent_banks = 0
    for bank in range(len(G)):
        if G.nodes[bank]["solv"] is False:
            insolvent_banks = insolvent_banks + 1
    return insolvent_banks

def evaluate_bank(G: nx.DiGraph, index: int, q: float, liq: float = 0) -> nx.DiGraph:
    """Evaluate edges, degre weith, out edges, then set values and calculate balance and solvency"""
    AIB = len(G.in_edges(index))
    wAIB = G.in_degree(weight='weight')[index]
    LIB =  len(G.out_edges(index))
    wLIB = G.out_degree(weight='weight')[index]
    IB = wAIB-wLIB
    AM = G.nodes[index]['am']
    D = G.nodes[index]['d']
    G = set_bank_values(G,index,AIB,wAIB,q,LIB,wLIB,IB,AM,D,liq)
    return G

def set_bank_values(G: nx.DiGraph, index: int, AIB: int, wAIB: int, q: float,
                    LIB: int, wLIB: int, IB: int, AM: int, D: int, liq: float = 0) -> nx.DiGraph:
    """ Set the bank values based on passed parameters and calculate balance and solvency"""
    # set the things on the nodes again
    G.nodes[index]['aib'] = AIB
    G.nodes[index]['waib'] = wAIB
    G.nodes[index]['lib'] = LIB
    G.nodes[index]['wlib'] = wLIB
    G.nodes[index]['ib'] = IB
    G.nodes[index]['am']=AM
    G.nodes[index]['d']=D
    balance = calculate_balance(wAIB,wLIB,q,AM,D,liq)
    G.nodes[index]['bal']=balance
    solv = balance >= 0
    G.nodes[index]['solv']=solv
    return G

def calculate_balance(wAIB: int, wLIB: int, q: float, AM: int, D: int, liq: float = 0) -> float:
    """Calculates the balance for a bank"""
    return wAIB - wLIB + (q * AM) - D + liq

def process_insolvency(G: nx.DiGraph, index: int, q: float, liq: float = 0, d_override: int = 0) -> nx.DiGraph:
    """Sets the bank on the passed index to have 0 weight in it's edges"""

    # List of tuples - (bank, debtor) - just by ids.
    # This sets the weight of all the edges fron this node to 0
    # weight was previously hardcoded to 2
    for v, w in G.edges:
        if v == index:
            G.edges[v,w]["weight"]=0

    AIB = len(G.in_edges(index))
    wAIB = G.in_degree(weight='weight')[index]
    LIB = len(G.out_edges(index))
    wLIB = G.out_degree(weight='weight')[index]
    AM = 0
    if d_override > 0:
        D = d_override
    else:
        D = G.nodes[index]['d']
    IB = wAIB-wLIB
    G = set_bank_values(G,index,AIB,wAIB,q,LIB,wLIB,IB,AM,D,liq)

    return G

def print_banks(heading_text: str, G: nx.DiGraph):
    """Prints out the banks """

    print (f"\n{heading_text}")
    for bank in range(len(G)):
        print (
            "Bank:",G.nodes[bank]['id'],
            "AIB:",G.nodes[bank]['aib'],
            "wAIB:",G.nodes[bank]['waib'],
            "LIB:", G.nodes[bank]['lib'],
            "wLIB:",G.nodes[bank]['wlib'],
            "IB:",G.nodes[bank]['ib'],
            "\tAM:", G.nodes[bank]['am'],
            "\tD:", G.nodes[bank]['d'],
            "\t Liquidity", G.nodes[bank]['liq'],
            "\tbalance:", G.nodes[bank]['bal'],
            "\tsolv:",G.nodes[bank]['solv']
        )

def print_edges(G:nx.DiGraph):
    """Debugging number of edge"""
    print(f'Total edges: {len(G.edges)}')
    print(f'G has edges {G.edges}')


def make_chart(target_file_path: str, G: nx.DiGraph, node_size: int = 100, font_size: int = 10):
    """Makes a chart with colors saving it as the passed filename"""

    # clear the figure before drawing again.
    plt.clf()
    pos = nx.spring_layout(G)

    # color solvent banks green and insolvent banks red
    color_map = []
    color_edges =[]
    for bank in range(len(G)):
        if G.nodes[bank]['solv'] is False:
            color_map.append('red')
            color_edges.append('red')
        else:
            color_map.append('green')
            color_edges.append('green')

    nx.draw(G,
            pos,
            node_size=node_size,
            edge_color=color_edges,
            node_color=color_map,
            with_labels=True,
    )

    labels = nx.get_node_attributes(G, "id")

    nx.draw_networkx_labels(G, pos, labels=labels, font_size=font_size, font_color="white")

    plt.savefig(target_file_path)

if __name__ == '__main__':
    main()  # pylint: disable=no-value-for-parameter
