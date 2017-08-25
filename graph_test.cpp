#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;
using std::vector; 

class Vertex {
    //    #constructor, takes in an x coordinate, y coordinate, and the dimensions of the graph that this vertex belongs to
  public:
    //int coordinate[2];
    int xCoord;
    int yCoord;
    //int graphXDim;
    ///int graphYDim;
// set value for coordinate
    Vertex();
    ~Vertex();
/*returns the coordinates, (x coordinate, y coordinate) of this vertex*/
    //int * getCoordinated(){ return coodinate;}//return an array

    void _init_(int x,int y);//, int graphx, int graphy );
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

void Vertex :: _init_(int x,int y ){

        xCoord = x;
        yCoord = y;
       // graphXDim = graphx;
       // graphYDim = graphy;
    }

Vertex :: ~Vertex(void) {}

class Edge 
{//    # Orient the vertices so that an edge has a left to right orientation or bottom to up orientation
  public:
    //int weight;
    //int graphXDim;
    //int graphYDim;
    Vertex v1;
    Vertex v2;
    int level;
// constructor and de~~~
    Edge (void) {}
    ~Edge (void) {}
// initialize edges
    void _init_ (Vertex vert1, Vertex vert2, int level);
};//Edge

void Edge ::_init_ (Vertex vert1, Vertex vert2, int level){
         v1 = vert1; 
         v2 = vert2; 
         //weight = weight;
         //graphXDim = graphx;
         //graphYDim =  graphy; 
         level = level;
     //int * substractVertex = vert2.substract(vert2);
     
     }//initial
Edge merge(Edge edge1, Edge edge2)
{
    Edge mergedEdge;
    Vertex v11,v12,v21,v22, Ve1,Ve2;
    v11 = edge1.v1;
    v12 = edge1.v2;
    v21 = edge2.v1;
    v22 = edge2.v2;
    int level = edge1.level;

    if (v11._eq_(v21) & !v12._eq_(v22))
    {
        Ve1 = v12; Ve2 = v22;
    }  else if (v11._eq_(v22) & ! v12._eq_(v21) )
    {
        Ve1 = v12; Ve2 = v21;
    }  else if (! v11._eq_(v22) & v12._eq_(v21) )
    {
        Ve1 = v11;  Ve2 = v22;
    }  else if (! v11._eq_(v21) & v12._eq_(v22))
    {
        Ve1 = v11;  Ve2 = v21;
    } else { cout << "ilegal merging"<<endl; }

    mergedEdge._init_(Ve1,Ve2, level);
    return mergedEdge;
}//merge

int main ()
{
    Vertex V1, V2 ,V3;
    V1.xCoord = 1;
    V1.yCoord =2;
    // get Vertex array
    vector < Vertex> vertices ;
    vertices.push_back(V1); 
    //vertices.pop();
    cout<<"size of vertices "<< vertices.size()<<endl;
    cout<<V1.xCoord<<V1.yCoord<<endl;
    V2._init_(1,3);
    V3._init_(2,2) ;
//    int * v12 = V2.substract(V3);
   // cout<<v12[0]<<v12[1]<<endl;
    cout<<V1._eq_(V2)<<endl;
    int level = 0;
    Edge edge1, edge2;
    edge1._init_(V1,V2,level);
    edge2._init_(V1,V3,level);
    cout<<edge1.v1.xCoord<<endl;
    Edge newE;
    newE = merge(edge1,edge2);
    // get edge array
    vector <Edge>  edges;
    //cout<<"merge E"<< newE.v1.xCoord<<newE.v1.yCoord<<endl; 
//
// testing input 
char str[255] = "[((0, 0), (0, 1), 2), ((0, 0), (1, 0), 0), ((1, 0), (1, 1), 2), ((0, 1), (1, 1), 0), ((0, 0), (1, 0), 1), ((0, 0), (0, 1), 0), ((0, 1), (1, 1), 1), ((1, 0), (1, 1), 0), ((0, 0), (0, 1), 1), ((0, 0), (1, 0), 2), ((0, 1), (1, 1), 2), ((1, 0), (1, 1), 1)]";
int i =0;
int v11,v12,v21,v22;
while (str[i]!= ']')
{ 
  if(str[i]=='(' & str[i+1] =='('){
  i += 2;
  while (str[i]<'0' | str[i]> '9') { i++;}
  v11 = str[i] -'0'; i++;
  while (str[i]<'0' | str[i]> '9') { i++;}
  v12 = str[i]-'0'; i++;
  while (str[i]<'0' | str[i]> '9') { i++;}
  v21 = str[i]-'0'; i++;
  while (str[i]<'0' | str[i]> '9') { i++;}
  v22 = str[i]- '0'; i++;
  while (str[i]<'0' | str[i]> '9') { i++;}
  level = str[i]- '0'; 
  cout<<v11<<v12<<v21<<v22<<level<<endl;
  V1._init_(v11,v12);
  V2._init_(v21,v22);
  vertices.push_back(V1);
  vertices.push_back(V2);
  Edge edge;
  edge._init_(V1,V2, level);
  edges.push_back(edge);
  }
  
  else i++;
  
}
cout<<"# edges"<< edges.size()<<endl;
//    cout<<str[0]<<endl;
   

return 0;
}




