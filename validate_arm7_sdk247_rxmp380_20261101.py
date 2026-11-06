import copy
import gzip
import hashlib
import json
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk247_rxmp380_20261101 as matcher
import link_arm7_sdk247_rxmp380_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk246_rxmp380_native_20261101 as native
import source_dependencies
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk247-rxmp380-controls-20261101.json'
_FRESH=None

def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('Settings full current source/input/product missing or changed')
    return path

def fresh():
    global _FRESH
    if _FRESH is None:
        result=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=600)
        if result.returncode:raise ValueError(result.stderr[-7000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH

def validate(report):
    if report!=fresh():raise ValueError('Fresh settings source/native/link report differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSha256']!=sha256(matcher.__file__)or report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current settings source-only closure differs')
    for pin in pins:checked(pin['path'],pin['sha256'])
    if len(report['matches'])!=1 or report['matchedInitializedBytes']!=380 or report['matchedCodeBytes']!=364 or report['generatedLiteralBytes']!=16 or report['initializedDenominatorDelta']!=0:raise ValueError('Complete settings extents differ')
    output={}
    for row in report['matches']:
        policy.qualified(row)
        if not source_dependencies.dependencies_current(row):raise ValueError('Quoted complete source-parent include closure differs')
        for key,digest in[('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Complete ordinary C and unchanged real-link evidence absent')
        trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
        if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic settings trace differs')
        records=json.loads(raw)
        if len(records)!=len(native.cases())or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Actual returning source/native independent state/port evidence absent')
        output[('arm7','','arm7-main',row['address'],'arm')]=row
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[4,4,0x694,48,50,66,844,942,972,936,966,1250,46,44,8,12,10,16,6,16,30,36,4,16]:raise ValueError('Complete settings and beacon declaration layout differs')
    return output

def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid settings proof survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    changes=[('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('program',('program',),'child.srl'),('module',('module',),'arm7-wram'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('bytes',('matchedInitializedBytes',),381),('code',('matchedCodeBytes',),380),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),380),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),0),('nested',('totalActualHelperReturns',),1),('fill',('totalActualPrefixFillReturns',),0),('constructor',('constructorActualReturnCredit',),1),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('mode-returns',('totalActualSetupEntryReturns',),0),('mode-helper-returns',('totalActualHelperReturns',),1),('backing-domain',('matches',0,'sourceAbiContract','halfwordAlignedCompletePacketRequired'),False),('callback-credit',('calleeSourceCredit',),1),('setup-erased',('matches',0,'oracle','originalHeapOwnedIncomingBufferAndQueueRequired'),False)]
    for index in range(1):
        for name,key,value in[('address','address','0x27f2454'),('mode','mode','thumb'),('source','sourceSha256','0'*64),('headers','sourceDependencies',[]),('flags','compilerFlags',[]),('exact','exactBytes',False),('source-only','sourceOnlyCompilerInput',False),('blob','originalObjectScaffolding',True)]:changes.append((name+str(index),('matches',index,key),value))
    for name,path,value in changes:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    for row in report['matches']:
        for key,value in[('name','other'),('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27f2454'),('bytes',row['bytes']+4),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],physicalArgumentWords=4)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],sourceNativeModelSha256='0'*64)),('nativeInterfaceContract',dict(row['nativeInterfaceContract'],sourceAidShiftUnsigned=False)),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-settings-producer.json'))]:
            bad=dict(row);bad[key]=value;rejected(row['address']+'-'+key,lambda bad=bad:policy.qualified(bad),direct)
        before=base.data_binding;policy.validate(row,matcher.WORK/('restoration-'+row['address'][2:]))
        if base.data_binding is not before:raise ValueError('Settings word rule leaked after success')
        rejected(row['address']+'-default-refusal',lambda row=row:base.validate(row,matcher.WORK/('default-refusal-'+row['address'][2:])),direct);rejected(row['address']+'-output-escape',lambda row=row:policy.validate(row,ROOT/'evidence'),direct)
        if base.data_binding is not before:raise ValueError('Settings word rule leaked after error')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(report['matches'][0],address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();body=(matcher.WORK/'positive/real-link/caller.bin').read_bytes()
    def supported(case,budget,candidate,image=main,ram=wram):
        result=native.run(image,ram,case,0,body=candidate,budget=budget)
        if not result['actualOwnReturn']or not result.get('modelPassed'):raise ValueError('Copy prerequisite unsupported; zero return/post-fault credit')
    case=next(c for c in native.cases()if c['sta']==0x40 and c['bssidMatches']and c['linkMatches'])
    for name,changed,budget in [('runtime-word',dict(case,wrongRuntimePointer=True),100000),('frame',dict(case,nullFrame=True),100000),('queue',dict(case,missingMessageQueue=True),100000),('aid-domain',dict(case,aid=32),100000),('exhaustion',case,1)]:
        for label,candidate in [('original',None),('compiled',body)]:rejected(name+'-'+label,lambda changed=changed,budget=budget,candidate=candidate:supported(changed,budget,candidate),execution)
    for name,image,ram in [('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:rejected('current-'+name,lambda image=image,ram=ram:supported(case,100000,None,image,ram),execution)
    row=report['matches'][0];path=matcher.WORK/'positive/real-link/caller.bin';raw=path.read_bytes()
    try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected('changed-linked-product',lambda:validate(report),metadata)
    finally:path.write_bytes(raw)
    trace=ROOT/row['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0));print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution))),flush=True)
if __name__=='__main__':main()
