import copy
import json
from pathlib import Path
import match_arm7_lane_mmio_poll44_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = '24b0119084f0e824b1852097629838a01df6824bf44b84d9d0e2c4af981d0f11'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current poll input/product: ' + str(name))
    return path


def validate(report):
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    required = {Path(matcher.__file__).name, matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != required or len(report['generatorSources']) != len(required):
        raise ValueError('Poll generator dependency closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    if report['generator'] != Path(matcher.__file__).name or report['generatorSha256'] != MATCHER_SHA or report['pinnedGeneratorAndRuntimeDependencies'] != pins:
        raise ValueError('Poll generator/runtime identity differs')
    expected = {'romSha256': matcher.ROM, 'program': '', 'processor': 'arm7', 'module': 'arm7-wram',
        'matchedInitializedBytes': 44, 'matchedInstructionBytes': 40, 'generatedLiteralBytes': 4,
        'actualNativeAndCompiledReturns': 228, 'actualSeparatelyObservedNestedReturns': 38,
        'actualSeparatelyObservedNativeCallerSuffixReturns': 38, 'providerFreeReturnCredit': 0,
        'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0, 'originalDataSourceCredit': 0,
        'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Poll measured scope/count/namespace differs')
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    rows = report['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('Poll qualified unit missing or duplicated')
    for pin, row in zip(profile, rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen poll source/compiler/profile differs')
        checked(row['source'], row['sourceSha256'])
        checked(row['compiler'], row['compilerSha256'])
        checked(row['object'], row['objectSha256'])
        proof = row['realArm7Link']
        checked(proof['linkCommand'][0], proof['linkerSha256'])
        checked(proof['lcf'], proof['lcfSha256'])
        checked(str(Path(proof['cwd']) / 'linked.elf'), proof['linkedElfSha256'])
        checked(str(Path(proof['cwd']) / 'caller.bin'), row['targetSha256'])
        if proof['zeroCodeAnchors']:
            raise ValueError('Leaf poll unexpectedly gained callee anchors')
    if matcher.publication(rows) != (report['nativeSymbols'], report['nativeSymbolEntries']):
        raise ValueError('Poll qualified native symbol publication differs')
    key = matcher.digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if key not in _FRESH:
        _FRESH[key] = json.loads(json.dumps([matcher.build(pin) for pin in profile]))
    if rows != _FRESH[key]:
        raise ValueError('Poll source-only complete link/boundary/native evidence differs')
    return {('arm7', '', 'arm7-wram', rows[0]['address'], 'arm'): rows[0]}


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
            raise ValueError('Invalid poll source/evidence accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-program', ('program',), 'utility-child'),
        ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-module', ('module',), 'arm7-main'),
        ('source-generator-change', ('generatorSha256',), '0' * 64),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('pool-as-instructions', ('matchedInstructionBytes',), 44),
        ('physical-hardware-overclaim', ('physicalHardwareExecutionCredit',), 1),
        ('provider-free-overclaim', ('providerFreeReturnCredit',), 228),
        ('source-data-overclaim', ('originalDataSourceCredit',), 2),
        ('callee-overclaim', ('calleeSourceCredit',), 1),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('caller-suffix-as-whole-entry', ('actualNativeAndCompiledReturns',), 266),
        ('wrong-mode', ('matches', 0, 'mode'), 'thumb'),
        ('source-change', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('source-includes-added', ('matches', 0, 'sourceDependencies'), ['unproved.h']),
        ('original-object-scaffold', ('matches', 0, 'originalObjectScaffolding'), True),
        ('source-byte-comparison-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-code-as-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('unmapped-bus-as-supported-error', ('matches', 0, 'oracle', 'unsupportedControls', 1, 'supportedErrorPathCredit'), 1),
        ('lost-volatile-read-bound', ('matches', 0, 'oracle', 'syntheticMmioReadContract', 'readLimit'), 3999),
        ('wrong-read-width', ('matches', 0, 'oracle', 'syntheticMmioReadContract', 'width'), 4),
        ('hardware-meaning-invented', ('matches', 0, 'oracle', 'syntheticMmioReadContract', 'physicalHardwareExecuted'), True),
        ('uninitialized-source-read-unqualified', ('matches', 0, 'oracle', 'sourceLocalAssignmentDominance'), ''),
        ('negative-signed-return-invented', ('matches', 0, 'oracle', 'rawReturnContract'), 'returns signed16 status'),
        ('caller-prefix-credit-invented', ('matches', 0, 'boundaries', 'callerSuffix', 'completeCallerOrPrefixCredit'), 1),
        ('opaque-interior-control-erased', ('matches', 0, 'boundaries', 'outsideInteriorBranches'), [{'pc': '0x1'}]),
        ('incoming-opaque-argument-invented', ('matches', 0, 'boundaries', 'initialArgumentOrFlagInputs'), ['R0']),
        ('native-symbol-map-missing', ('nativeSymbols',), {}),
        ('wrong-mmio-address', ('nativeSymbolEntries', 0, 'address'), '0x04808198'),
        ('literal-addend-patched', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 4),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['matches'][0]
    for name, path in (('missing-compiled-object-after-cache', ROOT / row['object']),
        ('missing-current-linked-body-after-cache', Path(row['realArm7Link']['cwd']) / 'caller.bin')):
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    for name, offset, word in (('model-rejects-wrong-stop-bit', 16, 0xE3100040),
        ('model-rejects-signed-halfword-result', 12, 0xE1D100F0), ('model-rejects-omitted-live-read', 12, 0xE1A00000)):
        altered = bytearray(body)
        altered[offset:offset + 4] = word.to_bytes(4, 'little')
        reject(name, lambda altered=altered: matcher.fixture.execute(bytes(altered), matcher.fixture.cases()[0], 0))
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    text = (ROOT / pin['source']).read_text()
    for name, old, new in (('wrong-stop-bit', 'status & 128', 'status & 64'),
        ('wrong-poll-limit', 'remaining = 4000', 'remaining = 3999'),
        ('missing-volatile-access', 'extern volatile u16', 'extern u16')):
        if old not in text:
            raise ValueError('Expected ordinary poll C mutation site absent')
        source = matcher.WORK / 'controls' / (name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text.replace(old, new))
        variant = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()))
        reject('actual-compiled-C-rejects-' + name, lambda variant=variant: matcher.build(variant))
    matcher.build(pin)
    if len(validate(report)) != len(positive):
        raise ValueError('Positive complete poll proof not restored')
    output = ROOT / 'evidence/verification/arm7-lane-mmio-poll44-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'positiveUnits': 1, 'matchedInitializedBytes': 44, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeHistoricalProductChecks': True, 'acceptedSourceOrInstructionBytesPatched': False}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
