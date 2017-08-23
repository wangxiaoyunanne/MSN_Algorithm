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
import numpy
#from mpi4py import MPI
import itertools
import argparse
import collections
import os
import re
import sys
import pickle
###### EXTRA METHODS ######
def extractListOfEdges(listOfEdgeStr):
    outputList = []
    edge = []
    currTup = []
    paren = 0
    number = ""
    for char in listOfEdgeStr:
        if char == ' ':
            continue
        if char == '(':
            paren += 1
            continue
        #if char == ')' and paren == 2:
        #    paren -= 1
        #    edge.append(currTup)
        #    currTup = []
        #    continue
        if char == ')' and number == "":
            paren -= 1
            continue
        if char == ')' and paren == 2:
            currTup.append(int(number))
            edge.append(currTup)
            currTup = []
            paren -= 1
            number = ""
            continue
        if char == ')' and paren == 1:
            edge.append(int(number))
            outputList.append(edge)
            edge = []
            number = ""
            paren -= 1
        try:
            tempNum = int(char)
            number += str(tempNum)
            continue
            #print number
        except ValueError:
            #if char == ')':
            #    edge.append(int(number))
            #    paren -= 1
            #    number = ""
            if char == ',' and len(number) != 0:
                currTup.append(int(number))
                #print currTup
                number = ""
                continue
    return outputList
            
def makeGraph(listOfEdges, graphXDim, graphYDim, n):
    listOfV = util.Counter()
    listOfE = util.Counter()
    for edgeCoord in listOfEdges:
        vertex1 = Graph.Vertex(edgeCoord[0][0], edgeCoord[0][1], graphXDim, graphYDim)
        vertex2 = Graph.Vertex(edgeCoord[1][0], edgeCoord[1][1], graphXDim, graphYDim)
        listOfV[vertex1.getCoordinate()] = vertex1
        listOfV[vertex2.getCoordinate()] = vertex2
        newE = Graph.Edge(vertex1, vertex2, edgeCoord[2], graphXDim, graphYDim)
        listOfE[newE.getCoordinate()] = newE
    return Graph.Graph(listOfV, listOfE, graphXDim, graphYDim, n)

def makeKnot(listOfEdges, graphXDim, graphYDim, n):
    listOfV = util.Counter()
    listOfE = util.Counter()
    for edgeCoord in listOfEdges:
        vertex1 = Graph.Vertex(edgeCoord[0][0], edgeCoord[0][1], graphXDim, graphYDim)
        vertex2 = Graph.Vertex(edgeCoord[1][0], edgeCoord[1][1], graphXDim, graphYDim)
        listOfV[vertex1.getCoordinate()] = vertex1
        listOfV[vertex2.getCoordinate()] = vertex2
        newE = Graph.DiagramEdge(vertex1, vertex2, graphXDim, graphYDim, edgeCoord[2])
        listOfE[newE.getCoordinate()] = newE
    return Graph.Graph(listOfV, listOfE, graphXDim, graphYDim, n)

## method to measure time of algorithm
def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.3f ms' % (func.func_name, (t2-t1)*1000.0)
        return res
    return wrapper

## method for reading subparts and parsing it to our need
def parse_subpart(line, xDim, yDim, slabNum, n):
    match = re.search(r'\(([-\d]+), "(.*)", \[(.*)\], \[(.*)\]', line)
    if not match:
        return
    output = extractListOfEdges(match.group(2))
    knot_diagram = makeKnot(output, xDim, yDim, n)
    configuration = [int(i) for i in match.group(3).split(',')]
    stack = []
    keys = []
    tup = ''
    allkeys = []
    for char in match.group(4):
        if len(stack) == 2:
            if char != ')' and char != '(':
                tup += char
        if char == '(':
            stack.append(char)
        if char == ')':
            stack.pop()
            if len(stack) == 1:
                num1, num2 = tup.split(',')
                vertex = (int(num1), int(num2))
                tup = ''
                keys.append(vertex)
            if len(stack) == 0:
                allkeys.append(tuple(keys))
                keys = []
    return int(match.group(1)), (knot_diagram, (configuration, tuple(allkeys)))

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

