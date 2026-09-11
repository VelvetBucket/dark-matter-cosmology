#!/usr/bin/env python3
"""
prepare_mg5_standalone.py

Generate a MadGraph5_aMC@NLO C++ standalone package from:
  1) a UFO model directory
  2) a list of Z2-odd particles (UFO names or PDG codes)

The script does NOT modify the MadGraph installation. It imports the UFO by
absolute path and exports a standalone_cpp directory that can be consumed by
the dark-matter-cosmology CMake/Kerrigan pipeline.

Default generation strategy:
    define dm_odd  = <resolved odd particle names>
    define dm_even = <all physical UFO particles not in dm_odd>
    generate dm_odd dm_odd > dm_even dm_even
    output standalone_cpp <OUTPUT>

MadGraph is therefore responsible for keeping only processes that actually
exist in the model.

An explicit-pair strategy is also available:
    --generation-mode explicit
which creates one "generate" plus a sequence of "add process" commands.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from itertools import combinations_with_replacement
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple


DEFAULT_REQUIRED_MG5_VERSION = "3.6.7"


@dataclass(frozen=True)
class Particle:
    pdg: int
    name: str
    antiname: str
    self_conjugate: bool
    goldstone: bool = False
    propagating: bool = True
    ghost_number: int = 0


def die(message: str, code: int = 2):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(code)


def normalize_version(raw: str) -> Optional[str]:
    m = re.search(r"(?im)^\s*version\s*=\s*([0-9]+(?:\.[0-9]+)+)", raw)
    if m:
        return m.group(1)
    m = re.search(r"\b([0-9]+(?:\.[0-9]+){1,3})\b", raw)
    return m.group(1) if m else None


def discover_mg5_executable(mg5_root: Path) -> Path:
    for rel in ("bin/mg5_aMC", "bin/mg5"):
        candidate = mg5_root / rel
        if candidate.is_file():
            return candidate.resolve()
    die(
        f"No MadGraph executable found under {mg5_root}. "
        "Expected bin/mg5_aMC (preferred) or bin/mg5."
    )


def validate_mg5(
    mg5_root: Path,
    required_version: Optional[str],
) -> Tuple[Path, Optional[str]]:
    mg5_root = mg5_root.expanduser().resolve()

    if not mg5_root.is_dir():
        die(f"MadGraph root does not exist or is not a directory: {mg5_root}")

    exe = discover_mg5_executable(mg5_root)

    version = None
    version_file = mg5_root / "VERSION"
    if version_file.is_file():
        version = normalize_version(version_file.read_text(errors="replace"))

    if required_version:
        if version is None:
            die(
                f"Could not determine MadGraph version from {version_file}. "
                f"This run requires {required_version}."
            )
        if version != required_version:
            die(
                f"MadGraph version mismatch: found {version}, "
                f"required {required_version}."
            )

    return exe, version


def validate_ufo_dir(ufo_dir: Path) -> Path:
    ufo_dir = ufo_dir.expanduser().resolve()

    if not ufo_dir.is_dir():
        die(f"UFO path is not a directory: {ufo_dir}")

    required = [
        "particles.py",
        "parameters.py",
        "vertices.py",
        "couplings.py",
        "lorentz.py",
        "object_library.py",
        "__init__.py",
    ]

    missing = [name for name in required if not (ufo_dir / name).is_file()]
    if missing:
        die(
            f"{ufo_dir} does not look like a complete UFO directory. "
            f"Missing: {', '.join(missing)}"
        )

    return ufo_dir


def literal_kw(call: ast.Call, name: str, default=None):
    for kw in call.keywords:
        if kw.arg == name:
            try:
                return ast.literal_eval(kw.value)
            except Exception:
                return default
    return default


def parse_ufo_particles(ufo_dir: Path) -> List[Particle]:
    """
    Parse Particle(...) declarations in particles.py without importing or
    executing the UFO. A base UFO Particle declaration contains both name
    and antiname, so both MG5 aliases can be reconstructed.
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
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        else:
            func_name = None

        if func_name != "Particle":
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

        goldstone = bool(literal_kw(node, "goldstoneboson", False))

        propagating = literal_kw(node, "propagating", True)
        propagating = True if propagating is None else bool(propagating)

        ghost_number = literal_kw(node, "GhostNumber", 0)
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
            f"No Particle(...) declarations could be read from {particles_file}. "
            "The UFO may use an unusual particles.py format."
        )

    seen = set()
    unique: List[Particle] = []

    for particle in particles:
        key = (particle.pdg, particle.name, particle.antiname)
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
        by_name[particle.name] = (particle, particle.name)
        by_pdg[particle.pdg] = (particle, particle.name)

        if particle.self_conjugate:
            by_name[particle.antiname] = (particle, particle.name)
        else:
            by_name[particle.antiname] = (particle, particle.antiname)
            by_pdg[-particle.pdg] = (particle, particle.antiname)

    return by_name, by_pdg


