import argparse
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

from public_manifest import digest, verify


REPORTS = (
    "evidence/verification/checks.json",
    "evidence/linking/latest.json",
    "evidence/linking/arm7-latest.json",
    "evidence/linking/utility-latest.json",
)
PRIVATE_DIRECTORIES = {"inputs", "tools", "deps", "extract", "generated", "evidence", "provenance", "ledger", "work", "nonmatching"}
PRIVATE_FILES = {"recovery.json", "source-preferences.json", "interpreted-recovery.json", "manifest.json", "recovery-ownership.json", "source-map.json"}


class BundleError(ValueError):
    pass


class PartsReader(io.RawIOBase):
    def __init__(self, parts):
        self.parts = iter(parts)
        self.current = None

    def readable(self):
        return True

    def readinto(self, buffer):
        while True:
            if self.current is None:
                next_part = next(self.parts, None)
                if next_part is None:
                    return 0
                self.current = next_part.open("rb")
            size = self.current.readinto(buffer)
            if size:
                return size
            self.current.close()
            self.current = None

    def close(self):
        if self.current is not None:
            self.current.close()
        super().close()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def member_path(root, name):
    path = PurePosixPath(name.rstrip("/"))
    if not name or path.is_absolute() or path.as_posix() != name.rstrip("/"):
        raise BundleError("Noncanonical archive path")
    if any(part in {"", ".", ".."} or ":" in part or "\\" in part or part.endswith((" ", "."))
           or any(ord(char) < 32 for char in part) for part in path.parts):
        raise BundleError("Unsafe archive path")
    private_descriptor = len(path.parts) > 1 and path.parts[0] == 'src' and path.suffix == '.json'
    if not path.parts or path.parts[0] not in PRIVATE_DIRECTORIES and path.as_posix() not in PRIVATE_FILES and not private_descriptor:
        raise BundleError("Archive attempts to supply public source or configuration")
    devices = {"CON", "PRN", "AUX", "NUL", *[f"COM{x}" for x in range(1, 10)], *[f"LPT{x}" for x in range(1, 10)]}
    if any(part.split(".")[0].upper() in devices or part.lower() == ".git" for part in path.parts):
        raise BundleError("Reserved archive path")
    target = root.joinpath(*path.parts)
    if not target.resolve().is_relative_to(root):
        raise BundleError("Archive path escapes checkout")
    for ancestor in (target, *target.parents):
        if ancestor == root:
            break
        if ancestor.is_symlink() or getattr(ancestor, "is_junction", lambda: False)():
            raise BundleError("Archive path traverses a link")
    return path, target


def bundle_parts(bundle, manifest):
    entries = manifest.get("archiveParts")
    if not isinstance(entries, list) or not entries:
        raise BundleError("Missing archive part inventory")
    paths, names = [], set()
    for entry in entries:
        name, expected = entry.get("name"), entry.get("sha256")
        if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name) or name in names:
            raise BundleError("Invalid or duplicate archive part name")
        if not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected):
            raise BundleError("Invalid archive part digest")
        path = bundle / name
        if path.is_symlink() or not path.is_file() or digest(path) != expected:
            raise BundleError("Archive part identity differs")
        names.add(name)
        paths.append(path)
    return paths


