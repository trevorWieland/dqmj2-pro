import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import uuid
from pathlib import Path

from project import ROOT, configuration, now, sha256, write_json
from stage_android_ndk_20261029 import CANONICAL_NDK, STAGE, REVISION, ARCHIVE

WORK = ROOT / "build/android-arm64-validation-20261029"
REPORT = ROOT / "evidence/portability/android-arm64-compile-20261029.json"
NDK_SHA256 = "b830098aaf18b67a42eb831c404e15e5f2990a474f054ac145b0bc957ac6d729"
TARGET = "aarch64-linux-android33"
SOURCE_FILES = [
    "src/save_checksum.c", "ports/android-native/checksum_runner.c",
    "ports/android-native/generated/checksum_vectors.h", "ports/android-native/CMakeLists.txt",
]
TOOLCHAIN = CANONICAL_NDK / "toolchains/llvm/prebuilt/windows-x86_64"
BIN = TOOLCHAIN / "bin"
ENV_NAMES = ["CPATH", "C_INCLUDE_PATH", "CPLUS_INCLUDE_PATH", "OBJC_INCLUDE_PATH",
             "LIBRARY_PATH", "COMPILER_PATH", "SDKROOT", "INCLUDE", "LIB", "LIBPATH"]


def command(arguments, directory, name, environment, input_text=None, log_directory=None):
    process = subprocess.run([str(arg) for arg in arguments], cwd=directory, env=environment,
                             capture_output=True, text=True, input=input_text, timeout=120)
    record = {"arguments": [str(arg) for arg in arguments], "cwd": str(directory),
              "returncode": process.returncode, "stdout": process.stdout, "stderr": process.stderr}
    write_json((log_directory or directory) / (name + ".json"), record)
    if process.returncode:
        raise ValueError(record)
    return record


def inspect_elf(path):
    data = path.read_bytes()
    if data[:6] != b"\x7fELF\x02\x01":
        raise ValueError("Expected little-endian ELF64")
    fields = struct.unpack_from("<HHIQQQIHHHHHH", data, 16)
    kind, machine, version, entry, phoff, shoff, flags, ehsize, phsize, phcount = fields[:10]
    if kind != 3 or machine != 183 or version != 1 or phsize != 56:
        raise ValueError("Android runner is not an AArch64 position-independent ELF executable")
    loads, notes, interpreter = [], [], None
    stack_flags = None
    for index in range(phcount):
        item = struct.unpack_from("<IIQQQQQQ", data, phoff + index * phsize)
        segment, permissions, offset, address, physical, files, memory, alignment = item
        if offset + files > len(data) or files > memory:
            raise ValueError("ELF segment exceeds its measured bounds")
        if segment == 1:
            if alignment < 16384 or alignment & (alignment - 1):
                raise ValueError("ELF LOAD alignment is below16KiB or is not a power of two")
            if offset % alignment != address % alignment or permissions & 3 == 3:
                raise ValueError("ELF LOAD congruence or write/execute permissions invalid")
            loads.append({"offset": offset, "address": address, "fileBytes": files,
                          "memoryBytes": memory, "flags": permissions, "alignment": alignment})
        elif segment == 3:
            interpreter = data[offset:offset + files].rstrip(b"\0").decode("ascii")
        elif segment == 4:
            position = offset
            while position + 12 <= offset + files:
                name_size, description_size, note_kind = struct.unpack_from("<III", data, position)
                position += 12
                name = data[position:position + name_size].rstrip(b"\0").decode("ascii")
                position += (name_size + 3) & ~3
                description = data[position:position + description_size]
                position += (description_size + 3) & ~3
                note = {"owner": name, "type": note_kind, "descriptionHex": description.hex()}
                if name == "Android" and note_kind == 1 and len(description) >= 4:
                    note["androidApi"] = struct.unpack_from("<I", description)[0]
                    if len(description) >= 132:
                        note["ndkVersion"] = description[4:68].split(b"\0", 1)[0].decode("ascii")
                        note["ndkBuild"] = description[68:132].split(b"\0", 1)[0].decode("ascii")
                notes.append(note)
        elif segment == 0x6474E551:
            stack_flags = permissions
    android_notes = [note for note in notes if note.get("androidApi") == 33]
    if not loads or not android_notes or interpreter != "/system/bin/linker64":
        raise ValueError("Missing Android API33 identity, LOAD segments or64-bit Android interpreter")
    if stack_flags is None or stack_flags & 1:
        raise ValueError("Android runner has missing/execute-enabled GNU stack policy")
    if not any(note.get("ndkVersion") == "r30" and note.get("ndkBuild") == "16248370"
               for note in android_notes):
        raise ValueError("Android CRT note differs from the adopted NDK revision")
    return {"elfClass": 64, "byteOrder": "little", "machine": "EM_AARCH64",
            "type": "ET_DYN", "entry": entry, "interpreter": interpreter,
            "loads": loads, "notes": notes, "gnuStackFlags": stack_flags,
            "androidApi": 33, "abi": "arm64-v8a", "runtimeExecuted": False}


