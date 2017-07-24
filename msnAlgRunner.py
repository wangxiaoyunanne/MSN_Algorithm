# msnAlgRunner.py
# -------
# The main file that runs the algorithm

#classes I wrote
import Graph
import util
#python classes
import math
import time
import Queue
import threading
import pp

###### EXTRA METHODS ######
def hashToGraph(hashNumber, xDim, yDim):
    edgeArray = []
    for x in range(xDim*(yDim+1) + yDim*(xDim+1)):
        edgeArray.append(0)
    l = len(str(hashNumber))
    for i in range(l):
        edgeArray[i] = hashNumber%10
        hashNumber = int(hashNumber/10)
    returnGraph = Graph.Graph(util.Counter(), util.Counter(), xDim, yDim)
    for x in range(xDim*(yDim+1)):
        if edgeArray[x] == 1:
            newVert1 = Graph.Vertex(0, x, xDim, yDim)
            newVert2 = Graph.Vertex(1, x, xDim, yDim)
            returnGraph = returnGraph.addEdge(newVert1, newVert2)
    y = xDim*(yDim+1)
    i = 0
    j = 0
    while y < xDim*(yDim+1) + yDim*(xDim+1):
        if edgeArray[y] == 1:
            newVert1 = Graph.Vertex(i, (1+j), xDim, yDim)
            newVert2 = Graph.Vertex(i, (0+j), xDim, yDim)
            returnGraph = returnGraph.addEdge(newVert1, newVert2)
        y+=1
        j+=1
        if j >= yDim:
            j = 0
            i += 1
            
    return returnGraph

## method to measure time of algorithm
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper


##### Threading to improve step 0 #######
class ThreadUnweightedGraphs(threading.Thread):

    def __init__(self, listOfXGraphs, higherDimExpandibleGraphs, outputSet, setOfEqGraphs, listOfExpandibleVert, expandibleXTuples, x, xDim, yDim):
        threading.Thread.__init__(self)
        self.queue = queue
        self.listOfXGraphs = listOfXGraphs
        self.outputSet = outputSet
        self.setOfEqGraphs = setOfEqGraphs
        self.expandingXTuples = listOfExpandibleVert
        self.expandibleXTuples = expandibleXTuples
        self.currentX = x
        self.higherDimExpandibleGraphs = higherDimExpandibleGraphs
        self.xDim = xDim
        self.yDim = yDim
        #self.out_queue = out_queue
        
    def run(self):
        outputSet = set()
        isNotInEq = True
        expandedGraph = set()
        setOfEqGraphs = self.setOfEqGraphs
        outputSet = self.outputSet
        higherDimExpandibleGraphs = util.Queue()
        #for x in self.listOfXGraphs:
        for x in self.listOfXGraphs:
            #expandingGraph = self.queue.get()
            expandingGraph = x
            if expandingGraph not in expandedGraph:
                expandedGraph.add(expandingGraph)
                expandedGraph.add(expandingGraph.reflectXGraph())
                for newXGraph in expandGraphX(expandingGraph, self.expandingXTuples, self.currentX-1):
                    biggestDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, self.xDim, self.yDim)
                    isNotInList = True
                    isNotInEq = True
                    if isXExpandible(newXGraph, self.expandibleXTuples):
                        higherDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, self.currentX+1, self.yDim)
                        higherDimExpandibleGraphs.push(higherDimXGraph)
                    else:
                        higherDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, self.xDim, self.yDim)
                    if higherDimXGraph in self.outputSet:
                            isNotInList = False
                    for newEqXGraph in newXGraph.generateEqClass():
                        biggestDimEqXGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, self.xDim, self.yDim)
                        if isXExpandible(newEqXGraph, self.expandibleXTuples):
                            higherDimXEqGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, self.currentX+1, self.yDim)
                            higherDimExpandibleGraphs.push(higherDimXEqGraph)
                        if biggestDimEqXGraph in setOfEqGraphs:
                            isNotInEq = False
                        else:
                            setOfEqGraphs.add(biggestDimEqXGraph)
                    if isNotInList and isNotInEq:
                        outputSet.add(biggestDimXGraph)
        self.outputSet = outputSet
        self.higherDimExpandibleGraphs = higherDimExpandibleGraphs
            #self.queue.task_done()
    
################# STEP ZERO METHOD ########################
# Step 0 of the MSN Alg: to enumerate all possible planar graphs

#helper methods to make expandible vertices
def makeYExpandibleVertices(x, y, xDim, yDim):
    listOfTup = set()
    if y == yDim:
        listOfTup = []
    elif y > yDim:
        listOfTup = []
    else:
        for i in range(x+1):
            listOfTup.add((i, y))
    return listOfTup

def makeXExpandibleVertices(x, y, xDim, yDim):
    listOfTup = set()
    if x == xDim:
        listOfTup = []
    elif x > xDim:
        listOfTup = []
    else:
        for i in range(y+1):
            listOfTup.add((x, i))
    return listOfTup

#helper methods to see if the graph contains one of the expandible vertices; if so, add back to queue
def isYExpandible(givenGraph, listOfExpandibleVert):
    for tuple in listOfExpandibleVert:
        if tuple in givenGraph.allVertices.keys():
            return True
    return False
    
def isXExpandible(givenGraph, listOfExpandibleVert):
    for tuple in listOfExpandibleVert:
        if tuple in givenGraph.allVertices.keys():
            return True
    return False

