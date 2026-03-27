#include "momenta.h"

// =======================================================================
//  Momenta en función de t Usando Kinematics.pdf (49.34–49.37)
// =======================================================================
std::vector<double*> momenta(int ninitial, double energy, std::vector<double> masses, double t) {
    // s y sqrt{s}
    double s      = energy * energy;
    double sqrt_s = std::sqrt(s);

    // Masas
    double m1 = masses[0];
    double m2 = masses[1];
    double m3 = masses[2];
    double m4 = masses[3];

    // ===== (49.36): Energías en el CM para el estado inicial =====
    double E1cm = (s + m1*m1 - m2*m2) / (2.0 * sqrt_s);
    double E2cm = (s + m2*m2 - m1*m1) / (2.0 * sqrt_s);

    // ===== (49.37): Magnitud del momento inicial en CM =====
    double p1cm = std::sqrt(E1cm*E1cm - m1*m1);

    // ===== (49.36) con m3,m4: Energías finales en el CM =====
    double E3cm = (s + m3*m3 - m4*m4) / (2.0 * sqrt_s);
    double E4cm = (s + m4*m4 - m3*m3) / (2.0 * sqrt_s);

    // ===== (49.37): Magnitud del momento final en CM =====
    double p3cm = std::sqrt(E3cm*E3cm - m3*m3);  // = |p4_cm|

    // ===== (49.35): extremos t0 (θ=0) y t1 (θ=π) *en función de masas* =====
    // Δ = (m1^2 - m3^2 - m2^2 + m4^2) / (2√s)
    double Delta = (m1*m1 - m3*m3 - m2*m2 + m4*m4) / (2.0 * sqrt_s);
    double t0 = Delta*Delta - (p1cm - p3cm)*(p1cm - p3cm); // θ=0
    double t1 = Delta*Delta - (p1cm + p3cm)*(p1cm + p3cm); // θ=π

    // Restringimos t al rango físico [t1, t0] por estabilidad numérica
    double t_phys = t;
//    if (t_phys > t0) t_phys = t0;
//    if (t_phys < t1) t_phys = t1;

    // ===== (49.34): invertir para obtener θ_cm(t)
    // t = t0 - 4 p1 p3 sin^2(θ/2)  ⇒  sin^2(θ/2) = (t0 - t)/(4 p1 p3), como lo pidio Javier la primera vez
    double x = (t0 - t_phys) / (4.0 * p1cm * p3cm);
//    if (x < 0.0) x = 0.0;
//    if (x > 1.0) x = 1.0;
    double theta = 2.0 * std::asin(std::sqrt(x));

    // Construimos los 4-momentos (eje z como dirección del haz)
    std::vector<double*> p;
    p.reserve(4);

    // Entrantes
    p.push_back(new double[4]{E1cm, 0.0, 0.0,  p1cm});
    p.push_back(new double[4]{E2cm, 0.0, 0.0, -p1cm});

    // Salientes (elegimos φ=0 para fijar el plano de dispersión: py=0)
    p.push_back(new double[4]{E3cm,  p3cm * std::sin(theta), 0.0,  p3cm * std::cos(theta)});
    p.push_back(new double[4]{E4cm, -p3cm * std::sin(theta), 0.0, -p3cm * std::cos(theta)});

    return p;
}

