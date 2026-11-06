import copy
import hashlib
import json
from pathlib import Path
import match_arm7_lane_card_control_20261031 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent
REPORT = ROOT / 'evidence/matches/arm7-lane-card-control452-20261031.json'
GENERATOR_SHA = '7e5ff4cc93fc80a4ae7c306a5c5a655d79710cbef482a39e6b4776792c59408d'
REFERENCE = {'kind': 'native-qualified-card-protocol-controls-and-word-interfaces', 'compilerInput': False}
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
    if report.get('matchedInitializedBytes') != 452 or report.get('matchedInstructionBytes') != 436 or report.get('generatedLiteralBytes') != 16:
        raise ValueError('Measured card-service code/literal coverage differs')
    if report.get('actualNativeAndCompiledReturns')!=6944 or report.get('actualResumedOuterSleepReturns')!=0 or report.get('actualNonlocalContextTransfers')!=0:
        raise ValueError('Owned normal returns and resumed outer/context counts differ')
    if report.get('actualSeparatelyObservedNestedReturns')!=sum(sum(row['oracle']['actualSeparatelyObservedNestedReturns'].values()) for row in report['matches']):
        raise ValueError('Separately observed normal helper return counts differ')
    if report.get('newCandidateBytes')!=452 or report.get('zeroCoverageMigrationBytes')!=0:
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
    if len(rows) != 4:
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
        count={0x03802824:128,0x03803094:80,0x03803114:576,0x038031d4:2688}[int(row['address'],0)]
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


