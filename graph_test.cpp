#include <iostream>
using namespace std;

class Vertex {
    //    #constructor, takes in an x coordinate, y coordinate, and the dimensions of the graph that this vertex belongs to
  public:
    //int coordinate[2];
    int xCoord;
    int yCoord;
    int graphXDim;
    int graphYDim;
// set value for coordinate
    Vertex();
    ~Vertex();
/*returns the coordinates, (x coordinate, y coordinate) of this vertex*/
    //int * getCoordinated(){ return coodinate;}//return an array

    void _init_(int x,int y, int graphx, int graphy );
// to string method that prints the coordinates
    string _str_() { 
        string returnstring = "";
        returnstring+= xCoord+'0'; returnstring+= yCoord+'0';
        return returnstring;
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
        if (xCoord == other.xCoord & yCoord == other.yCoord)
             return true;
        else
             return false;
    }
}; //Vertex
Vertex :: Vertex(void) {}

void Vertex :: _init_(int x,int y, int graphx, int graphy ){

        xCoord = x;
        yCoord = y;
        graphXDim = graphx;
        graphYDim = graphy;
    }

Vertex :: ~Vertex(void) {}

class Edge 
{//    # Orient the vertices so that an edge has a left to right orientation or bottom to up orientation
  public:
    int weight;
    int graphXDim;
    int graphYDim;
    Vertex v1;
    Vertex v2;
// constructor and de~~~
    Edge (void) {}
    ~Edge (void) {}
// initialize edges
    void _init_ (Vertex vert1, Vertex vert2, int weight, int graphx, int graphy);};//Edge

void Edge ::_init_ (Vertex vert1, Vertex vert2, int weight, int graphx, int graphy){
         v1 = vert1; 
         v2 = vert2; 
         weight = weight;
         graphXDim = graphx;
         graphYDim =  graphy; 

     int * substractVertex = vert2.substract(vert2);
     
     }//initial

int main ()
{
    Vertex V1, V2 ,V3;
    V1.xCoord = 1;
    V1.yCoord =2;
    cout<<V1.xCoord<<V1.yCoord<<endl;
    V2._init_(1,2,3,4);
    V3 = V2;
    int * v12 = V2.substract(V3);
    cout<<v12[0]<<v12[1]<<endl;
    cout<<V1._eq_(V2)<<endl;
return 0;
}