"""
def generateLsOfYCoord(yDim):
    lsOfYCoords = []
    for ele in divideArr(range(yDim +1)):
        if isinstance(ele, int):
            lsOfYCoords.append([ele])
        else:
            tmp = []
            for x in iter_flatten(ele):
                tmp.append(x)
            lsOfYCoords.append(tmp)
    return lsOfYCoords

#returns list of possible x expansions
def createXGraphs(xDim, yDim, n):
    expandibleGraphs = util.Stack()
    expandedGraphs = set()
    newGraphSet = set()
    keyVertexList = []
    leftVertices = []
    left = []
    rightVertices = dict()
    allGraphs = []
    returnGraphSet = dict()
    lsOfYCoords = generateLsOfYCoord(yDim)
    for yC in range(yDim+1):
        returnGraphSet[yC] = []
    listOfExpandibleVert = makeXExpandibleVertices(0, yDim, xDim, yDim)
    givenGraph = Graph.Graph(util.Counter(), util.Counter(), xDim, yDim, n)
    x = 0
    for vertTup in listOfExpandibleVert:
        newVert = Graph.Vertex(vertTup[0], vertTup[1], xDim, yDim)
        leftVertices.append(newVert)
        left.append(newVert)
        givenGraph.allVertices[vertTup] = newVert
    #givenGraph.toPrint()
    for i in range(yDim+1):
        rightVertex = Graph.Vertex(x+1, i, givenGraph.graphXDim, givenGraph.graphYDim)
        rightVertices[i] = rightVertex
    for lef in divideArr(left):
        if isinstance(lef, Graph.Vertex):
            expandingGraph = givenGraph.addEdge(lef, rightVertices[lef.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
            for edge in expandingGraph.allEdges.values():
                if edge.v1.xCoord == x and edge.v2.xCoord==x+1:
                    returnGraphSet[edge.v1.yCoord].append(expandingGraph)            
        else:
            expandingGraph = givenGraph
            for v in iter_flatten(lef):
                expandingGraph = expandingGraph.addEdge(v, rightVertices[v.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
            for edge in expandingGraph.allEdges.values():
                if edge.v1.xCoord == x and edge.v2.xCoord==x+1:
                    returnGraphSet[edge.v1.yCoord].append(expandingGraph)
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
                        elif xDim < 6 and xDim == yDim:
                            condition = (neighborVertex.xCoord != x and vert.xCoord != x and neighborVertex.xCoord != x-1) or (neighborVertex.xCoord == x and neighborVertex.yCoord == vert.yCoord) and neighborVertex not in givenGraph.allVertices.values()
                        else:
                            condition = neighborVertex not in givenGraph.allVertices.values()
                        if condition:
                            if not expandingGraph.hasEdge(vert, neighborVertex):
                                newGraph = expandingGraph.addEdge(vert, neighborVertex)
                                if not newGraph in newGraphSet:
                                    theYCoords = []
                                    for edge in newGraph.allEdges.values():
                                        if edge.v2.xCoord == x+1 and edge.v1.xCoord == x:
                                            returnGraphSet[edge.v1.yCoord].append(newGraph)
                                    newGraphSet.add(newGraph)
                                    expandibleGraphs.push(newGraph)
    return returnGraphSet
@print_timing
def expandGraphX2(givenGraph, expandingAddonSet, x, xDim, yDim):
    #print "given Graph"
    #givenGraph.toPrint()
    alreadyExpanded = set()
    output = set()
    for yC in range(yDim+1):
        for addons in expandingAddonSet[yC]:
            #addons.toPrint()
            if addons not in alreadyExpanded:
                alreadyExpanded.add(addons)
                addonE = addons.allEdges.values()
                edge1 = addonE[0]
                newE1 = Graph.Edge(Graph.Vertex(edge1.v1.xCoord+x, edge1.v1.yCoord, xDim, yDim), Graph.Vertex(edge1.v2.xCoord+x, edge1.v2.yCoord, xDim, yDim), edge1.weight, xDim, yDim)
                newGraph = givenGraph.addEdge(newE1.v1, newE1.v2)
                for edge in addonE[1:-1]:
                    newE = Graph.Edge(Graph.Vertex(edge.v1.xCoord+x, edge.v1.yCoord, xDim, yDim), Graph.Vertex(edge.v2.xCoord+x, edge.v2.yCoord, xDim, yDim), edge.weight, xDim, yDim)
                    newGraph.imm_addEdge(newE)
                if len(addonE) >= 2:
                    edgeF = addonE[-1]
                    newEF = Graph.Edge(Graph.Vertex(edgeF.v1.xCoord+x, edgeF.v1.yCoord, xDim, yDim), Graph.Vertex(edgeF.v2.xCoord+x, edgeF.v2.yCoord, xDim, yDim), edgeF.weight, xDim, yDim)
                    newGraph = newGraph.addEdge(newEF.v1, newEF.v2)
                #newGraph.toPrint()
                if newGraph not in output:
                    #newGraph.toPrint()
                    output.add(newGraph)
    return output
@print_timing
"""
def expandGraphX(givenGraph, listOfExpandibleVert, x, xDim, yDim):
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
    for lef in divideArr(left):
        if isinstance(lef, Graph.Vertex):
            expandingGraph = givenGraph.addEdge(lef, rightVertices[lef.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
        else:
            expandingGraph = givenGraph
            for v in iter_flatten(lef):
                expandingGraph = expandingGraph.addEdge(v, rightVertices[v.yCoord])
            expandibleGraphs.push(expandingGraph)
            newGraphSet.add(expandingGraph)
            allGraphs.append(expandingGraph)
    while not expandibleGraphs.isEmpty():
        expandingGraph = expandibleGraphs.pop()
        #expandingGraph.toPrint()
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
                        elif xDim < 6 and xDim == yDim:
                            condition = (neighborVertex.xCoord != x and vert.xCoord != x and neighborVertex.xCoord != x-1) or (neighborVertex.xCoord == x and neighborVertex.yCoord == vert.yCoord) and neighborVertex not in givenGraph.allVertices.values()
                        else:
                            condition = neighborVertex not in givenGraph.allVertices.values()
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
def enumerateAllGraphs(xDim, yDim, n):
    #xExpanded = createXGraphs(xDim, yDim, n)
    listOfAllGraphs = []
    setOfGraphs = set()
    expandedGraph = set()
    v0 = Graph.Vertex(0, 0, 1, 1)
    graph0 = Graph.Graph(util.Counter(), util.Counter(), 1, 1, n)
    graph0.addVertex(v0)
    higherDimExpandibleGraphs = util.Stack()
    xDimExpandibleGraphs = set()
    toBeExpandedGraphs = util.Stack()
    toBeExpandedGraphs.push(graph0)
    x, y = 1, 1
    
    #WLOG, we can choose to expand in the y-direction first.
    while y <= yDim:
        expandibleTuple = makeYExpandibleVertices(x, y, xDim, yDim)
        expandingTuple = makeYExpandibleVertices(x, y-1, xDim, yDim)
        expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
        #base case: 1 x 1 square
        if y == 1:
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for vertex in expandingGraph.allVertices.values():
                        for neighborVertex in expandingGraph.getLegalNeighborVertex(vertex):
                            if not expandingGraph.hasEdge(vertex, neighborVertex):
                                newGraph = expandingGraph.addEdge(vertex, neighborVertex)
                                eqClass = newGraph.generateEqClass()
                                biggestDimGraph2 = Graph.Graph(eqClass[0].allVertices, eqClass[0].allEdges, xDim, yDim, n)
                                if isXExpandible(newGraph, expandibleXTuples):
                                    xHigherDimGraph = Graph.Graph(newGraph.allVertices, newGraph.allEdges, x+1, yDim, n)
                                    xDimExpandibleGraphs.add(xHigherDimGraph)
                                if biggestDimGraph2 in setOfGraphs:
                                    continue
                                setOfGraphs.add(biggestDimGraph2)
                                for eqGraph in eqClass[1]:
                                    toBeExpandedGraphs.push(eqGraph)
                                    if isYExpandible(eqGraph, expandibleTuple):
                                        higherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x, y+1, n)
                                        higherDimExpandibleGraphs.push(higherDimGraph)
                                    if isXExpandible(eqGraph, expandibleXTuples):
                                        xHigherDimGraph = Graph.Graph(eqGraph.allVertices, eqGraph.allEdges, x+1, yDim, n)
                                        xDimExpandibleGraphs.add(xHigherDimGraph)
        else:
            #induct on y-expansion first
            while not toBeExpandedGraphs.isEmpty():
                expandingGraph = toBeExpandedGraphs.pop()
                if expandingGraph not in expandedGraph:
                    expandedGraph.add(expandingGraph)
                    for newGraphExpanded in expandGraphY(expandingGraph, expandingTuple, y-1):
                        eqClass2 = newGraphExpanded.generateEqClassY()
                        biggestDimGraph2 = Graph.Graph(eqClass2[0].allVertices, eqClass2[0].allEdges, xDim, yDim, n)
                        if isXExpandible(newGraphExpanded, expandibleXTuples):
                            xHigherDimGraph = Graph.Graph(newGraphExpanded.allVertices, newGraphExpanded.allEdges, x+1, yDim, n)
                            xDimExpandibleGraphs.add(xHigherDimGraph)
                        if biggestDimGraph2 in setOfGraphs:
                            continue
                        if newGraphExpanded.isYFull:
                            setOfGraphs.add(biggestDimGraph2)
                        for newEqGraph in eqClass2[1]:
                            #if newEqGraph.isYFull:
                            if isYExpandible(newEqGraph, expandibleTuple):
                                higherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x, y+1, n)
                                higherDimExpandibleGraphs.push(higherDimGraph)
                            if isXExpandible(newEqGraph, expandibleXTuples):
                                xHigherDimGraph = Graph.Graph(newEqGraph.allVertices, newEqGraph.allEdges, x+1, yDim, n)
                                xDimExpandibleGraphs.add(xHigherDimGraph)
                                
        y += 1
        toBeExpandedGraphs = higherDimExpandibleGraphs
        higherDimExpandibleGraphs = util.Queue()
        expandedGraph = set() 
    x+=1
    newSet = xDimExpandibleGraphs
    xDimExpandibleGraphs = set()
    #Now expand in the x-direction
    while x <= xDim:
        for expandingGraph in newSet:
            if expandingGraph not in expandedGraph:
                expandibleXTuples = makeXExpandibleVertices(x, yDim, xDim, yDim)
                expandingXTuples = makeXExpandibleVertices(x-1, yDim, xDim, yDim)
                expandedGraph.add(expandingGraph)
                expandedGraph.add(expandingGraph.reflectXGraph())
                #expandingGraph.toPrint()
                for newXGraph in expandGraphX(expandingGraph, expandingXTuples, x-1, xDim, yDim):
                #for newXGraph in expandGraphX2(expandingGraph, xExpanded, x-1, xDim, yDim):
                    if isXExpandible(newXGraph, expandibleXTuples):
                        higherDimXEqGraph = Graph.Graph(newXGraph.allVertices, newXGraph.allEdges, x+1, yDim, n)
                        xDimExpandibleGraphs.add(higherDimXEqGraph)
                    # Ignore if y is full but x is not
                    if not newXGraph.isXFull and newXGraph.isYFull:
                        continue
                    # Check if x is full but y is not full if x > y. if so then add. else we know eq is made at y expansion so ignore
                    if newXGraph.isXFull and not newXGraph.isYFull:
                        tempGraph = newXGraph.reduceGraph()
                        if newXGraph.graphXDim > newXGraph.graphYDim:
                            eqClass = tempGraph.generateEqClass()
                            checkEq = eqClass[0]
                            biggestDimXGraph = Graph.Graph(checkEq.allVertices, checkEq.allEdges, xDim, yDim, n)
                            if biggestDimXGraph in setOfGraphs:
                                continue       
                            setOfGraphs.add(biggestDimXGraph)
                        elif newXGraph.graphXDim < newXGraph.graphYDim:
                            if tempGraph.graphYDim != 1:
                                eqClass = tempGraph.generateEqClass()
                                checkEq = eqClass[0]
                                biggestDimXGraph = Graph.Graph(checkEq.allVertices, checkEq.allEdges, xDim, yDim, n)
                                setOfGraphs.add(biggestDimXGraph)
                        eqClass = newXGraph.generateEqClass()
                            
                    # Check if both x and y full. If so, add
                    elif newXGraph.isXFull and newXGraph.isYFull:
                        eqClass = newXGraph.generateEqClass()
                        checkEq = eqClass[0]
                        biggestDimXGraph = Graph.Graph(checkEq.allVertices, checkEq.allEdges, xDim, yDim, n)
                        if biggestDimXGraph in setOfGraphs:
                            continue       
                        setOfGraphs.add(biggestDimXGraph)
                    # both not full
                    else:
                        eqClass = newXGraph.generateEqClass()
                    # For the case x is not full and y is not full, note it has been added before so just check for equivalent ones for future expansion
                    for newEqXGraph in eqClass[1]:
                        if isXExpandible(newEqXGraph, expandibleXTuples):
                            higherDimXEqGraph = Graph.Graph(newEqXGraph.allVertices, newEqXGraph.allEdges, x+1, yDim, n)
                            xDimExpandibleGraphs.add(higherDimXEqGraph)
        x += 1
        newSet = xDimExpandibleGraphs
        xDimExpandibleGraphs = set()
        expandedGraph = set() 
    return setOfGraphs


