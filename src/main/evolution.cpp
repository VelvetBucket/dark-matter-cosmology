#include <iostream>
#include <fstream>
#include <sstream> 
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cmath> 
#include "tools/tools.h"

using namespace std;

vector<vector<double>> dataset_ath = data_extractor("./interp_ath.dat",3);
vector<pair<double,double>> T_a = datatable_to_pairs(dataset_ath,0,1);
vector<pair<double,double>> H_a = datatable_to_pairs(dataset_ath,0,2);

double Hubble(double a){
  return xlog_ylog_interpolator(H_a, a);
}

double Temp(double a){
  return xlog_ylog_interpolator(T_a, a);
}

vector<double> Nsolver(const vector<pair<double,double>> neq_Temp_data, const vector<pair<double,double>> sigmav_x_data, const double j_i, const double N_i, double h = 0.01, const double rtol = 1.e-2, const double atol = 1.e-8, const bool debug = false){
  
  const double m1 = 1.87710315e+00, h_min = 1.e-9;
  const double a_i = exp(j_i), T_i = Temp(a_i), H_i = Hubble(a_i);
  const double sigmav_i = xlog_ylog_interpolator(sigmav_x_data, m1/T_i);
  const double Neq_i = pow(a_i, 3) * xlog_ylog_interpolator(neq_Temp_data, T_i); 
  const double z_i = sigmav_i/(pow(a_i, 3)*H_i);
  
  double j_iplus = j_i + h, a_iplus = exp(j_iplus);
  double T_iplus = Temp(a_iplus), H_iplus = Hubble(a_iplus);
  double sigmav_iplus = xlog_ylog_interpolator(sigmav_x_data, m1/T_iplus);
  double Neq_iplus = pow(a_iplus, 3) * xlog_ylog_interpolator(neq_Temp_data, T_iplus); 
  double z_iplus = sigmav_iplus/(pow(a_iplus, 3)*H_iplus);
  
  double NT, NE, NT_old, diff;
  //cout << "starting loops" << endl;
  // Covering the case where z_i+1 == 0
  while (z_iplus == 0.0 && h >= 2.0*h_min) {
    h = h/2.;
    j_iplus = j_i + h;
    a_iplus = exp(j_iplus);
    T_iplus = Temp(a_iplus);
    H_iplus = Hubble(a_iplus);
    sigmav_iplus = xlog_ylog_interpolator(sigmav_x_data, m1/T_iplus);
    Neq_iplus = pow(a_iplus, 3) * xlog_ylog_interpolator(neq_Temp_data, T_iplus); 
    z_iplus = sigmav_iplus/(pow(a_iplus, 3)*H_iplus);
  } 
  
  if (z_iplus == 0.0) {
    if (false) {
      cout << "DEBUG: z_i+1 == 0.0 " << NT << " " << NT_old << " " << diff << " " << diff/NT << " " << h << endl;
    }
    NT = N_i + h/2. * (-1. * z_i * (pow(N_i, 2) - pow(Neq_i, 2)));
    NE = N_i;
    return {j_iplus, NT, Neq_iplus, fabs(1. - NE/NT)};
  }
  
  // Now with z_i+1 !=0
  double u = h*z_iplus, rho = z_i/z_iplus;
  double cT = 2.*N_i + u*((pow(Neq_iplus,2) + rho*pow(Neq_i,2)) - rho*pow(N_i,2));
  double cE = 4.*(N_i + u*pow(Neq_iplus,2));
  
  while (u*cT < -1.0 || u*cE < -1.0) {
  
    if (false) {
      cout << "DEBUG: U*C < -1.: " << " " << pow(Neq_iplus,2) + rho*pow(Neq_i,2) << " "  << rho*pow(N_i,2) << endl;
    }
  
    h = h/2.;
    j_iplus = j_i + h;
    a_iplus = exp(j_iplus);
    T_iplus = Temp(a_iplus);
    H_iplus = Hubble(a_iplus);
    sigmav_iplus = xlog_ylog_interpolator(sigmav_x_data, m1/T_iplus);
    Neq_iplus = pow(a_iplus, 3) * xlog_ylog_interpolator(neq_Temp_data, T_iplus); 
    z_iplus = sigmav_iplus/(pow(a_iplus, 3)*H_iplus);
    
    u = h*z_iplus;
    rho = z_i/z_iplus;
    cT = 2.*N_i + u*((pow(Neq_iplus,2) + rho*pow(Neq_i,2)) - rho*pow(N_i,2));
    cE = 4.*(N_i + u*pow(Neq_iplus,2));
  }
  
  NT = cT / (1. + sqrt(1. + u*cT));
  NE = 0.5 * cE / (1. + sqrt(1. + u*cE));
  
  diff = fabs(NT) + 2*atol;
  
  while (diff > (fabs(NT*rtol) + atol) && h >= 2.*h_min){
  
    h = h/2.;  
    
    j_iplus = j_i + h;
    a_iplus = exp(j_iplus);
    T_iplus = Temp(a_iplus);
    H_iplus = Hubble(a_iplus);
    sigmav_iplus = xlog_ylog_interpolator(sigmav_x_data, m1/T_iplus);
    Neq_iplus = pow(a_iplus, 3) * xlog_ylog_interpolator(neq_Temp_data, T_iplus); 
    z_iplus = sigmav_iplus/(pow(a_iplus, 3)*H_iplus);
    
    u = h*z_iplus;
    rho = z_i/z_iplus;
    
    if (false) {
      cout << "DEBUG: RHO: " << " " << u << endl;
      cout << "DEBUG: RHO: " << " " << rho << endl;
      cout << "DEBUG: NI: " << " " << N_i << endl;
      cout << "DEBUG: NeqI: " << " " << Neq_i << endl;
      cout << "DEBUG: WEIRD: " << " " << pow(Neq_iplus,2) + rho*pow(Neq_i,2) << " "  << rho*pow(N_i,2) << endl;
    }
    
    cT = 2.*N_i + u*((pow(Neq_iplus,2) + rho*pow(Neq_i,2)) - rho*pow(N_i,2));
    cE = 4.*(N_i + u*pow(Neq_iplus,2));
    
    NT_old = NT;
    NT = cT / (1. + sqrt(1. + u*cT));
    NE = 0.5 * cE / (1. + sqrt(1. + u*cE));
    diff = fabs(NT - NT_old);
    //cout << diff/NT << endl;
    //cout << fabs(NT*rtol) << " " <<(fabs(NT*rtol) + atol) << endl;
    if (false) {
      cout << "DEBUG: " << NT << " " << NT_old << " " << diff << " " << diff/NT << " " << h << endl;
    }
  }
  
  if (debug) {
      cout << "DEBUG: h " << h << endl;
  }
  
  return {j_iplus, NT, Neq_iplus, sigmav_iplus};
}

