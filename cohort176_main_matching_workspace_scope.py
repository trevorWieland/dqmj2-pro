import argparse
from collections import Counter
import hashlib
import importlib
import json
from pathlib import Path
import stat
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def key(path):
    return str(path).replace('\\', '/').casefold()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def integer(value, expected):
    return type(value) is int and value == expected


def source_rows(rows):
    result = {}
    seen = set()
    for row in rows:
        name = row['path']
        require(key(name) not in seen, 'source path collision')
        require(not Path(name).is_absolute() and '\\' not in name and '..' not in Path(name).parts, 'source path unsafe')
        result[name] = row
        seen.add(key(name))
    return result


def check_policy(old, candidates, support, activation, current):
    expected = source_rows(old)
    require(current['passed'] is True and current['failures'] == [], 'source policy failed')
    require(not support or isinstance(activation, dict) and activation.get('reviewedBy') == 'Root'
            and all(isinstance(activation.get(k), str) and len(activation[k]) == 64
                    and all(c in '0123456789abcdef' for c in activation[k])
                    for k in ('mappingSha256', 'reviewSha256')), 'support activation absent')
    require(len(support) <= 16, 'support bound exceeded')
    for row in candidates + support:
        require(row['path'] not in expected and key(row['path']) not in {key(p) for p in expected}, 'addition collision')
        expected[row['path']] = row
    for row in support:
        require('/' not in row['path'] and '\\' not in row['path'] and row['path'].endswith('.py')
                and isinstance(row.get('role'), str) and bool(row['role'])
                and type(row.get('bytes')) is int and row['bytes'] > 0
                and isinstance(row.get('sha256'), str) and len(row['sha256']) == 64
                and all(c in '0123456789abcdef' for c in row['sha256']), 'support pin invalid')
    observed = source_rows(current['authoredFiles'])
    require(set(expected) == set(observed), 'unreviewed source addition/removal')
    for path, row in expected.items():
        actual = observed[path]
        require(actual['sha256'] == row['sha256'], 'source hash changed: ' + path)
        require(type(actual['physicalLines']) is int and actual['physicalLines'] <= 500
                and actual['hasComments'] is False, 'source policy metadata differs')
    return len(observed)


def check_driver(driver, logs, registry):
    require(driver['state'] == 'failed' and len(driver['steps']) == 16, 'wrong failed driver')
    require(driver['sourceRegistrySha256'] == registry, 'driver registry differs')
    require(len(logs) == 16, 'log count differs')
    for i, (step, frozen) in enumerate(zip(driver['steps'], logs)):
        require(integer(frozen['index'], i) and step['command'] == frozen['command']
                and step['log'] == frozen['log']['path']
                and step['logSha256'] == frozen['log']['sha256'], 'gate identity changed')
        require(integer(step['exitCode'], 0 if i < 15 else 1)
                and step['exitCode'] == frozen['exitCode'], 'gate exit differs')
    require(driver['steps'][-1]['command'] == ['verify_workspace.py'], 'wrong final gate')


def isolation_signature(report):
    require(report['auditAvailable'] is True and report['unavailableSnapshots'] == [], 'isolation unavailable')
    for name in ('allRecordedFilesUnchanged', 'baselineAndInputsUnchanged', 'applicationObservedUnchanged'):
        require(report[name] is False, 'historical isolation must remain false')
    return sorted((row['category'], key(row['path']), row.get('expectedSha256'), row.get('actualSha256'))
                  for row in report['observedChanges'])


def check_isolation(frozen, current):
    require(isolation_signature(frozen) == isolation_signature(current), 'new external delta')
    require(current['filesChecked'] == frozen['filesChecked']
            and current['originalInputsChecked'] == frozen['originalInputsChecked'], 'isolation scope changed')