#helper method to expand graph in the y-direction
def expandGraphY(givenGraph, listOfExpandibleVert, y):
    newGraphSet = set()
    for vertex in listOfExpandibleVert:
        if y == vertex[1]:
            if vertex in givenGraph.allVertices.keys():
                newVert1 = Graph.Vertex(vertex[0], vertex[1]+1, givenGraph.graphXDim, givenGraph.graphYDim)
                newVert2 = Graph.Vertex((vertex[0]+1)%2, vertex[1]+1, givenGraph.graphXDim, givenGraph.graphYDim)
                newVert3 = Graph.Vertex((vertex[0]+1)%2, vertex[1], givenGraph.graphXDim, givenGraph.graphYDim)
                newGraph = givenGraph.addEdge(givenGraph.allVertices[vertex], newVert1)
                newGraphSet.add(newGraph)
                newGraph2 = newGraph.addEdge(newVert1, newVert2)
                newGraphSet.add(newGraph2)
                newGraph2 = newGraph2.addEdge(newVert2, newVert3)
                newGraphSet.add(newGraph2)
                if newVert3 in givenGraph.allVertices.values():
                    newGraph3 = newGraph.addEdge(newVert2, newVert3)
                    newGraphSet.add(newGraph3)
                    
    return newGraphSet

#helper method to divide an array of y coordinates to all possible configurations:
def divideArr(givenArray):
    result = []
    if len(givenArray) < 1:
        return []
    if len(givenArray) == 1:
        return givenArray
    else:
        while len(givenArray) != 0:
            i = 0
            x = givenArray.pop(0)
            newList = []
            result.append(x)
            for y in givenArray:
                i += 1
                result.append([x,y])
                newDiv = divideArr(givenArray[i:])
                if newDiv is not None:
                    for ls in newDiv:
                        result.append([x,y]+[ls])
        return result

#code from stackoverflow.com
def iter_flatten(iterable):
  it = iter(iterable)
  for e in it:
    if isinstance(e, (list, tuple)):
      for f in iter_flatten(e):
        yield f
    else:
      yield e

def expandGraphX(givenGraph, listOfExpandibleVert, x):
    expandibleGraphs = util.Stack()
    expandedGraphs = set()
    newGraphSet = set()
    keyVertexList = []
    leftVertices = []
    left = []
    rightVertices = dict()
    allGraphs = []
    for vertTup in listOfExpandibleVert:
        if vertTup in givenGraph.allVertices.keys():
            leftVertices.append(givenGraph.allVertices[vertTup])
            left.append(givenGraph.allVertices[vertTup])
    for i in range(givenGraph.graphYDim+1):
        rightVertex = Graph.Vertex(x+1, i, givenGraph.graphXDim, givenGraph.graphYDim)
        rightVertices[i] = rightVertex
        if isinstance(x, list):
            y = iter_flatten(x)
    for x in divideArr(left):
        if isinstance(x, Graph.Vertex):
            expandingGraph = givenGraph.addEdge(x, rightVertices[x.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
        else:
            expandingGraph = givenGraph
            for v in iter_flatten(x):
                expandingGraph = expandingGraph.addEdge(v, rightVertices[v.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
    while not expandibleGraphs.isEmpty():
        expandingGraph = expandibleGraphs.pop()
        if expandingGraph not in expandedGraphs:
            expandedGraphs.add(expandingGraph)
            #for vert in rightVertices.values():
            for vertex in expandingGraph.allVertices.keys():
                if vertex not in givenGraph.allVertices.keys():
                    vert = expandingGraph.allVertices[vertex]
                    for neighborVertex in expandingGraph.getLegalNeighborVertex(vert):
                        condition = False
                        if len(leftVertices) == givenGraph.graphYDim+1:
                            condition = neighborVertex.xCoord != x and neighborVertex.yCoord != vert.yCoord
                        else:
                            condition = neighborVertex not in givenGraph.allVertices.values()#(neighborVertex.xCoord != x and vert.xCoord != x) or neighborVertex.xCoord == x-1
                        if condition:
                            if not expandingGraph.hasEdge(vert, neighborVertex):
                                newGraph = expandingGraph.addEdge(vert, neighborVertex)
                                if not newGraph in newGraphSet:
                                    newGraphSet.add(newGraph)
                                    expandibleGraphs.push(newGraph)
                                    allGraphs.append(newGraph)
                                    
    return allGraphs

#main method to inductively enumerate all graphs that fit in xDim, yDim.
@print_timing
def enumerateAllGraphs(xDim, yDim):
    listOfAllGraphs = []
    setOfGraphs = set()
    setOfEqGraphs = set()
    expandedGraph = set()
    v0 = Graph.Vertex(0, 0, 1, 1)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), 1, 1)
    graph0.addVertex(v0)
    higherDimExpandibleGraphs = util.Queue()
    xDimExpandibleGraphs = util.Queue()
    toBeExpandedGraphs = util.Stack()
    toBeExpandedGraphs.push(graph0)
    x, y = 1, 1
    
    #WLOG, we can choose to expand in the y-direction first.
    while y <= yDim:
        expandibleTuple = makeYExpandibleVertices(x, y, xDim, yDim)
        expandingTuple = makeYExpandibleVertices(x, y-1, xDim, yDim)
        
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        if y == 1:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for vertex in expandingGraph.allVertices.values():
                        for neighborVertex in expandingGraph.getLegalNeighborVertex(vertex):
                            if not expandingGraph.hasEdge(vertex, neighborVertex):
                                isNotInList = True
                                isNotInEq = True
                                newGraph = expandingGraph.addEdge(vertex, neighborVertex)
                                biggestDimGraph2 = Graph.Graph(newGraph.allVertices, newGraph.allEdges, xDim, yDim)
                                if isYExpandible(newGraph, expandibleTuple):
                                    higherDimGraph2 = Graph.Graph(newGraph.allVertices, newGraph.allEdges, x, y+1)
                                else:
                                    higherDimGraph2 = newGraph
                                if isXExpandible(newGraph, expandibleXTuples):
                                    xHigherDimGraph = Graph.Graph(newGraph.allVertices, newGraph.allEdges, x+1, yDim)
                                    xDimExpandibleGraphs.push(xHigherDimGraph)
                                if biggestDimGraph2 in setOfGraphs:
                                    isNotInList = False
                                for eqGraph in newGraph.generateEqClass():
                                    biggestDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, xDim, yDim)
                                    if isYExpandible(eqGraph, expandibleTuple):
                                        higherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, y+1)
                                        higherDimExpandibleGraphs.push(higherDimGraph)
                                    else:
                                        higherDimGraph =  Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, yDim)
                                    if isXExpandible(eqGraph, expandibleXTuples):
                                        xHigherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x+1, yDim)
                                        xDimExpandibleGraphs.push(xHigherDimGraph)
                                    if biggestDimGraph in setOfEqGraphs:
                                        isNotInEq = False
                                    if biggestDimGraph not in setOfEqGraphs:
                                        toBeExpandedGraphs.push(eqGraph)
                                        setOfEqGraphs.add(biggestDimGraph)
                                if isNotInList and isNotInEq:
                                    setOfGraphs.add(biggestDimGraph2)
                                    listOfAllGraphs.append(biggestDimGraph2)
        else:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for newGraphExpanded in expandGraphY(expandingGraph, expandingTuple, y-1):
                        biggestDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, xDim, yDim)
                        isNotInList = True
                        isNotInEq = True
                        if isYExpandible(newGraphExpanded, expandibleTuple):
                            higherDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x, y+1)
                            higherDimExpandibleGraphs.push(higherDimGraph2)
                        else:
                            higherDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x, yDim)
                        if isXExpandible(newGraphExpanded, expandibleXTuples):
                            xHigherDimGraph = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x+1, yDim)
                            xDimExpandibleGraphs.push(xHigherDimGraph)
                        if higherDimGraph2 in setOfGraphs:
                            isNotInList = False
                        for newEqGraph in newGraphExpanded.generateEqClass():
                            biggestDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, xDim, yDim)
                            if isYExpandible(newEqGraph, expandibleTuple):
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, y+1)
                                higherDimExpandibleGraphs.push(higherDimGraph)
                            else:
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, yDim)
                            if isXExpandible(newEqGraph, expandibleXTuples):
                                xHigherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x+1, yDim)
                                xDimExpandibleGraphs.push(xHigherDimGraph)
                            if biggestDimGraph in setOfEqGraphs:
                                isNotInEq = False
                            if biggestDimGraph not in setOfEqGraphs:
                                setOfEqGraphs.add(biggestDimGraph)
                        if isNotInList and isNotInEq:
                            setOfGraphs.add(biggestDimGraph2)
                            listOfAllGraphs.append(biggestDimGraph2)
                                
        y += 1
        toBeExpandedGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set() 
    x+=1
    
    #Now expand in the x-direction
    while x <= xDim:
        while not xDimExpandibleGraphs.isEmpty():
            expandingGraph = xDimExpandibleGraphs.pop()
            if expandingGraph not in expandedGraph:
                expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
                expandingXTuples = makeXExpandibleVertices(x-1, yDim, xDim, yDim)
                expandedGraph.add(expandingGraph)
                expandedGraph.add(expandingGraph.reflectXGraph())
                for newXGraph in expandGraphX(expandingGraph, expandingXTuples, x-1):
                    biggestDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, xDim, yDim)
                    isNotInList = True
                    isNotInEq = True
                    if isXExpandible(newXGraph, expandibleXTuples):
                        higherDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, x+1, yDim)
                        higherDimExpandibleGraphs.push(higherDimXGraph)
                    else:
                        higherDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, xDim, yDim)
                    if higherDimXGraph in setOfGraphs:
                            isNotInList = False
                    for newEqXGraph in newXGraph.generateEqClass():
                        biggestDimEqXGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, xDim, yDim)
                        if isXExpandible(newEqXGraph, expandibleXTuples):
                            higherDimXEqGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, x+1, yDim)
                            higherDimExpandibleGraphs.push(higherDimXEqGraph)
                        if biggestDimEqXGraph in setOfEqGraphs:
                            isNotInEq = False
                        else:
                            setOfEqGraphs.add(biggestDimEqXGraph)
                    if isNotInList and isNotInEq:
                        setOfGraphs.add(biggestDimXGraph)
                        listOfAllGraphs.append(biggestDimXGraph)
        x += 1
        xDimExpandibleGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set() 
    return setOfGraphs

