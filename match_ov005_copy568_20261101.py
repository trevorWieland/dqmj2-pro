import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov005_copy568_machine_20261101 as M
import ov005_copy568_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov005_20261101_copy568/copy.c'
WORK=ROOT/'work/ol568-proof'
PINS=ROOT/'evidence/verification/ov005-copy568-inputs-20261101.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    previous=c.symbol_address
    def resolver(symbol):
        if symbol=='_s32_div_f':return M.DIV
        if __import__('re').fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('568 unqualified compiler intrinsic rejected')
        return previous(symbol)
    c.symbol_address=resolver;c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,'ov005','2','off',False)
    finally:c.symbol_address=previous
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('568 compiler failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('568 runtime differs')
    for row in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('568 frozen input differs',row['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort107-identities-v2-20261101.json';accepted=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov005'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('568 accepted overlap')
    original=M.inputs();row,proof,body=compile_unit(SOURCE,'caller',True);native=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    if body!=native:raise ValueError('568 genuine linked caller differs')
    row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=M.SIZE;profiles=P.profiles();traces=[];cases=[];direct=[];controls=[];seen=set();copySeen=set();totalDeps=0;zero=[];callSites={}
    for sourceAlign in range(4):
        for destAlign in range(4):
            for length in range(18):
                p=dict(name=f'direct-{sourceAlign}-{destAlign}-{length}',sourceAlign=sourceAlign,destAlign=destAlign,length=length);r=M.Machine(original,p,direct=True).run();model=P.model(r);copySeen.update(r['ownObserved']);direct.append(dict(profile=p,model=model,returnedWords=r['returnedWords'],dataReads=r['dataReads'],nonstackWrites=r['nonstackWrites'],instructions=r['instructions'],ownObserved=r['ownObserved']))
    if copySeen!=set(range(M.COPY,M.COPY+304,4)):raise ValueError(('568 direct original copy code coverage differs',len(copySeen)*4))
    for p in profiles:
        n=M.Machine(original,p).run();nm=P.model(n);candidate=M.Machine(original,p,body).run();cm=P.model(candidate)
        if nm!=cm or n['allArmCoreRegistersAndCpsr']!=candidate['allArmCoreRegistersAndCpsr']or n['returnedWords']!=candidate['returnedWords']or n['nativeReturns']!=candidate['nativeReturns']or n['nonstackWrites']!=candidate['nonstackWrites']or n['dataReads']!=candidate['dataReads']or n['after']!=candidate['after']:raise ValueError(('568 complete original/C execution differs',p['name']))
        seen.update(n['ownObserved']);deps=len(n['nativeReturns'])+len(candidate['nativeReturns']);totalDeps+=deps
        if not nm['abstractCDefinedRemainderDomain']:zero.append(p['name'])
        for ret in n['nativeReturns']:callSites[hex(ret['callPc'])]=callSites.get(hex(ret['callPc']),0)+1
        trace=dict(profile=p,model=nm,allArmCoreRegistersAndCpsr=n['allArmCoreRegistersAndCpsr'],returnedWords=n['returnedWords'],nativeReturns=n['nativeReturns'],nonstackWrites=n['nonstackWrites'],dataReads=n['dataReads'],fullAfterRamSha256=c.sha(n['after']),nativeInstructions=n['instructions'],candidateInstructions=candidate['instructions'],ownObserved=n['ownObserved']);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,abstractCDefinedRemainderDomain=nm['abstractCDefinedRemainderDomain'],traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+160,4)):raise ValueError(('568 own code coverage differs',len(seen)*4))
    template=SOURCE.read_text();signature='u32 native_ov005_021d9ae0(void *arg0, u32 arg1, void *arg2, void *arg3) {';wrongSources=[('mask-after-locals',template.replace('    var_r0 = M2C_FIELD(', '    arg1 &= 0xFFFFU;\n    var_r0 = M2C_FIELD(',1),dict(stride=1,rows=3,total=3,index=0xFFFFFFFF)),('quotient',template.replace(' % ',' / '),dict(stride=5,rows=3,total=11,index=2)),('zero-fallback',template.replace('if (temp_r1 != 0)','if (temp_r1 == 0)',1),dict(stride=5,rows=3,total=15,index=2))]
    for name,text,p in wrongSources:
        directory=ROOT/'nonmatching/overlay-lane/20261101-ov005-copy568-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c';header=directory/'context.h'
        if source.exists()and source.read_text()!=text:raise ValueError('568 frozen wrong source differs')
        source.write_text(text);header.write_bytes(SOURCE.with_name('context.h').read_bytes());wrongRow,wrongProof,wrongBody=compile_unit(source,'wrong-'+name,False);p['name']='wrong-'+name;r=M.Machine(original,p,wrongBody).run()
        try:P.model(r)
        except ValueError as error:failure=str(error)
        else:raise ValueError('568 wrong source escaped independent model')
        trace=dict(profile=p,returnedWords=r['returnedWords'],nativeReturns=r['nativeReturns'],nonstackWrites=r['nonstackWrites'],dataReads=r['dataReads'],instructions=r['instructions'],actualReturned=True,failure=failure);controls.append(dict(name=name,actualReturned=True,source=wrongRow,genuineLinkComparison=wrongProof,traceSha256=c.sha(encoded(trace)),failure=failure,trace=trace))
    raw=encoded(dict(cases=traces,directOriginalCopy=direct,wrongSources=[r['trace']for r in controls]));artifact=ROOT/'evidence/generated/ov005-copy568-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for item in controls:del item['trace']
    literal=M.ENTRY+160;readers=sorted(set(pc for trace in traces for pc,address,size,value in trace['dataReads']if address==literal));row['oracle']=dict(cases=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalDeps,providedCalls=0,providerFreePairs=len(profiles),fullRamAndOrderedWritesEqual=True,allArmCoreRegistersAndCpsrEqual=True,ownObservedCodeBytes=160,referencedLiteralBytes=4,unclassifiedBytes=0,actualNativeCallSites=callSites,originalDirectCopyReturns=len(direct),originalDirectCopyObservedCodeBytes=len(copySeen)*4,zeroDenominatorCompiledPairs=len(zero),zeroDenominatorProfiles=zero,casesEvidence=cases)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov005',moduleInputSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=dict(address=hex(literal),value='0x0000FFFF',readers=[hex(p)for p in readers]),rawInputContract=dict(register='R1',view='full32 word, low16 destination store, three exact full32 sentinel comparisons',sentinels=['0x0000FFFF','0x0000FFFE','0x0000FFFD'],originalFormalTypeProven=False),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw),uncompressedBytes=len(raw)),wholeModuleLinked=False,sourceReconstructionComplete=False,limitations=['Synthetic aligned pointer chains, descriptors and payloads are supplied; no scene initialization or asset semantics are claimed.','Only the164-byte caller is reconstructed; actual native copy/division helpers add zero source credit.','Partial overlap is unsupported; distinct buffers and identical source/destination payloads are tested.','Four zero-step last-block pairs are pinned compiled behavior outside abstract C remainder semantics; all remaining caller pairs use a defined remainder domain.','Physical R0 can contain a pointer word or merged tail halfword; no original pointer-return or public prototype claim is made.','Direct helper alignment/length probes are separate from caller dependency totals; raw R1 upper-bit distinctions are retained.'])
    write_json(ROOT/'evidence/matches/ov005-20261101-copy568.json',report);print(dict(matchedBytes=164,functions=1,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalDeps,directOriginalCopyReturns=len(direct),providedCalls=0,zeroDenominatorPairs=len(zero),wrongActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
