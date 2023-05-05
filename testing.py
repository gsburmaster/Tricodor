import circuitgraph as cg
import pandas as pd
import re
import multiprocessing as mp
import pdb


def multithreadedNodes(node,inputArr): #[circuitIn,circuitIn2,file_name,nodes]
    temp = []
    print('node',node,inputArr[2])
    #print(node)
    
    fanInVals = getFanIn(node, inputArr[0])
    temp.append(fanInVals[0]) #append fanInL1
    temp.append(fanInVals[1]) #append fanInL2
    fanOutVals = getFanOut(node, inputArr[0])
    temp.append(fanOutVals[0]) #append fanOutL1
    temp.append(fanOutVals[1]) #append fanOutL2

    DFFinList = list(filter(isDFFin,inputArr[0].nodes()))
    DFFoutList = list(filter(isDFFout,inputArr[0].nodes()))
    DFFList = list(filter(isDFFatall,inputArr[0].nodes()))

    sortDFFs(DFFList)
    # print(cg.props.avg_sensitivity(cg.tx.strip_blackboxes(c),"G5"))
    # print('paths for output',list(c.paths("G11","DFF_1.D")))
    
    temp.append(closestDFFin(node,DFFinList,inputArr[0]))
    temp.append(closestDFFout(node,DFFoutList,inputArr[0]))
    temp.append(closestInput(node,inputArr[0],DFFList))
    temp.append(closestOutput(node,inputArr[0],DFFList))
    
    if (len(DFFList) <= 0):
        temp.append(cg.props.signal_probability(inputArr[0],node,False))
    else:
        if (node in inputArr[1].nodes()):
            temp.append(cg.props.signal_probability(inputArr[1],node,False))
        else:
            temp.append(-1)
    temp.append(9)
    return [temp,node]


def extractFeatures(circuitIn, file_name, blackboxIn):
    features=["FanIn L1", "FanIn L2", "FanOut L1", "FanOut L2","Closest DFF In","Closest DFF Out","Closest PI","Closest PO","Static Probability","(broken)Observability"]
    print('runnning with',file_name)
    nodes = circuitIn.topo_sort()
    
    filepath = "benchmarks/"
    if ("c" in file_name):
        filepath += "labeled_nets/"
    file = open(filepath + file_name + ".v","r")
    BBtext = file.read() # for some reason this is the way that this works
    file.close()
    NoBBtext = re.sub(r"dff (\w+)\(\.CK\((\w+)\),\.Q\((\w+)\),\.D\((\w+)\)\);",r"buf \1(\3,\4);",BBtext)
    NoBBtext = re.sub(r"module dff(.|\n)+endmodule(\n)+module","module",NoBBtext)
    # print(NoBBtext)
    circuitIn2 = cg.parsing.verilog.parse_verilog_netlist(NoBBtext,blackboxIn)

    inputArrForFunction = [circuitIn,circuitIn2,file_name]
    thingtoadd = []
    for node in nodes:
        thingtoadd.append(inputArrForFunction)
    # print(thingtoadd, "thing to add")
    nodeList = list(circuitIn.nodes())
    # print(list(nodeList),"nodes")
    nodeArgArr = []
    for node in nodeList:
        nodeArgArr.append((node,inputArrForFunction))
    
    if __name__ == '__main__':
        pool = mp.Pool(mp.cpu_count()-2)
        outputs = pool.starmap(multithreadedNodes,nodeArgArr)
        print(outputs)
        rows = [] 
        data = []
        for output in outputs:
            rows.append(output[1])
            data.append(output[0])
        df = pd.DataFrame(data,index=rows,columns=features)
        df.to_csv(path_or_buf='./parsed_nets/' + file_name + '.csv', sep=',') #put the data frame into a csv file, comma delim value
        pool.close()
        pool.join()
    
    # for node in nodes:
    #     temp = []
    #     print('node',node,file_name)
    #     #print(node)
        
    #     fanInVals = getFanIn(node, circuitIn)
    #     temp.append(fanInVals[0]) #append fanInL1
    #     temp.append(fanInVals[1]) #append fanInL2
    #     fanOutVals = getFanOut(node, circuitIn)
    #     temp.append(fanOutVals[0]) #append fanOutL1
    #     temp.append(fanOutVals[1]) #append fanOutL2

    #     DFFinList = list(filter(isDFFin,circuitIn.nodes()))
    #     DFFoutList = list(filter(isDFFout,circuitIn.nodes()))
    #     DFFList = list(filter(isDFFatall,circuitIn.nodes()))

    #     sortDFFs(DFFList)
    #     # print(cg.props.avg_sensitivity(cg.tx.strip_blackboxes(c),"G5"))
    #     # print('paths for output',list(c.paths("G11","DFF_1.D")))
        
    #     temp.append(closestDFFin(node,DFFinList,circuitIn))
    #     temp.append(closestDFFout(node,DFFoutList,circuitIn))
    #     temp.append(closestInput(node,circuitIn,DFFList))
    #     temp.append(closestOutput(node,circuitIn,DFFList))
        
    #     if (len(DFFList) <= 0):
    #         temp.append(cg.props.signal_probability(circuitIn,node,False))
    #     else:
    #         if (node in circuitIn2.nodes()):
    #             temp.append(cg.props.signal_probability(circuitIn2,node,False))
    #         else:
    #             temp.append(-1)
    #     temp.append(9)


    #     df[node] = temp

    #print(df)
    #print(df.T)
    # df = df.T
    # df.to_csv(path_or_buf='./parsed_nets/' + file_name + '.csv', sep=',') #put the data frame into a csv file, comma delim value

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