int main(int argc, char** argv){
  
  const string card = "35_75-1";
  
  const vector<pair<double,double>> neq_Temp_data = datatable_to_pairs(data_extractor("./output/" + card + "/neq.dat"));
  const vector<pair<double,double>> sigmav_x_data = datatable_to_pairs(data_extractor("./output/" + card + "/TOTALS_T.dat"));
  
  const double ai = 1.e-10, af = 1.e+10, default_h = 0.01;  
  double an = ai, jn = log(an), jf = log(af), Tn = Temp(an);
  double Nn = pow(ai, 3) * xlog_ylog_interpolator(neq_Temp_data, Tn);
  double Neqn = Nn;
  double h = default_h, rel_err = 0.;
  bool plateau = false;
  vector<double> results(4);
  
  //cout << "start: " << jn << endl;
  //cout << "end: " << jf << endl;\
  
  cout << setiosflags(ios::scientific) << setprecision(8) << jn << " " << h << " " << an << " " << Tn << " " << Nn << " " << Neqn << " " << rel_err << "\n";
  
  while (jn < jf) {
    h = 2.*min(default_h, (jf-jn));
    //cout << jf << endl;
    //cout << h << endl;
    results = Nsolver(neq_Temp_data, sigmav_x_data, jn, Nn, h, 1.e-2, 1.e-20, false);
    h = results[0] - jn; 
    jn = results[0];
    
    //plateau = ( fabs(Nn - results[1]) < results[1]*1.e-10);
    Nn = results[1];
    Neqn = results[2];
    rel_err = results[3];
    an = exp(jn);
    Tn = Temp(an);
    cout << setiosflags(ios::scientific) << setprecision(8) << jn << " " << h << " " << an << " " << Tn << " " << Nn << " " << Neqn << " " << rel_err << "\n";
    
    if (plateau) break;
  }
  
  return 0;
}
