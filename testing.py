import circuitgraph as cg
import pandas as pd

dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/s27.v', blackboxes=dff)
#print(c.nodes())

def extractFeatures(cg):
    features=["FanIn L1", "FanIn L2", "FanOut L1", "FanOut L2","f5","f6","f7","f8","f9","f10"]
    nodes = cg.topo_sort()
    df = pd.DataFrame(index=features)

    for node in nodes:
        temp = []

        #print(node)

        fanInVals = getFanIn(node, cg)
        temp.append(fanInVals[0]) #append fanInL1
        temp.append(fanInVals[1]) #append fanInL2
        fanOutVals = getFanOut(node, cg)
        temp.append(fanOutVals[0]) #append fanOutL1
        temp.append(fanOutVals[1]) #append fanOutL2
        temp.append(4)
        temp.append(5)
        temp.append(6)
        temp.append(7)
        temp.append(8)
        temp.append(9)


        df[node] = temp

    #print(df)
    #print(df.T)
    df = df.T
    df.to_csv(path_or_buf='test.csv', sep=',') #put the data frame into a csv file, comma delim value

    return



#both fan out/in functions return a list, first value is the L1 fan in/out, second value is the L2 fan in/out
def getFanOut(node, cg):
    values = [] #get first and second level fanout, put into this values list
    outList = list(cg.fanout(node)) #fan functions give set of node, cast to list

    values.append(len(outList)) #put the length of the L1 list into values

    temp = 0
    for net in outList: #loop through list of L1 nodes, get there fan length, add to temp count
        temp = temp + len(list(cg.fanout(net)))

    values.append(temp) #put count of L2 into the list we are returning

    return values

def getFanIn(node, cg):
    values = [] #get first and second level fanin, put into this values list
    inList = list(cg.fanin(node))

    values.append(len(inList))

    temp = 0
    for net in inList:
        temp = temp + len(list(cg.fanin(net)))

    values.append(temp)

    return values





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
                tmpdistance = len(min(list(circuit.paths(othernode,node)))) + len(min(list(circuit.paths(othernode,dff)))) -2
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
                tmpdistance = len(min(list(circuit.paths(othernode,node)))) + len(min(list(circuit.paths(othernode,dff)))) -2
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
        dffFinalStack = []
        for dffArr in dffsortedlist:
            #need to check distance of each path- one dff could be shorter to, but longer after vs another that is medium on both.
            doubleLoopTmp = -1
            fastestPathToNode = [] #we need: path from input to DFF and then path from other DFF port to node we want (or from other node to node we want and to other DFF port)
            arrayofpaths = []
            for dffPort in dffArr:
                if (arrayofpaths == []):
                    fastestPathToDFF = min(list(circuit.paths(input,dffPort)))
                    arrayofpaths.append(fastestPathToDFF)
                else:
                    True



# print(cg.props.avg_sensitivity(cg.tx.strip_blackboxes(c),"G5"))
# print('paths for output',list(c.paths("G11","DFF_1.D")))
for node in c.nodes():
   closestDFFin(node,DFFList,c)
#    closestDFFout(node,DFFList,c)
#    closestInput(node,c,DFFList)

# extractFeatures(c)
