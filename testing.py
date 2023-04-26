import circuitgraph as cg
import pandas as pd

dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/s27.v', blackboxes=dff)
#print(c.nodes())

def extractFeatures(cg):
    features=["f1", "f2", "f3", "f4","f5","f6","f7","f8","f9","f10"]
    nodes = cg.topo_sort()
    df = pd.DataFrame(index=features)

    for node in nodes:
        temp = []

        #extract feature
        temp.append(0) #append return value
        temp.append(1)
        #extract feature
        temp.append(2) #append return value ect..
        temp.append(3)
        temp.append(4)
        temp.append(5)
        temp.append(6)
        temp.append(7)
        temp.append(8)
        temp.append(9)

        df[node] = temp

    print(df)
    print(df.T)
    df = df.T
    df.to_csv(path_or_buf='test.xlsx', sep=',')

    return



# this takes one array of all dff ports and sorts into multiple arrays of each dff (so an array of DFF_1, an array of DFF_2, etc)
def sortDFFs(dfflistin):
    dfflist = [] + dfflistin
    outputList = []
    if (len(dfflist) == 0):
        return outputList
    while (len(dfflist) > 0):
        sortFilter = dfflist[0].replace('.D','')
        sortFilter = sortFilter.replace('.Q','')
        sortFilter = sortFilter.replace('.CK','')
        outputList+=[[k for k in dfflist if sortFilter in k]]
        dfflist = list(set(dfflist) - set(list(filter(lambda k: sortFilter in k,dfflist))))
    return outputList

def isDFFatall(input):
    if ".D" in input or '.Q' in input or '.CK' in input:
        return True
    return False
def isDFFin(input):
    if ".D" in input:
        # print(input)
        return True
    return False
def isDFFout(input):
    if ".Q" in input:
        return True
    return False
DFFinList = list(filter(isDFFin,c.nodes()))
DFFoutList = list(filter(isDFFout,c.nodes()))
DFFList = list(filter(isDFFatall,c.nodes()))
#https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/#
def closestDFFin(node,DFFinList,circuit):
    # print('about to print dfflist')
    distance = -1
    if ('.D' in node):
        distance = 0
    if ('.Q' in node):
        distance = 1
    if ('.CK' in node):
        distance = 1
    for dff in DFFinList:
        pathsbackward = list(circuit.paths(node,dff))
        pathsforward = list(circuit.paths(dff,node))
        fullpaths = pathsbackward + pathsforward
        for path in fullpaths:
            if ((len(path) < distance or distance == -1) and '.D' in dff): 
                distance = len(path) -1
            elif ((len(path) < distance or distance == -1) and '.Q' in dff):
                distance = len(path) 
            elif ((len(path) < distance or distance == -1) and '.CK' in dff):
                distance = len(path) 
            elif (distance == -1):
                if '.D' in dff:
                    distance = len(path)
                else:
                    distance = len(path) +1
        for othernode in circuit.nodes():
            if ((len(list(circuit.paths(othernode,node))) > 0) and (len(list(circuit.paths(othernode,dff))) > 0)):
                tmpdistance = len(min(list(circuit.paths(othernode,node)))) + len(min(list(circuit.paths(othernode,dff)))) -1
                if (tmpdistance < distance):
                    distance = tmpdistance -1
    # print(node,distance)
    return distance

def closestDFFout(node,DFFinList,circuit):
    # print('about to print dfflist')
    distance = -1
    if ('.Q' in node):
        distance = 0
    if ('.D' in node):
        distance = 1
    if ('.CK' in node):
        distance = 1
    for dff in DFFinList:
        pathsbackward = list(circuit.paths(node,dff))
        pathsforward = list(circuit.paths(dff,node))
        fullpaths = pathsbackward + pathsforward
        for path in fullpaths:
            if ((len(path) < distance or distance == -1) and '.Q' in dff): 
                distance = len(path) -1
            elif ((len(path) < distance or distance == -1) and '.D' in dff):
                distance = len(path) 
            elif ((len(path) < distance or distance == -1) and '.CK' in dff):
                distance = len(path) 
            elif (distance == -1):
                if '.Q' in dff:
                    distance = len(path)
                else:
                    distance = len(path) +1
        for othernode in circuit.nodes():
            if ((len(list(circuit.paths(othernode,node))) > 0) and (len(list(circuit.paths(othernode,dff))) > 0)):
                tmpdistance = len(min(list(circuit.paths(othernode,node)))) + len(min(list(circuit.paths(othernode,dff)))) -1
                if (tmpdistance < distance):
                    distance = tmpdistance -1
    # print(node,distance)
    return distance


def closestInput(node,circuit,dfflist):
    dffsortedlist = sortDFFs(dfflist)
    inputs = list(circuit.inputs())
    distance = -1
    for input in inputs:
        paths = list(circuit.paths(input,node))
        if (len(paths) > 0):
            path = min(paths)
            if (distance == -1) or (len(path) -1 < distance):
                distance = len(path)-1
        for dffArr in dffsortedlist:
            #need to check distance of each path- one dff could be shorter to, but longer after vs another that is medium on both.
            doubleLoopTmp = -1
            for dffPort in dffArr:
                fastestPath = min(list(circuit.paths(node,dffPort)))
                

            
sortDFFs(DFFList)
# print(cg.props.avg_sensitivity(cg.tx.strip_blackboxes(c),"G5"))
# print('paths for output',list(c.paths("G11","DFF_1.D")))
for node in c.nodes():
   closestDFFin(node,DFFList,c)
#    closestDFFout(node,DFFList,c)
#    closestInput(node,c,DFFList)

