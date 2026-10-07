#!/usr/bin/env python3
"""
Scotogenic subprocess selector and UI/orchestrator (v3).

Two user-facing selection modes are provided:

1. combined
   Keeps the original automatic effective-dark-sector selection.  The
   freeze-out reference x_f is configurable with --xf and defaults to 25.

2. pdg
   The first supplied PDG is the dark-matter candidate.  Candidate-candidate
   annihilation channels are always selected; each additional PDG requests
   candidate-partner coannihilation channels.  The program validates each
   requested pair against the actual SubProcesses directories, so impossible
   or unavailable interactions are reported and skipped.

The selected folders are copied from SubProcesses into effective_SubProcesses;
SubProcesses itself is never moved or deleted.  The previous effective
selection is replaced by default, or preserved under back_up/ when --backup
is enabled.

After selection, both physics tasks are delegated to the CMake-configured
Kerrigan.sh runtime.  --task relic asks Kerrigan for the density pipeline, while
--task sigmav asks the same Kerrigan runtime to stop after sigmaV/TOTALS_T.
The selector never calls mind_master.sh directly.  A precise Bash regex built
from exactly the selected process folders is passed to Kerrigan so the physics
run uses the same selection shown by the UI.

The parameter card may be given as an absolute/relative file path or as a file
name together with --cards-dir.  The same information can be supplied through
a text input file.  The CMake build directory can be supplied with --build-dir;
the program then executes the generated build/scripts/Kerrigan.sh, never the
raw Kerrigan.sh.in template.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Model metadata
# ---------------------------------------------------------------------------
#
# These aliases connect:
#     param_card particle / PDG  <->  SubProcesses folder token
#
# Examples:
#     Chi_1 -> n1
#     etR   -> etr
#     etI   -> eti
#     etp   -> etp and etpc (particle/antiparticle)
#
# This mapping is model-specific, but the selection logic below is generic.
#
SCOTOGENIC_FOLDER_ALIASES: dict[int, tuple[str, ...]] = {
    1001: ("etr",),
    1002: ("eti",),
    1003: ("etp", "etpc"),
    1012: ("n1",),
    1014: ("n2",),
    1016: ("n3",),
}

# Default dark-sector PDGs for this scotogenic UFO.
DEFAULT_DARK_PDGS: tuple[int, ...] = (1001, 1002, 1003, 1012, 1014, 1016)

# Approximate total internal degrees of freedom used only in the
# coannihilator relevance estimate.
#
# etR, etI: real neutral scalars -> g = 1
# etp: charged scalar plus antiparticle -> effective g = 2
# Chi_i: Majorana fermions -> g = 2
#
# If your UFO uses a different convention, edit this dictionary.
SCOTOGENIC_DOF: dict[int, float] = {
    1001: 1.0,
    1002: 1.0,
    1003: 2.0,
    1012: 2.0,
    1014: 2.0,
    1016: 2.0,
}

PROCESS_MARKER = "_UFO_"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Particle:
    pdg: int
    name: str
    mass: float
    width: Optional[float] = None


@dataclass
class DarkSectorDecision:
    pdg: int
    name: str
    mass: float
    width: Optional[float]
    delta_mass: float
    relative_eq_weight: float
    included: bool
    reason: str


@dataclass
class ProcessRecord:
    directory: str
    initial_compact: str
    initial_token_1: str
    initial_token_2: str
    initial_pdg_1: int
    initial_pdg_2: int
    final_compact: str
    category: str
    selected: bool


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def normalize_name(value: str) -> str:
    """Case-insensitive comparison ignoring spaces, underscores and symbols."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def parse_float(value: str) -> float:
    """Read E/e or Fortran D/d scientific notation."""
    return float(value.replace("D", "E").replace("d", "e"))


def yes_no(prompt: str, default: bool = False) -> bool:
    suffix = " [S/n]: " if default else " [s/N]: "
    answer = input(prompt + suffix).strip().lower()

    if not answer:
        return default

    return answer in {"s", "si", "sí", "y", "yes"}


def safe_relative_weight(
    candidate: Particle,
    particle: Particle,
    x_ref: float,
) -> tuple[float, float]:
    """
    Approximate equilibrium-density ratio:

        n_i^eq / n_DM^eq
          ~= (g_i/g_DM) (m_i/m_DM)^(3/2) exp[-x_ref * Delta_i]

        Delta_i = (m_i - m_DM) / m_DM

    This is a relevance filter, not a replacement for the full
    effective cross-section calculation.
    """
    if candidate.mass <= 0.0 or particle.mass <= 0.0:
        return math.inf, 0.0

    delta = (particle.mass - candidate.mass) / candidate.mass

    if 1.0 + delta <= 0.0:
        return delta, 0.0

    g_candidate = SCOTOGENIC_DOF.get(candidate.pdg, 1.0)
    g_particle = SCOTOGENIC_DOF.get(particle.pdg, 1.0)

    exponent = -x_ref * delta

    if exponent < -745.0:
        boltzmann = 0.0
    elif exponent > 700.0:
        boltzmann = math.inf
    else:
        boltzmann = math.exp(exponent)

    weight = (
        (g_particle / g_candidate)
        * math.pow(1.0 + delta, 1.5)
        * boltzmann
    )

    return delta, weight


# ---------------------------------------------------------------------------
# param_card parser
# ---------------------------------------------------------------------------

def read_param_card(path: Path) -> list[Particle]:
    """
    Read particles from Block MASS and widths from DECAY lines.

    Returned variable name in main:
        read_particles
    """
    particles: dict[int, Particle] = {}
    widths: dict[int, float] = {}
    in_mass_block = False

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            body, _, comment = raw_line.partition("#")
            stripped = body.strip()

            if not stripped:
                continue

            block_match = re.match(r"^block\s+(\S+)", stripped, re.IGNORECASE)
            if block_match:
                in_mass_block = block_match.group(1).lower() == "mass"
                continue

            decay_match = re.match(
                r"^decay\s+([+-]?\d+)\s+(\S+)",
                stripped,
                re.IGNORECASE,
            )
            if decay_match:
                pdg = int(decay_match.group(1))
                widths[pdg] = parse_float(decay_match.group(2))
                in_mass_block = False
                continue

            if not in_mass_block:
                continue

            fields = stripped.split()
            if len(fields) < 2:
                continue

            try:
                pdg = int(fields[0])
                mass = parse_float(fields[1])
            except ValueError:
                continue

            name = (
                comment.strip().split()[0]
                if comment.strip()
                else f"PDG_{pdg}"
            )

            particles[pdg] = Particle(
                pdg=pdg,
                name=name,
                mass=mass,
                width=None,
            )

    for pdg, width in widths.items():
        if pdg in particles:
            particles[pdg].width = width

    if not particles:
        raise ValueError(f"No se encontraron partículas en Block MASS de {path}")

    return list(particles.values())


def print_particle_table(read_particles: list[Particle]) -> None:
    print("\nPartículas leídas del param_card:")
    print("-" * 78)
    print(f"{'PDG':>8}  {'nombre':<14} {'masa [GeV]':>18} {'ancho [GeV]':>18}")
    print("-" * 78)

    for particle in read_particles:
        width_text = (
            "no disponible"
            if particle.width is None
            else f"{particle.width:.8e}"
        )
        print(
            f"{particle.pdg:>8d}  "
            f"{particle.name:<14} "
            f"{particle.mass:>18.8e} "
            f"{width_text:>18}"
        )

    print("-" * 78)


