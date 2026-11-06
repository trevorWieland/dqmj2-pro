import copy
import hashlib
import json
from pathlib import Path
import match_arm7_lane_card_frontier_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-lane-card-frontier2240-20261031.json'
GENERATOR_SHA = 'e46c52e8c3938d5bd55a13fda7415aad881c2e7d270212369cf6b97df47ffb24'
REFERENCE = {'kind': 'native-qualified-card-storage-prefix-migration-and-frontier', 'compilerInput': False}
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
    if report.get('matchedInitializedBytes') != 2240 or report.get('matchedInstructionBytes') != 2128 or report.get('generatedLiteralBytes') != 112:
        raise ValueError('Measured card-service code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns')!=7120 or report.get('actualResumedOuterSleepReturns')!=1144 or report.get('actualNonlocalContextTransfers')!=2288:
        raise ValueError('Owned normal returns and resumed outer/context counts differ')
    if report.get('actualSeparatelyObservedNestedReturns')!=sum(sum(row['oracle']['actualSeparatelyObservedNestedReturns'].values()) for row in report['matches']):
        raise ValueError('Separately observed normal helper return counts differ')
    if report.get('newCandidateBytes')!=988 or report.get('zeroCoverageMigrationBytes')!=1252:
        raise ValueError('New coverage versus byte-identical-body migration differs')
    if report.get('wholeModuleLinked') is not False or report.get('sourceReconstructionComplete') is not False:
        raise ValueError('Scheduler-counter scope overclaimed')
    if any(report.get(key) != 0 for key in ('ordinaryAssemblyOrBlobCredit', 'originalDataSourceCredit', 'calleeSourceCredit')):
        raise ValueError('Scheduler-counter scaffold/original data/callee credit overstated')
    if report.get('referenceProvenance') != REFERENCE:
        raise ValueError('Reference-only typed source provenance differs')
    profile = json.loads(matcher.PROFILE.read_text())
    if report.get('sharedInterface')!=profile['interfaceContract'] or report.get('unchangedCBodyHistory')!=profile['sourceBodyHistory']:
        raise ValueError('Shared complete interface/body-history contract differs')
    for row in profile['sourceBodyHistory']:
        verify_file(row['newSource'],row['unchangedSourceSha256'])
        verify_file(row['originalSource'],row['unchangedSourceSha256'])
        for item in row['originalHeaderClosure']+row['newHeaderClosure']:verify_file(item['path'],item['sha256'])
    rows = report.get('matches', [])
    if len(rows) != 13:
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
        count={0x03802624:100,0x0380272c:136,0x03802860:100,0x038028e4:124,0x03802924:124,0x03802974:124,0x03802b70:432,0x03802c28:432,0x03802d70:540,0x03802e0c:648,0x03802f04:288,0x03802ffc:512,0x038032b8:572}[int(row['address'],0)]
        if len(records)!=count or trace['records']!=count or any(any(not state['actualReturn'] for state in record['states']) if 'states' in record else not record['state'].get('actualReturn',record['state'].get('actualResumedOuterSleepReturn',False)) for record in records):
            raise ValueError('Current CARD vectors lost actual returns')
    scope=json.loads(verify_file('evidence/arm7/lane-card-callback-scope-20261031.json','762a389d613559fa4216031db86a72fda3fad9a327d443e33347efe6131f2258').read_text())
    role_product=scope['traceProduct']
    role_raw=gzip.decompress(verify_file(role_product['path'],role_product['sha256']).read_bytes())
    if digest(role_raw)!=role_product['rawSha256'] or len(role_raw)!=role_product['rawBytes']:
        raise ValueError('Current callback boundary witness differs')
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
        ('wrong-rom',('romSha256',),'0'*64),('wrong-processor',('processor',),'arm9'),
        ('whole-module-overclaim',('wholeModuleLinked',),True),('data-source-overclaim',('originalDataSourceCredit',),4),
        ('callee-source-overclaim',('calleeSourceCredit',),132),('missing-generator-closure',('generatorSources',),[]),
        ('missing-runtime-closure',('pinnedGeneratorAndRuntimeDependencies',),[]),
        ('native-compiler-input',('referenceProvenance','compilerInput'),True),
        ('inflated-owned-return-count',('actualNativeAndCompiledReturns',),4248),
        ('invented-helper-count',('actualSeparatelyObservedNestedReturns',),55401),
        ('wrong-source-mode',('matches',0,'mode'),'thumb'),
        ('absent-comparison',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('source-closure-mutation',('matches',0,'sourceSha256'),'0'*64),
        ('original-code-compiler-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('false-return',('matches',0,'oracle','verifiedReturn'),False),
        ('unsupported-return-credit',('matches',0,'oracle','unsupportedReturnCredit'),1),
        ('false-device-completion',('matches',3,'oracle','limitations'),['all busy waits complete']),
        ('missing-symbol-map',('nativeSymbols',),None),('invented-symbol-entries',('nativeSymbolEntries',),[]),
        ('invented-include',('matches',0,'sourceDependencies'),[]),
        ('hardware-overclaim',('matches',0,'oracle','hardwareExecutionCredit'),1),
        ('unverified-cpu-memory',('matches',0,'oracle','fullRegistersFlagsStackAndMemoryCompared'),False),
        ('missing-memory-model',('matches',3,'oracle','independentCompleteMappedMemoryModel'),False),
        ('invented-complete-helper-model',('matches',1,'oracle','independentCompleteMappedMemoryModel'),True),
        ('invented-caller-source',('matches',3,'oracle','actualOriginalTransferCallerSourceCredit'),132),
        ('wrong-direct-owned-count',('matches',3,'oracle','actualDirectOwnedEntryReturns'),248),
        ('lost-indirect-owned-return',('matches',4,'oracle','actualIndirectOwnedCallbackReturns'),0),
        ('lost-separate-caller-return',('matches',5,'oracle','separateOriginalTransferCallerReturns'),0),
        ('wrong-pointer-word-count',('matches',3,'sourceAbiContract','physicalArgumentWords'),0),
        ('wrong-pointer-width',('matches',5,'sourceAbiContract','argumentWidths'),16),
        ('wrong-shared-state-size',('sharedInterface','cardTransferBytes'),12),
        ('wrong-storage-flags-offset',('sharedInterface','cardCommonFlagsOffset'),248),
        ('claimed-total-original-object-size',('sharedInterface','originalTotalObjectExtentsClaimed'),True),
        ('worker-false-normal-return',('matches',12,'oracle','actualOriginalAndCompiledReturns'),1144),
        ('worker-invented-load-return',('matches',12,'oracle','ordinaryLoadContextReturns'),2),
        ('worker-inflated-request-domain',('matches',12,'oracle','compiledShiftRequestDomain'),[0,0xffffffff]),
        ('lost-actual-context-flow',('matches',12,'oracle','verifiedNonreturningContextFlow'),False),
        ('missing-C-body-history',('unchangedCBodyHistory',),[]),
        ('lost-row-shared-type',('matches',0,'sourceAbiContract','sharedCardTransferBytes'),12),
        ('missing-qualified-scope',('matches',3,'qualifiedCanonicalScope'),{}),
        ('wrong-denominator-delta',('matches',3,'realArm7Link','qualifiedCanonicalScope','additionalInitializedDenominatorBytes'),244),
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
    import crossreuse_utility_c
    from elftools.elf.elffile import ELFFile
    mutations=((0,'wrong-priority','state->priority=4;','state->priority=5;'),
        (1,'wrong-timeout','result=4','result=3'),(2,'wrong-control','0xa040','0xa041'),
        (3,'wrong-destination-step','state->destination++;','state->destination+=2;'),
        (4,'wrong-source-step','state->source++;','state->source+=2;'),
        (5,'wrong-mismatch','state->matched=0;','state->matched=2;'),
        (6,'wrong-command2','address,2)','address,3)'),
        (7,'wrong-command10','address,10)','address,11)'),
        (8,'wrong-alignment-result','result=2','result=3'),
        (9,'wrong-command20','address,0x20)','address,0x21)'),
        (10,'wrong-payload-header','command[0]=1;','command[0]=2;'),
        (11,'wrong-task-clear','~0x4c','~0x48'),
        (12,'wrong-worker-result','prefix.result=3','prefix.result=2'))
    def check_bad(address,bad,index):
        if index==0:
            native=matcher.fixture.initialization.fixture
            result=native.execute(native.setup(address,bad,dict(flag=0,console=2,passes=1),1))
            if not result['states'][0]['actualReturn']:raise ValueError('Wrong initializer did not return')
        elif index in (3,4,5):
            result=matcher.fixture.callbacks.fixture.execute(address,bad,dict(count=2,flag=0x80000000,source=1,response=0),0)
            if not result['actualReturn']:raise ValueError('Wrong callback did not return')
        elif index>=9:
            native=matcher.fixture.worker if index==12 else matcher.fixture.completion if index==11 else matcher.fixture.commands
            if index==9:case=dict(size=1,address=0,length=1,width=3,result=0)
            elif index==10:case=dict(value=0x12345678,result=0,statuses=[0])
            elif index==11:case=dict(flags=4,callback=0,result=0xffffffff,count=0,source=0)
            else:case=dict(request=4,allowed=True,length=0,task=False)
            result=native.execute(address,bad,case,0)
            if not result.get('actualReturn',result.get('actualResumedOuterSleepReturn',False)):raise ValueError('Wrong frontier source failed termination')
        else:
            if index==1:case=dict(minimum=0,maximum=1,statuses=[1],passes=1)
            elif index==2:case=dict(count=1,length=1,callback=0x03802924,passes=1)
            elif index==8:case=dict(size=4,address=1,length=4,width=3,result=0,statuses=[0],passes=1)
            else:case=dict(size=4,address=0,length=5,width=3,result=0,passes=1)
            native=matcher.fixture.pages.fixture if index in (6,7) else matcher.fixture.service.fixture
            if not native.execute(address,bad,case,1)['actualReturn']:raise ValueError('Wrong ordinary caller did not return')
    for index,name,old,new in mutations:
        pin=pins[index];text=path(pin['source']).read_text();changed_text=text.replace(old,new)
        if changed_text==text:raise ValueError('Required shared-family negative token absent')
        import shutil
        directory=matcher.WORK/'controls'/name;unit=directory/'src'
        if unit.exists():
            source=unit/path(pin['source']).relative_to(matcher.ABI_ROOT)
            source.write_bytes(path(pin['source']).read_bytes())
        else:shutil.copytree(matcher.ABI_ROOT,unit)
        source=unit/path(pin['source']).relative_to(matcher.ABI_ROOT);source.write_text(changed_text,encoding='utf-8')
        dependencies=[]
        for item in pin['sourceDependencies']:
            current=unit/path(item['path']).relative_to(matcher.ABI_ROOT)
            dependencies.append(dict(path=current.relative_to(ROOT).as_posix(),sha256=digest(current.read_bytes())))
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=digest(source.read_bytes()),sourceDependencies=dependencies)
        attempt,compiled=crossreuse_utility_c.compile_origin(changed,path(pin['compiler']),pin['compilerFlags'],directory)
        if compiled is None:raise ValueError('Negative source failed before meaningful link: '+str(attempt))
        derived,masks,body=compiled
        if len(body)!=pin['bytes']:raise ValueError('Negative source is not same-size')
        with path(derived['probeObject']).open('rb') as stream:
            elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==pin['name'])
            section,offset=symbol['st_shndx'],symbol['st_value']
        entry=dict(changed,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
            relocations=[dict(r,format='SHT_RELA',explicitAddend=r['addend'],originalEncodedWord=body[r['offset']:r['offset']+4].hex()) for r in derived['relocations']])
        reject('actual-compiler-and-qualified-link-rejects-'+name,lambda entry=entry,directory=directory:matcher.qualified.validate(entry,directory/'real-link'))
        bad=(directory/'real-link/caller.bin').read_bytes()
        if len(bad)!=pin['bytes'] or digest(bad)==pin['targetSha256']:raise ValueError('Runtime negative did not use actual changed linked C')
        reject('actually-executed-linked-C-model-rejects-'+name,lambda address=int(pin['address'],0),bad=bad,index=index:check_bad(address,bad,index))
    if matcher.qualified.linker.namespace is not matcher.qualified.BASE_NAMESPACE:raise ValueError('Qualified namespace override leaked')
    for pin in pins:
        matcher.build(pin)
    identities={('arm7','','arm7-wram',pin['address'],'arm') for pin in pins}
    if set(validate(report))!=identities:
        raise ValueError('Qualified utility-child transfer identities differ')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 2240, 'newCandidateBytes':988,'zeroCoverageMigrationBytes':1252,'actualOriginalAndCompiledReturns': 7120,
        'actualSeparateNestedReturns':report['actualSeparatelyObservedNestedReturns'], 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeSourceVariants': 'Thirteen actual same-size wrong C bodies genuinely compiled/qualified-linked then independently executed and rejected; shared-size/offset/body-history/current-product controls'}
    destination = ROOT / 'evidence/verification/arm7-lane-card-frontier2240-controls-20261031.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
