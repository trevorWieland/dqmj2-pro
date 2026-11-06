import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "evidence/tools"
WORK = ROOT / "work/tool-validation"
M2C = ROOT / "tools/m2c/m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317/m2c.py"
GHIDRA = ROOT / "tools/ghidra/ghidra_12.2_PUBLIC"
JAVA = ROOT / "tools/jdk/jdk-25.0.5+8/bin/java.exe"
ENV = dict(os.environ, PYTHONPATH=str(ROOT / "tools/m2c-python"), PYTHONNOUSERSITE="1")
REPORT = {"schemaVersion": 1, "date": "2026-10-26", "validationScope": "Tool smoke tests; exact source matching is reported separately per probe", "wholeModuleLinked": False, "wholeRomMatched": False, "checks": []}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(name, command, timeout=60):
    record = {"name": name, "command": [str(x) for x in command], "timeoutSeconds": timeout}
    try:
        result = subprocess.run(command, cwd=ROOT, env=ENV, capture_output=True, timeout=timeout)
        output = result.stdout.decode("utf-8", errors="replace")
        error = result.stderr.decode("utf-8", errors="replace")
        (OUT / (name + ".stdout.txt")).write_text(output, encoding="utf-8")
        (OUT / (name + ".stderr.txt")).write_text(error, encoding="utf-8")
        record.update(returncode=result.returncode, passed=result.returncode == 0)
        REPORT["checks"].append(record)
        return result.returncode, output, error
    except subprocess.TimeoutExpired as failure:
        record.update(passed=False, failure="timeout", stdout=str(failure.stdout), stderr=str(failure.stderr))
        REPORT["checks"].append(record)
        return -1, "", "timeout"


def m2c_checks():
    source = (ROOT / "asm/_dsd_gap@main_3.s").read_text()
    cases = [("arm", "func_0207da70"), ("thumb", "func_0208b900")]
    for mode, symbol in cases:
        match = re.search(rf"{mode}_func_start {symbol}\n(.*?){mode}_func_end {symbol}", source, re.S)
        if not match:
            raise ValueError("Missing native assembly sample")
        body = "\n".join(line.split(";")[0].rstrip() for line in match.group(1).splitlines())
        adapted = ".text\n.global " + symbol + "\n" + body + "\n"
        path = OUT / ("m2c-" + mode + ".s")
        path.write_text(adapted, encoding="utf-8")
        command = [sys.executable, str(M2C), "--target", "arm-mwcc-c", "--comment-style", "none", "--no-cache", "--valid-syntax", "-f", symbol, str(path)]
        code, output, error = run("m2c-" + mode, command)
        (OUT / ("m2c-" + mode + "-draft.c")).write_text(output, encoding="utf-8")
        REPORT["checks"][-1].update(nativeAssemblySymbol=symbol, mode=mode, draftOnly=True, sourceMatched=False, adapter="function macros removed; semicolon comments removed; GNU .text/.global retained", inputSha256=digest(path))
        if code == 0 and ("Error" in error or "Error" in output or symbol + "(" not in output):
            REPORT["checks"][-1]["passed"] = False
            REPORT["checks"][-1]["failure"] = "CLI returned success without usable function draft"
        REPORT["checks"][-1]["contextProvided"] = False
        REPORT["checks"][-1]["semanticValidation"] = "Not accepted; ARM sample infers void and removes checksum accumulation without prototype context" if mode == "arm" else "Not behaviorally validated"
        context = OUT / ("m2c-" + mode + "-context.c")
        signature = "u32 " + symbol + "(u32 *arg0);" if mode == "arm" else "s32 " + symbol + "(void);"
        types = "typedef unsigned int u32;\ntypedef int s32;\n"
        context.write_text(types + signature + "\n", encoding="utf-8")
        code, output, error = run("m2c-" + mode + "-typed", command + ["--context", str(context)])
        draft = OUT / ("m2c-" + mode + "-typed-draft.c")
        draft.write_text(types + output, encoding="utf-8")
        REPORT["checks"][-1].update(contextProvided=True, draftOnly=True, sourceMatched=False)
        if code == 0:
            compile_draft(mode, symbol, draft)


def compile_draft(mode, symbol, draft):
    sys.path.insert(0, str(ROOT / "deps/native"))
    from elftools.elf.elffile import ELFFile
    metadata = json.loads((ROOT / "oracle/results.json").read_text())
    flags = metadata["compiler"]["flags"]
    compiler = ROOT / "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe"
    ENV["LM_LICENSE_FILE"] = str(ROOT / "tools/mwccarm/mwccarm/license.dat")
    obj = WORK / ("m2c-" + mode + ".o")
    command = [str(compiler), *flags, *(["-thumb"] if mode == "thumb" else []), "-c", str(draft), "-o", str(obj)]
    code, output, error = run("m2c-" + mode + "-compile", command)
    if code != 0:
        return
    address = 0x0207DA70 if mode == "arm" else 0x0208B900
    size = 48 if mode == "arm" else 4
    expected = (ROOT / "extract/arm9/arm9.bin").read_bytes()[address - 0x02000000:address - 0x02000000 + size]
    actual = None
    with obj.open("rb") as stream:
        elf = ELFFile(stream)
        for entry in elf.get_section_by_name(".symtab").iter_symbols():
            if entry.name == symbol:
                section = elf.get_section(entry["st_shndx"])
                actual = section.data()[entry["st_value"]:entry["st_value"] + entry["st_size"]]
    REPORT["checks"][-1].update(sourceMatched=actual == expected, expectedBytes=size, actualBytes=None if actual is None else len(actual), expectedSha256=hashlib.sha256(expected).hexdigest(), actualSha256=None if actual is None else hashlib.sha256(actual).hexdigest(), compilerFlags=flags + (["-thumb"] if mode == "thumb" else []), compilerSha256=digest(compiler), objectSha256=digest(obj), acceptance="Compiler success alone does not establish source match")