def resolve_candidate(
    query: str,
    read_particles: list[Particle],
) -> Particle:
    """Resolve a candidate from PDG, param-card name, or folder alias."""
    query = query.strip()

    # PDG lookup
    try:
        requested_pdg = int(query)
    except ValueError:
        requested_pdg = None

    if requested_pdg is not None:
        for particle in read_particles:
            if particle.pdg == requested_pdg:
                return particle
        raise ValueError(f"No existe el PDG {requested_pdg} en Block MASS.")

    normalized_query = normalize_name(query)
    matches: list[Particle] = []

    for particle in read_particles:
        possible_names = {
            normalize_name(particle.name),
            normalize_name(str(particle.pdg)),
        }

        for alias in SCOTOGENIC_FOLDER_ALIASES.get(particle.pdg, ()):
            possible_names.add(normalize_name(alias))

        # Convenient forms: Chi_1 -> chi1; etR -> etr, etc.
        if normalized_query in possible_names:
            matches.append(particle)

    if not matches:
        raise ValueError(
            f"No pude identificar '{query}'. "
            "Use el nombre del param_card, un alias de carpeta o el PDG."
        )

    if len(matches) > 1:
        options = ", ".join(f"{p.name} (PDG {p.pdg})" for p in matches)
        raise ValueError(f"Nombre ambiguo. Coincidencias: {options}")

    return matches[0]


# ---------------------------------------------------------------------------
# Candidate validation and effective dark sector
# ---------------------------------------------------------------------------

def get_dark_particles(
    read_particles: list[Particle],
    requested_dark_pdgs: Optional[set[int]],
) -> list[Particle]:
    particles_by_pdg = {particle.pdg: particle for particle in read_particles}

    if requested_dark_pdgs:
        missing = sorted(requested_dark_pdgs - particles_by_pdg.keys())
        if missing:
            raise ValueError(
                "Los siguientes PDG oscuros no existen en el param_card: "
                + ", ".join(map(str, missing))
            )
        dark_pdgs = requested_dark_pdgs
    else:
        available_defaults = {
            pdg for pdg in DEFAULT_DARK_PDGS if pdg in particles_by_pdg
        }

        # Model-specific list first; fallback for related UFOs.
        dark_pdgs = (
            available_defaults
            if available_defaults
            else {
                particle.pdg
                for particle in read_particles
                if abs(particle.pdg) >= 1000
            }
        )

    return [
        particles_by_pdg[pdg]
        for pdg in sorted(dark_pdgs)
    ]


def validate_candidate(
    candidate: Particle,
    dark_particles: list[Particle],
    allow_unstable: bool,
    allow_nonlightest: bool,
    width_tolerance: float,
) -> list[str]:
    warnings: list[str] = []

    if candidate.mass <= 0.0 or not math.isfinite(candidate.mass):
        raise ValueError(
            f"El candidato {candidate.name} tiene una masa inválida: "
            f"{candidate.mass}"
        )

    if candidate.pdg not in SCOTOGENIC_FOLDER_ALIASES:
        raise ValueError(
            f"No hay alias de SubProcesses configurado para "
            f"{candidate.name} (PDG {candidate.pdg})."
        )

    if candidate.width is None:
        warnings.append(
            "El ancho de decaimiento del candidato no aparece en el param_card; "
            "no se pudo validar su estabilidad."
        )
    elif abs(candidate.width) > width_tolerance:
        message = (
            f"El candidato {candidate.name} tiene ancho no nulo: "
            f"Gamma={candidate.width:.8e} GeV. "
            "Una partícula de materia oscura debe ser estable."
        )
        if allow_unstable:
            warnings.append(message)
        else:
            raise ValueError(
                message
                + " Use --allow-unstable-candidate solo para una prueba consciente."
            )

    lighter = [
        particle
        for particle in dark_particles
        if particle.pdg != candidate.pdg
        and particle.mass > 0.0
        and particle.mass < candidate.mass * (1.0 - 1.0e-12)
    ]

    if lighter:
        details = ", ".join(
            f"{particle.name}={particle.mass:.8e} GeV"
            for particle in lighter
        )
        message = (
            f"Existen partículas del sector oscuro más ligeras que "
            f"{candidate.name}: {details}."
        )
        if allow_nonlightest:
            warnings.append(message)
        else:
            raise ValueError(
                message
                + " Use --allow-nonlightest-candidate solo para una prueba consciente."
            )

    return warnings


def build_effective_dark_sector(
    candidate: Particle,
    dark_particles: list[Particle],
    x_ref: float,
    max_delta: float,
    min_relative_weight: float,
) -> tuple[set[int], list[DarkSectorDecision]]:
    active_pdgs: set[int] = {candidate.pdg}
    decisions: list[DarkSectorDecision] = []

    for particle in dark_particles:
        delta, weight = safe_relative_weight(candidate, particle, x_ref)

        if particle.pdg == candidate.pdg:
            included = True
            reason = "candidate"
        elif particle.mass <= 0.0:
            included = False
            reason = "invalid/non-positive mass"
        elif delta < 0.0:
            included = False
            reason = "lighter than candidate"
        elif delta > max_delta:
            included = False
            reason = f"Delta={delta:.3e} > max_delta"
        elif weight < min_relative_weight:
            included = False
            reason = (
                f"relative_eq_weight={weight:.3e} "
                f"< min_relative_weight"
            )
        else:
            included = True
            reason = "mass-close and thermally relevant"
            active_pdgs.add(particle.pdg)

        decisions.append(
            DarkSectorDecision(
                pdg=particle.pdg,
                name=particle.name,
                mass=particle.mass,
                width=particle.width,
                delta_mass=delta,
                relative_eq_weight=weight,
                included=included,
                reason=reason,
            )
        )

    return active_pdgs, decisions


def print_dark_sector_table(
    decisions: list[DarkSectorDecision],
    x_ref: float,
    max_delta: float,
    min_relative_weight: float,
) -> None:
    print("\nValidación del sector oscuro efectivo")
    print(
        f"x_ref={x_ref:g}, max_delta={max_delta:g}, "
        f"min_relative_weight={min_relative_weight:g}"
    )
    print("-" * 116)
    print(
        f"{'PDG':>8}  {'nombre':<10} {'masa [GeV]':>16} "
        f"{'Delta':>13} {'peso eq. relativo':>19} "
        f"{'activo':>8}  motivo"
    )
    print("-" * 116)

    for decision in decisions:
        active_text = "sí" if decision.included else "no"
        print(
            f"{decision.pdg:>8d}  "
            f"{decision.name:<10} "
            f"{decision.mass:>16.8e} "
            f"{decision.delta_mass:>13.5e} "
            f"{decision.relative_eq_weight:>19.5e} "
            f"{active_text:>8}  "
            f"{decision.reason}"
        )

    print("-" * 116)


# ---------------------------------------------------------------------------
# SubProcesses parser
# ---------------------------------------------------------------------------

def build_alias_lookup(
    dark_particles: list[Particle],
) -> tuple[dict[str, int], list[str]]:
    alias_to_pdg: dict[str, int] = {}

    for particle in dark_particles:
        aliases = SCOTOGENIC_FOLDER_ALIASES.get(particle.pdg, ())
        for alias in aliases:
            if alias in alias_to_pdg and alias_to_pdg[alias] != particle.pdg:
                raise ValueError(f"Alias duplicado en configuración: {alias}")
            alias_to_pdg[alias] = particle.pdg

    # Longest first prevents etp from interfering with etpc.
    sorted_aliases = sorted(alias_to_pdg, key=len, reverse=True)
    return alias_to_pdg, sorted_aliases


def split_initial_state(
    initial_compact: str,
    alias_to_pdg: dict[str, int],
    sorted_aliases: list[str],
) -> Optional[tuple[str, str]]:
    candidates: list[tuple[str, str]] = []

    for first_alias in sorted_aliases:
        if not initial_compact.startswith(first_alias):
            continue

        second_alias = initial_compact[len(first_alias):]

        if second_alias in alias_to_pdg:
            candidates.append((first_alias, second_alias))

    if not candidates:
        return None

    # Normally unique. Deterministic choice if aliases produce duplicates.
    candidates.sort(
        key=lambda pair: (len(pair[0]) + len(pair[1]), len(pair[0])),
        reverse=True,
    )

    best = candidates[0]

    if len(candidates) > 1 and candidates[1] != best:
        # Keep the best deterministic split; it will be visible in the manifest.
        return best

    return best