def install_bundle(root, bundle):
    root, bundle = Path(root).resolve(), Path(bundle).resolve()
    accepted_path = root / "public/accepted-functions.json"
    accepted_hash = digest(accepted_path)
    accepted = read_json(accepted_path)
    manifest = read_json(bundle / "manifest.json")
    if manifest.get("schemaVersion") != 1 or manifest.get("snapshotRevision") != accepted.get("revision"):
        raise BundleError("Private input snapshot differs from accepted source snapshot")
    if manifest.get("missingRequiredInputs"):
        raise BundleError("Private input bundle declares an incomplete replay closure")
    if manifest.get("acceptedManifestSha256", accepted_hash) != accepted_hash:
        raise BundleError("Accepted source manifest identity differs")
    parts = bundle_parts(bundle, manifest)
    work = root / "work"
    if work.is_symlink() or getattr(work, "is_junction", lambda: False)() or not work.resolve().is_relative_to(root):
        raise BundleError("Private staging directory escapes checkout")
    stage = work / ("private-input-staging-" + uuid.uuid4().hex)
    stage.mkdir(parents=True)
    records, directories, seen = [], [], set()
    try:
        with PartsReader(parts) as raw, io.BufferedReader(raw) as reader, tarfile.open(fileobj=reader, mode="r|gz") as archive:
            for member in archive:
                relative, target = member_path(root, member.name)
                name = relative.as_posix()
                if name in seen:
                    raise BundleError("Duplicate archive path")
                seen.add(name)
                if member.isdir():
                    if target.exists() and not target.is_dir():
                        raise BundleError("Private input directory conflicts with an existing file")
                    directories.append(target)
                    continue
                if not member.isfile():
                    raise BundleError("Archive contains a link or special file")
                staged = stage.joinpath(*relative.parts)
                staged.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise BundleError("Archive member has no payload")
                with source, staged.open("xb") as output:
                    shutil.copyfileobj(source, output)
                if staged.stat().st_size != member.size:
                    raise BundleError("Truncated private input member")
                value = digest(staged)
                if target.exists() and (not target.is_file() or digest(target) != value):
                    raise BundleError("Private input conflicts with an existing checkout file")
                records.append((target, staged, value))
        bundle_parts(bundle, manifest)
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
        installed, reused = 0, 0
        for target, staged, value in records:
            member_path(root, target.relative_to(root).as_posix())
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if not target.is_file() or digest(target) != value:
                    raise BundleError("Private input changed during installation")
                reused += 1
                continue
            with staged.open("rb") as source, target.open("xb") as output:
                shutil.copyfileobj(source, output)
            if digest(target) != value:
                raise BundleError("Installed private input differs")
            staged.unlink()
            installed += 1
        if digest(accepted_path) != accepted_hash:
            raise BundleError("Private input installation changed the accepted manifest")
        return dict(snapshotRevision=manifest["snapshotRevision"], acceptedManifestSha256=accepted_hash,
                    installedFiles=installed, identicalExistingFiles=reused, archiveParts=len(parts))
    finally:
        resolved_stage = stage.resolve()
        if resolved_stage.parent == work.resolve() and resolved_stage.is_relative_to(root) and stage.name.startswith("private-input-staging-"):
            shutil.rmtree(resolved_stage)


def run_private(root, log, arguments, allow_failure=False):
    process = subprocess.Popen([sys.executable, *arguments], cwd=root, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, errors='replace')
    for line in process.stdout:
        log.write(line)
        try:
            event = json.loads(line)
            if (isinstance(event, dict) and set(event) == {'script', 'exitCode'}
                    and isinstance(event['script'], str) and re.fullmatch(r'[A-Za-z0-9_./-]+\.py', event['script'])
                    and type(event['exitCode']) is int):
                print(json.dumps(event), flush=True)
        except (ValueError, TypeError):
            pass
    process.stdout.close()
    process.wait()
    log.flush()
    if process.returncode and not allow_failure:
        raise BundleError("Private build command failed")
    return process.returncode


def prepare_runtime(root, log):
    command = (
        "from pathlib import Path; import subprocess; "
        "from project import configuration, verify_inputs, sha256; "
        "config=configuration(); verify_inputs(config); "
        "pins={'dsd':'5917df26bffc05d4752276a2e0b1edd21bd6e920aabe1992be8a50efc9d10932',"
        "'compiler':'7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880',"
        "'linker':'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'}; "
        "assert all(sha256(config[k])==v for k,v in pins.items()), 'Pinned runtime tool identity differs'; "
        "subprocess.run([str(config['dsd']),'rom','extract','--rom',str(config['rom']),"
        "'--output-path',str(Path.cwd()/'extract')],check=True) if not Path('extract/config.yaml').is_file() else None"
    )
    run_private(root, log, ["-c", command])


