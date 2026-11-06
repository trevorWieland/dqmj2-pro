import copy
import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
import match_arm7_sdk180_ssid280_20261101 as matcher
import link_arm7_sdk180_ssid208_20261101 as policy
import link_arm7_bulk_20261030 as base
import arm7_sdk157_ssid_native_20261101 as ssid
import arm7_sdk159_byte_helpers_native_20261101 as byte
from unicorn import UcError
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/verification/arm7-sdk180-ssid280-controls-20261101.json'
_FRESH=None
def checked(path,digest):
    path=(ROOT/path).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=digest:raise ValueError('SSID complete source/input/product missing or changed')
    return path
def fresh():
    global _FRESH
    if _FRESH is None:
        call=subprocess.run([sys.executable,str(Path(matcher.__file__).resolve())],cwd=Path.cwd(),capture_output=True,text=True,timeout=600)
        if call.returncode:raise ValueError(call.stderr[-6000:])
        _FRESH=json.loads(matcher.REPORT.read_text())
    return _FRESH
def validate(report):
    if report!=fresh():raise ValueError('Fresh full SSID/byte source/link/native/input evidence differs')
    if report['generatorSha256']!=sha256(matcher.__file__):raise ValueError('SSID generator differs')
    pins=json.loads((matcher.SOURCE/'generator-pins.json').read_text())['files'];complete=pins+[dict(path=(matcher.SOURCE/'generator-pins.json').relative_to(ROOT).as_posix(),sha256=sha256(matcher.SOURCE/'generator-pins.json'))]
    if report['generatorSources']!=complete or report['pinnedGeneratorAndRuntimeDependencies']!=pins:raise ValueError('Current complete SSID replay closure differs')
    for item in pins:checked(item['path'],item['sha256'])
    if len(report['matches'])!=3 or report['matchedInitializedBytes']!=280 or report['matchedCodeBytes']!=276 or report['generatedLiteralBytes']!=4 or report['initializedDenominatorDelta']!=0:raise ValueError('Full qualified SSID/byte ranges differ')
    result={}
    for row in report['matches']:
        pending=[ROOT/row['source']];included=set()
        while pending:
            parent=pending.pop()
            for name in re.findall(r'(?m)^\s*#include\s+"([^"\n]+)"',parent.read_text(encoding='utf-8')):
                child=(parent.parent/name).resolve()
                if not child.is_relative_to(ROOT)or not child.is_file():raise ValueError('Quoted include does not resolve from its source parent')
                if child not in included:included.add(child);pending.append(child)
        if included!={(ROOT/dep['path']).resolve()for dep in row['sourceDependencies']}:raise ValueError('Complete declared relative include closure differs')
        if int(row['address'],0)==ssid.TOP:policy.qualified(row)
        for key,digest in [('source','sourceSha256'),('object','objectSha256'),('compiler','compilerSha256')]:checked(row[key],row[digest])
        for dep in row['sourceDependencies']:checked(dep['path'],dep['sha256'])
        link=row['realLink'];checked(link['lcf'],link['lcfSha256']);directory=Path(link['lcf']).parent;checked(directory/'caller.bin',row['targetSha256']);checked(directory/'linked.elf',link['linkedElfSha256'])
        if not row['exactBytes']or not row['exactAfterDeclaredRelocation']or not row['sourceOnlyCompilerInput']or row['originalObjectScaffolding']:raise ValueError('Full ordinary C/unchanged real-link proof absent')
        trace=row['oracle']['trace'];compressed=checked(trace['path'],trace['compressedSha256']).read_bytes();raw=gzip.decompress(compressed)
        if compressed[4:8]!=bytes(4)or hashlib.sha256(raw).hexdigest()!=trace['rawSha256']:raise ValueError('Deterministic SSID/byte trace differs')
        records=json.loads(raw);count=1154 if int(row['address'],0)==ssid.TOP else 2048
        if len(records)!=count or not all(r['original']==r['compiled']and r['original']['actualOwnReturn']and r['original']['modelPassed']for r in records):raise ValueError('Actual source returns/independent model absent')
        result[('arm7','','arm7-main',row['address'],'arm')]=row
    proof=report['abiLayoutProof'];checked(proof['source'],proof['sourceSha256']);checked(proof['object'],proof['objectSha256'])
    if proof['values']!=[4,4,4,0x694,0x362,0x364,0x384,0x404]:raise ValueError('SSID source declaration layout differs')
    return result
