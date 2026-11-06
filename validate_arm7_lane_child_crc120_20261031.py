import copy
import json
from pathlib import Path
import match_arm7_lane_child_crc120_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'd33d858de94b906a3a39fe95715f89c93ca5bdaa5bcf6861d55ce77ad087ef9e'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current CRC input/product: ' + str(name))
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
        raise ValueError('Frozen CRC generator/runtime differs')
    expected = {'romSha256': matcher.ROM, 'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-main',
        'matchedInitializedBytes': 120, 'matchedInstructionBytes': 112, 'generatedLiteralBytes': 8,
        'actualNativeAndCompiledReturns': 2592, 'actualSeparatelyObservedNestedReturns': 0,
        'providerFreeReturnCredit': 2592, 'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Typed source qualified scope or observed return counts differ')
    rows = report['matches']
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('One complete qualified CRC caller required')
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
            raise ValueError('Invalid CRC source/evidence accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-program', ('program',), ''),
        ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-module', ('module',), 'utility-child-arm7-wram'),
        ('generator-change', ('generatorSha256',), '0' * 64),
        ('generator-closure-removed', ('generatorSources',), []),
        ('runtime-closure-removed', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('literal-as-code', ('matchedInstructionBytes',), 120),
        ('literal-omitted', ('generatedLiteralBytes',), 0),
        ('own-return-count-inflated', ('actualNativeAndCompiledReturns',), 5184),
        ('whole-module-credit', ('wholeModuleLinked',), True),
        ('entry-mode-change', ('matches', 0, 'mode'), 'thumb'),
        ('source-changed', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('compiler-profile-changed', ('matches', 0, 'compilerFlags'), []),
        ('include-closure-added', ('matches', 0, 'sourceDependencies'), ['unapproved.h']),
        ('blob-as-source', ('matches', 0, 'originalObjectScaffolding'), True),
        ('exact-byte-gate-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('wrong-polynomial', ('matches', 0, 'oracle', 'table', 'polynomial'), '0x8408'),
        ('unproved-portability', ('matches', 0, 'oracle', 'sourceSignedShiftContract'), 'All C compilers and all targets proved'),
        ('full-word-inputs-unqualified', ('matches', 0, 'oracle', 'abiContract'), 'Only byte inputs tested'),
        ('table-index-missing', ('matches', 0, 'oracle', 'all16TableIndexesRead'), [0]),
        ('table-as-source', ('matches', 0, 'oracle', 'sourceDataCredit'), 32),
        ('provider-injected', ('matches', 0, 'oracle', 'providerReplacements'), ['fake table']),
        ('budget-as-return', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('original-table-extent-widened', ('matches', 0, 'boundaries', 'originalTableDependency', 'storageBytes'), 64),
        ('opaque-interior-omitted', ('matches', 0, 'boundaries', 'outsideInteriorReferences'), [{'target': '0x27e93d8'}]),
        ('data-address-publication-omitted', ('nativeSymbols',), {}),
        ('relocation-addend-patched', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 4),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['matches'][0]
    for name, path in (('missing-object-after-fresh-cache', ROOT / row['object']),
        ('missing-linked-body-after-fresh-cache', Path(row['realArm7Link']['cwd']) / 'caller.bin')):
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    body = bytearray((Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes())
    body[112:116] = (0x027F7F76).to_bytes(4, 'little')
    reject('independent-shifted-table-pointer', lambda: matcher.fixture.execute(bytes(body), (255, 0xFFFF), 0))
    body = bytearray((Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes())
    body[116:120] = (0x7FF).to_bytes(4, 'little')
    reject('independent-truncated-prior-mask', lambda: matcher.fixture.execute(bytes(body), (0, 0x8000), 0))
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    text = (ROOT / pin['source']).read_text()
    for name, old, new in (('wrong-prior-shift', 'previous >> 4', 'previous >> 3'),
        ('wrong-low-nibble', 'byte & 15', 'byte & 7')):
        if old not in text:
            raise ValueError('Expected ordinary C mutation missing')
        source = matcher.WORK / 'controls' / (name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text.replace(old, new))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()))
        reject('fresh-compiled-' + name, lambda changed=changed: matcher.build(changed))
    matcher.build(pin)
    if len(validate(report)) != len(positive):
        raise ValueError('Positive full CRC source/evidence not restored')
    output = ROOT / 'evidence/verification/arm7-lane-child-crc120-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'positiveUnits': 1, 'matchedInitializedBytes': 120, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeProductChecks': True, 'acceptedSourcesOrNativeInstructionsPatched': False, 'tableSourceCredit': 0}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()


