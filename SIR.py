import networkx as nx
import numpy as np 
from scipy import interpolate
import matplotlib.pyplot as plt
from collections import defaultdict
import time

def SIR(G,beta,gamma,times) :
    t = list(range(times))
    I_node = []
    count = times
    actual_statu = {node : 0 for node in G.nodes()}
    actual_statu[np.random.choice(G.nodes())] = 1
    while count > 0 :
        
        for u in G.nodes() :
            if actual_statu[u] == 0 :
                nb = [n for n in G.neighbors(u) if actual_statu[n] == 1]
                l = len(nb)
                p = 1 - (1 - beta) ** l
                if np.random.rand() < p:
                    actual_statu[u] = 1
            elif actual_statu[u] == 1:  
                if np.random.rand() < gamma :
                    actual_statu[u] = 2
        num = 0
        n = 0
        for i in G.nodes() :
            n += 1
            if actual_statu[i] == 1 :
                num += 1
        I_node.append(num / n)
        count -= 1
    return G,actual_statu,t,I_node


def R_node_in_any_rate() :
    s = time.time()
    x =[]
    t = range(500)
    y1 = defaultdict(list)
    y2 = defaultdict(list)
    z1 = []
    z2 = []
    w = list(np.arange(0,0.7,0.02))
    w.extend(list(np.arange(0.7,1,0.05)))
    
    num = 50
    while num > 0 : # run the SIR model 50 times independently
        for i in w : # for every the propogationg rate of disease
            G1,statu1,_,_ = SIR(nx.fast_gnp_random_graph(5000,0.0016),i,1,500) #ER_graph for 200 times
            G2,statu2,_,_ = SIR(nx.barabasi_albert_graph(5000,1),i,1,500) #BA_graph for 200 times
            sum = 0
            count = 0
            for j in G1.nodes() :
                sum += 1 if statu1[j] == 2 else 0 #statistic the number of R node in ER_graph
                count += 1
            y1[i].append(sum * 1.0 / count)
            sum = 0
            count = 0
            for j in G2.nodes() :
                sum += 1 if statu2[j] == 2 else 0 #statistic the number of R node in BA_graph
                count += 1
            y2[i].append(sum * 1.0 / count)
        num -= 1
    for i in w :
        x.append(i)
        sum = 0
        count = 0
        for j in y1[i] :
            sum += j
            count += 1
        z1.append(sum / count)
        sum = 0
        count = 0
        for j in y2[i] :
            sum += j
            count += 1
        z2.append(sum / count)
    e = time.time()
    print (e - s)
    print(x)
    print(z1)
    print(z2)
    f1 = interpolate.interp1d(x,z1,kind = 5)
    f2 = interpolate.interp1d(x,z2,kind = 5)
    z1new = f1(x)
    z2new = f2(x)
    plot1 = plt.plot(x,z1,'ko')
    plot2 = plt.plot(x,z1new,'b-')
    plot3 = plt.plot(x,z2,'ko')
    plot4 = plt.plot(x,z2new,'g-')
    plt.xlabel('lambda')
    plt.ylabel('r')
    plt.show()

def I_node_in_any_time() :
    G1,statu1,t1,I1_node = SIR(nx.fast_gnp_random_graph(5000,0.0016),0.2,1,200) #ER_graph with lambda = 0.2 for 200 times
    G2,statu2,t2,I2_node = SIR(nx.fast_gnp_random_graph(5000,0.0016),0.6,1,200) #ER_graph with lambda = 0.6 for 200 times
    x = t1
    y1 = I1_node
    y2 = I2_node
    print(x)
    print(y1)
    print(y2)
    f1 = interpolate.interp1d(x,y1,kind = 5)
    f2 = interpolate.interp1d(x,y2,kind = 5)
    y1new = f1(x)
    y2new = f2(x)
    plot1 = plt.plot(x,y1,'ko')  # propogation rate is 0.2, blue line
    plot2 = plt.plot(x,y1new,'b-')
    plot3 = plt.plot(x,y2,'ko')
    plot4 = plt.plot(x,y2new,'g-') # propogation rate is 0.6 ,green line
    plt.xlabel('t')
    plt.ylabel('I')
    plt.show()

if __name__ == '__main__' :
    # I_node_in_any_time()

    R_node_in_any_rate()
    
