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

// Integra dσ/dcosθ en cosθ ∈ [-1, 1]
double sigma(double s, const vector<double>& masses){

  const double a = 0;  // cosθ_min
  const double b =  M_PI;  // cosθ_max

  const double mi1 = masses[0];
  const double mi2 = masses[1];
  const double mf1 = masses[2];
  const double mf2 = masses[3];
  
  double p_f, p_i, factor;
  
  //double integral = gauss(&diff_sigma, s, a, b, 7);
  auto f1 = [s, &masses](double theta) { return sigmav_iface::sigmaKin(s, theta, masses); };
  double integral = mb::gauss_kronrod(f1, a, b, 5, 1.e-02);

  if (integral > 0.0) {
    p_f = 0.5 * sqrt((s - pow(mf1 + mf2,2))*(s - pow(mf1 - mf2,2))/s);
    if (p_f < 1.e-15) return 0.0;
    factor = p_f/(32.0 * M_PI);
    integral*=factor;
  }
  return integral;
}

double diff_A(double u, double T, const double m1, double k2_m1_scaled, const vector<double>& masses, const vector<std::pair<double, double>>& newDOF, const vector<double>& newMasses){
  
  const double mi1 = masses[0];
  const double mi2 = masses[1];
  
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
  
  const double p_ij = 0.5 * sqrt((s - pow(mi1 + mi2,2))*(s - pow(mi1 - mi2,2))/s);
  
  if (p_ij < 1.e-15) return 0.0;
  
  const double sigma_ij = sigma(s, masses);
  
  if (s < 1.e-15) return 0.0;
  
  const double b12 = exp(-(sqrt(s) - 2.0*m1)/T) * gsl_sf_bessel_Kn_scaled(1, sqrt(s)/T)/(k2_m1_scaled*k2_m1_scaled);
 
  return gi * gj * p_ij * sigma_ij * b12;
}

double sigma_v(double T, const double m1, const vector<double>& masses, const vector<std::pair<double, double>>& newDOF, const vector<double>& newMasses){
  
  const double k2_m1 = bessK2(m1/T);
  
  const double lim_inf = 0.0;
  const double lim_sup = 60.0;
  const double k2_m1_scaled = gsl_sf_bessel_Kn_scaled(2, m1 / T);
  
  double den, mi, b22, k2_mi, factor_den = 0.0;
  den = pow(m1,4);
  for (auto mi_gi : newDOF) {
    mi = mi_gi.first;
    if (mi == m1) {
      factor_den += mi_gi.second;
    } else {
      k2_mi = bessK2(mi/T);
      if (mi/T > 10.0){
        b22 = exp(-(mi - m1)/T) * gsl_sf_bessel_Kn_scaled(2, mi/T)/k2_m1_scaled;
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
  
  auto f1 = [T,m1,k2_m1_scaled,&masses,&newDOF,&newMasses](double u) { return diff_A(u,T,m1,k2_m1_scaled,masses,newDOF,newMasses); };
  double A = mb::gauss_kronrod(f1, lim_inf, lim_sup, 5, 1.e-02);
  return A/den;
}

int main(int argc, char** argv){

  Options opt = parse_args(argc, argv);

  string card = opt.inputFile;
  const double x0 = opt.x0, xf = opt.xf;
  const int N = opt.N;
  
  sigmav_iface::initProc(card);
  const auto& newDOF = sigmav_iface::getNewDOF();
  const auto& newMasses = sigmav_iface::getNewMasses();
  const double m1 = *std::min_element(newMasses.begin(), newMasses.end());
  
  const double T0 = m1/x0, Tf = m1/xf, ui = log(T0), h=log(Tf/T0)/(N-1);
  double un, Tn, sigv_n;
  
  cout << setiosflags(ios::scientific) << setprecision(8) << "# m1 = " << m1 << " GeV" << "\n";
  
  if (opt.neq) {
    
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
    
    const auto& masses = sigmav_iface::getMasses();
    const double mi1 = masses[0];
    const double mi2 = masses[1];
    const double delta1 = mi1/m1 - 1.;
    const double delta2 = mi2/m1 - 1.;
    
    if (std::max(delta1, delta2) > 0.25) return 0;
    
    double g1 = 0.0, gi1 = 0.0, gi2 = 0.0; 
    
    for (auto mi_gi : newDOF) {
      if (mi_gi.first == m1){
        g1 = mi_gi.second;
      }
      if (mi_gi.first == mi1){
        gi1 = mi_gi.second;
      }
      if (mi_gi.first == mi2){
        gi2 = mi_gi.second;
      }
      if (g1 > 0.0 && gi1 > 0.0 && gi2 > 0.0){
        break;
      }
    }
    
    const double x_f = 15.;
    const double frac1 = (gi1/g1) * std::pow(1. + delta1, 1.5) * std::exp(-x_f * delta1);
    const double frac2 = (gi2/g1) * std::pow(1. + delta2, 1.5) * std::exp(-x_f * delta2);
    
    if (std::min(frac1, frac2) < 0.001) return 0;
    
    cout << "# x (DM_candidate_mass/T) vs. sigma*v" << endl;

    // Precompute T values (cheap, avoids exp() in the parallel region)
    std::vector<double> Ts(N);
    for (int n = 0; n < N; n++) {
        Ts[n] = std::exp(ui + n * h);
    }

    // Parallel evaluation of sigma_v(Ts[n])
    std::vector<double> sigv(N, 0.0);

    int n_threads = std::min(12, static_cast<int>(std::thread::hardware_concurrency()) / 2);
    if (n_threads > N) n_threads = N;
    if (n_threads < 1) n_threads = 1;

    std::cerr << "# Using " << n_threads << " threads\n";

    std::atomic<int> next{0};
    std::vector<std::thread> workers;
    workers.reserve(n_threads);

    for (int w = 0; w < n_threads; ++w) {
        workers.emplace_back([&, masses, newDOF, newMasses]() {
            while (true) {
                int n = next.fetch_add(1);
                if (n >= N) break;
                sigv[n] = sigma_v(Ts[n], m1, masses, newDOF, newMasses);
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
