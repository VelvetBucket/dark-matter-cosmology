#!/usr/bin/env python3
"""
UI2 - Scotogenic subprocess selector and physics orchestrator.

Normal use is intentionally short.  UI2 auto-discovers the selected model
layout (param_cards, SubProcesses, Build/build, effective_SubProcesses and
back_up) relative to this file/project, so those paths do not need to be typed
on every run.  When more than one model layout exists, choose it with
--model 1 / --model 2 (or interactively).  A parameter card is then resolved
inside that SAME model layout; UI2 rejects a card from another model root to
avoid mixing model-1 inputs with model-2 SubProcesses.

Selection modes:

1. combined
   Performs a THERMAL PRESELECTION of possible coannihilators.  x_f=m_DM/T
   defaults to 25 and enters the equilibrium-density ratio

       n_i^eq / n_DM^eq
         ~= (g_i/g_DM) (m_i/m_DM)^(3/2) exp[-x_f Delta_i].

   A state must pass both the relative mass-splitting cut and the equilibrium
   abundance/Boltzmann-suppression cut.  This is deliberately only a
   preselection: a state that passes these cuts is not guaranteed to matter
   dynamically.  Its actual importance requires sigma-v information.

2. pdg
   Manual selection.  The first PDG is the dark-matter candidate and later
   PDGs request candidate-partner coannihilation channels.

After selection, both relic-density and sigma-v tasks are delegated to the
CMake-generated Kerrigan.sh runtime.  --task sigmav computes sigmaV/TOTALS_T
for the thermally/manual selected set; UI2 does NOT currently use sigma-v as an
automatic pruning gate because this file has no validated per-process sigma-v
contribution parser/threshold.  Therefore the report explicitly distinguishes
thermal preselection from final dynamical relevance.

The external calculation is executed with its working directory set to the
resolved Build/build directory.  UI2 prints that exact directory before and
after the run so messages such as 'This directory ...' from run_madgraph are
unambiguous.
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

DEFAULT_XF = 25.0
DEFAULT_MAX_DELTA = 0.25
DEFAULT_MIN_RELATIVE_WEIGHT = 1.0e-3
DEFAULT_WIDTH_TOLERANCE = 1.0e-30

MODEL_DIR_PATTERNS: dict[str, tuple[str, ...]] = {
    "1": ("Model1", "model1", "Model_1", "model_1", "Modelo1", "modelo1", "Modelo_1", "modelo_1"),
    "2": ("Model2", "model2", "Model_2", "model_2", "Modelo2", "modelo2", "Modelo_2", "modelo_2"),
}

PARAM_CARD_DIR_NAMES: tuple[str, ...] = (
    "param_cards", "ParamCards", "paramcards", "cards", "Cards"
)
BUILD_DIR_NAMES: tuple[str, ...] = ("Build", "build")


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


@dataclass(frozen=True)
class RuntimeLayout:
    model_label: str
    model_root: Path
    cards_dir: Optional[Path]
    subprocesses_dir: Path
    output_dir: Path
    backup_root: Path
    build_dir: Optional[Path]
    strict_model_binding: bool
    # The CMake layout stores inputs and generated standalone code in
    # different model-specific directories.
    mg5_output: Optional[Path] = None


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
    suffix = " [Y/n]: " if default else " [y/N]: "
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
        raise ValueError(f"No particles were found in Block MASS of {path}")

    return list(particles.values())


def print_particle_table(read_particles: list[Particle]) -> None:
    print("\nParticles read from the parameter card:")
    print("-" * 78)
    print(f"{'PDG':>8}  {'name':<14} {'mass [GeV]':>18} {'decay width [GeV]':>18}")
    print("-" * 78)

    for particle in read_particles:
        width_text = (
            "not available"
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
        raise ValueError(f"PDG code {requested_pdg} was not found in Block MASS.")

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
            f"Could not identify '{query}'. "
            "Use a particle name from the parameter card, a folder alias, or a PDG code."
        )

    if len(matches) > 1:
        options = ", ".join(f"{p.name} (PDG {p.pdg})" for p in matches)
        raise ValueError(f"Ambiguous particle name. Matches: {options}")

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
                "The following dark-sector PDG codes are missing from the parameter card: "
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
            f"Candidate {candidate.name} has an invalid mass: "
            f"{candidate.mass}"
        )

    if candidate.pdg not in SCOTOGENIC_FOLDER_ALIASES:
        raise ValueError(
            f"No SubProcesses alias is configured for "
            f"{candidate.name} (PDG {candidate.pdg})."
        )

    if candidate.width is None:
        warnings.append(
            "The candidate's decay width is missing from the parameter card; "
            "its stability could not be verified."
        )
    elif abs(candidate.width) > width_tolerance:
        message = (
            f"Candidate {candidate.name} has a nonzero decay width: "
            f"Gamma={candidate.width:.8e} GeV. "
            "A dark matter candidate must be stable."
        )
        if allow_unstable:
            warnings.append(message)
        else:
            raise ValueError(
                message
                + " Use --allow-unstable-candidate only for an intentional test."
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
            f"There are dark-sector particles lighter than "
            f"{candidate.name}: {details}."
        )
        if allow_nonlightest:
            warnings.append(message)
        else:
            raise ValueError(
                message
                + " Use --allow-nonlightest-candidate only for an intentional test."
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
            reason = "thermal preselection passed; sigmaV relevance pending"
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
    print("\nDark-Sector Thermal Preselection")
    print(
        f"x_ref={x_ref:g}, max_delta={max_delta:g}, "
        f"min_relative_weight={min_relative_weight:g}"
    )
    print("-" * 116)
    print(
        f"{'PDG':>8}  {'name':<10} {'mass [GeV]':>16} "
        f"{'Delta':>13} {'relative eq. weight':>19} "
        f"{'preselected.':>10}  reason"
    )
    print("-" * 116)

    for decision in decisions:
        active_text = "yes" if decision.included else "no"
        print(
            f"{decision.pdg:>8d}  "
            f"{decision.name:<10} "
            f"{decision.mass:>16.8e} "
            f"{decision.delta_mass:>13.5e} "
            f"{decision.relative_eq_weight:>19.5e} "
            f"{active_text:>10}  "
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
                raise ValueError(f"Duplicate alias in configuration: {alias}")
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
            raise ValueError(f"Unknown selection mode: {mode}")

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

    print("\nSelection Summary")
    print("-" * 72)
    print(f"Mode                         : {mode}")
    print(f"Directories scanned       : {len(records) + len(unparsed)}")
    print(f"Directories parsed    : {len(records)}")
    print(f"Unparsed directories : {len(unparsed)}")
    print(f"Selected directories    : {len(selected)}")

    for category in (
        "candidate_only",
        "candidate_coannihilation",
        "coannihilator_pair",
    ):
        print(f"  {category:<28}: {categories.get(category, 0)}")

    print("-" * 72)


def print_selected_processes(records: list[ProcessRecord]) -> None:
    selected = [record for record in records if record.selected]

    print("\nSelected Processes:")
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
        raise ValueError("No processes were selected for copying.")

    source_resolved = subprocesses_dir.resolve()
    output_resolved = output_dir.resolve()

    if source_resolved == output_resolved:
        raise ValueError(
            "The output directory cannot be the same as SubProcesses."
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
                f"\rCopying {index}/{total}: {record.directory}",
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
            f"Copy operation failed. Source directory {subprocesses_dir} was not modified.",
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
        f"Invalid Boolean value for {field_name}: {value!r}. "
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
            raise ValueError(f"Invalid PDG code in input: {token!r}") from exc

    return pdgs


def load_input_file(path: Path) -> dict[str, object]:
    """
    Read either:

        1012 1014 1001

    or a key/value block such as:

        model = 1
        param_card = param_card_model1.dat
        mode = pdg
        pdgs = 1012 1014 1001
        xf = 28
        verbose = yes
        backup = no
        task = relic

    Normal UI2 use no longer needs cards_dir/SubProcesses/Build paths when
    they follow the model layout. Advanced path keys remain available as
    explicit overrides.

    CLI arguments override values from this file.
    """
    if not path.is_file():
        raise FileNotFoundError(f"Input file does not exist: {path}")

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
        "model_id": "model",
        "modelo": "model",
        "root": "project_root",
        "project-root": "project_root",
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
                    f"Unrecognized line {line_number} in {path}: {stripped!r}. "
                    "Use key=value or a list of PDG codes."
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


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _first_existing_dir(root: Path, relative_candidates: tuple[str, ...]) -> Optional[Path]:
    for relative in relative_candidates:
        candidate = (root / relative).resolve()
        if candidate.is_dir():
            return candidate
    return None


def _looks_like_model_root(root: Path) -> bool:
    if not root.is_dir():
        return False
    has_subprocesses = any(
        (root / rel).is_dir()
        for rel in ("SubProcesses", "MG5/SubProcesses", "MadGraph/SubProcesses")
    )
    has_cards = any((root / name).is_dir() for name in PARAM_CARD_DIR_NAMES)
    has_build = any((root / name).is_dir() for name in BUILD_DIR_NAMES)
    return has_subprocesses or (has_cards and has_build)


def _model_root_candidates(project_root: Path, model_value: str) -> list[Path]:
    raw = Path(model_value).expanduser()
    candidates: list[Path] = []
    if raw.is_absolute() or raw.parts and len(raw.parts) > 1:
        candidates.append(raw.resolve())

    names = MODEL_DIR_PATTERNS.get(str(model_value).strip(), (str(model_value).strip(),))
    for base in (project_root, project_root.parent):
        for name in names:
            candidates.append((base / name).resolve())

    result: list[Path] = []
    seen: set[Path] = set()
    for candidate in candidates:
        if candidate in seen:
            continue
        seen.add(candidate)
        if _looks_like_model_root(candidate):
            result.append(candidate)
    return result


def _discover_named_model_roots(project_root: Path) -> list[Path]:
    roots: list[Path] = []
    seen: set[Path] = set()
    for base in (project_root, project_root.parent):
        for names in MODEL_DIR_PATTERNS.values():
            for name in names:
                candidate = (base / name).resolve()
                if candidate in seen:
                    continue
                seen.add(candidate)
                if _looks_like_model_root(candidate):
                    roots.append(candidate)
    return roots


def _choose_interactively(title: str, paths: list[Path]) -> Path:
    print(f"\n{title}")
    for index, path in enumerate(paths, start=1):
        print(f"  {index}. {path}")
    while True:
        answer = input("Select an option by number: ").strip()
        try:
            selected = int(answer)
        except ValueError:
            selected = 0
        if 1 <= selected <= len(paths):
            return paths[selected - 1]
        print("Invalid option.")




def find_cmake_build_dir(
    script_root: Path,
    project_root_value: Optional[object],
    explicit_build_dir: Optional[object],
) -> Optional[Path]:
    """Discover the CMake build tree, never inventing alternate build paths."""
    if explicit_build_dir is not None:
        selected = Path(str(explicit_build_dir)).expanduser().resolve()
        if not (selected / "CMakeCache.txt").is_file():
            raise FileNotFoundError(
                f"--build-dir must contain CMakeCache.txt: {selected}"
            )
        return selected

    project = (
        Path(str(project_root_value)).expanduser().resolve()
        if project_root_value is not None else script_root.resolve().parent
    )
    cwd = Path.cwd().resolve()
    candidates = [
        os.environ.get("BUILD_DIR"),
        os.environ.get("SCOTOGENIC_BUILD_DIR"),
        script_root.parent,
        script_root.parent / "build",
        project,
        project / "build",
        cwd,
        cwd / "build",
    ]
    checked = set()
    for value in candidates:
        if not value:
            continue
        candidate = Path(str(value)).expanduser().resolve()
        if candidate in checked:
            continue
        checked.add(candidate)
        if (candidate / "CMakeCache.txt").is_file():
            return candidate
    return None


def discover_cmake_model_layout(
    build_dir: Path,
    model_value: Optional[object],
    explicit_mg5_output: Optional[object],
) -> Optional[RuntimeLayout]:
    """Use CMake's <build>/input and MadGraph's generation manifest/pointer.

    An explicit --model selects a variant, overriding the last-model pointer;
    an explicit --mg5-output can select a different standalone for that variant.
    Nothing is inferred from the MG5 *installation* directory.
    """
    input_dir = (build_dir / "input").resolve()
    output_root = (build_dir / "output").resolve()
    pointer = build_dir / "generated" / "current_mg5_output.json"
    requested_variant = None if model_value is None else str(model_value).strip()
    if requested_variant:
        # Absolute model directories from the legacy layout remain handled by
        # discover_runtime_layout. Only plain variant names enter this path.
        raw = Path(requested_variant).expanduser()
        if raw.is_absolute() or len(raw.parts) > 1:
            if raw.resolve().parent == input_dir:
                requested_variant = raw.name
            else:
                return None
        if not (input_dir / requested_variant).is_dir():
            return None

    if explicit_mg5_output is not None:
        output = Path(str(explicit_mg5_output)).expanduser().resolve()
    elif requested_variant:
        base = output_root / requested_variant
        available = sorted(
            child.resolve() for child in base.iterdir()
            if child.is_dir() and (child / "SubProcesses").is_dir()
            and (child / "src").is_dir()
        ) if base.is_dir() else []
        if len(available) != 1:
            raise ValueError(
                f"Expected exactly one MG5 standalone output for model "
                f"{requested_variant!r} in {base}; found {len(available)}. "
                "Use --mg5-output /absolute/path/to/standalone to disambiguate."
            )
        output = available[0]
    elif pointer.is_file():
        try:
            info = json.loads(pointer.read_text(encoding="utf-8"))
            output = Path(info["mg5_output"]).expanduser().resolve()
            pointed_subprocesses = Path(info["subprocesses"]).expanduser().resolve()
            if pointed_subprocesses != (output / "SubProcesses").resolve():
                raise ValueError("pointer SubProcesses does not match its model output")
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise ValueError(f"Invalid MG5 generation pointer {pointer}: {error}") from error
    else:
        # Legacy Model1/2 discovery remains available if a CMake model has
        # not yet been generated; do not infer the first arbitrary model.
        if not requested_variant and explicit_mg5_output is None:
            return None
        raise FileNotFoundError(
            "No MG5 output found. Generate the model first with "
            "run_madgraph.py or specify --mg5-output."
        )

    if not (output / "SubProcesses").is_dir() or not (output / "src").is_dir():
        raise FileNotFoundError(
            f"MG5 output is missing SubProcesses/ or src/: {output}"
        )
    manifest_file = output / "generation_manifest.json"
    if not manifest_file.is_file():
        raise FileNotFoundError(
            f"MG5 generation manifest is missing: {manifest_file}. "
            "Automated CMake model binding requires a manifest; use the legacy "
            "manual layout for older packages."
        )
    try:
        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        variant = manifest.get("variant")
        manifest_build = manifest.get("cmake_build_dir")
        manifest_output = manifest.get("output")
        if not isinstance(variant, str) or not variant:
            raise ValueError("manifest does not identify a model variant")
        if manifest_build and Path(manifest_build).resolve() != build_dir.resolve():
            raise ValueError("manifest belongs to a different CMake build")
        if manifest_output and Path(manifest_output).resolve() != output:
            raise ValueError("manifest output path does not match selected output")
        if requested_variant and requested_variant != variant:
            raise ValueError(
                f"--model {requested_variant!r} conflicts with MG5 output "
                f"variant {variant!r}"
            )
        variant_dir = (input_dir / variant).resolve()
        if not variant_dir.is_dir():
            raise FileNotFoundError(f"Model input directory does not exist: {variant_dir}")
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise ValueError(f"Invalid generation manifest {manifest_file}: {error}") from error

    cards_dir = _first_existing_dir(variant_dir, PARAM_CARD_DIR_NAMES)
    return RuntimeLayout(
        model_label=variant,
        model_root=variant_dir,
        cards_dir=cards_dir,
        subprocesses_dir=(output / "SubProcesses").resolve(),
        output_dir=(output / "effective_SubProcesses").resolve(),
        backup_root=(output / "back_up").resolve(),
        build_dir=build_dir,
        strict_model_binding=True,
        mg5_output=output,
    )


def discover_runtime_layout(
    script_root: Path,
    model_value: Optional[object],
    project_root_value: Optional[object],
    build_dir_hint: Optional[object] = None,
    mg5_output_hint: Optional[object] = None,
) -> RuntimeLayout:
    """Resolve CMake's model layout first, keeping the legacy UI layout as fallback."""
    cmake_build = find_cmake_build_dir(
        script_root=script_root,
        project_root_value=project_root_value,
        explicit_build_dir=build_dir_hint,
    )
    if cmake_build is not None:
        cmake_layout = discover_cmake_model_layout(
            build_dir=cmake_build,
            model_value=model_value,
            explicit_mg5_output=mg5_output_hint,
        )
        if cmake_layout is not None:
            return cmake_layout

    project_root = (
        Path(str(project_root_value)).expanduser().resolve()
        if project_root_value is not None
        else script_root.resolve()
    )

    strict_binding = model_value is not None
    if model_value is not None:
        matches = _model_root_candidates(project_root, str(model_value))
        if len(matches) == 0:
            expected = ", ".join(MODEL_DIR_PATTERNS.get(str(model_value), (str(model_value),)))
            raise FileNotFoundError(
                f"Could not locate model {model_value!r}. "
                f"Searched for directories matching: {expected} under {project_root} and {project_root.parent}. "
                "You may also provide the model's directory directly using --model /path/to/model."
            )
        if len(matches) > 1:
            if not sys.stdin.isatty():
                raise ValueError(
                    "Multiple compatible model roots were found for --model; provide an explicit path. "
                    + "; ".join(str(path) for path in matches)
                )
            model_root = _choose_interactively("Multiple model roots were found:", matches)
        else:
            model_root = matches[0]
        model_label = str(model_value)
    else:
        # If the script already lives in a complete model root, keep the legacy
        # one-folder workflow.  Otherwise detect Model1/Model2 and force a choice
        # when both are present so cards and SubProcesses cannot be mixed silently.
        if _looks_like_model_root(script_root):
            model_root = script_root.resolve()
            model_label = model_root.name
        else:
            discovered = _discover_named_model_roots(project_root)
            if len(discovered) == 1:
                model_root = discovered[0]
                model_label = model_root.name
                strict_binding = True
            elif len(discovered) > 1:
                if not sys.stdin.isatty():
                    raise ValueError(
                        "Multiple models are available. Use --model 1 or --model 2 "
                        "to explicitly select a model and prevent parameter cards from different models from being mixed."
                    )
                model_root = _choose_interactively(
                    "UI2 detected multiple models. Select one to keep the parameter card and SubProcesses linked to the same model:",
                    discovered,
                )
                model_label = model_root.name
                strict_binding = True
            else:
                model_root = script_root.resolve()
                model_label = model_root.name

    cards_dir = _first_existing_dir(model_root, PARAM_CARD_DIR_NAMES)
    subprocesses_dir = _first_existing_dir(
        model_root,
        ("SubProcesses", "MG5/SubProcesses", "MadGraph/SubProcesses"),
    )
    if subprocesses_dir is None:
        subprocesses_dir = (model_root / "SubProcesses").resolve()

    build_dir = _first_existing_dir(model_root, BUILD_DIR_NAMES)
    if build_dir is None:
        # A shared project Build is allowed; unlike the param_card, it does not
        # define the model physics input.
        build_dir = _first_existing_dir(model_root.parent, BUILD_DIR_NAMES)

    output_dir = (subprocesses_dir.parent / "effective_SubProcesses").resolve()
    backup_root = (subprocesses_dir.parent / "back_up").resolve()

    return RuntimeLayout(
        model_label=model_label,
        model_root=model_root,
        cards_dir=cards_dir,
        subprocesses_dir=subprocesses_dir,
        output_dir=output_dir,
        backup_root=backup_root,
        build_dir=build_dir,
        strict_model_binding=strict_binding,
    )


