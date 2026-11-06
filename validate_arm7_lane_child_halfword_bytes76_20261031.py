import copy
import json
from pathlib import Path
import match_arm7_lane_child_halfword_bytes76_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'a463f8b37e43b4b8d72bcbfcfcdbaacf4dd3414890bf8132894d824f3f4c16a2'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current halfword-byte input/product: ' + str(name))
    return path


def validate(report):
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    required = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != required or len(report['generatorSources']) != len(required):
        raise ValueError('Complete typed source/runtime closure differs')
    for item in report['generatorSources']:
        checked(item['path'], item['sha256'])
    if report['generator'] != Path(matcher.__file__).name or report['generatorSha256'] != MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies'] != pins:
        raise ValueError('Frozen halfword-byte generator/runtime differs')
    expected = {'romSha256': matcher.ROM, 'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-main',
        'matchedInitializedBytes': 76, 'matchedInstructionBytes': 76, 'generatedLiteralBytes': 0,
        'actualNativeAndCompiledReturns': 5232, 'actualSeparatelyObservedNestedReturns': 0,
        'providerFreeReturnCredit': 5232, 'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Typed source qualified scope or observed return counts differ')
    rows = report['matches']
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 2 or len(profile) != 2:
        raise ValueError('One complete qualified halfword-byte caller required')
    for pin, row in zip(profile, rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed C/compiler profile differs')
        checked(row['source'], row['sourceSha256'])
        checked(row['compiler'], row['compilerSha256'])
        checked(row['object'], row['objectSha256'])
        proof = row['realArm7Link']
        checked(proof['linkCommand'][0], proof['linkerSha256'])
        checked(proof['lcf'], proof['lcfSha256'])
        checked(str(Path(proof['cwd']) / 'linked.elf'), proof['linkedElfSha256'])
        checked(str(Path(proof['cwd']) / 'caller.bin'), row['targetSha256'])
        for anchor in proof['zeroCodeAnchors']:
            checked(anchor['object'], anchor['objectSha256'])
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Qualified original call-target publication differs')
    key = matcher.digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if key not in _FRESH:
        _FRESH[key] = json.loads(json.dumps([matcher.build(row) for row in profile]))
    if rows != _FRESH[key]:
        raise ValueError('Current complete source/link/boundary/dual-register native evidence differs')
    return {('arm7', 'dwc/utility.bin/move/child.srl', 'utility-child-arm7-main', row['address'], 'arm'): row for row in rows}


def main():
    matcher.main()
    report = json.loads(REPORT.read_text())
    positive = validate(report)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid byte primitive source/evidence accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-program', ('program',), ''),
        ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-module', ('module',), 'utility-child-arm7-wram'),
        ('generator-change', ('generatorSha256',), '0' * 64),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('padding-invented', ('generatedLiteralBytes',), 4),
        ('source-unit-omitted', ('matches',), report['matches'][:1]),
        ('source-unit-duplicated', ('matches',), [report['matches'][0]] * 2),
        ('own-return-count-inflated', ('actualNativeAndCompiledReturns',), 10464),
        ('whole-module-credit', ('wholeModuleLinked',), True),
        ('instruction-mode-confusion', ('matches', 0, 'mode'), 'thumb'),
        ('source-changed', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('compiler-profile-changed', ('matches', 1, 'compilerFlags'), []),
        ('include-closure-added', ('matches', 0, 'sourceDependencies'), ['unapproved.h']),
        ('blob-as-source', ('matches', 0, 'originalObjectScaffolding'), True),
        ('exact-byte-gate-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('getter-false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('writer-false-return', ('matches', 1, 'oracle', 'verifiedReturn'), False),
        ('byte-width-invented', ('matches', 0, 'oracle', 'memoryContract'), 'Byte load instead of actual halfword read'),
        ('writer-preservation-unqualified', ('matches', 1, 'oracle', 'abiContract'), 'No meaningful raw address return'),
        ('provider-injected', ('matches', 0, 'oracle', 'providerReplacements'), ['replacement']),
        ('budget-as-return', ('matches', 1, 'oracle', 'unsupportedReturnCredit'), 1),
        ('interior-reference-hidden', ('matches', 0, 'boundaries', 'outsideInteriorReferences'), [{'target': '0x27e94cc'}]),
        ('source-data-credit', ('originalDataSourceCredit',), 4),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    for name, path in (('missing-getter-object-after-fresh-cache', ROOT / report['matches'][0]['object']),
        ('missing-writer-body-after-fresh-cache', Path(report['matches'][1]['realArm7Link']['cwd']) / 'caller.bin')):
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    getter, writer = report['matches']
    body = bytearray((Path(getter['realArm7Link']['cwd']) / 'caller.bin').read_bytes())
    body[24:28] = (0xE200007F).to_bytes(4, 'little')
    reject('independent-getter-high-bit-loss', lambda: matcher.fixture.execute(0x027E94C8, bytes(body), {'word': 0xFFFF, 'parity': 0, 'value': 0}, 0))
    body = bytearray((Path(writer['realArm7Link']['cwd']) / 'caller.bin').read_bytes())
    body[16:20] = (0x15401001).to_bytes(4, 'little')
    reject('independent-writer-byte-instead-of-halfword-store', lambda: matcher.fixture.execute(0x027E94E8, bytes(body), {'word': 0xA55A, 'parity': 1, 'value': 0x123456FF}, 0))
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    for name, pin, old, new in (('getter-source-mask', profile[0], 'return (u8)value;', 'return value & 127;'),
        ('writer-source-shift', profile[1], 'value << 8', 'value << 7')):
        text = (ROOT / pin['source']).read_text()
        if old not in text:
            raise ValueError('Expected ordinary C negative source missing')
        source = matcher.WORK / 'controls' / (name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text.replace(old, new))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()))
        reject('fresh-compiled-' + name, lambda changed=changed: matcher.build(changed))
    for pin in profile:
        matcher.build(pin)
    if len(validate(report)) != len(positive):
        raise ValueError('Positive exact two-unit evidence not restored')
    output = ROOT / 'evidence/verification/arm7-lane-child-halfword-bytes76-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'positiveUnits': 2, 'matchedInitializedBytes': 76, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeProductChecks': True, 'acceptedSourcesOrNativeInstructionsPatched': False}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()