###################### STEP ONE METHODS #########################

# helper method for Step 1 in creating possible a, b, and c to add in the weights
def makeChart(n, xDim, yDim):
    c_max = int(math.floor(n/3))
    if c_max%2 == 1:
        c_max -= 1
    c_min = 4
    c_value = 4
    c_range = [4]
    while c_value != c_max:
        c_value += 2
        c_range.append(c_value)
    a_min = 4
    listOfTripletABC = []
    a_value = a_min
    b_value = n - a_min - c_min
    for c in c_range:
        a_value = c
        b_value = n - a_value - c
        while b_value >= c:
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
def enumerateAllWeightedGraphs(givenGraph, xDim, yDim, slabNum, givenChart, n):
    #initialize the sets
    filter = set()
    equivalentGraphSet = set()
    weightedGraphSet = set()
    
    #start with all possible triplets
    for possible_triplet in givenChart:
        possibleAWeights = partition(possible_triplet[2], givenGraph.unweighted_a)
        possibleBWeights = partition(possible_triplet[1], givenGraph.unweighted_b)  
        for a_value in possibleAWeights:
            legalAVal = True
            for a_vals in a_value:
                if a_vals > slabNum+1:
                    legalAVal = False
                    break
            if not legalAVal:
                break
            permutationOfAValues = permutate(a_value)
            for b_value in possibleBWeights:
                legalBVal = True
                for b_vals in b_value:
                    if b_vals > slabNum+1:
                        legalBVal = False
                        break
                if not legalBVal:
                    break
                permutationOfBValues = permutate(b_value)
                for permute_a in permutationOfAValues:
                    for permute_b in permutationOfBValues:
                        newAllEdges = util.Counter()
                        i = 0
                        j = 0
                        for edge in givenGraph.allEdges:
                            graphEdge = givenGraph.allEdges[edge]
                            if graphEdge.orientation == '|':
                                newEdge = Graph.Edge(graphEdge.v1, graphEdge.v2, permute_b[i], graphEdge.graphXDim, graphEdge.graphYDim)
                                i += 1
                            elif graphEdge.orientation == '_':
                                newEdge = Graph.Edge(graphEdge.v1, graphEdge.v2, permute_a[j], graphEdge.graphXDim, graphEdge.graphYDim)
                                j += 1
                            newAllEdges[newEdge.getCoordinate()] = newEdge
                        newGraph = Graph.Graph(givenGraph.allVertices, newAllEdges, givenGraph.graphXDim, givenGraph.graphYDim, n)
                        legal = newGraph.isLegalWeightedGraph() and (not newGraph.isReducible(slabNum))
                        if newGraph not in filter and legal:
                        #if legal:
                                #newGraph.toPrint()
                            weightedGraphSet.add(newGraph)
                            #if possible_triplet == [8, 10, 8]:
                            #    print permute_a, permute_b, possible_triplet
                            #    newGraph.toPrint()
                            for eqGraph in newGraph.generateEqClass()[1]:
                                filter.add(eqGraph)
    
    return weightedGraphSet

