import copy
import hashlib
import json
from pathlib import Path
import match_arm7_seq_public_20261030 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-seq-public-20261030.json'
GENERATOR_SHA = '43ba3ff340c281e2835c0e6529e64a6d12f980027804d2eb3f39dcf6a3149f37'
REFERENCE = {'path': 'deps/references/pokediamond-b623abef/arm7/lib/src/SND_seq.c',
    'sha256': 'ebfde6b73e78a1f0e1f84624daf60d1ce46766807922e004d0ffb2421e894eeb',
    'upstreamCommit': 'b623abef1b4dfe204ca50aab42447ac00c134290', 'functions': ['SND_StartPreparedSeq', 'SND_StopSeq', 'SND_PauseSeq', 'SND_SetTrackMute', 'SND_SetTrackAllocatableChannel', 'SND_InvalidateSeq', 'SNDi_SetPlayerParam', 'SNDi_SetTrackParam'],
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
    required = {report['generator'], 'arm7_seq_public_native_20261030.py', 'arm7_seq_public_boundaries_20261030.py',
        'arm7_seq_public_opcode_roles_20261030.py', 'arm7_seq_neighbor_opcode_roles_20261030.py', 'arm7_seq_access_native_20261030.py',
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
    if report.get('matchedInitializedBytes') != 828 or report.get('matchedInstructionBytes') != 792 or report.get('generatedLiteralBytes') != 36:
        raise ValueError('Measured track code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 3876 or report.get('actualSeparatelyObservedNestedReturns') != 36968:
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
    if len(rows) != 8:
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
        ('outer-count-includes-nested', ('actualNativeAndCompiledReturns',), 40844),
        ('wrong-source-mode', ('matches', 0, 'mode'), 'thumb'),
        ('absent-link-comparison-flag', ('matches', 1, 'exactAfterDeclaredRelocation'), False),
        ('source-closure-mutation', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 2, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('false-return', ('matches', 2, 'oracle', 'verifiedReturn'), False),
        ('unsupported-return-credit', ('matches', 2, 'oracle', 'unsupportedReturnCredit'), 1),
        ('replaced-native-list-helpers', ('matches', 2, 'oracle', 'providerReplacements'), ['replacement']),
        ('invented-void-r0-result', ('matches', 2, 'oracle', 'returnContract'), 'meaningful u32 result'),
        ('false-word-store-contract', ('matches', 7, 'oracle', 'returnContract'), 'scalar successful-store result'),
        ('false-parameter-bounds-claim', ('matches', 7, 'oracle', 'limitations'), ['all offsets universally valid']),
        ('missing-native-symbol-map', ('nativeSymbols',), {}),
        ('unqualified-native-symbol-mode', ('nativeSymbolEntries', 0, 'mode'), 'thumb'),
        ('changed-source-addend', ('matches', 0, 'realArm7Link', 'unchangedRelocations', 0, 'explicitAddend'), 4),
        ('changed-published-addend', ('nativeSymbolEntries', 0, 'unchangedExplicitAddend'), 4),
        ('incomplete-own-coverage', ('matches', 7, 'oracle', 'allOwnInstructionAddressesVisited'), []),
        ('discarded-word-role-proof', ('matches', 2, 'boundaries', 'initializedWordOpcodeQualifications'), []),
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
    prepared, stopped, paused, muted, allocated, invalidated, player_param, track_param = report['matches']
    def context(row, **changes):
        return dict(matcher.fixture.cases(int(row['address'], 0))[0], **changes)
    code_reject('model-rejects-wrong-prepared-bit', prepared, 16, 0xE3800004,
        context(prepared, flags=0))
    code_reject('model-rejects-inverted-status-mask', stopped, 64, 0x11A00410,
        context(stopped, flags=1, shared=True, pattern='empty'))
    code_reject('model-rejects-low-bit-only-pause-branch', paused, 40, 0xE3110001,
        context(paused, flag=256, count=1, pattern='one', flags=1))
    code_reject('model-rejects-omitted-last-track', muted, 80, 0xE356000F,
        context(muted, mask=0x8000, pattern='last', mode=0, trackFlags=255))
    code_reject('model-rejects-omitted-channel-mask-flag', allocated, 68, 0x11A01001,
        context(allocated, mask=1, pattern='one', trackFlags=0))
    code_reject('model-rejects-inverted-inclusive-bound', invalidated, 80, 0xE150000A,
        context(invalidated, bounds=[0x023C02FF, 0x023C0300], pattern='one', playerPattern='one', flags=1))
    code_reject('model-rejects-player-word-narrowing', player_param, 36, 0x07CC2001,
        context(player_param, size=4, offset=4, data=0xFFFFFFFF))
    code_reject('model-rejects-track-word-narrowing', track_param, 100, 0x07C08009,
        context(track_param, mask=1, pattern='one', size=4, offset=4, data=0x80000000))
    profiles = json.loads(matcher.PROFILE.read_text())['matches']
    for index, name, old, new in ((2, 'actual-compiler-link-rejects-low-bit-only-pause', 'if (flag)', 'if (flag & 1)'),
            (6, 'actual-compiler-link-rejects-player-word-narrowing', 'case 4: *(u32 *)((u8 *)current + offset) = data;', 'case 4: *(u16 *)((u8 *)current + offset) = (u16)data;')):
        pin = copy.deepcopy(profiles[index])
        source = matcher.WORK / ('controls/' + name + '.c')
        source.parent.mkdir(parents=True, exist_ok=True)
        original = (ROOT / pin['source']).read_text()
        if old not in original:
            raise ValueError('Expected ordinary C negative-control statement absent')
        source.write_text(original.replace(old, new))
        pin.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=digest(source.read_bytes()))
        reject(name, lambda pin=pin: matcher.build(pin))
        matcher.build(profiles[index])
    if len(validate(report)) != len(accepted):
        raise ValueError('Track positive proof not restored after controls')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 828, 'actualOriginalAndCompiledReturns': 3876,
        'actualSeparateNestedReturns': 36968, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeCodeVariants': 'In-memory rejection controls only; accepted compiler objects/instructions/addends remain untouched'}
    destination = ROOT / 'evidence/verification/arm7-seq-public-controls-20261030.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
