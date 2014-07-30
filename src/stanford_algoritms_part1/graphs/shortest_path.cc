

#include <iostream>
#include <vector>
#include <string>
#include <stdexcept>

using namespace std;

// http://www.onlamp.com/pub/a/onlamp/2006/04/06/boostregex.html?page=3
//#include <boost/regex.hpp>  // too hard

vector<int> process_data_line(string line) {
  // 0\t8,89\t...  source sink, weight ... -> 0,8,89 - 
  vector<int> result;
  result.reserve(100);  // защита от лишний аллокаций  
  
  
  // postcondition
  if (result.size() % 2 != 0)
    throw invalid_argument(line);
  
  return result;  // сразу не поставил а gcc не отловил - в итоге дамп памяти
}

int main() {
  string test_line("0\t8,89\t9,90");
  vector<int> processed = process_data_line(test_line);
  
  
  return 0;
}