###################### STEP TWO METHODS #########################

#helper method to create alternating level edges
def generateEdgeBank(xDim, yDim, slabNum):
    edgeBank = util.Counter()
    xCoords = range(xDim+1)
    yCoords = range(yDim+1)
    verticeList = list(itertools.product(xCoords, yCoords))
        
    while len(verticeList) != 0:
        currVert = verticeList.pop(0)
        v = Graph.Vertex(currVert[0], currVert[1], xDim, yDim)
        if currVert[0]+1 <=  xDim and 0 <= currVert[0]+1:
            de = Graph.DiagramEdge(v, Graph.Vertex(currVert[0]+1, currVert[1], xDim, yDim), xDim, yDim , 0)
            coords = de.getCoordinate()
            tempTuple = (coords[0], coords[1])
            edgeBank[tempTuple] = []
            edgeBank[tempTuple].append(de)
            for i in range(slabNum):
                edgeBank[tempTuple].append(Graph.DiagramEdge(v, Graph.Vertex(currVert[0]+1, currVert[1], xDim, yDim), xDim, yDim , i+1))
                
        if currVert[0]-1 <=  xDim and 0 <= currVert[0]-1:
            de = Graph.DiagramEdge(v, Graph.Vertex(currVert[0]-1, currVert[1], xDim, yDim), xDim, yDim , 0)
            coords = de.getCoordinate()
            tempTuple = (coords[0], coords[1])
            edgeBank[tempTuple] = []
            edgeBank[tempTuple].append(de)
            for i in range(slabNum):
                edgeBank[tempTuple].append(Graph.DiagramEdge(v, Graph.Vertex(currVert[0]-1, currVert[1], xDim, yDim), xDim, yDim , i+1))
                
        if currVert[1]+1 <= yDim and 0 <= currVert[1]+1:
            de = Graph.DiagramEdge(v, Graph.Vertex(currVert[0], currVert[1]+1, xDim, yDim), xDim, yDim , 0)
            coords = de.getCoordinate()
            tempTuple = (coords[0], coords[1])
            edgeBank[tempTuple] = []
            edgeBank[tempTuple].append(de)
            for i in range(slabNum):
                edgeBank[tempTuple].append(Graph.DiagramEdge(v, Graph.Vertex(currVert[0], currVert[1]+1, xDim, yDim), xDim, yDim , i+1)) 
        if currVert[1]-1 <= yDim and 0 <= currVert[1]-1:
            de = Graph.DiagramEdge(v, Graph.Vertex(currVert[0], currVert[1]-1, xDim, yDim), xDim, yDim , 0)
            coords = de.getCoordinate()
            tempTuple = (coords[0], coords[1])
            edgeBank[tempTuple] = []
            edgeBank[tempTuple].append(de)
            for i in range(slabNum):
                edgeBank[tempTuple].append(Graph.DiagramEdge(v, Graph.Vertex(currVert[0], currVert[1]-1, xDim, yDim), xDim, yDim , i+1)) 
    return edgeBank
    
