#!/usr/bin/env python3
"""
run_madgraph.py

Pipeline-aware MadGraph5_aMC@NLO standalone generator.

Inputs:
  1) a UFO model directory,
  2) a list of Z2-odd particles (UFO names and/or PDG codes),
  3) a MadGraph installation.

Output:
  a standalone_cpp directory containing at least:
      SubProcesses/
      src/
  and, when produced by MadGraph:
      lib/

The generated output is directly compatible with the current UI/Kerrigan
contract: both consume an MG5 output root containing SubProcesses/ and src/.

Two invocation styles are supported:

A) Pipeline mode (recommended)
   Run after CMake configuration and point the script to the build directory.
   The script can infer:
      - MadGraph from CMakeCache.txt,
      - the UFO from <build>/input/,
      - odd_particles.txt from <build>/input/,
      - output as <build>/generated/<UFO-name>_standalone.

B) Explicit mode (backward compatible)
   Provide --mg5-root, --ufo, --odd/--odd-file and --output manually.

The MadGraph installation and source UFO are never modified.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


DEFAULT_MG5_MIN_VERSION = "3.6.7"
DEFAULT_MG5_MAX_VERSION = "3.7.0"
DEFAULT_ODD_FILENAMES = (
    "odd_particles.txt",
    "odd_particles.dat",
    "odd_particles",
)

UFO_REQUIRED_FILES = (
    "particles.py",
    "parameters.py",
    "vertices.py",
    "couplings.py",
    "lorentz.py",
    "object_library.py",
    "__init__.py",
)


@dataclass(frozen=True)
class Particle:
    pdg: int
    name: str
    antiname: str
    self_conjugate: bool
    goldstone: bool = False
    propagating: bool = True
    ghost_number: int = 0


def die(message: str, code: int = 2) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


# ---------------------------------------------------------------------------
# Version handling
# ---------------------------------------------------------------------------

def normalize_version(raw: str) -> Optional[str]:
    match = re.search(
        r"(?im)^\s*version\s*=\s*([0-9]+(?:\.[0-9]+)+)",
        raw,
    )
    if match:
        return match.group(1)

    match = re.search(
        r"\b([0-9]+(?:\.[0-9]+){1,3})\b",
        raw,
    )
    return match.group(1) if match else None


def version_tuple(version: str) -> Tuple[int, ...]:
    try:
        return tuple(int(piece) for piece in version.split("."))
    except ValueError as exc:
        raise ValueError(f"Invalid version string: {version!r}") from exc


def version_in_range(
    version: str,
    minimum: Optional[str],
    maximum: Optional[str],
) -> bool:
    current = version_tuple(version)

    if minimum is not None and current < version_tuple(minimum):
        return False

    if maximum is not None and current > version_tuple(maximum):
        return False

    return True


# ---------------------------------------------------------------------------
# CMake/build discovery
# ---------------------------------------------------------------------------

def read_cmake_cache(build_dir: Path) -> Dict[str, str]:
    cache = build_dir / "CMakeCache.txt"

    if not cache.is_file():
        return {}

    values: Dict[str, str] = {}

    with cache.open("r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.strip()

            if (
                not line
                or line.startswith("#")
                or line.startswith("//")
                or "=" not in line
            ):
                continue

            left, value = line.split("=", 1)

            if ":" in left:
                key, _type = left.split(":", 1)
            else:
                key = left

            values[key.strip()] = value.strip()

    return values


def infer_mg5_root_from_build(build_dir: Path) -> Optional[Path]:
    """
    Try common cache names used by this project and previous revisions.

    The function deliberately checks that the resolved directory actually
    contains bin/mg5_aMC or bin/mg5 before accepting it.
    """
    cache = read_cmake_cache(build_dir)

    cache_keys = (
        "MADGRAPH_DIR",
        "MADGRAPH_ROOT",
        "MG5_DIR",
        "MG5_ROOT",
        "MG5_BASE_DIR",
        "FOLDER",
    )

    candidates: List[Path] = []

    for key in cache_keys:
        value = cache.get(key)
        if value:
            candidates.append(Path(value).expanduser())

    env_keys = (
        "MADGRAPH_DIR",
        "MADGRAPH_ROOT",
        "MG5_DIR",
        "MG5_ROOT",
        "MG5_BASE_DIR",
    )

    for key in env_keys:
        value = os.environ.get(key)
        if value:
            candidates.append(Path(value).expanduser())

    checked = set()

    for candidate in candidates:
        try:
            resolved = candidate.resolve()
        except OSError:
            continue

        if resolved in checked:
            continue
        checked.add(resolved)

        if (
            (resolved / "bin" / "mg5_aMC").is_file()
            or (resolved / "bin" / "mg5").is_file()
        ):
            return resolved

    return None


# ---------------------------------------------------------------------------
# MadGraph validation
# ---------------------------------------------------------------------------

def discover_mg5_executable(mg5_root: Path) -> Path:
    for relative in ("bin/mg5_aMC", "bin/mg5"):
        candidate = mg5_root / relative
        if candidate.is_file():
            return candidate.resolve()

    die(
        f"No MadGraph executable found under {mg5_root}. "
        "Expected bin/mg5_aMC (preferred) or bin/mg5."
    )


def validate_mg5(
    mg5_root: Path,
    exact_version: Optional[str],
    min_version: Optional[str],
    max_version: Optional[str],
) -> Tuple[Path, Optional[str]]:
    mg5_root = mg5_root.expanduser().resolve()

    if not mg5_root.is_dir():
        die(
            f"MadGraph root does not exist or is not a directory: "
            f"{mg5_root}"
        )

    executable = discover_mg5_executable(mg5_root)

    version: Optional[str] = None
    version_file = mg5_root / "VERSION"

    if version_file.is_file():
        version = normalize_version(
            version_file.read_text(errors="replace")
        )

    if exact_version is not None:
        if version is None:
            die(
                f"Could not determine MadGraph version from "
                f"{version_file}; exact version {exact_version} was requested."
            )

        if version != exact_version:
            die(
                f"MadGraph version mismatch: found {version}, "
                f"required exactly {exact_version}."
            )

    elif min_version is not None or max_version is not None:
        if version is None:
            die(
                f"Could not determine MadGraph version from "
                f"{version_file}. Expected a version in the supported range."
            )

        if not version_in_range(version, min_version, max_version):
            bounds = []

            if min_version is not None:
                bounds.append(f">= {min_version}")

            if max_version is not None:
                bounds.append(f"<= {max_version}")

            die(
                f"Unsupported MadGraph version: found {version}; "
                f"expected {' and '.join(bounds)}."
            )

    return executable, version


# ---------------------------------------------------------------------------
# UFO discovery and parser
# ---------------------------------------------------------------------------

def looks_like_ufo(path: Path) -> bool:
    return (
        path.is_dir()
        and all((path / name).is_file() for name in UFO_REQUIRED_FILES)
    )


def validate_ufo_dir(ufo_dir: Path) -> Path:
    ufo_dir = ufo_dir.expanduser().resolve()

    if not ufo_dir.is_dir():
        die(f"UFO path is not a directory: {ufo_dir}")

    missing = [
        name
        for name in UFO_REQUIRED_FILES
        if not (ufo_dir / name).is_file()
    ]

    if missing:
        die(
            f"{ufo_dir} does not look like a complete UFO directory. "
            f"Missing: {', '.join(missing)}"
        )

    return ufo_dir


def discover_ufo_from_input(input_dir: Path) -> Path:
    """
    Conservative discovery:
      1. input_dir itself,
      2. its direct child directories.

    We intentionally do not recursively search arbitrary trees because a
    reproducible pipeline should never guess between hidden/nested models.
    """
    input_dir = input_dir.expanduser().resolve()

    if not input_dir.is_dir():
        die(
            f"Pipeline input directory does not exist: {input_dir}. "
            "Create it and place exactly one UFO model directory inside it, "
            "or pass --ufo explicitly."
        )

    candidates: List[Path] = []

    if looks_like_ufo(input_dir):
        candidates.append(input_dir)

    for child in sorted(input_dir.iterdir()):
        if looks_like_ufo(child):
            candidates.append(child)

    # Deduplicate in case input_dir itself was somehow encountered twice.
    candidates = list(dict.fromkeys(path.resolve() for path in candidates))

    if not candidates:
        die(
            f"No UFO model was found in {input_dir}. "
            "Expected a directory containing particles.py, parameters.py, "
            "vertices.py, couplings.py, lorentz.py, object_library.py and "
            "__init__.py. You may also pass --ufo /path/to/model_UFO."
        )

    if len(candidates) > 1:
        formatted = "\n  - ".join(str(path) for path in candidates)
        die(
            "More than one UFO model was found in the pipeline input "
            "directory. Refusing to guess. Use --ufo explicitly.\n"
            f"  - {formatted}"
        )

    return candidates[0]


def literal_kw(call: ast.Call, name: str, default=None):
    for keyword in call.keywords:
        if keyword.arg == name:
            try:
                return ast.literal_eval(keyword.value)
            except Exception:
                return default

    return default


def parse_ufo_particles(ufo_dir: Path) -> List[Particle]:
    """
    Parse Particle(...) declarations without importing/executing the UFO.

    This keeps discovery side-effect free and lets the script resolve both
    UFO names and PDG codes before MadGraph is launched.
    """
    particles_file = ufo_dir / "particles.py"
    source = particles_file.read_text(errors="replace")

    try:
        tree = ast.parse(source, filename=str(particles_file))
    except SyntaxError as exc:
        die(f"Could not parse UFO particles.py: {exc}")

    particles: List[Particle] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue

        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        else:
            function_name = None

        if function_name != "Particle":
            continue

        pdg = literal_kw(node, "pdg_code")
        name = literal_kw(node, "name")
        antiname = literal_kw(node, "antiname")

        if (
            not isinstance(pdg, int)
            or not isinstance(name, str)
            or not isinstance(antiname, str)
        ):
            continue

        goldstone = bool(
            literal_kw(
                node,
                "goldstone",
                literal_kw(node, "goldstoneboson", False),
            )
        )

        propagating = literal_kw(
            node,
            "propagating",
            True,
        )
        propagating = (
            True
            if propagating is None
            else bool(propagating)
        )

        ghost_number = literal_kw(
            node,
            "GhostNumber",
            0,
        )

        if not isinstance(ghost_number, int):
            ghost_number = 0

        particles.append(
            Particle(
                pdg=pdg,
                name=name,
                antiname=antiname,
                self_conjugate=(name == antiname),
                goldstone=goldstone,
                propagating=propagating,
                ghost_number=ghost_number,
            )
        )

    if not particles:
        die(
            f"No Particle(...) declarations could be read from "
            f"{particles_file}. The UFO may use an unusual particles.py format."
        )

    unique: List[Particle] = []
    seen = set()

    for particle in particles:
        key = (
            particle.pdg,
            particle.name,
            particle.antiname,
        )

        if key not in seen:
            seen.add(key)
            unique.append(particle)

    return unique


def build_particle_lookup(
    particles: Sequence[Particle],
) -> Tuple[
    Dict[str, Tuple[Particle, str]],
    Dict[int, Tuple[Particle, str]],
]:
    by_name: Dict[str, Tuple[Particle, str]] = {}
    by_pdg: Dict[int, Tuple[Particle, str]] = {}

    for particle in particles:
        by_name[particle.name] = (
            particle,
            particle.name,
        )
        by_pdg[particle.pdg] = (
            particle,
            particle.name,
        )

        if particle.self_conjugate:
            by_name[particle.antiname] = (
                particle,
                particle.name,
            )
        else:
            by_name[particle.antiname] = (
                particle,
                particle.antiname,
            )
            by_pdg[-particle.pdg] = (
                particle,
                particle.antiname,
            )

    return by_name, by_pdg


# ---------------------------------------------------------------------------
# Odd-particle input
# ---------------------------------------------------------------------------

def tokenize_particle_spec(text: str) -> List[str]:
    tokens: List[str] = []

    lines = text.splitlines()

    # Detect the structured format generated by UI1:
    #   # particle  antiparticle  mass  dof
    #   N1          N1            MN1   2
    structured_ui1_format = any(
        all(
            keyword in raw_line.lower()
            for keyword in (
                "particle",
                "antiparticle",
                "mass",
                "dof",
            )
        )
        for raw_line in lines
        if raw_line.strip().startswith("#")
    )

    for raw_line in lines:
        line = raw_line.split("#", 1)[0].strip()

        if not line:
            continue

        line = line.replace(",", " ")
        columns = line.split()

        if structured_ui1_format:
            # UI1 format:
            # particle antiparticle mass dof
            # run_madgraph only needs the particle column.
            # Antiparticles are added later automatically.
            tokens.append(columns[0])
        else:
            # Backward-compatible simple format:
            # N1 N2 N3 etI etR etp
            tokens.extend(columns)

    return tokens

def discover_odd_file(input_dir: Path) -> Optional[Path]:
    for filename in DEFAULT_ODD_FILENAMES:
        candidate = input_dir / filename

        if candidate.is_file():
            return candidate.resolve()

    return None


def read_odd_tokens(
    odd_values: Optional[Sequence[str]],
    odd_file: Optional[Path],
) -> List[str]:
    tokens: List[str] = []

    if odd_values:
        tokens.extend(str(item) for item in odd_values)

    if odd_file is not None:
        odd_file = odd_file.expanduser().resolve()

        if not odd_file.is_file():
            die(
                f"Odd-particle file does not exist: "
                f"{odd_file}"
            )

        tokens.extend(
            tokenize_particle_spec(
                odd_file.read_text(errors="replace")
            )
        )

    unique: List[str] = []
    seen = set()

    for token in tokens:
        if token not in seen:
            seen.add(token)
            unique.append(token)

    if not unique:
        die(
            "No odd particles were provided. Use --odd ..., --odd-file FILE, "
            "or place odd_particles.txt in the pipeline input directory."
        )

    return unique


def resolve_odd_particles(
    tokens: Sequence[str],
    particles: Sequence[Particle],
    auto_antiparticles: bool = True,
) -> Tuple[List[str], List[dict]]:
    by_name, by_pdg = build_particle_lookup(
        particles
    )

    resolved_names: List[str] = []
    audit: List[dict] = []

    def add_name(name: str) -> None:
        if name not in resolved_names:
            resolved_names.append(name)

    for token in tokens:
        try:
            pdg = int(token)
        except ValueError:
            pdg = None

        match = (
            by_pdg.get(pdg)
            if pdg is not None
            else by_name.get(token)
        )

        if match is None:
            known_preview = ", ".join(
                sorted(by_name)[:25]
            )
            die(
                f"Odd particle {token!r} was not found in the UFO. "
                f"Examples of known UFO names: {known_preview}"
            )

        particle, selected_name = match
        add_name(selected_name)

        auto_added: Optional[str] = None

        if (
            auto_antiparticles
            and not particle.self_conjugate
        ):
            partner = (
                particle.antiname
                if selected_name == particle.name
                else particle.name
            )
            add_name(partner)
            auto_added = partner

        selected_pdg = particle.pdg

        if (
            selected_name == particle.antiname
            and not particle.self_conjugate
        ):
            selected_pdg = -particle.pdg

        audit.append(
            {
                "input": token,
                "pdg": selected_pdg,
                "resolved_name": selected_name,
                "self_conjugate": particle.self_conjugate,
                "auto_added_antiparticle": auto_added,
            }
        )

    return resolved_names, audit


def physical_particle_names(
    particles: Sequence[Particle],
) -> List[str]:
    names: List[str] = []

    for particle in particles:
        if (
            particle.goldstone
            or not particle.propagating
            or particle.ghost_number != 0
        ):
            continue

        for name in (
            particle.name,
            particle.antiname,
        ):
            if name not in names:
                names.append(name)

    return names


def build_even_particles(
    particles: Sequence[Particle],
    odd_names: Sequence[str],
) -> List[str]:
    odd_set = set(odd_names)

    even = [
        name
        for name in physical_particle_names(
            particles
        )
        if name not in odd_set
    ]

    if not even:
        die(
            "No even/visible final-state particles remain "
            "after excluding the odd sector."
        )

    return even


# ---------------------------------------------------------------------------
# MadGraph command generation
# ---------------------------------------------------------------------------

def build_mg5_commands(
    ufo_dir: Path,
    output_dir: Path,
    odd_names: Sequence[str],
    even_names: Sequence[str],
    generation_mode: str,
    group_subprocesses: bool,
) -> Tuple[str, List[Tuple[str, str]]]:
    lines: List[str] = [
        "# Auto-generated by run_madgraph.py",
        (
            "set group_subprocesses "
            + (
                "True"
                if group_subprocesses
                else "False"
            )
        ),
        "set automatic_html_opening False",
        f"import model {ufo_dir} -modelname",
        "define dm_odd = " + " ".join(odd_names),
        "define dm_even = " + " ".join(even_names),
        "",
    ]

    pairs = list(
        combinations_with_replacement(
            odd_names,
            2,
        )
    )

    if generation_mode == "multiparticle":
        lines.append(
            "generate dm_odd dm_odd > dm_even dm_even"
        )

    elif generation_mode == "explicit":
        if not pairs:
            die(
                "No odd-particle initial-state pairs "
                "were generated."
            )

        for index, (particle_1, particle_2) in enumerate(
            pairs
        ):
            keyword = (
                "generate"
                if index == 0
                else "add process"
            )

            lines.append(
                f"{keyword} {particle_1} {particle_2} "
                f"> dm_even dm_even"
            )

    else:
        die(
            f"Unknown generation mode: "
            f"{generation_mode}"
        )

    lines.extend(
        [
            "",
            f"output standalone_cpp {output_dir}",
            "",
        ]
    )

    return "\n".join(lines), pairs


# ---------------------------------------------------------------------------
# Output safety and validation
# ---------------------------------------------------------------------------

def safe_remove_output(path: Path) -> None:
    path = path.expanduser().resolve()

    dangerous = {
        Path("/").resolve(),
        Path.home().resolve(),
    }

    if (
        path in dangerous
        or len(path.parts) < 3
    ):
        die(
            f"Refusing to remove suspicious "
            f"output path: {path}"
        )

    if path.exists():
        shutil.rmtree(path)


def stream_process(
    command: Sequence[str],
    log_path: Path,
    env: Optional[Dict[str, str]] = None,
) -> int:
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with log_path.open(
        "w",
        encoding="utf-8",
    ) as log:
        process = subprocess.Popen(
            list(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            env=env,
        )

        assert process.stdout is not None

        for line in process.stdout:
            sys.stdout.write(line)
            log.write(line)

        return process.wait()


def validate_standalone(
    output_dir: Path,
) -> dict:
    # Kerrigan requires SubProcesses/ and src/.
    required_dirs = (
        "SubProcesses",
        "src",
    )

    missing = [
        directory
        for directory in required_dirs
        if not (
            output_dir / directory
        ).is_dir()
    ]

    if missing:
        die(
            "MadGraph returned success but the standalone_cpp "
            "output is incomplete. Missing directories: "
            + ", ".join(missing)
        )

    subprocess_root = (
        output_dir / "SubProcesses"
    )

    subprocess_dirs = sorted(
        entry.name
        for entry in subprocess_root.iterdir()
        if (
            entry.is_dir()
            and entry.name.startswith("P")
        )
    )

    if not subprocess_dirs:
        die(
            "No P* subprocess directories were found under "
            f"{subprocess_root}."
        )

    has_lib = (
        output_dir / "lib"
    ).is_dir()

    if not has_lib:
        print(
            "WARNING: standalone output does not contain lib/. "
            "This is allowed by the current Kerrigan contract, "
            "which can keep the build-side libraries when lib/ "
            "is absent.",
            file=sys.stderr,
        )

    return {
        "subprocess_count": len(
            subprocess_dirs
        ),
        "subprocess_directories": (
            subprocess_dirs
        ),
        "has_lib_directory": has_lib,
    }


def write_pipeline_pointer(
    build_dir: Path,
    output_dir: Path,
    manifest_path: Path,
) -> Tuple[Path, Path]:
    """
    Keep a tiny machine-readable pointer to the latest generated MG5 root.
    Existing UI/Kerrigan do not require this file, so this is non-breaking.
    """
    generated_root = (
        build_dir / "generated"
    )
    generated_root.mkdir(
        parents=True,
        exist_ok=True,
    )

    text_pointer = (
        generated_root
        / "current_mg5_output.txt"
    )

    json_pointer = (
        generated_root
        / "current_mg5_output.json"
    )

    text_pointer.write_text(
        str(output_dir.resolve()) + "\n",
        encoding="utf-8",
    )

    json_pointer.write_text(
        json.dumps(
            {
                "mg5_output": str(
                    output_dir.resolve()
                ),
                "subprocesses": str(
                    (
                        output_dir
                        / "SubProcesses"
                    ).resolve()
                ),
                "generation_manifest": str(
                    manifest_path.resolve()
                ),
            },
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    return (
        text_pointer,
        json_pointer,
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a MadGraph standalone_cpp package from a UFO "
            "model and a list of Z2-odd particles. Supports both an "
            "explicit CLI and a CMake-build-aware pipeline mode."
        )
    )

    parser.add_argument(
        "--build-dir",
        type=Path,
        help=(
            "Configured CMake build directory. Recommended pipeline mode. "
            "When supplied, the script can infer MadGraph from CMakeCache.txt, "
            "use <build>/input for user inputs and <build>/generated for output."
        ),
    )

    parser.add_argument(
        "--input-dir",
        type=Path,
        help=(
            "Pipeline input directory. Default with --build-dir: <build>/input."
        ),
    )

    parser.add_argument(
        "--mg5-root",
        type=Path,
        help=(
            "MadGraph5_aMC root directory. Optional in pipeline mode when "
            "the path can be inferred from CMakeCache.txt or environment."
        ),
    )

    parser.add_argument(
        "--ufo",
        type=Path,
        help=(
            "Path to the UFO model directory. Optional in pipeline mode when "
            "exactly one UFO exists under <build>/input."
        ),
    )

    parser.add_argument(
        "--odd",
        nargs="+",
        help=(
            "Odd particles as UFO names and/or PDG codes. "
            "Example: --odd n1 n2 etp or --odd 1012 1014."
        ),
    )

    parser.add_argument(
        "--odd-file",
        type=Path,
        help=(
            "Text file containing odd particle names/PDGs. "
            "Optional in pipeline mode when <input>/odd_particles.txt exists."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Destination standalone_cpp directory. "
            "Default with --build-dir: "
            "<build>/generated/<UFO-name>_standalone."
        ),
    )

    parser.add_argument(
        "--generation-mode",
        choices=(
            "multiparticle",
            "explicit",
        ),
        default="multiparticle",
        help=(
            "multiparticle (default): one generate command using "
            "dm_odd/dm_even. explicit: one generate plus add-process "
            "commands for every unordered odd-particle initial pair."
        ),
    )

    parser.add_argument(
        "--no-auto-antiparticles",
        action="store_true",
        help=(
            "Do not automatically add the antiparticle of a "
            "non-self-conjugate odd state."
        ),
    )

    parser.add_argument(
        "--group-subprocesses",
        action="store_true",
        help=(
            "Allow MG5 subprocess grouping. Default is False to preserve "
            "transparent P* process directories for downstream selection."
        ),
    )

    parser.add_argument(
        "--min-version",
        default=DEFAULT_MG5_MIN_VERSION,
        help=(
            "Minimum supported MG5 version. "
            f"Default: {DEFAULT_MG5_MIN_VERSION}."
        ),
    )

    parser.add_argument(
        "--max-version",
        default=DEFAULT_MG5_MAX_VERSION,
        help=(
            "Maximum tested/supported MG5 version. "
            f"Default: {DEFAULT_MG5_MAX_VERSION}."
        ),
    )

    parser.add_argument(
        "--require-version",
        default=None,
        help=(
            "Backward-compatible exact-version override. "
            "Example: --require-version 3.6.7. "
            "Use --require-version any to disable version checking."
        ),
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "Delete and recreate --output if it already exists."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate inputs and print the MG5 command card without "
            "running MadGraph or creating the standalone output."
        ),
    )

    return parser.parse_args()


# ---------------------------------------------------------------------------
# Runtime resolution
# ---------------------------------------------------------------------------

def resolve_runtime_inputs(
    args: argparse.Namespace,
) -> dict:
    build_dir: Optional[Path] = None

    if args.build_dir is not None:
        build_dir = (
            args.build_dir
            .expanduser()
            .resolve()
        )

        if not build_dir.is_dir():
            die(
                f"Configured build directory does not exist: "
                f"{build_dir}"
            )

        if not (
            (build_dir / "CMakeCache.txt").is_file()
            or (build_dir / "Makefile").is_file()
        ):
            die(
                f"{build_dir} does not look like a configured CMake "
                "build directory (CMakeCache.txt/Makefile not found)."
            )

    input_dir: Optional[Path] = None

    if args.input_dir is not None:
        input_dir = (
            args.input_dir
            .expanduser()
            .resolve()
        )
    elif build_dir is not None:
        input_dir = (
            build_dir / "input"
        ).resolve()

    # MadGraph root: explicit > environment/cache from build.
    mg5_root: Optional[Path]

    if args.mg5_root is not None:
        mg5_root = (
            args.mg5_root
            .expanduser()
            .resolve()
        )
    elif build_dir is not None:
        mg5_root = infer_mg5_root_from_build(
            build_dir
        )
    else:
        mg5_root = None

    if mg5_root is None:
        die(
            "MadGraph path could not be resolved. Pass --mg5-root, "
            "or use --build-dir with a CMakeCache.txt/environment that "
            "contains the MadGraph path."
        )

    # UFO: explicit > discover from pipeline input.
    if args.ufo is not None:
        ufo_dir = validate_ufo_dir(
            args.ufo
        )
    elif input_dir is not None:
        ufo_dir = discover_ufo_from_input(
            input_dir
        )
    else:
        die(
            "No UFO model was specified. Pass --ufo or use --build-dir/"
            "--input-dir with exactly one UFO model in the input directory."
        )

    # Odd file: explicit --odd and/or explicit/discovered file.
    odd_file = (
        args.odd_file
        .expanduser()
        .resolve()
        if args.odd_file is not None
        else None
    )

    if (
        odd_file is None
        and not args.odd
        and input_dir is not None
    ):
        odd_file = discover_odd_file(
            input_dir
        )

    # Output: explicit > build/generated/<model>_standalone.
    if args.output is not None:
        output_dir = (
            args.output
            .expanduser()
            .resolve()
        )
    elif build_dir is not None:
        output_dir = (
            build_dir
            / "generated"
            / f"{ufo_dir.name}_standalone"
        ).resolve()
    else:
        die(
            "No output directory was specified. Pass --output, or use "
            "--build-dir to receive the default <build>/generated output."
        )

    return {
        "build_dir": build_dir,
        "input_dir": input_dir,
        "mg5_root": mg5_root,
        "ufo_dir": ufo_dir,
        "odd_file": odd_file,
        "output_dir": output_dir,
    }


def main() -> int:
    args = parse_args()
    runtime = resolve_runtime_inputs(
        args
    )

    build_dir: Optional[Path] = (
        runtime["build_dir"]
    )
    input_dir: Optional[Path] = (
        runtime["input_dir"]
    )
    mg5_root: Path = (
        runtime["mg5_root"]
    )
    ufo_dir: Path = (
        runtime["ufo_dir"]
    )
    odd_file: Optional[Path] = (
        runtime["odd_file"]
    )
    output_dir: Path = (
        runtime["output_dir"]
    )

    # Backward-compatible exact version option.
    exact_version: Optional[str] = None
    min_version: Optional[str] = (
        str(args.min_version)
        if args.min_version is not None
        else None
    )
    max_version: Optional[str] = (
        str(args.max_version)
        if args.max_version is not None
        else None
    )

    if args.require_version is not None:
        requested = str(
            args.require_version
        ).strip()

        if requested.lower() == "any":
            exact_version = None
            min_version = None
            max_version = None
        else:
            exact_version = requested
            min_version = None
            max_version = None

    mg5_executable, mg5_version = (
        validate_mg5(
            mg5_root=mg5_root,
            exact_version=exact_version,
            min_version=min_version,
            max_version=max_version,
        )
    )

    particles = parse_ufo_particles(
        ufo_dir
    )

    odd_tokens = read_odd_tokens(
        odd_values=args.odd,
        odd_file=odd_file,
    )

    odd_names, resolution_audit = (
        resolve_odd_particles(
            odd_tokens,
            particles,
            auto_antiparticles=(
                not args.no_auto_antiparticles
            ),
        )
    )

    even_names = build_even_particles(
        particles,
        odd_names,
    )

    if output_dir.exists():
        if not args.force:
            die(
                f"Output already exists: {output_dir}. "
                "Choose another --output or use --force."
            )

        safe_remove_output(
            output_dir
        )

    # Do not create the final output directory itself. MadGraph owns it.
    output_dir.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command_text, pairs = (
        build_mg5_commands(
            ufo_dir=ufo_dir,
            output_dir=output_dir,
            odd_names=odd_names,
            even_names=even_names,
            generation_mode=(
                args.generation_mode
            ),
            group_subprocesses=(
                args.group_subprocesses
            ),
        )
    )

    run_stamp = (
        dt.datetime.now()
        .astimezone()
        .isoformat(
            timespec="seconds"
        )
    )

    command_file = (
        output_dir.parent
        / f".{output_dir.name}.generation.mg5"
    )

    log_file = (
        output_dir.parent
        / f".{output_dir.name}.mg5.log"
    )

    command_file.write_text(
        command_text,
        encoding="utf-8",
    )

    print("=" * 76)
    print(
        "MadGraph standalone_cpp generation"
    )
    print("=" * 76)
    print(
        f"Invocation mode    : "
        f"{'pipeline' if build_dir is not None else 'explicit'}"
    )

    if build_dir is not None:
        print(
            f"CMake build        : "
            f"{build_dir}"
        )

    if input_dir is not None:
        print(
            f"Pipeline input     : "
            f"{input_dir}"
        )

    print(
        f"MG5 root           : "
        f"{mg5_root}"
    )
    print(
        f"MG5 executable     : "
        f"{mg5_executable}"
    )
    print(
        f"MG5 version        : "
        f"{mg5_version or 'unknown'}"
    )
    print(
        f"UFO model          : "
        f"{ufo_dir}"
    )
    print(
        f"Odd-particle file  : "
        f"{odd_file or '(CLI only)'}"
    )
    print(
        f"Standalone output  : "
        f"{output_dir}"
    )
    print(
        f"Generation mode    : "
        f"{args.generation_mode}"
    )
    print(
        f"group_subprocesses : "
        f"{args.group_subprocesses}"
    )
    print(
        f"Odd states         : "
        f"{' '.join(odd_names)}"
    )
    print(
        f"Even states        : "
        f"{len(even_names)}"
    )
    print(
        f"Odd initial pairs  : "
        f"{len(pairs)}"
    )
    print(
        f"Command card       : "
        f"{command_file}"
    )
    print("=" * 76)

    print(
        "\nResolved odd-particle input:"
    )

    for item in resolution_audit:
        extra = ""

        if item[
            "auto_added_antiparticle"
        ]:
            extra = (
                " (+ anti: "
                + item[
                    "auto_added_antiparticle"
                ]
                + ")"
            )

        print(
            f"  {item['input']:>12} -> "
            f"{item['resolved_name']} "
            f"(PDG {item['pdg']})"
            f"{extra}"
        )

    if args.dry_run:
        print(
            "\nDRY RUN: MadGraph was not executed and no standalone "
            "output was created.\n"
        )
        print(command_text)

        # The temporary command card is useful for inspection in dry-run.
        return 0

    print(
        "\nRunning MadGraph...\n"
    )

########
    mg5_env = os.environ.copy()

    ufo_parent = str(
        ufo_dir.parent.resolve()
    )

    existing_pythonpath = mg5_env.get(
        "PYTHONPATH",
        "",
    )

    if existing_pythonpath:
        mg5_env["PYTHONPATH"] = (
            ufo_parent
            + os.pathsep
            + existing_pythonpath
        )
    else:
        mg5_env["PYTHONPATH"] = ufo_parent
########

    return_code = stream_process(
        [
            str(mg5_executable),
            str(command_file),
        ],
        log_file,
        env=mg5_env,
    )

    if return_code != 0:
        die(
            f"MadGraph exited with status {return_code}. "
            f"See log: {log_file}",
            code=(
                return_code
                if 0 < return_code < 256
                else 1
            ),
        )

    validation = validate_standalone(
        output_dir
    )

    generation_commands_path = (
        output_dir
        / "generation_commands.mg5"
    )
    generation_log_path = (
        output_dir
        / "mg5_generation.log"
    )
    manifest_path = (
        output_dir
        / "generation_manifest.json"
    )

    shutil.copy2(
        command_file,
        generation_commands_path,
    )

    shutil.copy2(
        log_file,
        generation_log_path,
    )

    particle_catalog = [
        {
            "pdg": particle.pdg,
            "name": particle.name,
            "antiname": particle.antiname,
            "self_conjugate": (
                particle.self_conjugate
            ),
        }
        for particle in particles
    ]

    manifest = {
        "created_at": run_stamp,
        "invocation_mode": (
            "pipeline"
            if build_dir is not None
            else "explicit"
        ),
        "cmake_build_dir": (
            None
            if build_dir is None
            else str(build_dir)
        ),
        "pipeline_input_dir": (
            None
            if input_dir is None
            else str(input_dir)
        ),
        "mg5_root": str(
            mg5_root
        ),
        "mg5_executable": str(
            mg5_executable
        ),
        "mg5_version": (
            mg5_version
        ),
        "supported_mg5_min": (
            min_version
        ),
        "supported_mg5_max": (
            max_version
        ),
        "exact_mg5_version_override": (
            exact_version
        ),
        "ufo_model": str(
            ufo_dir
        ),
        "output": str(
            output_dir
        ),
        "generation_mode": (
            args.generation_mode
        ),
        "group_subprocesses": (
            args.group_subprocesses
        ),
        "auto_antiparticles": (
            not args.no_auto_antiparticles
        ),
        "odd_input": odd_tokens,
        "odd_resolution": (
            resolution_audit
        ),
        "odd_states_used": (
            odd_names
        ),
        "even_states_used": (
            even_names
        ),
        "particle_catalog": (
            particle_catalog
        ),
        "odd_initial_pairs": [
            {
                "p1": particle_1,
                "p2": particle_2,
            }
            for (
                particle_1,
                particle_2,
            ) in pairs
        ],
        **validation,
    }

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )

    (
        output_dir
        / "odd_particles_resolved.txt"
    ).write_text(
        "\n".join(odd_names)
        + "\n",
        encoding="utf-8",
    )

    pointer_paths: Optional[
        Tuple[Path, Path]
    ] = None

    if build_dir is not None:
        pointer_paths = (
            write_pipeline_pointer(
                build_dir=build_dir,
                output_dir=output_dir,
                manifest_path=manifest_path,
            )
        )

    # Temporary files were copied into the final standalone.
    command_file.unlink(
        missing_ok=True
    )
    log_file.unlink(
        missing_ok=True
    )

    print(
        "\n" + "=" * 76
    )
    print("SUCCESS")
    print("=" * 76)
    print(
        f"Standalone output  : "
        f"{output_dir}"
    )
    print(
        f"Subprocesses       : "
        f"{validation['subprocess_count']}"
    )
    print(
        f"src/               : yes"
    )
    print(
        f"lib/               : "
        f"{'yes' if validation['has_lib_directory'] else 'no (allowed)'}"
    )
    print(
        f"Manifest           : "
        f"{manifest_path}"
    )
    print(
        f"MG5 commands       : "
        f"{generation_commands_path}"
    )
    print(
        f"MG5 log            : "
        f"{generation_log_path}"
    )

    if pointer_paths is not None:
        print(
            f"Pipeline pointer   : "
            f"{pointer_paths[0]}"
        )

    print()
    print(
        "This directory is the MG5 output root expected by the "
        "current selector/Kerrigan pipeline."
    )
    print()
    print(
        "Next-step paths:"
    )
    print(
        f"  --mg5-output {output_dir}"
    )
    print(
        f"  --subprocesses {output_dir / 'SubProcesses'}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
