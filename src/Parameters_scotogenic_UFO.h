//==========================================================================
// This file has been automatically generated for C++
// MadGraph5_aMC@NLO v. 3.6.6, 2025-10-30
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#ifndef Parameters_scotogenic_UFO_H
#define Parameters_scotogenic_UFO_H

#include <complex>

#include "read_slha.h"
using namespace std; 

class Parameters_scotogenic_UFO
{
  public:

    static Parameters_scotogenic_UFO * getInstance(); 

    // Define "zero"
    double zero, ZERO; 
    // Model parameters independent of aS
    double mdl_WN3, mdl_WN2, mdl_WN1, mdl_WetI, mdl_WetR, mdl_Wh, mdl_WWp,
        mdl_WZ, mdl_Wu3, mdl_rZX33, mdl_rZX32, mdl_rZX31, mdl_rZX23, mdl_rZX22,
        mdl_rZX21, mdl_rZX13, mdl_rZX12, mdl_rZX11, mdl_rYn33, mdl_rYn32,
        mdl_rYn31, mdl_rYn23, mdl_rYn22, mdl_rYn21, mdl_rYn13, mdl_rYn12,
        mdl_rYn11, mdl_rUV33, mdl_rUV32, mdl_rUV31, mdl_rUV23, mdl_rUV22,
        mdl_rUV21, mdl_rUV13, mdl_rUV12, mdl_rUV11, mdl_rZUR33, mdl_rZUR32,
        mdl_rZUR31, mdl_rZUR23, mdl_rZUR22, mdl_rZUR21, mdl_rZUR13, mdl_rZUR12,
        mdl_rZUR11, mdl_rZUL33, mdl_rZUL32, mdl_rZUL31, mdl_rZUL23, mdl_rZUL22,
        mdl_rZUL21, mdl_rZUL13, mdl_rZUL12, mdl_rZUL11, mdl_rZER33, mdl_rZER32,
        mdl_rZER31, mdl_rZER23, mdl_rZER22, mdl_rZER21, mdl_rZER13, mdl_rZER12,
        mdl_rZER11, mdl_rZEL33, mdl_rZEL32, mdl_rZEL31, mdl_rZEL23, mdl_rZEL22,
        mdl_rZEL21, mdl_rZEL13, mdl_rZEL12, mdl_rZEL11, mdl_rZDR33, mdl_rZDR32,
        mdl_rZDR31, mdl_rZDR23, mdl_rZDR22, mdl_rZDR21, mdl_rZDR13, mdl_rZDR12,
        mdl_rZDR11, mdl_rZDL33, mdl_rZDL32, mdl_rZDL31, mdl_rZDL23, mdl_rZDL22,
        mdl_rZDL21, mdl_rZDL13, mdl_rZDL12, mdl_rZDL11, aS, mdl_Gf, aEWM1,
        mdl_MN3, mdl_MN2, mdl_MN1, mdl_Metp, mdl_MetI, mdl_MetR, mdl_Mh,
        mdl_MZ, mdl_Me3, mdl_Me2, mdl_Me1, mdl_Mu3, mdl_Md3, mdl_Mu2, mdl_Md2,
        mdl_Mu1, mdl_Md1, mdl_iZX33, mdl_iZX32, mdl_iZX31, mdl_iZX23,
        mdl_iZX22, mdl_iZX21, mdl_iZX13, mdl_iZX12, mdl_iZX11, mdl_iYn33,
        mdl_iYn32, mdl_iYn31, mdl_iYn23, mdl_iYn22, mdl_iYn21, mdl_iYn13,
        mdl_iYn12, mdl_iYn11, mdl_iUV33, mdl_iUV32, mdl_iUV31, mdl_iUV23,
        mdl_iUV22, mdl_iUV21, mdl_iUV13, mdl_iUV12, mdl_iUV11, mdl_iZUR33,
        mdl_iZUR32, mdl_iZUR31, mdl_iZUR23, mdl_iZUR22, mdl_iZUR21, mdl_iZUR13,
        mdl_iZUR12, mdl_iZUR11, mdl_iZUL33, mdl_iZUL32, mdl_iZUL31, mdl_iZUL23,
        mdl_iZUL22, mdl_iZUL21, mdl_iZUL13, mdl_iZUL12, mdl_iZUL11, mdl_iZER33,
        mdl_iZER32, mdl_iZER31, mdl_iZER23, mdl_iZER22, mdl_iZER21, mdl_iZER13,
        mdl_iZER12, mdl_iZER11, mdl_iZEL33, mdl_iZEL32, mdl_iZEL31, mdl_iZEL23,
        mdl_iZEL22, mdl_iZEL21, mdl_iZEL13, mdl_iZEL12, mdl_iZEL11, mdl_iZDR33,
        mdl_iZDR32, mdl_iZDR31, mdl_iZDR23, mdl_iZDR22, mdl_iZDR21, mdl_iZDR13,
        mdl_iZDR12, mdl_iZDR11, mdl_iZDL33, mdl_iZDL32, mdl_iZDL31, mdl_iZDL23,
        mdl_iZDL22, mdl_iZDL21, mdl_iZDL13, mdl_iZDL12, mdl_iZDL11, mdl_ilam4,
        mdl_ilam3, mdl_ilam2, mdl_ilam1, mdl_lam5, mdl_rlam4, mdl_rlam3,
        mdl_rlam2, mdl_rlam1, mdl_MZ__exp__2, mdl_MZ__exp__4, mdl_sqrt__2,
        mdl_RXiWp, mdl_RXiZ, mdl_MAh, mdl_MgZ, mdl_el, mdl_MWp,
        mdl_MWp__exp__2, mdl_TW, mdl_cos__TW, mdl_g1, mdl_sin__TW, mdl_g2,
        mdl_g2__exp__2, mdl_v, mdl_MHp, mdl_MgWp, mdl_MgWC, mdl_g1__exp__2;
    std::complex<double> mdl_complexi, mdl_Yn11, mdl_Yn12, mdl_Yn13, mdl_Yn21,
        mdl_Yn22, mdl_Yn23, mdl_Yn31, mdl_Yn32, mdl_Yn33, mdl_lam1, mdl_lam2,
        mdl_lam4, mdl_lam3, mdl_ZX11, mdl_ZX12, mdl_ZX13, mdl_ZX21, mdl_ZX22,
        mdl_ZX23, mdl_ZX31, mdl_ZX32, mdl_ZX33, mdl_UV11, mdl_UV12, mdl_UV13,
        mdl_UV21, mdl_UV22, mdl_UV23, mdl_UV31, mdl_UV32, mdl_UV33, mdl_ZDL11,
        mdl_ZDL12, mdl_ZDL13, mdl_ZDL21, mdl_ZDL22, mdl_ZDL23, mdl_ZDL31,
        mdl_ZDL32, mdl_ZDL33, mdl_ZDR11, mdl_ZDR12, mdl_ZDR13, mdl_ZDR21,
        mdl_ZDR22, mdl_ZDR23, mdl_ZDR31, mdl_ZDR32, mdl_ZDR33, mdl_ZUL11,
        mdl_ZUL12, mdl_ZUL13, mdl_ZUL21, mdl_ZUL22, mdl_ZUL23, mdl_ZUL31,
        mdl_ZUL32, mdl_ZUL33, mdl_ZUR11, mdl_ZUR12, mdl_ZUR13, mdl_ZUR21,
        mdl_ZUR22, mdl_ZUR23, mdl_ZUR31, mdl_ZUR32, mdl_ZUR33, mdl_ZEL11,
        mdl_ZEL12, mdl_ZEL13, mdl_ZEL21, mdl_ZEL22, mdl_ZEL23, mdl_ZEL31,
        mdl_ZEL32, mdl_ZEL33, mdl_ZER11, mdl_ZER12, mdl_ZER13, mdl_ZER21,
        mdl_ZER22, mdl_ZER23, mdl_ZER31, mdl_ZER32, mdl_ZER33, mdl_Yu12,
        mdl_Yu13, mdl_Yu21, mdl_Yu23, mdl_Yu31, mdl_Yu32, mdl_Yd12, mdl_Yd13,
        mdl_Yd21, mdl_Yd23, mdl_Yd31, mdl_Yd32, mdl_Ye12, mdl_Ye13, mdl_Ye21,
        mdl_Ye23, mdl_Ye31, mdl_Ye32, mdl_conjg__lam1, mdl_conjg__lam3,
        mdl_conjg__lam4, mdl_conjg__ZDL11, mdl_conjg__ZDR11, mdl_conjg__ZDR12,
        mdl_conjg__ZDR13, mdl_conjg__ZDL12, mdl_conjg__ZDL13, mdl_conjg__Yd21,
        mdl_conjg__Yd31, mdl_conjg__Yd12, mdl_conjg__Yd32, mdl_conjg__Yd13,
        mdl_conjg__Yd23, mdl_conjg__ZDL21, mdl_conjg__ZDL22, mdl_conjg__ZDL23,
        mdl_conjg__ZDL31, mdl_conjg__ZDL32, mdl_conjg__ZDL33, mdl_conjg__ZDR21,
        mdl_conjg__ZDR22, mdl_conjg__ZDR23, mdl_conjg__ZDR31, mdl_conjg__ZDR32,
        mdl_conjg__ZDR33, mdl_conjg__ZEL11, mdl_conjg__ZER11, mdl_conjg__ZER12,
        mdl_conjg__ZER13, mdl_conjg__ZEL12, mdl_conjg__ZEL13, mdl_conjg__Ye21,
        mdl_conjg__Ye31, mdl_conjg__Ye12, mdl_conjg__Ye32, mdl_conjg__Ye13,
        mdl_conjg__Ye23, mdl_conjg__ZEL21, mdl_conjg__ZEL22, mdl_conjg__ZEL23,
        mdl_conjg__ZEL31, mdl_conjg__ZEL32, mdl_conjg__ZEL33, mdl_conjg__ZER21,
        mdl_conjg__ZER22, mdl_conjg__ZER23, mdl_conjg__ZER31, mdl_conjg__ZER32,
        mdl_conjg__ZER33, mdl_conjg__ZUL11, mdl_conjg__ZUR11, mdl_conjg__ZUR12,
        mdl_conjg__ZUR13, mdl_conjg__ZUL12, mdl_conjg__ZUL13, mdl_conjg__Yu21,
        mdl_conjg__Yu31, mdl_conjg__Yu12, mdl_conjg__Yu32, mdl_conjg__Yu13,
        mdl_conjg__Yu23, mdl_conjg__ZUL21, mdl_conjg__ZUL22, mdl_conjg__ZUL23,
        mdl_conjg__ZUL31, mdl_conjg__ZUL32, mdl_conjg__ZUL33, mdl_conjg__ZUR21,
        mdl_conjg__ZUR22, mdl_conjg__ZUR23, mdl_conjg__ZUR31, mdl_conjg__ZUR32,
        mdl_conjg__ZUR33, mdl_conjg__UV11, mdl_conjg__ZX11, mdl_conjg__ZX12,
        mdl_conjg__ZX13, mdl_conjg__UV12, mdl_conjg__UV13, mdl_conjg__Yn11,
        mdl_conjg__Yn21, mdl_conjg__Yn31, mdl_conjg__Yn12, mdl_conjg__Yn22,
        mdl_conjg__Yn32, mdl_conjg__Yn13, mdl_conjg__Yn23, mdl_conjg__Yn33,
        mdl_conjg__UV21, mdl_conjg__UV22, mdl_conjg__UV23, mdl_conjg__UV31,
        mdl_conjg__UV32, mdl_conjg__UV33, mdl_conjg__ZX21, mdl_conjg__ZX22,
        mdl_conjg__ZX23, mdl_conjg__ZX31, mdl_conjg__ZX32, mdl_conjg__ZX33,
        mdl_Yu11, mdl_Yu22, mdl_Yu33, mdl_Yd11, mdl_Yd22, mdl_Yd33, mdl_Ye11,
        mdl_Ye22, mdl_Ye33, mdl_conjg__Yd11, mdl_conjg__Yd22, mdl_conjg__Yd33,
        mdl_conjg__Ye11, mdl_conjg__Ye22, mdl_conjg__Ye33, mdl_conjg__Yu11,
        mdl_conjg__Yu22, mdl_conjg__Yu33;
    // Model couplings independent of aS
    std::complex<double> GC_3, GC_7, GC_8, GC_10, GC_12, GC_13, GC_14, GC_15,
        GC_16, GC_17, GC_24, GC_25, GC_26, GC_27, GC_29, GC_44, GC_45, GC_50,
        GC_51, GC_52, GC_58, GC_59, GC_172, GC_173, GC_174, GC_175, GC_176,
        GC_177, GC_178, GC_179, GC_180, GC_181, GC_182, GC_183, GC_184, GC_185,
        GC_186, GC_187, GC_188, GC_189, GC_217, GC_218, GC_219, GC_220, GC_221,
        GC_222, GC_223, GC_224, GC_225, GC_226, GC_227, GC_228, GC_229, GC_230,
        GC_231, GC_232, GC_233, GC_234, GC_235, GC_236, GC_237, GC_238, GC_239,
        GC_240, GC_241, GC_242, GC_243, GC_244, GC_245, GC_246, GC_247, GC_248,
        GC_249, GC_250, GC_251, GC_252, GC_286, GC_287, GC_292, GC_293, GC_294,
        GC_295, GC_296, GC_297, GC_298, GC_299, GC_300, GC_301, GC_302, GC_307,
        GC_308, GC_309, GC_310, GC_311, GC_312, GC_313, GC_314, GC_315, GC_316,
        GC_317, GC_322, GC_323, GC_334, GC_335, GC_340, GC_341, GC_346, GC_347,
        GC_348, GC_349, GC_350, GC_351, GC_352, GC_353, GC_354, GC_355, GC_356,
        GC_361, GC_362, GC_363, GC_364, GC_365, GC_366, GC_367, GC_368, GC_369,
        GC_371, GC_372, GC_118, GC_119, GC_120, GC_121, GC_122, GC_123, GC_124,
        GC_125, GC_126, GC_127, GC_128, GC_129, GC_130, GC_131, GC_132, GC_133,
        GC_134, GC_135, GC_136, GC_137, GC_138, GC_139, GC_140, GC_141, GC_142,
        GC_143, GC_144, GC_145, GC_146, GC_147, GC_148, GC_149, GC_150, GC_151,
        GC_152, GC_153, GC_154, GC_155, GC_156, GC_157, GC_158, GC_159, GC_160,
        GC_161, GC_162, GC_163, GC_164, GC_165, GC_166, GC_167, GC_168, GC_169,
        GC_170, GC_171;
    // Model parameters dependent on aS
    double mdl_sqrt__aS, G, mdl_G__exp__2; 
    // Model couplings dependent on aS


    // Set parameters that are unchanged during the run
    void setIndependentParameters(SLHAReader& slha); 
    // Set couplings that are unchanged during the run
    void setIndependentCouplings(); 
    // Set parameters that are changed event by event
    void setDependentParameters(); 
    // Set couplings that are changed event by event
    void setDependentCouplings(); 

    // Print parameters that are unchanged during the run
    void printIndependentParameters(); 
    // Print couplings that are unchanged during the run
    void printIndependentCouplings(); 
    // Print parameters that are changed event by event
    void printDependentParameters(); 
    // Print couplings that are changed event by event
    void printDependentCouplings(); 


  private:
    static Parameters_scotogenic_UFO * instance; 
}; 

#endif // Parameters_scotogenic_UFO_H

