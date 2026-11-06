import copy
import json
from pathlib import Path
import match_arm7_lane_child_record_check172_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = '684c82ad30c092d10bb99509c827cb309449a1855a12fbe56e2eeb1dfb83b5e3'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed current record-header input/product: ' + str(name))
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
        raise ValueError('Frozen record-header generator/runtime differs')
    expected = {'romSha256': matcher.ROM, 'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'module': 'utility-child-arm7-main',
        'matchedInitializedBytes': 172, 'matchedInstructionBytes': 164, 'generatedLiteralBytes': 8,
        'actualNativeAndCompiledReturns': 256, 'actualSeparatelyObservedNestedReturns': 81152,
        'providerFreeReturnCredit': 256, 'physicalHardwareExecutionCredit': 0, 'ordinaryAssemblyOrBlobCredit': 0,
        'originalDataSourceCredit': 0, 'calleeSourceCredit': 0, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if any(report.get(key) != value for key, value in expected.items()):
        raise ValueError('Typed source qualified scope or observed return counts differ')
    rows = report['matches']
    profile = json.loads(matcher.PROFILE.read_text())['matches']
    if len(rows) != 1 or len(profile) != 1:
        raise ValueError('One complete qualified record-header caller required')
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
        raise ValueError('Current complete source/link/boundary/primitive native evidence differs')
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
            raise ValueError('Invalid record caller qualification accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-program', ('program',), ''),
        ('wrong-processor', ('processor',), 'arm9'),
        ('wrong-module', ('module',), 'utility-child-arm7-wram'),
        ('generator-change', ('generatorSha256',), '0' * 64),
        ('generator-closure-removed', ('generatorSources',), []),
        ('runtime-closure-removed', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('literal-as-executable', ('matchedInstructionBytes',), 172),
        ('literal-pool-omitted', ('generatedLiteralBytes',), 0),
        ('helper-as-source', ('calleeSourceCredit',), 152),
        ('whole-module-claim', ('wholeModuleLinked',), True),
        ('nested-as-caller-return', ('actualNativeAndCompiledReturns',), 81408),
        ('entry-mode-change', ('matches', 0, 'mode'), 'thumb'),
        ('source-change', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('include-closure-added', ('matches', 0, 'sourceDependencies'), ['unapproved.h']),
        ('blob-credit', ('matches', 0, 'originalObjectScaffolding'), True),
        ('linked-byte-gate-disabled', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('byte-getter-not-original', ('matches', 0, 'oracle', 'actualSeparatelyObservedByteGetterReturns'), 0),
        ('crc-step-not-original', ('matches', 0, 'oracle', 'actualSeparatelyObservedCrcStepReturns'), 0),
        ('provider-injected', ('matches', 0, 'oracle', 'providerReplacements'), ['fake CRC']),
        ('budget-as-return', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('missing-pointer-proof', ('matches', 0, 'boundaries', 'runtimePointerWord', 'sha256'), '0' * 64),
        ('absolute-word-as-bss', ('matches', 0, 'boundaries', 'runtimePointerWord', 'moduleBssOwnershipCredit'), 4),
        ('external-word-data-credit', ('matches', 0, 'boundaries', 'runtimePointerWord', 'sourceDataCredit'), 4),
        ('unapproved-global-declaration', ('matches', 0, 'boundaries', 'declarationClosure', 'scalarWordAlias'), 'old-array-view'),
        ('historical-source-mutation', ('matches', 0, 'boundaries', 'declarationClosure', 'historicalSourcesChanged'), True),
        ('interior-omission', ('matches', 0, 'boundaries', 'outsideInteriorReferences'), [{'pc': '0x1'}]),
        ('symbol-publication-omitted', ('nativeSymbols',), {}),
        ('interworking-confusion', ('nativeSymbolEntries', 0, 'mode'), 'thumb'),
        ('relocation-addend-patch', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 0),
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
    qualified = matcher.linker.qualified_runtime_word
    for name, changes in (
        ('wrong-program-pointer', {'program': ''}), ('wrong-module-pointer', {'module': 'utility-child-arm7-wram'}),
        ('wrong-start-pointer', {'address': '0x27f5b14'}), ('wrong-size-pointer', {'bytes': 176}),
        ('wrong-mode-pointer', {'mode': 'thumb'}), ('wrong-processor-pointer', {'processor': 'arm9'}),
        ('qualification-omitted', {'runtimePointerQualification': {}}),
        ('unproved-eight-byte-extent', {'runtimePointerQualification': dict(matcher.linker.RUNTIME_WORD_REFERENCE, storageBytes=8)}),
        ('wrong-module-input', {'inputModuleSha256': '0' * 64})):
        changed = dict(row, **changes)
        reject(name, lambda changed=changed: qualified(changed, 0x0380FFF4))
    reject('outside-qualified-word', lambda: qualified(row, 0x0380FFF8))
    import link_arm7_bulk_20261030 as original_linker
    reject('original-linker-still-refuses-unowned-word', lambda: original_linker.validate(row, matcher.WORK / 'original-refusal'))
    body = (Path(row['realArm7Link']['cwd']) / 'caller.bin').read_bytes()
    altered = bytearray(body)
    altered[48:52] = (0xE3A00001).to_bytes(4, 'little')
    reject('independent-invalid-length-result', lambda: matcher.fixture.execute(bytes(altered), matcher.fixture.cases()[0], 0))
    altered = bytearray(body)
    word = int.from_bytes(body[132:136], 'little')
    altered[132:136] = ((word & ~0xF80) | (8 << 7)).to_bytes(4, 'little')
    case = dict(matcher.fixture.cases()[0], length=0xA4, pattern='random', output=True)
    reject('independent-raw-output-word-packing', lambda: matcher.fixture.execute(bytes(altered), case, 7))
    pin = json.loads(matcher.PROFILE.read_text())['matches'][0]
    text = (ROOT / pin['source']).read_text()
    for name, old, new in (('wrong-header-stride', 'record + 2', 'record + 4'),
        ('wrong-lower-bound', '0xA4', '0xA3'), ('wrong-packed-output', 'value << 16', 'value << 8')):
        if old not in text:
            raise ValueError('Expected real C mutation missing')
        source = matcher.WORK / 'controls' / (name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text.replace(old, new))
        changed = dict(pin, source=source.relative_to(ROOT).as_posix(), sourceSha256=matcher.digest(source.read_bytes()))
        reject('fresh-compiled-C-' + name, lambda changed=changed: matcher.build(changed))
    matcher.build(pin)
    if len(validate(report)) != len(positive):
        raise ValueError('Positive full caller not restored')
    output = ROOT / 'evidence/verification/arm7-lane-child-record-check172-controls-20261031.json'
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'positiveUnits': 1, 'matchedInitializedBytes': 172, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'producerRunsBeforeProductChecks': True, 'acceptedSourcesOrNativeInstructionsPatched': False,
        'scope': 'One complete child-main caller, original primitives and absolute four-byte descriptor word; no callee/data/module source credit'}
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()), 'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()


