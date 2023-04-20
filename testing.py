import circuitgraph as cg
import pdb
dff = [cg.BlackBox("dff", ["CK", "D"], ["Q"])]
c = cg.from_file('benchmarks/s27.v', blackboxes=dff)
print(c.nodes())
def isDFFin(input):
    if ".D" in input:
        return True
    return False
def isDFFout(input):
    if ".Q" in input:
        return True
    return False
DFFinList = filter(isDFFin,c.nodes())
DFFoutList = filter(isDFFout,c.nodes())
#https://www.geeksforgeeks.org/breadth-first-search-or-bfs-for-a-graph/#
def closestDFFin(node, DFFinList,circuit,distance):
    print('about to print dfflist')
    for x in DFFinList:
        print(x)
    distance = -1
    for dff in DFFinList:
        paths = circuit.paths(node,dff)
        for path in paths:
            print(node,path)
            if len(path) < distance or distance == -1:
                distance = len(path)
        print(node,distance)
    return distance
        





for node in c.nodes():
   closestDFFin(node,DFFinList,c,0)
#gonna do BFS to find nearest 

