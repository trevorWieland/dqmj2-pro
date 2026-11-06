import copy
import gzip
import json
from pathlib import Path
import match_arm7_lane_card_priority_20261031 as matcher
from project import ROOT,sha256,write_json
REPORT=ROOT/'evidence/matches/arm7-lane-card-priority64-20261031.json'
GENERATOR_SHA='0864c12a49e97a11b2b7f472ecc5338438d6c6e2bd9780b761eb527aebc20d68'
INVENTORY_SHA='315dd84918b3f29e87e3fa52dec838b399b28dd2adb286d9c27ac2247624ecd6'
_FRESH={}


def verify(name,pin):
    path=(ROOT/name).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file() or sha256(path)!=pin:raise ValueError('Current priority source/runtime/product differs: '+str(name))
    return path


def bindings(rows):
    symbols,entries={},[]
    for row in rows:
        raw=verify(row['binary'],row['inputModuleSha256']).read_bytes();first=int(row['address'],0)-row['base']
        for rel in row['relocations']:
            binding=row['realArm7Link']['bindings'][rel['symbol']];symbols[rel['symbol']]=binding['address']
            entries.append(dict(binding,symbol=rel['symbol'],sourceRelocationOffset=rel['offset'],sourceRelocationType=rel['type'],
                unchangedExplicitAddend=rel['explicitAddend'],nativeEncodedWord=hex(int.from_bytes(raw[first+rel['offset']:first+rel['offset']+4],'little')),sourceCredit=0,
                callerIdentity={key:row[key] for key in ('program','processor','module','address','mode')}))
    return symbols,entries


