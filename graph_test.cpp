#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;
using std::vector; 
#include <cmath>
#include <list>
using std::list;
#include <algorithm>  

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
/*
//substract
    int * substract(Vertex other) {
        int x = xCoord - other.xCoord;
        int y = yCoord - other.yCoord;
        int returnCoord[2];
        returnCoord[0] = x; returnCoord[1] = y;
        return returnCoord;
    }
*/
//equal or not
    bool _eq_(Vertex other) {
        if (xCoord == other.xCoord && yCoord == other.yCoord)
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
    
    Vertex v1;
    Vertex v2;
    int level;
// constructor and de~~~
    Edge (void) {}
    ~Edge (void) {}
// initialize edges
    void _init_ (Vertex vert1, Vertex vert2, int level);
    void merge(Edge &edge1, Edge edge2);
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
void Edge:: merge(Edge &edge1, Edge edge2)
{
    //Edge mergedEdge;
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

    edge1._init_(Ve1,Ve2, level);
    //return mergedEdge;
}//merge

bool canMerge(Edge edge1, Edge edge2)
{
    Vertex v11,v12,v21,v22, Ve1,Ve2;
    v11 = edge1.v1;
    v12 = edge1.v2;
    v21 = edge2.v1;
    v22 = edge2.v2;
    //int level = edge1.level;

    if (v11._eq_(v21) & !v12._eq_(v22))
    {
        return true;  
    }  else if (v11._eq_(v22) & ! v12._eq_(v21) )
    {
        return true;
    }  else if (! v11._eq_(v22) & v12._eq_(v21) )
    {
        return true;
    }  else if (! v11._eq_(v21) & v12._eq_(v22))
    {
        return true;
    } else {return false ;  }

}// canMerge

/*
//int numLevels (Edge )
void getConnEdges (Edge <vector> edges)
{
   //fist group edges by level
   vector<int>::iterator iter;
   vector<int> diffLevels;
   sort(levelList.begin(), levelList.end());
   std::cout << "level contains:"<< levelList[0];
   diffLevels.push_back(levelList[0]);
   for (iter=levelList.begin()+1; iter!=levelList.end(); ++iter)
   {
       if(*iter != *(iter-1)) {
          diffLevels.push_back(*iter);
          std::cout << ' ' << *iter;}
   }
}
*/ 

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
    cout<<"can merge ?"<<canMerge(edge1,edge2)<<endl;
    edge1.merge(edge1,edge2);
    cout<<edge1.v1.xCoord<<edge1.v1.yCoord<<edge1.v2.xCoord<<edge1.v2.yCoord <<endl;
    // get edge array
    vector <Edge>  edges;
    //cout<<"merge E"<< newE.v1.xCoord<<newE.v1.yCoord<<endl; 
//
// testing input 
char str[255] = "[((0, 0), (0, 1), 2), ((0, 0), (1, 0), 0), ((1, 0), (1, 1), 2), ((0, 1), (1, 1), 0), ((0, 0), (1, 0), 1), ((0, 0), (0, 1), 0), ((0, 1), (1, 1), 1), ((1, 0), (1, 1), 0), ((0, 0), (0, 1), 1), ((0, 0), (1, 0), 2), ((0, 1), (1, 1), 2), ((1, 0), (1, 1), 1)]";
int i =0;
int v11,v12,v21,v22;
vector <int> levelList;
while (str[i]!= ']')
{ 
  if(str[i]=='(' && str[i+1] =='('){
  i += 2;
  while (str[i]<'0' || str[i]> '9') { i++;}
  v11 = str[i] -'0'; i++;
  while (str[i]<'0' || str[i]> '9') { i++;}
  v12 = str[i]-'0'; i++;
  while (str[i]<'0' || str[i]> '9') { i++;}
  v21 = str[i]-'0'; i++;
  while (str[i]<'0' || str[i]> '9') { i++;}
  v22 = str[i]- '0'; i++;
  while (str[i]<'0' || str[i]> '9') { i++;}
  level = str[i]- '0'; 
  cout<<v11<<v12<<v21<<v22<<level<<endl;
  V1._init_(v11,v12);
  V2._init_(v21,v22);
  vertices.push_back(V1);
  vertices.push_back(V2);
  Edge edge;
  edge._init_(V1,V2, level);
  edges.push_back(edge);
  // number of distinct levels.
  // get how many different levels there are. 
  levelList.push_back(level);
 }
  
  else i++;
  
}
cout<<"# edges"<< edges.size()<<endl;
cout<<levelList.size()<<endl;
//    cout<<str[0]<<endl;
vector<int>::iterator iter;
vector<int> diffLevels;
sort(levelList.begin(), levelList.end());


std::cout << "level contains:"<< levelList[0];
diffLevels.push_back(levelList[0]);
for (iter=levelList.begin()+1; iter!=levelList.end(); iter++)
  {
    if(*iter != *(iter-1)) {
       diffLevels.push_back(*iter);
       std::cout << ' ' << *iter;}
  }//for
std::cout << '\n';
//end of get unique levels 

//vector<Edge> :: iterator iter_E;
//group edges by levels. 
for (iter= diffLevels.begin(); iter!= diffLevels.end(); iter++)
{
    int currLevel = *iter;
    vector <Edge> edgeList;
    vector<Edge> :: iterator iter_E;

    for (iter_E= edges.begin(); iter_E != edges.end(); iter_E ++)
    {
        if (iter_E -> level == currLevel)
        {
            edgeList.push_back(*iter_E);
        }  
    }//for
    cout<<"level is "<< currLevel<<endl;
    // add another iterator for edgeList
    vector <Edge> :: iterator iter_E2;
    for (iter_E = edgeList.begin(); iter_E != --edgeList.end() ; iter_E++)
    { 
       for (iter_E2 = edgeList.begin()+1; iter_E2 != edgeList.end(); iter_E2++ )
       {
           //test if the 2 edge can be merge    
           if (canMerge(*iter_E , *iter_E2 ))
           {   // merge   
               cout<< "can merge";
               iter_E -> merge(*iter_E,*iter_E2);
               cout<<"can merge"; 
               //edgeList.erase(iter_E2);
           }
       }//for

    }//for
   
}//for

return 0;
}




