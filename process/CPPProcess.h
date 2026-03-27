//==========================================================================
// This file has been automatically generated for C++ Standalone by
// MadGraph5_aMC@NLO v. 3.6.6, 2025-10-30
// By the MadGraph5_aMC@NLO Development Team
// Visit launchpad.net/madgraph5 and amcatnlo.web.cern.ch
//==========================================================================

#ifndef MG5_Sigma_scotogenic_UFO_n3n3_nu3nu3_H
#define MG5_Sigma_scotogenic_UFO_n3n3_nu3nu3_H

#include <complex>
#include <vector>
#include <unordered_map>


#include "Parameters_scotogenic_UFO.h"

using namespace std; 

//==========================================================================
// A class for calculating the matrix elements for
// Process: n3 n3 > nu3 nu3 BSM<=1 HIG<=1 HIW<=1 WEIGHTED<=4 @1
//--------------------------------------------------------------------------

class CPPProcess
{
  public:

    // Constructor.
    CPPProcess() {}

    // Initialize process.
    virtual void initProc(string param_card_name); 

    // Calculate flavour-independent parts of cross section.
    virtual double sigmaKin(double s, double theta); 

    // Evaluate sigmaHat(sHat).
    virtual double sigmaHat(); 

    // Info on the subprocess.
    virtual string name() const {return "n3 n3 > nu3 nu3 (scotogenic_UFO)";}

    virtual int code() const {return 1;}

    const vector<double> & getMasses() const {return mME;}
    const vector<double> & getNewMasses() const {return newMasses;}
    const vector < std::pair < double, double >> & getNewDOF() const 
    {
      return newDOF; 
    }

    // Get and set momenta for matrix element evaluation
    vector < double * > getMomenta(){return p;}
    void setMomenta(vector < double * > & momenta){p = momenta;}
    void setInitial(int inid1, int inid2){id1 = inid1; id2 = inid2;}

    // Get matrix element vector
    const double * getMatrixElements() const {return matrix_element;}

    // Constants for array limits
    static const int ninitial = 2; 
    static const int nexternal = 4; 
    static const int nprocesses = 1; 

  private:

    // Private functions to calculate the matrix element for all subprocesses
    // Calculate wavefunctions
    void calculate_wavefunctions(const int perm[], const int hel[]); 
    static const int nwavefuncs = 8; 
    std::complex<double> w[nwavefuncs][6]; 
    static const int namplitudes = 4; 
    std::complex<double> amp[namplitudes]; 
    double matrix_1_n3n3_nu3nu3(); 

    // Store the matrix element value from sigmaKin
    double matrix_element[nprocesses]; 

    // Color flows, used when selecting color
    double * jamp2[nprocesses]; 

    // Pointer to the model parameters
    Parameters_scotogenic_UFO * pars; 

    // vector with masses of new particles
    vector<double> newMasses; 

    // dictionary with dof of new particles
    vector < std::pair < double, double >> newDOF; 

    // vector with external particle masses
    vector<double> mME; 

    // vector with momenta (to be changed each event)
    vector < double * > p; 
    // Initial particle ids
    int id1, id2; 

}; 


#endif // MG5_Sigma_scotogenic_UFO_n3n3_nu3nu3_H

