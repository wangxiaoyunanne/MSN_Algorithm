#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;
using std::vector; 
#include <cmath>
#include <list>
using std::list;
#include <algorithm>  

#define XDIM 1
#define YDIM 3
#define ZDIM 3


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

//Vertex2 is a 3D class 
class Vertex2 {
  public :
    int xCoord;
    int yCoord;
    int zCoord;
     // set value for coordinate
    Vertex2();
    ~Vertex2();
    void _init_ (int x, int y, int z);
};//vertex2
Vertex2 :: Vertex2(void) {}

void Vertex2 :: _init_(int x,int y, int z ){

        xCoord = x;
        yCoord = y;
        zCoord = z;
       // graphXDim = graphx;
       // graphYDim = graphy;
    }

Vertex2 :: ~Vertex2(void) {}

// vertical pairs of nodes 
// x, y, level 1, level 2 
class VerticalPairs {
  public :
    int xCoord;
    int yCoord;
    int level_1;
    int level_2;
     // set value for coordinate
    VerticalPairs();
    ~VerticalPairs();
    void _init_ (int x, int y, int lev_1, int lev_2);
    bool find (vector<VerticalPairs > VP_list   ); // find if vp is in a vector     
    
};//vertical Paris
VerticalPairs :: VerticalPairs(void) {}

void VerticalPairs :: _init_(int x,int y, int lev_1, int lev_2 ){

        xCoord = x;
        yCoord = y;
        level_1 = lev_1;
        level_2 = lev_2;
       // graphXDim = graphx;
       // graphYDim = graphy;
}

bool VerticalPairs :: find  (vector<VerticalPairs > VP_list ) {
    vector <VerticalPairs> :: iterator iter_vp ;
    for (iter_vp = VP_list.begin(); iter_vp != VP_list.end(); iter_vp ++)
    {
        if (iter_vp -> xCoord == xCoord &&
           iter_vp -> yCoord == yCoord &&
           iter_vp -> level_2 == level_2 &&
           iter_vp -> level_1 == level_1 )
        {
            return true;  
        }
    }
    return false;
}

VerticalPairs :: ~VerticalPairs(void) {}

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
    void _init_ (Vertex vert1, Vertex vert2, int lev);
    void merge(Edge &edge1, Edge edge2);
};//Edge

void Edge ::_init_ (Vertex vert1, Vertex vert2, int lev){
         v1 = vert1; 
         v2 = vert2; 
         //weight = weight;
         //graphXDim = graphx;
         //graphYDim =  graphy; 
         level = lev;
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

bool isLegalPoly (int *** degTable )
{
    // check in each level if there is some vertices whose degree is > 2
    for (int k = 0 ; k< ZDIM +1; k ++)
    {
        //cout<< "k = " << k <<endl;
        bool all2Flag = 1;
        bool all0Flag = 1;
        int currLevel = k;
        for (int i =0; i< XDIM+1; i++)// x  dim
        {
            for (int j =0; j < YDIM+1; j++) //y dim
            {
                if (degTable [i][j][currLevel] >2)
                {
                    all0Flag = 0;
                    return false;
                    cout<<"illegal vertex degree (greater than 2) " <<endl;
                }
                else if (degTable [i][j][currLevel] ==1 )
                {
                    all2Flag = 0; // there is a vertex whose degree is not 2
                    all0Flag = 0;
                }     //elseif
                else if (degTable [i][j][currLevel] ==2 )
                {
                    all0Flag = 0;
                }
                
            }
        } //for
        //cout<< "all2Flag"<< all2Flag <<endl; 
        //cout<< "all0Flag"<< all0Flag <<endl;

        // in the currlevel there is a closed loop. 
        if (all2Flag && !all0Flag  )
        {
            return false;
            cout<< "illegal vertex degree ( all 2)" <<endl;
        }
        
    }// for

    // cout<<"no degree >2 "<<endl;
    // find whether the node of connected edges has neighours in other level
    // that we can connect
    // check if there are even number of nodes in each x-y position
    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
            int numNodes = 0;
            for (int k =0; k < ZDIM +1 ; k++) //z dim
            {
                if (degTable[i][j][k] == 1)
                {
                    numNodes += 1;

                }
            }
            if (numNodes % 2 == 0)// means legal
            {
               // cout<<"can merge"<<endl;
                // do emnumerate and connection
                return true;
            }
            else
            {
                return false;
                cout << "illegal number of nodes of connected edges" <<endl;
            }
        }
    }

    return false;
}
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
   // cout<<"size of vertices "<< vertices.size()<<endl;
    cout<<V1.xCoord<<V1.yCoord<<endl;
    V2._init_(1,3);
    V3._init_(2,2) ;