# index keeping track of possible knot diagram edges permutation by edge weight
def generateEdgeIndex(slabNum):
    edgeIndex = []
    for i in range(slabNum+2):
        edgeIndex.append([])
        
    for ele in divideArr(range(slabNum+1)):
        result = []
        if isinstance(ele, list):
            for ele2 in iter_flatten(ele):
                result.append(ele2)
        else:
            result.append(ele)
        edgeIndex[len(result)].append(result)
    return edgeIndex


###################### STEP TWO METHODS #########################

# Step 2 of MSN Algorithm: enumerate all knot diagram given weighted graphs
def enumerateAllKnotDiagrams(givenWeightedGraph, xDim, yDim, slabNum, n, edgeBank, edgeIndex):
    newAllVertices = givenWeightedGraph.allVertices
    for vertex in givenWeightedGraph.allVertices.values():
        if givenWeightedGraph.getValence(vertex) > (slabNum+1)*2:
            return []
    # list of permutation indices for each respective weighted edge
    edgePermutation = util.Counter()
    edgeWeights = []
    baseArray = []
    # fill in the edgeBankd and edgePermutation according to each edge in the given weighted graph    
    for theEdge in givenWeightedGraph.allEdges.values():
        # dictionary with key as coordinate of edge and value as the possible permutations of edge bank indices
        edgePermutation[theEdge.getCoordinate()] = edgeIndex[theEdge.weight]
    for permuted in edgePermutation.values():
        edgeWeights.append(len(permuted)-1)
        baseArray.append(0)
    baseArray[0] = -1
    while not baseArray == edgeWeights:
        result = []
        baseArray[0] += 1
        indexCount = 0
        while (baseArray[indexCount] > edgeWeights[indexCount]):
            baseArray[indexCount+1] += (baseArray[indexCount]-edgeWeights[indexCount])
            baseArray[indexCount] = 0
            indexCount += 1
        accessCounter = 0
        KnotDiagramEdges = util.Counter()
        vertexCounter = util.Counter()
        allkeys = edgePermutation.keys()
        broken = False
        for i in range(len(edgePermutation.values())):
            index = edgePermutation.values()[i]   
            for indexx in index[baseArray[accessCounter]]:
                tempKD = edgeBank[allkeys[i]][indexx]
                KnotDiagramEdges[tempKD.getCoordinate()] = tempKD
                vertexCounter[tempKD.getCoordinate()[0], tempKD.getCoordinate()[2]] += 1
                vertexCounter[tempKD.getCoordinate()[1], tempKD.getCoordinate()[2]] += 1
                if vertexCounter[tempKD.getCoordinate()[0], tempKD.getCoordinate()[2]] >= 3 or vertexCounter[tempKD.getCoordinate()[1], tempKD.getCoordinate()[2]] >= 3:
                    broken = True
                    break
            accessCounter+=1
        if not broken:
            targetKnotDiagram = Graph.KnotDiagram(givenWeightedGraph.allVertices, KnotDiagramEdges, xDim, yDim, n)
            #print targetKnotDiagram.toPrint()
            #f = open('tarKD.txt','a')
            print >> targetKnotDiagram.toPrint()
            #f.close()

            path = realizeAllKnots(targetKnotDiagram, n)
            if path:
                print path