def dependency_paths(path):
    text = re.sub(r"\\\r?\n", " ", path.read_text())
    body = text.split(": ", 1)[1]
    return [Path(value.replace("\\:", ":")) for value in body.split()]


def input_identity(path, source_root):
    resolved = path.resolve()
    if resolved.is_relative_to(CANONICAL_NDK):
        scope = "official-pinned-NDK"
        relative = resolved.relative_to(CANONICAL_NDK).as_posix()
    elif resolved.is_relative_to(source_root):
        scope = "unchanged-source-snapshot"
        relative = resolved.relative_to(source_root).as_posix()
    elif resolved.is_relative_to(WORK):
        scope = "new-build-artifact"
        relative = resolved.relative_to(WORK).as_posix()
    else:
        raise ValueError("Undeclared external build input: " + str(resolved))
    return {"scope": scope, "path": relative, "bytes": resolved.stat().st_size,
            "sha256": sha256(resolved)}


def build(directory, source_root, cwd_root):
    directory.mkdir(parents=True, exist_ok=True)
    temporary = directory / "temporary"
    temporary.mkdir(exist_ok=True)
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    environment.update(TMP=str(temporary), TEMP=str(temporary), SOURCE_DATE_EPOCH="0")
    common = [BIN / "clang.exe", "--target=" + TARGET, "--sysroot=" + str(TOOLCHAIN / "sysroot")]
    compile_flags = ["-std=c11", "-O2", "-fPIE", "-Wall", "-Wextra", "-Werror"]
    operations = []
    for label, relative in [("core", "src/save_checksum.c"),
                            ("runner", "ports/android-native/checksum_runner.c")]:
        arguments = common + compile_flags + ["-MD", "-MT", label, "-MF", directory / (label + ".d"),
                                               "-c", source_root / relative, "-o", directory / (label + ".o")]
        operations.append(command(arguments, cwd_root, label + "-compile", environment,
                                  log_directory=directory))
    archive = directory / "libj2p_checksum_core.a"
    operations.append(command([BIN / "llvm-ar.exe", "rcD", archive, directory / "core.o"],
                              cwd_root, "core-archive", environment, log_directory=directory))
    output = directory / "j2p_portable_checks"
    arguments = common + ["-fPIE", "-pie", "-v", "-Wl,--trace", directory / "runner.o", archive, "-o", output]
    operations.append(command(arguments, cwd_root, "link", environment, log_directory=directory))
    operations.append(command([BIN / "llvm-readelf.exe", "--all", output], cwd_root, "readelf",
                              environment, log_directory=directory))
    macro_command = common + ["-dM", "-E", "-x", "c", "-"]
    macros = command(macro_command, cwd_root, "target-macros", environment, "", directory)
    operations.append(macros)
    definitions = dict(re.findall(r"^#define (\w+) (.+)$", macros["stdout"], re.M))
    resolved = {}
    for name, expected in {"__ANDROID__": "1", "__ANDROID_API__": "33", "__aarch64__": "1",
                           "__SIZEOF_POINTER__": "8", "__SIZEOF_INT__": "4", "__CHAR_BIT__": "8"}.items():
        value = definitions.get(name)
        for unused in range(8):
            if value not in definitions:
                break
            value = definitions[value]
        resolved[name] = value
        if value != expected:
            raise ValueError("Compiler ABI/API definition differs: " + name)
    headers = set()
    for label in ("core", "runner"):
        headers.update(dependency_paths(directory / (label + ".d")))
    link_inputs = set()
    for line in operations[3]["stdout"].splitlines():
        value = re.sub(r"\([^()]*\)$", "", line.strip())
        candidate = Path(value)
        if candidate.is_file():
            link_inputs.add(candidate)
    if not any("crtbegin_dynamic.o" in str(path) for path in link_inputs):
        raise ValueError("Link trace did not identify the actual Android CRT input")
    dynamic = operations[4]["stdout"]
    needed = re.findall(r"\(NEEDED\).*?\[([^]]+)\]", dynamic)
    if "libc.so" not in needed:
        raise ValueError("Expected Android C runtime dependency is absent")
    if not all(name in dynamic for name in ("save_payload_checksum", "save_header_checksum", " main")):
        raise ValueError("ELF symbols do not contain both checksum functions and the runner")
    if not re.search(r"\(FLAGS_1\).*?PIE", dynamic):
        raise ValueError("Android executable lacks its explicit dynamic PIE flag")
    return {"directory": str(directory.relative_to(ROOT)), "cwd": str(cwd_root),
            "operations": operations, "binary": str(output.relative_to(ROOT)),
            "binarySha256": sha256(output), "binaryBytes": output.stat().st_size,
            "elf": inspect_elf(output), "dtNeeded": needed, "dynamicPieFlag": True,
            "sourceAndHeaderClosure": [input_identity(path, source_root) for path in sorted(headers)],
            "actualLinkInputClosure": [input_identity(path, source_root) for path in sorted(link_inputs)],
            "compilerDefinitions": definitions, "resolvedAbiDefinitions": resolved,
            "environmentNamesClearedForChild": ENV_NAMES,
            "childTemporaryDirectory": str(temporary), "androidExecution": "not-run-no-Android-target"}


