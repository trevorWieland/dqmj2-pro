import hashlib
import json
import os
import subprocess
from pathlib import Path, PurePosixPath


REPORTS = ('latest.json', 'arm7-latest.json', 'utility-latest.json')
DENOMINATOR = 2512636


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def relative_file(root, name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Build receipt requires canonical relative input paths')
    relative = PurePosixPath(name)
    if relative.is_absolute() or '..' in relative.parts or relative.as_posix() != name:
        raise ValueError('Build receipt input path escapes its checkout')
    path = root.joinpath(*relative.parts).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Build receipt input is missing or escapes its checkout')
    return path


def timestamp(value, label, positive=False):
    if type(value) is not int or value < (1 if positive else 0):
        raise ValueError('Build receipt lacks a valid ' + label)
    return value


def pinned_file(root, pin, not_before, label, required_parent=None):
    if not isinstance(pin, dict):
        raise ValueError('Build receipt lacks its ' + label + ' pin')
    path = relative_file(root, pin.get('path'))
    if required_parent is not None and path.parent != required_parent:
        raise ValueError(label + ' is outside its verified native build directory')
    modified = path.stat().st_mtime_ns
    if digest(path) != pin.get('sha256') or modified != pin.get('modifiedTimeNs') or modified < not_before:
        raise ValueError(label + ' is stale or differs from its build receipt')
    return path


def compile_report(root, data, manifest_hash, started, requested=None):
    path = pinned_file(root, data.get('publicSourceCompileReport'), started, 'Source compilation report')
    if requested is not None:
        requested = Path(requested)
        requested = (root / requested).resolve() if not requested.is_absolute() else requested.resolve()
        if requested != path:
            raise ValueError('Requested source compilation report differs from the build receipt')
    compiled = read(path)
    if compiled.get('status') != 'source-compilation-passed' or compiled.get('fullManifestCompiled') is not True or compiled.get('manifestSha256') != manifest_hash:
        raise ValueError('Complete source compilation for the current accepted manifest is required')
    return path


def native_reports(root, private, outer, revision, manifest_hash, started, requested):
    if private != root:
        raise ValueError('Native module receipts require their materialized private inputs in the public checkout')
    timestamp(started, 'CI build start time', positive=True)
    compiled_path = compile_report(root, outer, manifest_hash, started, requested)
    native_started = timestamp(outer.get('nativeStartedTimeNs'), 'native build start time', positive=True)
    if native_started < started:
        raise ValueError('Native module build predates this CI build')
    native_path = pinned_file(root, outer.get('nativeBuildReceipt'), native_started, 'Native build receipt')
    native_parent = native_path.parent
    if not native_parent.is_relative_to(root / 'work') or native_parent == root / 'work':
        raise ValueError('Native build receipt must belong to a dedicated work directory')
    native = read(native_path)
    if native.get('schemaVersion') != 1 or native.get('buildPassed') is not True or native.get('nativeBuildPassed') is not True:
        raise ValueError('A successful focused native module receipt is required')
    if native.get('publicGitRevision') != revision or native.get('acceptedManifestSha256') != manifest_hash:
        raise ValueError('Native build receipt belongs to another revision or accepted manifest')
    if native.get('startedTimeNs') != native_started or timestamp(native.get('finishedTimeNs'), 'native build finish time') < native_started:
        raise ValueError('Native receipt timing differs from the parent CI build')
    expected = {'moduleCount': 20, 'initializedBytes': DENOMINATOR, 'acceptedFunctionsLinked': 11482}
    if any(type(native.get(key)) is not int or native[key] != value for key, value in expected.items()):
        raise ValueError('Native build receipt omits the complete closed module/function scope')
    if any(native.get(key) is not True for key in ('allModuleBytesExact', 'allSymbolChecksPassed', 'frozenInputsUnchanged')):
        raise ValueError('All native module bytes, symbols, and frozen inputs must pass')
    if native.get('behavioralReplayPerformed') is not False or native.get('fullContainerBuildPerformed') is not False:
        raise ValueError('Focused native module receipt must preserve its explicit validation scope')
    if native.get('freshCompilationTimeBound') is not True or native.get('compilationNotBeforeTimeNs') != started:
        raise ValueError('Native source compilation is not bound to the parent CI build')
    if native.get('publicSourceCompileReport') != outer['publicSourceCompileReport']:
        raise ValueError('Native build used another source compilation report')
    if native.get('importedLinkageSourceCredit', 0) != 0:
        raise ValueError('Imported frozen linkage cannot receive source credit')
    reports = native.get('reports')
    if not isinstance(reports, dict) or outer.get('reports') != reports:
        raise ValueError('Parent and native link report inventories differ')
    report_parent = native_parent / 'evidence/linking'
    expected_paths = {(report_parent / name).relative_to(root).as_posix() for name in REPORTS}
    if set(reports) != expected_paths:
        raise ValueError('Native link report paths must remain in the verified native build directory')
    verified = {}
    for relative, pin in reports.items():
        record = dict(pin, path=relative)
        path = pinned_file(root, record, native_started, 'Native link report', report_parent)
        verified[path.name] = path
    return dict(revision=revision, buildScope='native-modules', reports=verified, compilation=compiled_path,
                receipt=outer, nativeReceipt=native)


def validate_build_receipt(root, private, receipt, manifest_hash, compilation=None):
    root, private = Path(root).resolve(), Path(private).resolve()
    receipt = Path(receipt)
    receipt = (root / receipt).resolve() if not receipt.is_absolute() else receipt.resolve()
    if not receipt.is_relative_to(root) or not receipt.is_file():
        raise ValueError('Build receipt is missing or escapes the public checkout')
    data = read(receipt)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    if data.get('buildPassed') is not True or data.get('publicGitRevision') != revision or data.get('acceptedManifestSha256') != manifest_hash:
        raise ValueError('Build receipt must bind a successful build to this public revision and manifest')
    if os.environ.get('GITHUB_SHA') and os.environ['GITHUB_SHA'] != revision:
        raise ValueError('Public build revision differs from CI revision')
    scope = data.get('buildScope')
    if scope not in (None, 'full-replay', 'native-modules'):
        raise ValueError('Unknown build receipt validation scope')
    started = timestamp(data.get('startedTimeNs', data.get('startTimeNs')), 'build start time')
    if scope == 'native-modules':
        return native_reports(root, private, data, revision, manifest_hash, started, compilation)
    compiled_path = compile_report(root, data, manifest_hash, started, compilation) if data.get('publicSourceCompileReport') else compilation
    replay_started = timestamp(data.get('replayStartedTimeNs', started), 'replay start time')
    verified = {}
    for name in REPORTS:
        relative = 'evidence/linking/' + name
        path = relative_file(private, relative)
        pin = data.get('reports', {}).get(relative, {})
        if digest(path) != pin.get('sha256') or path.stat().st_mtime_ns < replay_started:
            raise ValueError('Link report is stale or differs from fresh build receipt: ' + relative)
        if 'modifiedTimeNs' in pin and pin['modifiedTimeNs'] != path.stat().st_mtime_ns:
            raise ValueError('Link report modification time differs from its build receipt')
        verified[name] = path
    return dict(revision=revision, buildScope='full-replay', reports=verified, compilation=compiled_path, receipt=data)


def receipt_check(root, private, receipt, manifest_hash):
    return validate_build_receipt(root, private, receipt, manifest_hash)['revision']
