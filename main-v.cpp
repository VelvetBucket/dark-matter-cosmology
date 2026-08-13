#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include "process/CPPProcess.h"
#include "process/momenta.h"
#include "tools/tools.h"
#include <algorithm> 
#include <unordered_map>
#include <boost/math/quadrature/gauss_kronrod.hpp>
#include <boost/math/quadrature/tanh_sinh.hpp>
#include <gsl/gsl_sf_bessel.h>

using namespace std;

CPPProcess process;

double diff_sigma(double theta, double s){

  vector<double> masses = process.getMasses();
  double sigma = 0.0;
  
  vector<double *> ps = momenta(2,sqrt(s),masses,theta);

  for(int x = 0; x<4; x++){
    if (ps[x][0] <= 0.0){ //physical constraints
      for (auto* ptr : ps) {
        delete ptr;
      }
      ps.clear();
      masses.clear();
      return 0.0;
    }
  }
        
  process.setMomenta(ps);
  sigma = process.sigmaKin(s, theta);
  
  for (auto* ptr : ps) {
    delete ptr;
  }
  
  ps.clear();
  masses.clear();
  return sigma;
}

// Integra dσ/dcosθ en cosθ ∈ [-1, 1]
double sigma(double s){

  const double a = 0;  // cosθ_min
  const double b =  M_PI;  // cosθ_max
  
  const double mi1 = process.getMasses().at(0);
  const double mi2 = process.getMasses().at(1);
  const double mf1 = process.getMasses().at(2);
  const double mf2 = process.getMasses().at(3);
  double p_f, p_i, factor, error;
  
  //double integral = gauss(&diff_sigma, s, a, b, 7);
  auto f1 = [s](double theta) { return diff_sigma(theta,s); };
  boost::math::quadrature::tanh_sinh<double> integrator;
  //double integral = integrator.integrate(f1, a,b, 1e-04);
  double integral = boost::math::quadrature::gauss_kronrod<double, 15>::integrate(f1, a, b, 5, 1e-02, &error);
  //double integral = simpson(diff_sigma, s, a, b, 1.0e-03, NULL);
  
  if (integral > 0.0) {
    p_f = 0.5 * sqrt((s - pow(mf1 + mf2,2))*(s - pow(mf1 - mf2,2))/s);
    p_i = 0.5 * sqrt((s - pow(mi1 + mi2,2))*(s - pow(mi1 - mi2,2))/s);
    if (p_f < 1e-15 || p_i < 1e-15) return 0.0;
    factor = p_f/(32.0 * M_PI);
    integral*=factor;///(s * p_i);
  }
  return integral;
}

double diff_A(double u, double T){
  
  vector<std::pair<double, double>> newDOF = process.getNewDOF();
  const vector<double> newMasses = process.getNewMasses();
  const double m1 = *std::min_element(newMasses.begin(), newMasses.end());;
  
  const double mi1 = process.getMasses().at(0);
  const double mi2 = process.getMasses().at(1);
  const double mass_ratio_cut = 100.0;  // or 1.5, 2.0, etc.
  
  //if (mi1 > mass_ratio_cut*m1 || mi2 > mass_ratio_cut*m1) return 0.0; 
  
  //if (mi1 != m1 || mi2 != m1) return 0.0;
  double gi = 0.0, gj= 0.0; 
  
  for (auto mi_gi : newDOF) {
    if (mi_gi.first == mi1){
      gi = mi_gi.second;
    }
    if (mi_gi.first == mi2){
      gj = mi_gi.second;
    }
    if (gi > 0.0 && gj > 0.0){
      break;
    }
  }  
  
  if (gi == 0.0 || gj == 0.0){
    std::cerr << "No geff found!! mi1 = "  << mi1 << " mi2 = " << mi2 << "\n";
    return -1.0 * 1e+7;
  }
  // u = sqrt(s)/T - mi1/T -mi2/T
  const double s = pow(u*T + mi1 + mi2,2);
  const double var_change = 1.0;
  
  double p_ij = 0.5 * sqrt((s - pow(mi1 + mi2,2))*(s - pow(mi1 - mi2,2))/s);
  double sigma_ij = sigma(s);
  double dA, b12;
  
  if (p_ij < 1e-15) return 0.0; 
  
  if (m1/T > 10.0) {
    b12 = exp(-(sqrt(s) - 2.0*m1)/T) * gsl_sf_bessel_Kn_scaled(1, sqrt(s)/T)/pow(gsl_sf_bessel_Kn_scaled(2, m1/T),2);
  } else {
    b12 = bess12(sqrt(s)/T, m1/T);
  }
  
  dA = gi * gj * p_ij * sigma_ij * b12;
  //cout << sqrt(s)/T << " " << m1/T << " " << b12 << "\n"; 
  return dA;
}

