#!/usr/bin/env python3

import argparse
import ast
import math
import os
import shutil
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

PARAM_CARD_DIR_NAMES = (
    "cards",
    "Cards",
    "param_cards",
    "ParamCards",
    "paramcards",
)

STABILITY_WIDTH_TOLERANCE = 1.0e-30
MASS_DEGENERACY_RTOL = 1.0e-12
MASS_DEGENERACY_ATOL = 1.0e-12
CHARGE_TOLERANCE = 1.0e-12


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


def is_parameter_constructor(call):
    return is_constructor(call, "Parameter")


def parse_numeric_text(value):
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).strip().replace("D", "E").replace("d", "e")

    try:
        return float(text)
    except ValueError:
        return None


def evaluate_parameter_value(node):
    if node is None:
        return None

    try:
        return float(evaluate_number(node))
    except (TypeError, ValueError, ZeroDivisionError, OverflowError):
        pass

    if isinstance(node, ast.Constant):
        return parse_numeric_text(node.value)

    return None


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
# Read particles.py and parameters.py
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
        width = get_reference_keyword(node, "width")

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
            "width": width,
            "dof": dof,
        })

    if not particles:
        raise RuntimeError(
            f"No physical Particle(...) definitions were found in:\n"
            f"{particles_file}"
        )

    return particles


def read_ufo_parameter_values(parameters_file):
    """
    Read numerical default values from UFO parameters.py.

    Only values that can be evaluated safely as simple numbers are retained.
    This is enough for normal external mass/width parameters and ZERO.
    """
    if not parameters_file.is_file():
        raise RuntimeError(
            "UFO parameters.py was not found:\n"
            f"  {parameters_file}"
        )

    try:
        source = parameters_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source = parameters_file.read_text(encoding="latin-1")

    try:
        tree = ast.parse(source, filename=str(parameters_file))
    except SyntaxError as exc:
        raise RuntimeError(
            f"Could not parse UFO parameters file:\n"
            f"{parameters_file}\n\n"
            f"{exc}"
        ) from exc

    values = {}

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if not is_parameter_constructor(node):
            continue

        name = get_string_keyword(node, "name")

        if name is None:
            continue

        value_node = get_keyword_node(node, "value")
        value = evaluate_parameter_value(value_node)

        if value is not None and math.isfinite(value):
            values[name] = float(value)

    values.setdefault("ZERO", 0.0)

    return values


# ============================================================
# Particle / antiparticle species
# ============================================================