###################### STEP THREE METHODS #########################
# Step 3 of MSN Algorithm: realize all valid Knot Diagrams into actual Knots

def realizeAllKnots(givenKnotDiagram, n):
    path = givenKnotDiagram.getPath()
    if path!=0 and len(path) == n:
        return path
    else:
        return 0

#check if neighbor
def isNeighbor(vert1, vert2):
    if (abs(vert1[0]-vert2[0]) == 1 and vert1[1]-vert2[1] == 0 and vert1[2]-vert2[2] == 0) or (vert1[0]-vert2[0] == 0 and abs(vert1[1]-vert2[1]) == 1 and vert1[2]-vert2[2] == 0) or (abs(vert1[2]-vert2[2]) == 1 and vert1[1]-vert2[1] == 0 and vert1[0]-vert2[0] == 0):
        return True
    return False
#check to see if reducible
def checkReducible(path):
    for i in range(len(path)):
        if isNeighbor(path[i], (path[(i+3)%len(path)])):
            return (True, (path[i], path[(i+1)%len(path)], path[(i+2)%len(path)], path[(i+3)%len(path)]))
    return False
    
def realizeAllKnots(givenKnotDiagram, n):
    path = givenKnotDiagram.getPath()
    if path!=0 :
        return path
    else:
        return 0

