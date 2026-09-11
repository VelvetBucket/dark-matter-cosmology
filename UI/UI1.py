#!/usr/bin/env python3

import argparse
import ast
import os
import sys
from pathlib import Path


# ============================================================
# UFO parsing helpers
# ============================================================

def get_keyword_node(call, keyword_name):
    """
    Return the AST node corresponding to a keyword argument.

    Example:

        Particle(
            name='n1',
            spin=2,
            mass=Param.MN1,
            ...
        )
    """
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

    raise ValueError("Not a simple numerical expression")


def get_number_keyword(call, keyword_name):
    node = get_keyword_node(call, keyword_name)

    if node is None:
        return None

    try:
        return evaluate_number(node)
    except (TypeError, ValueError, ZeroDivisionError):
        return None


def get_reference_keyword(call, keyword_name):
    """
    Extract the name of a referenced UFO object.

    Examples:

        mass = Param.MN1  ->  "MN1"
        mass = P.MetR     ->  "MetR"
        mass = ZERO       ->  "ZERO"
        mass = Param.ZERO ->  "ZERO"
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


def is_particle_constructor(call):
    """
    Detect both:

        Particle(...)

    and:

        object_library.Particle(...)
    """
    if isinstance(call.func, ast.Name):
        return call.func.id == "Particle"

    if isinstance(call.func, ast.Attribute):
        return call.func.attr == "Particle"

    return False


# ============================================================
# Ghost detection
# ============================================================

def is_ghost_particle(call):
    """
    Ghosts in UFO models usually satisfy at least one of:

        GhostNumber != 0
        spin == -1

    They are completely excluded from the UI.
    """
    ghost_number = get_number_keyword(call, "GhostNumber")
    spin = get_number_keyword(call, "spin")

    if ghost_number is not None and ghost_number != 0:
        return True

    if spin == -1:
        return True

    return False


# ============================================================
# Degrees of freedom
# ============================================================

def is_massless(mass_parameter):
    """
    In UFO models a massless particle is normally represented by:

        mass = Param.ZERO

    or an equivalent ZERO reference.
    """
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

    # --------------------------------------------------------
    # Spin 0
    # UFO spin = 1
    # --------------------------------------------------------
    if spin == 1:
        if self_conjugate:
            return 1
        else:
            return 2

    # --------------------------------------------------------
    # Spin 1/2
    # UFO spin = 2
    # --------------------------------------------------------
    if spin == 2:
        if self_conjugate:
            return 2
        else:
            return 4

    # --------------------------------------------------------
    # Spin 1
    # UFO spin = 3
    # --------------------------------------------------------
    if spin == 3:
        massless = is_massless(mass_parameter)

        if massless:
            if self_conjugate:
                return 2
            else:
                return 4

        else:
            if self_conjugate:
                return 3
            else:
                return 6

    # Other spins are not covered by the rules currently used.
    return None


def ufo_spin_to_physical(spin):
    """
    Convert the UFO convention (2S+1) to readable physical spin.
    """
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
            filename=str(particles_file)
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

        # Ignore all ghost particles
        if is_ghost_particle(node):
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
            mass
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
            f"{particles_file}"
        )

    return particles


# ============================================================
# Particle / antiparticle species
# ============================================================

def build_particle_species(particles):
    """
    Combine particle-antiparticle pairs into a single
    user-facing species.

    Example:

        et+ / et-

    instead of presenting et+ and et- separately.

    The DOF represents the COMPLETE species:

        et+ / et-  -> 2

    rather than 2 per particle.
    """
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
# Input directory and UFO detection
# ============================================================

def find_input_directory(explicit_path=None):
    """
    Locate the ExtraDM build input directory.

    Priority:
        1. explicit --input-dir
        2. $INPUT_DIR from the environment
        3. cwd/input
        4. cwd/build/input
        5. <UI1.py>/../../build/input
    """
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
    """
    Return the variant directory inside input_dir.

    Layout expected:

        input/
        ├── var1/
        │   ├── <UFO model>/        # contains particles.py
        │   ├── param_cards/        # ignored by the UFO detection
        │   └── ...
        ├── var2/
        │   └── ...
        └── ...

    Exactly one UFO model (identified by particles.py) is
    expected under input/<variant_name>/ (at any depth up to 2).
    """
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
    Find the single UFO model directory inside variant_dir.

    A UFO model is identified by the presence of particles.py.

    The search is limited to the variant directory itself and
    one level below it, so that auxiliary directories such as
    param_cards/ do not confuse the detection.
    """
    candidates = []

    # The variant directory itself may be the UFO model
    if (variant_dir / "particles.py").is_file():
        candidates.append(variant_dir)

    # Or the UFO model may be a direct subdirectory
    for item in variant_dir.iterdir():
        if not item.is_dir():
            continue

        if (item / "particles.py").is_file():
            candidates.append(item)

    if len(candidates) == 0:
        raise RuntimeError(
            "No UFO model was found inside:\n"
            f"  {variant_dir}\n\n"
            "Expected something like:\n\n"
            f"  {variant_dir.name}/\n"
            "  ├── model_UFO/\n"
            "  │   ├── particles.py\n"
            "  │   ├── parameters.py\n"
            "  │   └── ...\n"
            "  ├── param_cards/\n"
            "  └── ...\n\n"
            "A UFO model is any directory that contains "
            "particles.py."
        )

    if len(candidates) > 1:
        models = "\n".join(
            f"  - {directory}"
            for directory in candidates
        )

        raise RuntimeError(
            "More than one UFO model was found inside:\n"
            f"  {variant_dir}\n\n"
            "Exactly one UFO model is expected.\n\n"
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


def particle_display_name(species):
    if species["name"] == species["antiname"]:
        return species["name"]

    return (
        f'{species["name"]} / '
        f'{species["antiname"]}'
    )


def print_particle_table(species):
    print()
    print("Available physical particle species:")
    print()

    index_width = len(str(len(species)))

    name_width = max(
        20,
        max(
            len(particle_display_name(particle))
            for particle in species
        ) + 2
    )

    header = (
        f"{'#':>{index_width}}   "
        f"{'Particle':<{name_width}}"
        f"{'PDG':>12}"
        f"{'Charge':>10}"
        f"{'Spin':>10}"
        f"{'Mass':>15}"
        f"{'DOF':>8}"
    )

    print(header)
    print("-" * len(header))

    for index, particle in enumerate(species, start=1):

        display_name = particle_display_name(particle)

        pdg = format_number(particle["pdg"])
        charge = format_number(particle["charge"])
        spin = ufo_spin_to_physical(particle["spin"])
        mass = particle["mass"] or "-"
        dof = (
            str(particle["dof"])
            if particle["dof"] is not None
            else "?"
        )

        print(
            f"{index:>{index_width}}   "
            f"{display_name:<{name_width}}"
            f"{pdg:>12}"
            f"{charge:>10}"
            f"{spin:>10}"
            f"{mass:>15}"
            f"{dof:>8}"
        )

    print()


# ============================================================
# User selection
# ============================================================

def parse_selection(text, maximum):
    """
    Accepted formats:

        3 5 7
        3,5,7
        3 5-8
        3, 5-8, 11
    """
    text = text.replace(",", " ")

    selected = []

    for token in text.split():

        if "-" in token:
            pieces = token.split("-")

            if len(pieces) != 2:
                raise ValueError(
                    f"Invalid range: {token}"
                )

            try:
                start = int(pieces[0])
                end = int(pieces[1])

            except ValueError:
                raise ValueError(
                    f"Invalid range: {token}"
                )

            if start > end:
                raise ValueError(
                    f"Invalid range: {token}"
                )

            for number in range(start, end + 1):
                selected.append(number)

        else:
            try:
                selected.append(int(token))

            except ValueError:
                raise ValueError(
                    f"Invalid selection: {token}"
                )

    if not selected:
        raise ValueError(
            "No particles were selected."
        )

    invalid = [
        number
        for number in selected
        if number < 1 or number > maximum
    ]

    if invalid:
        raise ValueError(
            "Particle number out of range: "
            + ", ".join(map(str, invalid))
        )

    # Remove duplicates while preserving order
    return list(dict.fromkeys(selected))


def validate_selected_dof(selected):
    """
    Reject a selected dark-sector particle if its spin is not
    covered by the current DOF rules.
    """
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
        "The current rules support physical spins "
        "0, 1/2 and 1."
    )