def build_particle_species(particles):
    """
    Combine particle-antiparticle pairs into one physical species.
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
            "width": particle["width"],
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
# Parameter-card discovery and parsing
# ============================================================

def is_within(path, root):
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def find_variant_param_cards(variant_dir):
    """
    Find parameter cards ONLY inside the active variant.

    This deliberately never scans sibling variants, preventing a card from
    model A from being combined with the UFO of model B.
    """
    cards = []
    seen = set()

    for directory_name in PARAM_CARD_DIR_NAMES:
        directory = variant_dir / directory_name

        if not directory.is_dir():
            continue

        for card in sorted(directory.glob("*.dat")):
            if not card.is_file():
                continue

            resolved = card.resolve()
            if resolved not in seen:
                seen.add(resolved)
                cards.append(resolved)

    # Also accept conventional param_card*.dat files placed directly in the
    # variant directory.
    for card in sorted(variant_dir.glob("param_card*.dat")):
        if not card.is_file():
            continue

        resolved = card.resolve()
        if resolved not in seen:
            seen.add(resolved)
            cards.append(resolved)

    return cards


def choose_variant_param_card(variant_dir):
    cards = find_variant_param_cards(variant_dir)

    if not cards:
        print()
        print("No parameter card was found for this variant.")
        print("DM-candidate masses and widths will use UFO default values.")
        return None

    if len(cards) == 1:
        print()
        print("Parameter card found for this variant:")
        print(f"  {cards[0]}")
        print("It will be used to determine masses and decay widths.")
        return cards[0]

    print()
    print("Several parameter cards were found inside the active variant:")
    print()

    for index, card in enumerate(cards, start=1):
        print(f"  {index}. {card.relative_to(variant_dir)}")

    print()

    while True:
        answer = input(
            "Select the parameter card to use for DM-candidate determination: "
        ).strip()

        try:
            index = int(answer)
        except ValueError:
            index = 0

        if 1 <= index <= len(cards):
            selected = cards[index - 1]

            if not is_within(selected, variant_dir):
                raise RuntimeError(
                    "Internal error: the selected parameter card is outside "
                    "the active variant."
                )

            return selected

        print("Please enter one of the listed numbers.")


def parse_slha_number(text):
    try:
        return float(text.replace("D", "E").replace("d", "e"))
    except ValueError:
        return None


def read_param_card_mass_widths(param_card):
    masses = {}
    widths = {}
    current_block = None

    try:
        lines = param_card.read_text(
            encoding="utf-8",
            errors="replace",
        ).splitlines()
    except OSError as exc:
        raise RuntimeError(
            f"Could not read parameter card:\n  {param_card}\n\n{exc}"
        ) from exc

    for raw_line in lines:
        body = raw_line.split("#", 1)[0].strip()

        if not body:
            continue

        fields = body.split()
        keyword = fields[0].lower()

        if keyword == "block" and len(fields) >= 2:
            current_block = fields[1].lower()
            continue

        if keyword == "decay" and len(fields) >= 3:
            try:
                pdg = abs(int(fields[1]))
            except ValueError:
                current_block = None
                continue

            width = parse_slha_number(fields[2])

            if width is not None:
                widths[pdg] = width

            current_block = None
            continue

        if current_block != "mass":
            continue

        if len(fields) < 2:
            continue

        try:
            pdg = abs(int(fields[0]))
        except ValueError:
            continue

        mass = parse_slha_number(fields[1])

        if mass is not None:
            masses[pdg] = mass

    return masses, widths


# ============================================================
# Numerical mass/width resolution
# ============================================================

def resolve_ufo_reference(reference, parameter_values):
    if reference is None:
        return None

    text = str(reference).strip()

    if text.upper() == "ZERO":
        return 0.0

    direct = parse_numeric_text(text)

    if direct is not None:
        return direct

    value = parameter_values.get(text)

    if value is None:
        return None

    return float(value)


def resolve_selected_properties(
    selected,
    parameter_values,
    param_card,
    card_masses,
    card_widths,
):
    resolved = []

    for particle in selected:
        item = dict(particle)

        pdg = item.get("pdg")

        if pdg is None:
            raise RuntimeError(
                "Cannot determine the DM candidate because the selected particle "
                f"{particle_display_name(item)} has no PDG code."
            )

        pdg_key = abs(int(pdg))

        if param_card is not None:
            if pdg_key not in card_masses:
                raise RuntimeError(
                    "The selected parameter card does not contain a MASS entry for:\n"
                    f"  {particle_display_name(item)} (PDG {int(pdg)})\n\n"
                    f"Parameter card:\n  {param_card}\n\n"
                    "The card may not correspond to the active UFO/variant."
                )

            mass_value = float(card_masses[pdg_key])
            mass_source = str(param_card)
        else:
            mass_value = resolve_ufo_reference(
                item.get("mass"),
                parameter_values,
            )
            mass_source = "UFO parameters.py"

        if mass_value is None or not math.isfinite(mass_value):
            raise RuntimeError(
                "Could not determine a numerical mass for:\n"
                f"  {particle_display_name(item)}\n"
                f"Mass reference: {item.get('mass')}"
            )

        if param_card is not None and pdg_key in card_widths:
            width_value = float(card_widths[pdg_key])
            width_source = str(param_card)
        else:
            width_value = resolve_ufo_reference(
                item.get("width"),
                parameter_values,
            )
            width_source = "UFO parameters.py"

        if width_value is not None and not math.isfinite(width_value):
            width_value = None

        item["resolved_mass"] = mass_value
        item["resolved_width"] = width_value
        item["mass_source"] = mass_source
        item["width_source"] = width_source

        resolved.append(item)

    return resolved


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

    if math.isclose(value, round(value), abs_tol=CHARGE_TOLERANCE):
        return str(int(round(value)))

    three_q = 3.0 * value

    if math.isclose(three_q, round(three_q), abs_tol=CHARGE_TOLERANCE):
        return f"{int(round(three_q))}/3"

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


def print_detected_odd_sector(selected):
    print()
    print("=" * 70)
    print("Z2-odd particles automatically detected from UFO '~' markers")
    print("=" * 70)
    print()

    for particle in selected:
        print(
            f"  - {particle_display_name(particle):<24} "
            f"PDG={format_number(particle['pdg']):<8} "
            f"mass={particle['mass'] or '-':<12} "
            f"dof={particle['dof']}"
        )

    print()


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
# DM-candidate determination
# ============================================================

def candidate_validation_reasons(particle):
    reasons = []

    mass = particle.get("resolved_mass")
    charge = particle.get("charge")
    width = particle.get("resolved_width")

    if mass is None or not math.isfinite(mass) or mass <= 0.0:
        reasons.append("its mass is not positive and finite")

    if charge is None:
        reasons.append("its electric charge could not be determined from the UFO")
    elif abs(float(charge)) > CHARGE_TOLERANCE:
        reasons.append(
            f"it is electrically charged (Q={format_charge(charge)})"
        )

    if width is None:
        reasons.append(
            "its decay width could not be determined, so stability cannot be verified"
        )
    elif abs(float(width)) > STABILITY_WIDTH_TOLERANCE:
        reasons.append(
            f"it has a non-zero decay width (Gamma={width:.8e} GeV)"
        )

    return reasons


def group_by_mass(sorted_particles):
    groups = []

    for particle in sorted_particles:
        mass = particle["resolved_mass"]

        if not groups:
            groups.append([particle])
            continue

        reference_mass = groups[-1][0]["resolved_mass"]

        if math.isclose(
            mass,
            reference_mass,
            rel_tol=MASS_DEGENERACY_RTOL,
            abs_tol=MASS_DEGENERACY_ATOL,
        ):
            groups[-1].append(particle)
        else:
            groups.append([particle])

    return groups


def choose_degenerate_candidate(valid_particles):
    print()
    print("Several neutral and stable Z2-odd particles share the lowest mass:")
    print()

    for index, particle in enumerate(valid_particles, start=1):
        print(
            f"  {index}. {particle_display_name(particle):<24} "
            f"PDG={format_number(particle['pdg']):<8} "
            f"mass={particle['resolved_mass']:.8e} GeV"
        )

    print()

    while True:
        answer = input("Select the dark-matter candidate: ").strip()

        try:
            index = int(answer)
        except ValueError:
            index = 0

        if 1 <= index <= len(valid_particles):
            return valid_particles[index - 1]

        print("Please enter one of the listed numbers.")


def ask_invalid_candidate_action(has_next):
    print()
    print("Choose an action:")

    if has_next:
        print("  1. Test the next-lightest odd particle")

    print("  2. Redefine the odd sector manually")
    print("  3. Cancel")
    print()

    valid_choices = {"2", "3"}
    if has_next:
        valid_choices.add("1")

    while True:
        answer = input("> ").strip()

        if answer in valid_choices:
            return answer

        print("Please select one of the available options.")


def choose_dm_candidate(resolved_selected):
    sorted_particles = sorted(
        resolved_selected,
        key=lambda particle: particle["resolved_mass"],
    )

    mass_groups = group_by_mass(sorted_particles)

    for group_index, group in enumerate(mass_groups):
        valid_particles = [
            particle
            for particle in group
            if not candidate_validation_reasons(particle)
        ]

        invalid_particles = [
            particle
            for particle in group
            if candidate_validation_reasons(particle)
        ]

        if valid_particles:
            if invalid_particles:
                print()
                print(
                    "Some particles at the lowest currently tested mass cannot "
                    "be DM candidates:"
                )
                for particle in invalid_particles:
                    reasons = "; ".join(candidate_validation_reasons(particle))
                    print(
                        f"  - {particle_display_name(particle)}: {reasons}."
                    )

            if len(valid_particles) == 1:
                candidate = valid_particles[0]
            else:
                candidate = choose_degenerate_candidate(valid_particles)

            print()
            print("Dark-matter candidate identified:")
            print(f"  Particle : {particle_display_name(candidate)}")
            print(f"  PDG      : {format_number(candidate['pdg'])}")
            print(f"  Mass     : {candidate['resolved_mass']:.8e} GeV")
            print(f"  Charge   : {format_charge(candidate['charge'])}")
            print(f"  Width    : {candidate['resolved_width']:.8e} GeV")
            print(f"  Mass src : {candidate['mass_source']}")
            print(f"  Width src: {candidate['width_source']}")

            return candidate

        print()
        print("=" * 70)
        print("The lightest currently tested Z2-odd state(s) cannot be DM")
        print("=" * 70)
        print()

        for particle in group:
            reasons = candidate_validation_reasons(particle)
            print(
                f"  {particle_display_name(particle)} "
                f"(PDG {format_number(particle['pdg'])}, "
                f"mass={particle['resolved_mass']:.8e} GeV)"
            )
            for reason in reasons:
                print(f"    - {reason}")

        has_next = group_index + 1 < len(mass_groups)
        action = ask_invalid_candidate_action(has_next)

        if action == "1":
            continue

        if action == "2":
            return None

        raise KeyboardInterrupt

    return None


def print_final_configuration(selected, candidate, param_card):
    print()
    print("=" * 78)
    print("Final dark-sector configuration")
    print("=" * 78)
    print()
    print("Dark-matter candidate:")
    print(f"  Particle : {particle_display_name(candidate)}")
    print(f"  PDG      : {format_number(candidate['pdg'])}")
    print(f"  Mass     : {candidate['resolved_mass']:.8e} GeV")
    print(f"  Charge   : {format_charge(candidate['charge'])}")
    print(f"  Width    : {candidate['resolved_width']:.8e} GeV")
    print()

    if param_card is not None:
        print("Mass/width configuration:")
        print(f"  Parameter card: {param_card}")
    else:
        print("Mass/width configuration:")
        print("  UFO default values from parameters.py")

    print()
    print("Z2-odd sector:")
    print()

    for particle in selected:
        marker = "  <DM>" if (
            particle["name"] == candidate["name"]
            and int(particle["pdg"]) == int(candidate["pdg"])
        ) else ""

        print(
            f"  - {particle_display_name(particle):<24} "
            f"PDG={format_number(particle['pdg']):<8} "
            f"mass={particle['resolved_mass']:.8e} GeV"
            f"{marker}"
        )

    print()


def confirm_final_configuration(selected, candidate, param_card):
    print_final_configuration(selected, candidate, param_card)

    return yes_no(
        "Write this configuration to odd_particles.txt?",
        default=True,
    )


# ============================================================
# odd_particles.txt
# ============================================================

def confirm_overwrite(path):
    if not path.exists():
        return True

    print()
    print("The following file already exists:")
    print(f"  {path}")
    print()

    return yes_no("Overwrite it?", default=False)


def write_odd_particles(output_file, selected, dm_candidate):
    """
    Output format:

        # DM candidate: N1    PDG: 1012
        # particle    antiparticle    mass    dof
          N1          N1              MN1     2
          etp         etpc            Metp    2

    The metadata line is a comment so existing consumers that ignore '#'
    comments remain compatible with the file.
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

    lines = [
        (
            f"# DM candidate: {dm_candidate['name']}    "
            f"PDG: {int(dm_candidate['pdg'])}"
        )
    ]

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
# Batch parameter-card processing
# ============================================================

