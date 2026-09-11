# MadGraph Standalone Preparation Script

**Author:** Juan Diego Inga

## Overview

`prepare_mg5_standalone.py` is a Python utility designed to prepare a MadGraph5_aMC@NLO standalone C++ output from:

1. a user-provided UFO model,
2. a list of Z2-odd particles,
3. a MadGraph5_aMC installation,
4. and an output directory where the generated standalone code will be stored.

The goal of this script is to act as the bridge between the user's physics model and the rest of the dark-matter-cosmology workflow.

The script does **not** modify the MadGraph installation itself. Instead, it imports the UFO model directly from the path supplied by the user and asks MadGraph to generate the relevant standalone C++ structure.

---

## What the script is intended to do

The expected workflow is:

```text
UFO model
   +
Odd-particle list
   +
MadGraph path
   |
   v
prepare_mg5_standalone.py
   |
   v
MadGraph5_aMC
   |
   v
standalone_cpp output
   |
   +-- src/
   +-- lib/
   +-- SubProcesses/
   |
   v
UI / Kerrigan / sigmaV / relic-density pipeline
```

The script is therefore responsible for preparing the MadGraph standalone environment. It is not intended to replace Kerrigan, the sigmaV calculation, or the relic-density calculation.

---

## Why Python is used

Python is preferred over Bash for this stage because the program needs to do more than simply launch MadGraph.

The script:

- validates filesystem paths,
- validates the MadGraph installation,
- validates the UFO structure,
- parses `particles.py`,
- accepts either UFO particle names or PDG codes,
- resolves particle/antiparticle relationships,
- builds the odd sector,
- builds the complementary even sector,
- generates MadGraph commands,
- launches MadGraph,
- validates the generated standalone output,
- stores logs and metadata for reproducibility,
- and avoids accidental overwriting unless explicitly requested.

Bash would still be appropriate for simpler wrappers, but Python is better suited for this level of input validation and workflow orchestration.

---

## Requirements

The current version of the script is configured to require:

- Python 3
- MadGraph5_aMC@NLO **3.6.7 by default**
- a valid UFO model directory
- a list of Z2-odd particles

### Important note about the MadGraph version

The script currently checks for **exactly version 3.6.7 by default**.

This means that:

```text
3.6.7    -> accepted
3.6.8    -> rejected by default
3.7.0    -> rejected by default
3.5.6    -> rejected by default
```

This behavior is intentional because the current project/build environment was developed around MadGraph 3.6.7.

If the user wants to disable the exact-version check, the script supports:

```bash
--require-version any
```

Example:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /path/to/MG5_aMC \
    --ufo /path/to/model_UFO \
    --odd-file odd_particles.txt \
    --output /path/to/output \
    --require-version any
```

This disables the version restriction, but it does **not** guarantee compatibility with every newer MadGraph version.

If future testing confirms compatibility with MadGraph versions newer than 3.6.7, the validation policy can later be changed from:

```text
version == 3.6.7
```

to:

```text
version >= 3.6.7
```

For now, exact 3.6.7 is the safest default.

---

## Expected UFO structure

The path passed through `--ufo` should point to a valid UFO model directory containing files such as:

```text
model_UFO/
├── __init__.py
├── particles.py
├── parameters.py
├── vertices.py
├── couplings.py
├── lorentz.py
├── object_library.py
└── ...
```

The script validates the presence of the main UFO files before launching MadGraph.

---

## Odd-particle input

The user can provide the odd sector in two ways.

### Option 1: directly from the command line

Using UFO particle names:

```bash
--odd n1 n2 n3 etR etI etp
```

or using PDG codes:

```bash
--odd 1012 1014 1016 1001 1002 1003
```

PDG codes are generally recommended when possible because particle names may vary between UFO models.

### Option 2: from a text file

Example:

```text
# odd_particles.txt

1012
1014
1016
1001
1002
1003
```

The parser also accepts entries separated by spaces or commas.

For example:

```text
1012 1014 1016 1001 1002 1003
```

or:

```text
1012, 1014, 1016, 1001, 1002, 1003
```

---

## Particle and antiparticle handling

The script reads the particle definitions from `particles.py`.

If an odd particle is not self-conjugate, its antiparticle is automatically added by default.

For example, if:

```text
etp
```

has antiparticle:

```text
etm
```

then supplying only:

```text
etp
```

may result in both being included in the effective odd-sector definition.

This behavior can be disabled with:

```bash
--no-auto-antiparticles
```

---

## Default MadGraph generation strategy

By default, the script creates two MadGraph multiparticle definitions:

```text
dm_odd
dm_even
```

where:

```text
dm_odd  = user-selected odd particles
dm_even = physical UFO particles not included in dm_odd
```

The generated MadGraph commands are conceptually:

```text
import model /absolute/path/to/model_UFO

define dm_odd = ...
define dm_even = ...

generate dm_odd dm_odd > dm_even dm_even

