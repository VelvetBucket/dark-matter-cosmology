# Dark Matter Cosmology

A C++ project for calculating dark matter observables using MadGraph5-generated matrix elements. This project computes sigma*v (velocity-weighted cross sections), evolution equations, and interpolation tables for dark matter models.

## Requirements

### Mandatory
- **CMake 3.10 or higher** - Build system
- **C++14 compatible compiler** (g++ 5.0+, clang 3.4+, or MSVC 2015+)
- **GSL (GNU Scientific Library)** - Required for numerical integration
- **MadGraph5_aMC@NLO 3.6.7** (exact version required)