def choose_dm_candidate_batch(resolved_selected):
    """
    Determine the DM candidate non-interactively for one parameter point.

    Particles are tested in ascending mass order. Charged, unstable, or
    otherwise unverifiable states are skipped. The first mass level that
    contains at least one neutral, stable state supplies the candidate.

    If several valid particles are mass-degenerate, choose deterministically
    by |PDG| and then name. The ambiguity is recorded for the final summary.
    """
    sorted_particles = sorted(
        resolved_selected,
        key=lambda particle: (
            particle["resolved_mass"],
            abs(int(particle["pdg"])),
            str(particle["name"]),
        ),
    )

    rejected = []

    for group in group_by_mass(sorted_particles):
        valid = []
        invalid = []

        for particle in group:
            reasons = candidate_validation_reasons(particle)

            if reasons:
                invalid.append({
                    "particle": particle,
                    "reasons": reasons,
                })
            else:
                valid.append(particle)

        rejected.extend(invalid)

        if not valid:
            continue

        valid = sorted(
            valid,
            key=lambda particle: (
                abs(int(particle["pdg"])),
                str(particle["name"]),
            ),
        )

        candidate = valid[0]

        return candidate, {
            "rejected_before_or_at_candidate": rejected,
            "degenerate_valid_candidates": valid,
            "used_degenerate_tiebreak": len(valid) > 1,
        }

    return None, {
        "rejected_before_or_at_candidate": rejected,
        "degenerate_valid_candidates": [],
        "used_degenerate_tiebreak": False,
    }


