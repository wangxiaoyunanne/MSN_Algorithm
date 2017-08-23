import util
# Vertex Class
# -------
# Primitive part of Graph that represents the Vertices that make the graph

class Vertex:
    #constructor, takes in an x coordinate, y coordinate, and the dimensions of the graph that this vertex belongs to
    def __init__(self, xCoord, yCoord, graphXDim, graphYDim):
        self.coordinate = (xCoord, yCoord)
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim
    #returns the coordinates, (x coordinate, y coordinate) of this vertex
    def getCoordinate(self):
        return self.coordinate
    
    #to string method that prints the coordinates
    def __str__(self):
        return self.coordinate.__str__()

    # subtracts two vertex objects by the x and y coordinate and returns the difference tuple
    def subtract(self, other):
        x = self.xCoord - other.xCoord
        y = self.yCoord - other.yCoord
        return (x,y)
        
    # equals method that returns if one vertex has the same coordinates as the other
    def __eq__(self, other):
        return self.getCoordinate() == other.getCoordinate()

# Edge Class
# -------
# Primitive part of Graph that represents the Edges that make the graph

class Edge:
    # Orient the vertices so that an edge has a left to right orientation or bottom to up orientation
    def __init__(self, vertex1, vertex2, weight, graphXDim, graphYDim):
        self.weight = weight
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim
        self.v1 = vertex1
        self.v2 = vertex2
        subtractVertex = vertex1.subtract(vertex2)
        if subtractVertex[0] == 0:
            self.orientation = '|'
            if subtractVertex[1] < 0:
                self.v1 = vertex1
                self.v2 = vertex2
            else:
                self.v1 = vertex2
                self.v2 = vertex1

        elif subtractVertex[1] == 0:
            self.orientation = '_'
            if subtractVertex[0] < 0:
                self.v1 = vertex1
                self.v2 = vertex2
            else:
                self.v1 = vertex2
                self.v2 = vertex1
        else:
            self.orientation = 'invalid'
        self.edgeCoordinates = (self.v1.getCoordinate(), self.v2.getCoordinate())

    def getCoordinate(self):
        return (self.v1.getCoordinate(), self.v2.getCoordinate())
    
    def isLegalVertex(self, vertex):
        return vertex.xCoord >= 0 and vertex.xCoord <= self.graphXDim and vertex.yCoord >= 0 and vertex.yCoord <= self.graphYDim

    def isLegalEdge(self):
        if self.isLegalVertex(self.v1) and self.isLegalVertex(self.v2):
            return not self.orientation == 'invalid'
        else:
            return False
    
    def rotateEdge(self, degree):
        factor1 = 0
        factor2 = 0
        factor3 = 0
        factor4 = 0
        xAddive = 0
        yAddive = 0
        if degree == 90:
            factor2 = -1
            factor3 = 1
            xAddive = 0
            yAddive = 0
        elif degree == 180:
            factor1 = -1
            factor4 = -1
            xAddive = 1
            yAddive = 1
        elif degree == 270:
            factor2 = 1
            factor3 = -1
        elif degree == 360:
            factor1 = 1
            factor4 = 1
        else:
            return None
        newVertex1 = Vertex(factor1*self.v1.getCoordinate()[0]+factor2*self.v1.getCoordinate()[1]+xAddive, factor3*self.v1.getCoordinate()[0]+factor4*self.v1.getCoordinate()[1]+yAddive, self.graphXDim, self.graphYDim)
        newVertex2 = Vertex(factor1*self.v2.getCoordinate()[0]+factor2*self.v2.getCoordinate()[1]+xAddive, factor3*self.v2.getCoordinate()[0]+factor4*self.v2.getCoordinate()[1]+yAddive, self.graphXDim, self.graphYDim)
        newEdge = Edge(newVertex1, newVertex2, self.weight, self.graphXDim, self.graphYDim)
        return newEdge
        
    def translateY(self, yAmount):
        newV1 = Vertex(self.v1.getCoordinate()[0], self.v1.getCoordinate()[1]+yAmount, self.graphXDim, self.graphYDim)
        newV2 = Vertex(self.v2.getCoordinate()[0], self.v2.getCoordinate()[1]+yAmount, self.graphXDim, self.graphYDim)
        newEdge = Edge(newV1, newV2, self.weight, self.graphXDim, self.graphYDim)
        return newEdge
    
    def translateX(self, xAmount):
        new_x1 = self.v1.getCoordinate()[0]+xAmount
        new_x2 = self.v2.getCoordinate()[0]+xAmount
        newV1 = Vertex(new_x1, self.v1.getCoordinate()[1], self.graphXDim, self.graphYDim)
        newV2 = Vertex(new_x2, self.v2.getCoordinate()[1], self.graphXDim, self.graphYDim)
        newEdge = Edge(newV1, newV2, self.weight, self.graphXDim, self.graphYDim)
        return newEdge
    
    def reflectX(self):
        newV1 = Vertex(self.v1.getCoordinate()[0], -1*self.v1.getCoordinate()[1]+self.graphYDim, self.graphXDim, self.graphYDim)
        newV2 = Vertex(self.v2.getCoordinate()[0], -1*self.v2.getCoordinate()[1]+self.graphYDim, self.graphXDim, self.graphYDim)
        newEdge = Edge(newV1, newV2, self.weight, self.graphXDim, self.graphYDim)
        return newEdge
   
    def reflectY(self):
        newV1 = Vertex(-1*self.v1.getCoordinate()[0]+self.graphXDim, self.v1.getCoordinate()[1], self.graphXDim, self.graphYDim)
        newV2 = Vertex(-1*self.v2.getCoordinate()[0]+self.graphXDim, self.v2.getCoordinate()[1], self.graphXDim, self.graphYDim)
        newEdge = Edge(newV1, newV2, self.weight, self.graphXDim, self.graphYDim)
        return newEdge

    def compareTo(self, other):
        if self.v1.getCoordinate()[0] < other.v1.getCoordinate()[0] or self.v1.getCoordinate()[1] < other.v1.getCoordinate()[1]:
            return -1
        else:
            return 1
    def distFromOrigin(self):
        return self.v1.xCoord + self.v1.yCoord+1
    
    def __str__(self):
        list = (self.edgeCoordinates[0], self.edgeCoordinates[1], self.weight)
        return list.__str__()
    
    def __eq__(self, other):
        return self.getCoordinate() == other.getCoordinate()
    
