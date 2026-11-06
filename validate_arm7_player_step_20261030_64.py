import copy
import hashlib
import json
from pathlib import Path
import match_arm7_player_step_20261030_64 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-player-step-20261030-64.json'
GENERATOR_SHA = 'bd49d361a2fe2bbbf2bd04aee94d09ee69c1baa52de25a8132e4ad5ed6dba21a'
REFERENCE = {'path': 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_seq.c',
    'sha256': 'ebfde6b73e78a1f0e1f84624daf60d1ce46766807922e004d0ffb2421e894eeb',
    'upstreamCommit': 'b623abef1b4dfe204ca50aab42447ac00c134290', 'functions': ['PlayerStepTicks', 'TrackStepTicks', 'TrackPlayNote'],
    'compilerInput': False, 'sameSdkVersionPresumed': False}
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
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {item['path'] for item in pins}
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
    if report.get('matchedInitializedBytes') != 2896 or report.get('matchedInstructionBytes') != 2884 or report.get('generatedLiteralBytes') != 12:
        raise ValueError('Measured track code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 2648 or report.get('actualSeparatelyObservedNestedReturns') != 76330 or report.get('actualOriginalPreparationReturns') != 1442:
        raise ValueError('Actual outer versus nested track return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Track scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Track scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    verify_file(REFERENCE['path'], REFERENCE['sha256'])
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 1:
        raise ValueError('Track qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed track source/profile differs')
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
        ('missing-masked-dispatch-exclusions', ('matches', 0, 'oracle', 'excludedMaskedDispatchDefaults'), []),
        ('unverified-full-state', ('matches', 0, 'oracle', 'fullRegistersFlagsStackAndMemoryCompared'), False),
        ('incomplete-velocity-domain', ('matches', 0, 'oracle', 'noteVelocityProducer', 'all256PositivePlaybackVelocitiesTested'), False),
        ('incomplete-own-coverage', ('matches', 0, 'oracle', 'allReachableOwnInstructionAddressesVisited'), []),
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
    for name, before, after in (
        ('wrong-track-volume', 'track->volume = par._u8;', 'track->volume = par._u8 ^ 1;'),
        ('signed-byte-velocity', 'u8 velocity = native_host_arm7_arm_03800290(track);', 's8 velocity = native_host_arm7_arm_03800290(track);')):
        directory = matcher.WORK/'controls'/name
        directory.mkdir(parents=True, exist_ok=True)
        source = directory/'native_arm7_wram_03800cf0.c'
        if before not in original:
            raise ValueError('Expected ordinary typed source expression is absent')
        source.write_text(original.replace(before, after))
        changed = copy.deepcopy(pin)
        dependencies = []
        for item in pin['sourceDependencies']:
            destination = directory/Path(item['path']).name
            destination.write_bytes((ROOT/item['path']).read_bytes())
            dependencies.append(dict(path=destination.relative_to(ROOT).as_posix(), sha256=digest(destination.read_bytes())))
        changed.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()), sourceDependencies=dependencies)
        reject('actual-compiler-link-rejects-'+name, lambda changed=changed: matcher.build(changed))
    matcher.build(pin)
    if len(validate(report)) != len(accepted):
        raise ValueError('Track positive proof not restored after controls')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 2896, 'actualOriginalAndCompiledReturns': 2648,
        'actualSeparateNestedReturns': 76330, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeSourceVariants': 'Separately compiled ordinary C mutations; accepted source, object instructions and relocation addends remain unchanged'}
    destination = ROOT / 'evidence/verification/arm7-player-step-controls-20261030-64.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
