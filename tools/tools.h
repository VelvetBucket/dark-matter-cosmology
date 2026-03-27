#ifndef TOOL_H
#define TOOL_H

#include <iostream>
#include <cmath>
#include <stdio.h>
#include <vector>


/* Bessel functions*/
double bessI0(double  x);
static double bessI1(double x);
double bessK0(double x);
double bessK1(double x);
double bessK2(double x);
double K2pol(double x);
double K1pol(double x);
double bess12(double x, double y);


/* Integration tools */
double gauss( double (*func)(double, double),double par, double a,double b, int n);
static void r_gauss( double(*func)(double, double),double par, double a,double b, 
double eps, double * aEps, double * ans, double * aAns, int* N, int depth, int * err);
double gauss345( double (*func)(double, double),double par, double a,double b, double eps,int * err_code);
double peterson21(double (*func)(double, double),double par, double a, double b, double *aerr);
static void r_simpson( double(*func)(double, double),double par,double * f,double a,double b, 
double eps, double * aEps, double * ans, double * aAns, double _f_ , int depth, int depth1, int*nErr);
double simpson( double (*func)(double, double),double par,double a,double b, double  eps, int *err);
double trapezoidal(double (*func)(double, double),double par, double a, double b, double  eps);
double romberg(double (*f)(double, double), double par, double a, double b, double acc);

std::vector<int> findMultiplePeaks(const std::vector<double> arr);
std::vector<std::pair<int, int>> findPeakWidth(const std::vector<double> data, std::vector<int> peakIndexes);

#endif 
