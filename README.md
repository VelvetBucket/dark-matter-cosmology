# Dark Matter Cosmology

A C++ project for calculating dark matter observables using MadGraph5-generated matrix elements. This project computes sigma*v (velocity-weighted cross sections), evolution equations, and interpolation tables for dark matter models.

## Requirements

### Mandatory
- **CMake 3.10 or higher** - Build system
- **C++14 compatible compiler** (g++ 5.0+, clang 3.4+, or MSVC 2015+)
- **GSL (GNU Scientific Library)** - Required for numerical integration
- **MadGraph5_aMC@NLO 3.6.7** (exact version required)

## Important Note About Source Files

The repository contains **placeholder/test files** in the following directories:

| Directory | Contents | Overwritten by |
|-----------|----------|----------------|
| `src/core/model/` | MadGraph5 model files (`HelAmps_*.cc`, `Parameters_*.cc`, etc.) | `$MG5_OUTPUT_FOLDER/src/` |
| `external/lib/` | MadGraph5 libraries (`libmodel_scotogenic_UFO.a`, PDF data) | `$MG5_OUTPUT_FOLDER/lib/` |
| `process/` | Temporary location for `CPPProcess.cc` and `CPPProcess.h` | Each subprocess from `$MG5_OUTPUT_FOLDER/SubProcesses/P1_*/` |

**These are only for initial testing** and will be **automatically overwritten** by `overseer.sh` when you run it with your MadGraph5 output folder. 

The actual workflow:
1. `src/core/model/` ← Copied from `$MG5_OUTPUT_FOLDER/src/`
2. `external/lib/` ← Copied from `$MG5_OUTPUT_FOLDER/lib/`
3. `process/` ← Copy `CPPProcess.cc/h` from each subprocess (changes per iteration)

> **Note:** The `process/` folder is special - it gets overwritten **for each subprocess** during the `overseer.sh` loop, which is why `sigmav` needs to be rebuilt (`make force-sigmav`) after each copy.

## Building

### 1. Configure with CMake

Create a build directory and configure the project with CMake. You must specify the path to your MadGraph5 base directory:

```bash
mkdir build && cd build
cmake .. -DFOLDER=/path/to/your/MadGraph5_base_directory
```

Example:

```bash
cmake .. -DFOLDER=/home/user/MadGraph5/MG5_aMC_v3_6_7
```

> **Note:** Your MadGraph5 version must match exactly 3.6.7. CMake will check the VERSION file in your MadGraph5 directory and fail if the version doesn't match.

### 2. Build the Project

Once CMake configuration is complete, build the project using make:

```bash
make
```
