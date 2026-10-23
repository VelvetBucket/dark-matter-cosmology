#!/usr/bin/env python3

import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

# Physical Standard-Model PDGs that must never be part of the
# Z2-odd BSM sector selected by UI1.
SM_ABS_PDGS = {
    1, 2, 3, 4, 5, 6,        # quarks
    11, 12, 13, 14, 15, 16,  # charged leptons and neutrinos
    21, 22, 23, 24, 25,      # g, gamma, Z, W, h
}


# ============================================================
# UFO parsing helpers
# ============================================================

def get_keyword_node(call, keyword_name):
    """Return the AST node corresponding to a keyword argument."""
    for keyword in call.keywords:
        if keyword.arg == keyword_name:
            return keyword.value

    return None


def get_string_keyword(call, keyword_name):
    node = get_keyword_node(call, keyword_name)

    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value

    return None


def evaluate_number(node):
    """
    Safely evaluate simple numerical AST expressions.

    Supports, for example:
        1
        -1
        2/3
        -2/3
        1.0e3
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.UnaryOp):
        value = evaluate_number(node.operand)

        if isinstance(node.op, ast.USub):
            return -value

        if isinstance(node.op, ast.UAdd):
            return value

    if isinstance(node, ast.BinOp):
        left = evaluate_number(node.left)
        right = evaluate_number(node.right)

        if isinstance(node.op, ast.Div):
            return left / right

        if isinstance(node.op, ast.Mult):
            return left * right

        if isinstance(node.op, ast.Add):
            return left + right

        if isinstance(node.op, ast.Sub):
            return left - right

        if isinstance(node.op, ast.Pow):
            return left ** right

    raise ValueError("Not a simple numerical expression")


def get_number_keyword(call, keyword_name):
    node = get_keyword_node(call, keyword_name)

    if node is None:
        return None

    try:
        return evaluate_number(node)
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        return None


def get_reference_keyword(call, keyword_name):
    """
    Extract the name of a referenced UFO object.

    Examples:
        mass = Param.MN1  -> "MN1"
        mass = P.MetR     -> "MetR"
        mass = ZERO       -> "ZERO"
        mass = Param.ZERO -> "ZERO"
    """
    node = get_keyword_node(call, keyword_name)

    if node is None:
        return None

    if isinstance(node, ast.Attribute):
        return node.attr

    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Constant):
        if isinstance(node.value, str):
            return node.value

        if isinstance(node.value, (int, float)):
            if node.value == 0:
                return "ZERO"

            return str(node.value)

    try:
        return ast.unparse(node)
    except Exception:
        return None


def is_constructor(call, constructor_name):
    if isinstance(call.func, ast.Name):
        return call.func.id == constructor_name

    if isinstance(call.func, ast.Attribute):
        return call.func.attr == constructor_name

    return False


def is_particle_constructor(call):
    return is_constructor(call, "Particle")


# ============================================================
# Physical-particle filtering
# ============================================================

def is_ghost_particle(call):
    """
    Ghosts in UFO models usually satisfy at least one of:
        GhostNumber != 0
        spin == -1
    """
    ghost_number = get_number_keyword(call, "GhostNumber")
    spin = get_number_keyword(call, "spin")

    if ghost_number is not None and ghost_number != 0:
        return True

    if spin == -1:
        return True

    return False


def is_goldstone_particle(call):
    value = get_number_keyword(call, "goldstone")

    if value is None:
        value = get_number_keyword(call, "goldstoneboson")

    return bool(value) if value is not None else False


def is_nonpropagating_particle(call):
    node = get_keyword_node(call, "propagating")

    if node is None:
        return False

    if isinstance(node, ast.Constant):
        return node.value is False

    return False


def is_standard_model_species(species):
    pdg = species.get("pdg")

    if pdg is None:
        return False

    try:
        return abs(int(pdg)) in SM_ABS_PDGS
    except (TypeError, ValueError):
        return False


def has_odd_marker(species):
    """Return True if the UFO particle or antiparticle name starts with '~'."""
    return (
        str(species.get("name", "")).startswith("~")
        or str(species.get("antiname", "")).startswith("~")
    )


# ============================================================
# Degrees of freedom
# ============================================================

def is_massless(mass_parameter):
    if mass_parameter is None:
        return False

    value = str(mass_parameter).strip().upper()

    return value in {
        "ZERO",
        "0",
        "0.0",
    }


def calculate_dof(spin, name, antiname, mass_parameter):
    """
    Calculate internal degrees of freedom according to:

    Spin 0:
        real / self-conjugate      -> 1
        particle + antiparticle    -> 2

    Spin 1/2:
        Majorana                   -> 2
        Dirac                      -> 4

    Spin 1, massless:
        real / self-conjugate      -> 2
        particle + antiparticle    -> 4

    Spin 1, massive:
        real / self-conjugate      -> 3
        particle + antiparticle    -> 6

    UFO convention:
        spin = 1  -> physical spin 0
        spin = 2  -> physical spin 1/2
        spin = 3  -> physical spin 1
    """
    self_conjugate = (name == antiname)

    if spin == 1:
        return 1 if self_conjugate else 2

    if spin == 2:
        return 2 if self_conjugate else 4

    if spin == 3:
        massless = is_massless(mass_parameter)

        if massless:
            return 2 if self_conjugate else 4

        return 3 if self_conjugate else 6

    return None


def ufo_spin_to_physical(spin):
    if spin == 1:
        return "0"

    if spin == 2:
        return "1/2"

    if spin == 3:
        return "1"

    if spin is None:
        return "-"

    return f"UFO:{spin}"


# ============================================================
# Read particles.py
# ============================================================

def read_ufo_particles(particles_file):
    try:
        source = particles_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = particles_file.read_text(encoding="latin-1")

    try:
        tree = ast.parse(
            source,
            filename=str(particles_file),
        )
    except SyntaxError as exc:
        raise RuntimeError(
            f"Could not parse UFO file:\n"
            f"{particles_file}\n\n"
            f"{exc}"
        ) from exc

    particles = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not is_particle_constructor(node):
            continue

        if is_ghost_particle(node):
            continue

        if is_goldstone_particle(node):
            continue

        if is_nonpropagating_particle(node):
            continue

        name = get_string_keyword(node, "name")
        antiname = get_string_keyword(node, "antiname")

        if name is None:
            continue

        if antiname is None:
            antiname = name

        spin = get_number_keyword(node, "spin")
        mass = get_reference_keyword(node, "mass")

        dof = calculate_dof(
            spin,
            name,
            antiname,
            mass,
        )

        particles.append({
            "name": name,
            "antiname": antiname,
            "pdg": get_number_keyword(node, "pdg_code"),
            "charge": get_number_keyword(node, "charge"),
            "spin": spin,
            "mass": mass,
            "dof": dof,
        })

    if not particles:
        raise RuntimeError(
            f"No physical Particle(...) definitions were found in:\n"
            f"  {particles_file}"
        )

    return particles


# ============================================================
# Particle / antiparticle species
# ============================================================

def build_particle_species(particles):
    """Combine particle-antiparticle pairs into one physical species."""
    species = []
    seen = set()

    for particle in particles:
        name = particle["name"]
        antiname = particle["antiname"]

        key = frozenset((name, antiname))

        if key in seen:
            continue

        seen.add(key)

        species.append({
            "name": name,
            "antiname": antiname,
            "pdg": particle["pdg"],
            "charge": particle["charge"],
            "spin": particle["spin"],
            "mass": particle["mass"],
            "dof": particle["dof"],
        })

    return species


# ============================================================
# Input directory, variant and UFO detection
# ============================================================

def find_input_directory(explicit_path=None):
    candidates = []

    if explicit_path is not None:
        candidates.append(Path(explicit_path).expanduser())

    env_input = os.environ.get("INPUT_DIR")
    if env_input:
        candidates.append(Path(env_input).expanduser())

    cwd = Path.cwd()
    candidates.extend([
        cwd / "input",
        cwd / "build" / "input",
        Path(__file__).resolve().parent.parent / "build" / "input",
    ])

    for candidate in candidates:
        if candidate.is_dir():
            return candidate.resolve()

    searched = "\n".join(f"  - {path}" for path in candidates)

    raise RuntimeError(
        "Could not find the input directory.\n\n"
        "Searched:\n"
        f"{searched}\n\n"
        "You can specify it manually with:\n"
        "  UI1.py --input-dir /path/to/build/input\n"
        "or by exporting INPUT_DIR."
    )


def find_variant_directory(input_dir, variant_name):
    variant_dir = (input_dir / variant_name).resolve()

    if not variant_dir.is_dir():
        raise RuntimeError(
            f"Variant directory does not exist:\n"
            f"  {variant_dir}\n\n"
            f"Create it and place the UFO model inside it, e.g.:\n"
            f"  mkdir -p {variant_dir}/model_UFO\n"
            f"  cp -r /path/to/your/UFO/* {variant_dir}/model_UFO/"
        )

    return variant_dir


def find_ufo_directory(variant_dir):
    """
    Find exactly one UFO inside the active variant.

    The search never leaves variant_dir, which keeps different model variants
    isolated from one another.
    """
    candidates = []

    if (variant_dir / "particles.py").is_file():
        candidates.append(variant_dir)

    for item in variant_dir.iterdir():
        if not item.is_dir():
            continue

        if (item / "particles.py").is_file():
            candidates.append(item)

    if len(candidates) == 0:
        raise RuntimeError(
            "No UFO model was found inside:\n"
            f"  {variant_dir}\n\n"
            "Expected a UFO directory containing particles.py."
        )

    if len(candidates) > 1:
        models = "\n".join(
            f"  - {directory}"
            for directory in candidates
        )

        raise RuntimeError(
            "More than one UFO model was found inside:\n"
            f"  {variant_dir}\n\n"
            "Exactly one UFO model is expected per variant.\n\n"
            f"Found:\n{models}"
        )

    return candidates[0]


# ============================================================
# Terminal display
# ============================================================

def format_number(value):
    if value is None:
        return "-"

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value)


def format_charge(value):
    if value is None:
        return "-"

    value = float(value)

    if value.is_integer():
        return str(int(value))

    three_q = 3.0 * value

    if three_q.is_integer():
        return f"{int(three_q)}/3"

    return f"{value:g}"


def particle_display_name(species):
    if species["name"] == species["antiname"]:
        return species["name"]

    return (
        f'{species["name"]} / '
        f'{species["antiname"]}'
    )


def print_particle_table(species, title="Available BSM particle species:"):
    print()
    print(title)
    print()

    if not species:
        print("  (none)")
        print()
        return

    name_width = max(
        20,
        max(
            len(particle_display_name(particle))
            for particle in species
        ) + 2,
    )

    header = (
        f"{'Particle':<{name_width}}"
        f"{'PDG':>12}"
        f"{'Charge':>10}"
        f"{'Spin':>10}"
        f"{'Mass':>15}"
        f"{'DOF':>8}"
    )

    print(header)
    print("-" * len(header))

    for particle in species:
        display_name = particle_display_name(particle)
        pdg = format_number(particle["pdg"])
        charge = format_charge(particle["charge"])
        spin = ufo_spin_to_physical(particle["spin"])
        mass = particle["mass"] or "-"
        dof = (
            str(particle["dof"])
            if particle["dof"] is not None
            else "?"
        )

        print(
            f"{display_name:<{name_width}}"
            f"{pdg:>12}"
            f"{charge:>10}"
            f"{spin:>10}"
            f"{mass:>15}"
            f"{dof:>8}"
        )

    print()


def print_proposed_odd_sector(selected, title, source_path=None):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)

    if source_path is not None:
        print()
        print("Source:")
        print(f"  {source_path}")

    print_particle_table(
        selected,
        title="Proposed Z2-odd dark-sector species:",
    )


# ============================================================
# User selection and validation
# ============================================================

def build_particle_lookups(species):
    by_name = {}
    by_pdg = {}

    for particle in species:
        name = particle["name"]
        antiname = particle["antiname"]
        pdg = particle["pdg"]

        by_name[name] = particle
        by_name[antiname] = particle

        if pdg is not None:
            pdg = int(pdg)
            by_pdg[pdg] = particle

            if name != antiname:
                by_pdg[-pdg] = particle

    return by_name, by_pdg


def parse_selection(text, selectable_species, all_species):
    """
    Select BSM physical species using UFO/MadGraph names or PDG codes.

    Standard-Model particles are resolved explicitly so that accidental SM
    input produces a dedicated error rather than a generic 'unknown particle'.
    """
    tokens = text.replace(",", " ").split()

    if not tokens:
        raise ValueError("No particles were selected.")

    all_by_name, all_by_pdg = build_particle_lookups(all_species)
    bsm_by_name, bsm_by_pdg = build_particle_lookups(selectable_species)

    selected = []
    seen = set()

    for token in tokens:
        try:
            pdg_token = int(token)
        except ValueError:
            pdg_token = None

        all_particle = (
            all_by_pdg.get(pdg_token)
            if pdg_token is not None
            else all_by_name.get(token)
        )

        if all_particle is not None and is_standard_model_species(all_particle):
            raise ValueError(
                f"{particle_display_name(all_particle)} "
                f"(PDG {format_number(all_particle['pdg'])}) belongs to the "
                "Standard Model and cannot be included in odd_particles.txt."
            )

        particle = (
            bsm_by_pdg.get(pdg_token)
            if pdg_token is not None
            else bsm_by_name.get(token)
        )

        if particle is None:
            raise ValueError(
                f"Unknown or non-BSM particle: {token}. "
                "Enter a UFO/MadGraph BSM particle name or a PDG code shown "
                "in the table."
            )

        key = (
            particle["name"],
            particle["antiname"],
        )

        if key not in seen:
            seen.add(key)
            selected.append(particle)

    return selected


def validate_selected_dof(selected):
    unsupported = [
        particle
        for particle in selected
        if particle["dof"] is None
    ]

    if not unsupported:
        return

    names = "\n".join(
        f"  - {particle_display_name(particle)} "
        f"(UFO spin = {particle['spin']})"
        for particle in unsupported
    )

    raise ValueError(
        "The DOF could not be calculated for the following "
        "selected particle(s):\n"
        f"{names}\n\n"
        "The current rules support physical spins 0, 1/2 and 1."
    )


def ask_selection(selectable_species, all_species):
    while True:
        print_particle_table(selectable_species)
        print("Select all Z2-odd particles of the dark sector.")
        print()
        print(
            "Enter UFO/MadGraph particle names or PDG codes "
            "separated by spaces or commas."
        )
        print()
        print("Standard-Model particles are not allowed.")
        print()
        print("Examples:")
        print("  N1 N2 N3 etp etI etR")
        print("  1012 1014 1016 1003 1002 1001")
        print("  ~N1, ~N2, 1003")
        print()

        answer = input("> ").strip()

        try:
            selected = parse_selection(
                answer,
                selectable_species,
                all_species,
            )

            validate_selected_dof(selected)
            return selected

        except ValueError as exc:
            print()
            print(f"Error: {exc}")
            print()


def confirm_selection(selected):
    print()
    print("=" * 70)
    print("Selected Z2-odd dark-sector particles")
    print("=" * 70)
    print()

    for particle in selected:
        name = particle_display_name(particle)
        spin = ufo_spin_to_physical(particle["spin"])
        mass = particle["mass"] or "-"
        dof = particle["dof"]

        print(
            f"  - {name}"
            f"    PDG={format_number(particle['pdg'])}"
            f"    mass={mass}"
            f"    spin={spin}"
            f"    dof={dof}"
        )

    print()

    while True:
        answer = input(
            "Is this odd-sector selection correct? [y/n]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


def manual_selection_loop(selectable_species, all_species):
    while True:
        selected = ask_selection(
            selectable_species,
            all_species,
        )

        if confirm_selection(selected):
            return selected

        print()
        print("Selection cancelled.")
        print("Please select the particles again.")


def yes_no(prompt, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "

    while True:
        answer = input(prompt + suffix).strip().lower()

        if not answer:
            return default

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


# ============================================================
# Predefined cards/odd_particles.txt input
# ============================================================

def tokenize_odd_particles_file(odd_file):
    """
    Read particle identifiers from an existing odd_particles.txt.

    Supported formats:

    Structured UI1 format:
        # particle antiparticle mass dof
        N1         N1           MN1  2
        etp        etpc         Metp 2

    Simple format:
        N1 N2 etp

    Comment lines and inline comments are ignored.  If the structured header
    is present, only the first column ('particle') is used; all mass/DOF
    information is reconstructed from the active UFO before writing the new
    root-level odd_particles.txt.
    """
    try:
        raw_lines = odd_file.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
    except OSError as exc:
        raise ValueError(
            f"Could not read predefined odd-particle file:\n"
            f"  {odd_file}\n\n"
            f"{exc}"
        ) from exc

    structured = False

    for raw_line in raw_lines:
        stripped = raw_line.strip()

        if not stripped.startswith("#"):
            continue

        header = stripped[1:].strip().lower().split()
        required = {"particle", "antiparticle", "mass", "dof"}

        if required.issubset(set(header)):
            structured = True
            break

    tokens = []

    for raw_line in raw_lines:
        body = raw_line.split("#", 1)[0].strip()

        if not body:
            continue

        columns = body.replace(",", " ").split()

        if structured:
            tokens.append(columns[0])
        else:
            tokens.extend(columns)

    if not tokens:
        raise ValueError(
            "The predefined odd-particle file contains no particle entries:\n"
            f"  {odd_file}"
        )

    return tokens


def load_predefined_odd_sector(odd_file, bsm_species, all_species):
    tokens = tokenize_odd_particles_file(odd_file)

    selected = parse_selection(
        " ".join(tokens),
        bsm_species,
        all_species,
    )

    validate_selected_dof(selected)
    return selected


# ============================================================
# odd_particles.txt output
# ============================================================

def confirm_overwrite(path):
    if not path.exists():
        return True

    print()
    print("The following file already exists:")
    print(f"  {path}")
    print()

    return yes_no("Overwrite it?", default=False)


def write_odd_particles(output_file, selected):
    """
    Output format:

        # particle    antiparticle    mass    dof
          N1          N1              MN1     2
          etp         etpc            Metp    2

    Each line represents one physical species.  No DM-candidate information
    is written by UI1.
    """
    rows = []

    for particle in selected:
        rows.append((
            particle["name"],
            particle["antiname"],
            particle["mass"] or "-",
            particle["dof"],
        ))

    particle_width = max(
        12,
        len("particle"),
        max(len(str(row[0])) for row in rows) + 2,
    )

    antiparticle_width = max(
        16,
        len("antiparticle"),
        max(len(str(row[1])) for row in rows) + 2,
    )

    mass_width = max(
        10,
        len("mass"),
        max(len(str(row[2])) for row in rows) + 2,
    )

    lines = []

    lines.append(
        f"# "
        f"{'particle':<{particle_width}}"
        f"{'antiparticle':<{antiparticle_width}}"
        f"{'mass':<{mass_width}}"
        f"dof"
    )

    for particle, antiparticle, mass, dof in rows:
        lines.append(
            f"  "
            f"{particle:<{particle_width}}"
            f"{antiparticle:<{antiparticle_width}}"
            f"{mass:<{mass_width}}"
            f"{dof}"
        )

    output_file.write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


# ============================================================
# MadGraph template configuration
# ============================================================

def get_madgraph_directory(build_dir):
    cache_file = build_dir / "CMakeCache.txt"

    if not cache_file.is_file():
        raise RuntimeError(
            "CMakeCache.txt was not found:\n"
            f"  {cache_file}\n\n"
            "Run CMake before running UI1."
        )

    for line in cache_file.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines():
        if line.startswith("MADGRAPH_DIR:"):
            _, value = line.split("=", 1)

            madgraph_dir = Path(
                value.strip()
            ).expanduser().resolve()

            if not madgraph_dir.is_dir():
                raise RuntimeError(
                    "The MadGraph directory stored in CMakeCache.txt "
                    "does not exist:\n"
                    f"  {madgraph_dir}"
                )

            return madgraph_dir

    raise RuntimeError(
        "MADGRAPH_DIR was not found in CMakeCache.txt."
    )


def find_modify_template_script(build_dir):
    repo_dir = build_dir.parent

    candidates = [
        build_dir / "scripts" / "modify_template.sh",
        build_dir / "scripts" / "modify_template" / "modify_template.sh",
        repo_dir / "scripts" / "modify_template.sh",
        repo_dir / "scripts" / "modify_template" / "modify_template.sh",
    ]

    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()

    searched = "\n".join(
        f"  - {candidate}"
        for candidate in candidates
    )

    raise RuntimeError(
        "Could not find modify_template.sh.\n\n"
        f"Searched:\n{searched}"
    )


def run_modify_template(input_dir, odd_particles_file):
    """
    Preserve the current UI1 contract:

        modify_template.sh <template_files_dir> <odd_particles.txt>
    """
    build_dir = input_dir.parent.resolve()

    madgraph_dir = get_madgraph_directory(build_dir)
    modify_script = find_modify_template_script(build_dir)

    template_dir = (
        madgraph_dir
        / "madgraph"
        / "iolibs"
        / "template_files"
    )

    if not template_dir.is_dir():
        raise RuntimeError(
            "MadGraph template_files directory was not found:\n"
            f"  {template_dir}"
        )

    if not odd_particles_file.is_file():
        raise RuntimeError(
            "odd_particles.txt was not found:\n"
            f"  {odd_particles_file}"
        )

    print()
    print("=" * 70)
    print("Configuring MadGraph templates")
    print("=" * 70)
    print()
    print(f"MadGraph         : {madgraph_dir}")
    print(f"template_files   : {template_dir}")
    print(f"odd_particles.txt: {odd_particles_file}")
    print()

    try:
        subprocess.run(
            [
                "bash",
                str(modify_script),
                str(template_dir),
                str(odd_particles_file),
            ],
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "modify_template.sh failed "
            f"with exit code {exc.returncode}."
        ) from exc

    print()
    print("MadGraph templates configured successfully.")


# ============================================================
# Program
# ============================================================

def resolve_variant(cli_variant):
    if cli_variant:
        return cli_variant

    env_variant = os.environ.get("VARIANT")
    if env_variant:
        return env_variant

    raise RuntimeError(
        "No variant was specified.\n\n"
        "Either:\n"
        "  * run through initiate_model.sh:  ./initiate_model.sh var1\n"
        "  * export VARIANT=var1 before running UI1.py\n"
        "  * pass --variant var1 explicitly"
    )


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Configure the Z2-odd BSM sector of an ExtraDM UFO variant. "
            "UI1 does not determine the dark-matter candidate."
        )
    )

    parser.add_argument(
        "--input-dir",
        help=(
            "Path to the ExtraDM input directory. "
            "Normally this is build/input. "
            "If omitted, $INPUT_DIR is used, then auto-detection."
        ),
    )

    parser.add_argument(
        "-v", "--variant",
        default=None,
        help=(
            "Name of the variant subdirectory inside input/. "
            "If omitted, $VARIANT is used (set by initiate_model.sh)."
        ),
    )

    args = parser.parse_args()

    variant_name = resolve_variant(args.variant)
    input_dir = find_input_directory(args.input_dir)
    variant_dir = find_variant_directory(input_dir, variant_name)
    ufo_dir = find_ufo_directory(variant_dir)

    particles_file = ufo_dir / "particles.py"
    cards_odd_file = variant_dir / "cards" / "odd_particles.txt"
    output_file = variant_dir / "odd_particles.txt"

    particles = read_ufo_particles(particles_file)
    all_species = build_particle_species(particles)

    bsm_species = [
        particle
        for particle in all_species
        if not is_standard_model_species(particle)
    ]

    if not bsm_species:
        raise RuntimeError(
            "No physical BSM particle species were found after excluding "
            "Standard-Model particles."
        )

    print()
    print("=" * 70)
    print("                 ExtraDM - Dark Sector Setup")
    print("=" * 70)
    print()
    print(f"Input directory : {input_dir}")
    print(f"Variant         : {variant_name}")
    print(f"Variant path    : {variant_dir}")
    print(f"UFO model       : {ufo_dir.name}")
    print(f"Particles file  : {particles_file}")
    print(f"Physical species: {len(all_species)}")
    print(f"BSM species     : {len(bsm_species)}")
    print()
    print("UI1 only defines the Z2-odd sector.")
    print("The dark-matter candidate will be determined later by UI2.")
    print()
    print("Press Ctrl+C at any time to exit.")

    selected = None

    # --------------------------------------------------------
    # Priority 1: cards/odd_particles.txt
    # --------------------------------------------------------
    print()
    print("=" * 70)
    print("Checking for a predefined odd-particle file")
    print("=" * 70)
    print()
    print("Expected file:")
    print(f"  {cards_odd_file}")

    if cards_odd_file.is_file():
        print()
        print("Found predefined odd-particle file:")
        print(f"  {cards_odd_file}")

        try:
            predefined = load_predefined_odd_sector(
                cards_odd_file,
                bsm_species,
                all_species,
            )
        except ValueError as exc:
            print()
            print("The predefined odd-particle file cannot be used:")
            print(exc)
            print()
            print("The odd sector will be selected manually.")
        else:
            print_proposed_odd_sector(
                predefined,
                title="Z2-odd particles loaded from cards/odd_particles.txt",
                source_path=cards_odd_file,
            )

            if yes_no(
                "Use these particles as the odd sector?",
                default=True,
            ):
                selected = list(predefined)
            else:
                print()
                print("The predefined odd sector was rejected by the user.")
                print("The odd sector will be selected manually.")
    else:
        print()
        print("No predefined odd-particle file was found at:")
        print(f"  {cards_odd_file}")

    # --------------------------------------------------------
    # Priority 2: '~' markers in UFO particles.py
    # Only attempted when cards/odd_particles.txt does NOT exist.
    # If the file existed but was rejected/invalid, go directly manual.
    # --------------------------------------------------------
    if selected is None and not cards_odd_file.is_file():
        print()
        print("=" * 70)
        print("Checking UFO '~' odd-particle markers")
        print("=" * 70)
        print()
        print("Searching in:")
        print(f"  {particles_file}")

        automatically_detected = [
            particle
            for particle in bsm_species
            if has_odd_marker(particle)
        ]

        if automatically_detected:
            try:
                validate_selected_dof(automatically_detected)
            except ValueError as exc:
                print()
                print("Particles marked with '~' were found, but they cannot be used:")
                print(exc)
                print()
                print("The odd sector will be selected manually.")
            else:
                print_proposed_odd_sector(
                    automatically_detected,
                    title="Z2-odd particles detected from UFO '~' markers",
                    source_path=particles_file,
                )

                if yes_no(
                    "Use these particles as the odd sector?",
                    default=True,
                ):
                    selected = list(automatically_detected)
                else:
                    print()
                    print("The UFO '~' odd-sector proposal was rejected by the user.")
                    print("The odd sector will be selected manually.")
        else:
            print()
            print("No particles marked with the '~' prefix were found in:")
            print(f"  {particles_file}")
            print()
            print("The odd sector will be selected manually.")

    # --------------------------------------------------------
    # Priority 3: manual selection
    # --------------------------------------------------------
    if selected is None:
        selected = manual_selection_loop(
            bsm_species,
            all_species,
        )

    validate_selected_dof(selected)

    # --------------------------------------------------------
    # Write one root-level odd_particles.txt, as in the original
    # pre-DM-candidate UI1 design.
    # --------------------------------------------------------
    print()
    print("=" * 70)
    print("Final odd-sector output")
    print("=" * 70)
    print()
    print("Output file:")
    print(f"  {output_file}")

    if not confirm_overwrite(output_file):
        print()
        print("No file was written.")
        return

    write_odd_particles(
        output_file,
        selected,
    )

    # modify_template.sh receives the same single, model-level odd sector.
    # It does not need a DM candidate or a per-param-card odd-particle file.
    run_modify_template(
        input_dir,
        output_file,
    )

    print()
    print("=" * 70)
    print("Configuration generated successfully")
    print("=" * 70)
    print()
    print("odd_particles.txt:")
    print(f"  {output_file}")
    print()
    print("Confirmed Z2-odd dark-sector species:")
    print()

    for particle in selected:
        print(
            f"  {particle_display_name(particle):<24} "
            f"PDG={format_number(particle['pdg']):<8} "
            f"mass={particle['mass'] or '-':<12} "
            f"dof={particle['dof']}"
        )

    print()
    print("DM candidate: not determined by UI1 (handled later by UI2).")
    print()


try:
    main()

except KeyboardInterrupt:
    print()
    print()
    print("Operation cancelled by user.")
    print()
    sys.exit(0)

except RuntimeError as exc:
    print()
    print("ERROR")
    print("=====")
    print(exc)
    print()
    sys.exit(1)

except OSError as exc:
    print()
    print("ERROR")
    print("=====")
    print(exc)
    print()
    sys.exit(1)