# Graph Class
# -------
# The main class that will help implement the MSN Algorithm.

class Graph:
    import util
    import array
    def __init__(self, allVertices, allEdges, graphXDim, graphYDim, n):
        import math
        self.n = n
        self.vertexEdgeMatrix = dict()
        self.allVertices = allVertices
        self.vertexCounter = util.Counter()
        self.allEdges = util.Counter()
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim
        self.length = 0
        self.edgeArray = []
        for x in range(graphXDim*(graphYDim+1) + graphYDim*(graphXDim+1)):
            self.edgeArray.append(0)
        self.unweighted_a = 0
        self.unweighted_b = 0
        self.a = 0
        self.b = 0
        self.c = 0
        self.isXFull = True
        self.isYFull = True
        vertXCoords = set()
        vertYCoords = set()
        for vert in allVertices:
            vertXCoords.add(vert[0])
            vertYCoords.add(vert[1])
        for i in range(graphXDim+1):
            if i not in vertXCoords:
                self.isXFull = False
                break
        for j in range(graphYDim+1):
            if j not in vertYCoords:
                self.isYFull = False
                break
        self.score = 10*len(allEdges)
        for edge in allEdges:
            theEdge = allEdges[edge]
            if theEdge.weight == self.graphYDim+1:
                self.score += theEdge.weight*0.1
            if theEdge.weight == (self.graphYDim+1)//2 or theEdge.weight == (self.graphYDim+2)//2:
                self.score += theEdge.weight*0.9
            if theEdge.weight == 1 or theEdge.weight == self.graphYDim+1:
                self.score += theEdge.weight*0.5
            if isinstance(theEdge,DiagramEdge):
                newEdge = DiagramEdge(theEdge.v1, theEdge.v2, graphXDim, graphYDim, theEdge.level)
            else:
                newEdge = Edge(theEdge.v1, theEdge.v2, theEdge.weight, graphXDim, graphYDim)
            self.allEdges[newEdge.getCoordinate()] = newEdge
            self.vertexCounter[newEdge.v1.getCoordinate()] += 1
            self.vertexCounter[newEdge.v2.getCoordinate()] += 1
            if theEdge.isLegalEdge():
                if theEdge.v1.getCoordinate() in self.vertexEdgeMatrix:
                    self.vertexEdgeMatrix[theEdge.v1.getCoordinate()].append(theEdge)
                else:
                    self.vertexEdgeMatrix[theEdge.v1.getCoordinate()] = [theEdge]
                if theEdge.v2.getCoordinate() in self.vertexEdgeMatrix:
                    self.vertexEdgeMatrix[theEdge.v2.getCoordinate()].append(theEdge)
                else:
                    self.vertexEdgeMatrix[theEdge.v2.getCoordinate()] = [theEdge]
                if theEdge.orientation == '_':
                    self.unweighted_a += 1
                    self.a += theEdge.weight
                    i = edge[0][1]+edge[0][0]*(graphYDim+1)
                elif theEdge.orientation == '|':
                    self.unweighted_b += 1
                    self.b += theEdge.weight
                    i = edge[0][1]+edge[0][0]*(graphYDim)+graphXDim*(graphYDim+1)
                self.edgeArray[i] = allEdges[edge].weight

            self.length += theEdge.weight
            
        self.c = n - self.a - self.b
        hashValue = 0
        
        s = ""
        for i in range(len(self.edgeArray)):
            s += str(self.edgeArray[i])
        self.hashValue= s.__hash__()

    def isLegalVertex(self, vertex):
        return vertex.xCoord >= 0 and vertex.xCoord <= self.graphXDim and vertex.yCoord >= 0 and vertex.yCoord <= self.graphYDim
    
    def getLegalNeighborVertex(self, vertex):
        newVertex1 = Vertex(vertex.xCoord+1, vertex.yCoord, self.graphXDim, self.graphYDim)
        newVertex2 = Vertex(vertex.xCoord-1, vertex.yCoord, self.graphXDim, self.graphYDim)
        newVertex3 = Vertex(vertex.xCoord, vertex.yCoord+1, self.graphXDim, self.graphYDim)
        newVertex4 = Vertex(vertex.xCoord, vertex.yCoord-1, self.graphXDim, self.graphYDim)
        listOfNeighbors = [newVertex1, newVertex2, newVertex3, newVertex4]
        listOfLegalNeghbors = []
        for vertex in listOfNeighbors:
            if self.isLegalVertex(vertex):
                listOfLegalNeghbors.append(vertex)
        return listOfLegalNeghbors
    
    #checks if this graph is connected
    #def isConnected(self):
        
    
    #Adds a Vertex to the graph
    def addVertex(self,vertex):
        if self.isLegalVertex(vertex):
            self.allVertices[vertex.getCoordinate()] = vertex
    
    #Given an edge, add it:
    def addEdge(self, edge):
        return addEdge(self, edge.v1, edge.v2)
    
    def imm_addEdge(self, edge):
        if edge.isLegalEdge():  
            if edge.getCoordinate() not in self.allEdges:
                self.allVertices[edge.v2.getCoordinate()] = edge.v2
                if edge.v1.getCoordinate() not in self.allVertices:
                    self.allVertices[edge.v1.getCoordinate()] = edge.v1
                self.allEdges[edge.getCoordinate()] = edge

    #Given two vertices, add an edge to the graph, unless it is an illegal edge
    def addEdge(self, vertex1, vertex2):
        edge = Edge(vertex1, vertex2, 1, self.graphXDim, self.graphYDim)
        newAllEdges = self.allEdges.copy()
        newAllVertices = self.allVertices.copy()
        if edge.isLegalEdge():  
            if edge.getCoordinate() not in newAllEdges:
                newAllVertices[vertex2.getCoordinate()] = vertex2
                if vertex1.getCoordinate() not in newAllVertices:
                    newAllVertices[vertex1.getCoordinate()] = vertex1
                newAllEdges[edge.getCoordinate()] = edge
            else:
                repEdge = Edge(vertex1, vertex2, newAllEdges[edge.getCoordinate()].weight+1, self.graphXDim, self.graphYDim)
                newAllEdges[repEdge.getCoordinate()] = repEdge
        newGraph = Graph(newAllVertices, newAllEdges, self.graphXDim, self.graphYDim, self.n)
        return newGraph

    def hasEdge(self, vertex1, vertex2):
        edgeCoord1 = (vertex1.getCoordinate(), vertex2.getCoordinate())
        edgeCoord2 = (vertex2.getCoordinate(), vertex1.getCoordinate())
        return edgeCoord1 in self.allEdges or edgeCoord2 in self.allEdges
   
    def isLegalGraph(self):
        legal = True
        for edge in self.allEdges:
            if not self.allEdges[edge].isLegalEdge():
                legal = False
        return legal
    
    def sortEdge(self):
        sortedKey = self.allEdges.sortedKeys()
        return sortedKey
    
    def rotateGraph(self, degree):
        import util
        newEdges = util.Counter()
        for edge in self.allEdges:
            newEdge = self.allEdges[edge].rotateEdge(degree)
            newEdges[newEdge.getCoordinate()] = newEdge
        newGraph = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim, self.n)
        newGraph=newGraph.refitGraph()
        
        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None
    
    def reflectXGraph(self):
        import util
        newEdges = util.Counter()
        newVertex = util.Counter()
        for edge in self.allEdges:
            newEdge = self.allEdges[edge].reflectX()
            newEdges[newEdge.getCoordinate()] = newEdge
            newVertex[newEdge.v1.getCoordinate()] = newEdge.v1
            newVertex[newEdge.v2.getCoordinate()] = newEdge.v2
        newGraph = Graph(newVertex, newEdges, self.graphXDim, self.graphYDim, self.n)
        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None

    def reflectYGraph(self):
        import util
        newEdges = util.Counter()
        newVertex = util.Counter()
        for edge in self.allEdges:
            newEdge = self.allEdges[edge].reflectY()
            newEdges[newEdge.getCoordinate()] = newEdge
            newVertex[newEdge.v1.getCoordinate()] = newEdge.v1
            newVertex[newEdge.v2.getCoordinate()] = newEdge.v2
        newGraph = Graph(newVertex, newEdges, self.graphXDim, self.graphYDim, self.n)

        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None

    def translateYGraph(self, val):
        import util
        newEdges = util.Counter()
        for edge in self.allEdges:
            newEdge = self.allEdges[edge].translateY(val)
            newEdges[newEdge.getCoordinate()] = newEdge
        newlyMade = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim, self.n)
        newGraph=newlyMade.refitGraph()
        #newGraph = Graph(newlyMade.allVertices, newlyMade.allEdges, self.graphXDim, self.graphYDim, self.n)

        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None

    def translateXGraph(self, val):
        import util
        newEdges = util.Counter()
        for edge in self.allEdges:
            newEdge = self.allEdges[edge].translateX(val)
            newEdges[newEdge.getCoordinate()] = newEdge
        newlyMade = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim, self.n)
        newGraph=newlyMade.refitGraph()
        #newGraph = Graph(newlyMade.allVertices, newlyMade.allEdges, self.graphXDim, self.graphYDim, self.n)
        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None

    def reduceGraph(self):
        import util
        minEdge = self.allVertices.findMinMax()
        newEdges = util.Counter()
        newVertices = util.Counter()
        newXDim =minEdge[2]-minEdge[0]
        if newXDim == 0:
            newXDim = 1
        newYDim =minEdge[3]-minEdge[1]
        if newYDim == 0:
            newYDim = 1
        for edge in self.allEdges:
            newVertex1 = Vertex(edge[0][0] - minEdge[0], edge[0][1] - minEdge[1], newXDim, newYDim)
            newVertex2 = Vertex(edge[1][0] - minEdge[0], edge[1][1] - minEdge[1], newXDim, newYDim)
            newEdge = Edge(newVertex1, newVertex2, self.allEdges[edge].weight, newXDim, newYDim)
            newVertices[newVertex1.getCoordinate()] = newVertex1
            newVertices[newVertex2.getCoordinate()] = newVertex2
            newEdges[newEdge.getCoordinate()] = newEdge
        newGraph = Graph(newVertices, newEdges, newXDim, newYDim, self.n)
        return newGraph
                
    def refitGraph(self):
        import util
        disFromOriginX = 0
        disFromOriginY = 0
        minEdge = self.allEdges.findMinXandMinY()
        if minEdge[0] < 0:
            disFromOriginX = -1*minEdge[0]
        if minEdge[1] < 0:
            disFromOriginY = -1*minEdge[1]
        newEdges = util.Counter()
        newVertices = util.Counter()
        for edge in self.allEdges:
            newVertex1 = Vertex(edge[0][0] + disFromOriginX, edge[0][1] + disFromOriginY, self.graphXDim, self.graphYDim)
            newVertex2 = Vertex(edge[1][0] + disFromOriginX, edge[1][1] + disFromOriginY, self.graphXDim, self.graphYDim)
            newEdge = Edge(newVertex1, newVertex2, self.allEdges[edge].weight, self.graphXDim, self.graphYDim)
            newVertices[newVertex1.getCoordinate()] = newVertex1
            newVertices[newVertex2.getCoordinate()] = newVertex2
            newEdges[newEdge.getCoordinate()] = newEdge
        newGraph = Graph(newVertices, newEdges, self.graphXDim, self.graphYDim, self.n)
        return newGraph
        """
        self.allEdges = newEdges
        self.allVertices = newVertices
        self.edgeArray = []
        for x in range(self.graphXDim*(self.graphYDim+1) + self.graphYDim*(self.graphXDim+1)):
            self.edgeArray.append(0)
        for edge in self.allEdges:
            theEdge = self.allEdges[edge]
            if theEdge.isLegalEdge():
                if theEdge.orientation == '_':
                    i = edge[0][1]+edge[0][0]*(self.graphYDim+1)
                elif theEdge.orientation == '|':
                    i = edge[0][1]+edge[0][0]*(self.graphYDim)+self.graphXDim*(self.graphYDim+1)
                self.edgeArray[i] = self.allEdges[edge].weight"""
                
    
    def generateEqClassY(self):
        maxHash = self.__hash__()
        maxGraph = self
        setOfGraphs = set()
        setOfGraphs.add(self)
        listOfGraphs = []
        #self.toPrint()
        newGraph = self.rotateGraph(180)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
            listOfGraphs.append(newGraph)
        for graph in listOfGraphs:
            newGraph = graph.reflectXGraph()
            if newGraph is not None:
                #newGraph.toPrint()
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
                setOfGraphs.add(newGraph)
        for graph in listOfGraphs:
            newGraph = graph.reflectYGraph()
            if newGraph is not None:
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
                setOfGraphs.add(newGraph)
        return (maxGraph, setOfGraphs)

    def generateEqClassX(self):
        maxHash = self.__hash__()
        maxGraph = self
        setOfGraphs = set()
        setOfGraphs.add(self)
        listOfGraphs = []
        newGraph = self.rotateGraph(180)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(90)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(270)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newSet = set()
        listOfGraphs = list(setOfGraphs)
        for graph in listOfGraphs:
            newGraph = graph.reflectXGraph()
            if newGraph is not None:
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
        for graph in listOfGraphs:
            newGraph = graph.reflectYGraph()
            if newGraph is not None:
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
                setOfGraphs.add(newGraph)
        return (maxGraph, setOfGraphs)

    
    #returns a list of equivalence classes
    def generateEqClass(self):
        maxHash = self.__hash__()
        maxGraph = self
        setOfGraphs = set()
        setOfGraphs.add(self)
        listOfGraphs = []
        newGraph = self.rotateGraph(180)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(90)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(270)
        if newGraph is not None:
            tempHash = newGraph.__hash__()
            if tempHash > maxHash:
                maxHash = tempHash
                maxGraph = newGraph
            setOfGraphs.add(newGraph)
        newSet = set()
        listOfGraphs = list(setOfGraphs)
        for graph in listOfGraphs:
            newGraph = graph.reflectXGraph()
            if newGraph is not None:
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
                setOfGraphs.add(newGraph)
        for graph in listOfGraphs:
            newGraph = graph.reflectYGraph()
            if newGraph is not None:
                tempHash = newGraph.__hash__()
                if tempHash > maxHash:
                    maxHash = tempHash
                    maxGraph = newGraph
                setOfGraphs.add(newGraph)
        return (maxGraph, setOfGraphs)
        
    def generateAllEqClass(self):
        listOfGraphs = set()
        listOfGraphs.add(self)
        #print 'self'
        #self.toPrint()
        newGraph = self.rotateGraph(180)
        if newGraph is not None:
            listOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(90)
        if newGraph is not None:
            listOfGraphs.add(newGraph)
        newGraph = self.rotateGraph(270)
        if newGraph is not None:
            listOfGraphs.add(newGraph)
        newSet = set()
        for graph in listOfGraphs:
            newGraph = graph.reflectXGraph()
            if newGraph is not None:
                newSet.add(newGraph)
                #print 'reflectX'
                #newGraph.toPrint()
                #graph.toPrint()
            newSet.add(graph)
        listOfGraphs = newSet
        newSet = set()
        for graph in listOfGraphs:
            newGraph = graph.reflectYGraph()
            if newGraph is not None:
                newSet.add(newGraph)
            newSet.add(graph)
        listOfGraphs = newSet
        newSet = set()
        for graph in listOfGraphs:
            for x in range(self.graphXDim):
                newGraph = graph.translateXGraph(x+1)
                newGraph2 = graph.translateXGraph(-x-1)
                if newGraph is not None:
                    newSet.add(newGraph)
                if newGraph2 is not None:
                    newSet.add(newGraph2)
            newSet.add(graph)
        listOfGraphs = newSet
        newSet = set()
        for graph in listOfGraphs:
            for y in range(self.graphYDim):
                newGraph = graph.translateYGraph(y+1)
                newGraph2 = graph.translateYGraph(-y-1)
                if newGraph is not None:
                    newSet.add(newGraph)
                if newGraph2 is not None:
                    newSet.add(newGraph2)
            newSet.add(graph)
        listOfGraphs = newSet
        newSet = set()
        return listOfGraphs
    
    def printEdges(self):
        s = ""
        for edge in self.allEdges.values():
            s += edge.__str__()
        return s
    
    
    def __hash__(self):
        return self.hashValue
    
    def __eq__(self, other):
        if self.hashValue != other.hashValue:
            return False
        else:
            for edge in self.allEdges:
                if edge not in other.allEdges:
                    return False
            return True
    
    #Time to implement WEIGHTED graphs
    #Returns the valency of a vertex
    def getValence(self, vertex):
        if vertex.getCoordinate() not in self.allVertices:
            return -1
        else:
            totalWeight = 0
            for edge in self.vertexEdgeMatrix[vertex.getCoordinate()]:
                totalWeight += edge.weight
            return totalWeight
                
    def isLegalWeightedGraph(self):
        isLegal = True
        # a, b, and c must be even
        if self.a % 2 == 1 or self.b % 2 == 1 or self.c % 2 == 1:
            isLegal = False
        # a, b, and c all must be greater than 4
        if 4 > self.a or 4 > self.b or 4 > self.c:
            isLegal = False
        # a, b, and c must add up to the total step number
        if not self.a + self.b + self.c == self.n:
            isLegal = False
        # proposition 3 of paper; if n > 6, then a and b must be greater than c
        if self.a > self.c or self.a > self.b:
            isLegal = False
        # valency of each vertex must be even
        for vertex in self.allVertices:
            if self.getValence(self.allVertices[vertex])%2 == 1:
                isLegal = False
        return isLegal
        
    #helper method for Step 1 that neglects reducible graphs and graphs whose number of cycles can be increased by a zero move
    #Proposition 2 under Theorem 1 in the paper
    def isReducible(self, slabNum):
        isReducible = False
        for edge in self.allEdges:
            theEdge = self.allEdges[edge]
            val1 = self.getValence(theEdge.v1)
            val2 = self.getValence(theEdge.v2)
            if (2*theEdge.weight > val1 and 2*theEdge.weight >= val2) or (2*theEdge.weight >= val1 and 2*theEdge.weight > val2) or (4*theEdge.weight > val1+val2):
                isReducible = True
            if val1 > 2*(slabNum+1) or val2 > 2*(slabNum+1):
                isReducible = True
            if (self.vertexCounter[theEdge.v1.getCoordinate()] == 1 or self.vertexCounter[theEdge.v2.getCoordinate()] == 1) and theEdge.weight == (slabNum+1 - ((slabNum+1)%2)):
                isReducible = True
            #if (self.vertexCounter[theEdge.v1.getCoordinate()] == 1 or self.vertexCounter[theEdge.v2.getCoordinate()] == 1) and theEdge.weight%2 == 0:
            #    isReducible = True
        return isReducible
                         
    # method that determines the number of crossings in the regular lattice projection (refer to page 11 of paper)
    #def getNumberOfCrossings(self):
        

    #print method for visual purposes: see how graph looks like
    def toPrint(self):
        i = 2*self.graphYDim
        print
        while i >= 0:
            s = ""
            j = 0
            while j<= self.graphXDim:
                if i % 2 == 0:
                    if (j, i/2) in self.allVertices:
                        s += 'x'
                    elif (j, i/2) not in self.allVertices:
                        s += '.'
                    if ((j, i/2), (j+1, i/2)) in self.allEdges:
                        s += '-' + str(self.allEdges[((j, i/2), (j+1, i/2))].weight) + '-'
                    else:
                        s += '   '
                else:
                    if ((j, i/2), (j, i/2+1)) in self.allEdges:
                        s += str(self.allEdges[((j, i/2), (j, i/2+1))].weight) + ' '
                    else:
                        s += '  '
                    s += '  '
                j += 1
            i -= 1
                
            print s
        print


