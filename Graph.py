import util
# Vertex Class
# -------
# Primitive part of Graph that represents the Vertices that make the graph

class Vertex:
    
    def __init__(self, xCoord, yCoord, graphXDim, graphYDim):
        self.coordinate = (xCoord, yCoord)
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim

    def getCoordinate(self):
        return self.coordinate

    def getWeight(self):
        return self.weight

    def __str__(self):
        return self.coordinate.__str__()

    
    def subtract(self, other):
        x = self.xCoord - other.xCoord
        y = self.yCoord - other.yCoord
        return (x,y)

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
        #print self, self.graphYDim
        #print newEdge
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
        list = (self.edgeCoordinates[0].__str__(), self.edgeCoordinates[1].__str__(), self.orientation)
        return list.__str__()
    
    def __eq__(self, other):
        return self.getCoordinate() == other.getCoordinate()

# Graph Class
# -------
# The main class that will help implement the MSN Algorithm.

class Graph:
    import util
    import array
    def __init__(self, allVertices, allEdges, graphXDim, graphYDim):
        self.vertexEdgeMatrix = dict()
        self.allVertices = allVertices
        self.allEdges = allEdges
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim
        self.length = 0
        self.edgeArray = []
        for x in range(graphXDim*(graphYDim+1) + graphYDim*(graphXDim+1)):
            self.edgeArray.append(0)
        self.unweighted_a = 0
        self.unweighted_c = 0
        self.a = 0
        self.b = 0
        self.c = 0
        
        for edge in self.allEdges:
            theEdge = self.allEdges[edge]
            theEdge.graphXDim = graphXDim
            theEdge.graphYDim = graphYDim
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
                    self.unweighted_c += 1
                    self.c += theEdge.weight
                    i = edge[0][1]+edge[0][0]*(graphYDim+1)
                elif theEdge.orientation == '|':
                    self.unweighted_a += 1
                    self.a += theEdge.weight
                    i = edge[0][1]+edge[0][0]*(graphYDim)+graphXDim*(graphYDim+1)
                self.edgeArray[i] = self.allEdges[edge].weight

            self.length += theEdge.weight
            
        self.b = 24 - self.a - self.c
    
    
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
                
    #Adds a Vertex to the graph
    def addVertex(self,vertex):
        if self.isLegalVertex(vertex):
            self.allVertices[vertex.getCoordinate()] = vertex
    
    #Given an edge, add it:
    def addEdge(self, edge):
        return addEdge(self, edge.v1, edge.v2)
    
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
        newGraph = Graph(newAllVertices, newAllEdges, self.graphXDim, self.graphYDim)
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
        newGraph = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim)
        newGraph.refitGraph()
                
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
        newGraph = Graph(newVertex, newEdges, self.graphXDim, self.graphYDim)

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
        newGraph = Graph(newVertex, newEdges, self.graphXDim, self.graphYDim)

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
        newlyMade = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim)
        newlyMade.refitGraph()
        newGraph = Graph(newlyMade.allVertices, newlyMade.allEdges, self.graphXDim, self.graphYDim)

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
        newlyMade = Graph(self.allVertices, newEdges, self.graphXDim, self.graphYDim)
        newlyMade.refitGraph()
        newGraph = Graph(newlyMade.allVertices, newlyMade.allEdges, self.graphXDim, self.graphYDim)
        if newGraph.isLegalGraph():
            return newGraph
        else:
            return None


    def refitGraph(self):
        if self is None:
            return None
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
                self.edgeArray[i] = self.allEdges[edge].weight
                
    
    #returns a list of equivalence classes
    def generateEqClass(self):
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
    
    
    def __hash__(self):
        s = ""
        for i in range(len(self.edgeArray)):
            s += str(self.edgeArray[i])
        """
        import math
        hashValue = 0
        
        for i in range(len(self.edgeArray)):
            if not self.edgeArray[i] == 0: 
                hashValue += math.pow(10,i)*self.edgeArray[i]
        return int(hashValue)"""
        
        return s.__hash__()
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
    """
    def hasCycle(self):
        hasCycle = False
        if self.edgeArray[0] and self.edgeArray[1] and self.edgeArray[2] and self.edgeArray[7]:
            hasCycle = True
        if self.edgeArray[2] and self.edgeArray[3] and self.edgeArray[4] and self.edgeArray[8]:
            hasCycle = True
        if self.edgeArray[4] and self.edgeArray[5] and self.edgeArray[6] and self.edgeArray[9]:
            hasCycle = True
        if self.edgeArray[0] and self.edgeArray[1] and self.edgeArray[3] and self.edgeArray[4] and self.edgeArray[8] and self.edgeArray[7]:
            hasCycle = True
        if self.edgeArray[2] and self.edgeArray[3] and self.edgeArray[5] and self.edgeArray[6] and self.edgeArray[8] and self.edgeArray[9]:
            hasCycle = True
        if self.edgeArray[0] and self.edgeArray[1] and self.edgeArray[3] and self.edgeArray[5] and self.edgeArray[6] and self.edgeArray[8] and self.edgeArray[9] and self.edgeArray[7]:
            hasCycle = True
        return hasCycle

    def isTree(self):
        isTree = False
        if self.edgeArray[1] and self.edgeArray[2] and self.edgeArray[3]:
            isTree = True
        if self.edgeArray[3] and self.edgeArray[4] and self.edgeArray[5]:
            isTree = True
        if self.edgeArray[4] and self.edgeArray[9] and self.edgeArray[8]:
            isTree = True
        if self.edgeArray[2] and self.edgeArray[7] and self.edgeArray[8]:
            isTree = True
        return isTree
    """
    
    #JUST NEED TO FINISH THIS METHOD TO MAKE ALL WORK
    def expandible(self):
        return self.length < 10
        #return len(self.generateEqClass()) > 2
        #return self.unweighted_a < 1 or self.unweighted_c < 2
        #return False
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
        if self.a % 2 == 1 or self.b % 2 == 1 or self.c % 2 == 1:
            isLegal = False
        if 4 > self.a or 4 > self.b or 4 > self.c:
            isLegal = False
        if not self.a + self.b + self.c == 24:
            isLegal = False
        if self.c > self.a or self.c > self.b:
            isLegal = False
        for vertex in self.allVertices:
            if self.getValence(self.allVertices[vertex])%2 == 1:
               # print self.getValence(self.allVertices[vertex])
               # print "isdatright?"
                isLegal = False
        return isLegal
        
    #helper method for Step 1 that neglects reducible graphs and graphs whose number of cycles can be increased by a zero move
    #Proposition 2 under Theorem 1 in the paper
    def isReducible(self):
        isReducible = False
        for edge in self.allEdges:
            theEdge = self.allEdges[edge]
            val1 = self.getValence(theEdge.v1)
            val2 = self.getValence(theEdge.v2)
            if (2*theEdge.weight > val1 and 2*theEdge.weight >= val2) or (2*theEdge.weight >= val1 and 2*theEdge.weight > val2):
                isReducible = True
        return isReducible
          
        
                         
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