def link_negative(entry, positive, directory):
    import os
    import shutil
    import subprocess
    from elftools.elf.elffile import ELFFile
    directory=directory.resolve();directory.relative_to(matcher.WORK.resolve());directory.mkdir(parents=True,exist_ok=True)
    proof=positive['realArm7Link'];old=path(proof['cwd'])
    if {r['symbol'] for r in entry['relocations']}!={r['symbol'] for r in positive['relocations']}:
        raise ValueError('Negative source changed qualified dependency identities')
    original=verify_file(entry['object'],entry['objectSha256']);caller=directory/'caller.o'
    with original.open('rb') as stream:matcher.linker.split_symbol(ELFFile(stream),entry['name'],caller)
    if matcher.linker.relocation_rows(original,entry['name'])!=matcher.linker.relocation_rows(caller,entry['name']):
        raise ValueError('Negative source split altered relocation/addend/instruction')
    for anchor in proof['zeroCodeAnchors']:
        current=verify_file(anchor['object'],anchor['objectSha256'])
        shutil.copyfile(current,directory/current.name)
    lcf=verify_file(proof['lcf'],proof['lcfSha256']);shutil.copyfile(lcf,directory/lcf.name)
    command=[str(directory/Path(value).name) if Path(value).is_absolute() and Path(value).parent==old else str(path(value)) if index==0 else value for index,value in enumerate(proof['linkCommand'])]
    result=subprocess.run(command,cwd=directory,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError('Actual negative-source link failed: '+result.stdout+result.stderr)
    linked=(directory/'caller.bin').read_bytes()
    return linked,dict(command=command,cwd=str(directory),sourceSha256=entry['sourceSha256'],objectSha256=entry['objectSha256'],
        linkedSha256=digest(linked),linkedElfSha256=digest((directory/'linked.elf').read_bytes()),lcfSha256=digest((directory/lcf.name).read_bytes()),
        bindingSource='Independently current-source/native-qualified positive LCF and unchanged zero-code anchors',sourceCredit=0)


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
    changes=(
        ('wrong-rom',('romSha256',),'0'*64),('wrong-processor',('processor',),'arm9'),
        ('whole-module-overclaim',('wholeModuleLinked',),True),('data-source-overclaim',('originalDataSourceCredit',),4),
        ('callee-source-overclaim',('calleeSourceCredit',),80),('missing-generator-closure',('generatorSources',),[]),
        ('missing-runtime-closure',('pinnedGeneratorAndRuntimeDependencies',),[]),('native-compiler-input',('referenceProvenance','compilerInput'),True),
        ('inflated-owned-count',('actualNativeAndCompiledReturns',),7000),('invented-helper-count',('actualSeparatelyObservedNestedReturns',),1),
        ('invented-context-transfer',('actualNonlocalContextTransfers',),2),('false-migration-credit',('zeroCoverageMigrationBytes',),108),
        ('wrong-mode',('matches',0,'mode'),'thumb'),('absent-comparison',('matches',0,'exactAfterDeclaredRelocation'),False),
        ('wrong-source',('matches',0,'sourceSha256'),'0'*64),('original-compiler-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('false-return',('matches',0,'oracle','verifiedReturn'),False),('unsupported-credit',('matches',0,'oracle','unsupportedReturnCredit'),1),
        ('missing-symbol-map',('nativeSymbols',),None),('invented-symbol-map',('nativeSymbolEntries',),[]),
        ('missing-include-closure',('matches',0,'sourceDependencies'),[]),('hardware-overclaim',('matches',1,'oracle','hardwareExecutionCredit'),1),
        ('missing-cpu-memory-comparison',('matches',3,'oracle','fullRegistersFlagsStackAndMemoryCompared'),False),
        ('missing-independent-task-memory-model',('matches',2,'oracle','independentCompleteMappedMemoryModel'),False),
        ('invented-receiver-complete-helper-model',('matches',3,'oracle','independentCompleteMappedMemoryModel'),True),
        ('wrong-zero-arg-ABI',('matches',1,'sourceAbiContract','physicalArgumentWords'),1),
        ('narrowed-full-return-contract',('matches',1,'sourceAbiContract','return'),'u8'),
        ('wrong-pointer-width',('matches',2,'sourceAbiContract','argumentWidths'),16),
        ('wrong-tag-data-enabled-count',('matches',3,'sourceAbiContract','physicalArgumentWords'),2),
        ('wrong-storage-view-size',('sharedInterface','cardCommonStorageViewBytes'),252),
        ('false-original-object-extent',('sharedInterface','originalTotalObjectExtentsClaimed'),True),
        ('wrong-profiled-return-contract',('matches',0,'sourceAbiContract','return'),'void'),
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
    mutations=((0,'cached-argument-before-wait','    native_host_arm7_fn_0380272c(0,50);\n    CardArgument *argument=CARD_COMMON.argument;',
        '    CardArgument *argument=CARD_COMMON.argument;\n    native_host_arm7_fn_0380272c(0,50);'),
        (1,'wrong-control-mask','~0x1fff','~0xfff'),(2,'wrong-busy-bit','flags|=4','flags|=8'),
        (3,'wrong-phase-increment','CardReadPhase(state)+1','CardReadPhase(state)+2'))
    def check_bad(address,bad,index):
        fixture=matcher.fixture.receiver if index==3 else matcher.fixture.normal
        if index==0:case=dict(old=0,new=4,swap=True)
        elif index==1:case=dict(control=0x00801fff,received=0xdeadbeef)
        elif index==2:case=dict(flags=0,callback=0,argument=0)
        else:case=dict(tag=11,enabled=1,phase=0,request=0,data=16,flags=0,other=False)
        if not fixture.execute(address,bad,case,0)['actualReturn']:raise ValueError('Wrong C did not actually return')
    negative_links=[]
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
        bad,negative_proof=link_negative(entry,report['matches'][index],directory/'negative-runtime-link')
        negative_links.append(dict(name=name,**negative_proof))
        if len(bad)!=pin['bytes'] or digest(bad)==pin['targetSha256']:raise ValueError('Runtime negative did not use actual changed linked C')
        reject('actually-executed-linked-C-model-rejects-'+name,lambda address=int(pin['address'],0),bad=bad,index=index:check_bad(address,bad,index))
    if matcher.qualified.linker.namespace is not matcher.qualified.BASE_NAMESPACE:raise ValueError('Qualified namespace override leaked')
    identities={('arm7','','arm7-wram',pin['address'],'arm') for pin in pins}
    if set(validate(report))!=identities:
        raise ValueError('Qualified utility-child transfer identities differ')
    result = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'report': REPORT.relative_to(ROOT).as_posix(), 'reportSha256': digest(REPORT.read_bytes()),
        'positiveUnits': len(accepted), 'matchedInitializedBytes': 452, 'newCandidateBytes':452,'zeroCoverageMigrationBytes':0,'actualOriginalAndCompiledReturns': 6944,
        'actualSeparateNestedReturns':report['actualSeparatelyObservedNestedReturns'], 'controls': controls, 'allPassed': all(row['rejected'] for row in controls),
        'negativeRuntimeLinks':negative_links,
        'negativeSourceVariants': 'Four actual same-size wrong C bodies genuinely compiled/qualified-linked then independently executed and rejected; shared-size/offset/body-history/current-product controls'}
    destination = ROOT / 'evidence/verification/arm7-lane-card-control452-controls-20261031.json'
    write_json(destination, result)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'controls': len(controls), 'allPassed': result['allPassed']}), flush=True)


if __name__ == '__main__':
    main()