def main():
    if sha256(ARCHIVE) != NDK_SHA256:
        raise ValueError("Official staged archive no longer matches the independently measured SHA256 pin")
    if f"Pkg.Revision = {REVISION}" not in (CANONICAL_NDK / "source.properties").read_text():
        raise ValueError("Canonical NDK revision changed")
    smoke_path = STAGE / "smoke-canonical.json"
    smoke = json.loads(smoke_path.read_text())
    for tool in smoke["results"]:
        if sha256(ROOT / tool["path"]) != tool["sha256"]:
            raise ValueError("Canonical Android compiler/binutils changed since smoke validation")
    original_report = ROOT / "evidence/portability/android-checksum-bundle-20261029.json"
    bundle = json.loads(original_report.read_text())
    pins = {row["path"]: row["sha256"] for row in bundle["artifacts"]}
    source_root = WORK / "source"
    for relative in SOURCE_FILES:
        source = ROOT / relative
        if sha256(source) != pins[relative]:
            raise ValueError("Checksum runner/source/goldens changed since native bundle validation")
        destination = source_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    run_root = WORK / ("run-" + uuid.uuid4().hex[:12])
    run_root.mkdir()
    results = [build(run_root / "cleanA", source_root, ROOT),
               build(run_root / "cleanB", source_root, WORK)]
    if results[0]["binarySha256"] != results[1]["binarySha256"]:
        raise ValueError("Independent clean cross-builds produced different Android ELF bytes")
    for relative in SOURCE_FILES:
        if sha256(ROOT / relative) != pins[relative]:
            raise ValueError("Original checksum/port source changed during validation")
    properties = ["source.properties", "meta/platforms.json",
                  "toolchains/llvm/prebuilt/windows-x86_64/clang_source_info.md"]
    report = {"schemaVersion": 1, "createdUtc": now(), "romSha256": configuration()["romSha256"],
              "ndkRevision": REVISION, "ndkRoot": str(CANONICAL_NDK.relative_to(ROOT)),
              "officialArchiveSha256": NDK_SHA256, "publisherSha256Available": False,
              "publisherSha1": "9bf167a1985fa7d4a036186b78f702eab9179408",
              "toolchainSmokeReport": str(smoke_path.relative_to(ROOT)), "toolchainSmokeSha256": sha256(smoke_path),
              "toolchainMetadata": [{"path": name, "sha256": sha256(CANONICAL_NDK / name)} for name in properties],
              "originalGoldenReport": str(original_report.relative_to(ROOT)), "originalGoldenReportSha256": sha256(original_report),
              "sourceFiles": [{"path": name, "sha256": pins[name]} for name in SOURCE_FILES],
              "syntheticVectorCountCompiled": len(bundle["vectors"]), "plannedFunctionComparisons": len(bundle["vectors"]) * 2,
              "builds": results, "cleanBuildHashesEqual": True, "androidCompileStatus": "passed-arm64-v8a-api33",
              "androidExecutionStatus": "not-run-no-Android-target", "androidExecutedComparisons": 0,
              "hostRunnerExecution": "not-run", "cmakeBuild": "not-run-direct-official-Clang-build",
              "dsMatchedSourceCredit": 0, "wholeRomMatchedCredit": 0, "deviceAccess": False,
              "generatorSha256": sha256(Path(__file__)),
              "reproduction": "python compile_android_checks_20261029.py"}
    write_json(REPORT, report)
    write_json(WORK / "validation.json", report)
    print(json.dumps({"androidCompileStatus": report["androidCompileStatus"],
                      "binarySha256": results[0]["binarySha256"], "bytes": results[0]["binaryBytes"],
                      "cleanBuildHashesEqual": True, "androidExecutionStatus": report["androidExecutionStatus"]}))


if __name__ == "__main__":
    main()