@print_timing
def parallelEnumerateAllGraphs(xDim, yDim):
    #initialize local variable sets
    filter = set()
    setOfExpandibleGraphs = set()
    setOfGraphs = set()
    expandedGraph = set()
    
    #setup
    v0 = Graph.Vertex(0, 0, 1, 1)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), 1, 1)
    graph0.addVertex(v0)
    higherDimExpandibleGraphs = util.Queue()
    xDimExpandibleGraphs = util.Queue()
    toBeExpandedGraphs = util.Stack()
    toBeExpandedGraphs.push(graph0)
    x, y = 1, 1
    
    #WLOG, we can choose to expand in the y-direction first.
    while y <= yDim:
        expandibleTuple = makeYExpandibleVertices(x, y, xDim, yDim)
        expandingTuple = makeYExpandibleVertices(x, y-1, xDim, yDim)
        
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        if y == 1:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for vertex in expandingGraph.allVertices.values():
                        for neighborVertex in expandingGraph.getLegalNeighborVertex(vertex):
                            if not expandingGraph.hasEdge(vertex, neighborVertex):
                                isNotInList = True
                                isNotInEq = True
                                newGraph = expandingGraph.addEdge(vertex, neighborVertex)
                                biggestDimGraph2 = Graph.Graph(newGraph.allVertices, newGraph.allEdges, xDim, yDim)
                                if biggestDimGraph2 in filter:
                                    continue
                                setOfGraphs.add(biggestDimGraph2)
                                for eqGraph in newGraph.generateEqClass():
                                    biggestDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, xDim, yDim)
                                    if isYExpandible(eqGraph, expandibleTuple):
                                        higherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, y+1)
                                        higherDimExpandibleGraphs.push(higherDimGraph)
                                    if isXExpandible(eqGraph, expandibleXTuples):
                                        xHigherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x+1, yDim)
                                        setOfExpandibleGraphs.add(xHigherDimGraph)
                                    toBeExpandedGraphs.push(eqGraph)
                                for eqBigGraph in biggestDimGraph2.generateEqClass():
                                    filter.add(eqBigGraph)
        else:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for newGraphExpanded in expandGraphY(expandingGraph, expandingTuple, y-1):
                        biggestDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, xDim, yDim)
                        isNotInList = True
                        isNotInEq = True
                        if biggestDimGraph2 in filter:
                            continue
                        setOfGraphs.add(biggestDimGraph2)
                        for newEqGraph in newGraphExpanded.generateEqClass():
                            biggestDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, xDim, yDim)
                            if isYExpandible(newEqGraph, expandibleTuple):
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, y+1)
                                higherDimExpandibleGraphs.push(higherDimGraph)
                            else:
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, yDim)
                            if isXExpandible(newEqGraph, expandibleXTuples):
                                xHigherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x+1, yDim)
                                setOfExpandibleGraphs.add(xHigherDimGraph)
                        for eqBigGraph in biggestDimGraph2.generateEqClass():
                            filter.add(eqBigGraph)
                                
        y += 1
        toBeExpandedGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set() 
    x+=1
    #Now expand in the x-direction
    while x <= xDim:
        unweighted = []
        ppservers = ()
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        expandingXTuples = makeXExpandibleVertices(x-1, yDim, xDim, yDim)
        job_server = pp.Server(ppservers=ppservers)
        jobs = [(expandingGraph, job_server.submit(expandGraphX, (expandingGraph, expandingXTuples, x-1), (divideArr, iter_flatten,), ("Graph", "util", ))) for expandingGraph in setOfExpandibleGraphs]
        setOfExpandibleGraphs = set()
        for expandingGraph, job in jobs:
            unweighted.extend(job())
        for newXGraph in unweighted:
            biggestDimXGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, xDim, yDim)
            if biggestDimXGraph in filter:
                continue
            setOfGraphs.add(biggestDimXGraph)
            for newEqXGraph in newXGraph.generateEqClass():
                biggestDimEqXGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, xDim, yDim)
                if isXExpandible(newEqXGraph, expandibleXTuples):
                    higherDimXEqGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, x+1, yDim)
                    higherDimExpandibleGraphs.push(higherDimXEqGraph)
                    setOfExpandibleGraphs.add(higherDimXEqGraph)
            for eqBigGraph in biggestDimXGraph.generateEqClass():
                filter.add(eqBigGraph)
                
        x += 1
        xDimExpandibleGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set()
        
    return setOfGraphs
    
    
