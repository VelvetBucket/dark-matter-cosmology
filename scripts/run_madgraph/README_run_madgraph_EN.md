# `run_madgraph.py` — MadGraph Standalone Preparation Guide

**Author:** Juan Diego Inga  
**Project:** Dark Matter Cosmology  
**Recommended script name:** `scripts/run_madgraph.py`

---

## 1. Purpose

`run_madgraph.py` prepares the MadGraph standalone C++ output required by the rest of the dark-matter pipeline.

It receives, directly or through the CMake build workspace:

1. a UFO model,
2. a list of Z2-odd particles,
3. a MadGraph5_aMC installation,

and generates a standalone MadGraph output containing:

```text
SubProcesses/
src/
lib/        # when produced by MadGraph
```

That generated directory is the **MG5 output root** consumed by the subprocess-selection UI and Kerrigan.

The script does **not** modify:

- the original UFO model,
- the MadGraph installation,
- the original MadGraph source tree.

---

## 2. Where this script belongs in the pipeline

The recommended project flow is:

```text
1. Configure the project with CMake
                |
                v
2. CMake creates/configures the build workspace
                |
                v
3. User places the UFO and odd-particle list in build/input/
                |
                v
4. scripts/run_madgraph.py
                |
                v
5. MadGraph generates standalone_cpp
                |
                v
6. build/generated/<MODEL>_standalone/
   ├── SubProcesses/
   ├── src/
   └── lib/   [optional]
                |
                v
7. select_effective_subprocesses_v3_ui.py
                |
                v
8. Kerrigan.sh
                |
                +--> sigmaV
                |
                +--> relic-density pipeline
```

### Important

`run_madgraph.py` should be run **after CMake configuration** because pipeline mode reads the configured build directory and can obtain the MadGraph path from `CMakeCache.txt`.

The script itself does not require Kerrigan or the UI to have run yet.

---

## 3. Official file to keep

The project should keep:

```text
scripts/run_madgraph.py
```

The development file:

```text
prepare_mg5_standalone_updated.py
```

contains the same implementation and is not required if `run_madgraph.py` is present.

The older:

```text
prepare_mg5_standalone.py
```

should be removed or archived to avoid having two different versions of the same pipeline stage.

If any CMake file, shell script, README, CI workflow, or documentation still refers to:

```text
prepare_mg5_standalone.py
```

update that reference to:

```text
run_madgraph.py
```

---

## 4. Recommended pipeline layout

After CMake configuration, a normal workspace can look like:

```text
build/
├── CMakeCache.txt
├── input/
│   ├── MyModel_UFO/
│   │   ├── __init__.py
│   │   ├── particles.py
│   │   ├── parameters.py
│   │   ├── vertices.py
│   │   ├── couplings.py
│   │   ├── lorentz.py
│   │   ├── object_library.py
│   │   └── ...
│   │
│   └── odd_particles.txt
│
├── generated/
└── ...
```

The simplest invocation is then:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

---

## 5. What pipeline mode automatically discovers

When called with:

```bash
--build-dir build
```

the script can automatically resolve:

### MadGraph

The script searches `CMakeCache.txt` for common variables such as:

```text
MADGRAPH_DIR
MADGRAPH_ROOT
MG5_DIR
MG5_ROOT
MG5_BASE_DIR
FOLDER
```

It also accepts equivalent environment variables.

The selected directory must actually contain:

```text
bin/mg5_aMC
```

or:

```text
bin/mg5
```

The script does not trust a path merely because it exists in CMake cache.

---

### UFO model

If `--ufo` is not supplied, the script searches:

```text
build/input/
```

for exactly one valid UFO model.

A UFO is recognized by the presence of the main files:

```text
particles.py
parameters.py
vertices.py
couplings.py
lorentz.py
object_library.py
__init__.py
```

If no UFO is found, the script stops.

If more than one UFO is found, the script also stops instead of guessing.

In that case use:

```bash
--ufo /path/to/SpecificModel_UFO
```

---

### Odd-particle list

If neither `--odd` nor `--odd-file` is supplied, pipeline mode looks for:

```text
odd_particles.txt
odd_particles.dat
odd_particles
```

inside the input directory.

The recommended name is:

```text
odd_particles.txt
```

---

### Output

If `--output` is not supplied, pipeline mode generates:

```text
build/generated/<UFO-directory-name>_standalone/
```

Example:

```text
build/generated/scotogenic_UFO_standalone/
```

---

## 6. MadGraph version policy

The current default supported range is:

```text
3.6.7 <= MadGraph <= 3.7.0
```

Therefore:

```text
3.6.7  -> accepted
3.6.8  -> accepted
3.7.0  -> accepted
3.7.1  -> rejected by default
3.5.6  -> rejected by default
```

This range is intentionally conservative and should represent versions tested by the project.

### Override the supported range

You may explicitly use:

```bash
--min-version 3.6.7
--max-version 3.7.0
```

### Require one exact version

For backward-compatible strict validation:

```bash
--require-version 3.6.7
```

### Disable version validation

For development/testing only:

```bash
--require-version any
```

Disabling the check does **not** imply that every MadGraph version is supported.

---

## 7. Odd-particle input

The odd sector can be specified using either UFO names or PDG codes.

### Recommended: PDG codes

Example `build/input/odd_particles.txt`:

```text
# Z2-odd sector
1012
1014
1016
1001
1002
1003
```

Values may also be written as:

```text
1012 1014 1016 1001 1002 1003
```

or:

```text
1012, 1014, 1016, 1001, 1002, 1003
```

Comments beginning with `#` are ignored.

### Direct command-line input

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --odd 1012 1014 1016 1001 1002 1003
```

UFO particle names are also accepted:

```bash
--odd n1 n2 n3 etR etI etp
```

PDG codes are generally preferred because UFO naming conventions may vary between models.

---

## 8. Particle / antiparticle handling

The script reads `particles.py` without executing the UFO.

For every odd state it resolves:

- PDG code,
- particle name,
- antiparticle name,
- whether the state is self-conjugate.

By default, when an odd particle is not self-conjugate, the antiparticle is automatically included.

Example:

```text
input: etp
resolved odd states: etp etm
```

Disable this behavior only when intentionally required:

```bash
--no-auto-antiparticles
```

---

## 9. Even-sector construction

After the odd sector is resolved, all remaining physical propagating UFO particles are used to construct:

```text
dm_even
```

Goldstone bosons, ghosts, and explicitly non-propagating particles are excluded by the parser when the UFO declares those properties.

The basic definitions generated for MadGraph are conceptually:

```text
define dm_odd = ...
define dm_even = ...
```

---

## 10. Default generation strategy

The default is:

```bash
--generation-mode multiparticle
```

which creates:

```text
import model /absolute/path/to/model_UFO

define dm_odd = ...
define dm_even = ...

generate dm_odd dm_odd > dm_even dm_even

output standalone_cpp /absolute/path/to/output
```

MadGraph is responsible for determining which amplitudes/processes actually exist in the UFO.

The Python script does not attempt to reproduce MadGraph's diagram generation.

---

## 11. Explicit generation mode

For debugging or inspection:

```bash
--generation-mode explicit
```

The program builds all unordered odd-particle initial pairs and generates commands conceptually equivalent to:

```text
generate n1 n1 > dm_even dm_even
add process n1 n2 > dm_even dm_even
add process n1 n3 > dm_even dm_even
...
```

The default `multiparticle` mode is recommended for normal use.

---

## 12. First recommended test: pipeline dry run

After configuring CMake and placing the UFO and odd list in `build/input/`:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Expected summary:

```text
Invocation mode    : pipeline
CMake build        : /.../build
Pipeline input     : /.../build/input
MG5 root           : /.../MG5_aMC...
MG5 executable     : /.../bin/mg5_aMC
MG5 version        : 3.6.7 ... 3.7.0
UFO model          : /.../build/input/MyModel_UFO
Odd-particle file  : /.../build/input/odd_particles.txt
Standalone output  : /.../build/generated/MyModel_UFO_standalone
```

The program must also print:

```text
Resolved odd-particle input:
```

and the complete MadGraph command card.

### Dry-run guarantee

`--dry-run` does not execute MadGraph and does not create the standalone output.

It may create the temporary generated `.mg5` command file beside the planned output so the command card can be inspected.

---

## 13. Real pipeline execution

Once the dry run looks correct:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

Expected output:

```text
SUCCESS
Standalone output  : /.../build/generated/MyModel_UFO_standalone
Subprocesses       : N
src/               : yes
lib/               : yes
```

or:

```text
lib/               : no (allowed)
```

---

## 14. Expected standalone output

A successful run produces:

```text
build/generated/MyModel_UFO_standalone/
├── SubProcesses/
│   ├── P1_...
│   ├── P2_...
│   └── ...
├── src/
├── lib/                         # optional
├── generation_commands.mg5
├── generation_manifest.json
├── odd_particles_resolved.txt
└── mg5_generation.log
```

### Required by the current UI/Kerrigan contract

```text
SubProcesses/
src/
```

### Optional

```text
lib/
```

If `lib/` is not produced, the script emits a warning rather than failing.

This is intentional because the current Kerrigan contract can retain build-side libraries when the generated standalone does not provide a `lib/` directory.

---

## 15. Pipeline pointer files

In pipeline mode the script also creates:

```text
build/generated/current_mg5_output.txt
build/generated/current_mg5_output.json
```

`current_mg5_output.txt` contains the absolute path to the latest successfully generated standalone root.

Example:

```text
/home/user/project/build/generated/scotogenic_UFO_standalone
```

The JSON pointer also stores:

```text
mg5_output
subprocesses
generation_manifest
```

These pointer files are convenience metadata.

The current UI and Kerrigan do **not** depend on them, so this feature does not alter the existing runtime contract.

---

## 16. Files stored for reproducibility

### `generation_commands.mg5`

The exact MadGraph command card used.

### `generation_manifest.json`

Contains information such as:

- invocation mode,
- CMake build directory,
- input directory,
- MadGraph path,
- MadGraph executable,
- MadGraph version,
- UFO path,
- complete particle catalogue,
- original odd input,
- resolved odd states,
- automatically added antiparticles,
- even states,
- odd initial-state pairs,
- generated subprocess directories,
- whether `lib/` was present.

### `odd_particles_resolved.txt`

Final odd particle names sent to MadGraph.

### `mg5_generation.log`

Complete MadGraph standard output/error log.

---

## 17. Passing the result to the UI

At the end of a successful run the script prints:

```text
Next-step paths:
  --mg5-output /.../MyModel_UFO_standalone
  --subprocesses /.../MyModel_UFO_standalone/SubProcesses
