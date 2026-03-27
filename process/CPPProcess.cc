//==========================================================================
// This file has been automatically generated for C++ Standalone by
// MadGraph5_aMC@NLO v. 3.6.6, 2025-10-30
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#include "CPPProcess.h"
#include "HelAmps_scotogenic_UFO.h"

using namespace MG5_scotogenic_UFO; 

//==========================================================================
// Class member functions for calculating the matrix elements for
// Process: n3 n3 > nu3 nu3 BSM<=1 HIG<=1 HIW<=1 WEIGHTED<=4 @1

//--------------------------------------------------------------------------
// Initialize process.

void CPPProcess::initProc(string param_card_name) 
{
  // Instantiate the model class and set parameters that stay fixed during run
  pars = Parameters_scotogenic_UFO::getInstance(); 
  SLHAReader slha(param_card_name); 
  pars->setIndependentParameters(slha); 
  pars->setIndependentCouplings(); 
  // pars->printIndependentParameters();
  // pars->printIndependentCouplings();
  // Set masses and degrees of freedom of new particles
  newMasses.push_back(pars->mdl_MN1); 
  newDOF.push_back({pars->mdl_MN1, 2.0}); 
  newMasses.push_back(pars->mdl_MN2); 
  newDOF.push_back({pars->mdl_MN2, 2.0}); 
  newMasses.push_back(pars->mdl_MN3); 
  newDOF.push_back({pars->mdl_MN3, 2.0}); 
  newMasses.push_back(pars->mdl_MetR); 
  newDOF.push_back({pars->mdl_MetR, 1.0}); 
  newMasses.push_back(pars->mdl_MetI); 
  newDOF.push_back({pars->mdl_MetI, 1.0}); 
  newMasses.push_back(pars->mdl_Metp); 
  newDOF.push_back({pars->mdl_Metp, 1.0}); 
  newMasses.push_back(pars->mdl_Metp); 
  newDOF.push_back({pars->mdl_Metp, 1.0}); 
  // Set external particle masses for this matrix element
  mME.push_back(pars->mdl_MN3); 
  mME.push_back(pars->mdl_MN3); 
  mME.push_back(pars->ZERO); 
  mME.push_back(pars->ZERO); 
  jamp2[0] = new double[1]; 
}

//--------------------------------------------------------------------------
// Evaluate |M|^2, part independent of incoming flavour.

double CPPProcess::sigmaKin(double s, double theta) 
{
  // Set the parameters which change event by event
  pars->setDependentParameters(); 
  pars->setDependentCouplings(); 
  static bool firsttime = true; 
  if (firsttime)
  {
    // pars->printDependentParameters();
    // pars->printDependentCouplings();
    firsttime = false; 
  }

  // Reset color flows
  for(int i = 0; i < 1; i++ )
    jamp2[0][i] = 0.; 

  // Local variables and constants
  const int ncomb = 16; 
  static bool goodhel[ncomb] = {ncomb * false}; 
  static int ntry = 0, sum_hel = 0, ngood = 0; 
  static int igood[ncomb]; 
  static int jhel; 
  std::complex<double> * * wfs; 
  double t[nprocesses]; 
  // Helicities for the process
  static const int helicities[ncomb][nexternal] = {{-1, -1, -1, -1}, {-1, -1,
      -1, 1}, {-1, -1, 1, -1}, {-1, -1, 1, 1}, {-1, 1, -1, -1}, {-1, 1, -1, 1},
      {-1, 1, 1, -1}, {-1, 1, 1, 1}, {1, -1, -1, -1}, {1, -1, -1, 1}, {1, -1,
      1, -1}, {1, -1, 1, 1}, {1, 1, -1, -1}, {1, 1, -1, 1}, {1, 1, 1, -1}, {1,
      1, 1, 1}};
  // Denominators: spins, colors and identical particles
  const int denominators[nprocesses] = {8}; 

  ntry = ntry + 1; 

  // Reset the matrix elements
  for(int i = 0; i < nprocesses; i++ )
  {
    matrix_element[i] = 0.; 
  }
  // Define permutation
  int perm[nexternal]; 
  for(int i = 0; i < nexternal; i++ )
  {
    perm[i] = i; 
  }

  if (sum_hel == 0 || ntry < 10)
  {
    // Calculate the matrix element for all helicities
    for(int ihel = 0; ihel < ncomb; ihel++ )
    {
      if (goodhel[ihel] || ntry < 2)
      {
        calculate_wavefunctions(perm, helicities[ihel]); 
        t[0] = matrix_1_n3n3_nu3nu3(); 

        double tsum = 0; 
        for(int iproc = 0; iproc < nprocesses; iproc++ )
        {
          matrix_element[iproc] += t[iproc]; 
          tsum += t[iproc]; 
        }
        // Store which helicities give non-zero result
        if (tsum != 0. && !goodhel[ihel])
        {
          goodhel[ihel] = true; 
          ngood++; 
          igood[ngood] = ihel; 
        }
      }
    }
    jhel = 0; 
    sum_hel = min(sum_hel, ngood); 
  }
  else
  {
    // Only use the "good" helicities
    for(int j = 0; j < sum_hel; j++ )
    {
      jhel++; 
      if (jhel >= ngood)
        jhel = 0; 
      double hwgt = double(ngood)/double(sum_hel); 
      int ihel = igood[jhel]; 
      calculate_wavefunctions(perm, helicities[ihel]); 
      t[0] = matrix_1_n3n3_nu3nu3(); 

      for(int iproc = 0; iproc < nprocesses; iproc++ )
      {
        matrix_element[iproc] += t[iproc] * hwgt; 
      }
    }
  }

  for (int i = 0; i < nprocesses; i++ )
    matrix_element[i] /= denominators[i]; 

  return matrix_element[0] * std::sin(theta); 


}

