MSN Algorithm.

Graph is the class used throughout the program that represents the weighted projections.
Steps 1 and 2 rely heavily on this Graph.

Knot is the class used to represent the 3-D lattice polygon.

msnAlgRunner is the main class with most of the logic for the MSN Algorithm.

Finally, pp-lib is the library that I downloaded and used to run it in parallel on the cluster.

##############################################################################################

new reversion of code 

1 Using msnAlgRunner.py for step 1 and step 2, it will output the diagrams of polygons. 

  complie and runs this part using :
  
  srun python msnAlgRunner.py 1 3 3 26 s > tarKD3.txt
  
  Put result in tarKD3.txt. 1 3 3 26 s meas: xdim =1 ydim =3 zdim =3 total length of polygon is <= 26. “s” means run serial code. 
  

2 Make sure XDIM, YDIM, ZDIM and LENGTH are set as you want, for example 3 by 1 case length 26 polygons, it is 

#define XDIM 1

#define YDIM 3

#define ZDIM 3

#define LENGTH 26

3 compile msnStep3.cpp

g++ -o graph_3 msnStep3.cpp -Wall -g

4 run, the result will be put in graph3.txt

srun ./graph_3  > graph3.txt 








