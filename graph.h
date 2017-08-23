#include <iostream>
using namespace std;

class Vertex {
    //    #constructor, takes in an x coordinate, y coordinate, and the dimensions of the graph that this vertex belongs to

    int coordinate[2];
    int xCoord;
    int yCoord;
    int graphXDim;
    int graphYDim;
    coordinate[0]= xCoord; coordinate[1] = yCoord;
/*returns the coordinates, (x coordinate, y coordinate) of this vertex*/
    int * getCoordinated(){ return coodinate;}//return an array

// to string method that prints the coordinates
    string _str_() { 
        string returnstring = "";
        for (int i = 0; i<2;i++) {returnstring+= coordinate[i]+'0';}
    }
//substract
    int * substract(Vertex other) {
        int x = xCoord - other.xCoord;
        int y = yCoord - other.yCoord;
        int returnCoord[2];
        returnCoord[0] = x; returnCoord[1] = y;
        return returnCoord;
    }
//equal or not
    bool _eq_(Vertex other) {
        if (xCoord == other.xCoord & yCoord == other.Coord)
             return true;
        else
             return false;
    }
} 

