#!/usr/bin/env python3
"""
Select relevant scotogenic subprocesses for a dark-matter candidate.

The script:

1. Reads Block MASS and DECAY from a param_card.dat.
2. Creates the list `read_particles`.
3. Asks for the candidate by name, MadGraph alias, or PDG code.
4. Validates the candidate using:
   - PDG identity,
   - mass,
   - decay width,
   - whether a lighter dark-sector particle exists.
5. Builds two selections:
   - candidate_only:
       only pure candidate/candidate initial states;
   - effective_dark_sector:
       candidate plus mass-close coannihilators, followed by all
       initial-state pairs formed from that active sector.
6. Shows how many process folders will be copied.
7. Optionally prints the complete list before copying.
8. Recreates effective_SubProcesses safely without modifying SubProcesses.

Expected folder format:
    P1_Sigma_scotogenic_UFO_<initial_state>_<final_state>

Examples:
    P1_Sigma_scotogenic_UFO_n1n1_emep
    P1_Sigma_scotogenic_UFO_etpcn1_aem
    P1_Sigma_scotogenic_UFO_etpetpc_aa
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import sys
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

def parse_dark_pdgs(value: Optional[str]) -> Optional[set[int]]:
    if value is None:
        return None

    values = {
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    }

    return values or None


def build_parser() -> argparse.ArgumentParser:
    script_root = Path(__file__).resolve().parent

    parser = argparse.ArgumentParser(
        description=(
            "Select and copy candidate-only or effective-dark-sector "
            "process folders from SubProcesses."
        )
    )

    parser.add_argument(
        "param_card",
        type=Path,
        help="Path to the param_card.dat to analyze.",
    )

    parser.add_argument(
        "--candidate",
        help=(
            "Candidate name, folder alias or PDG. "
            "If omitted, the script asks interactively."
        ),
    )

    parser.add_argument(
        "--mode",
        choices=[
            "candidate_only",
            "effective_dark_sector",
            "combined",
        ],
        default="combined",
        help=(
            "candidate_only: pure candidate/candidate initial states. "
            "effective_dark_sector: all active dark-sector pairs. "
            "combined: effective sector plus category validation/reporting."
        ),
    )

    parser.add_argument(
        "--subprocesses",
        type=Path,
        default=script_root / "SubProcesses",
        help="Source SubProcesses folder.",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=script_root / "effective_SubProcesses",
        help="Destination folder recreated after confirmation.",
    )

    parser.add_argument(
        "--x-ref",
        type=float,
        default=25.0,
        help="Reference x=m_DM/T used in the Boltzmann relevance estimate.",
    )

    parser.add_argument(
        "--max-delta",
        type=float,
        default=0.25,
        help="Maximum relative mass splitting Delta=(m_i-m_DM)/m_DM.",
    )

    parser.add_argument(
        "--min-relative-weight",
        type=float,
        default=1.0e-3,
        help="Minimum approximate n_i^eq/n_DM^eq at x_ref.",
    )

    parser.add_argument(
        "--dark-pdgs",
        help=(
            "Optional comma-separated dark-sector PDGs. "
            "Default for this UFO: 1001,1002,1003,1012,1014,1016."
        ),
    )

    parser.add_argument(
        "--width-tolerance",
        type=float,
        default=1.0e-30,
        help="Maximum width treated as stable for the candidate.",
    )

    parser.add_argument(
        "--allow-unstable-candidate",
        action="store_true",
        help="Allow a candidate with nonzero DECAY width.",
    )

    parser.add_argument(
        "--allow-nonlightest-candidate",
        action="store_true",
        help="Allow a candidate heavier than another dark-sector particle.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze and preview, but do not copy anything.",
    )

    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip interactive review/copy confirmations.",
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    param_card = args.param_card.expanduser().resolve()
    subprocesses_dir = args.subprocesses.expanduser().resolve()
    output_dir = args.output.expanduser().resolve()

    if not param_card.is_file():
        raise FileNotFoundError(f"No existe el param_card: {param_card}")

    if not subprocesses_dir.is_dir():
        raise FileNotFoundError(
            f"No existe la carpeta SubProcesses: {subprocesses_dir}"
        )

    if args.x_ref <= 0.0:
        raise ValueError("--x-ref debe ser positivo.")

    if args.max_delta < 0.0:
        raise ValueError("--max-delta no puede ser negativo.")

    if args.min_relative_weight < 0.0:
        raise ValueError("--min-relative-weight no puede ser negativo.")

    # Requested variable name:
    read_particles = read_param_card(param_card)
    print_particle_table(read_particles)

    candidate_query = args.candidate
    if not candidate_query:
        candidate_query = input(
            "\nIngrese el nombre, alias o PDG del candidato: "
        )

    candidate = resolve_candidate(candidate_query, read_particles)

    requested_dark_pdgs = parse_dark_pdgs(args.dark_pdgs)
    dark_particles = get_dark_particles(
        read_particles,
        requested_dark_pdgs,
    )

    warnings = validate_candidate(
        candidate=candidate,
        dark_particles=dark_particles,
        allow_unstable=args.allow_unstable_candidate,
        allow_nonlightest=args.allow_nonlightest_candidate,
        width_tolerance=args.width_tolerance,
    )

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

    for warning in warnings:
        print(f"ADVERTENCIA: {warning}")

    active_pdgs, decisions = build_effective_dark_sector(
        candidate=candidate,
        dark_particles=dark_particles,
        x_ref=args.x_ref,
        max_delta=args.max_delta,
        min_relative_weight=args.min_relative_weight,
    )

    print_dark_sector_table(
        decisions,
        x_ref=args.x_ref,
        max_delta=args.max_delta,
        min_relative_weight=args.min_relative_weight,
    )

    records, unparsed = scan_processes(
        subprocesses_dir=subprocesses_dir,
        dark_particles=dark_particles,
        candidate=candidate,
        active_pdgs=active_pdgs,
        mode=args.mode,
    )

    print_selection_summary(records, unparsed, args.mode)

    selected_count = sum(record.selected for record in records)

    if selected_count == 0:
        print(
            "No se seleccionó ningún proceso. "
            "Revise los aliases, el candidato o los criterios de masa.",
            file=sys.stderr,
        )
        return 2

    if args.mode == "combined":
        direct_count = sum(
            record.selected and record.category == "candidate_only"
            for record in records
        )
        if direct_count == 0:
            print(
                "ADVERTENCIA: no se encontró ningún canal candidato+candidato. "
                "Revise la correspondencia de aliases.",
                file=sys.stderr,
            )

    if args.yes:
        review = False
    else:
        review = yes_no(
            f"Se seleccionaron {selected_count} procesos. "
            "¿Desea revisar cuáles son?"
        )

    if review:
        print_selected_processes(records)

    if unparsed:
        print(
            f"\nNota: {len(unparsed)} carpetas no pudieron interpretarse. "
            "Se guardarán en el reporte para revisar aliases."
        )

    if args.dry_run:
        print("\nDry run: no se copió ni eliminó ninguna carpeta.")
        return 0

    if not args.yes:
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

    copy_selected_processes(
        subprocesses_dir=subprocesses_dir,
        output_dir=output_dir,
        records=records,
    )

    settings = {
        "x_ref": args.x_ref,
        "max_delta": args.max_delta,
        "min_relative_weight": args.min_relative_weight,
        "width_tolerance": args.width_tolerance,
        "dark_pdgs": [particle.pdg for particle in dark_particles],
    }

    json_report, csv_report = write_reports(
        output_dir=output_dir,
        param_card=param_card,
        candidate=candidate,
        mode=args.mode,
        active_pdgs=active_pdgs,
        decisions=decisions,
        records=records,
        unparsed=unparsed,
        settings=settings,
    )

    print("\nSelección completada")
    print("-" * 72)
    print(f"Fuente sin modificar : {subprocesses_dir}")
    print(f"Carpeta creada       : {output_dir}")
    print(f"Procesos copiados    : {selected_count}")
    print(f"Reporte JSON         : {json_report}")
    print(f"Reporte CSV          : {csv_report}")
    print("-" * 72)

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