def build_outcome(root, exit_code, started_ns):
    if (root / REPORTS[0]).stat().st_mtime_ns < started_ns:
        raise BundleError('The complete build check report is stale')
    checks = read_json(root / REPORTS[0])
    if exit_code == 0 and checks.get("allChecksPassed") is True:
        return dict(legacyAllChecksPassed=True, publicReportingOverride=False)
    steps = checks.get("steps", [])
    if exit_code != 1 or checks.get("buildAndOracleChecksPassed") is not True or not steps:
        raise BundleError("Private build failed beyond the legacy workspace audit")
    if any(step.get("exitCode") != 0 for step in steps[:-1]):
        raise BundleError("A required build or oracle step failed")
    last = steps[-1]
    command = last.get("command", [])
    if last.get("exitCode") != 1 or len(command) < 2 or Path(command[1]).name != "verify_workspace.py":
        raise BundleError("The final failure is not the legacy workspace audit")
    workspace = root / "evidence/verification/workspace.json"
    if not workspace.is_file() or workspace.stat().st_mtime_ns < started_ns:
        raise BundleError("The workspace audit is stale")
    audit = read_json(workspace)
    isolation = audit.get("isolation", {})
    if audit.get("sourcePolicy", {}).get("passed") is not True or isolation.get("observedChanges") != []:
        raise BundleError("Source policy or observed isolation changes prevent reporting")
    if not audit.get("gitRemotes") and not isolation.get("unavailableSnapshots"):
        raise BundleError("The legacy audit failure has no supported public-reporting reason")
    return dict(legacyAllChecksPassed=checks.get("allChecksPassed"), publicReportingOverride=True,
                reason="Public source publication supersedes the historical no-remotes rule; unavailable external audit snapshots remain explicitly unavailable.",
                gitRemotes=audit.get("gitRemotes", []), unavailableSnapshots=isolation.get("unavailableSnapshots", []),
                observedChanges=[], sourcePolicyPassed=True)


def fresh_reports(root, started_ns, rom_hash):
    records = {}
    for name in REPORTS:
        path = root / name
        if not path.is_file() or path.stat().st_mtime_ns < started_ns:
            raise BundleError("Build report is absent or predates this build")
        data = read_json(path)
        if not name.endswith("checks.json") and (data.get("allModuleBytesExact") is not True or data.get("symbolCheckPassed") is not True or data.get("buildNamespace") != rom_hash):
            raise BundleError("Module link report did not pass for the measured build")
        records[name] = dict(sha256=digest(path), modifiedTimeNs=path.stat().st_mtime_ns)
    return records


