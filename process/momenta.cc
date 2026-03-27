#include "momenta.h"

std::vector<double*> momenta(int ninitial, double energy, std::vector<double> masses, double theta) {
    // Precalcular el valor de e2 (energy al cuadrado) y sqrt(e2)
    double phi = 1.5 * M_PI;
    double e2 = energy * energy;
    double sqrt_e2 = energy;
    
    // Masas de las partículas
    double m1 = masses[0];
    double m2 = masses[1];

    // Calcular el momento de las partículas entrantes    
    double energy1 = 0.5 * sqrt_e2 * (1 + pow(m1, 2) / e2 - pow(m2, 2) / e2);
    double energy2 = 0.5 * sqrt_e2 * (1 + pow(m2, 2) / e2 - pow(m1, 2) / e2);
    
    double mom_i2 = energy1 * energy1 - m1 * m1;
    double mom_i = 0.0;
    
    if (mom_i2 <= 0.0 || energy1 <= 0.0 || energy2 <= 0.0){
      energy1 = -1.0;
      energy2 = -1.0;
    } 
    else{
      mom_i = std::sqrt(mom_i2);
    }
    
    // Crear vector de punteros a momentos
    std::vector<double*> p;
    p.reserve(4);
    
    // Asignar momentos de las partículas entrantes
    p.push_back(new double[4]{energy1, 0, 0, mom_i});
    p.push_back(new double[4]{energy2, 0, 0, -1.0*mom_i});

    // Masas de las partículas finales
    double m3 = masses[2];
    double m4 = masses[3];

    // Calcular las energías de las partículas salientes
    double energy3 = 0.5 * sqrt_e2 * (1 + pow(m3, 2) / e2 - pow(m4, 2) / e2);
    double energy4 = 0.5 * sqrt_e2 * (1 + pow(m4, 2) / e2 - pow(m3, 2) / e2);

    // Calcular el momento final
    double mom_f2 = energy3 * energy3 - m3 * m3;
    double mom_f = 0.0;
    
    if (mom_f2 <= 0.0 || energy3 <= 0.0 || energy4 <= 0.0){
      energy3 = -1.0;
      energy4 = -1.0;
    } 
    else{
      mom_f = std::sqrt(mom_f2);
    }

    // Asignar momentos de las partículas salientes
    p.push_back(new double[4]{energy3, mom_f * std::sin(theta) * std::cos(phi), mom_f * std::sin(theta) * std::sin(phi), mom_f * std::cos(theta)});
    p.push_back(new double[4]{energy4, -mom_f * std::sin(theta) * std::cos(phi), -mom_f * std::sin(theta) * std::sin(phi), -mom_f * std::cos(theta)});
    //std::cout << "adios__ " << mom << " " << (mom * mom) << "\n";
    return p;
}
