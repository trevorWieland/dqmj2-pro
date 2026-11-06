import copy
import gzip
import json
from pathlib import Path
import match_arm7_child_tick324_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = '94988c75d21ee0313d7926043c6d0da2bd82b854ac705b51c1ad28d84466cc3c'
_FRESH = None
CONTROL_REPORT = ROOT / 'evidence/verification' / ('arm7-' + Path(__file__).stem.removeprefix('validate_arm7_').removesuffix('_20261031').replace('_', '-') + '-controls-20261031.json')


def publish_controls(path, report):
    if path.resolve() != CONTROL_REPORT.resolve() or path.resolve() == REPORT.resolve():
        raise ValueError('Control publication escaped this validator namespace')
    write_json(path, report)


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Current child-alarm source/input/product changed: ' + str(name))
    return path


def validate(report):
    global _FRESH
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    names = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PINS.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != names or len(report['generatorSources']) != len(names):
        raise ValueError('Complete child compiler/runtime/source closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generatorSha256'] != MATCHER_SHA or report['generator'] != Path(matcher.__file__).name or report['pinnedGeneratorAndRuntimeDependencies'] != pins or report['romSha256'] != matcher.ROM:
        raise ValueError('Frozen child generator/input closure differs')
    expected = {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-wram',
        'matchedInitializedBytes': 324, 'matchedInstructionBytes': 284, 'generatedLiteralBytes': 40,
        'newOrdinaryFunctionCount': 2, 'newInitializedCoverageBytes': 324, 'declarationMigrationCount': 0,
        'declarationMigrationBytes': 0, 'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0,
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Qualified child scope or source-only credit differs')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 2 or len(profile) != 2:
        raise ValueError('Exactly two qualified child control entries required')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Complete source/header/compiler/function identity differs')
        for name, field in [(row['source'], 'sourceSha256'), (row['compiler'], 'compilerSha256'), (row['object'], 'objectSha256')]:
            checked(name, row[field])
        for dependency in row['sourceDependencies']:
            checked(dependency['path'], dependency['sha256'])
        link = row['realArm7Link']
        checked(link['linkCommand'][0], link['linkerSha256'])
        checked(link['lcf'], link['lcfSha256'])
        checked(str(Path(link['cwd']) / 'caller.bin'), row['targetSha256'])
        checked(str(Path(link['cwd']) / 'linked.elf'), link['linkedElfSha256'])
        for anchor in link['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    trace = report['sharedSourceLinkedNativeEvidence']['trace']
    compressed = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(compressed)) != trace['rawSha256'] or compressed[4:8] != bytes(4):
        raise ValueError('Complete deterministic native trace differs')
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified unchanged real-link bindings differ')
    if _FRESH is None:
        _FRESH = json.loads(json.dumps(matcher.proof()))
    current = {key: value for key, value in report.items() if key not in ('schemaVersion', 'generator', 'generatorSha256', 'generatorSources',
        'pinnedGeneratorAndRuntimeDependencies', 'romSha256', 'processor', 'program', 'module')}
    if current != _FRESH:
        raise ValueError('Fresh source-only linked child/native/model evidence differs')
    return {(row['processor'], row['program'], row['module'], row['address'], row['mode']): row for row in rows}


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
            raise ValueError('Invalid child source/evidence accepted: ' + name)

    changes = [('rom', ('romSha256',), '0' * 64), ('processor', ('processor',), 'arm9'), ('program', ('program',), ''),
        ('module', ('module',), 'arm7-wram'), ('generator', ('generatorSha256',), '0' * 64),
        ('closure', ('generatorSources',), []), ('runtime', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('byte-inflation', ('newInitializedCoverageBytes',), 600), ('duplicate-migration', ('declarationMigrationCount',), 1),
        ('missing-entry', ('matches',), []), ('mode', ('matches', 0, 'mode'), 'thumb'),
        ('source', ('matches', 1, 'sourceSha256'), '0' * 64), ('header', ('matches', 1, 'sourceDependencies'), []),
        ('flags', ('matches', 0, 'compilerFlags'), []), ('blob', ('matches', 0, 'originalObjectScaffolding'), True),
        ('exact-gate', ('matches', 1, 'exactAfterDeclaredRelocation'), False),
        ('code-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('ABI-word-count', ('matches', 0, 'sourceAbiContract', 'physicalArgumentWords'), 5),
        ('counter-width', ('tickViews', 'counter', 'bytes'), 4), ('initializer-return-width', ('matches', 1, 'sourceAbiContract', 'return'), 'void'),
        ('original-callback-credit', ('originalCallbackDependency', 'sourceCredit'), 136),
        ('return-inflation', ('matches', 0, 'oracle', 'actualOriginalAndCompiledReturns'), 9999),
        ('provider', ('sharedSourceLinkedNativeEvidence', 'providerReplacements'), ['clock']),
        ('budget-credit', ('sharedSourceLinkedNativeEvidence', 'unsupportedReturnCredit'), 1),
        ('scope-boundary-as-return', ('sharedSourceLinkedNativeEvidence', 'unsupportedControls', 0, 'actualReturn'), True),
        ('data-credit', ('originalDataSourceCredit',), 44), ('whole-module', ('wholeModuleLinked',), True)]
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    reject('prior-batch-report-destination', lambda: publish_controls(ROOT / 'evidence/verification/arm7-child-alarm544-controls-20261031.json', {}))
    reject('previous224-report-destination', lambda: publish_controls(ROOT / 'evidence/verification/arm7-child-alarm-control224-controls-20261031.json', {}))
    for index, row in enumerate(report['matches']):
        for field, path in [('object', ROOT / row['object']), ('linked-body', Path(row['realArm7Link']['cwd']) / 'caller.bin')]:
            saved = path.read_bytes()
            try:
                path.unlink()
                reject('missing-' + str(index) + '-' + field, lambda: validate(report))
            finally:
                path.write_bytes(saved)
    path = ROOT / report['sharedSourceLinkedNativeEvidence']['trace']['path']
    saved = path.read_bytes()
    try:
        path.unlink()
        reject('missing-native-trace', lambda: validate(report))
    finally:
        path.write_bytes(saved)
    pins = json.loads(matcher.PROFILE.read_text())['matches']
    mutations = [('counter-mask-truncated', 0, '0xFFFFFFFFFFFFULL', '0xFFFFFFFFULL', False),
        ('wrong-pending-bit', 0, '04000214 & 8)', '04000214 & 4)', False),
        ('wrong-reservation-index', 1, '037fd708(0);', '037fd708(1);', False),
        ('raw-initializer-return-erased', 1, 'return (u32)&native_utility_child_arm7_tick_reset_03805b5c;', 'return (u32)&native_utility_child_arm7_tick_initialized_03805b58;', False),
        ('counter-declaration-narrowed', 0, 'extern volatile u64 native_utility_child_arm7_tick_counter_03805b60;', 'extern volatile u32 native_utility_child_arm7_tick_counter_03805b60;', True)]
    for name, index, before, after, header_change in mutations:
        pin = pins[index]
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        header = ROOT / pin['sourceDependencies'][0]['path']
        source = ROOT / pin['source']
        text = (header if header_change else source).read_text()
        if before not in text:
            raise ValueError('Expected ordinary-C mutation location absent')
        copied = directory / header.name
        copied.write_text(text.replace(before, after) if header_change else header.read_text())
        authored = directory / source.name
        authored.write_text(source.read_text() if header_change else text.replace(before, after))
        changed = dict(pin, source=authored.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(authored.read_bytes()),
            sourceDependencies=[{'path': copied.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(copied.read_bytes())}])
        reject('fresh-C-' + name, lambda changed=changed: matcher.build(changed))
    for pin in pins:
        matcher.build(pin)
    validate(report)
    path = CONTROL_REPORT
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'controls': controls,
        'allPassed': all(row['rejected'] for row in controls), 'newSourceBytes': 324, 'newFunctionCount': 2,
        'producerBeforeProductChecks': True, 'oldAcceptedSourcesAndHeaderUnchanged': True}
    publish_controls(path, result)
    print(json.dumps({'report': path.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(path.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
