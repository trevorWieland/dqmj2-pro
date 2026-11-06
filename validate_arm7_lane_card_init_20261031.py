import copy
import hashlib
import json
from pathlib import Path
import match_arm7_lane_card_init_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-lane-card-init188-20261031.json'
GENERATOR_SHA = '4b799d8d5a694ae6ced8dbe012ae75e9067c85399a4a56c2324d9bbc32bd72ab'
REFERENCE = {'kind': 'native-card-common-layout-and-reference-qualifiers', 'compilerInput': False}
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
        raise ValueError('Current card-service input/product changed or missing: ' + name)
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
        raise ValueError('Frozen card-service matcher identity differs')
    verify_file(report['generator'], GENERATOR_SHA)
    verify_file(matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PROFILE_SHA)
    verify_file(matcher.PIN_FILE.relative_to(ROOT).as_posix(), matcher.PIN_SHA)
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    required = {report['generator'], matcher.PROFILE.relative_to(ROOT).as_posix(), matcher.PIN_FILE.relative_to(ROOT).as_posix()} | {item['path'] for item in pins}
    if len(report.get('generatorSources', [])) != len(required) or {row['path'] for row in report['generatorSources']} != required:
        raise ValueError('Complete card-service generator closure differs')
    for item in report['generatorSources']:
        verify_file(item['path'], item['sha256'])
    pins = json.loads(matcher.PIN_FILE.read_text())['files']
    if report.get('pinnedGeneratorAndRuntimeDependencies') != pins:
        raise ValueError('Published frozen card-service dependency closure differs')
    for item in pins:
        verify_file(item['path'], item['sha256'])
    verify_file('inputs/game.nds', matcher.ROM)
    if report.get('romSha256') != matcher.ROM or report.get('processor') != 'arm7' or report.get('program') != '' or report.get('module') != 'arm7-wram':
        raise ValueError('Scheduler-counter qualified ROM/processor/module identity differs')
    if report.get('matchedInitializedBytes') != 188 or report.get('matchedInstructionBytes') != 164 or report.get('generatedLiteralBytes') != 24:
        raise ValueError('Measured card-service code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns') != 200 or report.get('actualSeparatelyObservedNestedReturns') != 2800 or report.get('providerFreeOriginalAndCompiledReturns') != 200 or report.get('syntheticBiosContractOriginalAndCompiledReturns') != 0 or report.get('independentlyCheckedSigned64Returns') != 0 or report.get('originalBiosExecutionCredit') != 0:
        raise ValueError('Actual outer versus nested card-service return counts differ')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Scheduler-counter scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Scheduler-counter scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    profile = json.loads(matcher.PROFILE.read_text())
    rows = report.get('matches', [])
    if len(rows) != 1:
        raise ValueError('Scheduler-counter qualified source unit missing or duplicated')
    for pin, row in zip(profile['matches'], rows):
        if any(row.get(key) != value for key, value in pin.items()):
            raise ValueError('Frozen typed card-service source/profile differs')
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
        trace=row['oracle']['traceProduct']
        data=verify_file(trace['path'],trace['compressedSha256']).read_bytes()
        raw=gzip.decompress(data)
        if len(data)!=trace['compressedBytes'] or len(raw)!=trace['rawBytes'] or digest(raw)!=trace['rawSha256'] or data[4:8]!=bytes(4):
            raise ValueError('Current sound initialization trace differs')
        records=json.loads(raw)
        count=100
        if len(records)!=count or trace['records']!=count or any(len(record['states'])!=1 or not record['states'][0]['actualReturn'] for record in records):
            raise ValueError('Current CARD vectors lost actual returns')
    symbols, entries = derived_bindings(rows)
    if report.get('nativeSymbols') != symbols or report.get('nativeSymbolEntries') != entries:
        raise ValueError('Published typed-card-service function/data map differs from qualified real-link bindings/native addends')
    cache_key = digest(json.dumps(report['generatorSources'], sort_keys=True).encode())
    if cache_key not in _FRESH:
        _FRESH[cache_key] = dict(rows=json.loads(json.dumps([matcher.build(pin) for pin in profile['matches']])))
    if rows != _FRESH[cache_key]['rows']:
        raise ValueError('Published card-service source/link/boundary/native records differ from full fresh proof')
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
            raise ValueError('Invalid card-service proof accepted: ' + name)
    changes = (
        ('wrong-rom',('romSha256',),'0'*64),
        ('wrong-processor',('processor',),'arm9'),
        ('whole-module-overclaim',('wholeModuleLinked',),True),
        ('data-source-overclaim',('originalDataSourceCredit',),4),
        ('callee-source-overclaim',('calleeSourceCredit',),244),
        ('missing-generator-closure',('generatorSources',),[]),
        ('missing-runtime-closure',('pinnedGeneratorAndRuntimeDependencies',),[]),
        ('native-compiler-input',('referenceProvenance','compilerInput'),True),
        ('inflated-entry-count',('actualNativeAndCompiledReturns',),1554),
        ('inflated-helper-count',('actualSeparatelyObservedNestedReturns',),17465),
        ('wrong-source-mode',('matches',0,'mode'),'thumb'),
        ('absent-comparison',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('source-closure-mutation',('matches',0,'sourceSha256'),'0'*64),
        ('original-code-compiler-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('false-return',('matches',0,'oracle','verifiedReturn'),False),
        ('unsupported-return-credit',('matches',0,'oracle','unsupportedReturnCredit'),1),
        ('false-global-state',('matches',0,'oracle','limitations'),['all game state initialized']),
        ('missing-native-symbol-map',('nativeSymbols',),None),
        ('wrong-native-symbol-entries',('nativeSymbolEntries',),[]),
        ('invented-addend',('nativeSymbolEntries',),[{'unchangedExplicitAddend':4}]),
        ('invented-include',('matches',0,'sourceDependencies'),[]),
        ('physical-hardware-overclaim',('matches',0,'oracle','hardwareExecutionCredit'),1),
        ('unverified-cpu-memory',('matches',0,'oracle','fullRegistersFlagsStackAndMemoryCompared'),False),
        
        ('lost-transfer-memory-model',('matches',0,'oracle','independentCompleteMappedMemoryModel'),False),
        ('lost-own-state-model',('matches',0,'oracle','independentSixWordThreadAndCallbackFlagModel'),False),
        ('invented-task-execution',('matches',0,'oracle','taskThreadExecutions'),1),
        ('invented-context-execution',('matches',0,'oracle','contextSwitchExecutions'),1),
        ('invented-formal-arg-count',('matches',0,'sourceAbiContract','physicalArgumentWords'),3),
        ('invented-word-width',('matches',0,'sourceAbiContract','argumentWidths'),16),
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
    pins = json.loads(matcher.PROFILE.read_text())['matches']
    trace=path(report['matches'][0]['oracle']['traceProduct']['path'])
    backup=trace.read_bytes()
    try:
        trace.unlink()
        reject('missing-current-trace-after-cache',lambda:validate(report))
        trace.write_bytes(bytes([backup[0]^1])+backup[1:])
        reject('changed-current-trace-after-cache',lambda:validate(report))
    finally:
        trace.write_bytes(backup)
    native=matcher.fixture.fixture
    def require_return(value):
        if not value['states'][0]['actualReturn']:raise ValueError('Bounded card initializer did not actually return')
    mutations=(('wrong-owner','state->owner=-3;','state->owner=-4;'),
        ('wrong-priority','state->priority=4;','state->priority=5;'),
        ('wrong-stack-size','1024,state->priority','512,state->priority'),
        ('wrong-callback-tag','037fe39c(11,','037fe39c(10,'),
        ('inverted-console-gate','if(CardIsChild())','if(!CardIsChild())'),
        ('invented-formal-input','03802624(void)','03802624(u32 argument)'))
    pin=pins[0]
    for name,old,new in mutations:
        original=path(pin['source']).read_text();changed_text=original.replace(old,new)
        if changed_text==original:raise ValueError('Required card-init negative token absent')
        directory=matcher.WORK/'controls'/name;directory.mkdir(parents=True,exist_ok=True)
        source=directory/path(pin['source']).name;source.write_text(changed_text,encoding='utf-8')
        dependencies=[]
        for include in pin['sourceDependencies']:
            target=directory/path(include['path']).name;target.write_bytes(path(include['path']).read_bytes())
            dependencies.append(dict(path=target.relative_to(ROOT).as_posix(),sha256=digest(target.read_bytes())))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()),sourceDependencies=dependencies)
        reject(('source-ABI-rejects-' if name=='invented-formal-input' else 'actual-compiler-link-rejects-')+name,lambda changed=changed:matcher.build(changed))
        if name in ('wrong-owner','wrong-priority','wrong-callback-tag','inverted-console-gate'):
            bad=(matcher.WORK/pin['address'][2:]/'real-link/caller.bin').read_bytes()
            if len(bad)!=188:raise ValueError('Negative initializer C is not measured same-size')
            case=dict(flag=0,console=2,passes=1)
            reject('actually-executed-linked-C-model-rejects-'+name,
                lambda bad=bad:require_return(native.execute(native.setup(native.ADDRESS,bad,case,1))))
    body=path(pin['binary']).read_bytes()[native.ADDRESS-native.BASE:native.ADDRESS-native.BASE+native.SIZE]
    reject('cap-is-not-return',lambda:require_return(native.execute(native.setup(native.ADDRESS,body,native.cases(native.ADDRESS)[0],91),1)))
    for pin in pins:
        matcher.build(pin)
    identities={('arm7','','arm7-wram',pin['address'],'arm') for pin in pins}
    if set(validate(report))!=identities:
        raise ValueError('Qualified utility-child transfer identities differ')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 188, 'actualOriginalAndCompiledReturns': 200,
        'actualSeparateNestedReturns': 2800, 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeSourceVariants': 'Five compiler/link owner/priority/stack/tag/console variants, one no-formal-input ABI guard and four actual same-size linked-C memory/model rejections'}
    destination = ROOT / 'evidence/verification/arm7-lane-card-init188-controls-20261031.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
