# Dark Matter Cosmology

A C++ project for calculating dark matter observables using MadGraph5-generated matrix elements. This project computes sigma*v (velocity-weighted cross sections), evolution equations, and interpolation tables for dark matter models.

## Requirements

### Mandatory
- **CMake 3.10 or higher** - Build system
- **C++14 compatible compiler** (g++ 5.0+, clang 3.4+, or MSVC 2015+)
- **GSL (GNU Scientific Library)** - Required for numerical integration
- **MadGraph5_aMC@NLO 3.6.7** (exact version required)
- **Python 3.6+** - Required for the UI interface

### Optional
- **datamash** - For calculating totals in output files
  - Ubuntu/Debian: `sudo apt-get install datamash`
  - macOS: `brew install datamash`

## Important Note About Template Files

The repository uses **template files** for initial building, allowing you to compile and test the code immediately.

| Directory | Contents | Overwritten by |
|-----------|----------|----------------|
| `templates/model/` | MadGraph5 model files | `$MG5_OUTPUT_FOLDER/src/` |
| `templates/process/` | Template `CPPProcess.cc/h` | Each subprocess from `$MG5_OUTPUT_FOLDER/SubProcesses/P1_*/` |
| `templates/lib/` | Template libraries | `$MG5_OUTPUT_FOLDER/lib/` |

**Templates are only for initial testing** and are **automatically overwritten** by `Kerrigan.sh` at runtime.

## Building

### 1. Configure with CMake

Create a build directory and configure the project. You must specify the path to your MadGraph5 base directory:

```bash
mkdir build && cd build
cmake .. -DFOLDER=/path/to/your/MadGraph5_base_directory
```

Example:
```bash
cmake .. -DFOLDER=/home/user/MadGraph5/MG5_aMC_v3_6_7
```

> **Note:** Your MadGraph5 version must match exactly `3.6.7`. CMake will check the `VERSION` file in your MadGraph5 directory and fail if the version doesn't match.

During configuration, CMake will:
- Check your MadGraph5 version
- Run `scripts/modify_template.sh` to prepare template files
- Copy data files, scripts, and the UI to the build directory

### 2. Build the Project

```bash
make
```

This builds all three C++ executables:
- `bin/sigmav` - Sigma*v calculator
- `bin/evolution` - Evolution calculator
- `bin/interp` - Interpolation calculator (runs automatically after build if output doesn't exist)

## Running the Workflow

### Option 1: Use the UI (Recommended)

The project includes a Python-based UI for easier interaction:

```bash
# From the build directory
./run_ui

# Or using the make target
make ui
```

The UI provides a graphical interface to:
- Select MadGraph5 output folders
- Choose parameter cards
- Run calculations
- View results

### Option 2: Use Kerrigan.sh (Command Line)

For command-line usage or automation:

```bash
# From the build directory
./scripts/Kerrigan.sh DM_test

# Or using the make target
make run
```

Kerrigan.sh will:
1. Copy model files from `$MG5_OUTPUT_FOLDER/src/` → `build/model/` (overwrites templates)
2. Copy libraries from `$MG5_OUTPUT_FOLDER/lib/` → `build/lib/` (overwrites templates)
3. Build the model library with real files
4. For each subprocess:
   - Copy `CPPProcess.cc/h` to `build/process/` (overwrites templates)
   - Rebuild `sigmav`
   - Run calculations for each parameter card
5. Generate output files in `build/output/`

### Option 3: Run Individual Executables

```bash
# Run sigmav with a parameter card
./build/bin/sigmav build/data/cards/35_75-1.dat

# Run evolution
./build/bin/evolution

# Run interp (generates interp_ath.dat if not present)
./build/bin/interp
```

## Output

Results are saved in `build/output/<param_card_name>/` with:
- `P1_*.dat` - Results for each subprocess
- `TOTALS_T.dat` - Total cross sections
- `neq.dat` - Equilibrium data (if relic task)

## Quick Summary

```bash
# 1. Configure
mkdir build && cd build
cmake .. -DFOLDER=/path/to/MadGraph5/MG5_aMC_v3_6_7

# 2. Build
make

# 3. Run the UI
./run_ui

# OR run the command-line workflow
./scripts/Kerrigan.sh DM_test
```

## Troubleshooting

### "MadGraph5 version mismatch"
Your project requires exactly MadGraph5 3.6.7:
```bash
cat /path/to/MadGraph5/VERSION
# Should show: version = 3.6.7
```

### "GSL not found"
```bash
# Ubuntu/Debian
sudo apt-get install libgsl-dev

# macOS
brew install gsl
```

### "datamash not found" (warning)
```bash
# Ubuntu/Debian
sudo apt-get install datamash

# macOS
brew install datamash
```

### UI dependencies
If the UI requires additional Python packages:
```bash
pip install -r UI/requirements.txt
```

### Compilation warnings
Warnings from MadGraph5-generated code are **normal and safe to ignore**.

## Clean Build

```bash
rm -rf build
mkdir build && cd build
cmake .. -DFOLDER=/path/to/MadGraph5
make
```