//--------------------------------------------------------------------------
// Evaluate |M|^2, including incoming flavour dependence.

double CPPProcess::sigmaHat() 
{
  // Select between the different processes
  if(id1 == 1016 && id2 == 1016)
  {
    // Add matrix elements for processes with beams (1016, 1016)
    return matrix_element[0]; 
  }
  else
  {
    // Return 0 if not correct initial state assignment
    return 0.; 
  }
}

//==========================================================================
// Private class member functions

//--------------------------------------------------------------------------
// Evaluate |M|^2 for each subprocess

void CPPProcess::calculate_wavefunctions(const int perm[], const int hel[])
{
  // Calculate wavefunctions for all processes
  int i, j; 

  // Calculate all wavefunctions
  ixxxxx(p[perm[0]], mME[0], hel[0], +1, w[0]); 
  ixxxxx(p[perm[1]], mME[1], hel[1], +1, w[1]); 
  oxxxxx(p[perm[2]], mME[2], hel[2], +1, w[2]); 
  oxxxxx(p[perm[3]], mME[3], hel[3], +1, w[3]); 
  FFS1_2_3(w[0], w[2], pars->GC_134, pars->GC_135, pars->mdl_MetI,
      pars->mdl_WetI, w[4]);
  FFS1_2_3(w[0], w[2], pars->GC_161, pars->GC_162, pars->mdl_MetR,
      pars->mdl_WetR, w[5]);
  FFS1_2_3(w[0], w[3], pars->GC_134, pars->GC_135, pars->mdl_MetI,
      pars->mdl_WetI, w[6]);
  FFS1_2_3(w[0], w[3], pars->GC_161, pars->GC_162, pars->mdl_MetR,
      pars->mdl_WetR, w[7]);

  // Calculate all amplitudes
  // Amplitude(s) for diagram number 0
  FFS1_2_0(w[1], w[3], w[4], pars->GC_134, pars->GC_135, amp[0]); 
  FFS1_2_0(w[1], w[3], w[5], pars->GC_161, pars->GC_162, amp[1]); 
  FFS1_2_0(w[1], w[2], w[6], pars->GC_134, pars->GC_135, amp[2]); 
  FFS1_2_0(w[1], w[2], w[7], pars->GC_161, pars->GC_162, amp[3]); 

}
double CPPProcess::matrix_1_n3n3_nu3nu3() 
{

  // Local variables
  const int ngraphs = 4; 
  const int ncolor = 1; 
  std::complex<double> ztemp; 
  std::complex<double> jamp[ncolor]; 
  // The color matrix;
  static const int denom = 1; 
  static const int cf[ncolor * (ncolor + 1)/2] = {1}; 

  // Calculate color flows
  jamp[0] = -amp[0] - amp[1] + amp[2] + amp[3]; 

  // Sum and square the color flows to get the matrix element
  double matrix = 0; 
  int cf_index = 0; 
  for(int i = 0; i < ncolor; i++ )
  {
    ztemp = 0.; 
    for(int j = i; j < ncolor; j++ , cf_index++ )
    {
      ztemp = ztemp + static_cast<double> (cf[cf_index]) * jamp[j]; 
    }
    matrix = matrix + real(ztemp * conj(jamp[i])); 
  }
  matrix = matrix/denom; 

  // Store the leading color flows for choice of color
  for(int i = 0; i < ncolor; i++ )
    jamp2[0][i] += real(jamp[i] * conj(jamp[i])); 

  return matrix; 
}