def runAlgorithm(xDim, yDim, slabNum, n, serialFlag):
    import __main__
    #test cases to check code
    
######## RUNNING THE ALGORITHM    
    #all serial stuff
    edgeBank = generateEdgeBank(xDim, yDim, slabNum)
    edgeIndex = generateEdgeIndex(slabNum)
    listOfAllGraphs = []
    weightedList = []
    knotDiags = []
    allKnots = []
    chart = makeChart(n, xDim, yDim)
    if serialFlag:
        """
        fileName = "figEightSortedGraphs.txt"
        newWeightedList = []
        with open(fileName, 'r') as f:
            idLines=[L[:-1] for L in f.readlines()]
            iiii = 74
            for line in idLines[iiii:200]:
                if line[0] == '(':
                    output = extractListOfEdges(line)
                    newG = makeGraph(output, xDim, yDim, n)
                    newWeightedList.append(newG)
            #newWeightedList.sort(key=lambda x: x[0])
            
            for wgraph in newWeightedList:
                print iiii
                wgraph.toPrint()
                #    print wgraph[1].printEdges()
                enumerateAllKnotDiagrams(wgraph, xDim, yDim, slabNum, n, edgeBank, edgeIndex)
                iiii += 1
        """
        #print "Running for n = %u, for %u by %u" % (n, xDim, yDim)
        listOfAllGraphs = enumerateAllGraphs(xDim,yDim, n)
        print "Total number of unweighted graphs enumerated: " + len(listOfAllGraphs).__str__()
        #enumerate the weighted graphs now
        for ugraph in listOfAllGraphs:
            weightedList.extend(enumerateAllWeightedGraphs(ugraph, xDim, yDim, slabNum, chart, n)) 
        print "Total number of weighted graphs enumerated: " + len(weightedList).__str__()
        for wgraph in weightedList:
           # print wgraph.printEdges()
           # wgraph.toPrint()
            # Node ID is 0 for serial version
            enumerateAllKnotDiagrams(wgraph, xDim, yDim, slabNum, n, edgeBank, edgeIndex)
        #"""
    else:
        comm = MPI.COMM_WORLD
        size = comm.size
        root = 0
        scattering = []
        scattering1 = []
        scattering2 = []
        scattering3 = []
        if comm.rank == 0:
            #run with given weighted graphs`
            #fileName = "fig8W" + str(n) + "_weightedGraphs.txt"
            fileName = "figEightSortedGraphs.txt"
            incomplete = "indices_done.txt"
            newWeightedList = []
            with open(fileName, 'r') as f:
                idLines=[L[:-1] for L in f.readlines()]
                index_done = set()
                #### USED FOR FILLING IN UNFINISHED JOBS ####
                with open(incomplete, 'r') as f2:
                    idLines2=[L[:-1] for L in f2.readlines()]
                    for ind in idLines2:
                        try:
                            index_done.add(int(ind))
                        except ValueError:
                            continue
                #for remaining in index_left:
                #output = extractListOfEdges(idLines[remaining])
                #newWeightedList.append((makeGraph(output, xDim, yDim, n),remaining))
                for remaining in xrange(2000, len(idLines)):
                    if remaining not in index_done:
                        output = extractListOfEdges(idLines[remaining])
                        newWeightedList.append((makeGraph(output, xDim, yDim, n),remaining))
            #regular run
            """
            print "Running for n = %u, for %u by %u" % (n, xDim, yDim)
            listOfAllGraphs = enumerateAllGraphs(xDim,yDim, n)
            length = len(listOfAllGraphs)
            listOfGraphs = list(listOfAllGraphs)
            print "Total number of unweighted graphs enumerated: " + str(length)
            #length = 150
            if size < length:
                for i in range(size):
                    scattering1.append(listOfGraphs[i*length/size:(i+1)*length/size])
            else:
                scattering1.append(listOfGraphs)
                for i in range(size-1):
                    scattering1.append([])
            
            v1=comm.scatter(scattering1, root)
            y = []
            for unweightedGraph in v1:
                y.extend(enumerateAllWeightedGraphs(unweightedGraph, xDim, yDim, slabNum, chart, n))
            weightedList=comm.gather(y,root)
    
            if comm.rank==0:
                fullWeightedList = []
                for graphs in numpy.array(weightedList):
                    for x in graphs:
                        fullWeightedList.append(x)
                #newWeightedList = fullWeightedList[:100]
                newWeightedList = fullWeightedList
            """
            length = len(newWeightedList)
            #length = len(fullWeightedList)
            #length = len(newWeightedList)
            print "Total number of weighted graphs enumerated: " + str(length)
            #print "from " + str(start) + " to " + str(end)
            #for wgraphh in fullWeightedList:
            #print wgraphh.printEdges()
            #length = len(newWeightedListt)
            if size <= length:
                for i in range(size):
                    scattering2.append(newWeightedList[i*length/size:(i+1)*length/size])
            else:
                scattering2.append(newWeightedList)
                for i in range(size-1):
                    scattering2.append([])
    
        v2=comm.scatter(scattering2,root)
        y = []
        for weightedGraph in v2:
            enumerateAllKnotDiagrams(comm.rank, weightedGraph[0], xDim, yDim, slabNum, n, edgeBank, edgeIndex)
            print weightedGraph[1]
            