###################### STEP ONE METHODS #########################

# helper method for Step 1 in creating possible a, b, and c to add in the weights
def makeChart(n, xDim, yDim):
    c_max = int(math.floor(n/3))
    c_min = 4
    c_value = 4
    c_range = [4]
    while c_value is not c_max:
        c_value += 2
        c_range.append(c_value)
    a_min = 4
    listOfTripletABC = []
    a_value = a_min
    b_value = n - a_min - c_min
    for c in c_range:
        a_value = c
        b_value = n - a_value - c
        while b_value >= a_value:
            listOfTripletABC.append([a_value, b_value, c])
            a_value += 2
            b_value = n - a_value - c
    return listOfTripletABC

# helper method for Step 1 in creating partition for given a or c to add to each edge
def partitionAll(n):
    if n == 0:
        yield []
        return
    for p in partitionAll(n-1):
        yield[1] + p
        if p and (len(p) < 2 or p[1] > p[0]):
            yield[p[0]+1]+p[1:]

def partition(number, split_number):
    partitionWithSplitNum = []
    allPartition = partitionAll(number)
    for p in allPartition:
        if len(p) == split_number:
            partitionWithSplitNum.append(tuple(p))
    return partitionWithSplitNum

# helper method for Step 1 that returns all permutations of a given list:
    
def permutate(permutableSequence):
    if len(permutableSequence) == 1:
        return [permutableSequence]
    else:
        newAllPermutations = []
        for item in permutableSequence:
            newSequence = []
            for item1 in permutableSequence:
                newSequence.append(item1)
            newSequence.remove(item)
            for subseq in permutate(newSequence):
                newSeq = [item]+subseq
                if newSeq not in newAllPermutations:
                    newAllPermutations.append([item]+subseq)
        return newAllPermutations
    
# Step 1 of MSN Algorithm: enumerating all legal weighted graphs given a specific graph
def enumerateAllWeightedGraphs(givenGraph, xDim, yDim, slabNum, givenChart):
    #initialize the sets
    filter = set()
    equivalentGraphSet = set()
    weightedGraphSet = set()
    
    #start with all possible triplets
    for possible_triplet in givenChart:
        possibleAWeights = partition(possible_triplet[0], givenGraph.unweighted_a)
        possibleCWeights = partition(possible_triplet[1], givenGraph.unweighted_c)  
        for a_value in possibleAWeights:
            permutationOfAValues = permutate(a_value)
            for c_value in possibleCWeights:
                permutationOfCValues = permutate(c_value)
                for permute_a in permutationOfAValues:
                    for permute_c in permutationOfCValues:
                        newAllEdges = util.Counter()
                        i = 0
                        j = 0
                        for edge in givenGraph.allEdges:
                            graphEdge = givenGraph.allEdges[edge]
                            if graphEdge.orientation == '|':
                                newEdge = Graph.Edge(graphEdge.v1, graphEdge.v2, permute_a[i], graphEdge.graphXDim, graphEdge.graphYDim)
                                i += 1
                            elif graphEdge.orientation == '_':
                                newEdge = Graph.Edge(graphEdge.v1, graphEdge.v2, permute_c[j], graphEdge.graphXDim, graphEdge.graphYDim)
                                j += 1
                            newAllEdges[newEdge.getCoordinate()] = newEdge
                        newGraph = Graph.Graph(givenGraph.allVertices, newAllEdges, givenGraph.graphXDim, givenGraph.graphYDim)
                        valid = True
                        for edge in newGraph.allEdges.values():
                            if edge.weight > slabNum+1:
                                valid = False
                                break
                        legal = newGraph.isLegalWeightedGraph() and (not newGraph.isReducible()) and valid
                        if newGraph not in filter and legal:
                            weightedGraphSet.add(newGraph)
                            for eqGraph in newGraph.generateEqClass():
                                filter.add(eqGraph)
    
    #for graph in listOfWeightedGraphs:
    #    graph.toPrint()
    
    return weightedGraphSet

