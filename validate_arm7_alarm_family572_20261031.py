import copy
import gzip
import json
from pathlib import Path
import match_arm7_alarm_family572_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'b1c6a55a9b8063180748bb3e6df0e29ad363477f791a7024fd9edcf72da0647f'
_FRESH = None


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current source-linked family input/product missing or changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != names or len(report['generatorSources']) != len(names):
        raise ValueError('Complete source/header/runtime family closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Pinned family generator/runtime/original build differs')
    expected = {'processor': 'arm7', 'program': '', 'module': 'arm7-wram', 'matchedInitializedBytes': 572,
        'matchedInstructionBytes': 552, 'generatedLiteralBytes': 20, 'newOrdinaryFunctionCount': 2,
        'newInitializedCoverageBytes': 416, 'declarationMigrationCount': 1, 'declarationMigrationBytes': 156,
        'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Measured new source and preserved caller migration scopes differ')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 3 or len(profile) != 3:
        raise ValueError('Exactly three compatible source definitions are required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen C/header/compiler/identity metadata differs')
        for path, field in [(row['source'], 'sourceSha256'), (row['compiler'], 'compilerSha256'), (row['object'], 'objectSha256')]:
            checked(path, row[field])
        for dependency in row['sourceDependencies']:
            checked(dependency['path'], dependency['sha256'])
        link = row['realArm7Link']
        checked(link['linkCommand'][0], link['linkerSha256'])
        checked(link['lcf'], link['lcfSha256'])
        checked(str(Path(link['cwd']) / 'caller.bin'), row['targetSha256'])
        checked(str(Path(link['cwd']) / 'linked.elf'), link['linkedElfSha256'])
        for anchor in link['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified symbol/tag/addend publication differs')
    trace = report['sharedSourceLinkedNativeEvidence']['trace']
    data = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data)) != trace['rawSha256'] or data[4:8] != bytes(4):
        raise ValueError('Current native trace raw/compressed hash or deterministic gzip metadata differs')
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(matcher.proof()))
    current = {key: value for key, value in report.items() if key not in ('schemaVersion', 'generator', 'generatorSha256', 'generatorSources',
        'pinnedGeneratorAndRuntimeDependencies', 'romSha256', 'processor', 'program', 'module')}
    if current != _FRESH:
        raise ValueError('Fresh source-only whole-body/C ABI/native effect/branch/return proof differs')
    return {('arm7', '', 'arm7-wram', row['address'], 'arm'): row for row in rows}


def main():
    matcher.main()
    report = json.loads(REPORT.read_text())
    validate(report)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid shared-ABI family evidence accepted: ' + name)

    changes = [('rom', ('romSha256',), '0' * 64), ('processor', ('processor',), 'arm9'), ('program', ('program',), 'utility'),
        ('module', ('module',), 'arm7-main'), ('generator', ('generatorSha256',), '0' * 64),
        ('closure-omitted', ('generatorSources',), []), ('runtime-omitted', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('caller-double-credit', ('newInitializedCoverageBytes',), 572), ('three-new-functions', ('newOrdinaryFunctionCount',), 3),
        ('migration-hidden', ('declarationMigrationBytes',), 0), ('caller-body-history-hidden', ('sourceBodyHistory',), {}),
        ('header-view-shrunk', ('alarmLayout', 'sourceViewBytes'), 12),
        ('total-original-object-claimed', ('alarmLayout', 'originalTotalObjectExtentClaimed'), True),
        ('signature-compatibility-disabled', ('alarmLayout', 'allThreeUnitsUseOneHeaderAndCompatibleCFunctionDeclarations'), False),
        ('row-omitted', ('matches',), report['matches'][:2]), ('row-duplicated', ('matches',), report['matches'] + report['matches'][:1]),
        ('wrong-mode', ('matches', 0, 'mode'), 'thumb'), ('source-changed', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('header-dependency-omitted', ('matches', 0, 'sourceDependencies'), []), ('flags-erased', ('matches', 1, 'compilerFlags'), []),
        ('original-blob-input', ('matches', 0, 'originalObjectScaffolding'), True),
        ('exact-gate-disabled', ('matches', 1, 'exactAfterDeclaredRelocation'), False),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('linked-definitions-erased', ('sharedSourceLinkedNativeEvidence', 'sourceLinkedDefinitions'), 1),
        ('own-returns-inflated', ('sharedSourceLinkedNativeEvidence', 'actualReturnCountsByEntry', '0x37fd54c'), 1046),
        ('provider-injected', ('sharedSourceLinkedNativeEvidence', 'providersReplaced'), ['tick']),
        ('whole-module-claim', ('wholeModuleLinked',), True), ('data-credit', ('originalDataSourceCredit',), 44)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    products = [('missing-object-after-cache', ROOT / report['matches'][0]['object']),
        ('missing-body-after-cache', Path(report['matches'][1]['realArm7Link']['cwd']) / 'caller.bin'),
        ('missing-trace-after-cache', ROOT / report['sharedSourceLinkedNativeEvidence']['trace']['path'])]
    for name, path in products:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    for pin, before, after, name in [(profile[0], 'entry->start = start;', 'entry->start = period;', 'typed-start-period-confusion'),
        (profile[1], '(fire - next->fire) < 0', '(fire - next->fire) > 0', 'reversed-signed-delta-order')]:
        text = (ROOT / pin['source']).read_text()
        if before not in text:
            raise ValueError('Expected ordinary C regression target missing')
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        header = ROOT / pin['sourceDependencies'][0]['path']
        copied = directory / header.name
        copied.write_bytes(header.read_bytes())
        source = directory / Path(pin['source']).name
        source.write_text(text.replace(before, after))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()),
            sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
        reject('fresh-real-C-' + name, lambda changed=changed: matcher.build(changed))
    pin = profile[0]
    directory = matcher.WORK / 'controls' / 'incompatible-shared-return-type'
    directory.mkdir(parents=True, exist_ok=True)
    header = ROOT / pin['sourceDependencies'][0]['path']
    text = header.read_text()
    before = 'extern void native_host_arm7_arm_037fd54c('
    if before not in text:
        raise ValueError('Compatible shared declaration absent')
    copied = directory / header.name
    copied.write_text(text.replace(before, 'extern u32 native_host_arm7_arm_037fd54c('))
    source = directory / Path(pin['source']).name
    source.write_bytes((ROOT / pin['source']).read_bytes())
    changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()),
        sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
    reject('fresh-compiler-incompatible-shared-function-type', lambda: matcher.build(changed))
    for pin in profile:
        matcher.build(pin)
    validate(report)
    path = ROOT / 'evidence/verification/arm7-alarm-family572-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'controls': controls, 'allPassed': all(row['rejected'] for row in controls), 'producerRunsBeforeArtifactChecks': True,
        'newInitializedBytes': 416, 'priorCallerBytesMigratedWithoutNewCoverage': 156, 'oldSourceOrHeaderEdited': False}
    write_json(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