//    int * v12 = V2.substract(V3);
   // cout<<v12[0]<<v12[1]<<endl;
   // cout<<V1._eq_(V2)<<endl;
    int level = 0;
    Edge edge1, edge2;
    edge1._init_(V1,V2,level);
    edge2._init_(V1,V3,level);
//    cout<<"level of edge "<<edge1.level<<endl;
    Edge newE;
//    cout<<"can merge ?"<<canMerge(edge1,edge2)<<endl;
    edge1.merge(edge1,edge2);
    cout<<edge1.v1.xCoord<<edge1.v1.yCoord<<edge1.v2.xCoord<<edge1.v2.yCoord <<edge1.level<<endl;
    // get edge array


vector <Edge>  edges;
    //cout<<"merge E"<< newE.v1.xCoord<<newE.v1.yCoord<<endl; 
//
// testing input 
char str[255] = "[((0, 0), (0, 1), 2), ((0, 0), (1, 0), 2), ((1, 0), (1, 1), 2), ((0, 1), (0, 2), 1), ((1, 1), (1, 2), 1), ((0, 2), (0, 3), 0), ((0, 3), (1, 3), 0), ((1,3),(1,2),0)]";
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
  //cout<<v11<<v12<<v21<<v22<<level<<endl;
  V1._init_(v11,v12);
  V2._init_(v21,v22);
  vertices.push_back(V1);
  vertices.push_back(V2);
  Edge edge;
  edge._init_(V1,V2, level);
 // cout<< "this edge is "<<edge.level<<endl;
  edges.push_back(edge);
  // number of distinct levels.
  // get how many different levels there are. 
  levelList.push_back(level);
 }
  
  else i++;
  
}
//cout<<"# edges"<< edges.size()<<endl;

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
cout<<"# diff level"<< diffLevels.size()<<endl;
vector<Edge> :: iterator iter_E;
//for (iter_E= edges.begin(); iter_E != edges.end(); iter_E ++)
    //cout<<iter_E -> level;

//group edges by levels. 
// build a vertices table first
int ***degTable;
degTable = new int ** [XDIM+1];
for (int i =0; i< XDIM+1; i++)// x  dim
{
    degTable[i] = new int * [YDIM+1];
    for (int j =0; j < YDIM+1; j++) //y dim
    {
        degTable[i][j] = new int  [ZDIM+1];
        for (int k =0; k < ZDIM +1 ; k++) //z dim
        {
            degTable[i][j][k] = 0;
        }
    }
}// it gives each vertex degree



for ( vector<int>::iterator iter= diffLevels.begin(); iter!= diffLevels.end(); iter++)
{
    int currLevel = *iter;
    vector <Edge> edgeList;
    vector<Edge> :: iterator iter_E;

    cout<<"current level"<<currLevel<<endl;
// get a vertices list
    vector <Vertex>  vertList;
    vector <Vertex> :: iterator iter_V;
// get each level edge list    

    for (iter_E= edges.begin(); iter_E != edges.end(); iter_E ++)
    {
//        cout<<"levels" <<iter_E -> level<<currLevel <<endl;
        if (iter_E -> level == currLevel)
        {
  //          cout<<"if"<<endl;
            edgeList.push_back(*iter_E);
            vertList.push_back(iter_E -> v1);
            vertList.push_back (iter_E -> v2);
        }  
    }//for
 //   cout<<"level is "<< currLevel<<iter_E -> level<<endl;
    // add another iterator for edgeList
   // cout<< "vertlist size " << vertList.size()<<endl;
// make a table for each vertex degree
    for (iter_V= vertList.begin(); iter_V != vertList.end(); iter_V ++)
    {
        int xCoord,yCoord,zCoord;
        xCoord = iter_V -> xCoord;
        yCoord = iter_V -> yCoord;
        zCoord = currLevel;
        degTable[xCoord][yCoord][zCoord] += 1;
        
    }
/*
// for each level, check if any vertices has degree more than 2 or all of them are 2;
    bool all2Flag = 1;
    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
            if (degTable [i][j][currLevel] >2)
            {
                cout<<"illegal vertex degree (greater than 2) " <<endl;
            }
            else if (degTable [i][j][currLevel] ==1 )
            {
                all2Flag = 0; // there is a vertex whose degree is not 2
               
            }//elseif
        }
    }//for
    
    if (all2Flag)
    {
        cout<< "illegal vertex degree ( all 2)" <<endl;
    }

 */
   // end of checking degree of vertices


   // vector <Edge> :: iterator iter_E2;
    
/*
    for (iter_E = edgeList.begin(); iter_E != --edgeList.end() ; iter_E++)
    { 
       for (iter_E2 = edgeList.begin()+1; iter_E2 != edgeList.end(); iter_E2++ )
       {
           //test if the 2 edge can be merge    
           if (canMerge(*iter_E , *iter_E2 ))
           {   // merge   
 //              cout<< "can merge";
               iter_E -> merge(*iter_E,*iter_E2);
 //              cout<<"can merge"; 
               cout<<iter_E->v1.xCoord<<iter_E->v1.yCoord<<iter_E->v2.xCoord
               <<iter_E->v2.yCoord<<endl;
               edgeList.erase(iter_E2);
           }
           if (edgeList.size() == 1)
              break;
       }//for

    }//for
*/
   cout<<edgeList.size()<<endl;
   
   
}//for

