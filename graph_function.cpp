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
    
    int xCoord;
    int yCoord;
   
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
    // find whether a vertex is in a vector
    bool find (vector<Vertex2> vertex_list) ;
};//vertex2
Vertex2 :: Vertex2(void) {}

void Vertex2 :: _init_(int x,int y, int z ){

        xCoord = x;
        yCoord = y;
        zCoord = z;
       // graphXDim = graphx;
       // graphYDim = graphy;
    }

bool Vertex2 :: find (vector<Vertex2> vertex_list)
{
    vector <Vertex2> :: iterator iter_vt ;
    for (iter_vt = vertex_list.begin(); iter_vt != vertex_list.end(); iter_vt ++)
    {
        if (iter_vt -> xCoord == xCoord &&
           iter_vt -> yCoord == yCoord &&
           iter_vt -> zCoord == zCoord  )
        {
            return true;
        }
    }

   return false;
}

void eraseElement (vector<Vertex2> & vertex_list, Vertex2 value)
{
   // for (iter_vt = vertex_list.begin(); iter_vt != vertex_list.end(); iter_vt ++)

    vector <Vertex2> :: iterator iter_vt = vertex_list.begin();
    //for (iter_vt = vertex_list.begin(); iter_vt != vertex_list.end(); iter_vt ++)
    while (iter_vt != vertex_list.end())
    {
        if (iter_vt -> xCoord == value.xCoord &&
           iter_vt -> yCoord == value.yCoord &&
           iter_vt -> zCoord == value.zCoord  )
        {
            iter_vt = vertex_list.erase(iter_vt); 
        } else iter_vt ++;
            
    }

}

bool isNeighbor (Vertex2 v1, Vertex2 v2)
{
    int distance = abs(v1.xCoord - v2.xCoord)+ abs(v1.yCoord - v2.yCoord)+abs(v1.zCoord - v2.zCoord);
    if (distance == 1)
        return true;
    else 
        return false;
}

Vertex2 :: ~Vertex2(void) {}

vector<Vertex2> allVertices(int *** degTable)
{
    vector<Vertex2> vertical_list;
    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
           // int numNodes = 0;
           for (int k =0; k < ZDIM +1 ; k++) //z dim
           {
               if ( degTable[i][j][k] == 2 ) 
               {
                   Vertex2 vert;
                   vert._init_(i,j,k);
                   vertical_list.push_back(vert); 
               }
               
           }
        }
    }
    return vertical_list;
}

void PrintVertices (vector<Vertex2> vertex_list)
{
    vector <Vertex2> :: iterator iter_vt ;
    for (iter_vt = vertex_list.begin(); iter_vt != vertex_list.end(); iter_vt ++)
    {
        cout<<iter_vt -> xCoord<<" " << iter_vt -> yCoord<< " " << iter_vt -> zCoord<< "/";       
    }
    cout<< endl;
}

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
         level = lev;
     
     }//initial


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
       if (all2Flag && !all0Flag  )
        {
            return false;
            cout<< "illegal vertex degree ( all 2)" <<endl;
        }
        
    }// for

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


bool isLegalDegree  (int *** degTable)
{
    for (int i =0; i< XDIM+1; i++)// x  dim
    {
        for (int j =0; j < YDIM+1; j++) //y dim
        {
           // int numNodes = 0;
           for (int k =0; k < ZDIM +1 ; k++) //z dim
           {
               if ( degTable[i][j][k] != 0  && degTable[i][j][k] != 2 ) 
                   {//cout<<i<<j<<k<<degTable[i][j][k] <<endl;
                   return false;}
               
           }
        }
    }
    return true;
}

void WithVerticalEdges ( int *** degTable, VerticalPairs vp)
{
    int x = vp.xCoord;
    int y = vp.yCoord;
    int lev1 = vp.level_1;
    int lev2 = vp.level_2;
    for (int i = lev1; i <= lev2; i++)
    {
       if (i == lev1 || i == lev2)
       { degTable[x][y][i] += 1;  }
       else
       { degTable[x][y][i] += 2;
       }
    }
}


vector<Vertex2>  getNeighbor (Vertex2 curr , vector<VerticalPairs> vert_edges, vector<Edge> hori_edges)
{
   vector <Vertex2> result;
   Vertex2 neighV;
   for (unsigned int i =0; i < vert_edges.size() ;i++  )
   {
       int vert_x = vert_edges[i].xCoord;
       int vert_y = vert_edges[i].yCoord;
       int level_1 = vert_edges[i].level_1;
       int level_2 = vert_edges[i].level_2;
       if (curr.xCoord == vert_x && 
           curr.yCoord == vert_y &&
           curr.zCoord == level_1 )             
       {
          neighV._init_ ( vert_x,vert_y, level_2);
          result.push_back( neighV );
       }
       else if(curr.xCoord == vert_x &&     
            curr.yCoord == vert_y &&
            curr.zCoord == level_2 )
       {
          neighV._init_ ( vert_x,vert_y, level_1);
          result.push_back( neighV );

       }

    }// first for loop of vertical edges

    for (unsigned int i=0; i < hori_edges.size(); i++)
    {
       int level_h = hori_edges[i].level;
       Vertex V1, V2;
       V1 = hori_edges[i].v1;
       V2 = hori_edges[i].v2;
       if (curr.xCoord ==V1.xCoord &&
           curr.yCoord == V1.yCoord &&
           curr.zCoord == level_h)
       {
          neighV._init_(V2.xCoord,V2.yCoord,level_h);
          result.push_back(neighV);
       }
       else if (curr.xCoord ==V2.xCoord &&
           curr.yCoord == V2.yCoord &&
           curr.zCoord == level_h)
       {
          neighV._init_(V1.xCoord,V1.yCoord,level_h);
          result.push_back(neighV);
       }  
    }// second for loop of horizontal edges

    return result;
}