double sigma_v(double T){

  vector<std::pair<double, double>> newDOF = process.getNewDOF();
  const vector<double> newMasses = process.getNewMasses();
  const double m1 = *std::min_element(newMasses.begin(), newMasses.end());
  const double k2_m1 = bessK2(m1/T);
  
  double lim_inf = 0.0;
  double lim_sup = 80.0;//std::numeric_limits<double>::infinity();
  
  double error, den, mi, b22, k2_mi, factor_den = 0.0;
  int Err = 1;
  den = pow(m1,4);
  for (auto mi_gi : newDOF) {
    mi = mi_gi.first;
    if (mi == m1) {
      factor_den += mi_gi.second;
    } else {
      k2_mi = bessK2(mi/T);
      if (mi/T > 10.0){
        b22 = exp(-(mi - m1)/T) * gsl_sf_bessel_Kn_scaled(2, mi/T)/gsl_sf_bessel_Kn_scaled(2, m1/T);
      } else {
        b22 = k2_mi/k2_m1;
      }
      if (true) {
        factor_den += mi_gi.second * pow(mi/m1,2) * b22;
      }
    }
  }
  
  den *= pow(factor_den,2);
  if (den == 0.0) return 100000.0;
  
  auto f1 = [T](double t) { return diff_A(t,T); };
  double A = 0.0;
  boost::math::quadrature::tanh_sinh<double> integrator;
  //A = integrator.integrate(f1, lim_inf, lim_sup, 1e-04);
  A = boost::math::quadrature::gauss_kronrod<double, 15>::integrate(f1, lim_inf, lim_sup, 5, 1e-04, &error);
  return A/den;
}

int main(int argc, char** argv){
	
  std::string card = argv[1];
  process.initProc(card);
  
  const vector<double> newMasses = process.getNewMasses();
  const double m1 = *std::min_element(newMasses.begin(), newMasses.end());
  
  const double mi1 = process.getMasses().at(0);
  const double mi2 = process.getMasses().at(1);
  int N = 1000, N_neq = 10*N, Err=1;
  double Ti = m1*1e+10, Tf = m1*1e-7 , ui = log(Ti), h=log(Tf/Ti)/(N-1), Tn = Tf;
  double h_neq = log(Tf/Ti)/(N_neq-1);
  //double si=1e+8, sf=1e+18, h = log(sf/si)/(N-1), T= m1*1e+4, zi = log(si), zn;
  //double ui=1e-1, uf=1e+3, h = log(uf/ui)/(N-1), si=log(ui), T = m1/20.;
  double un, sn, sig;
  h = -0.04;
  //double Tn = m1*1e+01;
  
  if (argc == 3) {
    std::string neq_file = argv[2];
    const vector<std::pair<double, double>> newDOF = process.getNewDOF();
    double mi, neq, k2_mi;
    ofstream myFile(neq_file);
    
    myFile << setiosflags(ios::scientific) << setprecision(8) << "# m1 = " << m1  << "\n";
    
    for(int n = 0; n < N_neq; n++){
      un = ui + n*h_neq;
      Tn = std::exp(un);
      neq = 0.0;
      k2_mi = 0.0;
      for (auto mi_gi : newDOF) {
        mi = mi_gi.first;
        //cout << mi << " " << mi_gi.second << "\n";
        k2_mi = bessK2(mi/Tn);
        if (mi/Tn > 10.0 || k2_mi == 0.0) {
          k2_mi = exp(-mi/Tn) * gsl_sf_bessel_Kn_scaled(2, mi/Tn);
        } 
        if (true){
          neq += mi_gi.second * pow(mi,2) * k2_mi;
        }
      }
      neq *= Tn/(2.0*pow(M_PI,2)); 
      myFile << setiosflags(ios::scientific) << setprecision(8) << Tn << " " << neq  << "\n";
    }
    
    myFile.close();
  }
  //cout << m1 << "\n";
  for(int n = 0; n < N; n++){
    un = ui + n*h;
    Tn = std::exp(un);
    sig = sigma_v(Tn);
    cout << setiosflags(ios::scientific) << setprecision(8) << m1/Tn << " " << sig << "\n";
  }
 
  return 0;
}