def main():
    report=fresh();validate(report);metadata=[];direct=[];execution=[]
    def rejected(name,action,collection):
        try:action()
        except(ValueError,FileNotFoundError,KeyError,UcError)as error:collection.append(dict(name=name,rejected=True,error=str(error)))
        else:raise ValueError('Invalid SSID evidence survived:'+name)
    def changed(path,value):
        bad=copy.deepcopy(report);obj=bad
        for key in path[:-1]:obj=obj[key]
        obj[path[-1]]=value;validate(bad)
    for name,path,value in [('rom',('romSha256',),'0'*64),('processor',('processor',),'arm9'),('module',('module',),'arm7-wram'),('program',('program',),'child.srl'),('generator',('generatorSha256',),'0'*64),('closure',('generatorSources',),[]),('count',('newOrdinaryFunctionCount',),4),('bytes',('matchedInitializedBytes',),281),('code',('matchedCodeBytes',),280),('pools',('generatedLiteralBytes',),0),('denominator',('initializedDenominatorDelta',),280),('whole',('wholeModuleLinked',),True),('complete',('sourceReconstructionComplete',),True),('returns',('totalActualOwnReturns',),10501),('nested',('totalScopedNestedReturns',),0),('fill',('totalActualFillReturns',),0),('constructor',('constructorActualReturnCredit',),2308),('wrong',('wrongC',),[]),('layout',('abiLayoutProof','values'),[]),('setter-credit',('excludedInexactSetterBytes',),0),('shared-header-credit',('completeSharedHeadersAdditionalSourceCredit',),504),('address',('matches',0,'address'),'0x27ea3b4'),('mode',('matches',0,'mode'),'thumb'),('source',('matches',0,'sourceSha256'),'0'*64),('headers',('matches',0,'sourceDependencies'),[]),('flags',('matches',0,'compilerFlags'),[]),('exact',('matches',0,'exactBytes'),False),('source-only',('matches',0,'sourceOnlyCompilerInput'),False),('blob',('matches',0,'originalObjectScaffolding'),True),('argument',('matches',0,'sourceAbiContract','physicalArgumentWords'),4),('return',('matches',0,'sourceAbiContract','declaredReturn'),'u8'),('domain',('matches',0,'sourceAbiContract','rawNonstandardUpperArgumentBitsNotQualified'),False),('providers',('matches',0,'oracle','providerReplacements'),['byte']),('raw-state',('matches',0,'oracle','allRawCpuFlagsStackRamReadsAndOrderedWritesCompared'),False)]:rejected(name,lambda path=path,value=value:changed(path,value),metadata)
    row=report['matches'][0]
    for key,value in [('name','other'),('processor','arm9'),('program','dwc/utility.bin/move/child.srl'),('module','arm7-wram'),('mode','thumb'),('address','0x27ea3b4'),('bytes',204),('source','src/unowned.c'),('sourceSha256','0'*64),('sourceDependencies',[]),('compilerFlags',[]),('compilerSha256','0'*64),('targetSha256','0'*64),('inputModuleSha256','0'*64),('romSha256','0'*64),('runtimePointerQualification',dict(row['runtimePointerQualification'],storageBytes=8)),('runtimePointerQualification',dict(row['runtimePointerQualification'],report='evidence/no-producer.json'))]:
        bad=dict(row);bad[key]=value;rejected('caller-'+key,lambda bad=bad:policy.qualified(bad),direct)
    before=base.data_binding;policy.validate(row,matcher.WORK/'restoration-positive')
    if base.data_binding is not before:raise ValueError('SSID word rule leaked after success')
    rejected('default-word-refusal',lambda:base.validate(row,matcher.WORK/'default-refusal-control'),direct);rejected('output-escape',lambda:policy.validate(row,ROOT/'evidence'),direct)
    if base.data_binding is not before:raise ValueError('SSID word rule leaked after failure')
    modules,unused=base.namespace('')
    for address in(0x0380fff0,0x0380fff5,0x0380fff8,0x0380fffc):rejected('neighbor-'+hex(address),lambda address=address:base.data_binding(row,address,modules),direct)
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();bodies={int(r['address'],0):(matcher.WORK/r['address'][2:]/'real-link/caller.bin').read_bytes()for r in report['matches']}
    for name,case,budget in [('runtime-word',dict(ssid.cases()[0],wrongRuntimePointer=True),20000),('invalid-input',dict(ssid.cases()[0],length=1,storedLength=1,invalidInputPointer=True),20000),('exhaustion',ssid.cases()[0],1)]:
        for label,candidate in [('original',None),('compiled',bodies)]:rejected(name+'-'+label,lambda case=case,budget=budget,candidate=candidate:ssid.run(main,wram,case,0,budget=budget,bodies=candidate),execution)
    for entry in(byte.READ,byte.WRITE):
        for name,case,budget in [('invalid-backing',dict(byte.cases()[0],invalidBacking=True),100),('exhaustion',byte.cases()[0],1)]:
            for label,candidate in [('original',None),('compiled',bodies[entry])]:rejected(name+'-'+hex(entry)+'-'+label,lambda entry=entry,case=case,budget=budget,candidate=candidate:byte.run(main,wram,entry,case,0,budget=budget,body=candidate),execution)
    for name,image,ram in [('main',bytes([main[0]^1])+main[1:],wram),('wram',main,bytes([wram[0]^1])+wram[1:])]:
        rejected('current-input-'+name,lambda image=image,ram=ram:ssid.run(image,ram,ssid.cases()[0],0),execution);rejected('byte-current-input-'+name,lambda image=image,ram=ram:byte.run(image,ram,byte.READ,byte.cases()[0],0),execution)
    for row in report['matches']:
        path=matcher.WORK/row['address'][2:]/'real-link/caller.bin';raw=path.read_bytes()
        try:path.write_bytes(bytes([raw[0]^1])+raw[1:]);rejected('changed-linked-'+row['address'],lambda:validate(report),metadata)
        finally:path.write_bytes(raw)
    trace=ROOT/report['matches'][0]['oracle']['trace']['path'];held=trace.with_name('held-native-records.json.gz')
    try:trace.rename(held);rejected('missing-native-product',lambda:validate(report),metadata)
    finally:
        if held.is_file():held.rename(trace)
    validate(json.loads(matcher.REPORT.read_text()));write_json(REPORT,dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),inputReportSha256=sha256(matcher.REPORT),metadataControls=metadata,metadataControlCount=len(metadata),directPolicyControls=direct,directPolicyControlCount=len(direct),nativePrerequisiteControls=execution,nativeControlCount=len(execution),freshSourceOnlyBuildBeforeValidation=True,restoredPositive=True,additionalSourceCredit=0))
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),metadata=len(metadata),policy=len(direct),native=len(execution))),flush=True)
if __name__=='__main__':main()
