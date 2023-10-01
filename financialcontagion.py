#!/usr/bin/env python # pylint: disable=missing-module-docstring
# -*- coding: utf-8 -*-
# ******************************************************************************************************************120
#
# Financial Contagion Model
#
# Objectives:
#   Develop a network model of financial contagion that measures spread after exogenous shock causes one bank to fail.
#   Test how changing key factors including liquidity, ROI, interest rates, and government rescue thresholds
#   Enables "banks" to make tactical investment decisions during crisis and determine their optimal sultion.
# *********************************************************************************************************************
#
# Initial notes
# Gai and Kapadia,"Contagion in financial networks", Bank of England WP 383 (March 2010)
# Defined bank's capital balance as follows:
# k = AIB - LIB + qAM - D
# Such that to be liquid 1-phi(AIB - LIB) + qAM - D => 0
# Variable names in this model are matched to those in the Gai and Kapadia model, such that
#
# AIB = Assets interbank and is an incoming edge from another bank
# LIB = Liability interbank and is an outgoing edge to another bank (thus every AIB matches and LIB)
# q = Change in value of illiquid assets, largely due to prevailing economic circumstances.
# AM = Illiquid Assets, suchs as mortgages.
# D = Illiquid Debts, Consumer debts.
# Phi is the proportion of interbank assets that have failed
# L = Bank liquidity, cash assets that can immediately be drawn down.
#
# solv is a solvency boolean - if s=0 the bank is insolvent
## ie. 1-phi(AIB - LIB) + qAM - D <= 0
#
# We can expand this to include liquidity, a (typically) government mandated quantity of liquid assets
# That is expected to serve as
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
@click.option('-b', '--banks', type=int, required=False, default=10, help='Numer of banks')
@click.option('-l', '--links_per_bank', type=int, required=False, default=5, help='Number of links per bank')
@click.option('-a', '--am_factor', type=float, required=False, default=1.13, help='AM factor')
@click.option('-v', '--verbose', is_flag=True, required=False, default=False, help='Verbosity')
def main(img_output_dir: str, banks: int, links_per_bank: int, am_factor: float,
         verbose: bool) -> None:
    """Main Function"""
    # Number of banks
    # Value of illiquid assets
    # Liquidity
    # Lam (Lambda point of poisson distribution)

    # otherwise you will never know what is from this run or the next
    for file in os.listdir(img_output_dir):
        if file.endswith(".png"):
            file_uri = os.path.join(img_output_dir,file)
            print(f'Deleting: {file_uri}')
            os.remove(file_uri)

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
        print ("Where phi is the proportion of links banks that have failed")
        print ("AIB and LIB interbanks assets and liabilities")
        print ("AM is illiquid assets (eg. mortgages) multiplied by their current quality q,")
        print ("L is the banks liquid assets")
        print ("and D are consumer deposits. ")
        print ()
        print ("Gai and Kapadia's conclusion was that financial networks are stable but fragile")
        print ("- able to withstand exogenous")
        print ("systemic shocks provided there was sufficient interbank assets,")
        print ("but that even with a heavily interconnected")
        print ("network there would come a tipping point when the whole system collapses.")
        print ()
        print ("This simulation lets you test that theory while adjusting several key variables.")
        print ("[This functionality has not yet been added]")

    print ("STAGE 1: INITIALISE THE NETWORK")

    # *****************************************************************************************************************
    # Stage 1 - Initialise the Network
    # *****************************************************************************************************************

    # must have more banks than links
    assert banks > links_per_bank

    # Set value of illiquid assets q. 1 is neutral
    # Set liquidity requirement at 0.
    q = float(1)
    liq = float(0)
    lam = 5
    if verbose:
        print ("Asset quality (q) = ", q)
        print ("Liquidity requirement (liq) = ", liq)
        print ("Lambda for Poisson distribution (lam) = ", lam)

    # Initialise graph G
    G = nx.DiGraph()

    # Bank asset structure is (broadly) defined by G&K as follows:
    # AIB - LIB = 20% of bank capital
    # qAM - D = 80% of bank capital
    # Banks are assumed to have 4% Capital Buffer
    # Therefore 0.2(AIB-LIB)+0.8(qAM-D)= 104
    # AIB and LIB are determined first, by generating the LIB for each bank.

    # Generate nodes - one node per bank
    for bank in range(banks):
        G.add_node(bank, id=bank, aib=0, waib=0, lib=0, wlib=0, ib=0, am=0, d=0, bal=0, solv=1, liq=liq)

    # Set edges for LIB.
    # iterate through each bank - each bank is referenced by a raw ID 0-9
    # this is probably very confusing, recommend using i as an iterator, or bank as an object
    for bank in range(banks):

        # Poisson distribution currently producing bizarre results (not surprising)
        # replace with 5 links per bank until model works
        # rnd_links = numpy.random.poisson(lam)
        # rnd_links = int(rnd_links)
        # if rnd_links>banks: rnd_links=banks

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
        # If the bank has favourable IB loans than it has larger deposits to balance it out.
        AM = D-IB/2
        # Multiple by 1.04 to get an overall approximate 4% capital buffer
        # A is multiplied by 1.08 to approximately account for the 4% capital buffer,
        # then we add one to ensure all banks aresolvent
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

    print (f"\nSTAGE 2 - BANK {first_default} FAILS DUE TO EXOGENOUS FACTORS")
    # force the first bank bust with a big d_override
    G = process_insolvency(G,first_default,q,d_override=100)

    # *****************************************************************************************************************
    # Stage 3 - Iterate until contagion
    # *****************************************************************************************************************

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
    """Sets the bank on the passed index to have 0 weight in it's edges - replace this"""
        # Set its out edges to 0, its am and d to 0.

    # ok so list of tuples - (bank, debtor) - again just by ids.
    # so this is setting the weight of every relationship to the bank to 0
    # weight was previously hardcoded to 2
    # print_edges(G)
    for v, w in G.edges:
        if v == index:
            G.edges[v,w]["weight"]=0
            # print(f'{v},{w} = {G.edges[v,w]}')
    # print_edges(G)

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