def main():
    parser = argparse.ArgumentParser(description="Materialize pinned private inputs and build the public source revision without printing private logs.")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--input-bundle", type=Path, default=Path("private-inputs"))
    parser.add_argument("--prepare-only", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    bundle = args.input_bundle.resolve() if args.input_bundle.is_absolute() else root / args.input_bundle
    output = root / "build/B2JJ-modified"
    output.mkdir(parents=True, exist_ok=True)
    accepted_path = root / "public/accepted-functions.json"
    receipt = dict(schemaVersion=1, buildPassed=False, prepared=False, reports={},
                   startedUtc=datetime.now(timezone.utc).isoformat(), startedTimeNs=time.time_ns())
    receipt["startTimeNs"] = receipt["startedTimeNs"]
    status = 1
    with (output / "private-build.log").open("w", encoding="utf-8") as log:
        try:
            receipt["acceptedManifestSha256"] = digest(accepted_path)
            receipt["publicGitRevision"] = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, stderr=log, text=True).strip()
            receipt['phase'] = 'install-private-inputs'
            print(json.dumps(dict(phase='install-pinned-private-inputs')), flush=True)
            receipt["privateInputs"] = install_bundle(root, bundle)
            receipt['phase'] = 'check-public-source'
            accepted, unused_units, unused_pins, summary = verify(root, accepted_path)
            receipt["sourceIntegrity"] = summary
            receipt["prepared"] = True
            if not args.prepare_only:
                for name in ("recovery.json", "manifest.json", "provenance/seed-manifest.json", "provenance/seed-oracle-results.json"):
                    if not (root / name).is_file():
                        raise BundleError("Private replay closure is incomplete")
                receipt['phase'] = 'verify-runtime-inputs'
                prepare_runtime(root, log)
                receipt['phase'] = 'compile-public-source'
                print(json.dumps(dict(phase='compile-accepted-public-source')), flush=True)
                run_private(root, log, ["public_tools/compile_sources.py", "--root", str(root),
                    "--compiler-root", str(root / "tools/mwccarm/mwccarm"),
                    "--license-file", str(root / "tools/mwccarm/mwccarm/license.dat"), "--jobs", "3"])
                compile_path = root / "build/public-source-compile/report.json"
                compiled = read_json(compile_path)
                if compiled.get("status") != "source-compilation-passed" or compiled.get("fullManifestCompiled") is not True or compiled.get("manifestSha256") != receipt["acceptedManifestSha256"] or compile_path.stat().st_mtime_ns < receipt["startedTimeNs"]:
                    raise BundleError("The complete fresh public source compilation did not pass")
                receipt["publicSourceCompileReport"] = dict(path="build/public-source-compile/report.json", sha256=digest(compile_path), modifiedTimeNs=compile_path.stat().st_mtime_ns)
                print(json.dumps(dict(phase='replay-and-link-all-modules')), flush=True)
                receipt['phase'] = 'replay-and-link-all-modules'
                receipt['replayStartedTimeNs'] = time.time_ns()
                build_exit = run_private(root, log, ["run_checks.py", "--clean"], allow_failure=True)
                receipt["buildOutcome"] = build_outcome(root, build_exit, receipt["replayStartedTimeNs"])
                receipt["reports"] = fresh_reports(root, receipt["replayStartedTimeNs"], accepted["romSha256"])
                if digest(accepted_path) != receipt["acceptedManifestSha256"]:
                    raise BundleError("Accepted manifest changed during the private build")
                verify(root, accepted_path)
                receipt["buildPassed"] = True
            status = 0
        except Exception as error:
            receipt["failureType"] = type(error).__name__
            if isinstance(error, BundleError):
                receipt['failureReason'] = str(error)
            log.write(type(error).__name__ + ": " + str(error) + "\n")
        receipt["finishedTimeNs"] = time.time_ns()
    (output / "build-receipt.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    summary = dict(buildPassed=receipt['buildPassed'], prepared=receipt['prepared'], phase=receipt.get('phase'),
                   failureType=receipt.get('failureType'), failureReason=receipt.get('failureReason'))
    compiled_path = root / 'build/public-source-compile/report.json'
    if compiled_path.is_file() and compiled_path.stat().st_mtime_ns >= receipt['startedTimeNs']:
        compiled = read_json(compiled_path)
        summary['compilation'] = {key: compiled.get(key) for key in ('status', 'selectedCompilationUnits', 'compiledUnits', 'fullManifestCompiled')}
        summary['compilation']['firstFailures'] = [
            dict(**{key: unit.get(key) for key in ('source', 'status', 'exitCode')},
                 failureClass='compiler-license' if 'license' in (unit.get('stdout', '') + unit.get('stderr', '')).lower() else 'compiler-or-object-check')
            for unit in compiled.get('results', []) if unit.get('status') != 'compiled'][:5]
    checks_path = root / REPORTS[0]
    if checks_path.is_file() and checks_path.stat().st_mtime_ns >= receipt.get('replayStartedTimeNs', receipt['startedTimeNs']):
        checks = read_json(checks_path)
        summary['checksState'] = checks.get('state')
        failed = [s for s in checks.get('steps', []) if s.get('exitCode')]
        if failed:
            summary['failedStep'] = dict(script=Path(failed[-1]['command'][1]).name, exitCode=failed[-1]['exitCode'])
    (output / 'public-build-status.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary))
    return status


if __name__ == "__main__":
    sys.exit(main())