def safe_filename_component(value):
    value = str(value)
    cleaned = "".join(
        character
        if character.isalnum() or character in ("-", "_", ".")
        else "_"
        for character in value
    )

    cleaned = cleaned.strip("._")
    return cleaned or "card"


def odd_output_name_for_card(param_card, variant_dir, used_names):
    """
    Build a deterministic filename without writing the param-card identity
    inside odd_particles itself.

    Example:
        cards/param_card_001.dat
          -> odd_particles_param_card_001.txt
    """
    relative = param_card.resolve().relative_to(variant_dir.resolve())
    relative_without_suffix = relative.with_suffix("")
    parts = list(relative_without_suffix.parts)

    if parts and parts[0] in PARAM_CARD_DIR_NAMES:
        parts = parts[1:]

    if not parts:
        parts = [param_card.stem]

    token = "__".join(
        safe_filename_component(part)
        for part in parts
    )

    base_name = f"odd_particles_{token}.txt"
    name = base_name
    counter = 2

    while name in used_names:
        name = f"odd_particles_{token}__{counter}.txt"
        counter += 1

    used_names.add(name)
    return name


def prepare_batch_output_directory(output_dir, legacy_file):
    existing_items = []

    if output_dir.exists():
        existing_items.append(output_dir)

    if legacy_file.exists():
        existing_items.append(legacy_file)

    if existing_items:
        print()
        print("Existing odd-sector output from a previous run was found:")
        for item in existing_items:
            print(f"  - {item}")
        print()
        print(
            "The new multi-card layout requires regenerating these outputs "
            "to avoid mixing old and new DM-candidate information."
        )

        if not yes_no("Replace the existing odd-sector output?", default=False):
            return False

    if output_dir.exists():
        shutil.rmtree(output_dir)

    if legacy_file.exists():
        legacy_file.unlink()

    output_dir.mkdir(parents=True, exist_ok=True)
    return True