def list_param_cards(cards_dir: Path) -> list[Path]:
    preferred = sorted(cards_dir.glob("param_card*.dat"))
    if preferred:
        return [path.resolve() for path in preferred if path.is_file()]
    broader = sorted(cards_dir.glob("*.dat"))
    return [path.resolve() for path in broader if path.is_file()]


def resolve_ui2_param_card(
    requested: Optional[object],
    layout: RuntimeLayout,
    explicit_cards_dir: Optional[Path],
    config_dir: Optional[Path],
) -> Path:
    cards_dir = explicit_cards_dir or layout.cards_dir

    if requested is None:
        if cards_dir is None or not cards_dir.is_dir():
            raise ValueError(
                "UI2 could not find a parameter-card directory in the selected model. "
                "Provide a parameter-card name or path, or use the advanced --cards-dir option."
            )
        cards = list_param_cards(cards_dir)
        if not cards:
            raise FileNotFoundError(f"No .dat parameter cards were found in {cards_dir}")
        if len(cards) == 1:
            card = cards[0]
        elif sys.stdin.isatty():
            card = _choose_interactively(
                f"Found {len(cards)} parameter cards in {cards_dir}:",
                cards,
            )
        else:
            raise ValueError(
                "Multiple parameter cards are available. Specify a name or path for non-interactive execution."
            )
    else:
        card = resolve_param_card_path(requested, cards_dir=cards_dir, config_dir=config_dir)

    if layout.strict_model_binding and not _is_within(card, layout.model_root):
        # Explicit external cards support scans; never accept a card from a
        # different configured CMake model variant.
        build_dir = layout.build_dir
        known_variants = (build_dir / "input").resolve() if build_dir else None
        if (known_variants is not None and _is_within(card, known_variants)) or requested is None:
            raise ValueError(
                "MODEL_PARAM_CARD_MISMATCH: The selected parameter card belongs "
                f"to another model or was inferred outside {layout.model_root}: {card}."
            )
        print(
            f"WARNING: Explicit external parameter card {card} is not inside "
            f"the selected model {layout.model_root}. Verify its physics consistency.",
            file=sys.stderr,
        )

    return card.resolve()


