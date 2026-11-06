import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,write_json,sha256,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_rows598_machine_20261101 as M
import ov001_rows598_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov001_20261101_rows598/caller.c'
WORK=ROOT/'work/ol598-proof'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov001','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('598 C compilation failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('598 runtime differs')
    pins=ROOT/'evidence/verification/ov001-rows598-inputs-20261101.json'
    for item in json.loads(pins.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('598 frozen input differs',item['path']))
    accepted=json.loads((ROOT/'evidence/verification/accepted-cohort110-identities-v2-20261101.json').read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov001'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('598 accepted overlap')
    original=M.inputs();row,proof,body=compile_unit(SOURCE,'caller',True)
    if body!=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]:raise ValueError('598 actual complete caller differs')
    row['exactBytes']=132;row['genuineLinkComparison']=freeze_link(proof);cases=[];traces=[];seen=set();deps=0;providers=0;profiles=P.profiles()
    for p in profiles:
        native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();nm=P.model(native);cm=P.model(candidate)
        for key in['allArmCoreRegistersAndCpsr','returnedWords','nativeReturns','providedCalls','providedCallEdges','nonstackWrites','after']:
            if native[key]!=candidate[key]:raise ValueError(('598 complete original/C differs',p['name'],key))
        if nm!=cm:raise ValueError('598 independent models differ')
        seen.update(native['ownObserved']);count=len(native['nativeReturns'])*2;provided=len(native['providedCalls'])*2;deps+=count;providers+=provided;trace={k:native[k]for k in['profile','allArmCoreRegistersAndCpsr','returnedWords','nativeReturns','providedCalls','providedCallEdges','nonstackWrites','ownObserved','helperObserved','instructions']};trace.update(model=nm,fullAfterRamSha256=c.sha(native['after']),candidateInstructions=candidate['instructions']);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=count,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+124,4)):raise ValueError('598 own code coverage differs')
    template=SOURCE.read_text();variants=[('short-clear',template.replace('0, 396','0, 392',1)),('wrong-order',template.replace('            native_fn_ov001_0222ceb8(index, modifier);\n            native_fn_ov001_0222cf34(index, modifier);','            native_fn_ov001_0222cf34(index, modifier);\n            native_fn_ov001_0222ceb8(index, modifier);',1)),('narrow-modifier',template.replace('native_fn_ov001_0222cf34(index, modifier)','native_fn_ov001_0222cf34(index, (u8) modifier)',1))];controls=[]
    for name,text in variants:
        if text==template:raise ValueError('598 negative source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-rows598-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('598 frozen negative source differs')
        source.write_text(text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wr,wp,wb=compile_unit(source,'wrong-'+name,False);p=dict(name='wrong-'+name,count=1,modifier=65535);result=M.Machine(original,p,wb).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError('598 wrong source escaped independent model')
        trace={k:result[k]for k in['profile','returnedWords','nativeReturns','providedCalls','providedCallEdges','nonstackWrites','instructions']};trace.update(actualReturned=True,failure=failure);controls.append(dict(name=name,actualReturned=True,source=wr,genuineLinkComparison=wp,failure=failure,traceSha256=c.sha(encoded(trace)),trace=trace))
    span=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE];literals=[]
    for offset in[124,128]:
        target=M.ENTRY+offset;value=int.from_bytes(span[offset:offset+4],'little');readers=[]
        for index in range(0,124,4):
            word=int.from_bytes(span[index:index+4],'little');pc=M.ENTRY+index
            if word>>28==14 and word&0x0F7F0000==0x051F0000 and pc+8+((word&4095)if word&0x00800000 else-(word&4095))==target:readers.append(hex(pc))
        if not readers or any(int(pc,16)not in seen for pc in readers):raise ValueError('598 referenced literal reader absent')
        literals.append(dict(address=hex(target),value=hex(value),bytes=4,observedUnconditionalReaders=readers))
    raw=encoded(dict(cases=traces,wrongSources=[control['trace']for control in controls]));artifact=ROOT/'evidence/generated/ov001-rows598-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for control in controls:del control['trace']
    row['oracle']=dict(callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=deps,providedCalls=providers,ownObservedCodeBytes=124,referencedLiteralBytes=8,unclassifiedBytes=0,fullRamAndOrderedEffectsEqual=True,allArmCoreRegistersAndCpsrEqual=True,bothBuffersClearedBeforeEveryProvidedStage=True,casesEvidence=cases);report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=literals,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),getterContract=dict(module='main',address='0x020C5938',mode='arm',inputWordsConsumed=0,readAddress='0x021D637C',readWidthBits=16,signed=False,returnedRepresentation='Zero-extended unsigned16 inR0',actualRuntimeValueProvided=True,originalFieldMeaningProven=False),wholeModuleLinked=False,sourceReconstructionComplete=False,limits=['Only this132-byte ordinary caller is reconstructed; native fill/getter leaves add zero source credit.','All four per-index overlay steps are explicitly supplied with zero RAM effects, includingCF34; its separately proved native behavior is not counted or executed here.','Only the shown prepared input words are asserted; full callee formal arities,types,inherited inputs and scene prerequisites remain unresolved.','Count0..3 and synthetic unsigned16 getter values are tested; the cleared3-row capacity is measured,not proof of a universal legal count limit.','The caller clears both buffers even for count0 and forwards the full zero-extended16-bit scalar. Its game meaning/current value is not inferred from ROM.'])
    write_json(ROOT/'evidence/matches/ov001-20261101-rows598.json',report);print(dict(functions=1,matchedBytes=132,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=deps,providedCalls=providers,wrongActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