# Knot Diagram
# ------------

        
#subclass of the Edge class that now has weight of 1 and a new parameter, level
class DiagramEdge(Edge):
    def __init__(self, vertex1, vertex2, graphXDim, graphYDim, level):
        Edge.__init__(self, vertex1, vertex2, 1, graphXDim, graphYDim)
        self.level = level
      
    #overridden methods specific for DiagramEdges
    def compareTo(self, other):
        if self.v1.getCoordinate()[0] < other.v1.getCoordinate()[0] or self.v1.getCoordinate()[1] < other.v1.getCoordinate()[1] or self.level is not other.level:
            return -1
        else:
            return 1
    
    def getCoordinate(self):
        return (self.v1.getCoordinate(), self.v2.getCoordinate(), self.level)
        
    def getVertices(self):
        zCoord = self.level
        v1 = ThreeDVertex(self.v1.xCoord, self.v1.yCoord, zCoord, self.graphXDim, self.graphYDim)
        v2 = ThreeDVertex(self.v2.xCoord, self.v2.yCoord, zCoord, self.graphXDim, self.graphYDim)
        return (v1, v2)
        
        
    def __str__(self):
        list = (self.edgeCoordinates[0].__str__(), self.edgeCoordinates[1].__str__(), self.orientation, self.level)
        return list.__str__()
    
    def __eq__(self, other):
        return self.getCoordinate() == other.getCoordinate() and self.level == other.level

