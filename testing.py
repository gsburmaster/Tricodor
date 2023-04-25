import circuitgraph as cg
import pdb
dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/s27.v', blackboxes=dff)
print(c.nodes())
def isDFFatall(input):
    if ".D" in input or '.Q' or '.CK' in input:
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
def closestDFFin(node,DFFinList,circuit,distance):
    # print('about to print dfflist')
    distance = -1
    if ('.D' in node):
        distance = 0
    if ('.Q' in node):
        distance = 1
    if ('.CK' in node):
        distance = 1
    for dff in DFFinList:
        if "G17" in node:
            True
            # print(dff,node,"ha")
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
    print(node,distance)
    return distance


# print(cg.props.avg_sensitivity(cg.tx.strip_blackboxes(c),"G5"))
# print('paths for output',list(c.paths("G11","DFF_1.D")))
for node in c.nodes():
   closestDFFin(node,DFFList,c,0)
#gonna do BFS to find nearest 