def print_runtime_layout(layout: RuntimeLayout, param_card: Path, build_dir: Path) -> None:
    print("\nResolved UI2 Layout")
    print("-" * 88)
    print(f"Model            : {layout.model_label}")
    print(f"Model root         : {layout.model_root}")
    print(f"param_card         : {param_card}")
    print(f"SubProcesses       : {layout.subprocesses_dir}")
    print(f"Build              : {build_dir}")
    print(f"effective output   : {layout.output_dir}")
    print("Binding card/model : " + ("STRICT" if layout.strict_model_binding else "legacy/local"))
    print("-" * 88)


def print_combined_selection_criteria(
    xf: float,
    max_delta: float,
    min_relative_weight: float,
) -> None:
    print("\nCoannihilator Preselection Criteria (combined mode)")
    print("-" * 100)
    print(
        f"1) Mass proximity: Delta_i=(m_i-m_DM)/m_DM <= {max_delta:g}. "
        "This excludes states with excessively large mass splittings."
    )
    print(
        "2) Thermal suppression / equilibrium abundance: "
        "n_i^eq/n_DM^eq = (g_i/g_DM)(1+Delta_i)^(3/2) exp[-x_f Delta_i]."
    )
    print(
        f"   UI2 uses x_f={xf:g} and requires "
        f"n_i^eq/n_DM^eq >= {min_relative_weight:g}. "
        "Since x_f=m_DM/T, a larger x_f implies stronger Boltzmann "
        "suppression for the same mass splitting."  
    )
    print(
        "3) Dynamical relevance: requires sigma-v information. "
        "UI2 does NOT currently use sigma-v as an automatic selection criterion; --task sigmav calculates it AFTER thermal preselection. "
    )
    print(
        "   Therefore, 'included' means thermally plausible, not a dynamically significant coannihilation channel. "
        "A validated per-process contribution calculation and threshold "
        "are required for sigma-v-based pruning."
    )
    print("-" * 100)


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
    raise ValueError(f"PDG code {pdg} was not found in Block MASS of the parameter card.")