def parse_process_directory(
    directory_name: str,
    alias_to_pdg: dict[str, int],
    sorted_aliases: list[str],
) -> Optional[tuple[str, str, str, str]]:
    if PROCESS_MARKER not in directory_name:
        return None

    payload = directory_name.split(PROCESS_MARKER, 1)[1]

    if "_" not in payload:
        return None

    initial_compact, final_compact = payload.split("_", 1)

    split = split_initial_state(
        initial_compact,
        alias_to_pdg,
        sorted_aliases,
    )

    if split is None:
        return None

    first_alias, second_alias = split

    return initial_compact, first_alias, second_alias, final_compact


def scan_processes(
    subprocesses_dir: Path,
    dark_particles: list[Particle],
    candidate: Particle,
    active_pdgs: set[int],
    mode: str,
) -> tuple[list[ProcessRecord], list[str]]:
    alias_to_pdg, sorted_aliases = build_alias_lookup(dark_particles)

    records: list[ProcessRecord] = []
    unparsed: list[str] = []

    candidate_aliases = set(
        SCOTOGENIC_FOLDER_ALIASES.get(candidate.pdg, ())
    )

    for child in sorted(subprocesses_dir.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue

        parsed = parse_process_directory(
            child.name,
            alias_to_pdg,
            sorted_aliases,
        )

        if parsed is None:
            unparsed.append(child.name)
            continue

        initial_compact, token_1, token_2, final_compact = parsed
        pdg_1 = alias_to_pdg[token_1]
        pdg_2 = alias_to_pdg[token_2]

        direct_candidate = (
            token_1 in candidate_aliases
            and token_2 in candidate_aliases
        )

        active_pair = (
            pdg_1 in active_pdgs
            and pdg_2 in active_pdgs
        )

        if direct_candidate:
            category = "candidate_only"
        elif active_pair and candidate.pdg in {pdg_1, pdg_2}:
            category = "candidate_coannihilation"
        elif active_pair:
            category = "coannihilator_pair"
        else:
            category = "outside_effective_sector"

        if mode == "candidate_only":
            selected = direct_candidate
        elif mode in {"effective_dark_sector", "combined"}:
            selected = active_pair
        else:
            raise ValueError(f"Modo desconocido: {mode}")

        records.append(
            ProcessRecord(
                directory=child.name,
                initial_compact=initial_compact,
                initial_token_1=token_1,
                initial_token_2=token_2,
                initial_pdg_1=pdg_1,
                initial_pdg_2=pdg_2,
                final_compact=final_compact,
                category=category,
                selected=selected,
            )
        )

    return records, unparsed


def print_selection_summary(
    records: list[ProcessRecord],
    unparsed: list[str],
    mode: str,
) -> None:
    selected = [record for record in records if record.selected]

    categories: dict[str, int] = {}
    for record in selected:
        categories[record.category] = categories.get(record.category, 0) + 1

    print("\nResumen de selección")
    print("-" * 72)
    print(f"Modo                         : {mode}")
    print(f"Directorios analizados       : {len(records) + len(unparsed)}")
    print(f"Directorios interpretados    : {len(records)}")
    print(f"Directorios no interpretados : {len(unparsed)}")
    print(f"Directorios seleccionados    : {len(selected)}")

    for category in (
        "candidate_only",
        "candidate_coannihilation",
        "coannihilator_pair",
    ):
        print(f"  {category:<28}: {categories.get(category, 0)}")

    print("-" * 72)


def print_selected_processes(records: list[ProcessRecord]) -> None:
    selected = [record for record in records if record.selected]

    print("\nProcesos seleccionados:")
    print("-" * 120)

    for index, record in enumerate(selected, start=1):
        print(
            f"{index:>5d}. [{record.category:<25}] "
            f"{record.initial_token_1}({record.initial_pdg_1}) + "
            f"{record.initial_token_2}({record.initial_pdg_2}) "
            f"-> {record.final_compact:<20} "
            f"{record.directory}"
        )

    print("-" * 120)


# ---------------------------------------------------------------------------
# Copy and reports
# ---------------------------------------------------------------------------

def write_reports(
    output_dir: Path,
    param_card: Path,
    candidate: Particle,
    mode: str,
    active_pdgs: set[int],
    decisions: list[DarkSectorDecision],
    records: list[ProcessRecord],
    unparsed: list[str],
    settings: dict,
) -> tuple[Path, Path]:
    report_base = output_dir.parent / f"{output_dir.name}_selection"
    json_path = report_base.with_suffix(".json")
    csv_path = report_base.with_suffix(".csv")

    selected_records = [record for record in records if record.selected]

    report = {
        "param_card": str(param_card.resolve()),
        "candidate": asdict(candidate),
        "mode": mode,
        "active_dark_pdgs": sorted(active_pdgs),
        "settings": settings,
        "dark_sector_decisions": [asdict(item) for item in decisions],
        "selected_count": len(selected_records),
        "selected_processes": [asdict(item) for item in selected_records],
        "unparsed_processes": unparsed,
        "output_directory": str(output_dir.resolve()),
    }

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)

    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = list(ProcessRecord.__dataclass_fields__.keys())
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for record in selected_records:
            writer.writerow(asdict(record))

    return json_path, csv_path


def copy_selected_processes(
    subprocesses_dir: Path,
    output_dir: Path,
    records: list[ProcessRecord],
) -> None:
    selected = [record for record in records if record.selected]

    if not selected:
        raise ValueError("No hay procesos seleccionados para copiar.")

    source_resolved = subprocesses_dir.resolve()
    output_resolved = output_dir.resolve()

    if source_resolved == output_resolved:
        raise ValueError(
            "La carpeta de salida no puede ser la misma que SubProcesses."
        )

    temporary_dir = output_dir.with_name(output_dir.name + ".__tmp__")

    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)

    temporary_dir.mkdir(parents=True)

    try:
        total = len(selected)

        for index, record in enumerate(selected, start=1):
            source = subprocesses_dir / record.directory
            destination = temporary_dir / record.directory

            print(
                f"\rCopiando {index}/{total}: {record.directory}",
                end="",
                flush=True,
            )

            shutil.copytree(
                source,
                destination,
                symlinks=True,
                copy_function=shutil.copy2,
            )

        print()

        # Atomic-style replacement: the old output is removed only after
        # the complete new selection was copied successfully.
        if output_dir.exists():
            shutil.rmtree(output_dir)

        temporary_dir.rename(output_dir)

    except Exception:
        print()
        print(
            f"Falló la copia. La fuente {subprocesses_dir} no fue modificada.",
            file=sys.stderr,
        )
        raise


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# V2: manual PDG mode, input files, backup, UI and pipeline orchestration
# ---------------------------------------------------------------------------

def parse_dark_pdgs(value: Optional[str]) -> Optional[set[int]]:
    if value is None:
        return None

    values = {
        int(item.strip())
        for item in re.split(r"[\s,;]+", value)
        if item.strip()
    }

    return values or None


@dataclass
class ManualPDGDecision:
    pdg: int
    name: str
    mass: float
    width: Optional[float]
    delta_mass: float
    interaction_count: int
    included: bool
    reason: str


def parse_bool(value: object, field_name: str = "value") -> bool:
    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()

    if normalized in {"1", "true", "yes", "y", "si", "sí", "on"}:
        return True
    if normalized in {"0", "false", "no", "n", "off"}:
        return False

    raise ValueError(
        f"Valor booleano inválido para {field_name}: {value!r}. "
        "Use yes/no, true/false, 1/0 o si/no."
    )


def parse_pdg_tokens(value: object) -> list[int]:
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        tokens: list[str] = []
        for item in value:
            tokens.extend(re.split(r"[\s,;]+", str(item).strip()))
    else:
        tokens = re.split(r"[\s,;]+", str(value).strip())

    pdgs: list[int] = []
    for token in tokens:
        if not token:
            continue
        try:
            pdgs.append(int(token))
        except ValueError as exc:
            raise ValueError(f"PDG inválido en la entrada: {token!r}") from exc

    return pdgs


