import copy
import gzip
import json
from pathlib import Path
import match_arm7_valarm_insert164_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = '1f3978800ac0dfdbd17ffeb80a937ab841056d6431e8e7afb68decaa2987eae4'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current explicit-ABI initializer input/product: ' + str(name))
    return path


def validate(report):
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    required = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != required or len(report['generatorSources']) != len(required):
        raise ValueError('Complete source/runtime input closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    expected = {'romSha256': matcher.ROM, 'generator': Path(matcher.__file__).name, 'generatorSha256': MATCHER_SHA,
        'pinnedGeneratorAndRuntimeDependencies': pins, 'program': '', 'processor': 'arm7', 'module': 'arm7-wram',
        'matchedInitializedBytes': 164, 'matchedInstructionBytes': 160, 'generatedLiteralBytes': 4,
        'actualNativeAndCompiledReturns': 360, 'actualSeparatelyObservedNestedReturns': 170, 'providerFreeReturnCredit': 360,
        'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0,
        'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Measured scope, source-only gate or distinct return counts differ')
    rows, profile = report['matches'], json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('Exactly one complete initializer is supported')
    for row, pin in zip(rows, profile):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen complete source/compiler/native view differs')
        for path, field in ((row['source'], 'sourceSha256'), (row['compiler'], 'compilerSha256'), (row['object'], 'objectSha256')):
            checked(path, row[field])
        link = row['realArm7Link']
        checked(link['linkCommand'][0], link['linkerSha256'])
        checked(link['lcf'], link['lcfSha256'])
        checked(str(Path(link['cwd']) / 'linked.elf'), link['linkedElfSha256'])
        checked(str(Path(link['cwd']) / 'caller.bin'), row['targetSha256'])
        for anchor in link['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    trace = rows[0]['oracle']['trace']
    data = checked(trace['path'], trace['compressedSha256']).read_bytes()
    if matcher.digest(gzip.decompress(data)) != trace['rawSha256'] or data[4:8] != bytes(4):
        raise ValueError('Current deterministic compressed native evidence differs')
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Measured real-link function/data assignments differ')
    key = matcher.digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if key not in _FRESH:
        _FRESH[key] = json.loads(json.dumps([matcher.build(pin) for pin in profile]))
    if rows != _FRESH[key]:
        raise ValueError('Current full native/C/branch/ABI/store evidence differs')
    return {('arm7', '', 'arm7-wram', rows[0]['address'], 'arm'): rows[0]}


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
            raise ValueError('Invalid initializer source/evidence accepted: ' + name)

    changes = [('wrong-rom', ('romSha256',), '0' * 64), ('wrong-program', ('program',), 'utility'),
        ('wrong-processor', ('processor',), 'arm9'), ('wrong-module', ('module',), 'arm7-main'),
        ('changed-generator', ('generatorSha256',), '0' * 64), ('missing-closure', ('generatorSources',), []),
        ('missing-runtime', ('pinnedGeneratorAndRuntimeDependencies',), []), ('missing-unit', ('matches',), []),
        ('duplicated-unit', ('matches',), report['matches'] * 2), ('wrong-mode', ('matches', 0, 'mode'), 'thumb'),
        ('source-changed', ('matches', 0, 'sourceSha256'), '0' * 64), ('flags-changed', ('matches', 0, 'compilerFlags'), []),
        ('source-dependencies-added', ('matches', 0, 'sourceDependencies'), ['unknown.h']),
        ('blob-instead-of-C', ('matches', 0, 'originalObjectScaffolding'), True),
        ('exact-gate-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('source-input-native-code', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('wrong-node-view', ('matches', 0, 'nodeViewMinimumBytes'), 12),
        ('outside-interior-hidden', ('matches', 0, 'boundaries', 'outsideInteriorOrPoolReferences'), [{'target': '0x37fd368'}]),
        ('data-extent-invented', ('matches', 0, 'originalAllocationExtentClaimed'), True),
        ('provider-injected', ('matches', 0, 'oracle', 'providerReplacements'), ['timer']),
        ('own-return-inflated', ('actualNativeAndCompiledReturns',), 530), ('callee-source-credit', ('calleeSourceCredit',), 3),
        ('data-credit-invented', ('originalDataSourceCredit',), 12), ('hardware-claim', ('physicalHardwareExecutionCredit',), 1),
        ('whole-module-claim', ('wholeModuleLinked',), True), ('pool-as-instructions', ('matchedInstructionBytes',), 164)]
    for name, path, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['matches'][0]
    for name, path in [('missing-object-after-cache', ROOT / row['object']),
        ('missing-body-after-cache', Path(row['realArm7Link']['cwd']) / 'caller.bin'),
        ('missing-native-trace-after-cache', ROOT / row['oracle']['trace']['path'])]:
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    source = (ROOT / pin['source']).read_text()
    for name, before, after in [('unsigned-key-made-signed', 'next->frame >= entry->frame', '(signed int)next->frame >= (signed int)entry->frame'),
        ('signed-halfword-made-unsigned', 's16 scan;', 'u16 scan;')]:
        if before not in source:
            raise ValueError('Required source contract unavailable')
        path = matcher.WORK / 'controls' / (name + '.c')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(source.replace(before, after))
        changed = dict(pin, source=path.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(path.read_bytes()))
        reject(name, lambda changed=changed: matcher.build(changed))
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    bounded = matcher.fixture.execute(body, matcher.fixture.cases()[0], 0, budget=1)
    if bounded['actualReturn']:
        raise ValueError('Instruction exhaustion counted as normal return')
    controls.append({'name': 'instruction-exhaustion-no-return', 'rejected': True})
    matcher.build(pin)
    validate(report)
    output = ROOT / 'evidence/verification/arm7-valarm-insert164-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()), 'positiveUnits': 1,
        'matchedInitializedBytes': 164, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeProductChecks': True, 'acceptedSourcesOrNativeInputsPatched': False}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