#class KnotDiagramSubpart(Graph):
#subclass of the Graph class that now consists of DiagramEdges not regular Edges
class KnotDiagram(Graph):
    def __init__(self, allVertices, allDiagramEdges, graphXDim, graphYDim, n):
        Graph.__init__(self, allVertices, util.Counter(), graphXDim, graphYDim, n)
        self.allEdges = allDiagramEdges
        self.vertexCounter = util.Counter()
        self.vertexEdgeMatrix1 = util.Counter()
        for theEdge in allDiagramEdges.values():
            self.vertexCounter[(theEdge.v1.getCoordinate(), theEdge.level)] += 1
            self.vertexCounter[(theEdge.v2.getCoordinate(), theEdge.level)] += 1
            if self.vertexEdgeMatrix1[theEdge.v1.getCoordinate()] == 0:
                self.vertexEdgeMatrix1[theEdge.v1.getCoordinate()] = [theEdge.getCoordinate()]
            else:
                self.vertexEdgeMatrix1[theEdge.v1.getCoordinate()].append(theEdge.getCoordinate())
            if self.vertexEdgeMatrix1[theEdge.v2.getCoordinate()] == 0:
                self.vertexEdgeMatrix1[theEdge.v2.getCoordinate()] = [theEdge.getCoordinate()]
            else:
                self.vertexEdgeMatrix1[theEdge.v2.getCoordinate()].append(theEdge.getCoordinate())
        self.tooMany = False
        self.illegal = False
        self.valency1Vertices = util.Counter()
        self.ySteps = util.Counter()
        self.illegalVert = None
        for vert in self.vertexCounter:
            if self.vertexCounter[vert] > 2:
                self.illegal = True
                break
            if self.vertexCounter[vert] == 1:
                if self.valency1Vertices[vert[0]] == 0:
                    self.valency1Vertices[vert[0]] = [vert[1]]
                else:
                    self.valency1Vertices[vert[0]].append(vert[1])
        if self.illegal:
            return
        for valency1 in self.valency1Vertices:
            value = self.valency1Vertices[valency1]
            if len(value)%2 == 1:
                self.illegal = True
                self.illegalVert = valency1
                break
            else:
                value.sort()
                i = 0
                while i < len(value)-1:
                    for betwn in range(value[i+1]-value[i]-1):
                        if self.vertexCounter[(valency1, betwn+1+value[i])] >= 1:
                            self.illegal = True
                            self.illegalVert = valency1
                    if self.illegal:
                        break
                    if self.ySteps[valency1] == 0:
                        self.ySteps[valency1] = [(value[i], value[i+1])]
                    else:
                        self.ySteps[valency1].append((value[i], value[i+1]))
                    i += 2
        
    #checks if there is an illegal pattern of open vertices not at the conjunction
    def checkIllegalLoneVertices(self, conjunction):
        conjVerts = conjunction.getCoordinate()
        for valence1 in self.valency1Vertices:
            if valence1 not in conjVerts:
                if len(self.valency1Vertices[valence1]) % 2 != 0:
                    return self.vertexEdgeMatrix1[valence1]
    #edge is the current edge we are at
    #vertex is the vertex we are expanding onto
    def getConnectedEdge(self, edge, vertex, edgeList):
        vCoord = vertex
        eCoord = edge.getCoordinate()
        if not (vCoord == eCoord[0] or vCoord == eCoord[1]):
            return []
        sameLevelConnectedEdges = []
        awayEdges=[]
        for edgeKey in edgeList:
            theEdge = self.allEdges[edgeKey]
            # make sure the edge we're looking at has the same vertex
            if (vCoord == edgeKey[0] or vCoord == edgeKey[1]):
                # if same level, then add to same level list
                if theEdge == edge:
                    continue
                if  eCoord[2] == edgeKey[2]:
                    sameLevelConnectedEdges.append(self.allEdges[edgeKey])
        if len(sameLevelConnectedEdges) == 0:
            levelOfFar = self.valency1Vertices[vCoord]
            try:
                ind = levelOfFar.index(eCoord[2])
                if self.ySteps[vCoord]:
                    awayEdges.append(self.ySteps[vCoord][ind/2])
            except ValueError:
                True
            except AttributeError:
                True
                        
        return (sameLevelConnectedEdges, awayEdges)
    
    #return neighbor edges 
    def getNeighborEdge(self, edge):
        coords = edge.getCoordinate()
        if edge.orientation == '|':
            neighborCoord1 = ((coords[0][0]+1, coords[0][1]), (coords[1][0]+1, coords[1][1]), coords[2])
            neighborCoord2 = ((coords[0][0]-1, coords[0][1]), (coords[1][0]-1, coords[1][1]), coords[2])
        else:
            neighborCoord1 = ((coords[0][0], coords[0][1]+1), (coords[1][0], coords[1][1]+1), coords[2])
            neighborCoord2 = ((coords[0][0], coords[0][1]-1), (coords[1][0], coords[1][1]-1), coords[2])
        neighborCoord3 = ((coords[0][0], coords[0][1]), (coords[1][0], coords[1][1]), coords[2]+1)
        neighborCoord4 = ((coords[0][0], coords[0][1]), (coords[1][0], coords[1][1]), coords[2]-1)
        neighbors = (neighborCoord1, neighborCoord2,neighborCoord3,neighborCoord4)  
        keys = self.allEdges.keys()
        output= []
        for neighborEdge in neighbors:
            if neighborEdge in keys:
                output.append(neighborEdge)
        return output
    
    #helper method to see if the final result is knot, i.e. first vertex is connected to the final vertex traversed
    def connected(self, v1, v2):
        return (v1[0] == v2[0] and v1[1] == v2[1] and abs(v1[2]-v2[2]) > 0) or (v1[0] == v2[0] and v1[2] == v2[2] and abs(v1[1]-v2[1]) == 1) or (v1[2] == v2[2] and v1[1] == v2[1] and abs(v1[0]-v2[0]) == 1) 
    #returns new Knot Diagram with the added Edge
    def addEdge(self, knotEdge):
        newAllEdges = self.allEdges.copy()
        newAllVertices = self.allVertices.copy()
        
        if knotEdge.getCoordinate() not in self.allEdges:
            newAllEdges[knotEdge.getCoordinate()] = knotEdge
            if knotEdge.v1.getCoordinate() not in newAllVertices:
                newAllVertices[knotEdge.v1.getCoordinate()] = knotEdge.v1
            if knotEdge.v2.getCoordinate() not in newAllVertices:
                newAllVertices[knotEdge.v2.getCoordinate()] = knotEdge.v2
        newKnotDiag = KnotDiagram(self.allVertices, newAllEdges, self.graphXDim, self.graphYDim, self.n)
        return newKnotDiag
    
    #check if a diagram is minus two reducible
    def checkMinusTwoReducible(self, conjunction):
        all_edges = self.allEdges.keys()
        for edge in all_edges:
            neighbors = self.getNeighborEdge(self.allEdges[edge])
            for neighbor in neighbors:
                if neighbor[2] == edge[2]:
                    edge1 = ((neighbor[0][0], neighbor[0][1]), (edge[0][0], edge[0][1]), neighbor[2])
                    edge2 = ((neighbor[1][0], neighbor[1][1]), (edge[1][0], edge[1][1]), neighbor[2])
                    if edge1 in all_edges:
                        return (edge, neighbor, edge1)
                    elif edge2 in all_edges:
                        return (edge, neighbor, edge2)
                else:
                    if neighbor in all_edges:
                        conjVert = 0
                        if conjunction is None:
                            conj_two_verts = []
                        else:
                            conj_two_verts = conjunction.getCoordinate()[:2]
                        non_conj_ind = []
                        if edge[0] in conj_two_verts:
                            conjVert += 1
                            non_conj_ind = [1]
                        if edge[1] in conj_two_verts:
                            conjVert += 1
                            non_conj_ind = [0]
                        if conjVert == 2:
                            continue
                        else:
                            if conjVert == 0:
                                non_conj_ind = [0, 1]
                            for checking_ind in non_conj_ind:
                                if edge[checking_ind] in self.ySteps.keys():
                                    graphHeights = self.ySteps[edge[checking_ind]]
                                else:
                                    continue
                                #print neighbor
                                heights = [edge[2], neighbor[2]]
                                heights.sort()
                            
                                if tuple(heights) in graphHeights:
                                    #print self.vertexEdgeMatrix[edge[conjVert]]
                                    return self.vertexEdgeMatrix1[edge[checking_ind]]
        return ()
        
    #returns the list of Vertices in traversed order
    def getPath(self):
        allEdgeKeys = self.allEdges.keys()
        pathSet = set()
        path = []
        currEdge = None
        for edge in allEdgeKeys:
            if edge[2] == 0:
                currEdge = edge
                allEdgeKeys.remove(edge)
                break
        if currEdge is None:
            currEdge = allEdgeKeys.pop()
        fromVertex = (currEdge[0][0], currEdge[0][1])
        vert = (fromVertex[0], fromVertex[1], currEdge[2])
        path.append(vert)
        pathSet.add(vert)
        ontoVertex = (currEdge[1][0], currEdge[1][1])
        while len(allEdgeKeys) != 0:
            vert = (ontoVertex[0], ontoVertex[1], currEdge[2])
            if vert not in pathSet:
                pathSet.add(vert)
                path.append(vert)
            else:
                return 0
            connectedEdges = self.getConnectedEdge(self.allEdges[currEdge], ontoVertex, allEdgeKeys)
            #check if connection on the SAME LEVEL
            if len(connectedEdges[0]) > 0:
                currEdge = connectedEdges[0][0].getCoordinate()
                allEdgeKeys.remove(currEdge)
                if ontoVertex == currEdge[0]:
                    ontoVertex = currEdge[1]
                else:
                    ontoVertex = currEdge[0]
            #check if not, if we can go UP or NOT
            elif len(connectedEdges[1]) > 0:
                ySteps = None
                #print connectedEdges[1]
                for possibleConnections in connectedEdges[1]:
                    if currEdge[2] in possibleConnections:
                        ySteps = possibleConnections
                        break
                if ySteps is not None:
                    level = currEdge[2]
                    level_ind = ySteps.index(level)
                    goal = ySteps[(level_ind+1)%2]
                    while abs(level - goal) > 0:
                        if level > goal:
                            level -= 1
                        if level < goal:
                            level += 1
                        vert = (ontoVertex[0], ontoVertex[1], level)
                        if vert not in pathSet:
                            pathSet.add(vert)
                            path.append(vert)
                        else:
                            return 0
                    for edge in allEdgeKeys:
                        if edge[2] == goal:
                            if edge[0] == ontoVertex or edge[1] == ontoVertex:
                                currEdge = edge
                                break
                allEdgeKeys.remove(currEdge)
                if ontoVertex == currEdge[0]:
                    ontoVertex = currEdge[1]
                else:
                    ontoVertex = currEdge[0]
        vert = (ontoVertex[0], ontoVertex[1], currEdge[2])
        #print "vert "+str(vert)+"path0 "+ str(path[0]) 
        #vert is the final vertex. We must finalize the polygon by connecting it to first vertex
        if vert == path[0]:
           # print "they equal"
            return path
        """
        if self.connected(path[0], vert):
            if vert[2] == path[0][2] or abs(vert[2]-path[0][2]) ==1:
                if vert not in pathSet:
                    pathSet.add(vert)
                    path.append(vert)
            else:
                distance = vert[2] - path[0][2]
                if distance < 0:
                    for gogogo in range(abs(distance)):
                        newV = (vert[0], vert[1], vert[2]+gogogo)
                        if vert not in pathSet:
                            pathSet.add(newV)
                            path.append(newV)
                else:
                    for gogogogo in range(abs(distance)):
                        newV = (vert[0], vert[1], vert[2]-gogogogo)
                        if newV not in pathSet:
                            pathSet.add(newV)
                            path.append(newV)
            return path
        else:
            return 0
        """
    #printing method
    def toPrint(self):
        levels = ("d","u")
        i = 2*self.graphYDim
        j = 0
        print
        while i >= 0:
            s = ""
            j = 0
            if i % 2 == 0:
                for k in range(2):
                    while j<= self.graphXDim:
                        if (j, i/2) in self.allVertices:
                            s += 'x x'
                        elif (j, i/2) not in self.allVertices:
                            s += '. .'
                        if ((j, i/2), (j+1, i/2), k) in self.allEdges:
                            s += ' - ' + levels[k] + ' - '
                        else:
                            s+= '       '
                        j += 1
                    j = 0
                    print s
                    s = ''
                    
            else:
                for k in range(3):
                    while j <= self.graphXDim:
                        if ((j, i/2), (j, i/2+1),1) in self.allEdges:
                            if k == 1:
                                s += levels[1] + ' '
                            else:
                                s += "|" + ' '
                        else:
                            s += '  '
                        if ((j, i/2), (j, i/2+1),0) in self.allEdges:
                            if k == 1:
                                s += levels[0] + ' '
                            else:
                                s+="|" + ' '
                        else:
                            s += '  '
                        s += '     '
                        j += 1
                    print s
                    s = ''
                    j = 0
            i -= 1
        print
        print
        
        
    def Projection(self):
        projected = Graph(util.Counter(), util.Counter(), self.graphXDim, self.graphYDim, self.n)
        for edge in self.allEdges.values():
            projected = projected.addEdge(edge.v1, edge.v2)
        return projected
