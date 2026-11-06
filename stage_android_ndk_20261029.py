import argparse
import hashlib
import json
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

from project import ROOT, now, sha256, write_json

STAGE = ROOT / "build/android-toolchain-staging/20261029-r30"
URL = "https://dl.google.com/android/repository/android-ndk-r30-windows.zip"
PUBLISHER = "https://developer.android.com/ndk/downloads"
CHANGELOG = "https://github.com/android/ndk/wiki/Changelog-r30"
BYTES = 727980788
SHA1 = "9bf167a1985fa7d4a036186b78f702eab9179408"
REVISION = "30.0.16248370"
ARCHIVE = STAGE / "android-ndk-r30-windows.zip"
NDK = STAGE / "android-ndk-r30"
CANONICAL_NDK = ROOT / "tools/android-ndk/r30"


def check_space(required):
    space = shutil.disk_usage(ROOT)
    if space.free < required:
        raise ValueError("Insufficient workspace-volume capacity")
    return {"total": space.total, "used": space.used, "free": space.free,
            "requiredFreeBytes": required}


def hashes(path):
    first, second = hashlib.sha1(), hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            first.update(block)
            second.update(block)
    return {"bytes": path.stat().st_size, "sha1": first.hexdigest(), "sha256": second.hexdigest()}


def download():
    STAGE.mkdir(parents=True, exist_ok=True)
    if not STAGE.resolve().is_relative_to((ROOT / "build").resolve()):
        raise ValueError("Toolchain staging escaped the repository build directory")
    space = check_space(12 * 1024 ** 3)
    request = urllib.request.Request(PUBLISHER, headers={"User-Agent": "J2P-private-build-validation"})
    with urllib.request.urlopen(request, timeout=60) as response:
        page = response.read()
    text = page.decode("utf-8")
    if REVISION not in text or SHA1 not in text or str(BYTES) not in text:
        raise ValueError("Current official NDK metadata differs from the selected pin")
    (STAGE / "official-downloads.html").write_bytes(page)
    partial = ARCHIVE.with_suffix(".zip.partial")
    headers = {}
    if not ARCHIVE.exists():
        with urllib.request.urlopen(URL, timeout=60) as response, partial.open("wb") as output:
            headers = dict(response.headers)
            if response.status != 200:
                raise ValueError("Official NDK artifact did not return HTTP200")
            count = 0
            while block := response.read(8 * 1024 * 1024):
                output.write(block)
                count += len(block)
                if count > BYTES:
                    raise ValueError("Official NDK download exceeds its published size")
        measured = hashes(partial)
        if measured["bytes"] != BYTES or measured["sha1"] != SHA1:
            raise ValueError("Downloaded official NDK artifact fails publisher identity")
        partial.replace(ARCHIVE)
    measured = hashes(ARCHIVE)
    if measured["bytes"] != BYTES or measured["sha1"] != SHA1:
        raise ValueError("Existing staged NDK artifact differs from publisher identity")
    result = {"schemaVersion": 1, "createdUtc": now(), "version": "r30", "revision": REVISION,
              "url": URL, "publisherMetadata": PUBLISHER, "changelog": CHANGELOG,
              "publisherBytes": BYTES, "publisherSha1": SHA1, "measured": measured,
              "httpHeaders": headers, "diskBeforeDownload": space,
              "officialMetadataSha256": sha256(STAGE / "official-downloads.html"),
              "archive": str(ARCHIVE.relative_to(ROOT)), "stage": str(STAGE.relative_to(ROOT)),
              "installedIntoTools": False, "execution": "not-run-no-Android-target",
              "generatorSha256": sha256(Path(__file__))}
    write_json(STAGE / "download.json", result)
    print(json.dumps({"stage": str(STAGE.relative_to(ROOT)), **measured}), flush=True)


