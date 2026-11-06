import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_builder584_machine_20261101 as M
import main_builder584_models_20261101 as P
SOURCE=ROOT/'src/overlays/main_20261101_builder588/builder.c'
WORK=ROOT/'work/ol588-proof'
PINS=ROOT/'evidence/verification/main-builder588-inputs-20261101.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'main','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('588 compiler failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('588 runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('588 frozen input differs',item['path']))
    accepted=json.loads((ROOT/'evidence/verification/accepted-cohort107-identities-v2-20261101.json').read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='main'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('588 accepted overlap')
    original=M.inputs();row,proof,body=compile_unit(SOURCE,'caller',True)
    if body!=original['arm'][M.ENTRY-M.BASE:M.ENTRY-M.BASE+M.SIZE]:raise ValueError('588 actual caller differs')
    row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=M.SIZE;cases=[];traces=[];seen=set();helperSeen={str(a):set()for a in M.RANGES};totalDeps=0;provided=0;profiles=P.profiles();controls=[]
    for index,p in enumerate(profiles):
        native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();nm=P.model(native);cm=P.model(candidate)
        for key in['allArmCoreRegistersAndCpsr','returnedWords','nativeReturns','providedCalls','tailForwardings','nonstackWrites','after']:
            if native[key]!=candidate[key]:raise ValueError(('588 full original/C differs',p['name'],key))
        if nm!=cm:raise ValueError('588 independent original/C models differ')
        seen.update(native['ownObserved'])
        for key in helperSeen:helperSeen[key].update(native['helperObserved'][key])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns']);totalDeps+=deps;provided+=len(native['providedCalls'])*2
        trace={k:native[k]for k in['profile','slot','allArmCoreRegistersAndCpsr','returnedWords','nativeReturns','providedCalls','tailForwardings','nonstackWrites','ownObserved','helperObserved','instructions']};trace.update(model=nm,fullAfterRamSha256=c.sha(native['after']),candidateInstructions=candidate['instructions']);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,providedCalls=len(native['providedCalls'])*2,traceSha256=c.sha(encoded(trace))))
        if index%200==0:print(dict(completedPairs=index+1,total=len(profiles)),flush=True)
    if seen!=set(range(M.ENTRY,M.ENTRY+M.SIZE,4)):raise ValueError(('588 own instruction coverage differs',len(seen)))
    for key,size in M.RANGES.items():
        if helperSeen[str(key)]!=set(range(key,key+size,4)):raise ValueError(('588 helper coverage differs',key))
    template=SOURCE.read_text();variants=[('byte-status',template.replace('if (*temp_r0 != 0)','if (*(u8 *)temp_r0 != 0)'),dict(name='wrong-byte-status',mode=1,occupied=256,counter=1,args=[1,4,127,12,1,2,3,4,0,1])),('sum-dimensions',template.replace('*(u8 *)&arg6 * *(u8 *)&arg7','*(u8 *)&arg6 + *(u8 *)&arg7'),dict(name='wrong-sum',mode=1,occupied=0,counter=1,args=[1,4,127,12,1,2,3,4,0,1])),('unsigned-byte',template.replace('(s32) *(s8 *)&arg8','(s32) *(u8 *)&arg8'),dict(name='wrong-sign',mode=1,occupied=0,counter=1,args=[1,4,127,12,1,2,3,4,255,1]))]
    for name,text,p in variants:
        if text==template:raise ValueError('588 negative source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-main-builder588-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c';header=directory/'context.h'
        if source.exists()and source.read_text()!=text:raise ValueError('588 frozen control changed')
        source.write_text(text);header.write_bytes(SOURCE.with_name('context.h').read_bytes());wrongRow,wrongProof,wrongBody=compile_unit(source,'wrong-'+name,False);result=M.Machine(original,p,wrongBody).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError('588 returning control escaped model')
        trace={k:result[k]for k in['profile','returnedWords','nativeReturns','providedCalls','nonstackWrites','instructions']};trace.update(actualReturned=True,failure=failure);controls.append(dict(name=name,actualReturned=True,source=wrongRow,genuineLinkComparison=wrongProof,traceSha256=c.sha(encoded(trace)),failure=failure,trace=trace))
    raw=encoded(dict(cases=traces,wrongSources=[control['trace']for control in controls]));artifact=ROOT/'evidence/generated/main-builder588-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for control in controls:del control['trace']
    row['oracle']=dict(cases=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalDeps,providedCalls=provided,fullRamAndOrderedWritesEqual=True,allArmCoreRegistersAndCpsrEqual=True,ownObservedCodeBytes=168,referencedLiteralBytes=0,unclassifiedBytes=0,nativeObservedCodeBytes={key:len(value)*4 for key,value in helperSeen.items()},tailForwardings=len(profiles)*2,tailForwardingsNotAdditionalReturns=True,casesEvidence=cases)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='main',moduleInputSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw),uncompressedBytes=len(raw)),inputContract=dict(preparedPhysicalWords=10,registerWords=4,stackWords=6,stackConsumption=['SP+0 low8','SP+4 low8','SP+8 low8','SP+0xC low8','SP+0x10 signed8','SP+0x14 full32'],slotStatusWidth=32,originalPublicPrototypeProven=False),wholeModuleLinked=False,sourceReconstructionComplete=False,limitations=['Synthetic runtime bank byte, mapped slot words and counter state are supplied, not ordinary scene initialization.','Negative and bank-wrapped indices are binary mapped-address probes; no legal slot-array domain is inferred.','Only main02049794/168 is reconstructed; actual native index/getter/counter helpers add zero source credit.','Main02049BE4 is an explicit supplied eleven-word lower constructor boundary with zero RAM effects and poisoned caller-saved registers/flags. Resource allocation, rendering, slot population and hardware effects remain unqualified.','Ten full-word formals use defined character access to their low object byte; this is a little-endian C target view, not an original public-header proof.','All five consumed stack byte fields are independently exercised across256 low-byte values with nonzero upper bits; resource-counter overflow is unsigned32.'])
    write_json(ROOT/'evidence/matches/main-20261101-builder588.json',report);print(dict(functions=1,matchedBytes=168,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalDeps,providedCalls=provided,tailForwardingsNotAdditionalReturns=len(profiles)*2,wrongActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