def print_batch_plan(param_cards, output_dir):
    print()
    print("=" * 78)
    print("DM-candidate determination plan")
    print("=" * 78)

    if param_cards:
        print(f"Parameter cards : {len(param_cards)}")
        print("Mode            : batch (all cards in the active variant)")
    else:
        print("Parameter cards : 0")
        print("Mode            : UFO default parameters.py")

    print(f"Output directory: {output_dir}")
    print()
    print(
        "The confirmed odd sector will be reused for every parameter point. "
        "For each card, UI1 will choose the lightest neutral and stable odd "
        "state as the DM candidate."
    )
    print()


def process_parameter_cards_batch(
    selected,
    parameter_values,
    param_cards,
    variant_dir,
    output_dir,
):
    """
    Generate one odd-particle file per parameter card.

    No param-card metadata is written inside the files. Each file contains only
    the DM-candidate comment plus the usual odd-sector table.
    """
    jobs = list(param_cards) if param_cards else [None]
    used_names = set()
    generated = []
    failed = []
    candidate_counts = {}
    skipped_invalid_count = 0
    degenerate_tiebreak_count = 0

    total = len(jobs)

    for index, param_card in enumerate(jobs, start=1):
        label = (
            "UFO defaults"
            if param_card is None
            else str(param_card.relative_to(variant_dir))
        )

        if total > 1:
            print(
                f"\rProcessing parameter cards: {index}/{total}",
                end="",
                flush=True,
            )

        try:
            card_masses = {}
            card_widths = {}

            if param_card is not None:
                card_masses, card_widths = read_param_card_mass_widths(
                    param_card
                )

            resolved_selected = resolve_selected_properties(
                selected=selected,
                parameter_values=parameter_values,
                param_card=param_card,
                card_masses=card_masses,
                card_widths=card_widths,
            )

            dm_candidate, candidate_info = choose_dm_candidate_batch(
                resolved_selected
            )

            if dm_candidate is None:
                reasons = []

                for rejected in candidate_info[
                    "rejected_before_or_at_candidate"
                ]:
                    particle = rejected["particle"]
                    reason_text = "; ".join(rejected["reasons"])
                    reasons.append(
                        f"{particle_display_name(particle)}: {reason_text}"
                    )

                failed.append({
                    "label": label,
                    "reason": (
                        "No neutral and stable odd particle could be identified. "
                        + " | ".join(reasons)
                    ),
                })
                continue

            rejected = candidate_info[
                "rejected_before_or_at_candidate"
            ]

            if rejected:
                skipped_invalid_count += 1

            if candidate_info["used_degenerate_tiebreak"]:
                degenerate_tiebreak_count += 1

            if param_card is None:
                output_name = "odd_particles_default.txt"
                used_names.add(output_name)
            else:
                output_name = odd_output_name_for_card(
                    param_card,
                    variant_dir,
                    used_names,
                )

            output_file = output_dir / output_name

            write_odd_particles(
                output_file,
                resolved_selected,
                dm_candidate,
            )

            pdg = int(dm_candidate["pdg"])
            candidate_key = (
                dm_candidate["name"],
                pdg,
            )
            candidate_counts[candidate_key] = (
                candidate_counts.get(candidate_key, 0) + 1
            )

            generated.append({
                "param_card": param_card,
                "label": label,
                "output_file": output_file,
                "candidate": dm_candidate,
                "candidate_info": candidate_info,
            })

        except (RuntimeError, OSError, ValueError) as exc:
            failed.append({
                "label": label,
                "reason": str(exc),
            })

    if total > 1:
        print()

    return {
        "generated": generated,
        "failed": failed,
        "candidate_counts": candidate_counts,
        "skipped_invalid_count": skipped_invalid_count,
        "degenerate_tiebreak_count": degenerate_tiebreak_count,
        "total": total,
    }


