#include <iostream>
#include <vector>
#include <cstdlib>
using namespace std;
using std::vector; 
#include <cmath>
#include <list>
using std::list;
#include <algorithm>  
#include <fstream>
#include <string>

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
// add here
vector <Vertex2> inner_vertices ( vector<VerticalPairs> vert_edges )
{
    vector <Vertex2> inner_vert;
    vector <VerticalPairs> :: iterator vp; 
    for ( vp = vert_edges.begin() ;vp != vert_edges.end(); vp ++)
    {
        if ((vp->level_2 - vp->level_1) >=2  )
        {
            for(int lev = vp -> level_1 +1 ; lev < vp-> level_2 ; lev++ )
            {
                Vertex2 inner ;
                inner._init_(vp->xCoord,vp->yCoord, lev);
                inner_vert.push_back(inner);
            }
        }
    }
    return inner_vert;
}

bool isOneLoop (vector<Vertex2> vertex_list , vector<VerticalPairs> vert_edges, vector<Edge> hori_edges, vector<Vertex2> & possi_path )
{
    // make sure the path is empty
    possi_path.clear();

    // remove inner vertices of vertical edges first
    vector<Vertex2> inner_vertical_vertices = inner_vertices(vert_edges);
    //PrintVertices(inner_vertical_vertices);
    vector <Vertex2> :: iterator inner_vp;
    
    for(inner_vp =inner_vertical_vertices.begin(); inner_vp != inner_vertical_vertices.end(); inner_vp ++ )
    {
        eraseElement(vertex_list, *inner_vp);
    }

    // here we go to search neighbors
    Vertex2 start_vertex = vertex_list.back( );
    vertex_list.pop_back();
    Vertex2 curr_vertex = start_vertex;
    possi_path.push_back(curr_vertex);
   // PrintVertices(possi_path);
    
    
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
     //       PrintVertices(possi_path);
       
        }
        else if (neighbors[1].find(vertex_list))
        {
           
            curr_vertex = neighbors[1];
            eraseElement (vertex_list, curr_vertex);          
            possi_path.push_back(curr_vertex);
       //     PrintVertices(possi_path);
          
        }
                
        else 
        {
            cout<< "not a loop"<<endl; 
 //   cout<< "final remain code"<<endl;
  //  PrintVertices ( vertex_list );
            return false;
        } 
    
    }

  //  cout<< "final remain code"<<endl;
  //  PrintVertices ( vertex_list );
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

void get3Dtable  ( vector<Edge> edges ,vector<int> diffLevels , int *** degTable )
{
  
//group edges by levels. 
    for ( vector<int>::iterator iter= diffLevels.begin(); iter!= diffLevels.end(); iter++)
    {
        int currLevel = *iter;
        vector <Edge> edgeList;
        vector<Edge> :: iterator iter_E;

        //cout<<"current level"<<currLevel<<endl;
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

       for (iter_V= vertList.begin(); iter_V != vertList.end(); iter_V ++)
       {
            int xCoord,yCoord,zCoord;
            xCoord = iter_V -> xCoord;
            yCoord = iter_V -> yCoord;
            zCoord = currLevel;
            degTable[xCoord][yCoord][zCoord] += 1;
        
       }

   ///cout<<edgeList.size()<<endl;
   
   
    }//for

}    

void find_connect_node(int *** degTable, vector<int> **possible_pairs)
{
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
                }
            }  
         }
     }//for
} // find connect node

vector <VerticalPairs> get_vertical_edges( int *** degTable , vector<int> **possible_pairs, vector<VerticalPairs> ** possible_connect  )
{
    vector <VerticalPairs> vertical_edges;
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
                 if (possible_pairs[i][j].size() ==2 )
       
                 {
                    
                    VerticalPairs vp;
                    int level_1, level_2;
                    level_1 = possible_pairs[i][j][0];
                    level_2 = possible_pairs[i][j][1];
                    vp._init_ (i,j, level_1,level_2);
                    if(!vp.find (possible_connect[i][j] ))
                     { possible_connect[i] [j].push_back(vp); {
            //             cout<<"pairs"<< vp.level_1 << vp.level_2<<endl;
                         WithVerticalEdges(degTable , vp);
                         vertical_edges.push_back (vp);
                       }
                     }
                  } //if
                  else if ( possible_pairs[i][j].size() ==4 )
                  {
                                     
                    VerticalPairs vp1,vp2;
                    int level_41, level_42, level_43,level_44;
                    level_41 = possible_pairs[i][j][0];
                    level_42 = possible_pairs[i][j][1];
                    vp1._init_ (i,j, level_41,level_42);
                    if(!vp1.find (possible_connect[i][j] )){
                      possible_connect[i] [j].push_back(vp1);
                      WithVerticalEdges(degTable, vp1);
                      vertical_edges.push_back (vp1);

                    }//if
                    level_43 = possible_pairs[i][j][2];
                    level_44 = possible_pairs[i][j][3];
                    vp2._init_ (i,j, level_43,level_44);
                    if(!vp2.find (possible_connect[i][j] )){
                      possible_connect[i] [j].push_back(vp2);
                      WithVerticalEdges(degTable, vp2);
                      vertical_edges.push_back (vp2);

                    }
                    
                  }              

           //      cout<<" # pairs"<<  possible_connect[i][j].size() <<endl;
              
               }//if
          } //for

       }//for
    } // for

    return vertical_edges;
}