def validate(report):
    verify('evidence/arm7/ghidra-runtime-inventory.json',INVENTORY_SHA)
    verify('inputs/game.nds',matcher.ROM);verify(matcher.PROFILE,matcher.PROFILE_SHA);verify(matcher.PIN_FILE,matcher.PIN_SHA)
    verify(Path(matcher.__file__).name,GENERATOR_SHA)
    if report['generator']!=Path(matcher.__file__).name or report['generatorSha256']!=GENERATOR_SHA:raise ValueError('Frozen priority generator differs')
    pins=json.loads(matcher.PIN_FILE.read_text())['files'];profile=json.loads(matcher.PROFILE.read_text())
    required={Path(matcher.__file__).name,matcher.PROFILE.relative_to(ROOT).as_posix(),matcher.PIN_FILE.relative_to(ROOT).as_posix()}|{p['path'] for p in pins}
    if len(report['generatorSources'])!=len(required) or {p['path'] for p in report['generatorSources']}!=required:raise ValueError('Complete priority generator closure differs')
    for pin in report['generatorSources']:verify(pin['path'],pin['sha256'])
    if report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Published runtime pins differ')
    if (report['romSha256'],report['processor'],report['program'],report['module'])!=(matcher.ROM,'arm7','','arm7-wram'):raise ValueError('Qualified priority identity differs')
    if (report['matchedInitializedBytes'],report['matchedInstructionBytes'],report['generatedLiteralBytes'])!=(64,60,4):raise ValueError('Complete priority bytes differ')
    if (report['actualNativeAndCompiledReturns'],report['actualSeparatelyObservedNestedReturns'],report['actualResumedOuterSleepReturns'],report['actualNonlocalContextTransfers'])!=(240,1632,0,0):raise ValueError('Owned/helper/context return scopes differ')
    if report['newCandidateBytes']!=64 or report['zeroCoverageMigrationBytes']!=0:raise ValueError('Priority added-byte scope differs')
    if report['wholeModuleLinked'] is not False or report['sourceReconstructionComplete'] is not False:raise ValueError('Priority module/completion overclaim')
    if any(report.get(key)!=0 for key in ('ordinaryAssemblyOrBlobCredit','originalDataSourceCredit','calleeSourceCredit','originalBiosExecutionCredit')):raise ValueError('Priority scaffold or BIOS credit overclaim')
    if report['referenceProvenance']!={'kind':'native-qualified-card-thread-priority-and-word-interface','compilerInput':False}:raise ValueError('Priority provenance differs')
    if report['sharedInterface']!=profile['interfaceContract'] or report['unchangedCBodyHistory']!=[]:raise ValueError('Shared storage declaration differs')
    if len(report['matches'])!=1:raise ValueError('Priority unit absent/duplicated')
    for pin,row in zip(profile['matches'],report['matches']):
        if any(row.get(key)!=value for key,value in pin.items()):raise ValueError('Frozen priority source/profile differs')
        verify(pin['source'],pin['sourceSha256'])
        for item in pin['sourceDependencies']:verify(item['path'],item['sha256'])
        verify(row['object'],row['objectSha256']);proof=row['realArm7Link']
        verify(proof['linkCommand'][0],proof['linkerSha256']);verify(proof['lcf'],proof['lcfSha256'])
        verify(Path(proof['cwd'])/'linked.elf',proof['linkedElfSha256']);verify(Path(proof['cwd'])/'caller.bin',pin['targetSha256'])
        for anchor in proof['zeroCodeAnchors']:verify(anchor['object'],anchor['objectSha256'])
        trace=row['oracle']['traceProduct'];data=verify(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(data)
        if len(data)!=trace['compressedBytes'] or len(raw)!=trace['rawBytes'] or matcher.digest(raw)!=trace['rawSha256'] or data[4:8]!=bytes(4):raise ValueError('Current priority native trace differs')
        records=json.loads(raw)
        if len(records)!=120 or trace['records']!=120 or any(not record['state']['actualReturn'] for record in records):raise ValueError('Priority supported return evidence differs')
    symbols,entries=bindings(report['matches'])
    if report['nativeSymbols']!=symbols or report['nativeSymbolEntries']!=entries:raise ValueError('Published qualified priority native symbols differ')
    key=matcher.digest(json.dumps(report['generatorSources'],sort_keys=True).encode())
    if key not in _FRESH:_FRESH[key]=[matcher.build(pin) for pin in profile['matches']]
    if report['matches']!=_FRESH[key]:raise ValueError('Published priority source/link/native evidence differs from fresh build')
    return {('arm7','','arm7-wram','0x38026e0','arm'):report['matches'][0]}


def main():
    report=json.loads(REPORT.read_text());validate(report);controls=[]
    def reject(name,operation):
        try:operation()
        except Exception as error:controls.append(dict(name=name,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid priority evidence accepted: '+name)
    changes=(('wrong-rom',('romSha256',),'0'*64),('wrong-processor',('processor',),'arm9'),
        ('whole-module-overclaim',('wholeModuleLinked',),True),('native-data-credit',('originalDataSourceCredit',),4),
        ('missing-generator-closure',('generatorSources',),[]),('missing-runtime-closure',('pinnedGeneratorAndRuntimeDependencies',),[]),
        ('missing-symbol-map',('nativeSymbols',),{}),('invented-symbol-binding',('nativeSymbolEntries',),[]),
        ('inflated-return-count',('actualNativeAndCompiledReturns',),241),('mixed-helper-count',('actualSeparatelyObservedNestedReturns',),240),
        ('invented-context-return',('actualNonlocalContextTransfers',),1),('wrong-mode',('matches',0,'mode'),'thumb'),
        ('missing-include-closure',('matches',0,'sourceDependencies'),[]),('wrong-source-hash',('matches',0,'sourceSha256'),'0'*64),
        ('absent-real-comparison',('matches',0,'exactAfterDeclaredRelocation'),False),('false-return',('matches',0,'oracle','verifiedReturn'),False),
        ('original-compiler-input',('matches',0,'sourceOnlyCompilerInput','originalCodeCompilerInput'),True),
        ('wrong-word-return',('matches',0,'sourceAbiContract','return'),'u8'),('wrong-argument-count',('matches',0,'sourceAbiContract','physicalArgumentWords'),0),
        ('invented-complete-helper-model',('matches',0,'oracle','independentCompleteMappedMemoryModel'),True),
        ('false-original-object-extent',('sharedInterface','originalTotalObjectExtentsClaimed'),True))
    for name,keys,value in changes:
        changed=copy.deepcopy(report);target=changed
        for key in keys[:-1]:target=target[key]
        target[keys[-1]]=value;reject(name,lambda changed=changed:validate(changed))
    proof=report['matches'][0]['realArm7Link'];binary=(ROOT/proof['cwd'])/'caller.bin';backup=binary.read_bytes()
    try:
        binary.unlink();reject('missing-linked-product-after-cache',lambda:validate(report))
        binary.write_bytes(bytes([backup[0]^1])+backup[1:]);reject('corrupt-linked-product-after-cache',lambda:validate(report))
    finally:binary.write_bytes(backup)
    trace=ROOT/report['matches'][0]['oracle']['traceProduct']['path'];backup=trace.read_bytes()
    try:
        trace.unlink();reject('missing-native-trace-after-cache',lambda:validate(report))
        trace.write_bytes(bytes([backup[0]^1])+backup[1:]);reject('corrupt-native-trace-after-cache',lambda:validate(report))
    finally:trace.write_bytes(backup)
    import shutil
    import crossreuse_utility_c
    from elftools.elf.elffile import ELFFile
    pin=json.loads(matcher.PROFILE.read_text())['matches'][0];negative=[]
    mutations=(('wrong-previous-word','previous=state->priority','previous=state->command'),
        ('wrong-stored-word','state->priority=priority','state->references=priority'),
        ('wrong-thread-pointer','(state->thread,priority)','(&state->thread[1],priority)'))
    for name,old,new in mutations:
        text=(ROOT/pin['source']).read_text();changed_text=text.replace(old,new)
        if changed_text==text:raise ValueError('Required priority negative token absent')
        directory=matcher.WORK/'controls'/name;unit=directory/'src';shutil.copytree(matcher.ABI_ROOT,unit,dirs_exist_ok=True)
        source=unit/(ROOT/pin['source']).relative_to(matcher.ABI_ROOT);source.write_text(changed_text,encoding='utf-8')
        deps=[dict(path=(unit/(ROOT/item['path']).relative_to(matcher.ABI_ROOT)).relative_to(ROOT).as_posix(),sha256=sha256(unit/(ROOT/item['path']).relative_to(matcher.ABI_ROOT))) for item in pin['sourceDependencies']]
        changed=dict(pin,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=deps)
        attempt,compiled=crossreuse_utility_c.compile_origin(changed,ROOT/pin['compiler'],pin['compilerFlags'],directory)
        if compiled is None:raise ValueError('Wrong priority C failed compilation: '+str(attempt))
        derived,masks,body=compiled
        if len(body)!=64:raise ValueError('Wrong priority C did not retain complete size')
        with (ROOT/derived['probeObject']).open('rb') as stream:
            elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==pin['name']);section,offset=symbol['st_shndx'],symbol['st_value']
        entry=dict(changed,object=derived['probeObject'],objectSha256=derived['probeObjectSha256'],sectionIndex=section,sectionOffset=offset,
            relocations=[dict(r,format='SHT_RELA',explicitAddend=r['addend'],originalEncodedWord=body[r['offset']:r['offset']+4].hex()) for r in derived['relocations']])
        reject('real-compiler-link-rejects-'+name,lambda entry=entry,directory=directory:matcher.linker.validate(entry,directory/'real-link'))
        bad=(directory/'real-link/caller.bin').read_bytes()
        if len(bad)!=64 or matcher.digest(bad)==pin['targetSha256']:raise ValueError('Priority runtime negative did not use actual changed linked C')
        fixture=matcher.fixture.normal;case=dict(previous=4,priority=5);machine=fixture.setup(0x038026e0,bad,case,0)
        execution=machine['invoke'](0x038026e0,[5],True,20000)
        if not execution['actualReturn']:raise ValueError('Wrong priority C failed before actual return')
        reject('actually-returning-wrong-C-model-rejects-'+name,lambda bad=bad:fixture.execute(0x038026e0,bad,case,0))
        negative.append(dict(name=name,actualReturnBeforeIndependentModel=execution,linkedSha256=matcher.digest(bad),sourceSha256=sha256(source),objectSha256=derived['probeObjectSha256'],sourceCredit=0))
    if len(validate(report))!=1:raise ValueError('Positive priority evidence not restored')
    output=ROOT/'evidence/verification/arm7-lane-card-priority64-controls-20261031.json'
    write_json(output,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),report=REPORT.relative_to(ROOT).as_posix(),reportSha256=sha256(REPORT),
        baselineInventory=dict(path='evidence/arm7/ghidra-runtime-inventory.json',sha256=INVENTORY_SHA),positiveUnits=1,matchedInitializedBytes=64,actualOriginalAndCompiledReturns=240,
        actualSeparateNestedReturns=1632,actualWrongCNormalReturns=len(negative),negativeSourceProofs=negative,controls=controls,allPassed=all(c['rejected'] for c in controls)))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),controls=len(controls),allPassed=True))


if __name__=='__main__':main()
