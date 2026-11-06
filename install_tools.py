import concurrent.futures
import argparse
import hashlib
import importlib
import importlib.metadata
import json
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "tools/cache"
LOCK = ROOT / "tools.lock.json"
SPECS = {
    "objdiff": {
        "version": "3.8.3",
        "commit": "9aeec9cbab1a056ade7dc1f1625aacc41b0f8511",
        "url": "https://github.com/encounter/objdiff/releases/download/v3.8.3/objdiff-cli-windows-x86_64.exe",
        "sha256": "dd12dfb5e9e94a7f6c949a37e1815963cf2cffe4c87b4999b7ebc8c15b398a1f",
        "archive": "objdiff-cli-3.8.3.exe",
        "destination": "tools/objdiff/3.8.3",
    },
    "ghidra": {
        "version": "12.2",
        "url": "https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.2_build/ghidra_12.2_PUBLIC_20261016.zip",
        "sha256": "2c2cd776db3c1f6a097ba418922378ac3649cadd5e844a6f5f088ae628a7be67",
        "archive": "ghidra_12.2_PUBLIC_20261016.zip",
        "destination": "tools/ghidra",
    },
    "jdk": {
        "version": "25.0.5+8",
        "url": "https://github.com/adoptium/temurin25-binaries/releases/download/jdk-25.0.5%2B8/OpenJDK25U-jdk_x64_windows_hotspot_25.0.5_8.zip",
        "sha256": "636bdc13dc649ddc7d5921c5c7d23cca6e44fd19d662b45cc9c02135a6c96c42",
        "archive": "OpenJDK25U-jdk_x64_windows_hotspot_25.0.5_8.zip",
        "destination": "tools/jdk",
    },
    "m2c": {
        "version": "commit",
        "commit": "c632946b8cfbe8fce442b522dba92dfa72f1f317",
        "url": "https://codeload.github.com/matt-kempster/m2c/zip/c632946b8cfbe8fce442b522dba92dfa72f1f317",
        "sha256": "503714b92b14ba0e1affcc6decf4ad5763b37035cca66247858298cdf1b38971",
        "archive": "m2c-c632946b8cfbe8fce442b522dba92dfa72f1f317.zip",
        "destination": "tools/m2c",
    },
}


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def acquire(item):
    name, spec = item
    path = CACHE / spec["archive"]
    if not path.exists():
        temporary = path.with_suffix(path.suffix + ".part")
        request = urllib.request.Request(spec["url"], headers={"User-Agent": "private-j2p-tool-bootstrap"})
        print("Downloading", name, flush=True)
        with urllib.request.urlopen(request, timeout=120) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        temporary.replace(path)
    actual = digest(path)
    if spec["sha256"] and actual != spec["sha256"]:
        raise ValueError(f"Archive hash mismatch for {name}: {actual}")
    destination = ROOT / spec["destination"]
    destination.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            distribution_files = [destination / member.filename for member in archive.infolist() if not member.is_dir()]
            for member in archive.infolist():
                target = (destination / member.filename).resolve()
                if not target.is_relative_to(destination.resolve()):
                    raise ValueError("Unsafe archive member")
            marker = destination / ".extracted"
            if marker.exists() and marker.read_text(encoding="utf-8") != actual:
                raise ValueError("Existing extraction has different archive identity")
            if not marker.exists():
                archive.extractall(destination)
                marker.write_text(actual, encoding="utf-8")
    else:
        shutil.copy2(path, destination / "objdiff-cli.exe")
        distribution_files = [destination / "objdiff-cli.exe"]
    result = dict(spec)
    result["sha256"] = actual
    result["archiveBytes"] = path.stat().st_size
    result["files"] = {str(p.relative_to(ROOT)).replace("\\", "/"): digest(p) for p in distribution_files}
    result["hashSource"] = "observed-pinned-commit-archive" if name == "m2c" else "upstream-release-digest"
    result["executables"] = {
        str(p.relative_to(ROOT)).replace("\\", "/"): digest(p)
        for p in destination.rglob("*")
        if p.is_file() and (p.suffix.lower() in {".exe", ".bat"} or p.name == "m2c.py")
    }
    print("Installed", name, actual, flush=True)
    return name, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify", action="store_true")
    options = parser.parse_args()
    if options.verify:
        verify()
        return
    CACHE.mkdir(parents=True, exist_ok=True)
    previous = json.loads(LOCK.read_text()) if LOCK.exists() else {}
    for name, value in previous.get("tools", {}).items():
        if name in SPECS and SPECS[name]["sha256"] is None:
            SPECS[name]["sha256"] = value["sha256"]
    report = {"schemaVersion": 1, "date": "2026-10-26", "tools": {}}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for future in concurrent.futures.as_completed([pool.submit(acquire, item) for item in SPECS.items()]):
            name, result = future.result()
            old = previous.get("tools", {}).get(name, {})
            if old.get("sha256") == result["sha256"] and old.get("files") and old["files"] != result["files"]:
                raise ValueError("Installed tool content changed: " + name)
            report["tools"][name] = result
    wheels = list(CACHE.glob("graphviz-0.20.3-*.whl"))
    if not wheels:
        command = [sys.executable, "-m", "pip", "--isolated", "--disable-pip-version-check", "download", "--no-input", "--index-url", "https://pypi.org/simple", "--no-deps", "--dest", str(CACHE), "graphviz==0.20.3"]
        subprocess.run(command, check=True, timeout=120)
        wheels = list(CACHE.glob("graphviz-0.20.3-*.whl"))
    if len(wheels) != 1:
        raise ValueError("Expected one graphviz wheel")
    wheel = wheels[0]
    if digest(wheel) != "81f848f2904515d8cd359cc611faba817598d2feaac4027b266aa3eda7b3dde5":
        raise ValueError("Graphviz wheel hash mismatch")
    subprocess.run([sys.executable, "-m", "pip", "--isolated", "--disable-pip-version-check", "install", "--no-input", "--no-deps", "--no-index", "--upgrade", "--target", str(ROOT / "tools/m2c-python"), str(wheel)], check=True, timeout=120)
    report["pythonDependencies"] = [{"name": "graphviz", "version": "0.20.3", "archive": str(wheel.relative_to(ROOT)).replace("\\", "/"), "sha256": digest(wheel), "installedFileHashes": {str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in sorted((ROOT / "tools/m2c-python/graphviz").rglob("*.py"))}}]
    report["python"] = {"executable": sys.executable, "version": sys.version, "sha256": digest(Path(sys.executable))}
    for name, path, expected in [
        ("dsd", "tools/dsd.exe", "5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932"),
        ("mwccarm", "tools/mwccarm/mwccarm/2.0/base/mwccarm.exe", "7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880"),
        ("mwldarm", "tools/mwccarm/mwccarm/2.0/base/mwldarm.exe", "bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74"),
        ("mwasmarm", "tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe", "e928cbcce71d687fadf25cf426280f23252e2aaae897fc2ce4e5570d8554dc8c"),
    ]:
        actual = digest(ROOT / path)
        if actual != expected:
            raise ValueError("Baseline tool changed: " + name)
        report.setdefault("baselineExecutables", {})[name] = {"path": path, "sha256": actual}
    sys.path.insert(0, str(ROOT / "deps/native"))
    report["nativeDependencies"] = []
    for name in ["unicorn", "elftools", "capstone", "ndspy", "yaml"]:
        try:
            module = importlib.import_module(name)
            module_path = Path(module.__file__).resolve()
            files = {str(path.relative_to(ROOT)).replace("\\", "/"): digest(path) for path in sorted(module_path.parent.rglob("*")) if path.is_file() and path.suffix.lower() in {".py", ".pyd", ".dll"}}
            report["nativeDependencies"].append({"module": name, "importedVersion": getattr(module, "__version__", None), "file": str(module_path.relative_to(ROOT)).replace("\\", "/"), "fileHashes": files})
        except ImportError as failure:
            report["nativeDependencies"].append({"module": name, "available": False, "failure": str(failure)})
    report["distributionMetadata"] = [{"name": entry.metadata["Name"], "version": entry.version} for entry in importlib.metadata.distributions(path=[str(ROOT / "deps/native")])]
    enforce_existing_runtime(previous, report)
    if previous:
        verify()
    else:
        LOCK.write_text(json.dumps(report, indent=2), encoding="utf-8")


