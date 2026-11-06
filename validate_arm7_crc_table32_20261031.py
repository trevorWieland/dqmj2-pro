import copy
import json
from pathlib import Path
import match_arm7_crc_table32_20261031 as matcher
import arm7_crc_table32_native_20261031 as fixture
from derive_arm7_crc_table32_20261031 import derive, source_text
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = matcher.REPORT
MATCHER_SHA = '037f74a499a5e918b269e78de8ab70f96fa8160d0f921492a65af534b77662fa'
_FRESH = {}


def checked(name, expected):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or matcher.digest(path.read_bytes()) != expected:
        raise ValueError('Missing or changed mathematical table input/product: ' + str(name))
    return path


def validate(report):
    checked(Path(matcher.__file__).name, MATCHER_SHA)
    pins = matcher.verify_inputs()
    required = {Path(matcher.__file__).name, matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.SOURCE} | {row['path'] for row in pins}
    if {row['path'] for row in report['generatorSources']} != required or len(report['generatorSources']) != len(required):
        raise ValueError('Mathematical source/runtime closure differs')
    for row in report['generatorSources']:
        checked(row['path'], row['sha256'])
    expected = {'generator': Path(matcher.__file__).name, 'generatorSha256': MATCHER_SHA, 'pinnedGeneratorAndRuntimeDependencies': pins,
        'romSha256': matcher.ROM_SHA, 'dataAliases': {matcher.NAME: hex(matcher.FIRST)}, 'nativeSymbols': {}, 'initializedDataBytes': 32,
        'ordinaryCCodeBytes': 0, 'ordinaryFunctionCredit': 0, 'generatedFromIndependentMathematics': True,
        'sourceDataBytesFromNativeInput': 0, 'sourceCreditAcceptedByThisScript': 0, 'wholeModuleLinked': False,
        'configuredBoundariesOrSymbolsChanged': False}
    if any(report.get(key) != value for key, value in expected.items()) or len(report['dataMatches']) != 1:
        raise ValueError('Qualified non-executable source-data scope differs')
    row = report['dataMatches'][0]
    for path, key in ((row['source'], 'sourceSha256'), (row['object'], 'objectSha256'), (row['compiler'], 'compilerSha256'),
        (row['splitObject'], 'splitObjectSha256'), (row['linkedElf'], 'linkedElfSha256'), (row['linkedDataBinary'], 'linkedDataBinarySha256'), (row['lcf'], 'lcfSha256')):
        checked(path, row[key])
    checked(matcher.LINKER, row['linkerSha256'])
    key = matcher.digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if key not in _FRESH:
        fresh = matcher.compile_data()
        native = fixture.oracle((ROOT / fresh['linkedDataBinary']).read_bytes())
        _FRESH[key] = (fresh, native)
    if (row, report['nativeOriginalConsumers']) != _FRESH[key]:
        raise ValueError('Current complete source/genuine-link/classification/original-consumer evidence differs')
    return {(row['program'], row['processor'], row['module'], row['address'], 'data'): row}


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
            raise ValueError('Invalid mathematical table evidence accepted: ' + name)

    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('generator-change', ('generatorSha256',), '0' * 64),
        ('closure-removed', ('generatorSources',), []),
        ('runtime-closure-removed', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('code-credit-invented', ('ordinaryCCodeBytes',), 32),
        ('function-credit-invented', ('ordinaryFunctionCredit',), 1),
        ('original-bytes-as-generator', ('sourceDataBytesFromNativeInput',), 32),
        ('whole-module-credit', ('wholeModuleLinked',), True),
        ('shared-config-promotion', ('configuredBoundariesOrSymbolsChanged',), True),
        ('wrong-program', ('dataMatches', 0, 'program'), ''),
        ('wrong-processor', ('dataMatches', 0, 'processor'), 'arm9'),
        ('wrong-module', ('dataMatches', 0, 'module'), 'utility-child-arm7-wram'),
        ('wrong-mode', ('dataMatches', 0, 'mode'), 'arm'),
        ('wrong-start', ('dataMatches', 0, 'address'), '0x27f7f76'),
        ('wrong-extent', ('dataMatches', 0, 'bytes'), 64),
        ('executable-symbol-invented', ('dataMatches', 0, 'sourceSymbolType'), 'STT_FUNC'),
        ('byte-gate-disabled', ('dataMatches', 0, 'exactAfterRealMwLink'), False),
        ('bss-as-initialized', ('dataMatches', 0, 'kind'), 'bss'),
        ('object-extent-invented', ('dataMatches', 0, 'classification', 'originalTotalObjectExtentClaimed'), True),
        ('code-overlap-hidden', ('dataMatches', 0, 'classification', 'configuredCodeOverlaps'), [{'address': '0x27f7f74'}]),
        ('code-branch-hidden', ('dataMatches', 0, 'classification', 'knownDirectBranchesIntoRange'), [{'target': '0x27f7f74'}]),
        ('denominator-increased', ('dataMatches', 0, 'classification', 'initializedCoverageDenominatorIncrease'), 32),
        ('consumer-code-credit', ('nativeOriginalConsumers', 'ordinarySourceFunctionCredit'), 1),
        ('fake-native-return', ('nativeOriginalConsumers', 'verifiedReturn'), False),
        ('table-index-unqualified', ('nativeOriginalConsumers', 'all16TableIndexesRead'), [0]),
        ('provider-injected', ('nativeOriginalConsumers', 'providerReplacements'), ['fake CRC']),
        ('consumer-code-replaced', ('nativeOriginalConsumers', 'originalConsumerCodeChanged'), True),
        ('execute-permission-invented', ('dataMatches', 0, 'mwldExternalRawRegionElfSidecar', 'runtimeExecutePermissionClaimed'), True),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        target = changed
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    row = report['dataMatches'][0]
    for name, path in (('missing-object-after-fresh-cache', ROOT / row['object']), ('missing-linked-table-after-fresh-cache', ROOT / row['linkedDataBinary'])):
        saved = path.read_bytes()
        try:
            path.unlink()
            reject(name, lambda: validate(report))
        finally:
            path.write_bytes(saved)
    values = derive()
    altered = list(values)
    altered[5] ^= 1
    mutants = []
    original = (ROOT / row['inputModule']).read_bytes()[matcher.FIRST - 0x027E0000:matcher.LAST - 0x027E0000]
    for name, wrong in (('wrong-polynomial', derive(0x8408)), ('wrong-one-entry', altered)):
        directory = matcher.WORK / 'controls' / name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / 'table.c'
        source.write_text(source_text(wrong))
        payload, proof = matcher.build_data(source, directory)
        if payload == original or payload != b''.join(value.to_bytes(2, 'little') for value in wrong):
            raise ValueError('Actual whole-C mutant did not compile/genuinely link its changed data')
        cases = []
        for byte in range(32):
            before, after = fixture.execute(original, (byte, 0), byte), fixture.execute(payload, (byte, 0), byte)
            if not before['actualReturn'] or not after['actualReturn']:
                raise ValueError('Data mutant consumer failed actual return')
            cases.append({'byte': byte, 'actualOriginalConsumerReturns': 2, 'nativeResult': before['registers'][0],
                'mutantResult': after['registers'][0], 'changed': before['registers'][0] != after['registers'][0]})
        if not any(item['changed'] for item in cases) or not any(not item['changed'] for item in cases):
            raise ValueError('Mutant lacks native rejection and positive-control outcomes')
        mutants.append({'name': name, 'sourceLinkProof': proof, 'wholeSourceCObjectChanged': True,
            'byteComparisonRejects': True, 'cases': cases, 'actualOriginalConsumerReturns': 64, 'ordinarySourceFunctionCredit': 0})
    reject('wrong-table-element-count', lambda: source_text(values[:8]))
    reject('unrepresentable-halfword-value', lambda: source_text(values[:-1] + [0x10000]))
    matcher.compile_data()
    if len(validate(report)) != len(positive):
        raise ValueError('Positive mathematical table evidence not restored')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': matcher.digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': matcher.digest(REPORT.read_bytes()),
        'controls': controls, 'allPassed': all(item['rejected'] for item in controls), 'compiledAndGenuinelyLinkedWholeCMutants': mutants,
        'mutantOriginalConsumerReturns': 128, 'positiveDataObjects': 1, 'candidateInitializedDataBytes': 32,
        'acceptedCredit': 0, 'ordinarySourceFunctionCredit': 0, 'originalConsumerCodeChanged': False,
        'producerRunsBeforeProductChecks': True, 'sharedConfigOrRegistryEdits': False}
    output = ROOT / 'evidence/verification/arm7-crc-table32-controls-20261031.json'
    write_json(output, result)
    print(json.dumps({'report': output.relative_to(ROOT).as_posix(), 'sha256': matcher.digest(output.read_bytes()),
        'controls': len(controls), 'realCMutants': len(mutants), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