def ask_selection(species):
    while True:
        print(
            "Select all Z2-odd particles of the dark sector."
        )
        print()
        print(
            "Enter particle numbers separated by spaces or commas."
        )
        print("Ranges are also accepted.")
        print()
        print("Examples:")
        print("  14 15 16 19")
        print("  14-19")
        print("  14-16, 19")
        print()

        answer = input("> ").strip()

        try:
            indices = parse_selection(
                answer,
                len(species)
            )

            selected = [
                species[index - 1]
                for index in indices
            ]

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
            f"    mass={mass}"
            f"    spin={spin}"
            f"    dof={dof}"
        )

    print()

    while True:
        answer = input(
            "Is this selection correct? [y/n]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


def confirm_overwrite(path):
    if not path.exists():
        return True

    print()
    print("The following file already exists:")
    print(f"  {path}")
    print()

    while True:
        answer = input(
            "Overwrite it? [y/n]: "
        ).strip().lower()

        if answer in ("y", "yes"):
            return True

        if answer in ("n", "no"):
            return False

        print("Please enter y or n.")


# ============================================================
# Write odd_particles.txt
# ============================================================

def write_odd_particles(output_file, selected):
    """
    Output format:

        # particle    antiparticle    mass    dof
        n1            n1              MN1     2
        et+           et-             Metp    2

    Each line represents ONE physical species.

    Therefore particle-antiparticle pairs are NOT duplicated.
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
        max(len(str(row[0])) for row in rows) + 2
    )

    antiparticle_width = max(
        16,
        len("antiparticle"),
        max(len(str(row[1])) for row in rows) + 2
    )

    mass_width = max(
        10,
        len("mass"),
        max(len(str(row[2])) for row in rows) + 2
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
        encoding="utf-8"
    )


# ============================================================
# Program
# ============================================================

def resolve_variant(cli_variant):
    """
    Resolve which variant to use.

    Priority:
        1. --variant on the command line
        2. $VARIANT from the environment
        3. error
    """
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
            "Configure the Z2-odd dark-sector particles "
            "of an ExtraDM UFO model stored in a specific "
            "variant inside input/."
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

    input_dir = find_input_directory(
        args.input_dir
    )

    variant_dir = find_variant_directory(
        input_dir,
        variant_name,
    )

    ufo_dir = find_ufo_directory(
        variant_dir
    )

    particles_file = (
        ufo_dir
        / "particles.py"
    )

    particles = read_ufo_particles(
        particles_file
    )

    species = build_particle_species(
        particles
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
    print(f"Particle species: {len(species)}")

    while True:
        print_particle_table(species)

        print(
            "Press Ctrl+C at any time to exit."
        )
        print()

        selected = ask_selection(species)

        if confirm_selection(selected):
            break

        print()
        print("Selection cancelled.")
        print(
            "Please select the particles again."
        )

    output_file = (
        variant_dir
        / "odd_particles.txt"
    )

    if not confirm_overwrite(output_file):
        print()
        print("No file was written.")
        return

    write_odd_particles(
        output_file,
        selected
    )

    print()
    print("=" * 70)
    print("Configuration generated successfully")
    print("=" * 70)
    print()
    print("File:")
    print(f"  {output_file}")
    print()
    print("Selected dark-sector species:")
    print()

    for particle in selected:
        print(
            f"  {particle_display_name(particle):<20} "
            f"mass={particle['mass'] or '-':<12} "
            f"dof={particle['dof']}"
        )

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
