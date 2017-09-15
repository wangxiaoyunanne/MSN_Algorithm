#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main()
{
  ifstream in("tarKD.txt");

  if(!in) {
    cout << "Cannot open input file.\n";
    return 1;
  }

  char str[255];
  //string str1;
 // int i =0;
  while(in) {
    in.getline(str, 255);  // delim defaults to '\n'
    //if(in) cout << str << endl;
   // i++;:q

  in.close();
  cout<<i<<endl;
  return 0;
}