def check_status(row, actual, owned):
    require(actual.get('present') is True and actual.get('sha256') == row['sha256'], 'file missing/changed: ' + row['path'])
    if 'bytes' in row:
        require(integer(actual.get('bytes'), row['bytes']), 'file size differs')
    if owned:
        require(actual.get('owned') is True and actual.get('noReparse') is True, 'Main path escaped/reparsed')


def merge_pin(pins, row, owned):
    item = {k: row[k] for k in ('path', 'sha256', 'bytes') if k in row}
    name = key(item['path'])
    if name in pins:
        prior, was_owned = pins[name]
        require(prior['sha256'] == item['sha256'] and ('bytes' not in prior or 'bytes' not in item
                or prior['bytes'] == item['bytes']), 'conflicting pin')
        pins[name] = ({**prior, **item}, was_owned or owned)
    else:
        pins[name] = (item, owned)


def acceptance_guards(manifest, plan, freshness, checksum, getters):
    require(manifest['functionMatched'] == plan['expectedSourceMatchedFunctions']
            and manifest['sourceLinkedBytes'] == plan['expectedSourceLinkedBytes'], 'source counts differ')
    require(manifest['exactContainerMatchWithScaffolding'] is True
            and manifest['rejectedMatchEvidence'] == [], 'exact/scaffolding evidence differs')
    require(freshness['passed'] is True and freshness['restoredSourceFunctions'] == manifest['functionMatched'], 'freshness failed')
    oracle = checksum['oracle']
    require(integer(oracle['vectors'], 36) and integer(oracle['executions'], 144)
            and oracle['verifiedReturn'] is True and oracle['isolatedState'] is True
            and len(checksum['functionMatches']) == 2, 'checksum guard failed')
    require(integer(getters['totalComparisons'], 5117) and getters['sourceFilesUnchanged'] is True, 'getter guard failed')
    require(sum(manifest[k] for k in ('currentHostArm9ModuleLinksExact', 'arm7RuntimeModuleLinksExact',
                                    'currentUtilityModuleLinksExact')) == 20, '20 exact links required')


def expected_pins(bundle, contract):
    pins = {}
    for row in bundle['workspace']['sourcePolicy']['authoredFiles']:
        merge_pin(pins, row, True)
    for row in bundle['preservation']['failedOriginalRecords']:
        merge_pin(pins, row, True)
    for row in bundle['preservation']['allSixteenLogs']:
        merge_pin(pins, row['log'], True)
    for row in contract['directPins']:
        merge_pin(pins, row, True)
    critical = bundle['critical']
    for row in critical['originals'] + critical['criticalToolsAndLicense'] + critical['compilerPackAndArchive'] + critical['nativeAllPinnedFiles'] + [critical['Python']]:
        require(row['exact'] is True, 'historical critical input not exact')
        merge_pin(pins, {'path': row['path'], **row['actual']}, row['path'] not in contract['externalOrRuntimePaths'])
    missing = []
    for row in bundle['tools']['rows']:
        if row['actual']['present']:
            require(row['exact'] is True, 'historical present tool changed')
            merge_pin(pins, {'path': row['path'], **row['actual']}, True)
        else:
            missing.append({'path': row['path'], 'sha256': row['expectedSha256']})
    require(len(missing) == 2 and sorted(missing, key=lambda r: r['path'])
            == sorted(contract['missingCachePins'], key=lambda r: r['path']), 'cache omission set differs')
    for row in bundle['equivalents']['rows']:
        main = row['MainEquivalent']
        if main['exact']:
            merge_pin(pins, {'path': main['path'], **main['actual']}, True)
    for row in contract['extraSupportPins'] + bundle['candidate']['files']:
        merge_pin(pins, row, True)
    merge_pin(pins, bundle['supplement']['exactLayoutROM'], True)
    return pins, missing