###################### STEP TWO METHODS #########################

#helper method to create alternating level edges

# Step 2 of MSN Algorithm: enumerate all knot diagram given weighted graphs
def enumerateAllKnotDiagrams(givenWeightedGraph, xDim, yDim, slabNum):
    newAllVertices = givenWeightedGraph.allVertices
    for vertex in givenWeightedGraph.allVertices.values():
        if givenWeightedGraph.getValence(vertex) > 4:
            return []
            
    listOfPossibleKnotDiagrams = []
    newKnotDiagram = Graph.KnotDiagram(givenWeightedGraph.allVertices, util.Counter(), xDim, yDim)
    #for each weightedEdge, convert into DiagramEdge
    allEdgeVals = givenWeightedGraph.allEdges.values()
    weight2Edges = []
    #make new datastructure for now: probably replacing allVertices with this for all graphs
    for edge in allEdgeVals:
        if edge.weight == 2:
            weight2Edges.append(edge)
            
    ##### start the enumeration #######

    #take care of weight 2 edges
    listOfPossibleKnotDiagrams.append(newKnotDiagram)
    while len(weight2Edges) != 0:
        weight2Edge = weight2Edges.pop()
        allEdgeVals.remove(weight2Edge)
        newList1 = []
        for knotDiag in listOfPossibleKnotDiagrams:
            #make two DiagramEdges and insert them into the already made knotDiagrams
            diagramEdge1 = Graph.DiagramEdge(weight2Edge.v1, weight2Edge.v2, xDim, yDim , 0)
            diagramEdge2 = Graph.DiagramEdge(weight2Edge.v1, weight2Edge.v2, xDim, yDim , 1)
            newKnotDiag = knotDiag.addEdge(diagramEdge1)
            newKnotDiag = newKnotDiag.addEdge(diagramEdge2)
            newList1.append(newKnotDiag) 
        listOfPossibleKnotDiagrams = newList1
        #take care of all the edges sharing its two vertices, for better efficiency.
        connectedEdges = (givenWeightedGraph.vertexEdgeMatrix[weight2Edge.v1.getCoordinate()], givenWeightedGraph.vertexEdgeMatrix[weight2Edge.v2.getCoordinate()])
        for connectedEdgeList in connectedEdges:
            for edge in weight2Edges:
                try:
                    connectedEdgeList.remove(edge)
                except ValueError:
                    continue
        
            if len(connectedEdgeList) == 2:
                newList2=[]
                for x in range(2):
                    diagramEdge1 = Graph.DiagramEdge(connectedEdgeList[0].v1, connectedEdgeList[0].v2, xDim, yDim , x)
                    diagramEdge2 = Graph.DiagramEdge(connectedEdgeList[1].v1, connectedEdgeList[1].v2, xDim, yDim , (x+1)%2)
                    for alreadyMadeKnotDiag in listOfPossibleKnotDiagrams:
                        newKnotDiag1 = alreadyMadeKnotDiag.addEdge(diagramEdge1).addEdge(diagramEdge2)
                        newList2.append(newKnotDiag1)
                listOfPossibleKnotDiagrams = newList2
                allEdgeVals.remove(connectedEdgeList[0])
                allEdgeVals.remove(connectedEdgeList[1])
                #"""
        
    #make two DiagramEdges and insert one or the other, making an additional new knotDiagram
    while len(allEdgeVals) != 0:
        newList=[]
        newEdge = allEdgeVals.pop()
        diagramEdge1 = Graph.DiagramEdge(newEdge.v1, newEdge.v2, xDim, yDim , 0)
        diagramEdge2 = Graph.DiagramEdge(newEdge.v1, newEdge.v2, xDim, yDim , 1)
        for alreadyMadeKnotDiag in listOfPossibleKnotDiagrams:
            newKnotDiag1 = alreadyMadeKnotDiag.addEdge(diagramEdge1)
            newKnotDiag2 = alreadyMadeKnotDiag.addEdge(diagramEdge2)
            newList.append(newKnotDiag1)
            newList.append(newKnotDiag2)
        listOfPossibleKnotDiagrams = newList
    
    return listOfPossibleKnotDiagrams

###################### STEP THREE METHODS #########################
# Step 3 of MSN Algorithm: realize all valid Knot Diagrams into actual Knots

def realizeAllKnots(givenKnotDiagram, n):
    path = givenKnotDiagram.getPath()
    if path!=0:
        return path


###################### MAIN RUNNER #########################
@print_timing
def runAlgorithm(n, xDim, yDim):
    import __main__
    
    print "Running for n = %u, for %u by %u" % (n, xDim, yDim)
    #test cases to check code
    