def tokenize_particle_spec(text: str) -> List[str]:
    tokens: List[str] = []

    for raw_line in text.splitlines():
        line = raw_line.split("#", 1)[0].strip()

        if not line:
            continue

        line = line.replace(",", " ")
        tokens.extend(token for token in line.split() if token)

    return tokens


def read_odd_tokens(args: argparse.Namespace) -> List[str]:
    tokens: List[str] = []

    if args.odd:
        tokens.extend(args.odd)

    if args.odd_file:
        odd_file = args.odd_file.expanduser().resolve()

        if not odd_file.is_file():
            die(f"Odd-particle file does not exist: {odd_file}")

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
            "No odd particles were provided. "
            "Use --odd ... or --odd-file FILE."
        )

    return unique


def resolve_odd_particles(
    tokens: Sequence[str],
    particles: Sequence[Particle],
    auto_antiparticles: bool = True,
) -> Tuple[List[str], List[dict]]:
    by_name, by_pdg = build_particle_lookup(particles)

    resolved_names: List[str] = []
    audit: List[dict] = []

    def add_name(name: str):
        if name not in resolved_names:
            resolved_names.append(name)

    for token in tokens:
        try:
            pdg = int(token)
        except ValueError:
            pdg = None

        if pdg is not None:
            match = by_pdg.get(pdg)
        else:
            match = by_name.get(token)

        if match is None:
            known_preview = ", ".join(sorted(by_name)[:25])
            die(
                f"Odd particle '{token}' was not found in the UFO. "
                f"Examples of known UFO names: {known_preview}"
            )

        particle, selected_name = match
        add_name(selected_name)

        auto_added = None

        if auto_antiparticles and not particle.self_conjugate:
            partner = (
                particle.antiname
                if selected_name == particle.name
                else particle.name
            )
            add_name(partner)
            auto_added = partner

        selected_pdg = particle.pdg
        if selected_name == particle.antiname and not particle.self_conjugate:
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

        for name in (particle.name, particle.antiname):
            if name not in names:
                names.append(name)

    return names


def build_even_particles(
    particles: Sequence[Particle],
    odd_names: Sequence[str],
) -> List[str]:
    odd = set(odd_names)

    even = [
        name
        for name in physical_particle_names(particles)
        if name not in odd
    ]

    if not even:
        die(
            "No even/visible final-state particles remain "
            "after excluding the odd sector."
        )

    return even


def build_mg5_commands(
    ufo_dir: Path,
    output_dir: Path,
    odd_names: Sequence[str],
    even_names: Sequence[str],
    generation_mode: str,
    group_subprocesses: bool,
) -> Tuple[str, List[Tuple[str, str]]]:
    lines: List[str] = [
        "# Auto-generated by prepare_mg5_standalone.py",
        (
            "set group_subprocesses "
            + ("True" if group_subprocesses else "False")
        ),
        "set automatic_html_opening False",
        f"import model {ufo_dir}",
        "define dm_odd = " + " ".join(odd_names),
        "define dm_even = " + " ".join(even_names),
        "",
    ]

    pairs = list(
        combinations_with_replacement(odd_names, 2)
    )

    if generation_mode == "multiparticle":
        lines.append(
            "generate dm_odd dm_odd > dm_even dm_even"
        )

    elif generation_mode == "explicit":
        if not pairs:
            die(
                "No odd-particle initial-state pairs were generated."
            )

        first = True

        for p1, p2 in pairs:
            keyword = "generate" if first else "add process"
            lines.append(
                f"{keyword} {p1} {p2} > dm_even dm_even"
            )
            first = False

    else:
        die(f"Unknown generation mode: {generation_mode}")

    lines.extend(
        [
            "",
            f"output standalone_cpp {output_dir}",
            "",
        ]
    )

    return "\n".join(lines), pairs