bool islegal = 0;
islegal =isLegalPoly( degTable);
cout<< "can go to enum ?? " << islegal<<endl;
/*
// find whether the node of connected edges has neighours in other level
// that we can connect
// check if number of nodes in each x-y position are even

    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
            int numNodes = 0
            for (int k =0; k < ZDIM +1 ; k++) //z dim
            {
                if (degTable[i][j][k] == 1)
                {
                    numNodes += 1;

                }
            }
            if (numNodes % 2 == 0)// means legal
            {
                // do emnumerate and connection
                
            }
            else 
            {
                cout << "illegal number of nodes of connected edges" <<endl;
            } 
        }
    }
*/
// if can be enumerate all of the
// possible pairs means possible nodes that can be paired   
if (islegal)
{
    vector<int> **possible_pairs ;
    possible_pairs = new vector<int>*[XDIM + 1];
    for (int i = 0; i <= XDIM; i++)
        possible_pairs[i] = new vector<int>[YDIM + 1];
    // first find nodes
    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
            for (int k =0; k < ZDIM +1 ; k++) //z dim
            {
                if (degTable[i][j][k] == 1)
                {

                   
                    possible_pairs[i][j].push_back (k);
                    //cout<<"ijk"<<i<<j<<k<<endl;
                    //cout<<possible_pairs[i][j][k]<<endl;
                }
            }  
         }
     }//for
  
    vector<VerticalPairs> ** possible_connect;
    possible_connect = new vector<VerticalPairs>*[XDIM + 1];
    for (int i = 0; i <= XDIM; i++)
        possible_connect[i] = new vector<VerticalPairs>[YDIM + 1];

    // enumerate all possible connections
    // possible connection is possible pairs of connections
    for (int i =0; i<XDIM +1; i++)
    {
       for (int j =0; j < YDIM +1; j++)
       {
           vector <int> :: iterator iter_level; 
           //cout << "size of nodes"<< possible_pairs[i][j].size()<< endl;
           for (iter_level = possible_pairs[i][j].begin(); iter_level != possible_pairs[i][j].end(); iter_level ++   )           
           {
               if (possible_pairs[i][j].size() >0 )
               {
                   //int node_1 = possible_pairs.pop_back();
                   for (int lev_1 = 0; lev_1 < possible_pairs[i][j].size() -1; lev_1++ )
                       for (int lev_2 = lev_1 + 1; lev_2 < possible_pairs[i][j].size(); lev_2++)
                       {
                           //vector <VerticalPairs> :: iterator iter_vp ;
                          // iter_vp = find(possible_connect[i][j].begin(), possible_connect[i][j].end(),vp )
                           VerticalPairs vp;
                           int level_1, level_2;
                           level_1 = possible_pairs[i][j][lev_1];
                           level_2 = possible_pairs[i][j][lev_2];
                           vp._init_ (i,j, level_1,level_2);
                           
                         // iter_vp = find(possible_connect[i][j].begin(), possible_connect[i][j].end(),vp );
                           if (!vp.find (possible_connect[i][j] ) )
                           {
                           possible_connect[i][j].push_back( vp );
                          // cout<<vp.level_1<< vp.level_2<<endl;
                           cout<<"pairs"<< possible_pairs[i][j][lev_1]<< possible_pairs[i][j][lev_2]<<endl;
                           }
                       }
                    //cout<<" # pairs"<<  possible_connect[i][j].size()<<endl;
               }//if
           }//for

       }//for
    } // for
    // check
   
}// if

return 0;
}




