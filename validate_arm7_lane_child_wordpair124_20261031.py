import copy
import json
from pathlib import Path
import match_arm7_lane_child_wordpair124_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = 'ca8832804ad5b91344ed6a581e8461100a2d464151068f24da889affb8d1872e'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current word-pair input/product: ' + str(name))
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
        raise ValueError('Frozen word-pair generator/runtime differs')
    expected = {'romSha256': matcher.ROM, 'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-main',
        'matchedInitializedBytes': 124, 'matchedInstructionBytes': 124, 'generatedLiteralBytes': 0,
        'actualNativeAndCompiledReturns': 896, 'actualSeparatelyObservedNestedReturns': 3584,
        'providerFreeReturnCredit': 896, 'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Typed source qualified scope or observed return counts differ')
    rows = report['matches']
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('One complete qualified word-pair caller required')
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
    return {('arm7', 'dwc/utility.bin/move/child.srl', 'utility-child-arm7-main', rows[0]['address'], 'arm'): rows[0]}


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
            raise ValueError('Invalid word-pair source/evidence accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-program', ('program',), ''),
        ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-module', ('module',), 'utility-child-arm7-wram'),
        ('generator-change', ('generatorSha256',), '0' * 64),
        ('incomplete-generator-closure', ('generatorSources',), []),
        ('incomplete-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('invented-literal-padding', ('generatedLiteralBytes',), 4),
        ('native-helper-code-credit', ('calleeSourceCredit',), 480),
        ('whole-module-credit', ('wholeModuleLinked',), True),
        ('nested-returns-counted-as-caller', ('actualNativeAndCompiledReturns',), 4480),
        ('incorrect-entry-mode', ('matches', 0, 'mode'), 'thumb'),
        ('source-bytes-changed', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('source-closure-added', ('matches', 0, 'sourceDependencies'), ['undeclared.h']),
        ('source-blob-as-reconstruction', ('matches', 0, 'originalObjectScaffolding'), True),
        ('linked-byte-check-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-code-as-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-native-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('no-original-divide-returns', ('matches', 0, 'oracle', 'actualSeparatelyObservedNativeDivideReturns'), 0),
        ('generic-int-return-misbinding', ('matches', 0, 'oracle', 'abiContract'), 'generic int return'),
        ('invented-signed-word-semantics', ('matches', 0, 'oracle', 'wordArithmetic'), 'signed overflow permitted'),
        ('caller-providers-added', ('matches', 0, 'oracle', 'providerReplacements'), ['replacement']),
        ('budget-as-return', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('native-scope-report-dropped', ('matches', 0, 'boundaries', 'helperRole', 'sha256'), '0' * 64),
        ('callee-boundary-enlarged', ('matches', 0, 'boundaries', 'helperRole', 'canonicalFunctionBoundaryEnlarged'), True),
        ('helper-own-source-credit', ('matches', 0, 'boundaries', 'helperRole', 'sourceCredit'), 480),
        ('old-c-source-silently-mutated', ('matches', 0, 'boundaries', 'declarationClosure', 'acceptedLowWordSourceChanged'), True),
        ('pair-alias-closure-omitted', ('matches', 0, 'boundaries', 'declarationClosure', 'pairAlias'), 'old-int-return-symbol'),
        ('known-interior-control-omitted', ('matches', 0, 'boundaries', 'outsideInteriorReferences'), [{'pc': '0x1'}]),
        ('native-symbol-publication-missing', ('nativeSymbols',), {}),
        ('callee-source-mode-confused', ('nativeSymbolEntries', 0, 'mode'), 'thumb'),
        ('unchanged-relocation-addend-patched', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 0),
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
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    altered = bytearray(body)
    altered[112:116] = (0xE1A00000).to_bytes(4, 'little')
    reject('model-rejects-quotient-instead-of-remainder', lambda: matcher.fixture.execute(bytes(altered), (0, 0, 0), 0))
    altered2 = bytearray(body)
    word = int.from_bytes(body[84:88], 'little')
    altered2[84:88] = ((word & ~0xF80) | (3 << 7)).to_bytes(4, 'little')
    reject('model-rejects-wrong-quarter-shift', lambda: matcher.fixture.execute(bytes(altered2), (400, 12, 31), 0))
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    text = (ROOT / pin['source']).read_text()
    for name, old, new in (('wrong-adjustment', 'var_r7 += 0xC', 'var_r7 += 0xB'),
        ('wrong-return-word', '>> 32', '>> 0'),
        ('conflicting-existing-c-prototype', 'native_utility_child_arm7_divpair_arm_03805184', 'native_utility_child_arm7_arm_03805184')):
        if old not in text:
            raise ValueError('Expected ordinary C mutation absent')
        source = matcher.WORK / 'controls' / (name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text.replace(old, new))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()))
        reject('actual-compiled-C-rejects-' + name, lambda changed=changed: matcher.build(changed))
    placeholder = matcher.WORK / 'controls' / 'pseudo-second-register.c'
    placeholder.write_text(text.replace('>> 32', '>> SECOND_REG(0)'))
    changed = dict(pin, source=placeholder.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(placeholder.read_bytes()))
    reject('generated-pseudo-register-helper-not-source', lambda: matcher.build(changed))
    matcher.build(pin)
    if len(validate(report)) != len(positive):
        raise ValueError('Positive complete caller proof not restored')
    output = ROOT / 'evidence/verification/arm7-lane-child-wordpair124-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'positiveUnits': 1, 'matchedInitializedBytes': 124, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeProductChecks': True, 'acceptedSourcesOrNativeInstructionsPatched': False}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
