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
   // i++;
    if (str[0] == '[')
        {
       // cout << str << endl;
        int i = 1;
            while (str[i] != ']')
            {
                if (str[i] == '(' & str[i+1] == '('  )
                    { // initalize 2 vertices and 1 edge 
                         int v11, v12,v21,v22,level;
                         i += 2;
                         if (str[i]<='9' & str[i] >= '0')
                             {v11 = atoi(str[i]);
                             i++;}
                         else i++;

                    }
                i++;
            }
        }
  }

  in.close();
  cout<<i<<endl;
  return 0;
}
