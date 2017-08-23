#include <python2.7/Python.h>
int main(){
    Py_SetProgramName("myPythonProgram");
    Py_Initialize();
    PyRun_SimpleString("exec(open('msnAlgRunner.py').read())");
    Py_Finalize();
}
