import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT,write_json,sha256,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov001_rows595_machine_20261101 as M
import ov001_rows595_models_20261101 as P
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-rows594/sequential-kind/source.c'
WORK=ROOT/'work/ol595-proof'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name):
    previous=c.symbol_address
    def resolver(symbol):
        if symbol=='_s32_div_f':return M.DIV
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('595 unqualified intrinsic rejected: '+symbol)
        return previous(symbol)
    c.symbol_address=resolver;c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,'ov001','2','off',True)
    finally:c.symbol_address=previous
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('595 ordinary C failed compilation')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('595 runtime differs')
    contract=ROOT/'evidence/abi/main-float592-row-parameter-chain-20261101.json'
    if sha256(contract)!='28e838158bb4372c0771c5c8e53fe8ce93ee1b8bd9337371220d35e47c26bac4':raise ValueError('595 finite math contracts differ')
    pins=ROOT/'evidence/verification/ov001-rows595-inputs-20261101.json'
    for item in json.loads(pins.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('595 frozen input differs',item['path']))
    original=M.inputs();row,proof,body=compile_unit(SOURCE,'caller');profiles=P.profiles();cases=[];traces=[];seen=set();deps=0;provided=0;writeDifferences=[];coreDifferences=[]
    for index,p in enumerate(profiles):
        native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();nm=P.model(native);cm=P.model(candidate)
        if nm!=cm:raise ValueError(('595 complete independent models differ',p['name']))
        if native['providedCalls']!=candidate['providedCalls']:raise ValueError(('595 prepared provided contracts differ',p['name']))
        n=[ret for ret in native['nativeReturns']if ret['entry']==M.RNG];cc=[ret for ret in candidate['nativeReturns']if ret['entry']==M.RNG]
        if[(r['inputWords'][0],r['returnedWords'][0])for r in n]!=[(r['inputWords'][0],r['returnedWords'][0])for r in cc]:raise ValueError('595 actual RNG sequences differ')
        nw=[w[1:]for w in native['nonstackWrites']];cw=[w[1:]for w in candidate['nonstackWrites']]
        if nw!=cw:writeDifferences.append(p['name'])
        different=[i for i,(a,b)in enumerate(zip(native['coreRegistersAndCpsr'],candidate['coreRegistersAndCpsr']))if a!=b]
        if different:coreDifferences.append(dict(profile=p['name'],coreWordIndexes=different))
        seen.update(native['ownObserved']);count=len(native['nativeReturns'])+len(candidate['nativeReturns']);deps+=count;providers=len(native['providedCalls'])+len(candidate['providedCalls']);provided+=providers;trace=dict(profile=p,model=nm,native={k:native[k]for k in['returnedWords','coreRegistersAndCpsr','nativeReturns','providedCalls','nonstackWrites','ownObserved','mainObserved','instructions']},candidate={k:candidate[k]for k in['returnedWords','coreRegistersAndCpsr','nativeReturns','providedCalls','nonstackWrites','ownObserved','mainObserved','instructions']},nativeFullAfterRamSha256=c.sha(native['after']),candidateFullAfterRamSha256=c.sha(candidate['after']),orderedEffectsEqual=nw==cw,rawCoreDifferences=different);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=providers,actualRngReturnsBoth=len(n)+len(cc),traceSha256=c.sha(encoded(trace))))
        if index%24==0:print(dict(completedPairs=index+1,total=len(profiles)),flush=True)
    template=SOURCE.read_text();controls=[];variants=[('wrong-rng-bound',template.replace('native_fn_0203d294(0xFF)','native_fn_0203d294(0xFE)',1),profiles[1]),('wrong-first-byte',template.replace('u8 *, 0x5F','u8 *, 0x5E',1),profiles[0]),('wrong-scale',template.replace('/ 100 + 1)','/ 100 + 2)',1),profiles[1])]
    for name,text,p in variants:
        if text==template:raise ValueError('595 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-rows595-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('595 frozen wrong source changed')
        source.write_text(text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wr,wp,wb=compile_unit(source,'wrong-'+name);result=M.Machine(original,p,wb).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError('595 wrong source escaped independent model')
        trace={k:result[k]for k in['profile','returnedWords','nativeReturns','providedCalls','nonstackWrites','instructions']};trace.update(actualReturned=True,failure=failure);controls.append(dict(name=name,actualReturned=True,source=wr,genuineLinkComparison=wp,failure=failure,traceSha256=c.sha(encoded(trace)),trace=trace))
    code=set(range(M.ENTRY,M.ENTRY+732,4))
    if seen!=code:raise ValueError(('595 native own instruction coverage differs',len(seen)))
    span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE];literals=[]
    for offset in range(732,780,4):
        address=M.ENTRY+offset;value=int.from_bytes(span[offset:offset+4],'little');readers=[]
        for index in range(0,732,4):
            word=int.from_bytes(span[index:index+4],'little');pc=M.ENTRY+index
            if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==address:readers.append(hex(pc))
        if not readers or any(int(pc,16)not in seen for pc in readers):raise ValueError('595 native literal reader absent')
        literals.append(dict(address=hex(address),bytes=4,value=hex(value),unconditionalObservedReaders=readers))
    raw=encoded(dict(cases=traces,wrongSources=[control['trace']for control in controls]));artifact=ROOT/'evidence/generated/ov001-rows595-functional-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for control in controls:del control['trace']
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=original['module']['sha256'],address=hex(M.ENTRY),mode='arm',bytes=780,sourceCredit=0,source=row,genuineLinkComparison=proof,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=deps,providedCalls=provided,fullRamIndependentModelsEqual=True,allPreparedProviderWordsEqual=True,actualRngSequencesEqual=True,orderedWriteDifferences=writeDifferences,rawCoreDifferences=coreDifferences,nativeOwnObservedCodeBytes=len(seen)*4,nativeReferencedLiteralBytes=48,nativeLiteralEvidence=literals,observedNativeOwnAddresses=sorted(seen),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['The complete ordinary C body remains nonmatching and earns zero source bytes.','Synthetic row/category/record/resource/predicate/output setup is supplied; no ordinary caller or scene reachability is claimed.','Actual original RNG,float math,wide-return math chain and signed division execute. Six named lower service boundaries are explicitly provided; no stub is counted as native.','Only category0..2,row0..2,fileCount0..4 with a sufficient supplied candidate pool are behavior-qualified here. Other paths and termination are unresolved.','Physical scratch registers and write-order differences are retained rather than promoted to exact equivalence.','Original public prototypes and meanings of fields remain separate from measured register/memory behavior.'])
    write_json(ROOT/'evidence/attempts/ov001-rows595-functional-source-20261101.json',report);print(dict(callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=deps,providedCalls=provided,orderedWriteDifferentCases=len(writeDifferences),rawCoreDifferentCases=len(coreDifferences),sourceCredit=0),flush=True)


if __name__=='__main__':execute()