######## RUNNING THE ALGORITHM
    filter = set()
    listOfAllGraphs = []
    weightedList = []
    knotDiags = []
    allKnots = []
    chart = makeChart(n, xDim, yDim)
    #parallel stuff
    allUnweightedGraphs = parallelEnumerateAllGraphs(xDim, yDim)
    
    #listOfAllGraphs2 = enumerateAllGraphs(xDim,yDim)
    
    print "Total number of unweighted graphs enumerated: " + str(len(allUnweightedGraphs))
    #print len(listOfAllGraphs2)
    #parallelize adding the weights:
    ppservers = ()
    job_server = pp.Server(ppservers=ppservers)
    
    # Parallelize dat adding of weights
    jobs = [(unweightedGraph, job_server.submit(enumerateAllWeightedGraphs, (unweightedGraph, xDim, yDim, 1, chart), (permutate, partition, partitionAll,), ("Graph", "util", ))) for unweightedGraph in allUnweightedGraphs]
    for unweightedGraph, job in jobs:
        weightedList.extend(job())
    
    print "Total number of weighted graphs enumerated: " + str(len(weightedList))
    
    # Parallelize dat enumeration of knot diagrams
    jobs = [(weightedGraph, job_server.submit(enumerateAllKnotDiagrams, (weightedGraph, xDim, yDim, 1), ( ), ("Graph", "util", ))) for weightedGraph in weightedList]
    for weightedGraph, job in jobs:
        knotDiags.extend(job())
    print "Total number of Knot Diagrams enumerated: " + str(len(knotDiags))

    # Parallelize dat getting all the vertices
    jobs = [(knotDiagram, job_server.submit(realizeAllKnots, (knotDiagram, n, ), ( ), ("Graph", "util",))) for knotDiagram in knotDiags]
    for knotDiagram, job in jobs:
        allKnots.append(job())
    knots = []
    for knot in allKnots:
        if knot!= None:
            knots.append(knot)
    
    print "Total number of Knots enumerated: " + str(len(knots))
    
    for knot in knots:
        for vertex in knot:
            print vertex
        print
        
if __name__ == "__main__":
    runAlgorithm(18, 2, 2)

    
        
       

    
    """
    # non parallel code
    listOfAllGraphs = []
    weightedList = []
    knotDiags = []
    
    listOfAllGraphs = enumerateAllGraphs(xDim, yDim)
    print len(listOfAllGraphs)
    for xx in listOfAllGraphs:
        weightedList += enumerateAllWeightedGraphs(xx, xDim, yDim, 1, chart)
    print len(weightedList)
    for weightedGraph in weightedList:
        knotDiags += enumerateAllKnotDiagrams(weightedGraph, xDim, yDim, 1)
    print len(knotDiags)"""
        
    #for x in knotDiags:
    #    if x.getPath():
    #        x.toPrint()
    #        print x.getPath()
    """
    with open('2by3NaiveStrHashNonEq.txt','r') as f:
        lines=[L[:-1] for L in f.readlines()]
    
    for x in listOfAllGraphs:
        notInLines = True
        theGraph = Graph.Graph(x.allVertices, x.allEdges, 3, 3)
        for eqX in x.generateEqClass():
            newGraph = Graph.Graph(eqX.allVertices, eqX.allEdges, 3, 3)
            if str(newGraph.__hash__()) in lines:
                notInLines = False
        if notInLines:
            theGraph.toPrint()
    print 'length is: ' + str(len(listOfAllGraphs))
    #weightedList = []    
    #chart = makeChart(18, xDim, yDim)
    
    
    with open('2by3NaiveStrHashNonEq.txt','r') as f:
        lines=[L[:-1] for L in f.readlines()]
    for hashN in theSet.keys():
        hashS = str(hashN)
        if hashS not in lines:
            #if theSet[hashN] not in alreadyPrinted:
            theSet[hashN].toPrint()
    for line in lines:
        #if line[0] == ">" or line[0] == "<":
        #    inSet = False
        try:
            #if line[0] == ">" and isinstance(int(line[3]), int):
            if theSet[int(line)] == 0:
                theSet[int(line[2:])].toPrint()
            except ValueError:
                print 'errorred'"""
                
    """
    for i in range(len(listOfAllGraphs)):
        weightedList += enumerateAllWeightedGraphs(listOfAllGraphs[i], xDim, yDim, 18, chart)
    
    for x in weightedList:
        x.toPrint()
    
    l = len(listOfAllGraphs)
    t1 = ThreadGraphs(listOfAllGraphs[0:l/2])
    t1.start()
    t2 = ThreadGraphs(listOfAllGraphs[l/2+1:l])
    t2.start()
    
            #testGraph = hashToGraph(hashNum, xDim, yDim)
            #for x in testGraph.generateEqClass():
            #    if x in checkSet:
            #        inSet = True
            #if not inSet:
            #    testGraph.toPrint() 
    chart = makeChart(n, xDim, yDim)
    weightedList = enumerateAllWeightedGraphs(listOfAllGraphs[-1], xDim, yDim, 1, chart)
    weightedList[-1].toPrint()
    list = enumerateAllKnotDiagrams(weightedList[-1], xDim, yDim, 1)
    count = 0
    for x in list:
        if x.getPath():
            x.toPrint()
            print x.g   etPath()"""

    """
    vertex1 = Graph.Vertex(0, 0, xDim, yDim)
    vertex2 = Graph.Vertex(0, 1, xDim, yDim)
    vertex3 = Graph.Vertex(1, 0, xDim, yDim)
    vertex4 = Graph.Vertex(1, 1, xDim, yDim)
    vertex5 = Graph.Vertex(1, 2, xDim, yDim)
    vertex6 = Graph.Vertex(0, 2, xDim, yDim)
    vertex7 = Graph.Vertex(0, 3, xDim, yDim)
    vertex8 = Graph.Vertex(1, 3, xDim, yDim)
    edge1 = Graph.Edge(vertex1, vertex2, 2, xDim, yDim)
    edge2 = Graph.Edge(vertex1, vertex3, 1, xDim, yDim)
    edge3 = Graph.Edge(vertex3, vertex4, 3, xDim, yDim)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), xDim, yDim)
    graph0.addVertex(vertex1)
    graph1 = graph0.addEdge(vertex1, vertex2)
    
    graph2 = graph1.addEdge(vertex3, vertex1)
    graph3 = graph2.addEdge(vertex2, vertex4)
    graph4 = graph3.addEdge(vertex4, vertex3)
    graph4 = graph4.addEdge(vertex4, vertex5)
    graph4 = graph4.addEdge(vertex4, vertex2)
    graph4 = graph4.addEdge(vertex2, vertex6)
    graph5 = graph4
    graph4 = graph4.addEdge(vertex5, vertex6)
    graph6 = graph3.addEdge(vertex3, vertex4)
    graph6 = graph6.addEdge(vertex2, vertex6)
    graph6 = graph6.addEdge(vertex6, vertex7)
    graph6 = graph6.addEdge(vertex8, vertex7)
    #graph6 = graph6.addEdge(vertex8, vertex5)
    chart = makeChart(n, xDim, yDim)
    weightedList = enumerateAllWeightedGraphs(graph4, 3, 1, 1, chart)
    
    list = enumerateAllKnotDiagrams(graph4, xDim, yDim, 1)
    for x in list:
        if x.getPath():
            x.toPrint()
            print x.getPath()
    graph4.toPrint()
    knotdiagram1 = Graph.KnotDiagram(util.Counter(), util.Counter(), xDim, yDim)
    kde1 = Graph.DiagramEdge(vertex1, vertex2, xDim, yDim , 0)
    kde2 = Graph.DiagramEdge(vertex1, vertex2, xDim, yDim , 0)
    knotdiag2 = knotdiagram1.addEdge(kde1)
    kde3 = Graph.DiagramEdge(vertex2, vertex4, xDim, yDim , 1)
    kde4 = Graph.DiagramEdge(vertex2, vertex4, xDim, yDim , 0)
    
    kde5 = Graph.DiagramEdge(vertex4, vertex3, xDim, yDim , 0)
    kde6 = Graph.DiagramEdge(vertex1, vertex3, xDim, yDim , 0)
    kde7 = Graph.DiagramEdge(vertex2, vertex6, xDim, yDim , 1)
    kde8 = Graph.DiagramEdge(vertex4, vertex5, xDim, yDim , 1)
    kde9 = Graph.DiagramEdge(vertex5, vertex6, xDim, yDim , 0)
    
    knotdiag2 = knotdiag2.addEdge(kde3)
    knotdiag2 = knotdiag2.addEdge(kde4)
    knotdiag2 = knotdiag2.addEdge(kde5)
    knotdiag2 = knotdiag2.addEdge(kde6)
    knotdiag2 = knotdiag2.addEdge(kde7)
    knotdiag2 = knotdiag2.addEdge(kde8)
    knotdiag2 = knotdiag2.addEdge(kde9)
    #knotdiag2.toPrint()
    #print knotdiag2.getPath()
    graph7 = graph3.addEdge(vertex3, vertex4).translateYGraph(1)
    graph10 = Graph.Graph(util.Counter(), util.Counter(), 1, 1)
    graph10 = graph10.addEdge(vertex1, vertex2)
    graph10 = graph10.addEdge(vertex1, vertex3)
    graph10 = graph10.addEdge(vertex4, vertex3)
    graph10 = graph10.addEdge(vertex2, vertex4)
    graph11 = Graph.Graph(graph10.allVertices, graph10.allEdges, 1, 2)
    graph3 = graph3.addEdge(vertex3, vertex4)"""
  
          
           