def safe_remove_output(path: Path):
    path = path.expanduser().resolve()

    dangerous = {
        Path("/").resolve(),
        Path.home().resolve(),
    }

    if path in dangerous or len(path.parts) < 3:
        die(
            f"Refusing to remove suspicious output path: {path}"
        )

    if path.exists():
        shutil.rmtree(path)


def stream_process(
    command: Sequence[str],
    log_path: Path,
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
        )

        assert process.stdout is not None

        for line in process.stdout:
            sys.stdout.write(line)
            log.write(line)

        return process.wait()


def validate_standalone(
    output_dir: Path,
) -> dict:
    required_dirs = [
        "SubProcesses",
        "src",
        "lib",
    ]

    missing = [
        directory
        for directory in required_dirs
        if not (output_dir / directory).is_dir()
    ]

    if missing:
        die(
            "MadGraph returned success but the standalone_cpp "
            "output is incomplete. Missing directories: "
            + ", ".join(missing)
        )

    subprocess_dirs = sorted(
        entry.name
        for entry in (output_dir / "SubProcesses").iterdir()
        if entry.is_dir()
        and entry.name.startswith("P")
    )

    if not subprocess_dirs:
        die(
            "No P* subprocess directories were found under "
            f"{output_dir / 'SubProcesses'}."
        )

    return {
        "subprocess_count": len(subprocess_dirs),
        "subprocess_directories": subprocess_dirs,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate an MG5 standalone_cpp package from a UFO "
            "model and a list of Z2-odd particles without "
            "modifying the MadGraph installation."
        )
    )

    parser.add_argument(
        "--mg5-root",
        type=Path,
        required=True,
        help=(
            "MadGraph5_aMC root directory, for example "
            "/path/MG5_aMC_v3_6_7"
        ),
    )

    parser.add_argument(
        "--ufo",
        type=Path,
        required=True,
        help="Path to the UFO model directory.",
    )

    parser.add_argument(
        "--odd",
        nargs="+",
        help=(
            "Odd particles as UFO names and/or PDG codes. "
            "Example: --odd n1 n2 etp or --odd 1012 1014"
        ),
    )

    parser.add_argument(
        "--odd-file",
        type=Path,
        help=(
            "Text file containing odd particle names/PDGs "
            "separated by spaces, commas, or newlines."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help=(
            "Destination directory for the MadGraph "
            "standalone_cpp output."
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
            "multiparticle (default): one generate command "
            "using dm_odd/dm_even; explicit: one generate plus "
            "add-process commands for every odd-particle pair."
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
            "Allow MG5 subprocess grouping. Default is False "
            "to keep transparent P* directories."
        ),
    )

    parser.add_argument(
        "--require-version",
        default=DEFAULT_REQUIRED_MG5_VERSION,
        help=(
            "Required MG5 version. Default: "
            f"{DEFAULT_REQUIRED_MG5_VERSION}. "
            "Use --require-version any to disable this check."
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
            "Validate inputs and print the MG5 command card "
            "without running MadGraph."
        ),
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    required_version = (
        None
        if str(args.require_version).lower() == "any"
        else str(args.require_version)
    )

    mg5_exe, mg5_version = validate_mg5(
        args.mg5_root,
        required_version,
    )

    ufo_dir = validate_ufo_dir(args.ufo)
    particles = parse_ufo_particles(ufo_dir)

    odd_tokens = read_odd_tokens(args)

    odd_names, resolution_audit = resolve_odd_particles(
        odd_tokens,
        particles,
        auto_antiparticles=(
            not args.no_auto_antiparticles
        ),
    )

    even_names = build_even_particles(
        particles,
        odd_names,
    )

    output_dir = args.output.expanduser().resolve()

    if output_dir.exists():
        if not args.force:
            die(
                f"Output already exists: {output_dir}. "
                "Choose a new --output path or use --force."
            )

        safe_remove_output(output_dir)

    output_dir.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    command_text, pairs = build_mg5_commands(
        ufo_dir=ufo_dir,
        output_dir=output_dir,
        odd_names=odd_names,
        even_names=even_names,
        generation_mode=args.generation_mode,
        group_subprocesses=args.group_subprocesses,
    )

    run_stamp = (
        dt.datetime.now()
        .astimezone()
        .isoformat(timespec="seconds")
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

    print("=" * 72)
    print("MadGraph standalone_cpp generation")
    print("=" * 72)
    print(
        f"MG5 root          : "
        f"{args.mg5_root.expanduser().resolve()}"
    )
    print(f"MG5 executable    : {mg5_exe}")
    print(
        f"MG5 version       : "
        f"{mg5_version or 'unknown'}"
    )
    print(f"UFO model         : {ufo_dir}")
    print(f"Output            : {output_dir}")
    print(
        f"Generation mode   : "
        f"{args.generation_mode}"
    )
    print(
        f"group_subprocesses: "
        f"{args.group_subprocesses}"
    )
    print(
        f"Odd states        : "
        f"{' '.join(odd_names)}"
    )
    print(
        f"Even states       : "
        f"{len(even_names)}"
    )
    print(
        f"Odd pair count    : "
        f"{len(pairs)}"
    )
    print(
        f"Command card      : "
        f"{command_file}"
    )
    print("=" * 72)

    print("\nResolved odd-particle input:")

    for item in resolution_audit:
        extra = ""

        if item["auto_added_antiparticle"]:
            extra = (
                " (+ anti: "
                + item["auto_added_antiparticle"]
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
            "\nDRY RUN: MadGraph was not executed.\n"
        )
        print(command_text)
        return 0

    print("\nRunning MadGraph...\n")

    return_code = stream_process(
        [
            str(mg5_exe),
            str(command_file),
        ],
        log_file,
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

    shutil.copy2(
        command_file,
        output_dir / "generation_commands.mg5",
    )

    shutil.copy2(
        log_file,
        output_dir / "mg5_generation.log",
    )

    manifest = {
        "created_at": run_stamp,
        "mg5_root": str(
            args.mg5_root.expanduser().resolve()
        ),
        "mg5_executable": str(mg5_exe),
        "mg5_version": mg5_version,
        "ufo_model": str(ufo_dir),
        "output": str(output_dir),
        "generation_mode": args.generation_mode,
        "group_subprocesses": args.group_subprocesses,
        "auto_antiparticles": (
            not args.no_auto_antiparticles
        ),
        "odd_input": odd_tokens,
        "odd_resolution": resolution_audit,
        "odd_states_used": odd_names,
        "even_states_used": even_names,
        "odd_initial_pairs": [
            {
                "p1": p1,
                "p2": p2,
            }
            for p1, p2 in pairs
        ],
        **validation,
    }

    (
        output_dir
        / "generation_manifest.json"
    ).write_text(
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
        "\n".join(odd_names) + "\n",
        encoding="utf-8",
    )

    try:
        command_file.unlink()
    except FileNotFoundError:
        pass

    try:
        log_file.unlink()
    except FileNotFoundError:
        pass

    print("\n" + "=" * 72)
    print("SUCCESS")
    print("=" * 72)
    print(
        f"Standalone output : "
        f"{output_dir}"
    )
    print(
        f"Subprocesses      : "
        f"{validation['subprocess_count']}"
    )
    print(
        f"Manifest          : "
        f"{output_dir / 'generation_manifest.json'}"
    )
    print(
        f"MG5 commands      : "
        f"{output_dir / 'generation_commands.mg5'}"
    )
    print(
        f"MG5 log           : "
        f"{output_dir / 'mg5_generation.log'}"
    )
    print()
    print(
        "The output contains src/, lib/, and SubProcesses/ "
        "and is ready to be passed as the MG5 output folder "
        "to the CMake/Kerrigan pipeline."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
