//==========================================================================
// This file has been automatically generated for C++ by
// MadGraph5_aMC@NLO v. 3.6.7, 2026-01-05
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#include <iostream>
#include <iomanip>
#include "Parameters_scotogenic_UFO.h"

// Initialize static instance
Parameters_scotogenic_UFO * Parameters_scotogenic_UFO::instance = 0; 

// Function to get static instance - only one instance per program
Parameters_scotogenic_UFO * Parameters_scotogenic_UFO::getInstance()
{
  if (instance == 0)
    instance = new Parameters_scotogenic_UFO(); 

  return instance; 
}

void Parameters_scotogenic_UFO::setIndependentParameters(SLHAReader& slha)
{
  // Define "zero"
  zero = 0; 
  ZERO = 0; 
  // Prepare a vector for indices
  vector<int> indices(2, 0); 
  mdl_WN3 = slha.get_block_entry("decay", 1016, 0.000000e+00); 
  mdl_WN2 = slha.get_block_entry("decay", 1014, 0.000000e+00); 
  mdl_WN1 = slha.get_block_entry("decay", 1012, 0.000000e+00); 
  mdl_WetI = slha.get_block_entry("decay", 1002, 0.000000e+00); 
  mdl_WetR = slha.get_block_entry("decay", 1001, 0.000000e+00); 
  mdl_Wh = slha.get_block_entry("decay", 25, 0.000000e+00); 
  mdl_WWp = slha.get_block_entry("decay", 24, 2.141000e+00); 
  mdl_WZ = slha.get_block_entry("decay", 23, 2.495200e+00); 
  mdl_Wu3 = slha.get_block_entry("decay", 6, 1.510000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZX33 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZX32 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZX31 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZX23 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZX22 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZX21 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZX13 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZX12 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZX11 = slha.get_block_entry("zxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rYn33 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rYn32 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rYn31 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rYn23 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rYn22 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rYn21 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rYn13 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rYn12 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rYn11 = slha.get_block_entry("yn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rUV33 = slha.get_block_entry("uvmix", indices, 1.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rUV32 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rUV31 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rUV23 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rUV22 = slha.get_block_entry("uvmix", indices, 1.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rUV21 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rUV13 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rUV12 = slha.get_block_entry("uvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rUV11 = slha.get_block_entry("uvmix", indices, 1.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZUR33 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZUR32 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZUR31 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZUR23 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZUR22 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZUR21 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZUR13 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZUR12 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZUR11 = slha.get_block_entry("uurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZUL33 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZUL32 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZUL31 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZUL23 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZUL22 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZUL21 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZUL13 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZUL12 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZUL11 = slha.get_block_entry("uulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZER33 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZER32 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZER31 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZER23 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZER22 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZER21 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZER13 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZER12 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZER11 = slha.get_block_entry("uermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZEL33 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZEL32 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZEL31 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZEL23 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZEL22 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZEL21 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZEL13 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZEL12 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZEL11 = slha.get_block_entry("uelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZDR33 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZDR32 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZDR31 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZDR23 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZDR22 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZDR21 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZDR13 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZDR12 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZDR11 = slha.get_block_entry("udrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_rZDL33 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_rZDL32 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_rZDL31 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_rZDL23 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_rZDL22 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_rZDL21 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_rZDL13 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_rZDL12 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_rZDL11 = slha.get_block_entry("udlmix", indices, 0.000000e+00); 
  aS = slha.get_block_entry("sminputs", 3, 1.190000e-01); 
  mdl_Gf = slha.get_block_entry("sminputs", 2, 1.166390e-05); 
  aEWM1 = slha.get_block_entry("sminputs", 1, 1.370360e+02); 
  mdl_MN3 = slha.get_block_entry("mass", 1016, 1.000000e+02); 
  mdl_MN2 = slha.get_block_entry("mass", 1014, 1.000000e+02); 
  mdl_MN1 = slha.get_block_entry("mass", 1012, 1.000000e+02); 
  mdl_Metp = slha.get_block_entry("mass", 1003, 1.000000e+02); 
  mdl_MetI = slha.get_block_entry("mass", 1002, 1.000000e+02); 
  mdl_MetR = slha.get_block_entry("mass", 1001, 1.000000e+02); 
  mdl_Mh = slha.get_block_entry("mass", 25, 1.000000e+02); 
  mdl_MZ = slha.get_block_entry("mass", 23, 9.118760e+01); 
  mdl_Me3 = slha.get_block_entry("mass", 15, 1.776000e+00); 
  mdl_Me2 = slha.get_block_entry("mass", 13, 1.050000e-01); 
  mdl_Me1 = slha.get_block_entry("mass", 11, 5.110000e-04); 
  mdl_Mu3 = slha.get_block_entry("mass", 6, 1.712000e+02); 
  mdl_Md3 = slha.get_block_entry("mass", 5, 4.200000e+00); 
  mdl_Mu2 = slha.get_block_entry("mass", 4, 1.270000e+00); 
  mdl_Md2 = slha.get_block_entry("mass", 3, 1.040000e-01); 
  mdl_Mu1 = slha.get_block_entry("mass", 2, 1.500000e-03); 
  mdl_Md1 = slha.get_block_entry("mass", 1, 3.500000e-03); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZX33 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZX32 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZX31 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZX23 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZX22 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZX21 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZX13 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZX12 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZX11 = slha.get_block_entry("imzxmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iYn33 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iYn32 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iYn31 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iYn23 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iYn22 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iYn21 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iYn13 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iYn12 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iYn11 = slha.get_block_entry("imyn", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iUV33 = slha.get_block_entry("imuvmix", indices, 1.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iUV32 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iUV31 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iUV23 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iUV22 = slha.get_block_entry("imuvmix", indices, 1.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iUV21 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iUV13 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iUV12 = slha.get_block_entry("imuvmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iUV11 = slha.get_block_entry("imuvmix", indices, 1.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZUR33 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZUR32 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZUR31 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZUR23 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZUR22 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZUR21 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZUR13 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZUR12 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZUR11 = slha.get_block_entry("imuurmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZUL33 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZUL32 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZUL31 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZUL23 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZUL22 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZUL21 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZUL13 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZUL12 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZUL11 = slha.get_block_entry("imuulmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZER33 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZER32 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZER31 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZER23 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZER22 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZER21 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZER13 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZER12 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZER11 = slha.get_block_entry("imuermix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZEL33 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZEL32 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZEL31 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZEL23 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZEL22 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZEL21 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZEL13 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZEL12 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZEL11 = slha.get_block_entry("imuelmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZDR33 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZDR32 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZDR31 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZDR23 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZDR22 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZDR21 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZDR13 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZDR12 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZDR11 = slha.get_block_entry("imudrmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 3; 
  mdl_iZDL33 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 2; 
  mdl_iZDL32 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 3; 
  indices[1] = 1; 
  mdl_iZDL31 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 3; 
  mdl_iZDL23 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 2; 
  mdl_iZDL22 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 2; 
  indices[1] = 1; 
  mdl_iZDL21 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 3; 
  mdl_iZDL13 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 2; 
  mdl_iZDL12 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  indices[0] = 1; 
  indices[1] = 1; 
  mdl_iZDL11 = slha.get_block_entry("imudlmix", indices, 0.000000e+00); 
  mdl_ilam4 = slha.get_block_entry("imhdm", 5, 0.000000e+00); 
  mdl_ilam3 = slha.get_block_entry("imhdm", 4, 0.000000e+00); 
  mdl_ilam2 = slha.get_block_entry("imhdm", 3, 0.000000e+00); 
  mdl_ilam1 = slha.get_block_entry("imhdm", 2, 0.000000e+00); 
  mdl_lam5 = slha.get_block_entry("hdm", 6, 0.000000e+00); 
  mdl_rlam4 = slha.get_block_entry("hdm", 5, 0.000000e+00); 
  mdl_rlam3 = slha.get_block_entry("hdm", 4, 0.000000e+00); 
  mdl_rlam2 = slha.get_block_entry("hdm", 3, 0.000000e+00); 
  mdl_rlam1 = slha.get_block_entry("hdm", 2, 0.000000e+00); 
  mdl_complexi = std::complex<double> (0., 1.); 
  mdl_Yn11 = mdl_rYn11 + mdl_complexi * mdl_iYn11; 
  mdl_Yn12 = mdl_rYn12 + mdl_complexi * mdl_iYn12; 
  mdl_Yn13 = mdl_rYn13 + mdl_complexi * mdl_iYn13; 
  mdl_Yn21 = mdl_rYn21 + mdl_complexi * mdl_iYn21; 
  mdl_Yn22 = mdl_rYn22 + mdl_complexi * mdl_iYn22; 
  mdl_Yn23 = mdl_rYn23 + mdl_complexi * mdl_iYn23; 
  mdl_Yn31 = mdl_rYn31 + mdl_complexi * mdl_iYn31; 
  mdl_Yn32 = mdl_rYn32 + mdl_complexi * mdl_iYn32; 
  mdl_Yn33 = mdl_rYn33 + mdl_complexi * mdl_iYn33; 
  mdl_lam1 = mdl_rlam1 + mdl_complexi * mdl_ilam1; 
  mdl_lam2 = mdl_rlam2 + mdl_complexi * mdl_ilam2; 
  mdl_lam4 = mdl_rlam4 + mdl_complexi * mdl_ilam4; 
  mdl_lam3 = mdl_rlam3 + mdl_complexi * mdl_ilam3; 
  mdl_ZX11 = mdl_rZX11 + mdl_complexi * mdl_iZX11; 
  mdl_ZX12 = mdl_rZX12 + mdl_complexi * mdl_iZX12; 
  mdl_ZX13 = mdl_rZX13 + mdl_complexi * mdl_iZX13; 
  mdl_ZX21 = mdl_rZX21 + mdl_complexi * mdl_iZX21; 
  mdl_ZX22 = mdl_rZX22 + mdl_complexi * mdl_iZX22; 
  mdl_ZX23 = mdl_rZX23 + mdl_complexi * mdl_iZX23; 
  mdl_ZX31 = mdl_rZX31 + mdl_complexi * mdl_iZX31; 
  mdl_ZX32 = mdl_rZX32 + mdl_complexi * mdl_iZX32; 
  mdl_ZX33 = mdl_rZX33 + mdl_complexi * mdl_iZX33; 
  mdl_UV11 = mdl_rUV11 + mdl_complexi * mdl_iUV11; 
  mdl_UV12 = mdl_rUV12 + mdl_complexi * mdl_iUV12; 
  mdl_UV13 = mdl_rUV13 + mdl_complexi * mdl_iUV13; 
  mdl_UV21 = mdl_rUV21 + mdl_complexi * mdl_iUV21; 
  mdl_UV22 = mdl_rUV22 + mdl_complexi * mdl_iUV22; 
  mdl_UV23 = mdl_rUV23 + mdl_complexi * mdl_iUV23; 
  mdl_UV31 = mdl_rUV31 + mdl_complexi * mdl_iUV31; 
  mdl_UV32 = mdl_rUV32 + mdl_complexi * mdl_iUV32; 
  mdl_UV33 = mdl_rUV33 + mdl_complexi * mdl_iUV33; 
  mdl_ZDL11 = mdl_rZDL11 + mdl_complexi * mdl_iZDL11; 
  mdl_ZDL12 = mdl_rZDL12 + mdl_complexi * mdl_iZDL12; 
  mdl_ZDL13 = mdl_rZDL13 + mdl_complexi * mdl_iZDL13; 
  mdl_ZDL21 = mdl_rZDL21 + mdl_complexi * mdl_iZDL21; 
  mdl_ZDL22 = mdl_rZDL22 + mdl_complexi * mdl_iZDL22; 
  mdl_ZDL23 = mdl_rZDL23 + mdl_complexi * mdl_iZDL23; 
  mdl_ZDL31 = mdl_rZDL31 + mdl_complexi * mdl_iZDL31; 
  mdl_ZDL32 = mdl_rZDL32 + mdl_complexi * mdl_iZDL32; 
  mdl_ZDL33 = mdl_rZDL33 + mdl_complexi * mdl_iZDL33; 
  mdl_ZDR11 = mdl_rZDR11 + mdl_complexi * mdl_iZDR11; 
  mdl_ZDR12 = mdl_rZDR12 + mdl_complexi * mdl_iZDR12; 
  mdl_ZDR13 = mdl_rZDR13 + mdl_complexi * mdl_iZDR13; 
  mdl_ZDR21 = mdl_rZDR21 + mdl_complexi * mdl_iZDR21; 
  mdl_ZDR22 = mdl_rZDR22 + mdl_complexi * mdl_iZDR22; 
  mdl_ZDR23 = mdl_rZDR23 + mdl_complexi * mdl_iZDR23; 
  mdl_ZDR31 = mdl_rZDR31 + mdl_complexi * mdl_iZDR31; 
  mdl_ZDR32 = mdl_rZDR32 + mdl_complexi * mdl_iZDR32; 
  mdl_ZDR33 = mdl_rZDR33 + mdl_complexi * mdl_iZDR33; 
  mdl_ZUL11 = mdl_rZUL11 + mdl_complexi * mdl_iZUL11; 
  mdl_ZUL12 = mdl_rZUL12 + mdl_complexi * mdl_iZUL12; 
  mdl_ZUL13 = mdl_rZUL13 + mdl_complexi * mdl_iZUL13; 
  mdl_ZUL21 = mdl_rZUL21 + mdl_complexi * mdl_iZUL21; 
  mdl_ZUL22 = mdl_rZUL22 + mdl_complexi * mdl_iZUL22; 
  mdl_ZUL23 = mdl_rZUL23 + mdl_complexi * mdl_iZUL23; 
  mdl_ZUL31 = mdl_rZUL31 + mdl_complexi * mdl_iZUL31; 
  mdl_ZUL32 = mdl_rZUL32 + mdl_complexi * mdl_iZUL32; 
  mdl_ZUL33 = mdl_rZUL33 + mdl_complexi * mdl_iZUL33; 
  mdl_ZUR11 = mdl_rZUR11 + mdl_complexi * mdl_iZUR11; 
  mdl_ZUR12 = mdl_rZUR12 + mdl_complexi * mdl_iZUR12; 
  mdl_ZUR13 = mdl_rZUR13 + mdl_complexi * mdl_iZUR13; 
  mdl_ZUR21 = mdl_rZUR21 + mdl_complexi * mdl_iZUR21; 
  mdl_ZUR22 = mdl_rZUR22 + mdl_complexi * mdl_iZUR22; 
  mdl_ZUR23 = mdl_rZUR23 + mdl_complexi * mdl_iZUR23; 
  mdl_ZUR31 = mdl_rZUR31 + mdl_complexi * mdl_iZUR31; 
  mdl_ZUR32 = mdl_rZUR32 + mdl_complexi * mdl_iZUR32; 
  mdl_ZUR33 = mdl_rZUR33 + mdl_complexi * mdl_iZUR33; 
  mdl_ZEL11 = mdl_rZEL11 + mdl_complexi * mdl_iZEL11; 
  mdl_ZEL12 = mdl_rZEL12 + mdl_complexi * mdl_iZEL12; 
  mdl_ZEL13 = mdl_rZEL13 + mdl_complexi * mdl_iZEL13; 
  mdl_ZEL21 = mdl_rZEL21 + mdl_complexi * mdl_iZEL21; 
  mdl_ZEL22 = mdl_rZEL22 + mdl_complexi * mdl_iZEL22; 
  mdl_ZEL23 = mdl_rZEL23 + mdl_complexi * mdl_iZEL23; 
  mdl_ZEL31 = mdl_rZEL31 + mdl_complexi * mdl_iZEL31; 
  mdl_ZEL32 = mdl_rZEL32 + mdl_complexi * mdl_iZEL32; 
  mdl_ZEL33 = mdl_rZEL33 + mdl_complexi * mdl_iZEL33; 
  mdl_ZER11 = mdl_rZER11 + mdl_complexi * mdl_iZER11; 
  mdl_ZER12 = mdl_rZER12 + mdl_complexi * mdl_iZER12; 
  mdl_ZER13 = mdl_rZER13 + mdl_complexi * mdl_iZER13; 
  mdl_ZER21 = mdl_rZER21 + mdl_complexi * mdl_iZER21; 
  mdl_ZER22 = mdl_rZER22 + mdl_complexi * mdl_iZER22; 
  mdl_ZER23 = mdl_rZER23 + mdl_complexi * mdl_iZER23; 
  mdl_ZER31 = mdl_rZER31 + mdl_complexi * mdl_iZER31; 
  mdl_ZER32 = mdl_rZER32 + mdl_complexi * mdl_iZER32; 
  mdl_ZER33 = mdl_rZER33 + mdl_complexi * mdl_iZER33; 
  mdl_MZ__exp__2 = ((mdl_MZ) * (mdl_MZ)); 
  mdl_MZ__exp__4 = ((mdl_MZ) * (mdl_MZ) * (mdl_MZ) * (mdl_MZ)); 
  mdl_sqrt__2 = sqrt(2.); 
  mdl_Yu12 = 0.; 
  mdl_Yu13 = 0.; 
  mdl_Yu21 = 0.; 
  mdl_Yu23 = 0.; 
  mdl_Yu31 = 0.; 
  mdl_Yu32 = 0.; 
  mdl_Yd12 = 0.; 
  mdl_Yd13 = 0.; 
  mdl_Yd21 = 0.; 
  mdl_Yd23 = 0.; 
  mdl_Yd31 = 0.; 
  mdl_Yd32 = 0.; 
  mdl_Ye12 = 0.; 
  mdl_Ye13 = 0.; 
  mdl_Ye21 = 0.; 
  mdl_Ye23 = 0.; 
  mdl_Ye31 = 0.; 
  mdl_Ye32 = 0.; 
  mdl_RXiWp = 1.; 
  mdl_RXiZ = 1.; 
  mdl_MAh = mdl_MZ * mdl_RXiZ; 
  mdl_MgZ = mdl_MZ * mdl_RXiZ; 
  mdl_conjg__lam1 = conj(mdl_lam1); 
  mdl_conjg__lam3 = conj(mdl_lam3); 
  mdl_conjg__lam4 = conj(mdl_lam4); 
  mdl_conjg__ZDL11 = conj(mdl_ZDL11); 
  mdl_conjg__ZDR11 = conj(mdl_ZDR11); 
  mdl_conjg__ZDR12 = conj(mdl_ZDR12); 
  mdl_conjg__ZDR13 = conj(mdl_ZDR13); 
  mdl_conjg__ZDL12 = conj(mdl_ZDL12); 
  mdl_conjg__ZDL13 = conj(mdl_ZDL13); 
  mdl_conjg__Yd21 = conj(mdl_Yd21); 
  mdl_conjg__Yd31 = conj(mdl_Yd31); 
  mdl_conjg__Yd12 = conj(mdl_Yd12); 
  mdl_conjg__Yd32 = conj(mdl_Yd32); 
  mdl_conjg__Yd13 = conj(mdl_Yd13); 
  mdl_conjg__Yd23 = conj(mdl_Yd23); 
  mdl_conjg__ZDL21 = conj(mdl_ZDL21); 
  mdl_conjg__ZDL22 = conj(mdl_ZDL22); 
  mdl_conjg__ZDL23 = conj(mdl_ZDL23); 
  mdl_conjg__ZDL31 = conj(mdl_ZDL31); 
  mdl_conjg__ZDL32 = conj(mdl_ZDL32); 
  mdl_conjg__ZDL33 = conj(mdl_ZDL33); 
  mdl_conjg__ZDR21 = conj(mdl_ZDR21); 
  mdl_conjg__ZDR22 = conj(mdl_ZDR22); 
  mdl_conjg__ZDR23 = conj(mdl_ZDR23); 
  mdl_conjg__ZDR31 = conj(mdl_ZDR31); 
  mdl_conjg__ZDR32 = conj(mdl_ZDR32); 
  mdl_conjg__ZDR33 = conj(mdl_ZDR33); 
  mdl_conjg__ZEL11 = conj(mdl_ZEL11); 
  mdl_conjg__ZER11 = conj(mdl_ZER11); 
  mdl_conjg__ZER12 = conj(mdl_ZER12); 
  mdl_conjg__ZER13 = conj(mdl_ZER13); 
  mdl_conjg__ZEL12 = conj(mdl_ZEL12); 
  mdl_conjg__ZEL13 = conj(mdl_ZEL13); 
  mdl_conjg__Ye21 = conj(mdl_Ye21); 
  mdl_conjg__Ye31 = conj(mdl_Ye31); 
  mdl_conjg__Ye12 = conj(mdl_Ye12); 
  mdl_conjg__Ye32 = conj(mdl_Ye32); 
  mdl_conjg__Ye13 = conj(mdl_Ye13); 
  mdl_conjg__Ye23 = conj(mdl_Ye23); 
  mdl_conjg__ZEL21 = conj(mdl_ZEL21); 
  mdl_conjg__ZEL22 = conj(mdl_ZEL22); 
  mdl_conjg__ZEL23 = conj(mdl_ZEL23); 
  mdl_conjg__ZEL31 = conj(mdl_ZEL31); 
  mdl_conjg__ZEL32 = conj(mdl_ZEL32); 
  mdl_conjg__ZEL33 = conj(mdl_ZEL33); 
  mdl_conjg__ZER21 = conj(mdl_ZER21); 
  mdl_conjg__ZER22 = conj(mdl_ZER22); 
  mdl_conjg__ZER23 = conj(mdl_ZER23); 
  mdl_conjg__ZER31 = conj(mdl_ZER31); 
  mdl_conjg__ZER32 = conj(mdl_ZER32); 
  mdl_conjg__ZER33 = conj(mdl_ZER33); 
  mdl_conjg__ZUL11 = conj(mdl_ZUL11); 
  mdl_conjg__ZUR11 = conj(mdl_ZUR11); 
  mdl_conjg__ZUR12 = conj(mdl_ZUR12); 
  mdl_conjg__ZUR13 = conj(mdl_ZUR13); 
  mdl_conjg__ZUL12 = conj(mdl_ZUL12); 
  mdl_conjg__ZUL13 = conj(mdl_ZUL13); 
  mdl_conjg__Yu21 = conj(mdl_Yu21); 
  mdl_conjg__Yu31 = conj(mdl_Yu31); 
  mdl_conjg__Yu12 = conj(mdl_Yu12); 
  mdl_conjg__Yu32 = conj(mdl_Yu32); 
  mdl_conjg__Yu13 = conj(mdl_Yu13); 
  mdl_conjg__Yu23 = conj(mdl_Yu23); 
  mdl_conjg__ZUL21 = conj(mdl_ZUL21); 
  mdl_conjg__ZUL22 = conj(mdl_ZUL22); 
  mdl_conjg__ZUL23 = conj(mdl_ZUL23); 
  mdl_conjg__ZUL31 = conj(mdl_ZUL31); 
  mdl_conjg__ZUL32 = conj(mdl_ZUL32); 
  mdl_conjg__ZUL33 = conj(mdl_ZUL33); 
  mdl_conjg__ZUR21 = conj(mdl_ZUR21); 
  mdl_conjg__ZUR22 = conj(mdl_ZUR22); 
  mdl_conjg__ZUR23 = conj(mdl_ZUR23); 
  mdl_conjg__ZUR31 = conj(mdl_ZUR31); 
  mdl_conjg__ZUR32 = conj(mdl_ZUR32); 
  mdl_conjg__ZUR33 = conj(mdl_ZUR33); 
  mdl_conjg__UV11 = conj(mdl_UV11); 
  mdl_conjg__ZX11 = conj(mdl_ZX11); 
  mdl_conjg__ZX12 = conj(mdl_ZX12); 
  mdl_conjg__ZX13 = conj(mdl_ZX13); 
  mdl_conjg__UV12 = conj(mdl_UV12); 
  mdl_conjg__UV13 = conj(mdl_UV13); 
  mdl_conjg__Yn11 = conj(mdl_Yn11); 
  mdl_conjg__Yn21 = conj(mdl_Yn21); 
  mdl_conjg__Yn31 = conj(mdl_Yn31); 
  mdl_conjg__Yn12 = conj(mdl_Yn12); 
  mdl_conjg__Yn22 = conj(mdl_Yn22); 
  mdl_conjg__Yn32 = conj(mdl_Yn32); 
  mdl_conjg__Yn13 = conj(mdl_Yn13); 
  mdl_conjg__Yn23 = conj(mdl_Yn23); 
  mdl_conjg__Yn33 = conj(mdl_Yn33); 
  mdl_conjg__UV21 = conj(mdl_UV21); 
  mdl_conjg__UV22 = conj(mdl_UV22); 
  mdl_conjg__UV23 = conj(mdl_UV23); 
  mdl_conjg__UV31 = conj(mdl_UV31); 
  mdl_conjg__UV32 = conj(mdl_UV32); 
  mdl_conjg__UV33 = conj(mdl_UV33); 
  mdl_conjg__ZX21 = conj(mdl_ZX21); 
  mdl_conjg__ZX22 = conj(mdl_ZX22); 
  mdl_conjg__ZX23 = conj(mdl_ZX23); 
  mdl_conjg__ZX31 = conj(mdl_ZX31); 
  mdl_conjg__ZX32 = conj(mdl_ZX32); 
  mdl_conjg__ZX33 = conj(mdl_ZX33); 
  mdl_el = 2. * sqrt(1./aEWM1) * sqrt(M_PI); 
  mdl_MWp = sqrt(mdl_MZ__exp__2/2. + sqrt(mdl_MZ__exp__4/4. - (mdl_MZ__exp__2 *
      M_PI)/(mdl_sqrt__2 * aEWM1 * mdl_Gf)));
  mdl_MWp__exp__2 = ((mdl_MWp) * (mdl_MWp)); 
  mdl_TW = asin(sqrt(1. - mdl_MWp__exp__2/mdl_MZ__exp__2)); 
  mdl_cos__TW = cos(mdl_TW); 
  mdl_g1 = mdl_el * 1./mdl_cos__TW; 
  mdl_sin__TW = sin(mdl_TW); 
  mdl_g2 = mdl_el * 1./mdl_sin__TW; 
  mdl_g2__exp__2 = ((mdl_g2) * (mdl_g2)); 
  mdl_v = 2. * sqrt(mdl_MWp__exp__2/mdl_g2__exp__2); 
  mdl_Yu11 = (mdl_sqrt__2 * mdl_Mu1)/mdl_v; 
  mdl_Yu22 = (mdl_sqrt__2 * mdl_Mu2)/mdl_v; 
  mdl_Yu33 = (mdl_sqrt__2 * mdl_Mu3)/mdl_v; 
  mdl_Yd11 = (mdl_sqrt__2 * mdl_Md1)/mdl_v; 
  mdl_Yd22 = (mdl_sqrt__2 * mdl_Md2)/mdl_v; 
  mdl_Yd33 = (mdl_sqrt__2 * mdl_Md3)/mdl_v; 
  mdl_Ye11 = (mdl_sqrt__2 * mdl_Me1)/mdl_v; 
  mdl_Ye22 = (mdl_sqrt__2 * mdl_Me2)/mdl_v; 
  mdl_Ye33 = (mdl_sqrt__2 * mdl_Me3)/mdl_v; 
  mdl_MHp = mdl_MWp * mdl_RXiWp; 
  mdl_MgWp = mdl_MWp * mdl_RXiWp; 
  mdl_MgWC = mdl_MWp * mdl_RXiWp; 
  mdl_g1__exp__2 = ((mdl_g1) * (mdl_g1)); 
  mdl_conjg__Yd11 = conj(mdl_Yd11); 
  mdl_conjg__Yd22 = conj(mdl_Yd22); 
  mdl_conjg__Yd33 = conj(mdl_Yd33); 
  mdl_conjg__Ye11 = conj(mdl_Ye11); 
  mdl_conjg__Ye22 = conj(mdl_Ye22); 
  mdl_conjg__Ye33 = conj(mdl_Ye33); 
  mdl_conjg__Yu11 = conj(mdl_Yu11); 
  mdl_conjg__Yu22 = conj(mdl_Yu22); 
  mdl_conjg__Yu33 = conj(mdl_Yu33); 
  if (mdl_MN1 < 0)
    mdl_WN1 = -abs(mdl_WN1); 
  if (mdl_MN2 < 0)
    mdl_WN2 = -abs(mdl_WN2); 
  if (mdl_MN3 < 0)
    mdl_WN3 = -abs(mdl_WN3); 
}
void Parameters_scotogenic_UFO::setIndependentCouplings()
{
  GC_3 = -1. * mdl_complexi * mdl_v * (-mdl_lam5 + mdl_conjg__lam3 +
      mdl_conjg__lam4);
  GC_7 = -1. * mdl_complexi * mdl_v * mdl_conjg__lam3; 
  GC_8 = -1. * mdl_complexi * mdl_v * (mdl_lam5 + mdl_conjg__lam3 +
      mdl_conjg__lam4);
  GC_10 = -3. * mdl_complexi * mdl_v * mdl_conjg__lam1; 
  GC_12 = 1./2. * mdl_complexi * mdl_g2__exp__2; 
  GC_13 = 1./2. * mdl_complexi * ((mdl_g2 * mdl_cos__TW + mdl_g1 * mdl_sin__TW)
      * (mdl_g2 * mdl_cos__TW + mdl_g1 * mdl_sin__TW));
  GC_14 = (mdl_g1 * mdl_g2 * mdl_cos__TW)/2.; 
  GC_15 = -(mdl_g1 * mdl_g2 * mdl_sin__TW)/2.; 
  GC_16 = -(mdl_g1 * mdl_g2 * mdl_cos__TW)/2.; 
  GC_17 = (mdl_g1 * mdl_g2 * mdl_sin__TW)/2.; 
  GC_24 = 1./2. * mdl_complexi * mdl_g1 * mdl_g2 * mdl_cos__TW; 
  GC_25 = -1./2. * mdl_complexi * mdl_g1 * mdl_g2 * mdl_sin__TW; 
  GC_26 = 1./2. * mdl_complexi * ((mdl_g1 * mdl_cos__TW + mdl_g2 * mdl_sin__TW)
      * (mdl_g1 * mdl_cos__TW + mdl_g2 * mdl_sin__TW));
  GC_27 = -1./4. * mdl_complexi * (-2. * mdl_g1 * mdl_g2 * cos(2. * mdl_TW) +
      (mdl_g1__exp__2 - mdl_g2__exp__2) * sin(2. * mdl_TW));
  GC_29 = 1./2. * mdl_complexi * ((mdl_g2 * mdl_cos__TW - mdl_g1 * mdl_sin__TW)
      * (mdl_g2 * mdl_cos__TW - mdl_g1 * mdl_sin__TW));
  GC_44 = (mdl_g2 * mdl_cos__TW + mdl_g1 * mdl_sin__TW)/2.; 
  GC_45 = -mdl_g2/2.; 
  GC_50 = 1./2. * mdl_complexi * mdl_g2; 
  GC_51 = 1./2. * mdl_complexi * (mdl_g1 * mdl_cos__TW + mdl_g2 * mdl_sin__TW); 
  GC_52 = 1./2. * mdl_complexi * (mdl_g2 * mdl_cos__TW - mdl_g1 * mdl_sin__TW); 
  GC_58 = 1./2. * mdl_complexi * mdl_g2__exp__2 * mdl_v; 
  GC_59 = 1./2. * mdl_complexi * mdl_v * ((mdl_g2 * mdl_cos__TW + mdl_g1 *
      mdl_sin__TW) * (mdl_g2 * mdl_cos__TW + mdl_g1 * mdl_sin__TW));
  GC_172 = (1. * mdl_complexi * (mdl_conjg__ZDL11 * (mdl_Yd11 *
      mdl_conjg__ZDR11 + mdl_Yd21 * mdl_conjg__ZDR12 + mdl_Yd31 *
      mdl_conjg__ZDR13) + mdl_conjg__ZDL12 * (mdl_Yd12 * mdl_conjg__ZDR11 +
      mdl_Yd22 * mdl_conjg__ZDR12 + mdl_Yd32 * mdl_conjg__ZDR13) +
      mdl_conjg__ZDL13 * (mdl_Yd13 * mdl_conjg__ZDR11 + mdl_Yd23 *
      mdl_conjg__ZDR12 + mdl_Yd33 * mdl_conjg__ZDR13)))/mdl_sqrt__2;
  GC_173 = (1. * mdl_complexi * (mdl_ZDL11 * (mdl_ZDR11 * mdl_conjg__Yd11 +
      mdl_ZDR12 * mdl_conjg__Yd21 + mdl_ZDR13 * mdl_conjg__Yd31) + mdl_ZDL12 *
      (mdl_ZDR11 * mdl_conjg__Yd12 + mdl_ZDR12 * mdl_conjg__Yd22 + mdl_ZDR13 *
      mdl_conjg__Yd32) + mdl_ZDL13 * (mdl_ZDR11 * mdl_conjg__Yd13 + mdl_ZDR12 *
      mdl_conjg__Yd23 + mdl_ZDR13 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_174 = (1. * mdl_complexi * (mdl_conjg__ZDL21 * (mdl_Yd11 *
      mdl_conjg__ZDR11 + mdl_Yd21 * mdl_conjg__ZDR12 + mdl_Yd31 *
      mdl_conjg__ZDR13) + mdl_conjg__ZDL22 * (mdl_Yd12 * mdl_conjg__ZDR11 +
      mdl_Yd22 * mdl_conjg__ZDR12 + mdl_Yd32 * mdl_conjg__ZDR13) +
      mdl_conjg__ZDL23 * (mdl_Yd13 * mdl_conjg__ZDR11 + mdl_Yd23 *
      mdl_conjg__ZDR12 + mdl_Yd33 * mdl_conjg__ZDR13)))/mdl_sqrt__2;
  GC_175 = (1. * mdl_complexi * (mdl_ZDL11 * (mdl_ZDR21 * mdl_conjg__Yd11 +
      mdl_ZDR22 * mdl_conjg__Yd21 + mdl_ZDR23 * mdl_conjg__Yd31) + mdl_ZDL12 *
      (mdl_ZDR21 * mdl_conjg__Yd12 + mdl_ZDR22 * mdl_conjg__Yd22 + mdl_ZDR23 *
      mdl_conjg__Yd32) + mdl_ZDL13 * (mdl_ZDR21 * mdl_conjg__Yd13 + mdl_ZDR22 *
      mdl_conjg__Yd23 + mdl_ZDR23 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_176 = (1. * mdl_complexi * (mdl_conjg__ZDL31 * (mdl_Yd11 *
      mdl_conjg__ZDR11 + mdl_Yd21 * mdl_conjg__ZDR12 + mdl_Yd31 *
      mdl_conjg__ZDR13) + mdl_conjg__ZDL32 * (mdl_Yd12 * mdl_conjg__ZDR11 +
      mdl_Yd22 * mdl_conjg__ZDR12 + mdl_Yd32 * mdl_conjg__ZDR13) +
      mdl_conjg__ZDL33 * (mdl_Yd13 * mdl_conjg__ZDR11 + mdl_Yd23 *
      mdl_conjg__ZDR12 + mdl_Yd33 * mdl_conjg__ZDR13)))/mdl_sqrt__2;
  GC_177 = (1. * mdl_complexi * (mdl_ZDL11 * (mdl_ZDR31 * mdl_conjg__Yd11 +
      mdl_ZDR32 * mdl_conjg__Yd21 + mdl_ZDR33 * mdl_conjg__Yd31) + mdl_ZDL12 *
      (mdl_ZDR31 * mdl_conjg__Yd12 + mdl_ZDR32 * mdl_conjg__Yd22 + mdl_ZDR33 *
      mdl_conjg__Yd32) + mdl_ZDL13 * (mdl_ZDR31 * mdl_conjg__Yd13 + mdl_ZDR32 *
      mdl_conjg__Yd23 + mdl_ZDR33 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_178 = (1. * mdl_complexi * (mdl_conjg__ZDL11 * (mdl_Yd11 *
      mdl_conjg__ZDR21 + mdl_Yd21 * mdl_conjg__ZDR22 + mdl_Yd31 *
      mdl_conjg__ZDR23) + mdl_conjg__ZDL12 * (mdl_Yd12 * mdl_conjg__ZDR21 +
      mdl_Yd22 * mdl_conjg__ZDR22 + mdl_Yd32 * mdl_conjg__ZDR23) +
      mdl_conjg__ZDL13 * (mdl_Yd13 * mdl_conjg__ZDR21 + mdl_Yd23 *
      mdl_conjg__ZDR22 + mdl_Yd33 * mdl_conjg__ZDR23)))/mdl_sqrt__2;
  GC_179 = (1. * mdl_complexi * (mdl_ZDL21 * (mdl_ZDR11 * mdl_conjg__Yd11 +
      mdl_ZDR12 * mdl_conjg__Yd21 + mdl_ZDR13 * mdl_conjg__Yd31) + mdl_ZDL22 *
      (mdl_ZDR11 * mdl_conjg__Yd12 + mdl_ZDR12 * mdl_conjg__Yd22 + mdl_ZDR13 *
      mdl_conjg__Yd32) + mdl_ZDL23 * (mdl_ZDR11 * mdl_conjg__Yd13 + mdl_ZDR12 *
      mdl_conjg__Yd23 + mdl_ZDR13 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_180 = (1. * mdl_complexi * (mdl_conjg__ZDL21 * (mdl_Yd11 *
      mdl_conjg__ZDR21 + mdl_Yd21 * mdl_conjg__ZDR22 + mdl_Yd31 *
      mdl_conjg__ZDR23) + mdl_conjg__ZDL22 * (mdl_Yd12 * mdl_conjg__ZDR21 +
      mdl_Yd22 * mdl_conjg__ZDR22 + mdl_Yd32 * mdl_conjg__ZDR23) +
      mdl_conjg__ZDL23 * (mdl_Yd13 * mdl_conjg__ZDR21 + mdl_Yd23 *
      mdl_conjg__ZDR22 + mdl_Yd33 * mdl_conjg__ZDR23)))/mdl_sqrt__2;
  GC_181 = (1. * mdl_complexi * (mdl_ZDL21 * (mdl_ZDR21 * mdl_conjg__Yd11 +
      mdl_ZDR22 * mdl_conjg__Yd21 + mdl_ZDR23 * mdl_conjg__Yd31) + mdl_ZDL22 *
      (mdl_ZDR21 * mdl_conjg__Yd12 + mdl_ZDR22 * mdl_conjg__Yd22 + mdl_ZDR23 *
      mdl_conjg__Yd32) + mdl_ZDL23 * (mdl_ZDR21 * mdl_conjg__Yd13 + mdl_ZDR22 *
      mdl_conjg__Yd23 + mdl_ZDR23 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_182 = (1. * mdl_complexi * (mdl_conjg__ZDL31 * (mdl_Yd11 *
      mdl_conjg__ZDR21 + mdl_Yd21 * mdl_conjg__ZDR22 + mdl_Yd31 *
      mdl_conjg__ZDR23) + mdl_conjg__ZDL32 * (mdl_Yd12 * mdl_conjg__ZDR21 +
      mdl_Yd22 * mdl_conjg__ZDR22 + mdl_Yd32 * mdl_conjg__ZDR23) +
      mdl_conjg__ZDL33 * (mdl_Yd13 * mdl_conjg__ZDR21 + mdl_Yd23 *
      mdl_conjg__ZDR22 + mdl_Yd33 * mdl_conjg__ZDR23)))/mdl_sqrt__2;
  GC_183 = (1. * mdl_complexi * (mdl_ZDL21 * (mdl_ZDR31 * mdl_conjg__Yd11 +
      mdl_ZDR32 * mdl_conjg__Yd21 + mdl_ZDR33 * mdl_conjg__Yd31) + mdl_ZDL22 *
      (mdl_ZDR31 * mdl_conjg__Yd12 + mdl_ZDR32 * mdl_conjg__Yd22 + mdl_ZDR33 *
      mdl_conjg__Yd32) + mdl_ZDL23 * (mdl_ZDR31 * mdl_conjg__Yd13 + mdl_ZDR32 *
      mdl_conjg__Yd23 + mdl_ZDR33 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_184 = (1. * mdl_complexi * (mdl_conjg__ZDL11 * (mdl_Yd11 *
      mdl_conjg__ZDR31 + mdl_Yd21 * mdl_conjg__ZDR32 + mdl_Yd31 *
      mdl_conjg__ZDR33) + mdl_conjg__ZDL12 * (mdl_Yd12 * mdl_conjg__ZDR31 +
      mdl_Yd22 * mdl_conjg__ZDR32 + mdl_Yd32 * mdl_conjg__ZDR33) +
      mdl_conjg__ZDL13 * (mdl_Yd13 * mdl_conjg__ZDR31 + mdl_Yd23 *
      mdl_conjg__ZDR32 + mdl_Yd33 * mdl_conjg__ZDR33)))/mdl_sqrt__2;
  GC_185 = (1. * mdl_complexi * (mdl_ZDL31 * (mdl_ZDR11 * mdl_conjg__Yd11 +
      mdl_ZDR12 * mdl_conjg__Yd21 + mdl_ZDR13 * mdl_conjg__Yd31) + mdl_ZDL32 *
      (mdl_ZDR11 * mdl_conjg__Yd12 + mdl_ZDR12 * mdl_conjg__Yd22 + mdl_ZDR13 *
      mdl_conjg__Yd32) + mdl_ZDL33 * (mdl_ZDR11 * mdl_conjg__Yd13 + mdl_ZDR12 *
      mdl_conjg__Yd23 + mdl_ZDR13 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_186 = (1. * mdl_complexi * (mdl_conjg__ZDL21 * (mdl_Yd11 *
      mdl_conjg__ZDR31 + mdl_Yd21 * mdl_conjg__ZDR32 + mdl_Yd31 *
      mdl_conjg__ZDR33) + mdl_conjg__ZDL22 * (mdl_Yd12 * mdl_conjg__ZDR31 +
      mdl_Yd22 * mdl_conjg__ZDR32 + mdl_Yd32 * mdl_conjg__ZDR33) +
      mdl_conjg__ZDL23 * (mdl_Yd13 * mdl_conjg__ZDR31 + mdl_Yd23 *
      mdl_conjg__ZDR32 + mdl_Yd33 * mdl_conjg__ZDR33)))/mdl_sqrt__2;
  GC_187 = (1. * mdl_complexi * (mdl_ZDL31 * (mdl_ZDR21 * mdl_conjg__Yd11 +
      mdl_ZDR22 * mdl_conjg__Yd21 + mdl_ZDR23 * mdl_conjg__Yd31) + mdl_ZDL32 *
      (mdl_ZDR21 * mdl_conjg__Yd12 + mdl_ZDR22 * mdl_conjg__Yd22 + mdl_ZDR23 *
      mdl_conjg__Yd32) + mdl_ZDL33 * (mdl_ZDR21 * mdl_conjg__Yd13 + mdl_ZDR22 *
      mdl_conjg__Yd23 + mdl_ZDR23 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_188 = (1. * mdl_complexi * (mdl_conjg__ZDL31 * (mdl_Yd11 *
      mdl_conjg__ZDR31 + mdl_Yd21 * mdl_conjg__ZDR32 + mdl_Yd31 *
      mdl_conjg__ZDR33) + mdl_conjg__ZDL32 * (mdl_Yd12 * mdl_conjg__ZDR31 +
      mdl_Yd22 * mdl_conjg__ZDR32 + mdl_Yd32 * mdl_conjg__ZDR33) +
      mdl_conjg__ZDL33 * (mdl_Yd13 * mdl_conjg__ZDR31 + mdl_Yd23 *
      mdl_conjg__ZDR32 + mdl_Yd33 * mdl_conjg__ZDR33)))/mdl_sqrt__2;
  GC_189 = (1. * mdl_complexi * (mdl_ZDL31 * (mdl_ZDR31 * mdl_conjg__Yd11 +
      mdl_ZDR32 * mdl_conjg__Yd21 + mdl_ZDR33 * mdl_conjg__Yd31) + mdl_ZDL32 *
      (mdl_ZDR31 * mdl_conjg__Yd12 + mdl_ZDR32 * mdl_conjg__Yd22 + mdl_ZDR33 *
      mdl_conjg__Yd32) + mdl_ZDL33 * (mdl_ZDR31 * mdl_conjg__Yd13 + mdl_ZDR32 *
      mdl_conjg__Yd23 + mdl_ZDR33 * mdl_conjg__Yd33)))/mdl_sqrt__2;
  GC_217 = (1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Ye11 *
      mdl_conjg__ZER11 + mdl_Ye21 * mdl_conjg__ZER12 + mdl_Ye31 *
      mdl_conjg__ZER13) + mdl_conjg__ZEL12 * (mdl_Ye12 * mdl_conjg__ZER11 +
      mdl_Ye22 * mdl_conjg__ZER12 + mdl_Ye32 * mdl_conjg__ZER13) +
      mdl_conjg__ZEL13 * (mdl_Ye13 * mdl_conjg__ZER11 + mdl_Ye23 *
      mdl_conjg__ZER12 + mdl_Ye33 * mdl_conjg__ZER13)))/mdl_sqrt__2;
  GC_218 = (1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZER11 * mdl_conjg__Ye11 +
      mdl_ZER12 * mdl_conjg__Ye21 + mdl_ZER13 * mdl_conjg__Ye31) + mdl_ZEL12 *
      (mdl_ZER11 * mdl_conjg__Ye12 + mdl_ZER12 * mdl_conjg__Ye22 + mdl_ZER13 *
      mdl_conjg__Ye32) + mdl_ZEL13 * (mdl_ZER11 * mdl_conjg__Ye13 + mdl_ZER12 *
      mdl_conjg__Ye23 + mdl_ZER13 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_219 = (1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Ye11 *
      mdl_conjg__ZER11 + mdl_Ye21 * mdl_conjg__ZER12 + mdl_Ye31 *
      mdl_conjg__ZER13) + mdl_conjg__ZEL22 * (mdl_Ye12 * mdl_conjg__ZER11 +
      mdl_Ye22 * mdl_conjg__ZER12 + mdl_Ye32 * mdl_conjg__ZER13) +
      mdl_conjg__ZEL23 * (mdl_Ye13 * mdl_conjg__ZER11 + mdl_Ye23 *
      mdl_conjg__ZER12 + mdl_Ye33 * mdl_conjg__ZER13)))/mdl_sqrt__2;
  GC_220 = (1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZER21 * mdl_conjg__Ye11 +
      mdl_ZER22 * mdl_conjg__Ye21 + mdl_ZER23 * mdl_conjg__Ye31) + mdl_ZEL12 *
      (mdl_ZER21 * mdl_conjg__Ye12 + mdl_ZER22 * mdl_conjg__Ye22 + mdl_ZER23 *
      mdl_conjg__Ye32) + mdl_ZEL13 * (mdl_ZER21 * mdl_conjg__Ye13 + mdl_ZER22 *
      mdl_conjg__Ye23 + mdl_ZER23 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_221 = (1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Ye11 *
      mdl_conjg__ZER11 + mdl_Ye21 * mdl_conjg__ZER12 + mdl_Ye31 *
      mdl_conjg__ZER13) + mdl_conjg__ZEL32 * (mdl_Ye12 * mdl_conjg__ZER11 +
      mdl_Ye22 * mdl_conjg__ZER12 + mdl_Ye32 * mdl_conjg__ZER13) +
      mdl_conjg__ZEL33 * (mdl_Ye13 * mdl_conjg__ZER11 + mdl_Ye23 *
      mdl_conjg__ZER12 + mdl_Ye33 * mdl_conjg__ZER13)))/mdl_sqrt__2;
  GC_222 = (1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZER31 * mdl_conjg__Ye11 +
      mdl_ZER32 * mdl_conjg__Ye21 + mdl_ZER33 * mdl_conjg__Ye31) + mdl_ZEL12 *
      (mdl_ZER31 * mdl_conjg__Ye12 + mdl_ZER32 * mdl_conjg__Ye22 + mdl_ZER33 *
      mdl_conjg__Ye32) + mdl_ZEL13 * (mdl_ZER31 * mdl_conjg__Ye13 + mdl_ZER32 *
      mdl_conjg__Ye23 + mdl_ZER33 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_223 = (1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Ye11 *
      mdl_conjg__ZER21 + mdl_Ye21 * mdl_conjg__ZER22 + mdl_Ye31 *
      mdl_conjg__ZER23) + mdl_conjg__ZEL12 * (mdl_Ye12 * mdl_conjg__ZER21 +
      mdl_Ye22 * mdl_conjg__ZER22 + mdl_Ye32 * mdl_conjg__ZER23) +
      mdl_conjg__ZEL13 * (mdl_Ye13 * mdl_conjg__ZER21 + mdl_Ye23 *
      mdl_conjg__ZER22 + mdl_Ye33 * mdl_conjg__ZER23)))/mdl_sqrt__2;
  GC_224 = (1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZER11 * mdl_conjg__Ye11 +
      mdl_ZER12 * mdl_conjg__Ye21 + mdl_ZER13 * mdl_conjg__Ye31) + mdl_ZEL22 *
      (mdl_ZER11 * mdl_conjg__Ye12 + mdl_ZER12 * mdl_conjg__Ye22 + mdl_ZER13 *
      mdl_conjg__Ye32) + mdl_ZEL23 * (mdl_ZER11 * mdl_conjg__Ye13 + mdl_ZER12 *
      mdl_conjg__Ye23 + mdl_ZER13 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_225 = (1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Ye11 *
      mdl_conjg__ZER21 + mdl_Ye21 * mdl_conjg__ZER22 + mdl_Ye31 *
      mdl_conjg__ZER23) + mdl_conjg__ZEL22 * (mdl_Ye12 * mdl_conjg__ZER21 +
      mdl_Ye22 * mdl_conjg__ZER22 + mdl_Ye32 * mdl_conjg__ZER23) +
      mdl_conjg__ZEL23 * (mdl_Ye13 * mdl_conjg__ZER21 + mdl_Ye23 *
      mdl_conjg__ZER22 + mdl_Ye33 * mdl_conjg__ZER23)))/mdl_sqrt__2;
  GC_226 = (1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZER21 * mdl_conjg__Ye11 +
      mdl_ZER22 * mdl_conjg__Ye21 + mdl_ZER23 * mdl_conjg__Ye31) + mdl_ZEL22 *
      (mdl_ZER21 * mdl_conjg__Ye12 + mdl_ZER22 * mdl_conjg__Ye22 + mdl_ZER23 *
      mdl_conjg__Ye32) + mdl_ZEL23 * (mdl_ZER21 * mdl_conjg__Ye13 + mdl_ZER22 *
      mdl_conjg__Ye23 + mdl_ZER23 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_227 = (1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Ye11 *
      mdl_conjg__ZER21 + mdl_Ye21 * mdl_conjg__ZER22 + mdl_Ye31 *
      mdl_conjg__ZER23) + mdl_conjg__ZEL32 * (mdl_Ye12 * mdl_conjg__ZER21 +
      mdl_Ye22 * mdl_conjg__ZER22 + mdl_Ye32 * mdl_conjg__ZER23) +
      mdl_conjg__ZEL33 * (mdl_Ye13 * mdl_conjg__ZER21 + mdl_Ye23 *
      mdl_conjg__ZER22 + mdl_Ye33 * mdl_conjg__ZER23)))/mdl_sqrt__2;
  GC_228 = (1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZER31 * mdl_conjg__Ye11 +
      mdl_ZER32 * mdl_conjg__Ye21 + mdl_ZER33 * mdl_conjg__Ye31) + mdl_ZEL22 *
      (mdl_ZER31 * mdl_conjg__Ye12 + mdl_ZER32 * mdl_conjg__Ye22 + mdl_ZER33 *
      mdl_conjg__Ye32) + mdl_ZEL23 * (mdl_ZER31 * mdl_conjg__Ye13 + mdl_ZER32 *
      mdl_conjg__Ye23 + mdl_ZER33 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_229 = (1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Ye11 *
      mdl_conjg__ZER31 + mdl_Ye21 * mdl_conjg__ZER32 + mdl_Ye31 *
      mdl_conjg__ZER33) + mdl_conjg__ZEL12 * (mdl_Ye12 * mdl_conjg__ZER31 +
      mdl_Ye22 * mdl_conjg__ZER32 + mdl_Ye32 * mdl_conjg__ZER33) +
      mdl_conjg__ZEL13 * (mdl_Ye13 * mdl_conjg__ZER31 + mdl_Ye23 *
      mdl_conjg__ZER32 + mdl_Ye33 * mdl_conjg__ZER33)))/mdl_sqrt__2;
  GC_230 = (1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZER11 * mdl_conjg__Ye11 +
      mdl_ZER12 * mdl_conjg__Ye21 + mdl_ZER13 * mdl_conjg__Ye31) + mdl_ZEL32 *
      (mdl_ZER11 * mdl_conjg__Ye12 + mdl_ZER12 * mdl_conjg__Ye22 + mdl_ZER13 *
      mdl_conjg__Ye32) + mdl_ZEL33 * (mdl_ZER11 * mdl_conjg__Ye13 + mdl_ZER12 *
      mdl_conjg__Ye23 + mdl_ZER13 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_231 = (1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Ye11 *
      mdl_conjg__ZER31 + mdl_Ye21 * mdl_conjg__ZER32 + mdl_Ye31 *
      mdl_conjg__ZER33) + mdl_conjg__ZEL22 * (mdl_Ye12 * mdl_conjg__ZER31 +
      mdl_Ye22 * mdl_conjg__ZER32 + mdl_Ye32 * mdl_conjg__ZER33) +
      mdl_conjg__ZEL23 * (mdl_Ye13 * mdl_conjg__ZER31 + mdl_Ye23 *
      mdl_conjg__ZER32 + mdl_Ye33 * mdl_conjg__ZER33)))/mdl_sqrt__2;
  GC_232 = (1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZER21 * mdl_conjg__Ye11 +
      mdl_ZER22 * mdl_conjg__Ye21 + mdl_ZER23 * mdl_conjg__Ye31) + mdl_ZEL32 *
      (mdl_ZER21 * mdl_conjg__Ye12 + mdl_ZER22 * mdl_conjg__Ye22 + mdl_ZER23 *
      mdl_conjg__Ye32) + mdl_ZEL33 * (mdl_ZER21 * mdl_conjg__Ye13 + mdl_ZER22 *
      mdl_conjg__Ye23 + mdl_ZER23 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_233 = (1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Ye11 *
      mdl_conjg__ZER31 + mdl_Ye21 * mdl_conjg__ZER32 + mdl_Ye31 *
      mdl_conjg__ZER33) + mdl_conjg__ZEL32 * (mdl_Ye12 * mdl_conjg__ZER31 +
      mdl_Ye22 * mdl_conjg__ZER32 + mdl_Ye32 * mdl_conjg__ZER33) +
      mdl_conjg__ZEL33 * (mdl_Ye13 * mdl_conjg__ZER31 + mdl_Ye23 *
      mdl_conjg__ZER32 + mdl_Ye33 * mdl_conjg__ZER33)))/mdl_sqrt__2;
  GC_234 = (1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZER31 * mdl_conjg__Ye11 +
      mdl_ZER32 * mdl_conjg__Ye21 + mdl_ZER33 * mdl_conjg__Ye31) + mdl_ZEL32 *
      (mdl_ZER31 * mdl_conjg__Ye12 + mdl_ZER32 * mdl_conjg__Ye22 + mdl_ZER33 *
      mdl_conjg__Ye32) + mdl_ZEL33 * (mdl_ZER31 * mdl_conjg__Ye13 + mdl_ZER32 *
      mdl_conjg__Ye23 + mdl_ZER33 * mdl_conjg__Ye33)))/mdl_sqrt__2;
  GC_235 = (-1. * mdl_complexi * (mdl_conjg__ZUL11 * (mdl_Yu11 *
      mdl_conjg__ZUR11 + mdl_Yu21 * mdl_conjg__ZUR12 + mdl_Yu31 *
      mdl_conjg__ZUR13) + mdl_conjg__ZUL12 * (mdl_Yu12 * mdl_conjg__ZUR11 +
      mdl_Yu22 * mdl_conjg__ZUR12 + mdl_Yu32 * mdl_conjg__ZUR13) +
      mdl_conjg__ZUL13 * (mdl_Yu13 * mdl_conjg__ZUR11 + mdl_Yu23 *
      mdl_conjg__ZUR12 + mdl_Yu33 * mdl_conjg__ZUR13)))/mdl_sqrt__2;
  GC_236 = (-1. * mdl_complexi * (mdl_ZUL11 * (mdl_ZUR11 * mdl_conjg__Yu11 +
      mdl_ZUR12 * mdl_conjg__Yu21 + mdl_ZUR13 * mdl_conjg__Yu31) + mdl_ZUL12 *
      (mdl_ZUR11 * mdl_conjg__Yu12 + mdl_ZUR12 * mdl_conjg__Yu22 + mdl_ZUR13 *
      mdl_conjg__Yu32) + mdl_ZUL13 * (mdl_ZUR11 * mdl_conjg__Yu13 + mdl_ZUR12 *
      mdl_conjg__Yu23 + mdl_ZUR13 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_237 = (-1. * mdl_complexi * (mdl_conjg__ZUL21 * (mdl_Yu11 *
      mdl_conjg__ZUR11 + mdl_Yu21 * mdl_conjg__ZUR12 + mdl_Yu31 *
      mdl_conjg__ZUR13) + mdl_conjg__ZUL22 * (mdl_Yu12 * mdl_conjg__ZUR11 +
      mdl_Yu22 * mdl_conjg__ZUR12 + mdl_Yu32 * mdl_conjg__ZUR13) +
      mdl_conjg__ZUL23 * (mdl_Yu13 * mdl_conjg__ZUR11 + mdl_Yu23 *
      mdl_conjg__ZUR12 + mdl_Yu33 * mdl_conjg__ZUR13)))/mdl_sqrt__2;
  GC_238 = (-1. * mdl_complexi * (mdl_ZUL11 * (mdl_ZUR21 * mdl_conjg__Yu11 +
      mdl_ZUR22 * mdl_conjg__Yu21 + mdl_ZUR23 * mdl_conjg__Yu31) + mdl_ZUL12 *
      (mdl_ZUR21 * mdl_conjg__Yu12 + mdl_ZUR22 * mdl_conjg__Yu22 + mdl_ZUR23 *
      mdl_conjg__Yu32) + mdl_ZUL13 * (mdl_ZUR21 * mdl_conjg__Yu13 + mdl_ZUR22 *
      mdl_conjg__Yu23 + mdl_ZUR23 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_239 = (-1. * mdl_complexi * (mdl_conjg__ZUL31 * (mdl_Yu11 *
      mdl_conjg__ZUR11 + mdl_Yu21 * mdl_conjg__ZUR12 + mdl_Yu31 *
      mdl_conjg__ZUR13) + mdl_conjg__ZUL32 * (mdl_Yu12 * mdl_conjg__ZUR11 +
      mdl_Yu22 * mdl_conjg__ZUR12 + mdl_Yu32 * mdl_conjg__ZUR13) +
      mdl_conjg__ZUL33 * (mdl_Yu13 * mdl_conjg__ZUR11 + mdl_Yu23 *
      mdl_conjg__ZUR12 + mdl_Yu33 * mdl_conjg__ZUR13)))/mdl_sqrt__2;
  GC_240 = (-1. * mdl_complexi * (mdl_ZUL11 * (mdl_ZUR31 * mdl_conjg__Yu11 +
      mdl_ZUR32 * mdl_conjg__Yu21 + mdl_ZUR33 * mdl_conjg__Yu31) + mdl_ZUL12 *
      (mdl_ZUR31 * mdl_conjg__Yu12 + mdl_ZUR32 * mdl_conjg__Yu22 + mdl_ZUR33 *
      mdl_conjg__Yu32) + mdl_ZUL13 * (mdl_ZUR31 * mdl_conjg__Yu13 + mdl_ZUR32 *
      mdl_conjg__Yu23 + mdl_ZUR33 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_241 = (-1. * mdl_complexi * (mdl_conjg__ZUL11 * (mdl_Yu11 *
      mdl_conjg__ZUR21 + mdl_Yu21 * mdl_conjg__ZUR22 + mdl_Yu31 *
      mdl_conjg__ZUR23) + mdl_conjg__ZUL12 * (mdl_Yu12 * mdl_conjg__ZUR21 +
      mdl_Yu22 * mdl_conjg__ZUR22 + mdl_Yu32 * mdl_conjg__ZUR23) +
      mdl_conjg__ZUL13 * (mdl_Yu13 * mdl_conjg__ZUR21 + mdl_Yu23 *
      mdl_conjg__ZUR22 + mdl_Yu33 * mdl_conjg__ZUR23)))/mdl_sqrt__2;
  GC_242 = (-1. * mdl_complexi * (mdl_ZUL21 * (mdl_ZUR11 * mdl_conjg__Yu11 +
      mdl_ZUR12 * mdl_conjg__Yu21 + mdl_ZUR13 * mdl_conjg__Yu31) + mdl_ZUL22 *
      (mdl_ZUR11 * mdl_conjg__Yu12 + mdl_ZUR12 * mdl_conjg__Yu22 + mdl_ZUR13 *
      mdl_conjg__Yu32) + mdl_ZUL23 * (mdl_ZUR11 * mdl_conjg__Yu13 + mdl_ZUR12 *
      mdl_conjg__Yu23 + mdl_ZUR13 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_243 = (-1. * mdl_complexi * (mdl_conjg__ZUL21 * (mdl_Yu11 *
      mdl_conjg__ZUR21 + mdl_Yu21 * mdl_conjg__ZUR22 + mdl_Yu31 *
      mdl_conjg__ZUR23) + mdl_conjg__ZUL22 * (mdl_Yu12 * mdl_conjg__ZUR21 +
      mdl_Yu22 * mdl_conjg__ZUR22 + mdl_Yu32 * mdl_conjg__ZUR23) +
      mdl_conjg__ZUL23 * (mdl_Yu13 * mdl_conjg__ZUR21 + mdl_Yu23 *
      mdl_conjg__ZUR22 + mdl_Yu33 * mdl_conjg__ZUR23)))/mdl_sqrt__2;
  GC_244 = (-1. * mdl_complexi * (mdl_ZUL21 * (mdl_ZUR21 * mdl_conjg__Yu11 +
      mdl_ZUR22 * mdl_conjg__Yu21 + mdl_ZUR23 * mdl_conjg__Yu31) + mdl_ZUL22 *
      (mdl_ZUR21 * mdl_conjg__Yu12 + mdl_ZUR22 * mdl_conjg__Yu22 + mdl_ZUR23 *
      mdl_conjg__Yu32) + mdl_ZUL23 * (mdl_ZUR21 * mdl_conjg__Yu13 + mdl_ZUR22 *
      mdl_conjg__Yu23 + mdl_ZUR23 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_245 = (-1. * mdl_complexi * (mdl_conjg__ZUL31 * (mdl_Yu11 *
      mdl_conjg__ZUR21 + mdl_Yu21 * mdl_conjg__ZUR22 + mdl_Yu31 *
      mdl_conjg__ZUR23) + mdl_conjg__ZUL32 * (mdl_Yu12 * mdl_conjg__ZUR21 +
      mdl_Yu22 * mdl_conjg__ZUR22 + mdl_Yu32 * mdl_conjg__ZUR23) +
      mdl_conjg__ZUL33 * (mdl_Yu13 * mdl_conjg__ZUR21 + mdl_Yu23 *
      mdl_conjg__ZUR22 + mdl_Yu33 * mdl_conjg__ZUR23)))/mdl_sqrt__2;
  GC_246 = (-1. * mdl_complexi * (mdl_ZUL21 * (mdl_ZUR31 * mdl_conjg__Yu11 +
      mdl_ZUR32 * mdl_conjg__Yu21 + mdl_ZUR33 * mdl_conjg__Yu31) + mdl_ZUL22 *
      (mdl_ZUR31 * mdl_conjg__Yu12 + mdl_ZUR32 * mdl_conjg__Yu22 + mdl_ZUR33 *
      mdl_conjg__Yu32) + mdl_ZUL23 * (mdl_ZUR31 * mdl_conjg__Yu13 + mdl_ZUR32 *
      mdl_conjg__Yu23 + mdl_ZUR33 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_247 = (-1. * mdl_complexi * (mdl_conjg__ZUL11 * (mdl_Yu11 *
      mdl_conjg__ZUR31 + mdl_Yu21 * mdl_conjg__ZUR32 + mdl_Yu31 *
      mdl_conjg__ZUR33) + mdl_conjg__ZUL12 * (mdl_Yu12 * mdl_conjg__ZUR31 +
      mdl_Yu22 * mdl_conjg__ZUR32 + mdl_Yu32 * mdl_conjg__ZUR33) +
      mdl_conjg__ZUL13 * (mdl_Yu13 * mdl_conjg__ZUR31 + mdl_Yu23 *
      mdl_conjg__ZUR32 + mdl_Yu33 * mdl_conjg__ZUR33)))/mdl_sqrt__2;
  GC_248 = (-1. * mdl_complexi * (mdl_ZUL31 * (mdl_ZUR11 * mdl_conjg__Yu11 +
      mdl_ZUR12 * mdl_conjg__Yu21 + mdl_ZUR13 * mdl_conjg__Yu31) + mdl_ZUL32 *
      (mdl_ZUR11 * mdl_conjg__Yu12 + mdl_ZUR12 * mdl_conjg__Yu22 + mdl_ZUR13 *
      mdl_conjg__Yu32) + mdl_ZUL33 * (mdl_ZUR11 * mdl_conjg__Yu13 + mdl_ZUR12 *
      mdl_conjg__Yu23 + mdl_ZUR13 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_249 = (-1. * mdl_complexi * (mdl_conjg__ZUL21 * (mdl_Yu11 *
      mdl_conjg__ZUR31 + mdl_Yu21 * mdl_conjg__ZUR32 + mdl_Yu31 *
      mdl_conjg__ZUR33) + mdl_conjg__ZUL22 * (mdl_Yu12 * mdl_conjg__ZUR31 +
      mdl_Yu22 * mdl_conjg__ZUR32 + mdl_Yu32 * mdl_conjg__ZUR33) +
      mdl_conjg__ZUL23 * (mdl_Yu13 * mdl_conjg__ZUR31 + mdl_Yu23 *
      mdl_conjg__ZUR32 + mdl_Yu33 * mdl_conjg__ZUR33)))/mdl_sqrt__2;
  GC_250 = (-1. * mdl_complexi * (mdl_ZUL31 * (mdl_ZUR21 * mdl_conjg__Yu11 +
      mdl_ZUR22 * mdl_conjg__Yu21 + mdl_ZUR23 * mdl_conjg__Yu31) + mdl_ZUL32 *
      (mdl_ZUR21 * mdl_conjg__Yu12 + mdl_ZUR22 * mdl_conjg__Yu22 + mdl_ZUR23 *
      mdl_conjg__Yu32) + mdl_ZUL33 * (mdl_ZUR21 * mdl_conjg__Yu13 + mdl_ZUR22 *
      mdl_conjg__Yu23 + mdl_ZUR23 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_251 = (-1. * mdl_complexi * (mdl_conjg__ZUL31 * (mdl_Yu11 *
      mdl_conjg__ZUR31 + mdl_Yu21 * mdl_conjg__ZUR32 + mdl_Yu31 *
      mdl_conjg__ZUR33) + mdl_conjg__ZUL32 * (mdl_Yu12 * mdl_conjg__ZUR31 +
      mdl_Yu22 * mdl_conjg__ZUR32 + mdl_Yu32 * mdl_conjg__ZUR33) +
      mdl_conjg__ZUL33 * (mdl_Yu13 * mdl_conjg__ZUR31 + mdl_Yu23 *
      mdl_conjg__ZUR32 + mdl_Yu33 * mdl_conjg__ZUR33)))/mdl_sqrt__2;
  GC_252 = (-1. * mdl_complexi * (mdl_ZUL31 * (mdl_ZUR31 * mdl_conjg__Yu11 +
      mdl_ZUR32 * mdl_conjg__Yu21 + mdl_ZUR33 * mdl_conjg__Yu31) + mdl_ZUL32 *
      (mdl_ZUR31 * mdl_conjg__Yu12 + mdl_ZUR32 * mdl_conjg__Yu22 + mdl_ZUR33 *
      mdl_conjg__Yu32) + mdl_ZUL33 * (mdl_ZUR31 * mdl_conjg__Yu13 + mdl_ZUR32 *
      mdl_conjg__Yu23 + mdl_ZUR33 * mdl_conjg__Yu33)))/mdl_sqrt__2;
  GC_286 = 1./6. * mdl_complexi * (mdl_g1 * mdl_cos__TW - 3. * mdl_g2 *
      mdl_sin__TW);
  GC_287 = -1./3. * mdl_complexi * mdl_g1 * mdl_cos__TW; 
  GC_292 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL11 * mdl_conjg__ZDL11 +
      mdl_ZUL12 * mdl_conjg__ZDL12 + mdl_ZUL13 * mdl_conjg__ZDL13))/mdl_sqrt__2;
  GC_293 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL11 * mdl_conjg__ZDL21 +
      mdl_ZUL12 * mdl_conjg__ZDL22 + mdl_ZUL13 * mdl_conjg__ZDL23))/mdl_sqrt__2;
  GC_294 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL11 * mdl_conjg__ZDL31 +
      mdl_ZUL12 * mdl_conjg__ZDL32 + mdl_ZUL13 * mdl_conjg__ZDL33))/mdl_sqrt__2;
  GC_295 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL21 * mdl_conjg__ZDL11 +
      mdl_ZUL22 * mdl_conjg__ZDL12 + mdl_ZUL23 * mdl_conjg__ZDL13))/mdl_sqrt__2;
  GC_296 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL21 * mdl_conjg__ZDL21 +
      mdl_ZUL22 * mdl_conjg__ZDL22 + mdl_ZUL23 * mdl_conjg__ZDL23))/mdl_sqrt__2;
  GC_297 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL21 * mdl_conjg__ZDL31 +
      mdl_ZUL22 * mdl_conjg__ZDL32 + mdl_ZUL23 * mdl_conjg__ZDL33))/mdl_sqrt__2;
  GC_298 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL31 * mdl_conjg__ZDL11 +
      mdl_ZUL32 * mdl_conjg__ZDL12 + mdl_ZUL33 * mdl_conjg__ZDL13))/mdl_sqrt__2;
  GC_299 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL31 * mdl_conjg__ZDL21 +
      mdl_ZUL32 * mdl_conjg__ZDL22 + mdl_ZUL33 * mdl_conjg__ZDL23))/mdl_sqrt__2;
  GC_300 = (1. * mdl_complexi * mdl_g2 * (mdl_ZUL31 * mdl_conjg__ZDL31 +
      mdl_ZUL32 * mdl_conjg__ZDL32 + mdl_ZUL33 * mdl_conjg__ZDL33))/mdl_sqrt__2;
  GC_301 = -1./6. * mdl_complexi * (3. * mdl_g2 * mdl_cos__TW + mdl_g1 *
      mdl_sin__TW);
  GC_302 = 1./3. * mdl_complexi * mdl_g1 * mdl_sin__TW; 
  GC_307 = (1. * mdl_complexi * mdl_g2 * (mdl_UV11 * mdl_conjg__ZEL11 +
      mdl_UV12 * mdl_conjg__ZEL12 + mdl_UV13 * mdl_conjg__ZEL13))/mdl_sqrt__2;
  GC_308 = (1. * mdl_complexi * mdl_g2 * (mdl_UV11 * mdl_conjg__ZEL21 +
      mdl_UV12 * mdl_conjg__ZEL22 + mdl_UV13 * mdl_conjg__ZEL23))/mdl_sqrt__2;
  GC_309 = (1. * mdl_complexi * mdl_g2 * (mdl_UV11 * mdl_conjg__ZEL31 +
      mdl_UV12 * mdl_conjg__ZEL32 + mdl_UV13 * mdl_conjg__ZEL33))/mdl_sqrt__2;
  GC_310 = (1. * mdl_complexi * mdl_g2 * (mdl_UV21 * mdl_conjg__ZEL11 +
      mdl_UV22 * mdl_conjg__ZEL12 + mdl_UV23 * mdl_conjg__ZEL13))/mdl_sqrt__2;
  GC_311 = (1. * mdl_complexi * mdl_g2 * (mdl_UV21 * mdl_conjg__ZEL21 +
      mdl_UV22 * mdl_conjg__ZEL22 + mdl_UV23 * mdl_conjg__ZEL23))/mdl_sqrt__2;
  GC_312 = (1. * mdl_complexi * mdl_g2 * (mdl_UV21 * mdl_conjg__ZEL31 +
      mdl_UV22 * mdl_conjg__ZEL32 + mdl_UV23 * mdl_conjg__ZEL33))/mdl_sqrt__2;
  GC_313 = (1. * mdl_complexi * mdl_g2 * (mdl_UV31 * mdl_conjg__ZEL11 +
      mdl_UV32 * mdl_conjg__ZEL12 + mdl_UV33 * mdl_conjg__ZEL13))/mdl_sqrt__2;
  GC_314 = (1. * mdl_complexi * mdl_g2 * (mdl_UV31 * mdl_conjg__ZEL21 +
      mdl_UV32 * mdl_conjg__ZEL22 + mdl_UV33 * mdl_conjg__ZEL23))/mdl_sqrt__2;
  GC_315 = (1. * mdl_complexi * mdl_g2 * (mdl_UV31 * mdl_conjg__ZEL31 +
      mdl_UV32 * mdl_conjg__ZEL32 + mdl_UV33 * mdl_conjg__ZEL33))/mdl_sqrt__2;
  GC_316 = -1./2. * mdl_complexi * (mdl_g1 * mdl_cos__TW + mdl_g2 *
      mdl_sin__TW);
  GC_317 = -1. * mdl_complexi * mdl_g1 * mdl_cos__TW; 
  GC_322 = -1./2. * mdl_complexi * (mdl_g2 * mdl_cos__TW - mdl_g1 *
      mdl_sin__TW);
  GC_323 = 1. * mdl_complexi * mdl_g1 * mdl_sin__TW; 
  GC_334 = 1./6. * mdl_complexi * (mdl_g1 * mdl_cos__TW + 3. * mdl_g2 *
      mdl_sin__TW);
  GC_335 = 2./3. * mdl_complexi * mdl_g1 * mdl_cos__TW; 
  GC_340 = 1./6. * mdl_complexi * (3. * mdl_g2 * mdl_cos__TW - mdl_g1 *
      mdl_sin__TW);
  GC_341 = -2./3. * mdl_complexi * mdl_g1 * mdl_sin__TW; 
  GC_346 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL11 * mdl_conjg__ZUL11 +
      mdl_ZDL12 * mdl_conjg__ZUL12 + mdl_ZDL13 * mdl_conjg__ZUL13))/mdl_sqrt__2;
  GC_347 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL11 * mdl_conjg__ZUL21 +
      mdl_ZDL12 * mdl_conjg__ZUL22 + mdl_ZDL13 * mdl_conjg__ZUL23))/mdl_sqrt__2;
  GC_348 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL11 * mdl_conjg__ZUL31 +
      mdl_ZDL12 * mdl_conjg__ZUL32 + mdl_ZDL13 * mdl_conjg__ZUL33))/mdl_sqrt__2;
  GC_349 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL21 * mdl_conjg__ZUL11 +
      mdl_ZDL22 * mdl_conjg__ZUL12 + mdl_ZDL23 * mdl_conjg__ZUL13))/mdl_sqrt__2;
  GC_350 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL21 * mdl_conjg__ZUL21 +
      mdl_ZDL22 * mdl_conjg__ZUL22 + mdl_ZDL23 * mdl_conjg__ZUL23))/mdl_sqrt__2;
  GC_351 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL21 * mdl_conjg__ZUL31 +
      mdl_ZDL22 * mdl_conjg__ZUL32 + mdl_ZDL23 * mdl_conjg__ZUL33))/mdl_sqrt__2;
  GC_352 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL31 * mdl_conjg__ZUL11 +
      mdl_ZDL32 * mdl_conjg__ZUL12 + mdl_ZDL33 * mdl_conjg__ZUL13))/mdl_sqrt__2;
  GC_353 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL31 * mdl_conjg__ZUL21 +
      mdl_ZDL32 * mdl_conjg__ZUL22 + mdl_ZDL33 * mdl_conjg__ZUL23))/mdl_sqrt__2;
  GC_354 = (1. * mdl_complexi * mdl_g2 * (mdl_ZDL31 * mdl_conjg__ZUL31 +
      mdl_ZDL32 * mdl_conjg__ZUL32 + mdl_ZDL33 * mdl_conjg__ZUL33))/mdl_sqrt__2;
  GC_355 = 1./2. * mdl_complexi * (mdl_g2 * mdl_cos__TW + mdl_g1 *
      mdl_sin__TW);
  GC_356 = -1./2. * mdl_complexi * (mdl_g2 * mdl_cos__TW + mdl_g1 *
      mdl_sin__TW);
  GC_361 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL11 * mdl_conjg__UV11 +
      mdl_ZEL12 * mdl_conjg__UV12 + mdl_ZEL13 * mdl_conjg__UV13))/mdl_sqrt__2;
  GC_362 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL11 * mdl_conjg__UV21 +
      mdl_ZEL12 * mdl_conjg__UV22 + mdl_ZEL13 * mdl_conjg__UV23))/mdl_sqrt__2;
  GC_363 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL11 * mdl_conjg__UV31 +
      mdl_ZEL12 * mdl_conjg__UV32 + mdl_ZEL13 * mdl_conjg__UV33))/mdl_sqrt__2;
  GC_364 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL21 * mdl_conjg__UV11 +
      mdl_ZEL22 * mdl_conjg__UV12 + mdl_ZEL23 * mdl_conjg__UV13))/mdl_sqrt__2;
  GC_365 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL21 * mdl_conjg__UV21 +
      mdl_ZEL22 * mdl_conjg__UV22 + mdl_ZEL23 * mdl_conjg__UV23))/mdl_sqrt__2;
  GC_366 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL21 * mdl_conjg__UV31 +
      mdl_ZEL22 * mdl_conjg__UV32 + mdl_ZEL23 * mdl_conjg__UV33))/mdl_sqrt__2;
  GC_367 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL31 * mdl_conjg__UV11 +
      mdl_ZEL32 * mdl_conjg__UV12 + mdl_ZEL33 * mdl_conjg__UV13))/mdl_sqrt__2;
  GC_368 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL31 * mdl_conjg__UV21 +
      mdl_ZEL32 * mdl_conjg__UV22 + mdl_ZEL33 * mdl_conjg__UV23))/mdl_sqrt__2;
  GC_369 = (1. * mdl_complexi * mdl_g2 * (mdl_ZEL31 * mdl_conjg__UV31 +
      mdl_ZEL32 * mdl_conjg__UV32 + mdl_ZEL33 * mdl_conjg__UV33))/mdl_sqrt__2;
  GC_371 = 1. * mdl_complexi * mdl_g2 * mdl_sin__TW; 
  GC_372 = -1. * mdl_complexi * mdl_g2 * mdl_cos__TW; 
  GC_118 = (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX11 + mdl_Yn21 *
      mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) + mdl_conjg__UV12 *
      (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 * mdl_conjg__ZX12 + mdl_Yn32 *
      mdl_conjg__ZX13) + mdl_conjg__UV13 * (mdl_Yn13 * mdl_conjg__ZX11 +
      mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 * mdl_conjg__ZX13))/mdl_sqrt__2;
  GC_119 = -((mdl_UV11 * (mdl_ZX11 * mdl_conjg__Yn11 + mdl_ZX12 *
      mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV12 * (mdl_ZX11 *
      mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_120 = (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX11 + mdl_Yn21 *
      mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) + mdl_conjg__UV22 *
      (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 * mdl_conjg__ZX12 + mdl_Yn32 *
      mdl_conjg__ZX13) + mdl_conjg__UV23 * (mdl_Yn13 * mdl_conjg__ZX11 +
      mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 * mdl_conjg__ZX13))/mdl_sqrt__2;
  GC_121 = -((mdl_UV21 * (mdl_ZX11 * mdl_conjg__Yn11 + mdl_ZX12 *
      mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV22 * (mdl_ZX11 *
      mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_122 = (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX11 + mdl_Yn21 *
      mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) + mdl_conjg__UV32 *
      (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 * mdl_conjg__ZX12 + mdl_Yn32 *
      mdl_conjg__ZX13) + mdl_conjg__UV33 * (mdl_Yn13 * mdl_conjg__ZX11 +
      mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 * mdl_conjg__ZX13))/mdl_sqrt__2;
  GC_123 = -((mdl_UV31 * (mdl_ZX11 * mdl_conjg__Yn11 + mdl_ZX12 *
      mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV32 * (mdl_ZX11 *
      mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_124 = (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX21 + mdl_Yn21 *
      mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) + mdl_conjg__UV12 *
      (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 * mdl_conjg__ZX22 + mdl_Yn32 *
      mdl_conjg__ZX23) + mdl_conjg__UV13 * (mdl_Yn13 * mdl_conjg__ZX21 +
      mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 * mdl_conjg__ZX23))/mdl_sqrt__2;
  GC_125 = -((mdl_UV11 * (mdl_ZX21 * mdl_conjg__Yn11 + mdl_ZX22 *
      mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV12 * (mdl_ZX21 *
      mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_126 = (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX21 + mdl_Yn21 *
      mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) + mdl_conjg__UV22 *
      (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 * mdl_conjg__ZX22 + mdl_Yn32 *
      mdl_conjg__ZX23) + mdl_conjg__UV23 * (mdl_Yn13 * mdl_conjg__ZX21 +
      mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 * mdl_conjg__ZX23))/mdl_sqrt__2;
  GC_127 = -((mdl_UV21 * (mdl_ZX21 * mdl_conjg__Yn11 + mdl_ZX22 *
      mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV22 * (mdl_ZX21 *
      mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_128 = (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX21 + mdl_Yn21 *
      mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) + mdl_conjg__UV32 *
      (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 * mdl_conjg__ZX22 + mdl_Yn32 *
      mdl_conjg__ZX23) + mdl_conjg__UV33 * (mdl_Yn13 * mdl_conjg__ZX21 +
      mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 * mdl_conjg__ZX23))/mdl_sqrt__2;
  GC_129 = -((mdl_UV31 * (mdl_ZX21 * mdl_conjg__Yn11 + mdl_ZX22 *
      mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV32 * (mdl_ZX21 *
      mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_130 = (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX31 + mdl_Yn21 *
      mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) + mdl_conjg__UV12 *
      (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 * mdl_conjg__ZX32 + mdl_Yn32 *
      mdl_conjg__ZX33) + mdl_conjg__UV13 * (mdl_Yn13 * mdl_conjg__ZX31 +
      mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 * mdl_conjg__ZX33))/mdl_sqrt__2;
  GC_131 = -((mdl_UV11 * (mdl_ZX31 * mdl_conjg__Yn11 + mdl_ZX32 *
      mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV12 * (mdl_ZX31 *
      mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_132 = (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX31 + mdl_Yn21 *
      mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) + mdl_conjg__UV22 *
      (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 * mdl_conjg__ZX32 + mdl_Yn32 *
      mdl_conjg__ZX33) + mdl_conjg__UV23 * (mdl_Yn13 * mdl_conjg__ZX31 +
      mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 * mdl_conjg__ZX33))/mdl_sqrt__2;
  GC_133 = -((mdl_UV21 * (mdl_ZX31 * mdl_conjg__Yn11 + mdl_ZX32 *
      mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV22 * (mdl_ZX31 *
      mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_134 = (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX31 + mdl_Yn21 *
      mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) + mdl_conjg__UV32 *
      (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 * mdl_conjg__ZX32 + mdl_Yn32 *
      mdl_conjg__ZX33) + mdl_conjg__UV33 * (mdl_Yn13 * mdl_conjg__ZX31 +
      mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 * mdl_conjg__ZX33))/mdl_sqrt__2;
  GC_135 = -((mdl_UV31 * (mdl_ZX31 * mdl_conjg__Yn11 + mdl_ZX32 *
      mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV32 * (mdl_ZX31 *
      mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33))/mdl_sqrt__2);
  GC_136 = 1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__ZEL12 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__ZEL13 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13));
  GC_137 = 1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__ZEL22 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__ZEL23 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13));
  GC_138 = 1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__ZEL32 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__ZEL33 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13));
  GC_139 = 1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__ZEL12 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__ZEL13 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23));
  GC_140 = 1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__ZEL22 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__ZEL23 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23));
  GC_141 = 1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__ZEL32 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__ZEL33 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23));
  GC_142 = 1. * mdl_complexi * (mdl_conjg__ZEL11 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__ZEL12 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__ZEL13 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33));
  GC_143 = 1. * mdl_complexi * (mdl_conjg__ZEL21 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__ZEL22 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__ZEL23 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33));
  GC_144 = 1. * mdl_complexi * (mdl_conjg__ZEL31 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__ZEL32 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__ZEL33 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33));
  GC_145 = (-1. * mdl_complexi * (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__UV12 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__UV13 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13)))/mdl_sqrt__2;
  GC_146 = (-1. * mdl_complexi * (mdl_UV11 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV12 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_147 = (-1. * mdl_complexi * (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__UV22 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__UV23 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13)))/mdl_sqrt__2;
  GC_148 = (-1. * mdl_complexi * (mdl_UV21 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV22 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_149 = (-1. * mdl_complexi * (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX11
      + mdl_Yn21 * mdl_conjg__ZX12 + mdl_Yn31 * mdl_conjg__ZX13) +
      mdl_conjg__UV32 * (mdl_Yn12 * mdl_conjg__ZX11 + mdl_Yn22 *
      mdl_conjg__ZX12 + mdl_Yn32 * mdl_conjg__ZX13) + mdl_conjg__UV33 *
      (mdl_Yn13 * mdl_conjg__ZX11 + mdl_Yn23 * mdl_conjg__ZX12 + mdl_Yn33 *
      mdl_conjg__ZX13)))/mdl_sqrt__2;
  GC_150 = (-1. * mdl_complexi * (mdl_UV31 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_UV32 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_151 = (-1. * mdl_complexi * (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__UV12 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__UV13 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23)))/mdl_sqrt__2;
  GC_152 = (-1. * mdl_complexi * (mdl_UV11 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV12 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_153 = (-1. * mdl_complexi * (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__UV22 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__UV23 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23)))/mdl_sqrt__2;
  GC_154 = (-1. * mdl_complexi * (mdl_UV21 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV22 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_155 = (-1. * mdl_complexi * (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX21
      + mdl_Yn21 * mdl_conjg__ZX22 + mdl_Yn31 * mdl_conjg__ZX23) +
      mdl_conjg__UV32 * (mdl_Yn12 * mdl_conjg__ZX21 + mdl_Yn22 *
      mdl_conjg__ZX22 + mdl_Yn32 * mdl_conjg__ZX23) + mdl_conjg__UV33 *
      (mdl_Yn13 * mdl_conjg__ZX21 + mdl_Yn23 * mdl_conjg__ZX22 + mdl_Yn33 *
      mdl_conjg__ZX23)))/mdl_sqrt__2;
  GC_156 = (-1. * mdl_complexi * (mdl_UV31 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_UV32 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_157 = (-1. * mdl_complexi * (mdl_conjg__UV11 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__UV12 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__UV13 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33)))/mdl_sqrt__2;
  GC_158 = (-1. * mdl_complexi * (mdl_UV11 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV12 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV13 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_159 = (-1. * mdl_complexi * (mdl_conjg__UV21 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__UV22 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__UV23 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33)))/mdl_sqrt__2;
  GC_160 = (-1. * mdl_complexi * (mdl_UV21 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV22 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV23 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_161 = (-1. * mdl_complexi * (mdl_conjg__UV31 * (mdl_Yn11 * mdl_conjg__ZX31
      + mdl_Yn21 * mdl_conjg__ZX32 + mdl_Yn31 * mdl_conjg__ZX33) +
      mdl_conjg__UV32 * (mdl_Yn12 * mdl_conjg__ZX31 + mdl_Yn22 *
      mdl_conjg__ZX32 + mdl_Yn32 * mdl_conjg__ZX33) + mdl_conjg__UV33 *
      (mdl_Yn13 * mdl_conjg__ZX31 + mdl_Yn23 * mdl_conjg__ZX32 + mdl_Yn33 *
      mdl_conjg__ZX33)))/mdl_sqrt__2;
  GC_162 = (-1. * mdl_complexi * (mdl_UV31 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_UV32 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_UV33 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33)))/mdl_sqrt__2;
  GC_163 = 1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_ZEL12 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_ZEL13 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33));
  GC_164 = 1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_ZEL12 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_ZEL13 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33));
  GC_165 = 1. * mdl_complexi * (mdl_ZEL11 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_ZEL12 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_ZEL13 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33));
  GC_166 = 1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_ZEL22 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_ZEL23 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33));
  GC_167 = 1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_ZEL22 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_ZEL23 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33));
  GC_168 = 1. * mdl_complexi * (mdl_ZEL21 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_ZEL22 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_ZEL23 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33));
  GC_169 = 1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZX11 * mdl_conjg__Yn11 +
      mdl_ZX12 * mdl_conjg__Yn21 + mdl_ZX13 * mdl_conjg__Yn31) + mdl_ZEL32 *
      (mdl_ZX11 * mdl_conjg__Yn12 + mdl_ZX12 * mdl_conjg__Yn22 + mdl_ZX13 *
      mdl_conjg__Yn32) + mdl_ZEL33 * (mdl_ZX11 * mdl_conjg__Yn13 + mdl_ZX12 *
      mdl_conjg__Yn23 + mdl_ZX13 * mdl_conjg__Yn33));
  GC_170 = 1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZX21 * mdl_conjg__Yn11 +
      mdl_ZX22 * mdl_conjg__Yn21 + mdl_ZX23 * mdl_conjg__Yn31) + mdl_ZEL32 *
      (mdl_ZX21 * mdl_conjg__Yn12 + mdl_ZX22 * mdl_conjg__Yn22 + mdl_ZX23 *
      mdl_conjg__Yn32) + mdl_ZEL33 * (mdl_ZX21 * mdl_conjg__Yn13 + mdl_ZX22 *
      mdl_conjg__Yn23 + mdl_ZX23 * mdl_conjg__Yn33));
  GC_171 = 1. * mdl_complexi * (mdl_ZEL31 * (mdl_ZX31 * mdl_conjg__Yn11 +
      mdl_ZX32 * mdl_conjg__Yn21 + mdl_ZX33 * mdl_conjg__Yn31) + mdl_ZEL32 *
      (mdl_ZX31 * mdl_conjg__Yn12 + mdl_ZX32 * mdl_conjg__Yn22 + mdl_ZX33 *
      mdl_conjg__Yn32) + mdl_ZEL33 * (mdl_ZX31 * mdl_conjg__Yn13 + mdl_ZX32 *
      mdl_conjg__Yn23 + mdl_ZX33 * mdl_conjg__Yn33));
  if (mdl_MN1 < 0)
    mdl_WN1 = -abs(mdl_WN1); 
  if (mdl_MN2 < 0)
    mdl_WN2 = -abs(mdl_WN2); 
  if (mdl_MN3 < 0)
    mdl_WN3 = -abs(mdl_WN3); 
}
void Parameters_scotogenic_UFO::setDependentParameters()
{
  mdl_sqrt__aS = sqrt(aS); 
  G = 2. * mdl_sqrt__aS * sqrt(M_PI); 
  mdl_G__exp__2 = ((G) * (G)); 
  if (mdl_MN1 < 0)
    mdl_WN1 = -abs(mdl_WN1); 
  if (mdl_MN2 < 0)
    mdl_WN2 = -abs(mdl_WN2); 
  if (mdl_MN3 < 0)
    mdl_WN3 = -abs(mdl_WN3); 
}
void Parameters_scotogenic_UFO::setDependentCouplings()
{
  if (mdl_MN1 < 0)
    mdl_WN1 = -abs(mdl_WN1); 
  if (mdl_MN2 < 0)
    mdl_WN2 = -abs(mdl_WN2); 
  if (mdl_MN3 < 0)
    mdl_WN3 = -abs(mdl_WN3); 
}

// Routines for printing out parameters
void Parameters_scotogenic_UFO::printIndependentParameters()
{
  cout <<  "scotogenic_UFO model parameters independent of event kinematics:"
      << endl;
  cout << setw(20) <<  "mdl_WN3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WN3 << endl;
  cout << setw(20) <<  "mdl_WN2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WN2 << endl;
  cout << setw(20) <<  "mdl_WN1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WN1 << endl;
  cout << setw(20) <<  "mdl_WetI " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WetI << endl;
  cout << setw(20) <<  "mdl_WetR " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WetR << endl;
  cout << setw(20) <<  "mdl_Wh " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Wh << endl;
  cout << setw(20) <<  "mdl_WWp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WWp << endl;
  cout << setw(20) <<  "mdl_WZ " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_WZ << endl;
  cout << setw(20) <<  "mdl_Wu3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Wu3 << endl;
  cout << setw(20) <<  "mdl_rZX33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX33 << endl;
  cout << setw(20) <<  "mdl_rZX32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX32 << endl;
  cout << setw(20) <<  "mdl_rZX31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX31 << endl;
  cout << setw(20) <<  "mdl_rZX23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX23 << endl;
  cout << setw(20) <<  "mdl_rZX22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX22 << endl;
  cout << setw(20) <<  "mdl_rZX21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX21 << endl;
  cout << setw(20) <<  "mdl_rZX13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX13 << endl;
  cout << setw(20) <<  "mdl_rZX12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX12 << endl;
  cout << setw(20) <<  "mdl_rZX11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rZX11 << endl;
  cout << setw(20) <<  "mdl_rYn33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn33 << endl;
  cout << setw(20) <<  "mdl_rYn32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn32 << endl;
  cout << setw(20) <<  "mdl_rYn31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn31 << endl;
  cout << setw(20) <<  "mdl_rYn23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn23 << endl;
  cout << setw(20) <<  "mdl_rYn22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn22 << endl;
  cout << setw(20) <<  "mdl_rYn21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn21 << endl;
  cout << setw(20) <<  "mdl_rYn13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn13 << endl;
  cout << setw(20) <<  "mdl_rYn12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn12 << endl;
  cout << setw(20) <<  "mdl_rYn11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rYn11 << endl;
  cout << setw(20) <<  "mdl_rUV33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV33 << endl;
  cout << setw(20) <<  "mdl_rUV32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV32 << endl;
  cout << setw(20) <<  "mdl_rUV31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV31 << endl;
  cout << setw(20) <<  "mdl_rUV23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV23 << endl;
  cout << setw(20) <<  "mdl_rUV22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV22 << endl;
  cout << setw(20) <<  "mdl_rUV21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV21 << endl;
  cout << setw(20) <<  "mdl_rUV13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV13 << endl;
  cout << setw(20) <<  "mdl_rUV12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV12 << endl;
  cout << setw(20) <<  "mdl_rUV11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rUV11 << endl;
  cout << setw(20) <<  "mdl_rZUR33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR33 << endl;
  cout << setw(20) <<  "mdl_rZUR32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR32 << endl;
  cout << setw(20) <<  "mdl_rZUR31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR31 << endl;
  cout << setw(20) <<  "mdl_rZUR23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR23 << endl;
  cout << setw(20) <<  "mdl_rZUR22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR22 << endl;
  cout << setw(20) <<  "mdl_rZUR21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR21 << endl;
  cout << setw(20) <<  "mdl_rZUR13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR13 << endl;
  cout << setw(20) <<  "mdl_rZUR12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR12 << endl;
  cout << setw(20) <<  "mdl_rZUR11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUR11 << endl;
  cout << setw(20) <<  "mdl_rZUL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL33 << endl;
  cout << setw(20) <<  "mdl_rZUL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL32 << endl;
  cout << setw(20) <<  "mdl_rZUL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL31 << endl;
  cout << setw(20) <<  "mdl_rZUL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL23 << endl;
  cout << setw(20) <<  "mdl_rZUL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL22 << endl;
  cout << setw(20) <<  "mdl_rZUL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL21 << endl;
  cout << setw(20) <<  "mdl_rZUL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL13 << endl;
  cout << setw(20) <<  "mdl_rZUL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL12 << endl;
  cout << setw(20) <<  "mdl_rZUL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZUL11 << endl;
  cout << setw(20) <<  "mdl_rZER33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER33 << endl;
  cout << setw(20) <<  "mdl_rZER32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER32 << endl;
  cout << setw(20) <<  "mdl_rZER31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER31 << endl;
  cout << setw(20) <<  "mdl_rZER23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER23 << endl;
  cout << setw(20) <<  "mdl_rZER22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER22 << endl;
  cout << setw(20) <<  "mdl_rZER21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER21 << endl;
  cout << setw(20) <<  "mdl_rZER13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER13 << endl;
  cout << setw(20) <<  "mdl_rZER12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER12 << endl;
  cout << setw(20) <<  "mdl_rZER11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZER11 << endl;
  cout << setw(20) <<  "mdl_rZEL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL33 << endl;
  cout << setw(20) <<  "mdl_rZEL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL32 << endl;
  cout << setw(20) <<  "mdl_rZEL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL31 << endl;
  cout << setw(20) <<  "mdl_rZEL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL23 << endl;
  cout << setw(20) <<  "mdl_rZEL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL22 << endl;
  cout << setw(20) <<  "mdl_rZEL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL21 << endl;
  cout << setw(20) <<  "mdl_rZEL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL13 << endl;
  cout << setw(20) <<  "mdl_rZEL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL12 << endl;
  cout << setw(20) <<  "mdl_rZEL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZEL11 << endl;
  cout << setw(20) <<  "mdl_rZDR33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR33 << endl;
  cout << setw(20) <<  "mdl_rZDR32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR32 << endl;
  cout << setw(20) <<  "mdl_rZDR31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR31 << endl;
  cout << setw(20) <<  "mdl_rZDR23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR23 << endl;
  cout << setw(20) <<  "mdl_rZDR22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR22 << endl;
  cout << setw(20) <<  "mdl_rZDR21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR21 << endl;
  cout << setw(20) <<  "mdl_rZDR13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR13 << endl;
  cout << setw(20) <<  "mdl_rZDR12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR12 << endl;
  cout << setw(20) <<  "mdl_rZDR11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDR11 << endl;
  cout << setw(20) <<  "mdl_rZDL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL33 << endl;
  cout << setw(20) <<  "mdl_rZDL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL32 << endl;
  cout << setw(20) <<  "mdl_rZDL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL31 << endl;
  cout << setw(20) <<  "mdl_rZDL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL23 << endl;
  cout << setw(20) <<  "mdl_rZDL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL22 << endl;
  cout << setw(20) <<  "mdl_rZDL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL21 << endl;
  cout << setw(20) <<  "mdl_rZDL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL13 << endl;
  cout << setw(20) <<  "mdl_rZDL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL12 << endl;
  cout << setw(20) <<  "mdl_rZDL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_rZDL11 << endl;
  cout << setw(20) <<  "aS " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << aS << endl;
  cout << setw(20) <<  "mdl_Gf " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Gf << endl;
  cout << setw(20) <<  "aEWM1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << aEWM1 << endl;
  cout << setw(20) <<  "mdl_MN3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MN3 << endl;
  cout << setw(20) <<  "mdl_MN2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MN2 << endl;
  cout << setw(20) <<  "mdl_MN1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MN1 << endl;
  cout << setw(20) <<  "mdl_Metp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Metp << endl;
  cout << setw(20) <<  "mdl_MetI " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MetI << endl;
  cout << setw(20) <<  "mdl_MetR " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MetR << endl;
  cout << setw(20) <<  "mdl_Mh " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Mh << endl;
  cout << setw(20) <<  "mdl_MZ " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MZ << endl;
  cout << setw(20) <<  "mdl_Me3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Me3 << endl;
  cout << setw(20) <<  "mdl_Me2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Me2 << endl;
  cout << setw(20) <<  "mdl_Me1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Me1 << endl;
  cout << setw(20) <<  "mdl_Mu3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Mu3 << endl;
  cout << setw(20) <<  "mdl_Md3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Md3 << endl;
  cout << setw(20) <<  "mdl_Mu2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Mu2 << endl;
  cout << setw(20) <<  "mdl_Md2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Md2 << endl;
  cout << setw(20) <<  "mdl_Mu1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Mu1 << endl;
  cout << setw(20) <<  "mdl_Md1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Md1 << endl;
  cout << setw(20) <<  "mdl_iZX33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX33 << endl;
  cout << setw(20) <<  "mdl_iZX32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX32 << endl;
  cout << setw(20) <<  "mdl_iZX31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX31 << endl;
  cout << setw(20) <<  "mdl_iZX23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX23 << endl;
  cout << setw(20) <<  "mdl_iZX22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX22 << endl;
  cout << setw(20) <<  "mdl_iZX21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX21 << endl;
  cout << setw(20) <<  "mdl_iZX13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX13 << endl;
  cout << setw(20) <<  "mdl_iZX12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX12 << endl;
  cout << setw(20) <<  "mdl_iZX11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iZX11 << endl;
  cout << setw(20) <<  "mdl_iYn33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn33 << endl;
  cout << setw(20) <<  "mdl_iYn32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn32 << endl;
  cout << setw(20) <<  "mdl_iYn31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn31 << endl;
  cout << setw(20) <<  "mdl_iYn23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn23 << endl;
  cout << setw(20) <<  "mdl_iYn22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn22 << endl;
  cout << setw(20) <<  "mdl_iYn21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn21 << endl;
  cout << setw(20) <<  "mdl_iYn13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn13 << endl;
  cout << setw(20) <<  "mdl_iYn12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn12 << endl;
  cout << setw(20) <<  "mdl_iYn11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iYn11 << endl;
  cout << setw(20) <<  "mdl_iUV33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV33 << endl;
  cout << setw(20) <<  "mdl_iUV32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV32 << endl;
  cout << setw(20) <<  "mdl_iUV31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV31 << endl;
  cout << setw(20) <<  "mdl_iUV23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV23 << endl;
  cout << setw(20) <<  "mdl_iUV22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV22 << endl;
  cout << setw(20) <<  "mdl_iUV21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV21 << endl;
  cout << setw(20) <<  "mdl_iUV13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV13 << endl;
  cout << setw(20) <<  "mdl_iUV12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV12 << endl;
  cout << setw(20) <<  "mdl_iUV11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_iUV11 << endl;
  cout << setw(20) <<  "mdl_iZUR33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR33 << endl;
  cout << setw(20) <<  "mdl_iZUR32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR32 << endl;
  cout << setw(20) <<  "mdl_iZUR31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR31 << endl;
  cout << setw(20) <<  "mdl_iZUR23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR23 << endl;
  cout << setw(20) <<  "mdl_iZUR22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR22 << endl;
  cout << setw(20) <<  "mdl_iZUR21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR21 << endl;
  cout << setw(20) <<  "mdl_iZUR13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR13 << endl;
  cout << setw(20) <<  "mdl_iZUR12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR12 << endl;
  cout << setw(20) <<  "mdl_iZUR11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUR11 << endl;
  cout << setw(20) <<  "mdl_iZUL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL33 << endl;
  cout << setw(20) <<  "mdl_iZUL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL32 << endl;
  cout << setw(20) <<  "mdl_iZUL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL31 << endl;
  cout << setw(20) <<  "mdl_iZUL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL23 << endl;
  cout << setw(20) <<  "mdl_iZUL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL22 << endl;
  cout << setw(20) <<  "mdl_iZUL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL21 << endl;
  cout << setw(20) <<  "mdl_iZUL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL13 << endl;
  cout << setw(20) <<  "mdl_iZUL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL12 << endl;
  cout << setw(20) <<  "mdl_iZUL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZUL11 << endl;
  cout << setw(20) <<  "mdl_iZER33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER33 << endl;
  cout << setw(20) <<  "mdl_iZER32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER32 << endl;
  cout << setw(20) <<  "mdl_iZER31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER31 << endl;
  cout << setw(20) <<  "mdl_iZER23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER23 << endl;
  cout << setw(20) <<  "mdl_iZER22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER22 << endl;
  cout << setw(20) <<  "mdl_iZER21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER21 << endl;
  cout << setw(20) <<  "mdl_iZER13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER13 << endl;
  cout << setw(20) <<  "mdl_iZER12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER12 << endl;
  cout << setw(20) <<  "mdl_iZER11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZER11 << endl;
  cout << setw(20) <<  "mdl_iZEL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL33 << endl;
  cout << setw(20) <<  "mdl_iZEL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL32 << endl;
  cout << setw(20) <<  "mdl_iZEL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL31 << endl;
  cout << setw(20) <<  "mdl_iZEL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL23 << endl;
  cout << setw(20) <<  "mdl_iZEL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL22 << endl;
  cout << setw(20) <<  "mdl_iZEL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL21 << endl;
  cout << setw(20) <<  "mdl_iZEL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL13 << endl;
  cout << setw(20) <<  "mdl_iZEL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL12 << endl;
  cout << setw(20) <<  "mdl_iZEL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZEL11 << endl;
  cout << setw(20) <<  "mdl_iZDR33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR33 << endl;
  cout << setw(20) <<  "mdl_iZDR32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR32 << endl;
  cout << setw(20) <<  "mdl_iZDR31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR31 << endl;
  cout << setw(20) <<  "mdl_iZDR23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR23 << endl;
  cout << setw(20) <<  "mdl_iZDR22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR22 << endl;
  cout << setw(20) <<  "mdl_iZDR21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR21 << endl;
  cout << setw(20) <<  "mdl_iZDR13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR13 << endl;
  cout << setw(20) <<  "mdl_iZDR12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR12 << endl;
  cout << setw(20) <<  "mdl_iZDR11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDR11 << endl;
  cout << setw(20) <<  "mdl_iZDL33 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL33 << endl;
  cout << setw(20) <<  "mdl_iZDL32 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL32 << endl;
  cout << setw(20) <<  "mdl_iZDL31 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL31 << endl;
  cout << setw(20) <<  "mdl_iZDL23 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL23 << endl;
  cout << setw(20) <<  "mdl_iZDL22 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL22 << endl;
  cout << setw(20) <<  "mdl_iZDL21 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL21 << endl;
  cout << setw(20) <<  "mdl_iZDL13 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL13 << endl;
  cout << setw(20) <<  "mdl_iZDL12 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL12 << endl;
  cout << setw(20) <<  "mdl_iZDL11 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_iZDL11 << endl;
  cout << setw(20) <<  "mdl_ilam4 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ilam4 << endl;
  cout << setw(20) <<  "mdl_ilam3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ilam3 << endl;
  cout << setw(20) <<  "mdl_ilam2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ilam2 << endl;
  cout << setw(20) <<  "mdl_ilam1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ilam1 << endl;
  cout << setw(20) <<  "mdl_lam5 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_lam5 << endl;
  cout << setw(20) <<  "mdl_rlam4 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rlam4 << endl;
  cout << setw(20) <<  "mdl_rlam3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rlam3 << endl;
  cout << setw(20) <<  "mdl_rlam2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rlam2 << endl;
  cout << setw(20) <<  "mdl_rlam1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_rlam1 << endl;
  cout << setw(20) <<  "mdl_complexi " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_complexi << endl;
  cout << setw(20) <<  "mdl_Yn11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn11 << endl;
  cout << setw(20) <<  "mdl_Yn12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn12 << endl;
  cout << setw(20) <<  "mdl_Yn13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn13 << endl;
  cout << setw(20) <<  "mdl_Yn21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn21 << endl;
  cout << setw(20) <<  "mdl_Yn22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn22 << endl;
  cout << setw(20) <<  "mdl_Yn23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn23 << endl;
  cout << setw(20) <<  "mdl_Yn31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn31 << endl;
  cout << setw(20) <<  "mdl_Yn32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn32 << endl;
  cout << setw(20) <<  "mdl_Yn33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yn33 << endl;
  cout << setw(20) <<  "mdl_lam1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_lam1 << endl;
  cout << setw(20) <<  "mdl_lam2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_lam2 << endl;
  cout << setw(20) <<  "mdl_lam4 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_lam4 << endl;
  cout << setw(20) <<  "mdl_lam3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_lam3 << endl;
  cout << setw(20) <<  "mdl_ZX11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX11 << endl;
  cout << setw(20) <<  "mdl_ZX12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX12 << endl;
  cout << setw(20) <<  "mdl_ZX13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX13 << endl;
  cout << setw(20) <<  "mdl_ZX21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX21 << endl;
  cout << setw(20) <<  "mdl_ZX22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX22 << endl;
  cout << setw(20) <<  "mdl_ZX23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX23 << endl;
  cout << setw(20) <<  "mdl_ZX31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX31 << endl;
  cout << setw(20) <<  "mdl_ZX32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX32 << endl;
  cout << setw(20) <<  "mdl_ZX33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZX33 << endl;
  cout << setw(20) <<  "mdl_UV11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV11 << endl;
  cout << setw(20) <<  "mdl_UV12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV12 << endl;
  cout << setw(20) <<  "mdl_UV13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV13 << endl;
  cout << setw(20) <<  "mdl_UV21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV21 << endl;
  cout << setw(20) <<  "mdl_UV22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV22 << endl;
  cout << setw(20) <<  "mdl_UV23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV23 << endl;
  cout << setw(20) <<  "mdl_UV31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV31 << endl;
  cout << setw(20) <<  "mdl_UV32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV32 << endl;
  cout << setw(20) <<  "mdl_UV33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_UV33 << endl;
  cout << setw(20) <<  "mdl_ZDL11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL11 << endl;
  cout << setw(20) <<  "mdl_ZDL12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL12 << endl;
  cout << setw(20) <<  "mdl_ZDL13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL13 << endl;
  cout << setw(20) <<  "mdl_ZDL21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL21 << endl;
  cout << setw(20) <<  "mdl_ZDL22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL22 << endl;
  cout << setw(20) <<  "mdl_ZDL23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL23 << endl;
  cout << setw(20) <<  "mdl_ZDL31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL31 << endl;
  cout << setw(20) <<  "mdl_ZDL32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL32 << endl;
  cout << setw(20) <<  "mdl_ZDL33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDL33 << endl;
  cout << setw(20) <<  "mdl_ZDR11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR11 << endl;
  cout << setw(20) <<  "mdl_ZDR12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR12 << endl;
  cout << setw(20) <<  "mdl_ZDR13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR13 << endl;
  cout << setw(20) <<  "mdl_ZDR21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR21 << endl;
  cout << setw(20) <<  "mdl_ZDR22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR22 << endl;
  cout << setw(20) <<  "mdl_ZDR23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR23 << endl;
  cout << setw(20) <<  "mdl_ZDR31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR31 << endl;
  cout << setw(20) <<  "mdl_ZDR32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR32 << endl;
  cout << setw(20) <<  "mdl_ZDR33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZDR33 << endl;
  cout << setw(20) <<  "mdl_ZUL11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL11 << endl;
  cout << setw(20) <<  "mdl_ZUL12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL12 << endl;
  cout << setw(20) <<  "mdl_ZUL13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL13 << endl;
  cout << setw(20) <<  "mdl_ZUL21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL21 << endl;
  cout << setw(20) <<  "mdl_ZUL22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL22 << endl;
  cout << setw(20) <<  "mdl_ZUL23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL23 << endl;
  cout << setw(20) <<  "mdl_ZUL31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL31 << endl;
  cout << setw(20) <<  "mdl_ZUL32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL32 << endl;
  cout << setw(20) <<  "mdl_ZUL33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUL33 << endl;
  cout << setw(20) <<  "mdl_ZUR11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR11 << endl;
  cout << setw(20) <<  "mdl_ZUR12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR12 << endl;
  cout << setw(20) <<  "mdl_ZUR13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR13 << endl;
  cout << setw(20) <<  "mdl_ZUR21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR21 << endl;
  cout << setw(20) <<  "mdl_ZUR22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR22 << endl;
  cout << setw(20) <<  "mdl_ZUR23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR23 << endl;
  cout << setw(20) <<  "mdl_ZUR31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR31 << endl;
  cout << setw(20) <<  "mdl_ZUR32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR32 << endl;
  cout << setw(20) <<  "mdl_ZUR33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZUR33 << endl;
  cout << setw(20) <<  "mdl_ZEL11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL11 << endl;
  cout << setw(20) <<  "mdl_ZEL12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL12 << endl;
  cout << setw(20) <<  "mdl_ZEL13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL13 << endl;
  cout << setw(20) <<  "mdl_ZEL21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL21 << endl;
  cout << setw(20) <<  "mdl_ZEL22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL22 << endl;
  cout << setw(20) <<  "mdl_ZEL23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL23 << endl;
  cout << setw(20) <<  "mdl_ZEL31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL31 << endl;
  cout << setw(20) <<  "mdl_ZEL32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL32 << endl;
  cout << setw(20) <<  "mdl_ZEL33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZEL33 << endl;
  cout << setw(20) <<  "mdl_ZER11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER11 << endl;
  cout << setw(20) <<  "mdl_ZER12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER12 << endl;
  cout << setw(20) <<  "mdl_ZER13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER13 << endl;
  cout << setw(20) <<  "mdl_ZER21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER21 << endl;
  cout << setw(20) <<  "mdl_ZER22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER22 << endl;
  cout << setw(20) <<  "mdl_ZER23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER23 << endl;
  cout << setw(20) <<  "mdl_ZER31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER31 << endl;
  cout << setw(20) <<  "mdl_ZER32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER32 << endl;
  cout << setw(20) <<  "mdl_ZER33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_ZER33 << endl;
  cout << setw(20) <<  "mdl_MZ__exp__2 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_MZ__exp__2 << endl;
  cout << setw(20) <<  "mdl_MZ__exp__4 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_MZ__exp__4 << endl;
  cout << setw(20) <<  "mdl_sqrt__2 " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_sqrt__2 << endl;
  cout << setw(20) <<  "mdl_Yu12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu12 << endl;
  cout << setw(20) <<  "mdl_Yu13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu13 << endl;
  cout << setw(20) <<  "mdl_Yu21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu21 << endl;
  cout << setw(20) <<  "mdl_Yu23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu23 << endl;
  cout << setw(20) <<  "mdl_Yu31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu31 << endl;
  cout << setw(20) <<  "mdl_Yu32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu32 << endl;
  cout << setw(20) <<  "mdl_Yd12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd12 << endl;
  cout << setw(20) <<  "mdl_Yd13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd13 << endl;
  cout << setw(20) <<  "mdl_Yd21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd21 << endl;
  cout << setw(20) <<  "mdl_Yd23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd23 << endl;
  cout << setw(20) <<  "mdl_Yd31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd31 << endl;
  cout << setw(20) <<  "mdl_Yd32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd32 << endl;
  cout << setw(20) <<  "mdl_Ye12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye12 << endl;
  cout << setw(20) <<  "mdl_Ye13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye13 << endl;
  cout << setw(20) <<  "mdl_Ye21 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye21 << endl;
  cout << setw(20) <<  "mdl_Ye23 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye23 << endl;
  cout << setw(20) <<  "mdl_Ye31 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye31 << endl;
  cout << setw(20) <<  "mdl_Ye32 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye32 << endl;
  cout << setw(20) <<  "mdl_RXiWp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_RXiWp << endl;
  cout << setw(20) <<  "mdl_RXiZ " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_RXiZ << endl;
  cout << setw(20) <<  "mdl_MAh " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MAh << endl;
  cout << setw(20) <<  "mdl_MgZ " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MgZ << endl;
  cout << setw(20) <<  "mdl_conjg__lam1 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__lam1 << endl;
  cout << setw(20) <<  "mdl_conjg__lam3 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__lam3 << endl;
  cout << setw(20) <<  "mdl_conjg__lam4 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__lam4 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR13 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd21 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd31 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd12 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd32 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDL33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDL33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZDR33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZDR33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER13 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL13 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye21 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye31 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye12 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye32 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye13 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZEL33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZEL33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZER33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZER33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR13 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu21 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu31 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu12 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu32 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUL33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUL33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZUR33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZUR33 << endl;
  cout << setw(20) <<  "mdl_conjg__UV11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX11 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX12 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX13 << endl;
  cout << setw(20) <<  "mdl_conjg__UV12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV12 << endl;
  cout << setw(20) <<  "mdl_conjg__UV13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn11 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn21 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn31 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn12 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn12 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn22 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn32 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn13 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn13 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn23 << endl;
  cout << setw(20) <<  "mdl_conjg__Yn33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yn33 << endl;
  cout << setw(20) <<  "mdl_conjg__UV21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV21 << endl;
  cout << setw(20) <<  "mdl_conjg__UV22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV22 << endl;
  cout << setw(20) <<  "mdl_conjg__UV23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV23 << endl;
  cout << setw(20) <<  "mdl_conjg__UV31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV31 << endl;
  cout << setw(20) <<  "mdl_conjg__UV32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV32 << endl;
  cout << setw(20) <<  "mdl_conjg__UV33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__UV33 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX21 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX21 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX22 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX23 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX23 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX31 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX31 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX32 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX32 << endl;
  cout << setw(20) <<  "mdl_conjg__ZX33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__ZX33 << endl;
  cout << setw(20) <<  "mdl_el " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_el << endl;
  cout << setw(20) <<  "mdl_MWp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MWp << endl;
  cout << setw(20) <<  "mdl_MWp__exp__2 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_MWp__exp__2 << endl;
  cout << setw(20) <<  "mdl_TW " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_TW << endl;
  cout << setw(20) <<  "mdl_cos__TW " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_cos__TW << endl;
  cout << setw(20) <<  "mdl_g1 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_g1 << endl;
  cout << setw(20) <<  "mdl_sin__TW " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_sin__TW << endl;
  cout << setw(20) <<  "mdl_g2 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_g2 << endl;
  cout << setw(20) <<  "mdl_g2__exp__2 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_g2__exp__2 << endl;
  cout << setw(20) <<  "mdl_v " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_v << endl;
  cout << setw(20) <<  "mdl_Yu11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu11 << endl;
  cout << setw(20) <<  "mdl_Yu22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu22 << endl;
  cout << setw(20) <<  "mdl_Yu33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yu33 << endl;
  cout << setw(20) <<  "mdl_Yd11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd11 << endl;
  cout << setw(20) <<  "mdl_Yd22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd22 << endl;
  cout << setw(20) <<  "mdl_Yd33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Yd33 << endl;
  cout << setw(20) <<  "mdl_Ye11 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye11 << endl;
  cout << setw(20) <<  "mdl_Ye22 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye22 << endl;
  cout << setw(20) <<  "mdl_Ye33 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_Ye33 << endl;
  cout << setw(20) <<  "mdl_MHp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MHp << endl;
  cout << setw(20) <<  "mdl_MgWp " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MgWp << endl;
  cout << setw(20) <<  "mdl_MgWC " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << mdl_MgWC << endl;
  cout << setw(20) <<  "mdl_g1__exp__2 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_g1__exp__2 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd11 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd22 << endl;
  cout << setw(20) <<  "mdl_conjg__Yd33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yd33 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye11 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye22 << endl;
  cout << setw(20) <<  "mdl_conjg__Ye33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Ye33 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu11 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu11 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu22 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu22 << endl;
  cout << setw(20) <<  "mdl_conjg__Yu33 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_conjg__Yu33 << endl;
}
void Parameters_scotogenic_UFO::printIndependentCouplings()
{
  cout <<  "scotogenic_UFO model couplings independent of event kinematics:" <<
      endl;
  cout << setw(20) <<  "GC_3 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_3 << endl;
  cout << setw(20) <<  "GC_7 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_7 << endl;
  cout << setw(20) <<  "GC_8 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_8 << endl;
  cout << setw(20) <<  "GC_10 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_10 << endl;
  cout << setw(20) <<  "GC_12 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_12 << endl;
  cout << setw(20) <<  "GC_13 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_13 << endl;
  cout << setw(20) <<  "GC_14 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_14 << endl;
  cout << setw(20) <<  "GC_15 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_15 << endl;
  cout << setw(20) <<  "GC_16 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_16 << endl;
  cout << setw(20) <<  "GC_17 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_17 << endl;
  cout << setw(20) <<  "GC_24 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_24 << endl;
  cout << setw(20) <<  "GC_25 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_25 << endl;
  cout << setw(20) <<  "GC_26 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_26 << endl;
  cout << setw(20) <<  "GC_27 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_27 << endl;
  cout << setw(20) <<  "GC_29 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_29 << endl;
  cout << setw(20) <<  "GC_44 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_44 << endl;
  cout << setw(20) <<  "GC_45 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_45 << endl;
  cout << setw(20) <<  "GC_50 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_50 << endl;
  cout << setw(20) <<  "GC_51 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_51 << endl;
  cout << setw(20) <<  "GC_52 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_52 << endl;
  cout << setw(20) <<  "GC_58 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_58 << endl;
  cout << setw(20) <<  "GC_59 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_59 << endl;
  cout << setw(20) <<  "GC_172 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_172 << endl;
  cout << setw(20) <<  "GC_173 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_173 << endl;
  cout << setw(20) <<  "GC_174 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_174 << endl;
  cout << setw(20) <<  "GC_175 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_175 << endl;
  cout << setw(20) <<  "GC_176 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_176 << endl;
  cout << setw(20) <<  "GC_177 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_177 << endl;
  cout << setw(20) <<  "GC_178 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_178 << endl;
  cout << setw(20) <<  "GC_179 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_179 << endl;
  cout << setw(20) <<  "GC_180 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_180 << endl;
  cout << setw(20) <<  "GC_181 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_181 << endl;
  cout << setw(20) <<  "GC_182 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_182 << endl;
  cout << setw(20) <<  "GC_183 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_183 << endl;
  cout << setw(20) <<  "GC_184 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_184 << endl;
  cout << setw(20) <<  "GC_185 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_185 << endl;
  cout << setw(20) <<  "GC_186 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_186 << endl;
  cout << setw(20) <<  "GC_187 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_187 << endl;
  cout << setw(20) <<  "GC_188 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_188 << endl;
  cout << setw(20) <<  "GC_189 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_189 << endl;
  cout << setw(20) <<  "GC_217 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_217 << endl;
  cout << setw(20) <<  "GC_218 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_218 << endl;
  cout << setw(20) <<  "GC_219 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_219 << endl;
  cout << setw(20) <<  "GC_220 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_220 << endl;
  cout << setw(20) <<  "GC_221 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_221 << endl;
  cout << setw(20) <<  "GC_222 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_222 << endl;
  cout << setw(20) <<  "GC_223 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_223 << endl;
  cout << setw(20) <<  "GC_224 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_224 << endl;
  cout << setw(20) <<  "GC_225 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_225 << endl;
  cout << setw(20) <<  "GC_226 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_226 << endl;
  cout << setw(20) <<  "GC_227 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_227 << endl;
  cout << setw(20) <<  "GC_228 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_228 << endl;
  cout << setw(20) <<  "GC_229 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_229 << endl;
  cout << setw(20) <<  "GC_230 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_230 << endl;
  cout << setw(20) <<  "GC_231 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_231 << endl;
  cout << setw(20) <<  "GC_232 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_232 << endl;
  cout << setw(20) <<  "GC_233 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_233 << endl;
  cout << setw(20) <<  "GC_234 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_234 << endl;
  cout << setw(20) <<  "GC_235 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_235 << endl;
  cout << setw(20) <<  "GC_236 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_236 << endl;
  cout << setw(20) <<  "GC_237 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_237 << endl;
  cout << setw(20) <<  "GC_238 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_238 << endl;
  cout << setw(20) <<  "GC_239 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_239 << endl;
  cout << setw(20) <<  "GC_240 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_240 << endl;
  cout << setw(20) <<  "GC_241 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_241 << endl;
  cout << setw(20) <<  "GC_242 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_242 << endl;
  cout << setw(20) <<  "GC_243 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_243 << endl;
  cout << setw(20) <<  "GC_244 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_244 << endl;
  cout << setw(20) <<  "GC_245 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_245 << endl;
  cout << setw(20) <<  "GC_246 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_246 << endl;
  cout << setw(20) <<  "GC_247 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_247 << endl;
  cout << setw(20) <<  "GC_248 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_248 << endl;
  cout << setw(20) <<  "GC_249 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_249 << endl;
  cout << setw(20) <<  "GC_250 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_250 << endl;
  cout << setw(20) <<  "GC_251 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_251 << endl;
  cout << setw(20) <<  "GC_252 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_252 << endl;
  cout << setw(20) <<  "GC_286 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_286 << endl;
  cout << setw(20) <<  "GC_287 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_287 << endl;
  cout << setw(20) <<  "GC_292 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_292 << endl;
  cout << setw(20) <<  "GC_293 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_293 << endl;
  cout << setw(20) <<  "GC_294 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_294 << endl;
  cout << setw(20) <<  "GC_295 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_295 << endl;
  cout << setw(20) <<  "GC_296 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_296 << endl;
  cout << setw(20) <<  "GC_297 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_297 << endl;
  cout << setw(20) <<  "GC_298 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_298 << endl;
  cout << setw(20) <<  "GC_299 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_299 << endl;
  cout << setw(20) <<  "GC_300 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_300 << endl;
  cout << setw(20) <<  "GC_301 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_301 << endl;
  cout << setw(20) <<  "GC_302 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_302 << endl;
  cout << setw(20) <<  "GC_307 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_307 << endl;
  cout << setw(20) <<  "GC_308 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_308 << endl;
  cout << setw(20) <<  "GC_309 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_309 << endl;
  cout << setw(20) <<  "GC_310 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_310 << endl;
  cout << setw(20) <<  "GC_311 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_311 << endl;
  cout << setw(20) <<  "GC_312 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_312 << endl;
  cout << setw(20) <<  "GC_313 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_313 << endl;
  cout << setw(20) <<  "GC_314 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_314 << endl;
  cout << setw(20) <<  "GC_315 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_315 << endl;
  cout << setw(20) <<  "GC_316 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_316 << endl;
  cout << setw(20) <<  "GC_317 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_317 << endl;
  cout << setw(20) <<  "GC_322 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_322 << endl;
  cout << setw(20) <<  "GC_323 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_323 << endl;
  cout << setw(20) <<  "GC_334 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_334 << endl;
  cout << setw(20) <<  "GC_335 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_335 << endl;
  cout << setw(20) <<  "GC_340 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_340 << endl;
  cout << setw(20) <<  "GC_341 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_341 << endl;
  cout << setw(20) <<  "GC_346 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_346 << endl;
  cout << setw(20) <<  "GC_347 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_347 << endl;
  cout << setw(20) <<  "GC_348 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_348 << endl;
  cout << setw(20) <<  "GC_349 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_349 << endl;
  cout << setw(20) <<  "GC_350 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_350 << endl;
  cout << setw(20) <<  "GC_351 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_351 << endl;
  cout << setw(20) <<  "GC_352 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_352 << endl;
  cout << setw(20) <<  "GC_353 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_353 << endl;
  cout << setw(20) <<  "GC_354 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_354 << endl;
  cout << setw(20) <<  "GC_355 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_355 << endl;
  cout << setw(20) <<  "GC_356 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_356 << endl;
  cout << setw(20) <<  "GC_361 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_361 << endl;
  cout << setw(20) <<  "GC_362 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_362 << endl;
  cout << setw(20) <<  "GC_363 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_363 << endl;
  cout << setw(20) <<  "GC_364 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_364 << endl;
  cout << setw(20) <<  "GC_365 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_365 << endl;
  cout << setw(20) <<  "GC_366 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_366 << endl;
  cout << setw(20) <<  "GC_367 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_367 << endl;
  cout << setw(20) <<  "GC_368 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_368 << endl;
  cout << setw(20) <<  "GC_369 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_369 << endl;
  cout << setw(20) <<  "GC_371 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_371 << endl;
  cout << setw(20) <<  "GC_372 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_372 << endl;
  cout << setw(20) <<  "GC_118 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_118 << endl;
  cout << setw(20) <<  "GC_119 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_119 << endl;
  cout << setw(20) <<  "GC_120 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_120 << endl;
  cout << setw(20) <<  "GC_121 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_121 << endl;
  cout << setw(20) <<  "GC_122 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_122 << endl;
  cout << setw(20) <<  "GC_123 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_123 << endl;
  cout << setw(20) <<  "GC_124 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_124 << endl;
  cout << setw(20) <<  "GC_125 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_125 << endl;
  cout << setw(20) <<  "GC_126 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_126 << endl;
  cout << setw(20) <<  "GC_127 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_127 << endl;
  cout << setw(20) <<  "GC_128 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_128 << endl;
  cout << setw(20) <<  "GC_129 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_129 << endl;
  cout << setw(20) <<  "GC_130 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_130 << endl;
  cout << setw(20) <<  "GC_131 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_131 << endl;
  cout << setw(20) <<  "GC_132 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_132 << endl;
  cout << setw(20) <<  "GC_133 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_133 << endl;
  cout << setw(20) <<  "GC_134 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_134 << endl;
  cout << setw(20) <<  "GC_135 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_135 << endl;
  cout << setw(20) <<  "GC_136 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_136 << endl;
  cout << setw(20) <<  "GC_137 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_137 << endl;
  cout << setw(20) <<  "GC_138 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_138 << endl;
  cout << setw(20) <<  "GC_139 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_139 << endl;
  cout << setw(20) <<  "GC_140 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_140 << endl;
  cout << setw(20) <<  "GC_141 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_141 << endl;
  cout << setw(20) <<  "GC_142 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_142 << endl;
  cout << setw(20) <<  "GC_143 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_143 << endl;
  cout << setw(20) <<  "GC_144 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_144 << endl;
  cout << setw(20) <<  "GC_145 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_145 << endl;
  cout << setw(20) <<  "GC_146 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_146 << endl;
  cout << setw(20) <<  "GC_147 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_147 << endl;
  cout << setw(20) <<  "GC_148 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_148 << endl;
  cout << setw(20) <<  "GC_149 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_149 << endl;
  cout << setw(20) <<  "GC_150 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_150 << endl;
  cout << setw(20) <<  "GC_151 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_151 << endl;
  cout << setw(20) <<  "GC_152 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_152 << endl;
  cout << setw(20) <<  "GC_153 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_153 << endl;
  cout << setw(20) <<  "GC_154 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_154 << endl;
  cout << setw(20) <<  "GC_155 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_155 << endl;
  cout << setw(20) <<  "GC_156 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_156 << endl;
  cout << setw(20) <<  "GC_157 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_157 << endl;
  cout << setw(20) <<  "GC_158 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_158 << endl;
  cout << setw(20) <<  "GC_159 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_159 << endl;
  cout << setw(20) <<  "GC_160 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_160 << endl;
  cout << setw(20) <<  "GC_161 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_161 << endl;
  cout << setw(20) <<  "GC_162 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_162 << endl;
  cout << setw(20) <<  "GC_163 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_163 << endl;
  cout << setw(20) <<  "GC_164 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_164 << endl;
  cout << setw(20) <<  "GC_165 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_165 << endl;
  cout << setw(20) <<  "GC_166 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_166 << endl;
  cout << setw(20) <<  "GC_167 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_167 << endl;
  cout << setw(20) <<  "GC_168 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_168 << endl;
  cout << setw(20) <<  "GC_169 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_169 << endl;
  cout << setw(20) <<  "GC_170 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_170 << endl;
  cout << setw(20) <<  "GC_171 " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << GC_171 << endl;
}
void Parameters_scotogenic_UFO::printDependentParameters()
{
  cout <<  "scotogenic_UFO model parameters dependent on event kinematics:" <<
      endl;
  cout << setw(20) <<  "mdl_sqrt__aS " <<  "= " << setiosflags(ios::scientific)
      << setw(10) << mdl_sqrt__aS << endl;
  cout << setw(20) <<  "G " <<  "= " << setiosflags(ios::scientific) <<
      setw(10) << G << endl;
  cout << setw(20) <<  "mdl_G__exp__2 " <<  "= " <<
      setiosflags(ios::scientific) << setw(10) << mdl_G__exp__2 << endl;
}
void Parameters_scotogenic_UFO::printDependentCouplings()
{
  cout <<  "scotogenic_UFO model couplings dependent on event kinematics:" <<
      endl;

}


