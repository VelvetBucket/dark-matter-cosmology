#include <iostream>
#include <fstream>
#include <sstream> 
#include <iomanip>
#include <vector>
#include <algorithm>
#include <cmath> 
#include "tools/tools.h"

using namespace std;

int main(int argc, char** argv){
  
  string dofeff_file = DATATABLES_DIR "/std_thg.txt";
  vector<vector<double>> dofeff_table = data_extractor(dofeff_file,3);
  //Remove T = 0 GeV
  dofeff_table.erase(remove_if(dofeff_table.begin(), dofeff_table.end(), [](vector<double> val) { return val[0] <= 0.0; }), dofeff_table.end());
  vector<pair<double, double>> heff_Temp = datatable_to_pairs(dofeff_table);
  vector<pair<double, double>> geff_Temp = datatable_to_pairs(dofeff_table,0,2);
  
  int N = 2500;
  double start = 1.e+21, end = 1.e-13, h = log(end/start)/(N-1);
  const double mu_M = 0.519*1.e-9, mu_DE = 2.24*1.e-3*1.e-9; //1. eV = 1.e-9 GeV
  const double Mp = 2.435e+18, T0 = 1.0, geff_T0 = xlog_ylog_interpolator(geff_Temp, T0);
  double Tn, geffn, heffn, an_a0, ro_rn, Hn;
  
  for (int n = 0; n < N; n++){
    Tn = exp(log(start) + n*h);
    geffn = xlog_ylog_interpolator(geff_Temp, Tn);
    heffn = xlog_ylog_interpolator(heff_Temp, Tn);
    
    // Calculate ratio a(T)/a0
    an_a0 = T0/Tn * pow(geff_T0/geffn, 0.25);
    
    //Calculate Hubble(T)
    ro_rn = pow(M_PI,2)/30.*geffn*pow(Tn,4) + mu_M*2.*pow(M_PI,2)/45.*heffn*pow(Tn,3) + pow(mu_DE,4);
    Hn = sqrt(ro_rn/(3.*pow(Mp,2)));
    
    // Write values
    cout << scientific << setprecision(8) << an_a0 << " " << Tn << " " << Hn << "\n";
  }
  return 0;
}