######## bad algorithm #########
"""
@print_timing
def enumerateAllGraphs2(xDim, yDim):
    #set-up to enumerate all graphs by starting with vertex at (0, 0)
    listOfAllGraphs = []
    listOfPaths = []
    listOfTrees = []
    listOfCycleGraph = []
    setOfGraphs = set()
    setOfAllEqGraphs = set()
    setOfExpandedGraphs = set()
    toBeExpandedGraphs = util.Queue()
    v0 = Graph.Vertex(0, 0, xDim, yDim)
    v1 = Graph.Vertex(1, 1, xDim, yDim)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), xDim, yDim)
    graph1 = Graph.Graph(util.Counter(), util.Counter(), xDim, yDim)
    graph0.addVertex(v0)
    graph1.addVertex(v1)
    toBeExpandedGraphs.push(graph0)
    toBeExpandedGraphs.push(graph1)
    counter = 0
    while not toBeExpandedGraphs.isEmpty():
        expandingGraph = toBeExpandedGraphs.pop()
        if expandingGraph!= graph0 and expandingGraph!= graph1:
            rotatedExpanding = expandingGraph.reflectYGraph()
        else:
            rotatedExpanding = None
        if expandingGraph not in setOfExpandedGraphs or expandingGraph == graph1:
            #expandingGraph.toPrint()
            counter += 1
            setOfExpandedGraphs.add(expandingGraph)
            #consider all neighboring vertex and see if you can expand there
            for vertex in expandingGraph.allVertices.values():
                for neighborVertex in expandingGraph.getLegalNeighborVertex(vertex):
                    if not expandingGraph.hasEdge(vertex, neighborVertex):
                        newGraph = expandingGraph.addEdge(vertex, neighborVertex)
                        #newGraph.toPrint()
                        isNotInList = True
                        isNotInEqClass = True
                        if newGraph in setOfGraphs:
                            isNotInList = False
                        eqList = newGraph.generateEqClass()
                        for newEqGraph in eqList:
                            if newEqGraph in setOfAllEqGraphs:
                                isNotInEqClass = False
                            setOfAllEqGraphs.add(newEqGraph)
                        if isNotInList:# and newGraph.expandible():
                            #print newGraph.length
                            #newGraph.toPrint()
                            toBeExpandedGraphs.push(newGraph)
                        if isNotInList and isNotInEqClass:
                            listOfAllGraphs.append(newGraph)
                            setOfGraphs.add(newGraph)
                            toBeExpandedGraphs.push(newGraph)
    
   # print counter
    return listOfAllGraphs
"""

