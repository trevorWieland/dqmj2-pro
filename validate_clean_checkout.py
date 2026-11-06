import argparse
import json
import shutil
import subprocess
import sys
import tarfile
from pathlib import Path
from project import ROOT, now, read_json, sha256, write_json
from clean_reference_policy_parallel_wave20261102 import committed_reference_pins, validate_source_paths, verify_reference_copy


def run(command, cwd, log, timeout):
    with log.open("w", encoding="utf-8") as output:
        result = subprocess.run(command, cwd=cwd, stdout=output, stderr=subprocess.STDOUT, timeout=timeout)
    return {"command": command, "cwd": str(cwd), "exitCode": result.returncode, "log": str(log), "logSha256": sha256(log)}


def materialize(target):
    target = target.resolve()
    if target.exists() or target.is_relative_to(ROOT) or ROOT.is_relative_to(target):
        raise ValueError("Fresh checkout requires a new separate private directory")
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    tracked = subprocess.run(["git", "ls-tree", "-r", "--name-only", "-z", revision], cwd=ROOT, check=True, capture_output=True).stdout.decode().split("\0")
    paths = [Path(value) for value in tracked if value]
    reference_pins = committed_reference_pins(ROOT, revision)
    validate_source_paths(paths, reference_pins)
    target.mkdir(parents=True)
    archive = target / ".source-snapshot.tar"
    subprocess.run(["git", "archive", "--format=tar", "--output=" + str(archive), revision], cwd=ROOT, check=True)
    with tarfile.open(archive) as stream:
        for member in stream.getmembers():
            if not (target / member.name).resolve().is_relative_to(target) or member.issym() or member.islnk():
                raise ValueError("Committed source archive contains an escaping path or dependency link")
        stream.extractall(target, filter="data")
    archive.unlink()
    sources = []
    for relative in paths:
        destination = target / relative
        digest = sha256(destination)
        sources.append({"path": relative.as_posix(), "sha256": digest})
    inputs = []
    for directory in ("tools", "deps", "inputs"):
        source_root = ROOT / directory
        for source in source_root.rglob("*"):
            if not source.is_file() or "__pycache__" in source.parts:
                continue
            if source.is_symlink():
                raise ValueError("Fresh dependencies cannot depend on links")
            relative = source.relative_to(ROOT)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if verify_reference_copy(relative, source, destination, reference_pins):
                continue
            shutil.copy2(source, destination)
            inputs.append({"path": relative.as_posix(), "sha256": sha256(destination)})
    subprocess.run(["git", "init", "--quiet", str(target)], check=True)
    return {"sourceRevision": revision, "sourceFromCommittedTree": True, "sourceFiles": sources, "inputFiles": inputs, "committedReferenceSources": reference_pins, "copiedCachedObjects": 0, "copiedGeneratedExtraction": False, "dependencyLinks": 0}



def archive_previous_checks(target, log_dir):
    current = target / "evidence/verification/checks.json"
    if not current.exists():
        return None
    archived = log_dir / "historical-checks-from-source-snapshot.json"
    if not current.resolve().is_relative_to(target.resolve()) or not archived.resolve().is_relative_to(target.resolve()) or archived.exists():
        raise ValueError("Unsafe historical clean-check report path")
    digest = sha256(current)
    current.rename(archived)
    return {"path": str(archived), "sha256": digest}


def current_checks(target, exit_code):
    checks = read_json(target / "evidence/verification/checks.json")
    if exit_code not in (0, 1):
        raise ValueError("Clean checker process did not finish with a supported status")
    if (exit_code == 0) != bool(checks["allChecksPassed"]):
        raise ValueError("Clean checker exit status contradicts its current report")
    return checks


def main(target, timeout):
    report = {"schemaVersion": 1, "createdUtc": now(), "target": str(target.resolve()), "sourceReconstructionComplete": False, "steps": []}
    evidence = ROOT / "evidence/verification/clean-checkout.json"
    try:
        report["snapshot"] = materialize(target)
        log_dir = target / "logs/clean-checkout"
        log_dir.mkdir(parents=True)
        report["steps"].append(run([sys.executable, str(target / "configure.py")], target.parent, log_dir / "configure.txt", 900))
        if report["steps"][-1]["exitCode"]:
            raise ValueError("Fresh configure failed")
        report["archivedHistoricalCheckReport"] = archive_previous_checks(target, log_dir)
        report["steps"].append(run([sys.executable, str(target / "run_checks.py"), "--clean", "--tools"], target.parent, log_dir / "checks.txt", timeout))
        checks = current_checks(target, report["steps"][-1]["exitCode"])
        report["checks"] = checks
        report["freshBuildAndOracleChecksPassed"] = checks["buildAndOracleChecksPassed"]
        report["allChecksPassed"] = checks["allChecksPassed"]
        report["manifest"] = read_json(target / "manifest.json")
        if not report["freshBuildAndOracleChecksPassed"]:
            raise ValueError("Fresh build/oracle regression failed")
    except Exception as error:
        report["failure"] = f"{type(error).__name__}: {error}"
        raise
    finally:
        write_json(evidence, report)
        stamp = report["createdUtc"].replace(":", "").replace(".", "").replace("+", "_")
        write_json(evidence.with_name("clean-checkout-" + stamp + ".json"), report)
    print(json.dumps({key: report[key] for key in ("target", "freshBuildAndOracleChecksPassed", "allChecksPassed")}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("--timeout", type=int, default=14400)
    args = parser.parse_args()
    main(args.target, args.timeout)
