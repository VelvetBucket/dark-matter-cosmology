#include "tools.h"
#include <iostream>
#include <fstream>
#include <sstream> 
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cmath> 

double xlog_ylin_interpolator(std::vector<std::pair<double, double>> points, double x) {
  
  //Define a lambda that returns true if the x value
  //of a point pair is < the caller's x value
  auto lessThan =
      [](const std::pair<double, double>& point, double x)
      {return point.first < x;};
 
  //Find the first table entry whose value is >= caller's x value
  auto iter = std::lower_bound(points.cbegin(), points.cend(), x, lessThan);
 
  //If the caller's X value is greater than the largest
  //X value in the table, we can't interpolate.
  if((points.cend() - 1)->first <= x) {
    return (points.cend() - 1)->second;
  }
 
  //If the caller's X value is less than the smallest X value in the table,
  //we can't interpolate.
  if(x <= points.cbegin()->first) {
    return points.cbegin()->second;
  }
 
  //We can interpolate!
  double upperX = iter->first;
  double upperY = iter->second;
  double lowerX = (iter - 1)->first;
  double lowerY = (iter - 1)->second;

  double ratioX = log(x/lowerX)/log(upperX/lowerX);
  double deltaY = upperY - lowerY;
 
  return lowerY + ratioX * deltaY;
}

double xlog_ylog_interpolator(std::vector<std::pair<double, double>> points, double x) {
  
  //Define a lambda that returns true if the x value
  //of a point pair is < the caller's x value
  auto lessThan =
      [](const std::pair<double, double>& point, double x)
      {return point.first < x;};
 
  //Find the first table entry whose value is >= caller's x value
  auto iter = std::lower_bound(points.cbegin(), points.cend(), x, lessThan);
 
  //If the caller's X value is greater than the largest
  //X value in the table, we can't interpolate.
  if((points.cend() - 1)->first <= x) {
    return (points.cend() - 1)->second;
  }
 
  //If the caller's X value is less than the smallest X value in the table,
  //we can't interpolate.
  if(x <= points.cbegin()->first) {
    return points.cbegin()->second;
  }
 
  //We can interpolate!
  double upperX = iter->first;
  double upperY = iter->second;
  double lowerX = (iter - 1)->first;
  double lowerY = (iter - 1)->second;

  // Avoiding case in with any of thew ys is zero
  if (lowerY <= 0.0 || upperY <= 0.0) return 0.0;
  
  double ratioX = log(x/lowerX)/log(upperX/lowerX);
  double deltaY = log(upperY/lowerY);
 
  return exp(log(lowerY) + ratioX * deltaY);
}