"""
@print_timing
def enumerateAllGraphs3(xDim, yDim):
    listOfAllGraphs = []
    setOfGraphs = set()
    setOfEqGraphs = set()
    expandedGraph = set()
    v0 = Graph.Vertex(0, 0, 1, 1)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), 1, 1)
    graph0.addVertex(v0)
    higherDimExpandibleGraphs = util.Queue()
    xDimExpandibleGraphs = util.Queue()
    toBeExpandedGraphs = util.Stack()
    toBeExpandedGraphs.push(graph0)
    x, y = 1, 1
    #WLOG, we can choose to expand in the y-direction first.
    
    #Now expand in the x-direction
    while y <= yDim:
        expandibleTuple = makeYExpandibleVertices(x, y, xDim, yDim)
        expandingTuple = makeYExpandibleVertices(x, y-1, xDim, yDim)
        
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        if y == 1 and x == 1:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for vertex in expandingGraph.allVertices.values():
                        for neighborVertex in expandingGraph.getLegalNeighborVertex(vertex):
                            if not expandingGraph.hasEdge(vertex, neighborVertex):
                                isNotInList = True
                                isNotInEq = True
                                newGraph = expandingGraph.addEdge(vertex, neighborVertex)
                                biggestDimGraph2 = Graph.Graph(newGraph.allVertices, newGraph.allEdges, xDim, yDim)
                                if isYExpandible(newGraph, expandibleTuple):
                                    higherDimGraph2 = Graph.Graph(newGraph.allVertices, newGraph.allEdges, x, y+1)
                                else:
                                    higherDimGraph2 = newGraph
                                if isXExpandible(newGraph, expandibleXTuples):
                                    xHigherDimGraph = Graph.Graph(newGraph.allVertices, newGraph.allEdges, x+1, yDim)
                                    xDimExpandibleGraphs.push(xHigherDimGraph)
                                if biggestDimGraph2 in setOfGraphs:
                                    isNotInList = False
                                for eqGraph in newGraph.generateEqClass():
                                    biggestDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, xDim, yDim)
                                    if isYExpandible(eqGraph, expandibleTuple):
                                        higherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, y+1)
                                        higherDimExpandibleGraphs.push(higherDimGraph)
                                    else:
                                        higherDimGraph =  Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, yDim)
                                    if isXExpandible(eqGraph, expandibleXTuples):
                                        xHigherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x+1, yDim)
                                        xDimExpandibleGraphs.push(xHigherDimGraph)
                                    if biggestDimGraph in setOfEqGraphs:
                                        isNotInEq = False
                                    if biggestDimGraph not in setOfEqGraphs:
                                        toBeExpandedGraphs.push(eqGraph)
                                        setOfEqGraphs.add(biggestDimGraph)
                                if isNotInList and isNotInEq:
                                    setOfGraphs.add(biggestDimGraph2)
                                    listOfAllGraphs.append(biggestDimGraph2)
        else:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for newGraphExpanded in expandGraphY(expandingGraph, expandingTuple, y-1):
                        biggestDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, xDim, yDim)
                        isNotInList = True
                        isNotInEq = True
                        if isYExpandible(newGraphExpanded, expandibleTuple):
                            higherDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x, y+1)
                            higherDimExpandibleGraphs.push(higherDimGraph2)
                        else:
                            higherDimGraph2 = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x, yDim)
                        if isXExpandible(newGraphExpanded, expandibleXTuples):
                            xHigherDimGraph = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x+1, yDim)
                            xDimExpandibleGraphs.push(xHigherDimGraph)
                        if higherDimGraph2 in setOfGraphs:
                            isNotInList = False
                        for newEqGraph in newGraphExpanded.generateEqClass():
                            biggestDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, xDim, yDim)
                            if isYExpandible(newEqGraph, expandibleTuple):
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, y+1)
                                higherDimExpandibleGraphs.push(higherDimGraph)
                            else:
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, yDim)
                            if isXExpandible(newEqGraph, expandibleXTuples):
                                xHigherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x+1, yDim)
                                xDimExpandibleGraphs.push(xHigherDimGraph)
                            if biggestDimGraph in setOfEqGraphs:
                                isNotInEq = False
                            if biggestDimGraph not in setOfEqGraphs:
                                setOfEqGraphs.add(biggestDimGraph)
                        if isNotInList and isNotInEq:
                            setOfGraphs.add(biggestDimGraph2)
                            listOfAllGraphs.append(biggestDimGraph2)
                                
        y += 1
        toBeExpandedGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set() 
    #CODE FOR THREADING!!!!!
    x += 1
    testList = []
    outputSet = setOfGraphs
    queue = Queue.Queue()
    while x <= xDim:
        while not xDimExpandibleGraphs.isEmpty():
            testGraph = xDimExpandibleGraphs.pop()
            if testGraph not in testList:
                testList.append(testGraph)
            #queue.put(xDimExpandibleGraphs.pop())
        l = len(testList)
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        expandingXTuples = makeXExpandibleVertices(x-1, yDim, xDim, yDim)
        t1 = ThreadUnweightedGraphs(testList[0:l], xDimExpandibleGraphs, outputSet, setOfEqGraphs, expandingXTuples, expandibleXTuples, x, xDim, yDim)
        t1.start()
        t2 = ThreadUnweightedGraphs(testList[l/4:2*l/4], xDimExpandibleGraphs, outputSet, setOfEqGraphs, expandingXTuples, expandibleXTuples, x, xDim, yDim)
        t2.start()
        t3 = ThreadUnweightedGraphs(testList[2*l/4:3*l/4], xDimExpandibleGraphs, outputSet, setOfEqGraphs, expandingXTuples, expandibleXTuples, x, xDim, yDim)
        t3.start()
        t4 = ThreadUnweightedGraphs(testList[3*l/4:l], xDimExpandibleGraphs, outputSet, setOfEqGraphs, expandingXTuples, expandibleXTuples, x, xDim, yDim)
        t4.start()
        x+= 1
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        queue = Queue.Queue()
    return outputSet
    """


