//==========================================================================
// This file has been automatically generated for C++ Standalone
// MadGraph5_aMC@NLO v. 3.6.6, 2025-10-30
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#ifndef HelAmps_scotogenic_UFO_H
#define HelAmps_scotogenic_UFO_H

#include <cmath> 
#include <complex>

using namespace std; 

namespace MG5_scotogenic_UFO 
{
void ixxxxx(double p[4], double fmass, int nhel, int nsf, std::complex<double>
    fi[6]);

void txxxxx(double p[4], double tmass, int nhel, int nst, std::complex<double>
    fi[18]);

void oxxxxx(double p[4], double fmass, int nhel, int nsf, std::complex<double>
    fo[6]);

double Sgn(double e, double f); 

void sxxxxx(double p[4], int nss, std::complex<double> sc[3]); 

void vxxxxx(double p[4], double vmass, int nhel, int nsv, std::complex<double>
    v[6]);

void FFS1C1_0(std::complex<double> F2[], std::complex<double> F1[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS1C1_1(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS1C1_2(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFS1_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS1_1(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFS1_2(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS1_3(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> S3[]);

void FFS2C1_0(std::complex<double> F2[], std::complex<double> F1[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS2C1_1(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS2C1_2(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFS2_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS2_1(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> F1[]);

void FFS2_2(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> F2[]);

void FFS2_3(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> S3[]);

void SSV1_0(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void SSV1_1(std::complex<double> S2[], std::complex<double> V3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> S1[]);

void SSV1_2(std::complex<double> S1[], std::complex<double> V3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> S2[]);

void SSV1P0_3(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> V3[]);

void SSV1_3(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> V3[]);

void SSS1_0(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> S3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void SSS1_1(std::complex<double> S2[], std::complex<double> S3[],
    std::complex<double> COUP, double M1, double W1, std::complex<double> S1[]);

void SSS1_2(std::complex<double> S1[], std::complex<double> S3[],
    std::complex<double> COUP, double M2, double W2, std::complex<double> S2[]);

void SSS1_3(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> COUP, double M3, double W3, std::complex<double> S3[]);

void FFV3C1_0(std::complex<double> F2[], std::complex<double> F1[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFV3_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void VVV1_0(std::complex<double> V1[], std::complex<double> V2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFV2_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void SSVV1_0(std::complex<double> S1[], std::complex<double> S2[],
    std::complex<double> V3[], std::complex<double> V4[], std::complex<double>
    COUP, std::complex<double> & vertex);

void SVV1_0(std::complex<double> S1[], std::complex<double> V2[],
    std::complex<double> V3[], std::complex<double> COUP, std::complex<double>
    & vertex);

void FFS1_2C1_0(std::complex<double> F2[], std::complex<double> F1[],
    std::complex<double> S3[], std::complex<double> COUP1, std::complex<double>
    COUP2, std::complex<double> & vertex);

void FFS1_2C1_1(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP1, std::complex<double> COUP2, double M2, double
    W2, std::complex<double> F2[]);

void FFS1_2C1_2(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP1, std::complex<double> COUP2, double M1, double
    W1, std::complex<double> F1[]);

void FFS1_2_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> S3[], std::complex<double> COUP1, std::complex<double>
    COUP2, std::complex<double> & vertex);

void FFS1_2_1(std::complex<double> F2[], std::complex<double> S3[],
    std::complex<double> COUP1, std::complex<double> COUP2, double M1, double
    W1, std::complex<double> F1[]);

void FFS1_2_2(std::complex<double> F1[], std::complex<double> S3[],
    std::complex<double> COUP1, std::complex<double> COUP2, double M2, double
    W2, std::complex<double> F2[]);

void FFS1_2_3(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> COUP1, std::complex<double> COUP2, double M3, double
    W3, std::complex<double> S3[]);

void FFV2_3_0(std::complex<double> F1[], std::complex<double> F2[],
    std::complex<double> V3[], std::complex<double> COUP1, std::complex<double>
    COUP2, std::complex<double> & vertex);

}  // end namespace MG5_scotogenic_UFO

#endif // HelAmps_scotogenic_UFO_H
