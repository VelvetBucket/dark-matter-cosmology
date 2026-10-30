#include <iostream>
#include <fstream>
#include <iomanip>
#include <string>
#include <cmath>
#include "sigmav_interface.h"
#include "tools.h"
#include "my_boost.h"
#include <algorithm> 
#include <unordered_map>
#include "options.h"
#include <gsl/gsl_sf_bessel.h>
#include <stdexcept>
#include <atomic>
#include <thread>
#include <vector>

using namespace std;

double diff_sigma(double theta, double s){

  vector<double> masses = sigmav_iface::getMasses();
  double sigma = 0.0;
  
  sigma = sigmav_iface::sigmaKin(s, theta);
  
  masses.clear();
  return sigma;
}

// Integra dσ/dcosθ en cosθ ∈ [-1, 1]
double sigma(double s){

  const double a = 0;  // cosθ_min
  const double b =  M_PI;  // cosθ_max
  
  const auto& masses = sigmav_iface::getMasses();   // const&, no copy

  const double mi1 = masses[0];
  const double mi2 = masses[1];
  const double mf1 = masses[2];
  const double mf2 = masses[3];
  
  double p_f, p_i, factor, error;
  
  //double integral = gauss(&diff_sigma, s, a, b, 7);
  auto f1 = [s](double theta) { return diff_sigma(theta,s); };
  //double integral = integrator.integrate(f1, a,b, 1e-04);
  double integral = mb::gauss_kronrod(f1, a, b, 5, 1e-04);
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
  
  vector<std::pair<double, double>> newDOF = sigmav_iface::getNewDOF();
  const vector<double> newMasses = sigmav_iface::getNewMasses();
  const double m1 = *std::min_element(newMasses.begin(), newMasses.end());;
  
  const double mi1 = sigmav_iface::getMasses().at(0);
  const double mi2 = sigmav_iface::getMasses().at(1);
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

  vector<std::pair<double, double>> newDOF = sigmav_iface::getNewDOF();
  const vector<double> newMasses = sigmav_iface::getNewMasses();
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
  //tanh_sinh<double> integrator;
  //A = integrator.integrate(f1, lim_inf, lim_sup, 1e-04);
  A = mb::gauss_kronrod(f1, lim_inf, lim_sup, 5, 1e-04);
  return A/den;
}

int main(int argc, char** argv){

  Options opt = parse_args(argc, argv);

  string card = opt.inputFile;
  double x0 = opt.x0, xf = opt.xf, m1 = opt.m1;
  int N = opt.N;
  
  sigmav_iface::initProc(card);
  const vector<double> newMasses = sigmav_iface::getNewMasses();
  if (m1 < 0.0) {
    m1 = *std::min_element(newMasses.begin(), newMasses.end());
  }
  
  const double mi1 = sigmav_iface::getMasses().at(0);
  const double mi2 = sigmav_iface::getMasses().at(1);
  double T0 = m1/x0, Tf = m1/xf, ui = log(T0), h=log(Tf/T0)/(N-1);
  double un, Tn, sigv_n;
  
  cout << setiosflags(ios::scientific) << setprecision(8) << "# m1 = " << m1 << " GeV" << "\n";
  
  if (opt.neq) {
    
    const vector<std::pair<double, double>> newDOF = sigmav_iface::getNewDOF();
    double mi, neq, k2_mi;
    
    cout << "# x (DM_candidate_mass/T) vs. n_equilibrium" << endl;
    
    for(int n = 0; n < N; n++){
      un = ui + n*h;
      Tn = std::exp(un);
      neq = 0.0;
      k2_mi = 0.0;
      for (auto mi_gi : newDOF) {
        mi = mi_gi.first;
        k2_mi = bessK2(mi/Tn);
        if (mi/Tn > 10.0 || k2_mi == 0.0) {
          k2_mi = exp(-mi/Tn) * gsl_sf_bessel_Kn_scaled(2, mi/Tn);
        } 
        neq += mi_gi.second * pow(mi,2) * k2_mi;
      }
      neq *= Tn/(2.0*pow(M_PI,2)); 
      cout << setiosflags(ios::scientific) << setprecision(8) << m1/Tn << " " << neq << "\n";
    }
    
  } else {
    
    cout << "# x (DM_candidate_mass/T) vs. sigma*v" << endl;

    // Precompute T values (cheap, avoids exp() in the parallel region)
    std::vector<double> Ts(N);
    for (int n = 0; n < N; n++) {
        Ts[n] = std::exp(ui + n * h);
    }

    // Parallel evaluation of sigma_v(Ts[n])
    std::vector<double> sigv(N, 0.0);

    int n_threads = std::min(8, static_cast<int>(std::thread::hardware_concurrency()) / 2);
    if (n_threads > N) n_threads = N;
    if (n_threads < 1) n_threads = 1;

    std::cerr << "# Using " << n_threads << " threads\n";

    std::atomic<int> next{0};
    std::vector<std::thread> workers;
    workers.reserve(n_threads);

    for (int w = 0; w < n_threads; ++w) {
        workers.emplace_back([&]() {
            while (true) {
                int n = next.fetch_add(1);
                if (n >= N) break;
                sigv[n] = sigma_v(Ts[n]);
            }
        });
    }
    for (auto& t : workers) t.join();

    // Print serially — deterministic order, no cout races
    for (int n = 0; n < N; n++) {
        cout << setiosflags(ios::scientific) << setprecision(8)
             << m1 / Ts[n] << " " << sigv[n] << "\n";
    }
  }
  
  return 0;
}
