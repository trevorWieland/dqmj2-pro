import copy
import hashlib
import json
from pathlib import Path
import match_arm7_seq_access_20261030 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-seq-access-20261030.json'
GENERATOR_SHA = '3cb1656545fbae9eb773021678651e1c2d7e1c23a447465c846a509414a6155a'
REFERENCE = {'path': 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_seq.c',
    'sha256': 'ebfde6b73e78a1f0e1f84624daf60d1ce46766807922e004d0ffb2421e894eeb',
    'upstreamCommit': 'b623abef1b4dfe204ca50aab42447ac00c134290', 'functions': ['PlayerGetVariablePointer', 'AllocateTrack', 'TrackMute'],
    'compilerInput': False, 'sameSdkVersionPresumed': False,
    'tableDeclaration': {'path': 'deps/references/pokediamond-b623abef/arm7/lib/include/SND_util.h',
        'sha256': '1e2e5e7eb0ee6fdb86fcb531ad3d3e437d302abcd5ae06579640e36f471c5f45', 'entries': 128}}
_FRESH = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path(name):
    result = (ROOT / name).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError('Track input/product path escaped repository')
    return result


def verify_file(name, sha):
    current = path(name)
    if not current.is_file() or digest(current.read_bytes()) != sha:
        raise ValueError('Current track input/product changed or missing: ' + name)
    return current


def derived_bindings(rows):
    symbols, entries = {}, []
    for row in rows:
        raw = verify_file(row['binary'], row['inputModuleSha256']).read_bytes()
        first = int(row['address'], 0) - row['base']
        for rel in row['relocations']:
            binding = row['realArm7Link']['bindings'][rel['symbol']]
            symbols[rel['symbol']] = binding['address']
            entries.append(dict(binding, symbol=rel['symbol'], sourceRelocationOffset=rel['offset'], sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'], nativeEncodedWord=hex(int.from_bytes(raw[first + rel['offset']:first + rel['offset'] + 4], 'little')), sourceCredit=0,
                callerIdentity={key: row[key] for key in ('program', 'processor', 'module', 'address', 'mode')}))
    return symbols, entries