def load_input_file(path: Path) -> dict[str, object]:
    """
    Read either:

        1012 1014 1001

    or a key/value block such as:

        mode = pdg
        cards_dir = /path/to/cards
        param_card = para_card1.dat
        build_dir = /path/to/project/build
        mg5_output = /path/to/MG5/scotogenic
        pdgs = 1012 1014 1001
        xf = 28
        verbose = yes
        backup = no
        task = relic

    CLI arguments override values from this file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo de entrada: {path}")

    config: dict[str, object] = {}
    bare_pdgs: list[int] = []

    key_aliases = {
        "x_ref": "xf",
        "x-ref": "xf",
        "candidate_pdg": "candidate",
        "candidate-pdg": "candidate",
        "process": "task",
        "calculation": "task",
        "ui": "verbose",
        "card_dir": "cards_dir",
        "cards_path": "cards_dir",
        "param_cards_dir": "cards_dir",
        "param-card-dir": "cards_dir",
        "cmake_build_dir": "build_dir",
        "cmake-build-dir": "build_dir",
        "build": "build_dir",
        "mg5-output": "mg5_output",
        "mg5_output_folder": "mg5_output",
        "physics_output": "physics_output_root",
        "physics-output": "physics_output_root",
        "output_root": "physics_output_root",
        "run_output": "physics_output_root",
    }

    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line_number, raw_line in enumerate(handle, start=1):
            stripped = raw_line.split("#", 1)[0].strip()
            if not stripped:
                continue

            match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*)\s*[:=]\s*(.*?)\s*$", stripped)
            if match:
                key = match.group(1).strip().lower()
                key = key_aliases.get(key, key)
                config[key] = match.group(2).strip()
                continue

            # A non-key line is accepted only when it is a list of integer PDGs.
            try:
                bare_pdgs.extend(parse_pdg_tokens(stripped))
            except ValueError as exc:
                raise ValueError(
                    f"Línea {line_number} de {path} no reconocida: {stripped!r}. "
                    "Use key=value o una lista de PDGs."
                ) from exc

    if bare_pdgs:
        if "pdgs" in config:
            config["pdgs"] = parse_pdg_tokens(config["pdgs"]) + bare_pdgs
        else:
            config["pdgs"] = bare_pdgs

    if "pdgs" in config and not isinstance(config["pdgs"], list):
        config["pdgs"] = parse_pdg_tokens(config["pdgs"])

    return config


def config_value(
    cli_value: object,
    file_config: dict[str, object],
    key: str,
    default: object,
) -> object:
    if cli_value is not None:
        return cli_value
    if key in file_config:
        return file_config[key]
    return default


def resolve_runtime_path(value: object, default: Path) -> Path:
    if value is None:
        return default.expanduser().resolve()
    return Path(str(value)).expanduser().resolve()


def unique_pdgs(values: list[int]) -> list[int]:
    result: list[int] = []
    seen: set[int] = set()
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result


def particle_by_pdg(read_particles: list[Particle], pdg: int) -> Particle:
    for particle in read_particles:
        if particle.pdg == pdg:
            return particle
    raise ValueError(f"El PDG {pdg} no existe en Block MASS del param_card.")


def print_candidate_summary(candidate: Particle) -> None:
    print("\nCandidato identificado")
    print("-" * 72)
    print(f"Nombre          : {candidate.name}")
    print(f"PDG             : {candidate.pdg}")
    print(f"Masa            : {candidate.mass:.8e} GeV")
    print(
        "Ancho           : "
        + (
            "no disponible"
            if candidate.width is None
            else f"{candidate.width:.8e} GeV"
        )
    )
    print(
        "Alias de carpeta: "
        + ", ".join(SCOTOGENIC_FOLDER_ALIASES[candidate.pdg])
    )
    print("-" * 72)


def scan_processes_pdg(
    subprocesses_dir: Path,
    dark_particles: list[Particle],
    candidate: Particle,
    requested_pdgs: list[int],
) -> tuple[list[ProcessRecord], list[str], list[ManualPDGDecision], list[str]]:
    """
    Manual PDG selection.

    requested_pdgs[0] is always the DM candidate.

    Selection rule:
      * include every candidate + candidate channel;
      * for every later PDG, include every candidate + partner channel;
      * do NOT automatically include partner + partner channels.

    A requested candidate/partner pair is considered physically available to
    this generated model only when at least one corresponding SubProcesses
    directory exists.  This validates the request against the actual MadGraph
    process inventory rather than guessing from names alone.
    """
    if not requested_pdgs:
        raise ValueError("El modo PDG necesita al menos el PDG del candidato.")

    candidate_pdg = requested_pdgs[0]
    partner_pdgs = [pdg for pdg in unique_pdgs(requested_pdgs[1:]) if pdg != candidate_pdg]

    # Ensure every requested initial-state particle can be mapped to a
    # SubProcesses token.
    for pdg in [candidate_pdg] + partner_pdgs:
        particle = particle_by_pdg(dark_particles, pdg)
        if pdg not in SCOTOGENIC_FOLDER_ALIASES:
            raise ValueError(
                f"{pdg} ({particle.name}) existe en el param_card, pero no tiene "
                "alias de estado inicial configurado para SubProcesses."
            )

    alias_to_pdg, sorted_aliases = build_alias_lookup(dark_particles)

    parsed_rows: list[tuple[Path, str, str, str, str, int, int]] = []
    unparsed: list[str] = []

    for child in sorted(subprocesses_dir.iterdir(), key=lambda path: path.name):
        if not child.is_dir():
            continue

        parsed = parse_process_directory(child.name, alias_to_pdg, sorted_aliases)
        if parsed is None:
            unparsed.append(child.name)
            continue

        initial_compact, token_1, token_2, final_compact = parsed
        pdg_1 = alias_to_pdg[token_1]
        pdg_2 = alias_to_pdg[token_2]
        parsed_rows.append(
            (child, initial_compact, token_1, token_2, final_compact, pdg_1, pdg_2)
        )

    pair_counts: dict[int, int] = {pdg: 0 for pdg in partner_pdgs}
    candidate_candidate_count = 0

    for _, _, _, _, _, pdg_1, pdg_2 in parsed_rows:
        if pdg_1 == candidate_pdg and pdg_2 == candidate_pdg:
            candidate_candidate_count += 1

        for partner_pdg in partner_pdgs:
            if (
                (pdg_1 == candidate_pdg and pdg_2 == partner_pdg)
                or (pdg_2 == candidate_pdg and pdg_1 == partner_pdg)
            ):
                pair_counts[partner_pdg] += 1

    valid_partners = {pdg for pdg, count in pair_counts.items() if count > 0}
    warnings: list[str] = []

    if candidate_candidate_count == 0:
        warnings.append(
            f"No existe ningún canal {candidate_pdg}+{candidate_pdg} en SubProcesses."
        )

    decisions: list[ManualPDGDecision] = []
    for pdg in partner_pdgs:
        partner = particle_by_pdg(dark_particles, pdg)
        delta = (
            (partner.mass - candidate.mass) / candidate.mass
            if candidate.mass > 0.0
            else math.inf
        )
        count = pair_counts[pdg]
        included = count > 0

        if included:
            reason = f"manual request; {count} channel(s) found"
        else:
            reason = "no candidate-partner process exists in SubProcesses"
            warnings.append(
                f"{candidate.pdg} ({candidate.name}) no puede interactuar con "
                f"{pdg} ({partner.name}) dentro del inventario actual de "
                "SubProcesses: no existe ningún canal generado para ese estado inicial."
            )

        decisions.append(
            ManualPDGDecision(
                pdg=pdg,
                name=partner.name,
                mass=partner.mass,
                width=partner.width,
                delta_mass=delta,
                interaction_count=count,
                included=included,
                reason=reason,
            )
        )

    records: list[ProcessRecord] = []

    for child, initial_compact, token_1, token_2, final_compact, pdg_1, pdg_2 in parsed_rows:
        direct_candidate = pdg_1 == candidate_pdg and pdg_2 == candidate_pdg
        manual_coannihilation = any(
            (
                (pdg_1 == candidate_pdg and pdg_2 == partner_pdg)
                or (pdg_2 == candidate_pdg and pdg_1 == partner_pdg)
            )
            for partner_pdg in valid_partners
        )

        selected = direct_candidate or manual_coannihilation

        if direct_candidate:
            category = "candidate_only"
        elif manual_coannihilation:
            category = "candidate_coannihilation"
        else:
            category = "outside_manual_pdg_selection"

        records.append(
            ProcessRecord(
                directory=child.name,
                initial_compact=initial_compact,
                initial_token_1=token_1,
                initial_token_2=token_2,
                initial_pdg_1=pdg_1,
                initial_pdg_2=pdg_2,
                final_compact=final_compact,
                category=category,
                selected=selected,
            )
        )

    return records, unparsed, decisions, warnings


def print_manual_pdg_table(
    candidate: Particle,
    requested_pdgs: list[int],
    decisions: list[ManualPDGDecision],
) -> None:
    print("\nValidación del modo PDG")
    print("-" * 118)
    print(
        "Regla: el primer PDG es el candidato; se incluyen todas sus "
        "aniquilaciones y solo las coaniquilaciones candidato+PDG solicitadas."
    )
    print(f"Entrada PDG: {' '.join(map(str, requested_pdgs))}")
    print(f"Candidato : {candidate.pdg} ({candidate.name})")
    print("-" * 118)
    print(
        f"{'PDG':>8}  {'nombre':<10} {'masa [GeV]':>16} "
        f"{'Delta':>13} {'canales':>10} {'válido':>8}  motivo"
    )
    print("-" * 118)

    if not decisions:
        print("No se solicitaron coaniquiladores adicionales; solo se usarán las aniquilaciones del candidato.")
    else:
        for decision in decisions:
            valid_text = "sí" if decision.included else "no"
            print(
                f"{decision.pdg:>8d}  "
                f"{decision.name:<10} "
                f"{decision.mass:>16.8e} "
                f"{decision.delta_mass:>13.5e} "
                f"{decision.interaction_count:>10d} "
                f"{valid_text:>8}  "
                f"{decision.reason}"
            )

    print("-" * 118)


def build_manual_report_decisions(
    candidate: Particle,
    dark_particles: list[Particle],
    requested_pdgs: list[int],
    xf: float,
) -> list[DarkSectorDecision]:
    """Use the original report schema while marking the PDG selection as manual."""
    requested_set = set(requested_pdgs)
    decisions: list[DarkSectorDecision] = []

    for particle in dark_particles:
        delta, weight = safe_relative_weight(candidate, particle, xf)
        included = particle.pdg in requested_set
        if particle.pdg == candidate.pdg:
            reason = "manual candidate"
        elif included:
            reason = "manual PDG request; mass filter not applied"
        else:
            reason = "not requested in manual PDG mode"

        decisions.append(
            DarkSectorDecision(
                pdg=particle.pdg,
                name=particle.name,
                mass=particle.mass,
                width=particle.width,
                delta_mass=delta,
                relative_eq_weight=weight,
                included=included,
                reason=reason,
            )
        )

    return decisions


def report_paths_for_output(output_dir: Path) -> tuple[Path, Path]:
    report_base = output_dir.parent / f"{output_dir.name}_selection"
    return report_base.with_suffix(".json"), report_base.with_suffix(".csv")


def next_backup_directory(backup_root: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destination = backup_root / stamp
    counter = 1
    while destination.exists():
        destination = backup_root / f"{stamp}_{counter}"
        counter += 1
    return destination


def copy_selected_processes_v2(
    subprocesses_dir: Path,
    output_dir: Path,
    records: list[ProcessRecord],
    backup: bool,
    backup_root: Path,
    verbose: bool,
) -> Optional[Path]:
    """
    Copy the new selection first, then replace the previous selection.

    SubProcesses is read-only from this program's point of view.

    If backup=True, the previous effective_SubProcesses and its JSON/CSV
    reports are moved into back_up/<timestamp>/ before the new selection is
    activated.  With backup=False they are simply replaced.
    """
    selected = [record for record in records if record.selected]
    if not selected:
        raise ValueError("No hay procesos seleccionados para copiar.")

    source_resolved = subprocesses_dir.resolve()
    output_resolved = output_dir.resolve()
    if source_resolved == output_resolved:
        raise ValueError("La carpeta de salida no puede ser la misma que SubProcesses.")

    temporary_dir = output_dir.with_name(output_dir.name + ".__tmp__")
    if temporary_dir.exists():
        shutil.rmtree(temporary_dir)
    temporary_dir.mkdir(parents=True)

    try:
        total = len(selected)
        for index, record in enumerate(selected, start=1):
            source = subprocesses_dir / record.directory
            destination = temporary_dir / record.directory

            if verbose:
                print(
                    f"\rCopiando {index}/{total}: {record.directory}",
                    end="",
                    flush=True,
                )

            shutil.copytree(
                source,
                destination,
                symlinks=True,
                copy_function=shutil.copy2,
            )

        if verbose:
            print()

        json_report, csv_report = report_paths_for_output(output_dir)
        previous_items = [path for path in (output_dir, json_report, csv_report) if path.exists()]
        backup_destination: Optional[Path] = None

        if previous_items and backup:
            backup_destination = next_backup_directory(backup_root)
            backup_destination.mkdir(parents=True, exist_ok=False)

            for item in previous_items:
                shutil.move(str(item), str(backup_destination / item.name))
        else:
            if output_dir.exists():
                shutil.rmtree(output_dir)
            for report in (json_report, csv_report):
                if report.exists():
                    report.unlink()

        temporary_dir.rename(output_dir)
        return backup_destination

    except Exception:
        if temporary_dir.exists():
            shutil.rmtree(temporary_dir, ignore_errors=True)
        print(
            f"Falló la copia. La fuente {subprocesses_dir} no fue modificada.",
            file=sys.stderr,
        )
        raise


def bash_regex_for_selected_processes(records: list[ProcessRecord]) -> str:
    names = sorted(record.directory for record in records if record.selected)
    if not names:
        raise ValueError("No hay procesos seleccionados para construir el selector.")

    # Directory names are mostly alphanumeric/underscore, but re.escape keeps
    # this safe if a future generated process contains regex metacharacters.
    alternatives = "|".join(re.escape(name) for name in names)
    return f"^({alternatives})$"


def resolve_param_card_path(
    value: object,
    cards_dir: Optional[Path],
    config_dir: Optional[Path],
) -> Path:
    """Resolve one parameter card without requiring Experiment/cards."""
    raw = Path(str(value)).expanduser()

    if raw.is_absolute():
        candidate = raw.resolve()
        if candidate.is_file():
            return candidate
        raise FileNotFoundError(f"No existe el param_card: {candidate}")

    candidates: list[Path] = []

    # When --cards-dir/cards_dir is supplied, it is the preferred source.
    if cards_dir is not None:
        candidates.append(cards_dir / raw)

    # A path written inside an input/config file may naturally be relative to
    # that file.  This is checked before the process working directory.
    if config_dir is not None:
        candidates.append(config_dir / raw)

    candidates.append(Path.cwd() / raw)

    seen: set[Path] = set()
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if resolved.is_file():
            return resolved

    tried = "\n  - ".join(str(path.resolve()) for path in candidates)
    raise FileNotFoundError(
        f"No pude localizar el param_card '{raw}'. Rutas probadas:\n  - {tried}"
    )


def resolve_cmake_kerrigan(
    script_root: Path,
    explicit_kerrigan: Optional[object],
    build_dir_value: Optional[object],
    config_dir: Optional[Path],
) -> tuple[Path, Path]:
    """
    Locate the Kerrigan.sh generated by CMake.

    The raw Kerrigan.sh.in template is deliberately rejected.  If --build-dir is
    supplied, the normal target is <build>/scripts/Kerrigan.sh.
    """
    candidate_paths: list[Path] = []
    resolved_build_dir: Optional[Path] = None

    if build_dir_value is not None:
        raw_build = Path(str(build_dir_value)).expanduser()
        if not raw_build.is_absolute() and config_dir is not None:
            config_relative = (config_dir / raw_build).resolve()
            cwd_relative = (Path.cwd() / raw_build).resolve()
            resolved_build_dir = (
                config_relative if config_relative.exists() else cwd_relative
            )
        else:
            resolved_build_dir = raw_build.resolve()

    if explicit_kerrigan is not None:
        raw = Path(str(explicit_kerrigan)).expanduser()
        if not raw.is_absolute() and config_dir is not None:
            config_relative = (config_dir / raw).resolve()
            cwd_relative = (Path.cwd() / raw).resolve()
            raw = config_relative if config_relative.exists() else cwd_relative
        candidate_paths.append(raw.resolve())
    else:
        env_kerrigan = os.environ.get("SCOTOGENIC_KERRIGAN") or os.environ.get(
            "KERRIGAN_RUNTIME"
        )
        if env_kerrigan:
            candidate_paths.append(Path(env_kerrigan).expanduser().resolve())

        env_build = os.environ.get("SCOTOGENIC_BUILD_DIR")
        if resolved_build_dir is None and env_build:
            resolved_build_dir = Path(env_build).expanduser().resolve()

        if resolved_build_dir is not None:
            candidate_paths.extend(
                [
                    resolved_build_dir / "scripts" / "Kerrigan.sh",
                    resolved_build_dir / "Kerrigan.sh",
                ]
            )

        # Conservative auto-discovery for common source/build layouts.
        candidate_paths.extend(
            [
                script_root / "build" / "scripts" / "Kerrigan.sh",
                script_root.parent / "build" / "scripts" / "Kerrigan.sh",
                script_root / "../build/scripts/Kerrigan.sh",
            ]
        )

    checked: list[Path] = []
    for candidate in candidate_paths:
        candidate = candidate.expanduser().resolve()
        if candidate in checked:
            continue
        checked.append(candidate)
        if not candidate.is_file():
            continue
        if candidate.name.endswith(".in"):
            continue

        content = candidate.read_text(encoding="utf-8", errors="replace")
        unresolved = [
            token
            for token in ("@FOLDER@", "@CMAKE_BINARY_DIR@", "@CMAKE_SOURCE_DIR@")
            if token in content
        ]
        if unresolved:
            continue

        # The generated script normally lives in <build>/scripts/.
        detected_build = (
            resolved_build_dir
            if resolved_build_dir is not None
            else (candidate.parent.parent if candidate.parent.name == "scripts" else candidate.parent)
        )
        return candidate, detected_build.resolve()

    tried = "\n  - ".join(str(path) for path in checked) or "(ninguna ruta candidata)"
    raise FileNotFoundError(
        "No encontré un Kerrigan.sh generado por CMake. El selector ya no ejecuta "
        "Kerrigan.sh.in ni mind_master.sh directamente.\n"
        "Ejecute CMake y/o indique --build-dir /ruta/al/build o --kerrigan "
        "/ruta/al/build/scripts/Kerrigan.sh.\n"
        f"Rutas probadas:\n  - {tried}"
    )


def infer_mg5_output(subprocesses_dir: Path, explicit_value: Optional[object]) -> Optional[Path]:
    if explicit_value is not None:
        path = Path(str(explicit_value)).expanduser().resolve()
        if not path.is_dir():
            raise FileNotFoundError(f"No existe el MG5 output: {path}")
        return path

    # A normal MadGraph output has .../<output>/SubProcesses and .../<output>/src.
    if subprocesses_dir.name == "SubProcesses":
        parent = subprocesses_dir.parent.resolve()
        if (parent / "src").is_dir():
            return parent

    return None


def run_kerrigan(
    kerrigan: Path,
    build_dir: Path,
    param_card: Path,
    task: str,
    mode: str,
    candidate: Particle,
    selector_regex: str,
    selection_report: Path,
    mg5_output: Optional[Path],
    physics_output_root: Optional[Path],
    verbose: bool,
) -> None:
    """Delegate both relic and sigmaV tasks to the CMake-configured Kerrigan."""
    if not kerrigan.is_file():
        raise FileNotFoundError(f"No existe el Kerrigan generado por CMake: {kerrigan}")

    command = [
        "bash",
        str(kerrigan),
        str(param_card.resolve()),
        "--task",
        task,
        "--mode",
        mode,
        "--candidate",
        candidate.name,
        "--candidate-pdg",
        str(candidate.pdg),
        "--selection-report",
        str(selection_report.resolve()),
        "--process-selector",
        selector_regex,
    ]

    if mg5_output is not None:
        command.extend(["--mg5-output", str(mg5_output.resolve())])

    if physics_output_root is not None:
        command.extend(["--output-root", str(physics_output_root.resolve())])

    environment = os.environ.copy()
    environment["KERRIGAN_PROCESS_SELECTOR"] = selector_regex
    environment["KERRIGAN_TASK"] = task
    environment["KERRIGAN_MODE"] = mode
    environment["KERRIGAN_CANDIDATE"] = candidate.name
    environment["KERRIGAN_CANDIDATE_PDG"] = str(candidate.pdg)
    environment["KERRIGAN_SELECTION_REPORT"] = str(selection_report.resolve())

    if verbose:
        print("\nIniciando cálculo con Kerrigan generado por CMake")
        print(f"Kerrigan runtime   : {kerrigan}")
        print(f"CMake build        : {build_dir}")
        print(f"Card               : {param_card}")
        print(f"Task               : {task}")
        if task == "sigmav":
            print("Pipeline            : sigmaV solamente (sin rama de relic density)")
        else:
            print("Pipeline            : relic density")
        print(
            f"Procesos filtrados : selector exacto con "
            f"{selector_regex.count('|') + 1} carpeta(s)"
        )
        if mg5_output is not None:
            print(f"MG5 output         : {mg5_output}")
        if physics_output_root is not None:
            print(f"Physics output root: {physics_output_root}")

    subprocess.run(
        command,
        cwd=build_dir if build_dir.is_dir() else kerrigan.parent,
        env=environment,
        check=True,
    )

def build_parser() -> argparse.ArgumentParser:
    script_root = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description=(
            "Select scotogenic subprocesses in combined or manual-PDG mode, "
            "optionally show the full UI, copy the clean selection and delegate "
            "both relic-density and sigmaV tasks to CMake-configured Kerrigan."
        )
    )

    parser.add_argument(
        "param_card",
        nargs="?",
        type=Path,
        help=(
            "Parameter-card path or filename. With --cards-dir, a bare filename is "
            "resolved inside that directory. Optional when supplied by --input-file."
        ),
    )

    parser.add_argument(
        "--input-file",
        "--config",
        dest="input_file",
        type=Path,
        help="Text file containing PDGs or a key=value run block.",
    )

    parser.add_argument(
        "--cards-dir",
        "--param-cards-dir",
        dest="cards_dir",
        type=Path,
        default=None,
        help=(
            "Directory containing parameter cards. Useful when param_card is only a "
            "filename. The same option is available as cards_dir=... in --input-file."
        ),
    )

    parser.add_argument(
        "--mode",
        choices=["combined", "pdg"],
        default=None,
        help="Selection mode. Default: combined, unless manual PDGs are supplied.",
    )

    parser.add_argument(
        "--candidate",
        default=None,
        help="Candidate name, alias or PDG for combined mode.",
    )

    parser.add_argument(
        "--pdgs",
        nargs="+",
        type=int,
        default=None,
        help=(
            "Manual PDG mode. First PDG is the DM candidate; later PDGs are "
            "requested candidate coannihilation partners."
        ),
    )

    parser.add_argument(
        "--xf",
        "--x-ref",
        dest="xf",
        type=float,
        default=None,
        help=(
            "Freeze-out x_f=m_DM/T used by the combined Boltzmann filter. "
            "Default: 25."
        ),
    )

    parser.add_argument(
        "--max-delta",
        type=float,
        default=None,
        help="Maximum relative mass splitting for combined mode. Default: 0.25.",
    )

    parser.add_argument(
        "--min-relative-weight",
        type=float,
        default=None,
        help="Minimum equilibrium weight for combined mode. Default: 1e-3.",
    )

    parser.add_argument(
        "--dark-pdgs",
        default=None,
        help=(
            "Advanced: comma-separated dark-sector PDGs used by combined-mode "
            "candidate/effective-sector validation."
        ),
    )

    parser.add_argument(
        "--task",
        choices=["relic", "sigmav"],
        default=None,
        help="Calculation to trigger after selection. Default: relic.",
    )

    verbose_group = parser.add_mutually_exclusive_group()
    verbose_group.add_argument(
        "--verbose",
        dest="verbose",
        action="store_true",
        default=None,
        help="Show the complete UI, tables and review question.",
    )
    verbose_group.add_argument(
        "--quiet",
        "--no-verbose",
        dest="verbose",
        action="store_false",
        help="Run without the detailed UI/review prompts.",
    )

    backup_group = parser.add_mutually_exclusive_group()
    backup_group.add_argument(
        "--backup",
        dest="backup",
        action="store_true",
        default=None,
        help="Save the previous effective selection under back_up/<timestamp>/.",
    )
    backup_group.add_argument(
        "--no-backup",
        dest="backup",
        action="store_false",
        help="Replace the previous effective selection. This is the default.",
    )

    parser.add_argument(
        "--subprocesses",
        type=Path,
        default=None,
        help=f"Source folder. Default: {script_root / 'SubProcesses'}",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help=f"Selected-process copy. Default: {script_root / 'effective_SubProcesses'}",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=None,
        help=f"Backup root. Default: {script_root / 'back_up'}",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=None,
        help=(
            "CMake build directory. The runtime is resolved as "
            "<build-dir>/scripts/Kerrigan.sh (preferred)."
        ),
    )
    parser.add_argument(
        "--kerrigan",
        type=Path,
        default=None,
        help=(
            "Explicit path to the Kerrigan.sh GENERATED by CMake. Kerrigan.sh.in "
            "is rejected as a runtime target."
        ),
    )
    parser.add_argument(
        "--mg5-output",
        type=Path,
        default=None,
        help=(
            "MadGraph output root containing SubProcesses/src. If omitted, it is "
            "inferred from --subprocesses when possible."
        ),
    )
    parser.add_argument(
        "--physics-output-root",
        "--run-output",
        dest="physics_output_root",
        type=Path,
        default=None,
        help=(
            "Optional output ROOT passed to Kerrigan. Kerrigan creates a unique "
            "run directory below it for both relic and sigmav tasks."
        ),
    )

    parser.add_argument(
        "--width-tolerance",
        type=float,
        default=None,
        help="Maximum width treated as stable. Default: 1e-30 GeV.",
    )
    parser.add_argument(
        "--allow-unstable-candidate",
        action="store_true",
        help="Allow a candidate with nonzero DECAY width.",
    )
    parser.add_argument(
        "--allow-nonlightest-candidate",
        action="store_true",
        help="Allow a candidate heavier than another configured dark-sector particle.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and preview only: no copy, backup or physics calculation.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip review/copy confirmation while keeping verbose output if requested.",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()
    script_root = Path(__file__).resolve().parent

    file_config: dict[str, object] = {}
    input_path: Optional[Path] = None
    config_dir: Optional[Path] = None
    if args.input_file is not None:
        input_path = args.input_file.expanduser().resolve()
        file_config = load_input_file(input_path)
        config_dir = input_path.parent

    # CLI > input file > defaults.
    pdgs_cli = args.pdgs
    pdgs_file = file_config.get("pdgs")
    manual_pdgs = (
        list(pdgs_cli)
        if pdgs_cli is not None
        else parse_pdg_tokens(pdgs_file)
    )

    mode_value = config_value(args.mode, file_config, "mode", None)
    if mode_value is None:
        mode = "pdg" if manual_pdgs else "combined"
    else:
        mode = str(mode_value).strip().lower()

    if mode not in {"combined", "pdg"}:
        raise ValueError("mode debe ser 'combined' o 'pdg'.")

    xf = float(config_value(args.xf, file_config, "xf", 25.0))
    max_delta = float(config_value(args.max_delta, file_config, "max_delta", 0.25))
    min_relative_weight = float(
        config_value(args.min_relative_weight, file_config, "min_relative_weight", 1.0e-3)
    )
    width_tolerance = float(
        config_value(args.width_tolerance, file_config, "width_tolerance", 1.0e-30)
    )
    task = str(config_value(args.task, file_config, "task", "relic")).strip().lower()
    task_aliases = {
        "relic_density": "relic",
        "relic-density": "relic",
        "density": "relic",
        "sigma": "sigmav",
        "sigma_v": "sigmav",
        "sigma-v": "sigmav",
    }
    task = task_aliases.get(task, task)

    if task not in {"relic", "sigmav"}:
        raise ValueError("task debe ser 'relic' o 'sigmav'.")

    if xf <= 0.0:
        raise ValueError("--xf debe ser positivo.")
    if max_delta < 0.0:
        raise ValueError("--max-delta no puede ser negativo.")
    if min_relative_weight < 0.0:
        raise ValueError("--min-relative-weight no puede ser negativo.")

    verbose_value = args.verbose
    if verbose_value is None and "verbose" in file_config:
        verbose_value = parse_bool(file_config["verbose"], "verbose")

    if verbose_value is None:
        if sys.stdin.isatty():
            verbose = yes_no("¿Desea ver la interfaz detallada?", default=True)
        else:
            verbose = False
    else:
        verbose = bool(verbose_value)

    backup_value = args.backup
    if backup_value is None and "backup" in file_config:
        backup_value = parse_bool(file_config["backup"], "backup")
    backup = bool(backup_value) if backup_value is not None else False

    cards_dir_value = config_value(args.cards_dir, file_config, "cards_dir", None)
    cards_dir: Optional[Path] = None
    if cards_dir_value is not None:
        raw_cards_dir = Path(str(cards_dir_value)).expanduser()
        if not raw_cards_dir.is_absolute() and config_dir is not None and args.cards_dir is None:
            cards_dir = (config_dir / raw_cards_dir).resolve()
        else:
            cards_dir = raw_cards_dir.resolve()
        if not cards_dir.is_dir():
            raise FileNotFoundError(f"No existe el directorio de param_cards: {cards_dir}")

    param_card_value: object = args.param_card
    if param_card_value is None:
        param_card_value = file_config.get("param_card")
    if param_card_value is None:
        raise ValueError(
            "Debe proporcionar el param_card como argumento o mediante "
            "param_card=... en --input-file. Puede añadir --cards-dir/cards_dir=... "
            "cuando solo quiera escribir el nombre de la card."
        )
    param_card = resolve_param_card_path(
        param_card_value,
        cards_dir=cards_dir,
        config_dir=config_dir,
    )

    subprocesses_dir = resolve_runtime_path(
        config_value(args.subprocesses, file_config, "subprocesses", None),
        script_root / "SubProcesses",
    )
    output_dir = resolve_runtime_path(
        config_value(args.output, file_config, "output", None),
        script_root / "effective_SubProcesses",
    )
    backup_root = resolve_runtime_path(
        config_value(args.backup_dir, file_config, "backup_dir", None),
        script_root / "back_up",
    )
    build_dir_value = config_value(args.build_dir, file_config, "build_dir", None)
    explicit_kerrigan = config_value(args.kerrigan, file_config, "kerrigan", None)
    kerrigan, cmake_build_dir = resolve_cmake_kerrigan(
        script_root=script_root,
        explicit_kerrigan=explicit_kerrigan,
        build_dir_value=build_dir_value,
        config_dir=config_dir,
    )

    mg5_output_value = config_value(args.mg5_output, file_config, "mg5_output", None)
    mg5_output = infer_mg5_output(subprocesses_dir, mg5_output_value)

    physics_output_value = config_value(
        args.physics_output_root,
        file_config,
        "physics_output_root",
        None,
    )
    physics_output_root = (
        None
        if physics_output_value is None
        else Path(str(physics_output_value)).expanduser().resolve()
    )

    if not param_card.is_file():
        raise FileNotFoundError(f"No existe el param_card: {param_card}")
    if not subprocesses_dir.is_dir():
        raise FileNotFoundError(f"No existe la carpeta SubProcesses: {subprocesses_dir}")

    read_particles = read_param_card(param_card)

    dark_pdgs_value = config_value(args.dark_pdgs, file_config, "dark_pdgs", None)
    requested_dark_pdgs = parse_dark_pdgs(
        None if dark_pdgs_value is None else str(dark_pdgs_value)
    )
    dark_particles = get_dark_particles(read_particles, requested_dark_pdgs)

    candidate_config = config_value(args.candidate, file_config, "candidate", None)

    if mode == "pdg":
        if not manual_pdgs:
            if not sys.stdin.isatty():
                raise ValueError(
                    "Modo PDG sin --pdgs y sin pdgs=... en el archivo de entrada."
                )
            manual_pdgs = parse_pdg_tokens(
                input(
                    "Ingrese los PDG (primero candidato; después coaniquiladores): "
                )
            )

        if not manual_pdgs:
            raise ValueError("El modo PDG necesita al menos el PDG del candidato.")

        manual_pdgs = unique_pdgs(manual_pdgs)
        candidate = particle_by_pdg(read_particles, manual_pdgs[0])

        if candidate_config is not None:
            candidate_from_flag = resolve_candidate(str(candidate_config), read_particles)
            if candidate_from_flag.pdg != candidate.pdg:
                raise ValueError(
                    f"--candidate/input candidate={candidate_from_flag.pdg} no coincide "
                    f"con el primer PDG manual ({candidate.pdg})."
                )

    else:
        candidate_query = candidate_config
        if candidate_query is None:
            if not sys.stdin.isatty():
                raise ValueError(
                    "Combined mode necesita --candidate o candidate=... en el input file."
                )
            candidate_query = input("\nIngrese el nombre, alias o PDG del candidato: ")
        candidate = resolve_candidate(str(candidate_query), read_particles)

    warnings = validate_candidate(
        candidate=candidate,
        dark_particles=dark_particles,
        allow_unstable=args.allow_unstable_candidate,
        allow_nonlightest=args.allow_nonlightest_candidate,
        width_tolerance=width_tolerance,
    )

    if verbose:
        print_particle_table(read_particles)
        print_candidate_summary(candidate)
        for warning in warnings:
            print(f"ADVERTENCIA: {warning}")

    if mode == "combined":
        # ORIGINAL COMBINED LOGIC: unchanged except that xf is now dynamic.
        active_pdgs, decisions = build_effective_dark_sector(
            candidate=candidate,
            dark_particles=dark_particles,
            x_ref=xf,
            max_delta=max_delta,
            min_relative_weight=min_relative_weight,
        )

        records, unparsed = scan_processes(
            subprocesses_dir=subprocesses_dir,
            dark_particles=dark_particles,
            candidate=candidate,
            active_pdgs=active_pdgs,
            mode="combined",
        )

        manual_decisions: list[ManualPDGDecision] = []
        mode_warnings: list[str] = []

        if verbose:
            print_dark_sector_table(
                decisions,
                x_ref=xf,
                max_delta=max_delta,
                min_relative_weight=min_relative_weight,
            )
            print_selection_summary(records, unparsed, "combined")

    else:
        # Manual mode intentionally bypasses the combined Delta/weight filter.
        records, unparsed, manual_decisions, mode_warnings = scan_processes_pdg(
            subprocesses_dir=subprocesses_dir,
            dark_particles=dark_particles,
            candidate=candidate,
            requested_pdgs=manual_pdgs,
        )

        active_pdgs = {candidate.pdg}
        active_pdgs.update(
            decision.pdg for decision in manual_decisions if decision.included
        )
        decisions = build_manual_report_decisions(
            candidate,
            dark_particles,
            [candidate.pdg] + [
                decision.pdg for decision in manual_decisions if decision.included
            ],
            xf,
        )

        if verbose:
            print_manual_pdg_table(candidate, manual_pdgs, manual_decisions)
            for warning in mode_warnings:
                print(f"ADVERTENCIA: {warning}")
            print_selection_summary(records, unparsed, "pdg")

    selected_count = sum(record.selected for record in records)
    if selected_count == 0:
        print(
            "No se seleccionó ningún proceso. Revise el candidato, los PDG o "
            "la correspondencia con SubProcesses.",
            file=sys.stderr,
        )
        return 2

    direct_count = sum(
        record.selected and record.category == "candidate_only"
        for record in records
    )
    if direct_count == 0:
        message = (
            "No se encontró ningún canal candidato+candidato en la selección."
        )
        if verbose:
            print(f"ADVERTENCIA: {message}")

    if not verbose:
        xf_label = f"{xf:g}" if mode == "combined" else "manual/no-filter"
        print(
            f"[{mode}] candidato={candidate.name}({candidate.pdg}) | "
            f"procesos={selected_count} | task={task} | xf={xf_label}"
        )
        for warning in warnings:
            print(f"ADVERTENCIA: {warning}")
        for warning in mode_warnings:
            print(f"ADVERTENCIA: {warning}")

    if verbose and not args.yes:
        review = yes_no(
            f"Se seleccionaron {selected_count} procesos. ¿Desea revisar cuáles son?"
        )
        if review:
            print_selected_processes(records)

    if verbose and unparsed:
        print(
            f"\nNota: {len(unparsed)} carpetas no pudieron interpretarse. "
            "Se guardarán en el reporte para revisar aliases."
        )

    if args.dry_run:
        print("\nDry run: no se copió, eliminó, respaldó ni ejecutó ningún cálculo.")
        return 0

    if verbose and not args.yes:
        proceed = yes_no(
            f"Se recreará '{output_dir.name}' y se copiarán "
            f"{selected_count} carpetas desde SubProcesses. ¿Continuar?"
        )
        if not proceed:
            print(
                "Operación cancelada. SubProcesses y la salida existente "
                "no fueron modificados."
            )
            return 0

    backup_destination = copy_selected_processes_v2(
        subprocesses_dir=subprocesses_dir,
        output_dir=output_dir,
        records=records,
        backup=backup,
        backup_root=backup_root,
        verbose=verbose,
    )

    settings = {
        "xf": xf,
        "x_ref": xf,
        "max_delta": max_delta,
        "min_relative_weight": min_relative_weight,
        "width_tolerance": width_tolerance,
        "dark_pdgs": [particle.pdg for particle in dark_particles],
        "manual_pdgs": manual_pdgs if mode == "pdg" else [],
        "task": task,
        "verbose": verbose,
        "backup": backup,
        "cards_dir": None if cards_dir is None else str(cards_dir),
        "cmake_build_dir": str(cmake_build_dir),
        "kerrigan_runtime": str(kerrigan),
        "mg5_output": None if mg5_output is None else str(mg5_output),
        "physics_output_root": (
            None if physics_output_root is None else str(physics_output_root)
        ),
    }

    json_report, csv_report = write_reports(
        output_dir=output_dir,
        param_card=param_card,
        candidate=candidate,
        mode=mode,
        active_pdgs=active_pdgs,
        decisions=decisions,
        records=records,
        unparsed=unparsed,
        settings=settings,
    )

    if verbose:
        print("\nSelección completada")
        print("-" * 72)
        print(f"Fuente sin modificar : {subprocesses_dir}")
        print(f"Carpeta creada       : {output_dir}")
        print(f"Procesos copiados    : {selected_count}")
        print(f"Reporte JSON         : {json_report}")
        print(f"Reporte CSV          : {csv_report}")
        if backup_destination is not None:
            print(f"Backup anterior      : {backup_destination}")
        elif backup:
            print("Backup anterior      : no había selección previa que respaldar")
        print("-" * 72)

    selector_regex = bash_regex_for_selected_processes(records)

    # Both tasks now use the same CMake-configured Kerrigan runtime.
    # Kerrigan itself decides whether to execute the full density branch or
    # stop after sigmaV/TOTALS_T.  The selector never calls mind_master.sh.
    run_kerrigan(
        kerrigan=kerrigan,
        build_dir=cmake_build_dir,
        param_card=param_card,
        task=task,
        mode=mode,
        candidate=candidate,
        selector_regex=selector_regex,
        selection_report=json_report,
        mg5_output=mg5_output,
        physics_output_root=physics_output_root,
        verbose=verbose,
    )

    if not verbose:
        print("Cálculo iniciado/completado correctamente con la selección filtrada.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print(
            f"ERROR: el proceso externo terminó con código {error.returncode}.",
            file=sys.stderr,
        )
        raise SystemExit(error.returncode or 1)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
