import argparse
import os
import re
import sys
import time
import profile

# Command line arguments
parser=argparse.ArgumentParser(description='Calculate the shortest path between all pairs of vertices in a graph')
parser.add_argument('--algorithm',default='a',
    help='Algorithm: Select the algorithm to run, default is all. (a)ll, (b)ellman-ford only or (f)loyd-warshall only')
parser.add_argument('-v','--verbose',action='store_true')
parser.add_argument('--profile',action='store_true')
parser.add_argument('filename',metavar='<filename>',help='Input file containing graph')

graphRE=re.compile("(\\d+)\\s(\\d+)")
edgeRE=re.compile("(\\d+)\\s(\\d+)\\s(-?\\d+)")

vertices=[]
edges=[]

def BellmanFord(G):
    pathPairs=[]
    inf=float("inf")
    w = []
    for i in edges:
        k = []
        for j in i:
            if j != float("inf"):
                k.append(int(j))
            elif j == float("inf"):
                k.append(inf)
        w.append(k)

    for z in range(len(vertices)):
        d=[]
        d=[inf]*len(vertices)
        d[z]=0
        for i in range(len(w)-1):
            for u in range(len(w)):
                for v in range(len(w[u])):
                    if d[v]>=d[u]+w[u][v]:
                         d[v] = d[u] + w[u][v]
        pathPairs.append(d)
    u=0
    v=0
    for u in range(len(w)):
        for v in range(len(w[u])):
            if d[v] > d[u] + w[u][v]:
                print("Graph has negative weights")


    return pathPairs

def FloydWarshall(G):
    pathPairs=[]
    d=[]
    inf = float("inf")
    w = []
    for i in edges:
        k = []
        for j in i:
            if j != float("inf"):
                k.append(int(j))
            elif j == float("inf"):
                k.append(inf)
        w.append(k)
    for m in range(len(vertices)):
        p = []
        for n in range(len(vertices)):
            p.append(inf)
        d.append(p)
    for i in range(len(d)):
        for j in range(len(d)):
            if i==j:
                d[i][j]=0
            elif w[i][j]!=inf:
                d[i][j]=w[i][j]
    i=0
    j=0
    k=0
    for i in range(len(vertices)):
        for j in range(len(vertices)):
            for k in range(len(vertices)):
                if d[j][k]>d[j][i]+d[i][k]:
                    d[j][k] = d[j][i] + d[i][k]
    pathPairs=d
    return pathPairs

def readFile(filename):
    global vertices
    global edges
    # File format:
    # <# vertices> <# edges>
    # <s> <t> <weight>
    # ...
    inFile=open(filename,'r')
    line1=inFile.readline()
    graphMatch=graphRE.match(line1)
    if not graphMatch:
        print(line1+" not properly formatted")
        quit(1)
    vertices=list(range(int(graphMatch.group(1))))
    edges=[]
    for i in range(len(vertices)):
        row=[]
        for j in range(len(vertices)):
            row.append(float("inf"))
        edges.append(row)
    for line in inFile.readlines():
        line = line.strip()
        edgeMatch=edgeRE.match(line)
        if edgeMatch:
            source=edgeMatch.group(1)
            sink=edgeMatch.group(2)
            if int(source) > len(vertices) or int(sink) > len(vertices):
                print("Attempting to insert an edge between "+source+" and "+sink+" in a graph with "+vertices+" vertices")
                quit(1)
            weight=edgeMatch.group(3)
            edges[int(source)-1][int(sink)-1]=weight
    G = (vertices,edges)
    return (vertices,edges)

def matrixEquality(a,b):
    if len(a) == 0 or len(b) == 0 or len(a) != len(b): return False
    if len(a[0]) != len(b[0]): return False
    for i,row in enumerate(a):
        for j,value in enumerate(b):
            if a[i][j] != b[i][j]:
                return False
    return True


def main(filename, algorithm):
    G=readFile(filename)
    pathPairs = []
    # G is a tuple containing a list of the vertices, and a list of the edges
    # in the format ((source,sink),weight)
    if algorithm == 'b' or algorithm == 'B':
        start_time = time.time()
        pathPairs = BellmanFord(G)
        print("Runtime: %s" % (time.time() - start_time))
    if algorithm == 'f' or algorithm == 'F':
        start_time = time.time()
        pathPairs = FloydWarshall(G)
        print("Runtime: %s" % (time.time() - start_time))
    if algorithm == 'a':
        print('running both') 
        pathPairsBellman = BellmanFord(G)
        pathPairsFloyd = FloydWarshall(G)
        pathPairs = pathPairsBellman
        if matrixEquality(pathPairsBellman,pathPairsFloyd):
            print('Floyd-Warshall and Bellman-Ford produced the same result')
    with open(os.path.splitext(filename)[0]+'_shortestPaths.txt','w') as f:
        for row in pathPairs:
            for weight in row:
                f.write(str(weight)+' ')
            f.write('\n')

if __name__ == '__main__':
    args=parser.parse_args()
    main(args.filename,args.algorithm)
