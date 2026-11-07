#include "momenta.h"

void momenta_into(double storage[4][4], int ninitial, double energy, std::vector<double> masses, double theta) {
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
    storage[0][0] = energy1;
    storage[0][1] = 0.0;
    storage[0][2] = 0.0;
    storage[0][3] = mom_i;
    
    storage[1][0] = energy2;
    storage[1][1] = 0.0;
    storage[1][2] = 0.0;
    storage[1][3] = -1.0 * mom_i;
    
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
    const double sin_theta = std::sin(theta);
    const double cos_theta = std::cos(theta);
    const double cos_phi   = std::cos(phi);
    const double sin_phi   = std::sin(phi);
    
    storage[2][0] = energy3;
    storage[2][1] = mom_f * sin_theta * cos_phi;
    storage[2][2] = mom_f * sin_theta * sin_phi;
    storage[2][3] = mom_f * cos_theta;
    
    storage[3][0] = energy4;
    storage[3][1] = -mom_f * sin_theta * cos_phi;
    storage[3][2] = -mom_f * sin_theta * sin_phi;
    storage[3][3] = -mom_f * cos_theta;
    
}