```

Example:

```bash
python3 UI/select_effective_subprocesses_v3_ui.py \
    /path/to/param_card.dat \
    --build-dir build \
    --mg5-output build/generated/MyModel_UFO_standalone \
    --subprocesses build/generated/MyModel_UFO_standalone/SubProcesses \
    --mode combined \
    --candidate 1012 \
    --task sigmav
```

The UI then selects the effective subset and calls the CMake-generated Kerrigan runtime.

---

## 18. Backward-compatible explicit mode

Pipeline mode is preferred, but all important paths can still be provided manually:

```bash
python3 scripts/run_madgraph.py \
    --mg5-root /path/to/MG5_aMC \
    --ufo /path/to/MyModel_UFO \
    --odd-file /path/to/odd_particles.txt \
    --output /path/to/MyModel_standalone
```

or:

```bash
python3 scripts/run_madgraph.py \
    --mg5-root /path/to/MG5_aMC \
    --ufo /path/to/MyModel_UFO \
    --odd 1012 1014 1016 \
    --output /path/to/MyModel_standalone
```

This preserves compatibility with earlier workflows.

---

## 19. Output overwrite protection

By default, if the requested standalone directory already exists the script stops:

```text
ERROR: Output already exists...
```

To explicitly replace it:

```bash
--force
```

Example:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --force
```

`--force` recursively deletes the selected output directory before MadGraph regenerates it.

Use it only when the target path has been verified.

---

# 20. Recommended validation tests

## Test 1 — Python syntax

```bash
python3 -m py_compile scripts/run_madgraph.py
```

Expected:

```text
no output
exit code 0
```

---

## Test 2 — Help

```bash
python3 scripts/run_madgraph.py --help
```

Expected to include:

```text
--build-dir
--input-dir
--mg5-root
--ufo
--odd
--odd-file
--output
--generation-mode
--min-version
--max-version
--require-version
--force
--dry-run
```

---

## Test 3 — Automatic pipeline discovery

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Check that the printed:

```text
MG5 root
UFO model
Odd-particle file
Standalone output
```

are all correct.

---

## Test 4 — Explicit UFO override

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --ufo /path/to/MyModel_UFO \
    --dry-run
```

The explicit UFO must override automatic discovery.

---

## Test 5 — Direct odd-PDG override

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --odd 1012 1014 1016 \
    --dry-run
```

The script should not require `odd_particles.txt`.

---

## Test 6 — Ambiguous UFO input

Place two valid UFO directories under `build/input/` and run:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --dry-run
```

Expected:

```text
ERROR: More than one UFO model was found...
```

Then verify explicit selection works:

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --ufo build/input/ChosenModel_UFO \
    --dry-run
```

---

## Test 7 — Unsupported MadGraph version

Using an installation outside the default range should fail before generation.

Expected policy:

```text
3.6.7 <= version <= 3.7.0
```

---

## Test 8 — Exact-version override

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --require-version 3.6.7 \
    --dry-run