def closestOutput(node,circuit,dfflist):
    dffsortedlist = sortDFFs(dfflist)
    outputs = list(circuit.outputs())
    distance = -1
    outputthatwon = ""
    pathwin = []
    if (node in outputs):
        distance = 0
        outputthatwon = node
        pathwin = [node]
    if (node in dfflist):
        possibleoutPaths = []
        minInputPath = []
        for output in outputs:
            for othernode in circuit.nodes():
                if (len(list(circuit.paths(othernode,node))) > 0 and (len(list(circuit.paths(othernode,output))) > 0)):
                    possibleoutPaths.append(list(set(min(circuit.paths(othernode,node))).union( set(min(circuit.paths(othernode,output))))))
                if (len(minInputPath) > 0 and len(possibleoutPaths) > 0):
                    minLength =( len(min(minInputPath)) + len(min(possibleoutPaths)) ) -2
                    if ((minLength < distance) or distance == -1) and minLength > 0:
                        outputthatwon = output
                        distance = minLength
                        pathwin = list(set(min(minInputPath)).union(set(min(possibleoutPaths))))
    for output in outputs:
        paths = list(circuit.paths(node,output))
        if (len(paths) > 0):
            path = min(paths)
            if (distance == -1) or (len(path) -1 < distance):
                distance = len(path)
                outputthatwon = output
                pathwin= path
        dffFinalStack = []
        for dffArr in dffsortedlist:
            minInputPath = []
            possibleoutPaths = []
            for dffPort in dffArr: #now we have min path to dff
                if (len(list(circuit.paths(node,dffPort))) > 0) and ".D" in dffPort:
                    minInputPath.append(min(list(circuit.paths(node,dffPort))))
                if (".Q" in dffPort):
                    for othernode in circuit.nodes():
                        if (len(list(circuit.paths(dffPort,output))) > 0):
                            possibleoutPaths.append(min(list(circuit.paths(dffPort,output))))
            if (len(minInputPath) > 0 and len(possibleoutPaths) > 0):
                minLength =( len(min(minInputPath)) + len(min(possibleoutPaths)) ) -2
                if ((minLength < distance) or distance == -1) and minLength > 0:
                    outputthatwon = output
                    distance = minLength
                    pathwin = list(set(min(minInputPath)).union(set(min(possibleoutPaths))))
    # print("node:",node,"winning output: ",outputthatwon,"len: ", distance, "path: ", pathwin)
    return distance


def closestInput(node,circuit,dfflist):
    dffsortedlist = sortDFFs(dfflist)
    inputs = list(circuit.inputs())
    distance = -1
    inputthatwon = ""
    pathwin = []
    if (node in inputs):
        distance = 0
        inputthatwon = node
        pathwin = [node]
    if (node in dfflist):
        if (".CK" in node):
            distance = 1
            inputthatwon = 'CK'
            pathwin = [node,"CK"]
        else:
            distance = 2
            inputthatwon = "CK"
            pathwin = [node,"The clock port for a dff","CK"]
    for input in inputs:
        paths = list(circuit.paths(input,node))
        if (len(paths) > 0):
            path = min(paths)
            if (distance == -1) or (len(path) -1 < distance):
                distance = len(path)
                inputthatwon = input
                pathwin= path
        dffFinalStack = []
        for dffArr in dffsortedlist:
            minInputPath = []
            possibleoutPaths = []
            for dffPort in dffArr: #now we have min path to dff
                if (len(list(circuit.paths(input,dffPort))) > 0):
                    minInputPath.append(min(list(circuit.paths(input,dffPort))))
            for dffPort in dffArr:
                if(len(list(circuit.paths(node,dffPort))) > 0):
                    possibleoutPaths.append(min(list(circuit.paths(node,dffPort) ) ) )
                for othernode in circuit.nodes():
                    if ((len(list(circuit.paths(othernode,node))) > 0) and (len(list(circuit.paths(othernode,dffPort))) > 0)):
                        possibleoutPaths.append(list(set(min(circuit.paths(othernode,node))).union( set(min(circuit.paths(othernode,dffPort))))))
            if (len(minInputPath) > 0 and len(possibleoutPaths) > 0):
                minLength =( len(min(minInputPath)) + len(min(possibleoutPaths)) ) -2
                if ((minLength < distance) or distance == -1) and minLength > 0:
                    inputthatwon = input
                    distance = minLength
                    pathwin = list(set(min(minInputPath)).union(set(min(possibleoutPaths))))
    # print("node:",node,"winning Input: ",inputthatwon,"len: ", distance, "path: ", pathwin)
    return distance



dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
# v_file = input("Enter verilog file name (don't add .v extension): ")
path = 'benchmarks/'
# path += v_file

files = ["s27","s420","s641","s713","s1238","c482","c1980","c6288"]
# files = ["s27"]


def featureDriver(prepathName):
    dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
    path = 'benchmarks/'
    if ('c' in prepathName):
        path += "labeled_nets/"
    filepath = path + prepathName
    c = cg.from_file(filepath + '.v', blackboxes=dff)
    extractFeatures(c,prepathName,dff)

for file in files:
    featureDriver(file)





print("finished")
# try:
#     c = cg.from_file(path + '.v', blackboxes=dff)
#     extractFeatures(c,path)
# except:
#     print(path + ".v could not be opened")




# for node in c.nodes():
#     closestInput(node,c,DFFList)
#     closestOutput(node,c,DFFList)
    # extractFeatures(c, v_file)