"""
#subclass of Vertex class which now has a z coordinate

class ThreeDVertex(Vertex):
    def __init__(self, xCoord, yCoord, zCoord, graphXDim, graphYDim):
        Vertex.__init__(self, xCoord, yCoord, graphXDim, graphYDim)
        self.zCoord = zCoord
    
    def getCoordinate(self):
        return (xCoord, yCoord, zCoord)
        
    def isLegalVertex(self):
        return super.isLegalVertex() and self.zCoord <= 1 and self.zCoord >= 0
    
    def getLegalNeighborVertex(self):
        newVertex1 = ThreeDVertex(self.xCoord+1, self.yCoord, self.zCoord, self.graphXDim, self.graphYDim)
        newVertex2 = ThreeDVertex(self.xCoord-1, self.yCoord, self.zCoord,  self.graphXDim, self.graphYDim)
        newVertex3 = ThreeDVertex(self.xCoord, self.yCoord+1, self.zCoord,  self.graphXDim, self.graphYDim)
        newVertex4 = ThreeDVertex(self.xCoord, self.yCoord-1, self.zCoord,  self.graphXDim, self.graphYDim)
        newVertex5 = ThreeDVertex(self.xCoord, self.yCoord, self.zCoord+1,  self.graphXDim, self.graphYDim)
        newVertex6 = ThreeDVertex(self.xCoord, self.yCoord, self.zCoord-1,  self.graphXDim, self.graphYDim)
        listOfNeighbors = [newVertex1, newVertex2, newVertex3, newVertex4, newVertex5, newVertex6]
        listOfLegalNeghbors = []
        for vertex in listOfNeighbors:
            if vertex.isLegalVertex():
                listOfLegalNeghbors.append(vertex)

        return listOfLegalNeghbors
        """
        
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

