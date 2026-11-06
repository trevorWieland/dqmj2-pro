import json
import os
import struct
import subprocess
from pathlib import Path

from compile_android_checks_20261029 import BIN, TOOLCHAIN, TARGET, ENV_NAMES
from ledger_state import collect_matches
from project import ROOT, configuration, now, sha256, write_json

WORK = ROOT / "build/android-candidates-20261029"
REPORT = ROOT / "evidence/portability/android-next-candidates-20261029.json"
CANDIDATES = {
    "src/mechanics_save/sdk_crc.c": {
        "priority": 1, "contract": "Typed host-owned tables/state/input; six pure CRC helpers",
        "dependencies": [], "testPlan": "All256 table entries; empty/split/boundary-length updates; independent bitwise models",
        "limitations": "Require aligned u16/u32 state/table objects and exact polynomial/truncation semantics"},
    "src/mechanics_save/runtime_rng.c": {
        "priority": 2, "contract": "Explicitly initialized private u32 state; one deterministic state transition",
        "dependencies": ["native_rng_state: host-owned aligned unsigned32 object"],
        "testPlan": "Boundary seeds and signed limits<=0/1/17/1024/INT_MAX; compare result and updated state",
        "limitations": "Seed inputs are synthetic; no live scene prediction or persistent seed claim; isolate concurrent callers"},
    "src/mechanics_save/sdk_md5_block.c": {
        "priority": 3, "contract": "Aligned32-bit MD5 state and64-byte block with measured readonly constants/index arrays",
        "dependencies": ["native_md5_constants", "native_md5_indices"],
        "testPlan": "Native block-transform vectors; all-zero/all-set/ramp/random state and blocks",
        "limitations": "Resolve actual table symbols without stubs; preserve little-endian block representation"},
    "src/mechanics_save/sdk_md5.c": {
        "priority": 4, "contract": "88-byte MD5 context with count offset16/buffer offset24, typed host storage",
        "dependencies": ["native_copy(source,destination,length)", "native_fill", "native_md5_compress", "native_md5_padding"],
        "testPlan": "Native reference streaming splits at0/1/55/56/63/64/65 bytes and multi-block sizes; digest and cleared context",
        "limitations": "Assert sizeof/alignof/offsetof; implement actual copy/fill contracts and qualified compressor; no zero stubs"},
}


def main():
    namespace = configuration()["romSha256"]
    matches, rejected = collect_matches(namespace)
    tools = json.loads((ROOT / "evidence/toolchains/android-ndk-r30-20261029.json").read_text())
    clang = BIN / "clang.exe"
    pinned = tools["provenance"]["smoke-canonical.json"]["report"]["results"][0]
    if sha256(clang) != pinned["sha256"]:
        raise ValueError("Candidate compiler differs from the adopted official pin")
    results = []
    for source_name, plan in CANDIDATES.items():
        entries = [entry for entry in matches.values() if entry.get("source") == source_name]
        if not entries:
            raise ValueError("Candidate lacks a current exact DS source match: " + source_name)
        source = ROOT / source_name
        folder = WORK / source.stem
        folder.mkdir(parents=True, exist_ok=True)
        snapshot = folder / source.name
        snapshot.write_bytes(source.read_bytes())
        temporary = folder / "temporary"
        temporary.mkdir(exist_ok=True)
        environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
        environment.update(TMP=str(temporary), TEMP=str(temporary), SOURCE_DATE_EPOCH="0")
        output = folder / (source.stem + ".o")
        arguments = [str(clang), "--target=" + TARGET, "--sysroot=" + str(TOOLCHAIN / "sysroot"),
                     "-std=c11", "-O2", "-fPIC", "-Wall", "-Wextra", "-Werror", "-c", str(snapshot), "-o", str(output)]
        process = subprocess.run(arguments, cwd=folder, env=environment, capture_output=True,
                                 text=True, timeout=120)
        compiled = process.returncode == 0
        if compiled:
            header = output.read_bytes()[:64]
            if header[:6] != b"\x7fELF\x02\x01" or struct.unpack_from("<HH", header, 16) != (1, 183):
                raise ValueError("Candidate object is not AArch64 ELF64 little-endian relocatable")
        native_entries = [{"processor": "arm9", "module": entry["module"], "mode": entry["mode"],
                           "address": hex(entry["address"]), "bytes": entry["bytes"], "name": entry["name"],
                           "nativeSpanSha256": entry["targetSha256"], "sourceSha256": entry["sourceSha256"],
                           "existingMatchReport": entry["report"],
                           "existingMatchReportSha256": sha256(ROOT / entry["report"])} for entry in entries]
        results.append({**plan, "source": source_name, "sourceSha256": sha256(source),
                        "snapshot": str(snapshot.relative_to(ROOT)), "nativeEntries": native_entries,
                        "command": arguments, "cwd": str(folder), "returncode": process.returncode,
                        "stdout": process.stdout, "stderr": process.stderr,
                        "androidObjectCompile": "passed" if compiled else "failed",
                        "object": str(output.relative_to(ROOT)) if compiled else None,
                        "objectSha256": sha256(output) if compiled else None,
                        "androidLink": "not-run-unresolved-suite-dependencies",
                        "androidExecution": "not-run-no-Android-target", "newDsSourceCredit": 0})
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": namespace,
              "target": TARGET, "compilerSha256": sha256(clang), "candidates": results,
              "existingDsFunctionsCoveredByCandidateSources": sum(len(row["nativeEntries"]) for row in results),
              "objectCompilesPassed": sum(row["androidObjectCompile"] == "passed" for row in results),
              "androidComparisonsExecuted": 0, "dsSourceCredit": 0,
              "reproduction": "python compile_android_candidates_20261029.py",
              "generatorSha256": sha256(Path(__file__))}
    write_json(REPORT, report)
    print(json.dumps({"sourceUnits": len(results), "objectsCompiled": report["objectCompilesPassed"],
                      "existingDsFunctions": report["existingDsFunctionsCoveredByCandidateSources"],
                      "androidExecution": "not-run"}))


if __name__ == "__main__":
    main()