def main(args):
    try:
        if args[0] == '-h':
            print
            print "Runs the MSN Algorithm with given parameters"
            print
            print "Usage: python msnAlgRunner.py [-h] x_dim y_dim z_dim step_number s/p"
            print
            print "Positional Arguments: "
            print "     x_dim           dimension of x projection/slab number"
            print "     y_dim           dimension of y projection"
            print "     z_dim           dimension of z realization"
            print "     step_number     target step number to enumerate"
            print "     s/p             flag to run it serial or parallel"
            print
            return
        else:
            flagg = args[4]
            args = args[:-1]
            args = [int(x) for x in args]
            
            if flagg == 's' or flagg == 'S':
                flag = True
            elif flagg == 'p' or flagg == 'P':
                flag = False
            else:
                print
                print "Make the last argument s or p for serial or parallel"
                print "Or type python msnAlgRunner.py -h for more help!"
                print
                return
            
    except Exception:
            print
            print "Type "
            print "python msnAlgRunner.py -h"
            print "for more help!"
            print
            return
    runAlgorithm(args[0], args[1], args[2], args[3], flag)
        
    
if __name__ == "__main__":
    main(sys.argv[1:])
          
           
######## extra stuff #########

"""
            path = realizeAllKnots(targetKnotDiagram, n)
            if path:
                checkRed = checkReducible(path)
                if not checkRed:
                    print path
                else:
                    reducibleEdges = []
                    for count in range(len(checkRed[1])-1):
                        coord1 = checkRed[1][count]
                        coord2 = checkRed[1][count+1]
                        if not (coord2[1] == coord1[1] and coord2[0] == coord1[0]):
                            if coord1[1] == coord2[1]:
                                if coord1[0] < coord2[0]:
                                    tup = ((coord1[0], coord1[1]), (coord2[0], coord2[1]))
                                else:
                                    tup = ((coord2[0], coord2[1]), (coord1[0], coord1[1]))
                            else:
                                if coord1[1] < coord2[1]:
                                    tup = ((coord1[0], coord1[1]), (coord2[0], coord2[1]))
                                else:
                                    tup = ((coord2[0], coord2[1]), (coord1[0], coord1[1]))
                            reducibleEdges.append(tup)
                    if len(reducibleEdges) == 3:
                        illegalConfig = []
                        for reducibE in reducibleEdges:
                            inddd = allkeys.index(reducibE)
                            illegalConfig.append((inddd, baseArray[inddd]))
                        setofIllegalConfigs.add(tuple(illegalConfig))
                        print illegalConfig
                    elif len(reducibleEdges) == 1:
                        illegalConfig = []
                        for ii in range(len(allkeys)):
                            key = allkeys[ii]
                            if key == reducibleEdges[0]:
                                illegalConfig.append((ii, baseArray[ii]))
                                print key
                            elif reducibleEdges[0][0] in key or reducibleEdges[0][1] in key:  
                                illegalConfig.append((ii, baseArray[ii]))
                                print key
                        setofIllegalConfigs.add(tuple(illegalConfig))
                        print illegalConfig"""