#subclass of the Graph class that now consists of DiagramEdges not regular Edges
class KnotDiagram(Graph):
    def __init__(self, allVertices, allDiagramEdges, graphXDim, graphYDim):
        Graph.__init__(self, allVertices, allDiagramEdges, graphXDim, graphYDim)
    
    def getConnectedEdge(self, edge, vertex, edgeList):
        vCoord = vertex
        eCoord = edge.getCoordinate()
        if not (vCoord == eCoord[0] or vCoord == eCoord[1]):
            return []
        sameLevelConnectedEdges = []
        diffLevelConnectedEdges = []
        for edgeKey in edgeList:
            if (vCoord == edgeKey[0] or vCoord == edgeKey[1]):
                if  eCoord[2] == edgeKey[2]:
                    sameLevelConnectedEdges.append(self.allEdges[edgeKey])
                elif (eCoord[2]+1)%2 == edgeKey[2]:
                    diffLevelConnectedEdges.append(self.allEdges[edgeKey])
        return (sameLevelConnectedEdges, diffLevelConnectedEdges)
    
    #helper method to see if the final result is knot, i.e. first vertex is connected to the final vertex traversed
    def connected(self, v1, v2):
        return (v1[0][0] == v2[0][0] and v1[0][1] == v2[0][1]) or (v1[0][0] == v2[0][0] and v1[1] == v2[1]) or (v1[0][1] == v2[0][1] and v1[1] == v2[1])
    
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
        
        newKnotDiag = KnotDiagram(newAllVertices, newAllEdges, self.graphXDim, self.graphYDim)
        return newKnotDiag
        
    #returns the list of Vertices in traversed order
    def getPath(self):
        if len(self.allEdges) == 0:
            return None
        else:
            c_counter = 0
            allEdgeCoordinates = self.allEdges.keys()
            outputList = []
            usedVertex = set()
            currentEdge = allEdgeCoordinates[0]
            vertex = currentEdge[0]
            firstVertex = (vertex, currentEdge[2])
            outputList.append((vertex[0], vertex[1], currentEdge[2]))
            while len(allEdgeCoordinates) != 0:
                neighborEdge = self.getConnectedEdge(self.allEdges[currentEdge], vertex, allEdgeCoordinates)
                usedVertex.add((vertex, currentEdge[2]))
                if len(neighborEdge[0]) > 1 and self.allEdges[currentEdge] not in neighborEdge[0]:
                    return 0
                elif len(neighborEdge[0]) == 0:
                    if len(neighborEdge[1]) == 0:
                        return 0
                    elif len(neighborEdge[1]) > 1:
                        return 0
                    else:
                        currentEdge = neighborEdge[1][0].getCoordinate()
                        c_counter += 1
                else:
                    currentEdge = neighborEdge[0][0].getCoordinate()
                    newVertex1 = (currentEdge[0], currentEdge[2])
                    newVertex2 = (currentEdge[1], currentEdge[2])
                    if newVertex1 not in usedVertex and newVertex2 not in usedVertex:
                        vertex = currentEdge[0]
                        usedVertex.add((vertex, currentEdge[2]))
                    elif newVertex1 in usedVertex and newVertex2 in usedVertex:
                        if len(allEdgeCoordinates) != 1:
                            return 0
                        else:
                            finalVertex = (vertex, currentEdge[2])
                            if self.connected(firstVertex, finalVertex):
                                return outputList
                            else:
                                return 0
                    else:
                        if newVertex1 in usedVertex:
                            vertex = currentEdge[1]
                        else:
                            vertex = currentEdge[0]
                        allEdgeCoordinates.remove(currentEdge)
                outputList.append((vertex[0], vertex[1], currentEdge[2]))
            finalVertex = (vertex, currentEdge[2])
            if self.connected(firstVertex,finalVertex):
                return outputList
            else:
                return 0
    

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