bool isOneLoop (vector<Vertex2> vertex_list , vector<VerticalPairs> vert_edges, vector<Edge> hori_edges, vector<Vertex2> & possi_path )
{

    Vertex2 start_vertex = vertex_list.back( );
    vertex_list.pop_back();
    Vertex2 curr_vertex = start_vertex;
    possi_path.push_back(curr_vertex);
    PrintVertices(possi_path);
    
    while( !vertex_list.empty() )
    {
      //  test if a vertex is neighbor of current vertex
      // if so, put this neighbor into path. 
        vector<Vertex2> neighbors = getNeighbor(curr_vertex, vert_edges, hori_edges); 
        if ( neighbors[0].find(vertex_list  ) )
        {
           // cout<< "go to neigh 0"<< endl;
            curr_vertex = neighbors[0];
            eraseElement (vertex_list , curr_vertex);
            possi_path.push_back(curr_vertex);
           // PrintVertices(possi_path);
       
        }
        else if (neighbors[1].find(vertex_list))
        {
           
            curr_vertex = neighbors[1];
            eraseElement (vertex_list, curr_vertex);          
            possi_path.push_back(curr_vertex);
           // PrintVertices(possi_path);
          
        }
                
        else 
        {
            cout<< "not a loop"<<endl; 
            return false;
        } 
    
    }

   // cout<< "final remain code"<<endl;
   // PrintVertices ( vertex_list );
    //cout<<"possible pass" << endl;
   // PrintVertices(possi_path;
 
    return true;
}

vector<Vertex2> add_inner_vertices (vector <Vertex2>  path )
{
    Vertex2 start_vertex = path[0];
    Vertex2 end_vertex = path.back( );
    vector <Vertex2> whole_path;
  //  whole_path.pushback ( start_vertex );
    int path_length = path.size(); 
    for(int i =0; i< path_length; i++)
    {
        whole_path.push_back (path[i]);
        int next_index =  (i+1) % path_length;
        if (abs( path[i].zCoord - path[ next_index].zCoord) >1 ) 
        {
            if ( path[i].zCoord > path[ next_index ].zCoord  )
            {
                for (int z = path[next_index].zCoord +1; z < path[i].zCoord; z++ )
                {
                    Vertex2 inner_v;
                    inner_v._init_( path[next_index].xCoord, path[next_index].yCoord, z);
                    whole_path.push_back(inner_v);
                }
            }
            else
            {
                for (int z = path[i].zCoord +1; z < path[next_index].zCoord; z++ )
                {
                    Vertex2 inner_v;
                    inner_v._init_( path[next_index].xCoord, path[next_index].yCoord, z);
                    whole_path.push_back (inner_v);
                }

            }
        }     
    }
    return whole_path;
}

bool check_reducible (vector <Vertex2> path)
{
    int path_length = path.size();
    for (int i = 0; i < path_length ; i++)
    {
        int next_index = (i+3) % path_length;
        if ( isNeighbor(path[i],path[next_index] ) )
        {
            return true ;
        }
    }
    return false;
}

vector <Edge> edge_vector (char * str , vector<int> & levelList) 
{
    int level;
    Vertex V1, V2;
    vector <Edge>  edges;

    int i =0;
    int v11,v12,v21,v22;
    vector < Vertex> vertices ;
    levelList.clear() ;

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
      }// if
  
      else i++;
  
    }//while

    return edges;
}// edge_vector


vector <int> diff_level (vector<int> levelList )
{
    vector<int>::iterator iter;
    vector<int> diffLevels;
    sort(levelList.begin(), levelList.end());

    diffLevels.push_back(levelList[0]);

    for (iter=levelList.begin()+1; iter!=levelList.end(); iter++)
    {
       if(*iter != *(iter-1)) {
         diffLevels.push_back(*iter);
       //  std::cout << ' ' << *iter;
       }
    }//for

    return diffLevels;
}// diff_level

bool msnAlgRun ( vector<Edge> edges ,vector<int> diffLevels , vector<Vertex2> & path  )
{
    return false;
}


int main ()
{
    char str[255] = "[((0, 0), (0, 1), 2), ((0, 0), (1, 0), 2), ((1, 0), (1, 1), 2), ((0, 1), (0, 2), 1), ((1, 1), (1, 2), 1), ((0, 2), (0, 3), 0), ((0, 3), (1, 3), 0), ((1,3),(1,2),0)]";

    vector<Edge> edges;
    vector <int > level_list;
    edges = edge_vector ( str, level_list);
    
    vector<int> diffLevels;
    diffLevels = diff_level(level_list);
    


    return 0;
}