def extract():
    identity = hashes(ARCHIVE)
    if identity["bytes"] != BYTES or identity["sha1"] != SHA1:
        raise ValueError("Staged archive changed before extraction")
    with zipfile.ZipFile(ARCHIVE) as archive:
        entries = archive.infolist()
        total = sum(entry.file_size for entry in entries)
        space = check_space(total + 2 * 1024 ** 3)
        for entry in entries:
            parts = PurePosixPath(entry.filename.replace("\\", "/")).parts
            if not parts or parts[0] != "android-ndk-r30" or ".." in parts:
                raise ValueError("Unexpected path in official toolchain archive")
            target = STAGE.joinpath(*parts).resolve()
            if not target.is_relative_to(NDK.resolve()):
                raise ValueError("Toolchain extraction escaped its private root")
        archive.extractall(STAGE)
    properties = (NDK / "source.properties").read_text()
    if f"Pkg.Revision = {REVISION}" not in properties:
        raise ValueError("Extracted NDK revision differs from the official pin")
    result = {"createdUtc": now(), "archive": identity, "archiveEntries": len(entries),
              "archiveUncompressedBytes": total, "diskBeforeExtraction": space,
              "sourceProperties": properties, "sourcePropertiesSha256": sha256(NDK / "source.properties"),
              "ndkRoot": str(NDK.relative_to(ROOT)), "installedIntoTools": False,
              "generatorSha256": sha256(Path(__file__))}
    write_json(STAGE / "extraction.json", result)
    print(json.dumps({"ndk": str(NDK.relative_to(ROOT)), "files": len(entries),
                      "uncompressedBytes": total}), flush=True)


def smoke():
    selected = CANONICAL_NDK if CANONICAL_NDK.exists() else NDK
    binary = selected / "toolchains/llvm/prebuilt/windows-x86_64/bin"
    results = []
    for name in ("clang.exe", "ld.lld.exe", "llvm-ar.exe", "llvm-readelf.exe"):
        executable = binary / name
        command = [str(executable), "--version"]
        process = subprocess.run(command, cwd=STAGE, capture_output=True, text=True, timeout=60)
        if process.returncode:
            raise ValueError({"command": command, "returncode": process.returncode,
                              "stdout": process.stdout, "stderr": process.stderr})
        results.append({"path": str(executable.relative_to(ROOT)), "sha256": sha256(executable),
                        "command": command, "returncode": process.returncode,
                        "stdout": process.stdout, "stderr": process.stderr})
    result = {"createdUtc": now(), "ndkRevision": REVISION, "results": results,
              "installedIntoTools": selected == CANONICAL_NDK,
              "androidExecution": "not-run-no-Android-target",
              "generatorSha256": sha256(Path(__file__))}
    write_json(STAGE / ("smoke-canonical.json" if selected == CANONICAL_NDK else "smoke.json"), result)
    print(json.dumps({"smokeTestsPassed": len(results)}), flush=True)


def adopt():
    if CANONICAL_NDK.exists():
        raise ValueError("Canonical Android NDK destination already exists; no overwrite is permitted")
    if not NDK.resolve().is_relative_to((ROOT / "build/android-toolchain-staging").resolve()):
        raise ValueError("Unexpected staging source for toolchain adoption")
    if not CANONICAL_NDK.resolve().is_relative_to((ROOT / "tools/android-ndk").resolve()):
        raise ValueError("Unexpected canonical target for toolchain adoption")
    staged = json.loads((STAGE / "smoke.json").read_text())
    for tool in staged["results"]:
        if sha256(ROOT / tool["path"]) != tool["sha256"]:
            raise ValueError("Staged executable changed before adoption")
    CANONICAL_NDK.parent.mkdir(parents=True, exist_ok=True)
    NDK.rename(CANONICAL_NDK)
    adopted = []
    for tool in staged["results"]:
        target = CANONICAL_NDK / (ROOT / tool["path"]).relative_to(NDK)
        if sha256(target) != tool["sha256"]:
            raise ValueError("Adopted tool identity differs from staging")
        adopted.append({"path": str(target.relative_to(ROOT)), "sha256": tool["sha256"]})
    result = {"createdUtc": now(), "from": str(NDK.relative_to(ROOT)),
              "to": str(CANONICAL_NDK.relative_to(ROOT)), "tools": adopted,
              "archive": hashes(ARCHIVE), "sourcePropertiesSha256": sha256(CANONICAL_NDK / "source.properties"),
              "parentSnapshotGate": "Explicit coordinator confirmation received after cleanG materialization",
              "systemChanges": False, "pathChanges": False,
              "generatorSha256": sha256(Path(__file__))}
    write_json(STAGE / "adoption.json", result)
    print(json.dumps({"adopted": str(CANONICAL_NDK.relative_to(ROOT)), "verifiedExecutables": len(adopted)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("download", "extract", "smoke", "adopt"))
    action = parser.parse_args().action
    {"download": download, "extract": extract, "smoke": smoke, "adopt": adopt}[action]()
