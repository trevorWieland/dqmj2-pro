import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from project import ROOT, configuration, now, read_json, sha256, verify_inputs, write_json
from recovery_registry import batches, verify_sources


def match_reports():
    verify_sources()
    reports = []
    for item in batches():
        path = ROOT / item["report"]
        report = read_json(path)
        if item["report"] == "evidence/matches/checksum.json" or report.get("program") or report.get("processor") == "arm7" or report.get("module", "").startswith("arm7"):
            continue
        reports.append(path)
    return reports


def integrate(clean=False):
    config = configuration()
    inputs = verify_inputs(config)
    units = read_json(ROOT / "evidence/linking/checksum-units.json")
    units["units"][0]["sha256"] = sha256(ROOT / "oracle/matched.o")
    write_json(ROOT / "evidence/linking/checksum-units.json", units)
    snapshots = ROOT / "work/integration-inputs"
    snapshots.mkdir(parents=True, exist_ok=True)
    def snapshot(payload, suffix):
        destination = snapshots / (hashlib.sha256(payload).hexdigest() + suffix)
        if destination.exists() and destination.read_bytes() != payload:
            raise ValueError("Immutable integration input changed")
        if not destination.exists():
            destination.write_bytes(payload)
        return destination
    for unit in units["units"]:
        obj = snapshot((ROOT / unit["object"]).read_bytes(), ".o")
        unit["object"] = obj.relative_to(ROOT).as_posix()
        unit["sha256"] = sha256(obj)
    unit_snapshot = snapshot((json.dumps(units, indent=2) + "\n").encode(), ".json")
    command = [sys.executable, str(ROOT / "build_modules_context_v4_20261106.py"), "--source-units", unit_snapshot.relative_to(ROOT).as_posix()]
    if clean:
        command.append("--clean")
    reports = match_reports()
    input_reports = []
    for path in reports:
        pinned = snapshot(path.read_bytes(), ".json")
        input_reports.append({"path": path.relative_to(ROOT).as_posix(), "sha256": sha256(pinned), "snapshot": pinned.relative_to(ROOT).as_posix()})
        command.extend(["--source-matches", pinned.relative_to(ROOT).as_posix()])
    content = "\n".join(command[2:]) + "\n"
    argument_file = ROOT / "work/integration-arguments" / (hashlib.sha256(content.encode()).hexdigest() + ".txt")
    argument_file.parent.mkdir(parents=True, exist_ok=True)
    if argument_file.exists() and argument_file.read_text() != content:
        raise ValueError("Immutable integration arguments changed")
    argument_file.write_text(content)
    command = command[:2] + ["@" + str(argument_file)]
    started = time.monotonic()
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, errors="replace", timeout=900)
    log = ROOT / "logs/integration/latest.txt"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    report = {"schemaVersion": 1, "createdUtc": now(), "command": command, "elapsedSeconds": time.monotonic() - started, "timeoutSeconds": 900, "argumentFile": {"path": argument_file.relative_to(ROOT).as_posix(), "sha256": sha256(argument_file)}, "inputReports": input_reports, "checksumUnitSnapshot": unit_snapshot.relative_to(ROOT).as_posix(), "exitCode": result.returncode, "originalInputsUnchanged": inputs == verify_inputs(config)}
    write_json(ROOT / "evidence/verification/integration.json", report)
    stamp = report["createdUtc"].replace(":", "").replace(".", "").replace("+", "_")
    write_json(ROOT / f"evidence/verification/integration-{stamp}.json", report)
    if result.returncode:
        print(result.stdout[-4000:] + result.stderr[-8000:])
        raise RuntimeError("Module integration failed; full log in logs/integration/latest.txt")
    linked = read_json(ROOT / "evidence/linking/latest.json")
    if linked.get("failure") or not linked.get("allModuleBytesExact") or not linked.get("symbolCheckPassed") or not linked.get("mixedScaffoldingRomBuilt"):
        raise RuntimeError("Module, symbol or ROM construction did not succeed")
    product = ROOT / "build/link-work/roundtrip.nds"
    if not product.is_file() or sha256(product) != linked.get("mixedScaffoldingRomSha256"):
        raise RuntimeError("Constructed ROM is missing or stale")
    floor = read_json(ROOT / "evidence/verification/accepted-2026-10-27-start.json")
    linked_ranges = linked["sourceUnits"]
    for function in floor["functions"]:
        address = int(function["address"], 0)
        if not any(unit["module"] == function["module"] and int(unit["start"], 0) <= address and address + function["bytes"] <= int(unit["end"], 0) for unit in linked_ranges):
            raise RuntimeError("An earlier accepted function was omitted: " + function["id"])
        if sha256(ROOT / function["sourceUnit"]) != function["sourceSha256"]:
            raise RuntimeError("An earlier accepted source was changed: " + function["sourceUnit"])
    print({"reports": len(reports), "sourceUnits": len(linked_ranges), "sourceBytes": linked["sourceLinkedBytes"], "moduleComparisons": len(linked["modules"]), "allModuleBytesExact": linked["allModuleBytesExact"], "preservedEarlierFunctions": len(floor["functions"])})
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--clean", action="store_true")
    integrate(parser.parse_args().clean)