output standalone_cpp /absolute/path/to/output
```

The important idea is that the Python script does not attempt to determine which Feynman diagrams are physically allowed.

MadGraph receives the model and decides which amplitudes and processes actually exist.

---

## Explicit generation mode

An alternative mode is available:

```bash
--generation-mode explicit
```

This generates commands of the form:

```text
generate n1 n1 > dm_even dm_even
add process n1 n2 > dm_even dm_even
add process n1 n3 > dm_even dm_even
...
```

This mode is useful when the user wants to inspect the initial-state combinations more explicitly.

The default `multiparticle` mode is generally more compact and more model-independent.

---

## Recommended first test: dry run

Before running MadGraph, validate the inputs with:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /path/to/MG5_aMC_v3_6_7 \
    --ufo /path/to/scotogenic_UFO \
    --odd-file odd_particles.txt \
    --output /path/to/scotogenic_standalone \
    --dry-run
```

A dry run:

- validates the MadGraph path,
- validates the MadGraph version,
- validates the UFO,
- reads the UFO particles,
- resolves the odd-particle list,
- constructs the MadGraph command card,
- prints the intended MadGraph commands,
- and does **not** run MadGraph.

The user should inspect the displayed `dm_odd` and `dm_even` definitions before continuing.

---

## Example real execution

Once the dry run is correct:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /path/to/MG5_aMC_v3_6_7 \
    --ufo /path/to/scotogenic_UFO \
    --odd-file odd_particles.txt \
    --output /path/to/scotogenic_standalone
```

or:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /path/to/MG5_aMC_v3_6_7 \
    --ufo /path/to/scotogenic_UFO \
    --odd 1012 1014 1016 1001 1002 1003 \
    --output /path/to/scotogenic_standalone
```

---

## Expected output

After a successful run, the output directory should contain a MadGraph standalone C++ structure similar to:

```text
scotogenic_standalone/
├── SubProcesses/
│   ├── P1_...
│   ├── P2_...
│   └── ...
├── src/
├── lib/
├── generation_commands.mg5
├── generation_manifest.json
├── odd_particles_resolved.txt
└── mg5_generation.log
```

The script verifies that:

```text
SubProcesses/
src/
lib/
```

exist and that at least one `P*` subprocess directory was generated.

---

## Generated metadata

### `generation_commands.mg5`

Contains the exact MadGraph command card used for the generation.

This is useful for:

- reproducibility,
- debugging,
- manual inspection,
- and comparing different runs.

### `generation_manifest.json`

Stores information such as:

- MadGraph path,
- MadGraph version,
- UFO path,
- requested odd particles,
- resolved particle names,
- resolved antiparticles,
- generation mode,
- output directory,
- subprocess count.

### `odd_particles_resolved.txt`

Contains the final odd-sector particle names used by MadGraph.

### `mg5_generation.log`

Contains the full MadGraph execution log.

---

## Overwrite protection

By default, the script refuses to overwrite an existing output directory.

If the user explicitly wants to replace it:

```bash
--force
```

Example:

```bash
python3 prepare_mg5_standalone.py \
    --mg5-root /path/to/MG5_aMC_v3_6_7 \
    --ufo /path/to/model_UFO \
    --odd-file odd_particles.txt \
    --output /path/to/standalone \
    --force
```

Use `--force` carefully.

---

## Recommended position in the project

A clean project layout could be:

```text
dark-matter-cosmology/
├── input/
│   ├── model_UFO/
│   └── odd_particles.txt
├── output/
├── scripts/
│   └── prepare_mg5_standalone.py
├── UI/
├── CMakeLists.txt
└── README.md
```

The generated MadGraph standalone can then be passed to the UI/Kerrigan workflow.

---

## Intended full project workflow

The long-term workflow is:

```text
UFO + odd-particle list
        |
        v
prepare_mg5_standalone.py
        |
        v
MadGraph standalone_cpp
        |
        +-- src/
        +-- lib/
        +-- SubProcesses/
        |
        v
select_effective_subprocesses_v3_ui.py
        |
        v
Kerrigan
        |
        +-- sigmaV
        |
        +-- relic-density workflow
```

This separation is intentional:

- `prepare_mg5_standalone.py` prepares MadGraph,
- the UI determines the relevant subprocess set,
- Kerrigan orchestrates the physics calculation,
- downstream code computes sigmaV and relic-density observables.

---

## Suggested user validation checklist

Before considering a run successful, verify:

- [ ] MadGraph path is correct.
- [ ] MadGraph version is accepted.
- [ ] UFO directory is valid.
- [ ] Odd particles are correctly identified.
- [ ] Antiparticles are handled as expected.
- [ ] Dry-run MadGraph commands look correct.
- [ ] `SubProcesses/` exists after the real run.
- [ ] `src/` exists.
- [ ] `lib/` exists.
- [ ] At least one `P*` subprocess directory exists.
- [ ] `generation_manifest.json` exists.
- [ ] `mg5_generation.log` contains no fatal MadGraph errors.
- [ ] The generated standalone can be passed to the UI/Kerrigan pipeline.

---

## Author

**Juan Diego Inga**

Dark Matter Cosmology Project