def print_candidate_summary(candidate: Particle) -> None:
    print("\nIdentified Dark Matter Candidate")
    print("-" * 72)
    print(f"Name          : {candidate.name}")
    print(f"PDG             : {candidate.pdg}")
    print(f"Mass            : {candidate.mass:.8e} GeV")
    print(
        "Decay width           : "
        + (
            "not available"
            if candidate.width is None
            else f"{candidate.width:.8e} GeV"
        )
    )
    print(
        "Folder aliases: "
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
        raise ValueError("PDG mode requires at least the candidate's PDG code.")

    candidate_pdg = requested_pdgs[0]
    partner_pdgs = [pdg for pdg in unique_pdgs(requested_pdgs[1:]) if pdg != candidate_pdg]

    # Ensure every requested initial-state particle can be mapped to a
    # SubProcesses token.
    for pdg in [candidate_pdg] + partner_pdgs:
        particle = particle_by_pdg(dark_particles, pdg)
        if pdg not in SCOTOGENIC_FOLDER_ALIASES:
            raise ValueError(
                f"{pdg} ({particle.name}) exists in the parameter card but has no configured initial-state "
                "alias for SubProcesses."
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
            f"No {candidate_pdg}+{candidate_pdg} channel exists in SubProcesses."
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
                f"{candidate.pdg} ({candidate.name}) can not interact with "
                f"{pdg} ({partner.name}) in the current SubProcesses inventory "
                "SubProcesses: No generated initial-state channel was found for this initial process."
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
    print("\nPDG Mode Validation")
    print("-" * 118)
    print(
        "Rule: the first PDG identifies the dark matter candidate. All candidate-candidate annihilation channels are included, "
        "along with the requested candidate-partner coannihilation channels."
    )
    print(f"Input PDGs: {' '.join(map(str, requested_pdgs))}")
    print(f"Candidate: {candidate.pdg} ({candidate.name})")
    print("-" * 118)
    print(
        f"{'PDG':>8}  {'name':<10} {'mass [GeV]':>16} "
        f"{'Delta':>13} {'channels':>10} {'valid':>8}  reason"
    )
    print("-" * 118)

    if not decisions:
        print("No additional coannihilators were requested; only candidate-candidate annihilation channels will be included.")
    else:
        for decision in decisions:
            valid_text = "yes" if decision.included else "no"
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
        raise ValueError("No processes were selected for copying.")

    source_resolved = subprocesses_dir.resolve()
    output_resolved = output_dir.resolve()
    if source_resolved == output_resolved:
        raise ValueError("The output directory cannot be the same as SubProcesses.")

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
                    f"\rCopying {index}/{total}: {record.directory}",
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
            f"Copy operation failed. Source directory {subprocesses_dir} was not modified.",
            file=sys.stderr,
        )
        raise


def bash_regex_for_selected_processes(records: list[ProcessRecord]) -> str:
    names = sorted(record.directory for record in records if record.selected)
    if not names:
        raise ValueError("No processes were selected to construct the subprocess filter.")

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
        raise FileNotFoundError(f"Parameter card does not exist: {candidate}")

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
        f"Could not locate parameter card '{raw}'. Paths checked:\n  - {tried}"
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
                script_root / "Build" / "scripts" / "Kerrigan.sh",
                script_root / "build" / "scripts" / "Kerrigan.sh",
                script_root.parent / "Build" / "scripts" / "Kerrigan.sh",
                script_root.parent / "build" / "scripts" / "Kerrigan.sh",
                script_root / "../Build/scripts/Kerrigan.sh",
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

    tried = "\n  - ".join(str(path) for path in checked) or "(no candidate paths)"
    raise FileNotFoundError(
        "Could not find a Kerrigan.sh script generated by CMake. "
        "The selector no longer executes Kerrigan.sh.in or mind_master.sh directly.\n"
        "Run CMake and/or provide --build-dir /path/to/build or --kerrigan "
        "/path/to/build/scripts/Kerrigan.sh.\n"
        f"Paths checked:\n  - {tried}"
    )


def infer_mg5_output(subprocesses_dir: Path, explicit_value: Optional[object]) -> Optional[Path]:
    if explicit_value is not None:
        path = Path(str(explicit_value)).expanduser().resolve()
        if not path.is_dir():
            raise FileNotFoundError(f"MG5 output directory does not exist: {path}")
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
        raise FileNotFoundError(f"CMake-generated Kerrigan script does not exist: {kerrigan}")

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

    working_dir = (build_dir if build_dir.is_dir() else kerrigan.parent).resolve()

    if verbose:
        print("\nStarting calculation using CMake-generated Kerrigan")
        print(f"Kerrigan runtime   : {kerrigan}")
        print(f"CMake build        : {build_dir}")
        print(f"Card               : {param_card}")
        print(f"Task               : {task}")
        if task == "sigmav":
            print("Pipeline            : sigmaV only (relic-density branch disabled)")
        else:
            print("Pipeline            : relic density")
        print(
            f"Filtered processes : exact selector with "
            f"{selector_regex.count('|') + 1} directories"
        )
        if mg5_output is not None:
            print(f"MG5 output         : {mg5_output}")
        if physics_output_root is not None:
            print(f"Physics output root: {physics_output_root}")

    print(f"Kerrigan/run_madgraph working directory: {working_dir}")
    print(
        "Note: any external message such as 'This directory ...' refers to "
        "the working directory shown above."
    )

    subprocess.run(
        command,
        cwd=working_dir,
        env=environment,
        check=True,
    )

    print("\nExternal calculation completed successfully.")
    print(f"Working directory used by Kerrigan/run_madgraph: {working_dir}")

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
            "Optional parameter-card filename/path. Defaults to the only card in "
            "<build>/input/<variant>/cards, or prompts if multiple cards exist."
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
        "--model",
        default=None,
        help=(
            "CMake model variant (e.g. example), or legacy model selector/root "
            "(1 or 2). Defaults to the last successfully generated MG5 model "
            "from <build>/generated/current_mg5_output.json."
        ),
    )
    parser.add_argument(
        "--project-root",
        type=Path,
        default=None,
        help=(
            "Advanced project root for locating the CMake build or a legacy model layout. "
            "Normally inferred from the source or build UI directory."
        ),
    )

    parser.add_argument(
        "--cards-dir",
        "--param-cards-dir",
        dest="cards_dir",
        type=Path,
        default=None,
        help="Advanced override: parameter-card directory (default: <build>/input/<variant>/cards).",
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
            "Advanced override. x_f=m_DM/T used ONLY by the combined thermal "
            "preselection through exp[-x_f Delta]. In pdg mode it is diagnostic only. "
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
        help=argparse.SUPPRESS,
    )

    parser.add_argument(
        "--task",
        choices=["relic", "sigmav"],
        default=None,
        help="Calculation after selection. Default: sigmav (relic remains paused).",
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
        help="Advanced override: generated SubProcesses directory (model match enforced).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Advanced override: effective_SubProcesses selection directory.",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=None,
        help="Advanced override: backup directory for previous selections.",
    )
    parser.add_argument(
        "--build-dir",
        type=Path,
        default=None,
        help="Advanced override: configured CMake build directory.",
    )
    parser.add_argument(
        "--kerrigan",
        type=Path,
        default=None,
        help="Advanced override: CMake-generated Kerrigan.sh path.",
    )
    parser.add_argument(
        "--mg5-output",
        type=Path,
        default=None,
        help="Advanced override: MadGraph standalone directory with SubProcesses/ and src/.",
    )
    parser.add_argument(
        "--physics-output-root",
        "--run-output",
        dest="physics_output_root",
        type=Path,
        default=None,
        help="Advanced override: Kerrigan physics output directory.",
    )

    parser.add_argument(
        "--width-tolerance",
        type=float,
        default=None,
        help=argparse.SUPPRESS,
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
        raise ValueError("mode must be 'combined' or 'pdg'.")

    xf = float(config_value(args.xf, file_config, "xf", DEFAULT_XF))
    max_delta = float(config_value(args.max_delta, file_config, "max_delta", DEFAULT_MAX_DELTA))
    min_relative_weight = float(
        config_value(args.min_relative_weight, file_config, "min_relative_weight", DEFAULT_MIN_RELATIVE_WEIGHT)
    )
    width_tolerance = float(
        config_value(args.width_tolerance, file_config, "width_tolerance", DEFAULT_WIDTH_TOLERANCE)
    )
    task = str(config_value(args.task, file_config, "task", "sigmav")).strip().lower()
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
        raise ValueError("task must be 'relic' or 'sigmav'.")

    if xf <= 0.0:
        raise ValueError("--xf must be positive.")
    if max_delta < 0.0:
        raise ValueError("--max-delta cannot be negative.")
    if min_relative_weight < 0.0:
        raise ValueError("--min-relative-weight cannot be negative.")

    verbose_value = args.verbose
    if verbose_value is None and "verbose" in file_config:
        verbose_value = parse_bool(file_config["verbose"], "verbose")

    if verbose_value is None:
        if sys.stdin.isatty():
            verbose = yes_no("Would you like to display the detailed interface?", default=True)
        else:
            verbose = False
    else:
        verbose = bool(verbose_value)

    backup_value = args.backup
    if backup_value is None and "backup" in file_config:
        backup_value = parse_bool(file_config["backup"], "backup")
    backup = bool(backup_value) if backup_value is not None else False

    model_value = config_value(args.model, file_config, "model", None)
    project_root_value = config_value(args.project_root, file_config, "project_root", None)
    build_dir_hint = config_value(args.build_dir, file_config, "build_dir", None)
    mg5_output_hint = config_value(args.mg5_output, file_config, "mg5_output", None)
    layout = discover_runtime_layout(
        script_root=script_root,
        model_value=model_value,
        project_root_value=project_root_value,
        build_dir_hint=build_dir_hint,
        mg5_output_hint=mg5_output_hint,
    )

    cards_dir_value = config_value(args.cards_dir, file_config, "cards_dir", layout.cards_dir)
    cards_dir: Optional[Path] = None
    if cards_dir_value is not None:
        raw_cards_dir = Path(str(cards_dir_value)).expanduser()
        if not raw_cards_dir.is_absolute() and config_dir is not None and args.cards_dir is None:
            cards_dir = (config_dir / raw_cards_dir).resolve()
        else:
            cards_dir = raw_cards_dir.resolve()
        if not cards_dir.is_dir():
            raise FileNotFoundError(f"Parameter-card directory does not exist: {cards_dir}")
        if layout.strict_model_binding and not _is_within(cards_dir, layout.model_root):
            cmake_input = (layout.build_dir / "input").resolve() if layout.build_dir else None
            if (cmake_input is not None and _is_within(cards_dir, cmake_input)) or args.cards_dir is None:
                raise ValueError(
                    "MODEL_CARDS_DIR_MISMATCH: cards_dir points into another model "
                    f"or was inferred outside {layout.model_root}: {cards_dir}."
                )
            print(
                f"WARNING: Explicit external --cards-dir {cards_dir} is outside "
                f"model {layout.model_root}.", file=sys.stderr,
            )

    param_card_value: Optional[object] = args.param_card
    if param_card_value is None:
        param_card_value = file_config.get("param_card")
    param_card = resolve_ui2_param_card(
        requested=param_card_value,
        layout=layout,
        explicit_cards_dir=cards_dir,
        config_dir=config_dir,
    )

    subprocesses_dir = resolve_runtime_path(
        config_value(args.subprocesses, file_config, "subprocesses", None),
        layout.subprocesses_dir,
    )
    output_dir = resolve_runtime_path(
        config_value(args.output, file_config, "output", None),
        layout.output_dir,
    )
    backup_root = resolve_runtime_path(
        config_value(args.backup_dir, file_config, "backup_dir", None),
        layout.backup_root,
    )

    if layout.strict_model_binding:
        expected_root = layout.mg5_output or layout.model_root
        if not _is_within(subprocesses_dir, expected_root):
            raise ValueError(
                "MODEL_SUBPROCESSES_MISMATCH: SubProcesses does not belong to the selected model. "
                f"Expected root={expected_root}; SubProcesses={subprocesses_dir}."
            )

    build_dir_value = config_value(args.build_dir, file_config, "build_dir", layout.build_dir)
    explicit_kerrigan = config_value(args.kerrigan, file_config, "kerrigan", None)
    kerrigan, cmake_build_dir = resolve_cmake_kerrigan(
        script_root=layout.model_root,
        explicit_kerrigan=explicit_kerrigan,
        build_dir_value=build_dir_value,
        config_dir=config_dir,
    )

    mg5_output_value = config_value(args.mg5_output, file_config, "mg5_output", None)
    mg5_output = infer_mg5_output(subprocesses_dir, mg5_output_value)
    if layout.mg5_output is not None and mg5_output != layout.mg5_output:
        raise ValueError(
            f"MODEL_MG5_MISMATCH: standalone output {mg5_output} does not match "
            f"the selected model {layout.mg5_output}."
        )
    if mg5_output is not None and subprocesses_dir.resolve() != (mg5_output / "SubProcesses").resolve():
        raise ValueError(
            f"MODEL_MG5_MISMATCH: SubProcesses {subprocesses_dir} does not match "
            f"--mg5-output {mg5_output}."
        )

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
        raise FileNotFoundError(f"Parameter card does not exist: {param_card}")
    if not subprocesses_dir.is_dir():
        raise FileNotFoundError(f"SubProcesses directory does not exist: {subprocesses_dir}")

    # Show the binding that prevents card/model cross-contamination before any
    # physics selection is performed.
    if verbose:
        print_runtime_layout(layout, param_card, cmake_build_dir)

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
                    "PDG mode requires --pdgs or pdgs=... in the input file."
                )
            manual_pdgs = parse_pdg_tokens(
                input(
                    "Enter PDG codes (candidate first, followed by coannihilators): "
                )
            )

        if not manual_pdgs:
            raise ValueError("PDG mode requires at least the candidate's PDG code.")

        manual_pdgs = unique_pdgs(manual_pdgs)
        candidate = particle_by_pdg(read_particles, manual_pdgs[0])

        if candidate_config is not None:
            candidate_from_flag = resolve_candidate(str(candidate_config), read_particles)
            if candidate_from_flag.pdg != candidate.pdg:
                raise ValueError(
                    f"--candidate/input candidate={candidate_from_flag.pdg} does not match the first "
                    f"manually supplied PDG ({candidate.pdg})."
                )

    else:
        candidate_query = candidate_config
        if candidate_query is None:
            if not sys.stdin.isatty():
                raise ValueError(
                    "Combined mode requires --candidate or candidate=... in the input file."
                )
            candidate_query = input("\nEnter the candidate's name, alias, or PDG code: ")
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
            print(f"WARNING: {warning}")

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
            print_combined_selection_criteria(
                xf=xf,
                max_delta=max_delta,
                min_relative_weight=min_relative_weight,
            )
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
                print(f"WARNING: {warning}")
            print_selection_summary(records, unparsed, "pdg")

    selected_count = sum(record.selected for record in records)
    if selected_count == 0:
        print(
            "No processes were selected. Check the candidate, PDG codes, "
            "and correspondence with SubProcesses.",
            file=sys.stderr,
        )
        return 2

    direct_count = sum(
        record.selected and record.category == "candidate_only"
        for record in records
    )
    if direct_count == 0:
        message = (
            "No candidate-candidate annihilation channel was found in the selection."
        )
        if verbose:
            print(f"WARNING: {message}")

    if not verbose:
        xf_label = f"{xf:g}" if mode == "combined" else "manual/no-filter"
        print(
            f"[{mode}] candidate={candidate.name}({candidate.pdg}) | "
            f"processes={selected_count} | task={task} | xf={xf_label}"
        )
        if mode == "combined":
            print(
                "Note: combined mode performs thermal preselection only; "
                "sigma-v is not yet used as an automatic contribution-based selection criterion."
            )
        for warning in warnings:
            print(f"WARNING: {warning}")
        for warning in mode_warnings:
            print(f"WARNING: {warning}")

    if verbose and not args.yes:
        review = yes_no(
            f"{selected_count} processes were selected. Would you like to review them?"
        )
        if review:
            print_selected_processes(records)

    if verbose and unparsed:
        print(
            f"Note: {len(unparsed)} subprocess directories could not be parsed. "
            "They will be recorded in the report for alias verification."
        )

    if args.dry_run:
        print("\nDry run: no files were copied, deleted, backed up, or processed.")
        return 0

    if verbose and not args.yes:
        proceed = yes_no(
            f"Directory '{output_dir.name}' will be recreated "
            f"and {selected_count} subprocess directories will be copied from SubProcesses. Continue?"
        )
        if not proceed:
            print(
                "Operation cancelled. SubProcesses and the existing output "
                "were not modified."
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
        "model": layout.model_label,
        "model_root": str(layout.model_root),
        "strict_model_binding": layout.strict_model_binding,
        "selection_stage": (
            "thermal_preselection_before_sigmav" if mode == "combined" else "manual_pdg_selection"
        ),
        "sigmav_filter_applied": False,
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
        print("\nSelection Completed")
        print("-" * 72)
        print(f"Unmodified source : {subprocesses_dir}")
        print(f"Created directory       : {output_dir}")
        print(f"Copied processes    : {selected_count}")
        print(f"JSON report         : {json_report}")
        print(f"CSV report          : {csv_report}")
        if backup_destination is not None:
            print(f"Previous backup      : {backup_destination}")
        elif backup:
            print("Previous backup      : no previous selection to back up")
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
        print("Calculation completed successfully using the filtered subprocess selection.")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except subprocess.CalledProcessError as error:
        print(
            f"ERROR: the external process exited with code {error.returncode}.",
            file=sys.stderr,
        )
        raise SystemExit(error.returncode or 1)
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
