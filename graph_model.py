import networkx as nx 
import matplotlib.pyplot as plt
import math
import numpy as np 
from collections import OrderedDict,defaultdict

from scipy import interpolate


def degree_distribution(avd) :
    x = []
    y = []
    d = dict()
    for key,val_list in avd.items() :
        sum = 0
        count = 0
        for val in val_list :
            sum += val
            count += 1
        d[key] = sum * 1.0 / count
    d = sorted(d.items(),key = lambda d:d[0])
    print(d)
    for i,j in d :
        x.append(i)
        y.append(j)
    f = interpolate.interp1d(x,y,kind = 5)
    ynew = f(x)
    plot1 = plt.plot(x,y,'ko')
    plot2 = plt.plot(x,ynew,'b-')
    plt.xlabel('k')
    plt.ylabel('Pk')
    plt.show()


def er_graph(n,p) :
    avd = defaultdict(list)
    num = 50
    while num > 0 :
        G = nx.empty_graph(n)
        degree = dict()
        v = 1
        w = -1
        lp = math.log(1.0 - p)
        while v < n :
            lr = math.log(1.0 - np.random.rand())
            k = int(lr/lp) + 1
            w += k
            while w >= v and v < n :
                w -= v
                v += 1
            if v < n :
                G.add_edge(v,w)
        for i in G.nodes() :
            nb = [n for n in G.neighbors(i)]
            l = len(nb)
            if degree.get(l) != None:
                degree[l] += 1
            else :
                degree[l] = 1
        for key,value in degree.items() :
            avd[key].append(value * (1.0 / (n - 1)))
        num -= 1
    degree_distribution(avd)
    return G


def ba_graph(n,m) :
    avd = defaultdict(list)
    num = 50
    while num > 0 :
        degree = dict()
        start = m
        G = nx.empty_graph(m)
        linked = list(range(m))
        exited = [] # already exited node in the graph,the number of same node means the degree of node.
        while start < n :
            cur = [start] * m
            G.add_edges_from(zip(cur,linked))
            exited.extend(cur)
            exited.extend(linked)
            update_linked = set()
            while len(update_linked) < m :
                update_linked.add(np.random.choice(exited))
            linked = list(update_linked)
            start += 1
        for i in G.nodes() :
            nb = [n for n in G.neighbors(i)]
            l = len(nb)
            if degree.get(l) != None :
                degree[l] += 1
            else :
                degree[l] = 1
        num -= 1
        for key,value in degree.items() :
            avd[math.log10(key)].append(math.log10(value * 1.0 / (n - 1)))

    #print(avd)
    degree_distribution(avd)
    return G

if __name__ == '__main__' :
    #G = er_graph(5000,0.0016)
    #G = ba_graph(100,1)
    num = 1000
    avd = defaultdict(list)
    
    while num > 0 :
        degree = dict()
        G = nx.barabasi_albert_graph(100,1)
        for i in G.nodes() :
            nb = [n for n in G.neighbors(i)]
            l = len(nb)
            if degree.get(l) != None :
                degree[l] += 1
            else :
                degree[l] = 1
        num -= 1
        for key,value in degree.items() :
            avd[math.log(key)].append(math.log(value * 1.0 / 100))
    degree_distribution(avd)
    
    