def enforce_existing_runtime(previous, report):
    if not previous:
        return
    for key in ("nativeDependencies", "pythonDependencies", "baselineExecutables"):
        if previous.get(key) != report.get(key):
            raise ValueError("Pinned runtime/dependency content changed: " + key)
    for key in ("version", "sha256"):
        if previous.get("python", {}).get(key) != report.get("python", {}).get(key):
            raise ValueError("Pinned Python runtime changed: " + key)


def verify():
    report = json.loads(LOCK.read_text())
    expected = {}
    for tool in report["tools"].values():
        expected[str(Path("tools/cache") / tool["archive"]).replace("\\", "/")] = tool["sha256"]
        expected.update(tool["files"])
    for tool in report["baselineExecutables"].values():
        expected[tool["path"]] = tool["sha256"]
    for dependency in report["pythonDependencies"]:
        expected[dependency["archive"]] = dependency["sha256"]
        expected.update(dependency["installedFileHashes"])
    for dependency in report["nativeDependencies"]:
        expected.update(dependency.get("fileHashes", {}))
    failures = []
    for relative, required in expected.items():
        path = (ROOT / relative).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            failures.append({"path": relative, "failure": "missing or outside repository"})
        elif digest(path) != required:
            failures.append({"path": relative, "failure": "SHA-256 mismatch"})
    if digest(Path(sys.executable)) != report["python"]["sha256"] or sys.version != report["python"]["version"]:
        failures.append({"path": sys.executable, "failure": "Python runtime identity mismatch"})
    print(json.dumps({"passed": not failures, "verifiedFiles": len(expected), "failures": failures}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