def validate(bundle, contract, observe, policy, isolation, remotes, verify_sources):
    require(integer(contract['schemaVersion'], 1) and integer(contract['cohort'], 176), 'wrong contract scope')
    require(contract['counts'] == {'historicalSources': 43636, 'candidateSources': 2, 'compilerPack': 247,
            'native': 147, 'toolsPresent': 7462, 'toolsMissing': 2, 'externalBaseline': 632,
            'externalApplication': 126}, 'contract counts differ')
    workspace = bundle['workspace']
    old = workspace['sourcePolicy']['authoredFiles']
    require(len(old) == 43636 and workspace['sourcePolicy']['passed'] is True, 'old source scope differs')
    require(remotes == [] and workspace['gitRemotes'] == [], 'Git remotes present')
    check_driver(bundle['driver'], bundle['preservation']['allSixteenLogs'], contract['registrySha256'])
    require(bundle['plan']['sourceRegistrySha256'] == contract['registrySha256'], 'plan registry differs')
    require(bundle['plan']['sourcePreferenceSha256'] == contract['preferenceSha256'], 'plan preferences differ')
    require(len(bundle['critical']['compilerPackAndArchive']) == 247
            and len(bundle['critical']['nativeAllPinnedFiles']) == 147
            and len(bundle['critical']['originals']) == 4, 'critical count differs')
    require(integer(bundle['tools']['exact'], 7462) and integer(bundle['tools']['missing'], 2)
            and integer(bundle['tools']['changed'], 0) and len(bundle['tools']['rows']) == 7464, 'tool envelope differs')
    delta = workspace['isolation']['observedChanges']
    require(Counter(r['category'] for r in delta) == Counter(baseline=632, application=126), 'external category counts differ')
    require(len(bundle['equivalents']['rows']) == 632 and bundle['equivalents']['groups'] == {
            'tools/decomp-wtf-source': 271, 'tools/ds-decomp-source': 113, 'tools/dsd.exe': 1,
            'tools/mwccarm/': 246, 'tools/mwccarm.zip': 1}, 'historical counterpart scope differs')
    check_isolation(workspace['isolation'], isolation)
    count = check_policy(old, bundle['candidate']['files'], contract['extraSupportPins'],
                         contract['supportActivation'], policy)
    pins, missing = expected_pins(bundle, contract)
    for row, owned in pins.values():
        check_status(row, observe(row['path']), owned)
    for row in missing:
        current = observe(row['path'])
        require(current.get('present') is False and current.get('owned') is True
                and current.get('noReparse') is True, 'cache delivery status or path changed')
    for name in contract['configuredOwnedPaths']:
        current = observe(name)
        require(current.get('owned') is True and current.get('noReparse') is True, 'configured path escaped')
    for row in bundle['equivalents']['rows']:
        if not row['MainEquivalent']['exact']:
            current = observe(row['MainEquivalent']['path'])
            require(row['group'] == 'tools/decomp-wtf-source'
                    and current.get('present') is False and current.get('owned') is True
                    and current.get('noReparse') is True, 'excluded historical counterpart changed')
    for row in contract['extraSupportPins']:
        require(observe(row['path'])['bytes'] == row['bytes'], 'support size differs')
    for text in bundle['membershipTexts']:
        for row in bundle['candidate']['files']:
            require(key(row['path']) not in key(text.replace('\\\\', '/')), 'unaccepted candidate selected')
    acceptance_guards(bundle['manifest'], bundle['plan'], bundle['freshness'], bundle['checksum'], bundle['getters'])
    verify_sources()
    return {'schemaVersion': 1, 'cohort': 176, 'MainMatchingWorkspaceScopePassed': True,
            'historicalOriginalGateExitCode': 1, 'preservedSuccessfulGates': 15,
            'strictWholeWorkspaceIsolationPassed': False, 'baselineAndInputsUnchanged': False,
            'applicationObservedUnchanged': False, 'allRecordedFilesUnchanged': False,
            'fullToolDelivery': False, 'missingCachePins': missing, 'currentAuthoredFiles': count,
            'historicalSourcePinsExact': 43636, 'unacceptedCandidateFiles': 2,
            'extraSupportFiles': len(contract['extraSupportPins']), 'sourceCreditAddedByScopeRepair': 0,
            'sourceRegistrySha256': contract['registrySha256'], 'sourcePreferenceSha256': contract['preferenceSha256'],
            'sourceMatchedFunctions': bundle['manifest']['functionMatched'],
            'sourceLinkedBytes': bundle['manifest']['sourceLinkedBytes'], 'moduleComparisonsExact': 20,
            'checksumVectors': 36, 'checksumActualReturns': 144, 'getterComparisons': 5117,
            'sourceReconstructionComplete': bundle['manifest']['sourceReconstructionComplete'],
            'fullCleanReplayOfThisCohortProven': False, 'observedPinCount': len(pins),
            'snapshotChecksOnly': True, 'externalUnlistedNewFilesDiscovered': False}


