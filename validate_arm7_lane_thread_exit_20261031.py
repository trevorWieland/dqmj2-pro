import copy
import hashlib
import json
from pathlib import Path
import match_arm7_lane_thread_exit_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-lane-thread-exit160-20261031.json'
GENERATOR_SHA = '3d550ee18f8866e38ccf4cc5c146a5f9c2afd35a4ee1cfd1c146a963dd877ea2'
REFERENCE = {'kind': 'measured-sdk-thread-exit-context-and-one-argument-destructor-contract', 'compilerInput': False}
_FRESH = {}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def path(name):
    result = (ROOT / name).resolve()
    if not result.is_relative_to(ROOT):
        raise ValueError('Scheduler-counter input/product path escaped repository')
    return result


def verify_file(name, sha):
    current = path(name)
    if not current.is_file() or digest(current.read_bytes()) != sha:
        raise ValueError('Current thread-exit input/product changed or missing: ' + name)
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
        raise ValueError('Frozen thread-exit matcher identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PROFILE_SHA)
    verify_file(matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.PIN_SHA)
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {item['path'] for item in pins}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete thread-exit generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published frozen thread-exit dependency closure differs')
    for item in pins:
        verify_file(item['path'], item['sha256'])
    verify_file('inputs/game.nds', matcher.ROM)
    if report.get('romSha256') != matcher.ROM or report.get('processor') != 'arm7' or report.get('program') != '' or report.get('module') != 'arm7-wram':
        raise ValueError('Scheduler-counter qualified ROM/processor/module identity differs')
    if report.get('matchedInitializedBytes') != 160 or report.get('matchedInstructionBytes') != 148 or report.get('generatedLiteralBytes') != 12:
        raise ValueError('Measured thread-exit code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 0 or report.get('actualResumedOuterSleepReturns') != 256 or report.get('actualOwnedNormalReturns') != 0 or report.get('verifiedNonreturningExitTransition') is not True or report.get('actualSeparatelyObservedNestedReturns') != 256 or report.get('providerFreeOriginalAndCompiledReturns') != 0 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0 or report.get('independentlyCheckedSigned64Returns') != 0 or report.get('originalBiosExecutionCredit') != 0:
        raise ValueError('Actual outer versus nested thread-exit return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Scheduler-counter scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Scheduler-counter scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 2:
        raise ValueError('Scheduler-counter qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed thread-exit source/profile differs')
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
    import gzip
    for row in rows:
        oracle=row['oracle']
        if oracle['verifiedReturn'] is not False or oracle['verifiedNonreturningExitTransition'] is not True or oracle['actualOwnedNormalReturns']!=0 or oracle['actualResumedOuterSleepReturns']!=128:
            raise ValueError('Nonreturning own APIs and resumed outer SleepThread returns conflated')
        trace=oracle['traceProduct']
        data=verify_file(trace['path'],trace['compressedSha256']).read_bytes()
        raw=gzip.decompress(data)
        if len(data)!=trace['compressedBytes'] or len(raw)!=trace['rawBytes'] or digest(raw)!=trace['rawSha256'] or data[4:8]!=bytes(4):
            raise ValueError('Current deterministic exit trace product differs')
        records=json.loads(raw)
        if len(records)!=64 or trace['records']!=64 or any(not record['actualResumedOuterSleepReturn'] or record['actualOwnedNormalReturns']!=0 for record in records):
            raise ValueError('Current per-scenario exit proof lost actual resumed caller returns')
        probe=oracle['syntheticCallbackProof']
        if probe['physicalArgumentWords']!=1 or probe['codeBytes']!=24 or probe['bytes']!=28 or any(probe[key]!=0 for key in ('sourceCredit','originalCalleeCredit')):
            raise ValueError('Synthetic destructor callback ABI or zero credit differs')
        verify_file(probe['source'],probe['sourceSha256'])
        verify_file(probe['object'],probe['objectSha256'])
        directory=Path(probe['linkCommand'][-1]).parent
        verify_file(str(directory/'probe.lcf'),probe['lcfSha256'])
        verify_file(str(directory/'probe.elf'),probe['linkedElfSha256'])
        verify_file(str(directory/'probe.bin'),probe['linkedBodySha256'])
    symbols, entries = derived_bindings(rows)
    if report.get('nativeSymbols') != symbols or report.get('nativeSymbolEntries') != entries:
        raise ValueError('Published typed-thread-exit function/data map differs from qualified real-link bindings/native addends')
    cache_key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if cache_key not in _FRESH:
        _FRESH[cache_key] = dict(rows=json.loads(json.dumps([matcher.build(pin) for pin in profile['matches']])))
    if rows != _FRESH[cache_key]['rows']:
        raise ValueError('Published thread-exit source/link/boundary/native records differ from full fresh proof')
    return {(row['processor'], row.get('program',''), row['module'], row['address'], row['mode']): row for row in rows}


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
            raise ValueError('Invalid thread-exit proof accepted: ' + name)
    changes = (
        ('wrong-rom', ('romSha256',), '0' * 64),
        ('wrong-namespace', ('processor',), 'arm9'),
        ('whole-module-overclaim', ('wholeModuleLinked',), True),
        ('data-source-overclaim', ('originalDataSourceCredit',), 8),
        ('callee-source-overclaim', ('calleeSourceCredit',), 156),
        ('missing-generator-closure', ('generatorSources',), []),
        ('missing-runtime-closure', ('pinnedGeneratorAndRuntimeDependencies',), []),
        ('native-measurement-compiler-input', ('referenceProvenance', 'compilerInput'), True),
        ('inflated-entry-count', ('actualNativeAndCompiledReturns',), 1032),
        ('wrong-source-mode', ('matches', 0, 'mode'), 'thumb'),
        ('absent-link-comparison-flag', ('matches', 0, 'exactAfterDeclaredRelocation'), False),
        ('source-closure-mutation', ('matches', 0, 'sourceSha256'), '0' * 64),
        ('original-code-compiler-input', ('matches', 0, 'sourceOnlyCompilerInput', 'originalCodeCompilerInput'), True),
        ('invented-owned-normal-return', ('matches', 0, 'oracle', 'verifiedReturn'), True),
        ('unsupported-return-credit', ('matches', 0, 'oracle', 'unsupportedReturnCredit'), 1),
        ('replaced-native-list-helpers', ('matches', 0, 'oracle', 'providerReplacements'), ['replacement']),
        ('invented-mute-r0-result', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'meaningful u32 result'),
        ('invented-result-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'returns number of active records'),
        ('false-complete-game-state', ('matches', 0, 'oracle', 'limitations'), ['all save/game state initialized']),
        ('missing-native-symbol-map', ('nativeSymbols',), None),
        ('invented-native-symbol-entries', ('nativeSymbolEntries',), [{'mode': 'thumb'}]),
        ('invented-source-addend', ('matches', 0, 'realArm7Link', 'unchangedRelocations'), [{'explicitAddend': 4}]),
        ('invented-published-addend', ('nativeSymbolEntries',), [{'unchangedExplicitAddend': 4}]),
        ('invented-declared-include', ('matches', 0, 'sourceDependencies'), [{'path':'invented.h','sha256':'0'*64}]),
        ('physical-hardware-overclaim', ('matches', 0, 'oracle', 'hardwareExecutionCredit'), 1),
        ('unverified-full-state', ('matches', 0, 'oracle', 'fullRegistersFlagsStackAndMemoryCompared'), False),
        ('narrow-word-return-contract', ('matches', 0, 'oracle', 'meaningfulReturnContract'), 'u8 attenuation'),
        ('lost-nonreturning-exit-proof', ('matches', 0, 'oracle', 'verifiedNonreturningExitTransition'), False),
        ('owned-return-inflation', ('matches', 0, 'oracle', 'actualOwnedNormalReturns'), 128),
        ('lost-real-sleep-continuation', ('matches', 0, 'oracle', 'actualResumedOuterSleepReturns'), 0),
        ('lost-context-abi-model', ('matches', 0, 'oracle', 'independentContextAbiAndAllMemoryOutsideDeclaredExecutionStacks'), False),
        ('lost-reachable-own-coverage', ('matches', 0, 'oracle', 'allReachableOwnInstructionAddressesVisited'), []),
        ('missing-compiler-nonreturn-exclusions', ('matches', 0, 'oracle', 'excludedOriginalNonreturnContinuations'), []),
        ('wrong-callback-arity', ('matches', 1, 'oracle', 'syntheticCallbackProof', 'physicalArgumentWords'), 2),
        ('invented-OS-Terminate-exit', ('matches', 1, 'oracle', 'originalTerminationFallbackCredit'), 1),
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
    products=[report['matches'][0]['oracle']['traceProduct']['path'],
        str(Path(report['matches'][0]['oracle']['syntheticCallbackProof']['linkCommand'][-1]).parent/'probe.bin')]
    for index,name in enumerate(products):
        target=path(name)
        backup=target.read_bytes()
        try:
            target.unlink()
            reject('missing-current-exit-product-after-cache-'+str(index),lambda:validate(report))
            target.write_bytes(bytes([backup[0]^1])+backup[1:])
            reject('changed-current-exit-product-after-cache-'+str(index),lambda:validate(report))
        finally:
            target.write_bytes(backup)
    native=matcher.fixture.fixture
    def require_exit(value):
        if not value['actualResumedOuterSleepReturn']:
            raise ValueError('Bounded exit has no actual resumed SleepThread caller return: '+str(value))
    pins = json.loads(matcher.PROFILE.read_text())['matches']
    mutations=((0,'wrong-context-irq-mask','|= HW_PSR_DISABLE_IRQ','|= 0x40'),
        (0,'wrong-context-ready-state','OS_THREAD_STATE_READY','OS_THREAD_STATE_TERMINATED'),
        (0,'lost-destructor-argument','thread->context.r[0] = (u32)arg;','thread->context.r[0] = 1;'),
        (1,'wrong-destructor-clear','currentThread->destructor = NULL;','currentThread->destructor = (OSThreadDestructor)1;'),
        (1,'skipped-destruction','OSi_ExitThread_Destroy();','return;'),
        (1,'wrong-destructor-argument','destructor(arg);','destructor((void *)1);'))
    for index,name,old,new in mutations:
        pin=pins[index]
        original=path(pin['source']).read_text()
        changed_text=original.replace(old,new)
        if changed_text==original:
            raise ValueError('Expected thread-exit source mutation absent')
        directory=matcher.WORK/'controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/path(pin['source']).name
        source.write_text(changed_text)
        dependencies=[]
        for include in pin['sourceDependencies']:
            target=directory/path(include['path']).name
            target.write_bytes(path(include['path']).read_bytes())
            dependencies.append(dict(path=target.relative_to(ROOT).as_posix(),sha256=digest(target.read_bytes())))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()),sourceDependencies=dependencies)
        reject('actual-compiler-link-rejects-'+name,lambda changed=changed:matcher.build(changed))
        if name in ('wrong-context-irq-mask','wrong-context-ready-state','wrong-destructor-clear'):
            body=(matcher.WORK/pin['address'][2:]/'real-link/caller.bin').read_bytes()
            if len(body)!=pin['bytes']:
                raise ValueError('Expected same-size negative C link extent differs')
            from build_arm7_lane_thread_exit_callback_20261031 import build as build_probe
            probe=build_probe()
            reject('actually-executed-linked-C-model-rejects-'+name,
                lambda body=body,address=int(pin['address'],0):require_exit(native.execute(address,body,1,True,callback_probe=probe)))

    for pin in pins:
        address=int(pin['address'],0)
        raw=path(pin['binary']).read_bytes()
        body=raw[address-native.BASE:address-native.BASE+native.SIZES[address]]
        reject('exit-exhaustion-is-not-resumed-return-'+pin['address'],
            lambda address=address,body=body:require_exit(native.execute(address,body,91,budget=1)))
    from build_arm7_lane_thread_exit_callback_20261031 import build as build_probe
    wrong=build_probe('wrong-count')
    last=pins[1]
    address=int(last['address'],0)
    raw=path(last['binary']).read_bytes()
    body=raw[address-native.BASE:address-native.BASE+native.SIZES[address]]
    reject('actually-executed-wrong-synthetic-callback-effect',lambda:native.execute(address,body,1,True,callback_probe=wrong))
    for pin in pins:
        matcher.build(pin)
    identities={('arm7','','arm7-wram',pin['address'],'arm') for pin in pins}
    if set(validate(report))!=identities:
        raise ValueError('Qualified utility-child transfer identities differ')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 160, 'actualOriginalAndCompiledReturns': 0, 'actualOwnedNormalReturns': 0,
        'actualResumedOuterSleepReturns': 256, 'actualSeparateNestedReturns': 256, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeSourceVariants': 'Six freshly compiled exit-context/state/argument/destructor mutations plus an actually executed wrong synthetic callback count'}
    destination = ROOT / 'evidence/verification/arm7-lane-thread-exit160-controls-20261031.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
