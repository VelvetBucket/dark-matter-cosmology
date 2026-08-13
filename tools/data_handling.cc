#include "tools.h"
#include <iostream>
#include <fstream>
#include <sstream> 
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cmath> 

std::vector<std::vector<double>> data_extractor(std::string filename, int ncols){

  std::vector<std::vector<double>> data;
  // Open the text file
  std::ifstream file(filename);  
  
  // Check if the file was opened successfully
  if (!file.is_open()) {
    std::cerr<<"File cannot be opened!"<< std::endl;
  }
  
  std::string line;
  while (getline(file, line)) {
    // Skip comment lines
    if (!line.empty() && line[0] == '#') {
      continue;
    }    
    
    // Process valid lines here
    std::string datastring[ncols];
    std::vector<double> datapoint(ncols);
    std::stringstream line_stream(line);
    
    // Passing values in a specfic row
    for (int i = 0; i < ncols; ++i) {
        line_stream >> datastring[i];
        datapoint[i] = std::stod(datastring[i]);
    }
    
    data.push_back(datapoint);
    datapoint.clear();
  }
  
  // Close the file
  file.close(); 
  
  return data;
}

std::vector<std::pair<double,double>> datatable_to_pairs(const std::vector<std::vector<double>> table, int x_col, int y_col){
  
  int n = table.size();
  std::vector<std::pair<double,double>> points(n);

  for (int i = 0; i < n; i++){
    points[i] = {table[i][x_col], table[i][y_col]};
  }
  
  //Ensure that the vector is sorted
  sort(points.begin(), points.end());
  
  return points;
}
