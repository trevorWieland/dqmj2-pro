import copy
import hashlib
import json
from pathlib import Path
import match_arm7_channel_parameters_20261030_67 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-channel-parameters-20261030-67.json'
GENERATOR_SHA = '9de204d540ffa633a120e2aeda53df03be864663fbf3269c2d1a7043825206be'
REFERENCE = {'path': 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_exChannel.c',
    'sha256': 'eb777836a18e618d23f2de2bde632dfbf1603e1ab1af4b247caef22afe419a35',
    'upstreamCommit': 'b623abef1b4dfe204ca50aab42447ac00c134290', 'functions': ['SND_UpdateExChannelEnvelope', 'SND_SetExChannelAttack'],
    'compilerInput': False, 'sameSdkVersionPresumed': False}
_FRESH = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path(name):
    result = (ROOT / name).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError('Channel-parameter input/product path escaped repository')
    return result


def verify_file(name, sha):
    current = path(name)
    if not current.is_file() or digest(current.read_bytes()) != sha:
        raise ValueError('Current channel-parameter input/product changed or missing: ' + name)
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
        raise ValueError('Frozen channel-parameter matcher identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PROFILE_SHA)
    verify_file(matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.PIN_SHA)
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {item['path'] for item in pins}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete channel-parameter generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published frozen channel-parameter dependency closure differs')
    for item in pins:
        verify_file(item['path'], item['sha256'])
    verify_file('inputs/game.nds', matcher.ROM)
    if report.get('romSha256') != matcher.ROM or report.get('processor') != 'arm7' or report.get('program') != '' or report.get('module') != 'arm7-wram':
        raise ValueError('Channel-parameter qualified ROM/processor/module identity differs')
    if report.get('matchedInitializedBytes') != 296 or report.get('matchedInstructionBytes') != 288 or report.get('generatedLiteralBytes') != 8:
        raise ValueError('Measured channel-parameter code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 3080 or report.get('actualSeparatelyObservedNestedReturns') != 0 or report.get('providerFreeOriginalAndCompiledReturns') != 3080 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0 or report.get('independentlyCheckedSigned64Returns') != 0 or report.get('originalBiosExecutionCredit') != 0:
        raise ValueError('Actual outer versus nested channel-parameter return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Channel-parameter scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Channel-parameter scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    verify_file(REFERENCE['path'], REFERENCE['sha256'])
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 3:
        raise ValueError('Channel-parameter qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed channel-parameter source/profile differs')
        verify_file(pin['source'], pin['sourceSha256'])
        for item in pin['sourceDependencies']:
            verify_file(item['path'], item['sha256'])
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
        raise ValueError('Published typed-channel-parameter function/data map differs from qualified real-link bindings/native addends')
    cache_key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if cache_key not in _FRESH:
        _FRESH[cache_key] = dict(rows=json.loads(json.dumps([matcher.build(pin) for pin in profile['matches']])), producer=matcher.producer.producer())
    if rows != _FRESH[cache_key]['rows'] or report.get('originalNoteAttackByteProducer') != _FRESH[cache_key]['producer']:
        raise ValueError('Published channel-parameter source/link/boundary/native records differ from full fresh proof')
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
            raise ValueError('Invalid channel-parameter proof accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-namespace', ('processor',), 'arm9'),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('data-source-overclaim', ('originalDataSourceCredit',), 8),
        ('callee-source-overclaim', ('calleeSourceCredit',), 156),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('same-sdk-presumption', ('referenceProvenance', 'sameSdkVersionPresumed'), True),
        ('inflated-entry-count', ('actualNativeAndCompiledReturns',), 1032),
        ('wrong-source-mode', ('matches', 0, 'mode'), 'thumb'),
        ('absent-link-comparison-flag', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('source-closure-mutation', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 0, 'oracle', 'verifiedReturn'), False),
        ('unsupported-return-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('replaced-native-list-helpers', ('matches', 0, 'oracle', 'providerReplacements'), ['replacement']),
        ('invented-mute-r0-result', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'meaningful u32 result'),
        ('invented-result-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'returns number of active records'),
        ('false-complete-game-state', ('matches', 0, 'oracle', 'limitations'), ['all save/game state initialized']),
        ('missing-native-symbol-map', ('nativeSymbols',), None),
        ('invented-native-symbol-entries', ('nativeSymbolEntries',), [{'mode': 'thumb'}]),
        ('invented-source-addend', ('matches', 0, 'realArm7Link', 'unchangedRelocations'), [{'explicitAddend': 4}]),
        ('invented-published-addend', ('nativeSymbolEntries',), [{'unchangedExplicitAddend': 4}]),
        ('missing-declared-includes', ('matches', 0, 'sourceDependencies'), []),
        ('physical-sound-overclaim', ('matches', 0, 'oracle', 'hardwareExecutionCredit'), 1),
        ('unverified-full-state', ('matches', 0, 'oracle', 'fullRegistersFlagsStackAndMemoryCompared'), False),
        ('narrow-word-return-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'u8 attenuation'),
        ('changed-byte-producer-domain', ('originalNoteAttackByteProducer', 'actualByteDomain'), [0,127]),
        ('producer-caller-source-overclaim', ('originalNoteAttackByteProducer', 'parentSourceCredit'), 328),
        ('invented-byte-producer-argument', ('originalNoteAttackByteProducer', 'records', 0, 'argumentWords'), [0,256]),
        ('wrong-data-window-hash', ('originalNoteAttackByteProducer', 'originalInitializedDataWindow', 'sha256'), '0'*64),
        ('incomplete-own-coverage', ('matches', 0, 'oracle', 'allOwnInstructionAddressesVisited'), []),
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
    pin = copy.deepcopy(json.loads(matcher.PROFILE.read_text())['matches'][0])
    original = (ROOT/pin['source']).read_text()
    header_name = Path(pin['sourceDependencies'][0]['path']).name
    original_header = (ROOT/pin['sourceDependencies'][0]['path']).read_text()
    for name, changed_source, changed_header in (
        ('wrong-attenuation-offset', original, original_header.replace('envAttenuation, sweepCounter, sweepLength', 'sweepCounter, envAttenuation, sweepLength')),
        ('narrow-envelope-return', original.replace('return chn->envAttenuation >> 7;', 'return (u8)(chn->envAttenuation >> 7);'), original_header),
        ('unsigned-attack-product', original.replace('(s32)((0u', '(u32)((0u'), original_header),
        ('boolean-step-equality', original.replace('if (step)', 'if (step == 1)'), original_header),
        ('shortened-typed-data-window', original, original_header.replace('data_038071e0[147]', 'data_038071e0[146]'))):
        if changed_source == original and changed_header == original_header:
            raise ValueError('Expected typed source/header control expression absent')
        directory = matcher.WORK/'controls'/name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory/'native_arm7_wram_037ff82c.c'
        source.write_text(changed_source)
        header = directory/header_name
        header.write_text(changed_header)
        changed = copy.deepcopy(pin)
        changed.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()),
            sourceDependencies=[dict(path=header.relative_to(ROOT).as_posix(), sha256=digest(header.read_bytes()))])
        reject('actual-compiler-link-rejects-'+name, lambda changed=changed: matcher.build(changed))
    setter_pin = copy.deepcopy(json.loads(matcher.PROFILE.read_text())['matches'][1])
    bad_directory = matcher.WORK/'controls'/'byte-exact-invalid-window'
    bad_directory.mkdir(parents=True, exist_ok=True)
    bad_source = bad_directory/'native_arm7_wram_037ff8d4.c'
    bad_source.write_bytes((ROOT/setter_pin['source']).read_bytes())
    bad_header = bad_directory/header_name
    bad_header.write_text(original_header.replace('data_038071e0[147]', 'data_038071e0[146]'))
    setter_pin.update(source=bad_source.relative_to(ROOT).as_posix(), sourceSha256=digest(bad_source.read_bytes()),
        sourceDependencies=[dict(path=bad_header.relative_to(ROOT).as_posix(),sha256=digest(bad_header.read_bytes()))])
    attempt, compiled = matcher.crossreuse_utility_c.compile_origin(setter_pin, ROOT/setter_pin['compiler'], setter_pin['compilerFlags'], bad_directory)
    if compiled is None:
        raise ValueError(attempt)
    derived, offsets, body = compiled
    with (ROOT/derived['probeObject']).open('rb') as stream:
        elf = matcher.ELFFile(stream)
        symbol = next(row for row in elf.get_section_by_name('.symtab').iter_symbols() if row.name == setter_pin['name'])
        section, offset = symbol['st_shndx'],symbol['st_value']
    bad_entry = dict(setter_pin, object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
        relocations=[dict(row,format='SHT_RELA',explicitAddend=row['addend'],originalEncodedWord=body[row['offset']:row['offset']+4].hex()) for row in derived['relocations']])
    bad_link = matcher.linker.validate(bad_entry,bad_directory/'byte-only-link')
    if not bad_link['exactLinkedBytes']:
        raise ValueError('Expected binary-neutral wrong object-bound counterexample absent')
    reject('byte-exact-invalid-object-bound-remains-unaccepted',lambda: matcher.build(setter_pin))
    native_fixture = matcher.fixture.fixture
    def require_return(value):
        if not value['states'][0]['actualReturn']:
            raise ValueError('Bounded channel-parameter execution did not return')
    reject('instruction-exhaustion-is-not-return', lambda: require_return(native_fixture.execute(0x037FF82C, saved, native_fixture.cases(0x037FF82C)[1], 91, budget=1)))
    matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Channel-parameter positive proof not restored after controls')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 296, 'actualOriginalAndCompiledReturns': 3080,
        'actualSeparateNestedReturns': 0, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'byteExactInvalidDataWindow': dict(realLink=bad_link,declaredBytes=146,requiredBytes=147,actualByteExact=True,sourceCredit=0),
        'negativeSourceVariants': 'Four independently compiled logic/layout mutations, an explicit declared-object-bound rejection, and an actually byte-exact wrong-bound counterexample; accepted inputs remain unchanged'}
    destination = ROOT / 'evidence/verification/arm7-channel-parameters-controls-20261030-67.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
