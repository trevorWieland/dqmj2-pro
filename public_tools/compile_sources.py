import argparse
import concurrent.futures
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path
from elf_metadata import inspect
from public_manifest import ManifestError, digest, verify, write_report


def compiler_index(directory, hashes):
    found = {}
    for path in sorted(directory.rglob("*.exe")):
        value = digest(path)
        if value in hashes:
            found.setdefault(value, path.resolve())
    missing = hashes - found.keys()
    if missing:
        raise ManifestError("Exact compiler binaries missing under --compiler-root: " + ", ".join(sorted(missing)))
    return found


def compile_unit(root, unit, compiler, output, license_file, timeout):
    identity = dict(source=unit["source"].relative_to(root).as_posix(), compilerSha256=unit["compilerSha256"],
                    compilerFlags=unit["rows"][0]["compilerFlags"])
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()[:20]
    directory = output / key
    directory.mkdir(parents=True, exist_ok=True)
    obj = directory / "compiled.o"
    flags = list(unit["flags"])
    if "-c" not in flags:
        flags.append("-c")
    argv = [str(compiler), *flags, str(unit["source"]), "-o", str(obj)]
    env = dict(os.environ)
    if license_file:
        env["LM_LICENSE_FILE"] = str(license_file)
    record = dict(**identity, functionIds=[r["id"] for r in unit["rows"]], command=argv, cwd=str(root),
                  object=str(obj), nativeMatchingVerified=False, moduleLinkingVerified=False, wholeRomVerified=False)
    try:
        if digest(compiler) != unit["compilerSha256"]:
            raise ManifestError("Compiler changed after exact hash resolution")
        process = subprocess.run(argv, cwd=root, env=env, capture_output=True, timeout=timeout)
        record.update(exitCode=process.returncode, stdout=process.stdout.decode(errors="replace"), stderr=process.stderr.decode(errors="replace"))
        if process.returncode:
            record["status"] = "compile-failed"
            return record
        metadata = inspect(obj)
        checks = []
        for row in unit["rows"]:
            name = row.get("compileSymbol") or row.get("symbol")
            choices = [f for f in metadata["functions"] if f["name"] == name]
            explicit = bool(row.get("compileSymbol"))
            if explicit and len(choices) != 1:
                raise ManifestError("Explicit compileSymbol is absent or ambiguous: " + str(name))
            check = dict(id=row["id"], requestedSymbol=name, explicitCompileSymbol=explicit,
                         ledgerSymbolDiagnosticOnly=not explicit, found=len(choices), functions=choices,
                         declaredObjectSha256=row.get("objectSha256"))
            if explicit:
                function = choices[0]
                if row.get("compiledBytes") is not None and function["bytes"] != row["compiledBytes"]:
                    raise ManifestError("Explicit compiled function extent differs: " + name)
                if function["mode"] != "unknown" and function["mode"] != row["mode"]:
                    raise ManifestError("Explicit function ARM/Thumb mapping differs: " + name)
                if row.get("sourceFunctionSha256") and function["sourceFunctionSha256"] != row["sourceFunctionSha256"]:
                    raise ManifestError("Explicit source-generated function digest differs: " + name)
            checks.append(check)
        actual_hash = digest(obj)
        record.update(status="compiled", objectSha256=actual_hash, sourceObjectMetadata=metadata, functionDiagnostics=checks,
                      wholeObjectHashesAreDiagnostic=True,
                      historicalObjectHashesIdentical=all(not c["declaredObjectSha256"] or c["declaredObjectSha256"] == actual_hash for c in checks))
    except (OSError, ValueError, subprocess.TimeoutExpired) as error:
        record.update(status="compile-or-object-validation-failed", error=str(error))
    return record


def main():
    parser = argparse.ArgumentParser(description="Compile accepted public source with exact local compiler hashes. This does not read a ROM, link modules, or verify native matching.")
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=Path("public/accepted-functions.json"))
    parser.add_argument("--compiler-root", required=True, type=Path)
    parser.add_argument("--license-file", type=Path)
    parser.add_argument("--out-dir", type=Path, default=Path("build/public-source-compile"))
    parser.add_argument("--jobs", type=int, choices=range(1, 4), default=3)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else root / args.manifest
    output = (args.out_dir if args.out_dir.is_absolute() else root / args.out_dir).resolve()
    try:
        manifest, all_units, pins, summary = verify(root, manifest_path)
        if not output.is_relative_to(root / "build") and not output.is_relative_to(root / "work"):
            raise ManifestError("Compilation output must stay beneath --root/build or --root/work")
        if args.timeout <= 0 or args.limit is not None and args.limit <= 0:
            raise ManifestError("Timeout and optional limit must be positive")
        units = [u for u in all_units if not args.source or u["source"].relative_to(root).as_posix() in args.source]
        if args.source and {u["source"].relative_to(root).as_posix() for u in units} != set(args.source):
            raise ManifestError("A requested source is not in the accepted manifest")
        units = sorted(units, key=lambda u: (str(u["source"]), u["compilerSha256"], tuple(u["flags"])))
        if args.limit:
            units = units[:args.limit]
        directory = args.compiler_root.resolve()
        if not directory.is_dir():
            raise ManifestError("--compiler-root must be a local compiler package directory")
        compilers = compiler_index(directory, {u["compilerSha256"] for u in units})
        license_file = args.license_file.resolve() if args.license_file else directory / "license.dat"
        if args.license_file and not license_file.is_file():
            raise ManifestError("Explicit --license-file is missing")
        if not license_file.is_file():
            license_file = None
        output.mkdir(parents=True, exist_ok=True)
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(compile_unit, root, u, compilers[u["compilerSha256"]], output,
                                   license_file, args.timeout) for u in units]
            records = [future.result() for future in futures]
        changes = [name for name, value in pins.items() if digest(root / name) != value]
        passed = not changes and all(r["status"] == "compiled" for r in records)
        summary.update(status="source-compilation-passed" if passed else "source-compilation-failed", compilerInvoked=True,
                       selectedCompilationUnits=len(units), compiledUnits=sum(r["status"] == "compiled" for r in records),
                       selectedFunctions=sum(len(u["rows"]) for u in units), sourceFilesChangedDuringCompilation=changes,
                       fullManifestCompiled=len(units) == len(all_units), results=records,
                       objectHashLimit="Debug/source paths can change whole object hashes; they are diagnostic unless an explicit function digest is provided.")
    except (OSError, ValueError, KeyError, TypeError) as error:
        summary = dict(status="source-compilation-preflight-failed", error=str(error), originalInputsRead=False,
                       nativeMatchingVerified=False, moduleLinkingVerified=False, wholeRomVerified=False)
    if output.is_relative_to(root / "build") or output.is_relative_to(root / "work"):
        write_report(output / "report.json", summary)
    print(json.dumps({k: v for k, v in summary.items() if k != "results"}, indent=2))
    return 0 if summary["status"] == "source-compilation-passed" else 1


if __name__ == "__main__":
    sys.exit(main())