class ReadOnlyFiles:
    def __init__(self, root):
        self.root = root.resolve()

    def path(self, name):
        candidate = Path(name)
        return candidate if candidate.is_absolute() else self.root / candidate

    def observe(self, name):
        path = self.path(name)
        owned = path.resolve().is_relative_to(self.root)
        no_reparse = True
        if owned:
            for parent in [path, *path.parents]:
                if parent.exists():
                    info = parent.lstat()
                    no_reparse &= not parent.is_symlink() and not bool(getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)
                if parent == self.root:
                    break
        if not path.exists():
            return {'present': False, 'owned': owned, 'noReparse': no_reparse}
        result = {'present': True, 'owned': owned, 'noReparse': no_reparse}
        if path.is_file():
            with path.open('rb') as stream:
                result.update(bytes=path.stat().st_size, sha256=hashlib.file_digest(stream, 'sha256').hexdigest())
        return result

    def read_pinned(self, row):
        check_status(row, self.observe(row['path']), True)
        raw = self.path(row['path']).read_bytes()
        require(digest(raw) == row['sha256'], 'pinned read changed')
        return raw


def qualify(root, contract_path, contract_sha256):
    files = ReadOnlyFiles(root)
    raw = files.path(contract_path).read_bytes()
    require(digest(raw) == contract_sha256, 'contract hash differs')
    contract = json.loads(raw)
    bundle = {name: json.loads(files.read_pinned(row)) for name, row in contract['jsonPins'].items()}
    require(sys.version_info[:3] == (3, 13, 5)
            and Path(sys.executable).resolve() == Path(bundle['critical']['Python']['path']).resolve(), 'Python runtime differs')
    bundle['membershipTexts'] = [files.read_pinned(row).decode('utf-8-sig') for row in contract['membershipPins']]
    for row in contract['directPins']:
        check_status(row, files.observe(row['path']), True)
    prior = sys.path[:]
    prior_bytecode = sys.dont_write_bytecode
    try:
        sys.dont_write_bytecode = True
        sys.path.insert(0, str(files.root))
        modules = {name: importlib.import_module(name) for name in ('project', 'verify_workspace', 'recovery_registry')}
        for name, module in modules.items():
            require(Path(module.__file__).resolve() == files.root / (name + '.py'), 'module origin differs')
        remotes = subprocess.run(['git', 'remote'], cwd=files.root, capture_output=True, text=True, check=True).stdout.splitlines()
        result = validate(bundle, contract, files.observe, modules['verify_workspace'].policy(),
                          modules['verify_workspace'].isolation(), remotes, modules['recovery_registry'].verify_sources)
        for row in contract['directPins'] + list(contract['jsonPins'].values()) + contract['membershipPins']:
            check_status(row, files.observe(row['path']), True)
        result['contractSha256'] = contract_sha256
        return result
    finally:
        sys.path[:] = prior
        sys.dont_write_bytecode = prior_bytecode


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', required=True, type=Path)
    parser.add_argument('--contract', required=True)
    parser.add_argument('--contract-sha256', required=True)
    options = parser.parse_args()
    print(json.dumps(qualify(options.root, options.contract, options.contract_sha256), indent=2))


if __name__ == '__main__':
    main()