def print_batch_summary(summary, output_dir):
    generated = summary["generated"]
    failed = summary["failed"]

    print()
    print("=" * 78)
    print("UI1 batch summary")
    print("=" * 78)
    print(f"Parameter points processed : {summary['total']}")
    print(f"odd_particles files written: {len(generated)}")
    print(f"Failed parameter points     : {len(failed)}")
    print(
        "Points where lighter/equal invalid odd states were skipped: "
        f"{summary['skipped_invalid_count']}"
    )
    print(
        "Degenerate valid-candidate tie-breaks                   : "
        f"{summary['degenerate_tiebreak_count']}"
    )
    print(f"Output directory            : {output_dir}")

    if summary["candidate_counts"]:
        print()
        print("DM candidates:")

        for (name, pdg), count in sorted(
            summary["candidate_counts"].items(),
            key=lambda item: (-item[1], abs(item[0][1]), item[0][0]),
        ):
            print(
                f"  {name:<20} PDG={pdg:<8} : {count} point(s)"
            )

    if failed:
        print()
        print("Failed parameter points (showing at most 20):")

        for item in failed[:20]:
            compact_reason = " ".join(item["reason"].split())
            if len(compact_reason) > 180:
                compact_reason = compact_reason[:177] + "..."

            print(f"  - {item['label']}: {compact_reason}")

        if len(failed) > 20:
            print(f"  ... and {len(failed) - 20} more failure(s).")

    print("=" * 78)
    print()

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
            "Configure the Z2-odd BSM sector and determine the dark-matter "
            "candidate for every parameter card of an ExtraDM UFO variant."
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
    parameters_file = ufo_dir / "parameters.py"

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

    parameter_values = read_ufo_parameter_values(parameters_file)
    param_cards = find_variant_param_cards(variant_dir)

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
    print(f"Parameter cards : {len(param_cards)}")

    if not param_cards:
        print("Mass/width source: UFO default values from parameters.py")
    else:
        print(
            "Mass/width source: every parameter card inside the active variant"
        )

    print()
    print("Press Ctrl+C at any time to exit.")

    automatically_detected = [
        particle
        for particle in bsm_species
        if has_odd_marker(particle)
    ]

    selected = None

    if automatically_detected:
        try:
            validate_selected_dof(automatically_detected)
        except ValueError as exc:
            print()
            print("Automatic '~' detection cannot be used:")
            print(exc)
            print()
        else:
            print_detected_odd_sector(automatically_detected)

            if yes_no(
                "Use these automatically detected particles as the odd sector?",
                default=True,
            ):
                selected = list(automatically_detected)

    if selected is None:
        if not automatically_detected:
            print()
            print(
                "No '~' Z2-odd markers were found in BSM particle names "
                "from particles.py."
            )

        print()
        print("The odd sector will be selected manually.")

        selected = manual_selection_loop(
            bsm_species,
            all_species,
        )

    # The automatic path was already confirmed by the yes/no question above.
    # The manual path is confirmed inside manual_selection_loop().
    validate_selected_dof(selected)

    output_dir = variant_dir / "odd_particles"
    legacy_file = variant_dir / "odd_particles.txt"

    print_batch_plan(
        param_cards,
        output_dir,
    )

    if not yes_no(
        "Generate the odd-particle configuration files for all parameter points?",
        default=True,
    ):
        print()
        print("No files were written.")
        return

    if not prepare_batch_output_directory(
        output_dir,
        legacy_file,
    ):
        print()
        print("No files were written.")
        return

    summary = process_parameter_cards_batch(
        selected=selected,
        parameter_values=parameter_values,
        param_cards=param_cards,
        variant_dir=variant_dir,
        output_dir=output_dir,
    )

    print_batch_summary(
        summary,
        output_dir,
    )

    generated = summary["generated"]

    if not generated:
        raise RuntimeError(
            "No odd_particles file could be generated because no valid "
            "neutral and stable DM candidate was found for any parameter point."
        )

    # Keep one legacy/root-level odd_particles.txt for consumers such as
    # run_madgraph.py, which still expect:
    #
    #     <variant>/odd_particles.txt
    #
    # All per-param-card files share the same odd-sector table, so the first
    # successfully generated configuration is sufficient for MadGraph.
    representative_file = generated[0]["output_file"]

    shutil.copy2(
        representative_file,
        legacy_file,
    )

    print()
    print("Representative odd-particle file for MadGraph:")
    print(f"  {legacy_file}")
    print(f"  copied from: {representative_file}")

    # modify_template.sh only needs the odd-sector table. Use the same
    # root-level compatibility copy consumed by run_madgraph.py.
    run_modify_template(
        input_dir,
        legacy_file,
    )

    print()
    print("=" * 70)
    print("Configuration generated successfully")
    print("=" * 70)
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
    print("Generated odd-particle configurations:")
    print(f"  {output_dir}")
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