def ghidra_checks():
    project = WORK / "projects"
    project.mkdir(parents=True, exist_ok=True)
    private = WORK / "profile"
    private.mkdir(parents=True, exist_ok=True)
    vmargs = []
    for line in (GHIDRA / "support/launch.properties").read_text().splitlines():
        if line.startswith("VMARGS=") or line.startswith("VMARGS_WINDOWS="):
            vmargs.append(line.split("=", 1)[1])
    vmargs += ["-Xmx2G", "-XX:ParallelGCThreads=2", "-XX:CICompilerCount=2", f"-Duser.home={private}"]
    for key in ["settingsdir", "cachedir", "tempdir"]:
        path = private / key
        path.mkdir(exist_ok=True)
        vmargs.append(f"-Dapplication.{key}={path}")
    command = [str(JAVA), *vmargs, "-cp", str(GHIDRA / "Ghidra/Framework/Utility/lib/Utility.jar"), "ghidra.Ghidra", "ghidra.app.util.headless.AnalyzeHeadless"]
    modules = [("main", "extract/arm9/arm9.bin", "0x02000000", ["0x0207da70", "0", "0x0208b900", "1"]), ("ov000", "extract/arm9_overlays/ov000.bin", "0x021d7240", ["0x021d7240", "0"]), ("ov001", "extract/arm9_overlays/ov001.bin", "0x021d7240", ["0x021d7240", "0"])]
    identities = []
    for module, path, base, probes in modules:
        output = OUT / ("ghidra-" + module + "-identity.json")
        if output.exists():
            output.unlink()
        args = [str(project), "j2p-private", "-import", str(ROOT / path), "-overwrite", "-loader", "BinaryLoader", "-loader-baseAddr", base, "-processor", "ARM:LE:32:v5t", "-cspec", "default", "-noanalysis", "-scriptPath", str(OUT), "-postScript", "J2PIdentity.java", module, base, str(output), *probes, "-max-cpu", "2", "-log", str(OUT / ("ghidra-" + module + ".log"))]
        code, stdout, stderr = run("ghidra-" + module, command + args, timeout=180)
        if output.exists():
            identity = json.loads(output.read_text())
            identity["inputSha256"] = digest(ROOT / path)
            valid = identity["sha256"] == identity["inputSha256"] and int(identity["base"], 16) == int(base, 16)
            REPORT["checks"][-1]["passed"] = code == 0 and valid
            REPORT["checks"][-1]["identity"] = identity
            identities.append(identity)
        else:
            REPORT["checks"][-1].update(passed=False, failure="Identity script produced no JSON")
        (OUT / "validation.json").write_text(json.dumps(REPORT, indent=2), encoding="utf-8")
    REPORT["overlayIdentitySeparation"] = len(identities) == 3 and len({x["program"] for x in identities}) == 3 and identities[1]["base"] == identities[2]["base"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-ghidra", action="store_true")
    options = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    run("objdiff-version", [str(ROOT / "tools/objdiff/3.8.3/objdiff-cli.exe"), "--version"])
    run("jdk-version", [str(JAVA), "-version"])
    run("m2c-help", [sys.executable, str(M2C), "--help"])
    obj = ROOT / "oracle/matched.o"
    if obj.exists():
        code, stdout, stderr = run("objdiff-self", [str(ROOT / "tools/objdiff/3.8.3/objdiff-cli.exe"), "diff", "-1", str(obj), "-2", str(obj), "-o", str(OUT / "objdiff-self.json"), "save_payload_checksum"])
        REPORT["checks"][-1]["inputSha256"] = digest(obj)
        result_path = OUT / "objdiff-self.json"
        if result_path.exists():
            result = json.loads(result_path.read_text())
            matches = [entry.get("match_percent") for entry in result["left"]["symbols"] if entry["name"] == "save_payload_checksum"]
            REPORT["checks"][-1]["matchPercent"] = matches
            REPORT["checks"][-1]["passed"] = code == 0 and matches == [100.0]
    m2c_checks()
    (OUT / "validation.json").write_text(json.dumps(REPORT, indent=2), encoding="utf-8")
    if not options.skip_ghidra:
        ghidra_checks()
    REPORT["passed"] = all(x["passed"] for x in REPORT["checks"])
    (OUT / "validation.json").write_text(json.dumps(REPORT, indent=2), encoding="utf-8")
    print(json.dumps({"passed": REPORT["passed"], "checks": [{"name": x["name"], "passed": x["passed"]} for x in REPORT["checks"]]}, indent=2))
    if not REPORT["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