```

Only 3.6.7 should pass.

---

## Test 9 — Version-check bypass

```bash
python3 scripts/run_madgraph.py \
    --build-dir build \
    --require-version any \
    --dry-run
```

This should bypass version validation.

Use only for development.

---

## Test 10 — Real standalone generation

```bash
python3 scripts/run_madgraph.py \
    --build-dir build
```

Verify:

```bash
test -d build/generated/*_standalone/SubProcesses
test -d build/generated/*_standalone/src
```

Then verify at least one process exists:

```bash
find build/generated/*_standalone/SubProcesses \
    -mindepth 1 -maxdepth 1 -type d \
    -name 'P*' | head
```

---

## Test 11 — Generated metadata

Verify:

```bash
test -s build/generated/*_standalone/generation_manifest.json
test -s build/generated/*_standalone/generation_commands.mg5
test -s build/generated/*_standalone/mg5_generation.log
test -s build/generated/*_standalone/odd_particles_resolved.txt
```

---

## Test 12 — Current-output pointer

Verify:

```bash
cat build/generated/current_mg5_output.txt
```

The path must point to the standalone just generated.

---

## Test 13 — UI compatibility

Use the generated paths:

```bash
python3 UI/select_effective_subprocesses_v3_ui.py \
    /path/to/param_card.dat \
    --build-dir build \
    --mg5-output "$(cat build/generated/current_mg5_output.txt)" \
    --subprocesses "$(cat build/generated/current_mg5_output.txt)/SubProcesses" \
    --mode pdg \
    --pdgs 1012 \
    --task sigmav \
    --dry-run
```

The UI should successfully scan the generated `SubProcesses/`.

---

# 21. Minimum acceptance checklist

A new model is ready for the next pipeline stage when:

- [ ] `run_madgraph.py` compiles with Python.
- [ ] MadGraph is correctly resolved.
- [ ] MadGraph version passes the project policy.
- [ ] Exactly one intended UFO is selected.
- [ ] Odd particles resolve correctly.
- [ ] Required antiparticles are added correctly.
- [ ] Dry-run MadGraph commands look physically sensible.
- [ ] Real MadGraph generation exits successfully.
- [ ] `SubProcesses/` exists.
- [ ] `src/` exists.
- [ ] At least one `P*` directory exists.
- [ ] `generation_manifest.json` exists.
- [ ] `generation_commands.mg5` exists.
- [ ] `mg5_generation.log` exists.
- [ ] `current_mg5_output.txt` points to the generated standalone.
- [ ] The UI can scan the generated `SubProcesses/`.
- [ ] The original MadGraph installation has not been modified.
- [ ] The original UFO has not been modified.

---

# 22. Troubleshooting

## `MadGraph path could not be resolved`

Either:

- CMake did not store the MadGraph path under a recognized variable,
- the environment variable is missing,
- or the path no longer contains `bin/mg5_aMC`.

Fix:

```bash
--mg5-root /absolute/path/to/MG5_aMC
```

---

## `Pipeline input directory does not exist`

Create:

```bash
mkdir -p build/input
```

and place the UFO and odd file there.

---

## `No UFO model was found`

Verify the UFO contains the required standard files.

Or pass:

```bash
--ufo /absolute/path/to/model_UFO
```

---

## `More than one UFO model was found`

The script refuses to guess.

Use:

```bash
--ufo build/input/ChosenModel_UFO
```

---

## `No odd particles were provided`

Provide one of:

```text
build/input/odd_particles.txt
```

or:

```bash
--odd-file /path/to/file
```

or:

```bash
--odd 1012 1014 ...
```

---

## `Odd particle ... was not found in the UFO`

The name or PDG does not match a particle declared in `particles.py`.

Check the UFO particle definitions.

---

## `Unsupported MadGraph version`

Use a project-supported MadGraph version.

Do not bypass the check in production unless that version has been validated.

---

## `Output already exists`

Choose another output or intentionally regenerate:

```bash
--force
```

---

## MadGraph exits non-zero

Inspect:

```text
<standalone-parent>/.<standalone-name>.mg5.log
```

If MadGraph completed successfully, the log is copied into:

```text
<standalone>/mg5_generation.log
```

---

# 23. Safety properties

The intended behavior is:

```text
MadGraph installation  -> read/execute only
UFO source             -> read only
odd-particle file      -> read only
build/input            -> read only
build/generated        -> generated runtime data
```

Only the selected generated standalone can be recursively replaced when:

```bash
--force
```

is explicitly supplied.

---

## Author

**Juan Diego Inga**

Dark Matter Cosmology Project
