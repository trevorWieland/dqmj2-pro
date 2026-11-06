import argparse
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path
from project import ROOT, configuration, sha256, verify_inputs

COMPILER_ARCHIVE = "dc386e37b2176e960954a733de928337d9b7e7620b9e94228008c31774339ace"
DSD_HASH = "5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932"


def private_copy(source, destination, expected):
    source = source.resolve()
    destination = destination.resolve()
    if not destination.is_relative_to(ROOT.resolve()):
        raise ValueError("Copy destination escapes repository")
    if sha256(source) != expected:
        raise ValueError("Supplied input identity differs: " + str(source))
    if destination.exists():
        if sha256(destination) != expected:
            raise ValueError("Refusing to replace a different existing private input")
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rom", type=Path)
    parser.add_argument("--save", type=Path)
    parser.add_argument("--dsd", type=Path)
    parser.add_argument("--compiler-archive", type=Path)
    parser.add_argument("--deps-source", type=Path)
    args = parser.parse_args()
    config = configuration()
    for name in ("rom", "save"):
        supplied = getattr(args, name)
        if supplied:
            private_copy(supplied, config[name], config[name + "Sha256"])
    if args.dsd:
        private_copy(args.dsd, config["dsd"], DSD_HASH)
    if args.compiler_archive:
        archive = ROOT / "tools/mwccarm.zip"
        private_copy(args.compiler_archive, archive, COMPILER_ARCHIVE)
        destination = ROOT / "tools/mwccarm"
        if not config["compiler"].exists():
            destination.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(archive) as stream:
                if any(not (destination / member.filename).resolve().is_relative_to(destination.resolve()) for member in stream.infolist()):
                    raise ValueError("Compiler archive path escapes destination")
                stream.extractall(destination)
    if args.deps_source and not config["deps"].exists():
        shutil.copytree(args.deps_source.resolve(), config["deps"], ignore=shutil.ignore_patterns("__pycache__"))
    verify_inputs(config)
    if sha256(config["dsd"]) != DSD_HASH:
        raise ValueError("Unexpected ds-decomp executable")
    if sha256(config["compiler"]) != "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880":
        raise ValueError("Unexpected compiler executable")
    if not (ROOT / "extract/config.yaml").exists():
        subprocess.run([str(config["dsd"]), "rom", "extract", "--rom", str(config["rom"]), "--output-path", str(ROOT / "extract")], cwd=ROOT, check=True, timeout=180)
    subprocess.run([sys.executable, str(ROOT / "install_tools.py")], cwd=ROOT, check=True, timeout=600)
    print("Private inputs and repository-local tool paths configured")