def validate(report):
    if report.get('generator') != Path(matcher.__file__).name or report.get('generatorSha256') != GENERATOR_SHA:
        raise ValueError('Frozen track matcher identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PROFILE_SHA)
    verify_file(matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.PIN_SHA)
    required = {report['generator'], 'arm7_seq_access_native_20261030.py', 'arm7_seq_access_boundaries_20261030.py',
        'arm7_seq_neighbor_native_20261030.py', 'arm7_seq_neighbor_model_20261030.py',
        'link_arm7_bulk_20261030.py', matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix(),
        'crossreuse_utility_c.py', 'elf_units.py', 'link_runtime_unit.py', 'arm7_runtime.py', 'utility_runtime.py',
        'match_runtime.py', 'match_lowlevel.py', 'project.py'}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete track generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published frozen track dependency closure differs')
    for item in pins:
        verify_file(item['path'], item['sha256'])
    verify_file('inputs/game.nds', matcher.ROM)
    if report.get('romSha256') != matcher.ROM or report.get('processor') != 'arm7' or report.get('program') != '' or report.get('module') != 'arm7-wram':
        raise ValueError('Track qualified ROM/processor/module identity differs')
    if report.get('matchedInitializedBytes') != 264 or report.get('matchedInstructionBytes') != 256 or report.get('generatedLiteralBytes') != 8:
        raise ValueError('Measured track code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 1910 or report.get('actualSeparatelyObservedNestedReturns') != 634:
        raise ValueError('Actual outer versus nested track return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Track scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Track scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    verify_file(REFERENCE['path'], REFERENCE['sha256'])
    verify_file(REFERENCE['tableDeclaration']['path'], REFERENCE['tableDeclaration']['sha256'])
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 3:
        raise ValueError('Track qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed track source/profile differs')
        verify_file(pin['source'], pin['sourceSha256'])
        verify_file(pin['compiler'], pin['compilerSha256'])
        verify_file(row['object'], row['objectSha256'])
        proof = row['realArm7Link']
        verify_file(proof['linkCommand'][0], proof['linkerSha256'])
        verify_file(proof['lcf'], proof['lcfSha256'])
        verify_file(str(Path(proof['cwd']) / 'linked.elf'), proof['linkedElfSha256'])
        verify_file(str(Path(proof['cwd']) / 'caller.bin'), pin['targetSha256'])
        for anchor in proof['zeroCodeAnchors']:
            verify_file(anchor['object'], anchor['objectSha256'])
    symbols, entries = derived_bindings(rows)
    if report.get('nativeSymbols') != symbols or report.get('nativeSymbolEntries') != entries:
        raise ValueError('Published typed-track function/data map differs from qualified real-link bindings/native addends')
    cache_key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if cache_key not in _FRESH:
        _FRESH[cache_key] = json.loads(json.dumps([matcher.build(pin) for pin in profile['matches']]))
    if rows != _FRESH[cache_key]:
        raise ValueError('Published track source/link/boundary/native records differ from full fresh proof')
    return {('arm7', '', 'arm7-wram', row['address'], 'arm'): row for row in rows}


def main():
    report = json.loads(REPORT.read_text())
    accepted = validate(report)
    controls = []
    def reject(name, operation):
        try:
            operation()
        except Exception as error:
            controls.append({'name': name, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)})
        else:
            raise ValueError('Invalid track proof accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-namespace', ('processor',), 'arm9'),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('data-source-overclaim', ('originalDataSourceCredit',), 8),
        ('callee-source-overclaim', ('calleeSourceCredit',), 156),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('same-sdk-presumption', ('referenceProvenance', 'sameSdkVersionPresumed'), True),
        ('outer-count-includes-nested', ('actualNativeAndCompiledReturns',), 2544),
        ('wrong-source-mode', ('matches', 0, 'mode'), 'thumb'),
        ('absent-link-comparison-flag', ('matches', 1, 'exactAfterDeclaredRelocation'), False),
        ('source-closure-mutation', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 2, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 2, 'oracle', 'verifiedReturn'), False),
        ('unsupported-return-credit', ('matches', 2, 'oracle', 'unsupportedReturnCredit'), 1),
        ('replaced-native-list-helpers', ('matches', 2, 'oracle', 'providerReplacements'), ['replacement']),
        ('invented-mute-r0-result', ('matches', 2, 'oracle', 'returnContract'), 'meaningful u32 result'),
        ('narrowed-free-sentinel', ('matches', 1, 'oracle', 'returnContract'), 'u8 index or255'),
        ('unbounded-pointer-validity', ('matches', 0, 'oracle', 'returnContract'), 'valid halfword storage for every index'),
        ('missing-native-symbol-map', ('nativeSymbols',), {}),
        ('unqualified-native-symbol-mode', ('nativeSymbolEntries', 0, 'mode'), 'thumb'),
        ('changed-source-addend', ('matches', 0, 'realArm7Link', 'unchangedRelocations', 0, 'explicitAddend'), 4),
        ('changed-published-addend', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 4),
        ('incomplete-own-coverage', ('matches', 2, 'oracle', 'allOwnInstructionAddressesVisited'), []),
    )
    for name, keys, value in changes:
        changed = copy.deepcopy(report)
        current = changed
        for key in keys[:-1]:
            current = current[key]
        current[keys[-1]] = value
        reject(name, lambda changed=changed: validate(changed))
    first = report['matches'][0]
    binary = path(str(Path(first['realArm7Link']['cwd']) / 'caller.bin'))
    saved = binary.read_bytes()
    try:
        binary.unlink()
        reject('missing-current-linked-product-after-cache', lambda: validate(report))
        binary.write_bytes(bytes([saved[0] ^ 1]) + saved[1:])
        reject('changed-current-linked-product-after-cache', lambda: validate(report))
    finally:
        binary.write_bytes(saved)
    def body(row):
        return path(str(Path(row['realArm7Link']['cwd']) / 'caller.bin')).read_bytes()
    def code_reject(name, row, offset, word, case):
        modified = bytearray(body(row))
        modified[offset:offset + 4] = word.to_bytes(4, 'little')
        reject(name, lambda: matcher.fixture.execute(row, bytes(modified), case, 0))
    getter, allocator, mute = report['matches']
    code_reject('model-rejects-wrong-player-id-offset', getter, 40, 0xE5D02000,
        {'pointer': matcher.fixture.memory.DATA + 0x3000, 'index': 0, 'playerId': 255, 'invalidPlayer': False, 'passes': 1})
    code_reject('model-rejects-narrowed-minus-one-sentinel', allocator, 56, 0xE3A000FF,
        {'firstFree': 32, 'inactive': 128, 'active': 255, 'passes': 1})
    code_reject('model-rejects-shortened-track-bound', allocator, 48, 0xE350001F,
        {'firstFree': 31, 'inactive': 128, 'active': 255, 'passes': 1})
    code_reject('model-rejects-wrong-mute-bit', mute, 56, 0xE3800008,
        {'mode': 1, 'count': 3, 'kind': 0, 'active': 1, 'passes': 1})
    code_reject('model-rejects-omitted-mode3-free', mute, 116, 0xE1A00000,
        {'mode': 3, 'count': 3, 'kind': 0, 'active': 1, 'passes': 1})
    pin = copy.deepcopy(json.loads(matcher.PROFILE.read_text())['matches'][1])
    source = matcher.WORK / 'controls/wrong-narrowed-sentinel.c'
    source.parent.mkdir(parents=True, exist_ok=True)
    original = (ROOT / pin['source']).read_text()
    if 'return -1;' not in original:
        raise ValueError('Expected ordinary first-free source sentinel absent')
    source.write_text(original.replace('return -1;', 'return 255;'))
    pin.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
    reject('actual-compiler-link-rejects-narrowed-sentinel', lambda: matcher.build(pin))
    matcher.build(json.loads(matcher.PROFILE.read_text())['matches'][1])
    if len(validate(report)) != len(accepted):
        raise ValueError('Track positive proof not restored after controls')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 264, 'actualOriginalAndCompiledReturns': 1910,
        'actualSeparateNestedReturns': 634, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeCodeVariants': 'In-memory rejection controls only; accepted compiler objects/instructions/addends remain untouched'}
    destination = ROOT / 'evidence/verification/arm7-seq-access-controls-20261030.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
