#Code written by Michael Jun
#copyright 2012
#Time to REALIZE IT TO THREE DIMENSIONS!
class ThreeDimVertex:
    def __init__(self, xCoord, yCoord, zCoord):
        self.xCoord = xCoord
        self.yCoord = yCoord
        self.zCoord = zCoord
        self.coordinate = (xCoord, yCoord, zCoord)
    def __str__(self):
        return str(self.coordinate)
        
    def subtract(self, other):
        x = self.xCoord - other.xCoord
        y = self.yCoord - other.yCoord
        z = self.zCoord - other.zCoord
        return (x,y,z)
    
class ThreeDimEdge:
    def __init__(self, vertex1, vertex2):
        self.v1 = vertex1
        self.v2 = vertex2
        subtractVertex = vertex1.subtract(vertex2)
        if subtractVertex[0] == 0 and subtractVertex[1] == 0:
            self.orientation = '|'
            if subtractVertex[1] < 0:
                self.v1 = vertex1
                self.v2 = vertex2
            else:
                self.v1 = vertex2
                self.v2 = vertex1

        elif subtractVertex[1] == 0 and subtractVertex[2] == 0:
            self.orientation = '_'
            if subtractVertex[0] < 0:
                self.v1 = vertex1
                self.v2 = vertex2
            else:
                self.v1 = vertex2
                self.v2 = vertex1
        elif subtractVertex[UP] == 0 and subtractVertex[2] == 0:
            self.orientation = 'UP'
            if subtractVertex[0] < 0:
                self.v1 = vertex1
                self.v2 = vertex2
            else:
                self.v1 = vertex2
                self.v2 = vertex1
        else:
            self.orientation = 'invalid'
        self.edgeCoordinates = (self.v1.getCoordinate(), self.v2.getCoordinate())
        
        
class Knots:
    import util
    import Graph
    
    def __init__(self, allVertices, allEdges, graphXDim, graphYDim, graphZDim):
        self.allVertices = allVertices
        self.allEdges = allEdges
        self.graphXDim = graphXDim
        self.graphYDim = graphYDim
        self.graphZDim = graphZDim
        
    def projectOnto(self, xyorzPlane):
        return None
    
    def __str__(self):
        for edge in allEdges:
            s += allEdges[edge].__str__()
        return s
        
        
        
        
        
        
        
        
        
        
        
        