bool runAlgMSN (char * str ,vector <Vertex2> &  whole_path  )

{
  
    vector<Edge> edges;
    vector <int > level_list;
    edges = edge_vector ( str, level_list);
    
    vector<int> diffLevels;
    diffLevels = diff_level(level_list);

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

// get 3D arrary degTable
    get3Dtable (edges,diffLevels, degTable);   
    bool islegal = 0;
    islegal =isLegalPoly( degTable);
    //cout<< "can go to enum ?? " << islegal<<endl;
    
// if can be enumerate all of the
// possible pairs means possible nodes that can be paired   
    if (islegal)
    {

    // initialize 2D array. 
    // possible_pairs is 2D array, each element of array is a vector<int>
        vector<int> **possible_pairs ;
        possible_pairs = new vector<int>*[XDIM + 1];
        for (int i = 0; i <= XDIM; i++)
            possible_pairs[i] = new vector<int>[YDIM + 1];
    // get degree = 1 node
        find_connect_node(degTable, possible_pairs) ;

    // initialize 2D array, each element is vertice pairs
        vector<VerticalPairs> ** possible_connect;
        possible_connect = new vector<VerticalPairs>*[XDIM + 1];
        for (int i = 0; i <= XDIM; i++)
            possible_connect[i] = new vector<VerticalPairs>[YDIM + 1];

    // get vertical edges and change table degree
        vector <VerticalPairs> vertical_edges =  get_vertical_edges (degTable, possible_pairs , possible_connect  ) ;
 
    // 832 
    // make sure all vertex has 0 or 2 degree
        if( isLegalDegree(degTable) )
        {
            // check if there are more than 1 loops
    //        cout<<"legal in degree"<<endl;   

            vector<Vertex2 > vertices_list;
            vertices_list = allVertices(degTable);
   //         cout<< "# vertices" << vertices_list.size()<<endl;
   //         PrintVertices(vertices_list);
        //eraseElement  (vertices_list, vertices_list[0]) ;
        //cout<< "# vertices" << vertices_list.size()<<endl;
            vector<Vertex2> possible_path;

//cout<< vertices_list.size()<< vertical_edges.size()<< edges.size()<<possible_path.size()<<endl;
            bool num_loop =  isOneLoop(vertices_list, vertical_edges, edges,possible_path);
       // cout<< "is one loop" << num_loop<<endl; 
           // PrintVertices (vertices_list);
            if(num_loop ){
              //  PrintVertices(possible_path);
            // get full vertices of a path
                whole_path = add_inner_vertices (possible_path);
     //           PrintVertices(whole_path);
     //           cout<< "reducible ? "<< check_reducible(whole_path)<<endl;            
                if ( ! check_reducible(whole_path)  ) 
                {
                   // PrintVertices(whole_path);
                    return true;
                }
                else 
                {
                    cout<< "this knot is reducible"<<endl;
                    return false;
                }
            } // if is only 1 loop
            else
            {
                cout<<"more than one loop "<< endl;
                return false;
            }
        }// if islegaldegree
        else 
        {
            cout<<"ilegal degree of degtable after adding vertical vertices"<< endl;
            return false;
        }
    
    }// if islegal
    else
    {
        cout<< "ilegal degree of degTable"<<endl;
        return false;
    }
     
} // runAlgMSN 

int main ()
{

//char str[255] = "[((0, 0), (0, 1), 2), ((0, 0), (1, 0), 2), ((1, 0), (1, 1), 2), ((0, 1), (0, 2), 1), ((1, 1), (1, 2), 1), ((0, 2), (0, 3), 0), ((0, 3), (1, 3), 0), ((1,3),(1,2),0)]";

//char str[1023] = "[((0,1),(0,2),3),((0,2),(0,3),3),((0,3),(1,3),3),((1,0),(1,1),2),((1,1),(1,2),2),((1,2),(0,2),2),((0,2),(0,3),2),((0,1),(1,1),1),((0,2),(1,2),1),((1,2),(1,3),1),((0,0),(1,0),0), ((0,0),(0,1),0), ((0,1), (0,2),0), ((1,1), (1,2),0) ,((1,2),(1,3),0), ((0,3),(1,3),0) ] ";

  ifstream in("tarKD3.txt");
  {
    if(! in)
    {
      cout << "Cannot open input file.\n";
      return 1;
    }
    char str [1023];
    while( in) {
      in.getline(str, 1023);
     // cout<< str<<endl;
      vector<Vertex2> whole_path ; 
      bool islegalknot = runAlgMSN (str,whole_path  );
      if ( islegalknot  )
      {
        cout<< "this knot is legal"<< endl;
        PrintVertices(whole_path);
      }//if  

    }// while     
  }
  in.close();  
 return 0;
}
