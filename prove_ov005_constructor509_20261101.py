import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,sha256,write_json,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
COUNTS={0x02002C98:3,0x02008C58:3,0x0201D444:2,0x0203CC2C:2,0x020481B8:3,0x0202A8E0:1,0x02048308:0,0x0202A498:2,0x02004E58:3,0x02004CD8:3,0x02004B58:3,0x021DA824:0,0x021DDD60:2,0x021DA838:1,0x02048A9C:2,0x02048A94:2,0x02048A60:3,0x02048644:3,0x021DB09C:3,0x021DD834:0,0x021DB95C:1,0x021DDF24:0}
import ov005_constructor509_machine_20261101 as M
import ov005_constructor509_models_20261101 as P
import probe_main_clear510_20261101 as Q
import verify_ov005_constructor505_20261101 as V
WORK=ROOT/'work/ol509-proof'
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-constructor509/source.c'


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov005','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('509 candidate did not compile')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];out=WORK/name/'linked'
    try:proof=validate(row,qualified_bindings(row),out)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(out/'caller.bin').read_bytes()


def equal_effect(a,b):
    cut=M.STACK-M.BASE;begin=M.ENTRY-M.BASE;end=begin+max(M.SIZE,a['extent'],b['extent'])
    return a['after'][:begin]==b['after'][:begin]and a['after'][end:cut-65536]==b['after'][end:cut-65536]and a['after'][cut+4096:]==b['after'][cut+4096:]and a['ioAfter']==b['ioAfter']and a['vramAfter']==b['vramAfter']and a['returnedR0']==b['returnedR0']and[a['address']for a in a['providedEvents']]==[b['address']for b in b['providedEvents']]


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('509 pinned runtime differs')
    for item in json.loads((ROOT/'evidence/verification/ov005-constructor509-inputs-20261101.json').read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('509 frozen input differs',item['path']))
    V.verify();Q.run();qualification=ROOT/'evidence/verification/main-clear510-r3-consumption-20261101.json'
    original=M.inputs();row,link,body=compile_unit(SOURCE,'candidate');traces=[];cases=[];observed=set();passed=0;independent=0;providerCalls=0;rawDifferences=0;writeDifferences=0;failed=[]
    for p in P.profiles():
        try:
            native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();native['extent']=M.SIZE;candidate['extent']=len(body);nm=P.model(native);cm=P.model(candidate)
            if nm!=cm:raise ValueError('509 independent original/candidate models differ')
            if not equal_effect(native,candidate):raise ValueError('509 original/candidate final effect orcall order differs')
            observed.update(native['ownObserved']);passed+=1;independent+=int(nm['independentlyModeled']);providerCalls+=len(native['providedEvents'])+len(candidate['providedEvents']);raw=sum(x['rawCallerWords']!=y['rawCallerWords']for x,y in zip(native['providedEvents'],candidate['providedEvents']));rawDifferences+=raw
            if any(x['rawCallerWords'][:COUNTS[x['address']]]!=y['rawCallerWords'][:COUNTS[x['address']]]for x,y in zip(native['providedEvents'],candidate['providedEvents'])):raise ValueError('509 prepared core caller words differ')
            for x,y in zip(native['providedEvents'],candidate['providedEvents']):
                changed=[i for i in range(4)if x['rawCallerWords'][i]!=y['rawCallerWords'][i]]
                if changed and(x['address']!=0x02008C58 or changed!=[3]):raise ValueError('509 unqualified extra register difference')
            writes=native['nonstackWrites']!=candidate['nonstackWrites'];writeDifferences+=writes
            if writes:raise ValueError('509 complete ordered writes differ')
            result=dict(profile=p,independentModel=nm,nativeInstructions=native['instructions'],candidateInstructions=candidate['instructions'],nativeReturn=native['returnedR0'],candidateReturn=candidate['returnedR0'],nativeProviders=native['providedEvents'],candidateProviders=candidate['providedEvents'],nativeWrites=native['nonstackWrites'],candidateWrites=candidate['nonstackWrites'],rawProviderWordViewsDiffer=raw,orderedWriteViewsDiffer=writes);traces.append(result);cases.append(dict(profile=p['name'],actualTopReturns=2,independentlyModeled=nm['independentlyModeled'],traceSha256=c.sha(encoded(result))))
        except Exception as error:
            failed.append(dict(profile=p,error=str(error)));cases.append(dict(profile=p['name'],passed=False,error=str(error)))
    controls=[]
    for tag in ['mode','mmio']:
        wrong=ROOT/'nonmatching/overlay-lane/20261101-constructor509-controls'/tag/'source.c';bad,bp,code=compile_unit(wrong,tag);p=P.profiles()[1];result=M.Machine(original,p,code).run();rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError('509 wrong compiled returning control passed')
        controls.append(dict(tag=tag,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),compilation=bad,genuineLink=bp,actualTopReturns=1,actualNativeDependencyReturns=0,providedCalls=len(result['providedEvents']),rejected=True,rejection=rejection))
    services=[]
    for address,meta in sorted(original['providers'].items()):
        data,base=(original['arm'],M.BASE)if meta['module']=='main'else(original['overlay'],M.OVERLAY)
        services.append(dict(address=hex(address),processor='arm9',program='',moduleSha256=original['main'if meta['module']=='main'else'module']['sha256'],**meta,sha256=c.sha(data[address-base:address-base+meta['bytes']]),executedOriginalBody=False))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov005-constructor509-provider-domain-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],address=hex(M.ENTRY),mode='arm',extraWordQualification=dict(path=qualification.relative_to(ROOT).as_posix(),sha256=sha256(qualification),actualIsolatedNativeHelperReturns=40,providedCalls=0,notIncludedInCallerDependencyCounts=True),pointerConsumptionProof=dict(path='evidence/verification/ov005-constructor505-pointer-consumption-20261101.json',sha256=sha256(ROOT/'evidence/verification/ov005-constructor505-pointer-consumption-20261101.json')),nativeSpanSha256=c.sha(original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]),nativeBytes=M.SIZE,sourceCredit=0,exactBytes=0,matchedFunctions=0,draftedNativeBytes=M.SIZE,compiledNativeBytes=M.SIZE,candidate=row,genuineLink=link,explicitPreparedWordCounts={hex(k):v for k,v in COUNTS.items()},oracle=dict(attemptedPairs=len(P.profiles()),passedFinalEffectPairs=passed,actualTopReturns=passed*2,actualNativeDependencyReturns=0,providedCalls=providerCalls,serviceCatalogue=services,independentlyModeledPairs=independent,independentlyModeledActualTopReturns=independent*2,observedOwnCodeBytes=len(observed)*4,fullOwnFunctionCoverage=False,rawCallerWordViewDifferences=rawDifferences,orderedNonstackWriteTraceDifferences=writeDifferences,cases=cases,failed=failed,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov005_constructor509_machine_20261101.py'),modelSha256=sha256(ROOT/'ov005_constructor509_models_20261101.py'),limits=['Zero accepted source credit: linked C is1720 bytes but1679 same-offset bytes match; it is not exact','All22 external entry points are supplied deterministic service providers; no original callee orwhole-scene behavior is claimed','Original/candidate final ownRAM andmapped MMIO storage,result andservice call order are compared outside substituted code/stack','Independent native-instruction model covers every supplied own-effect profile; lower provider behavior remains synthetic','Declared prepared core words and ordered own writes compare; extra raw caller words are retained separately without claiming complete original ABI arity','Descriptor32-byte writes,clears,load handles,sizes andfinal service return are explicit synthetic contracts; other lower services have no effects','Mapped MMIO is ordinary Unicorn-backed storage; physical display/timing/hardware effects are not established','All cases require actual bounded return,stack andcallee-saved preservation,ARM mode andguarded own code extents','Generated source andGhidra exports remain hypotheses; no compiler object ororiginal binary is counted as reconstructed source'],reproductionCommand='python prove_ov005_constructor509_20261101.py')
    write_json(ROOT/'evidence/attempts/ov005-constructor509-provider-domain-20261101.json',report);print(json.dumps({k:report['oracle'][k]for k in['attemptedPairs','passedFinalEffectPairs','actualTopReturns','providedCalls','independentlyModeledPairs','observedOwnCodeBytes','rawCallerWordViewDifferences','orderedNonstackWriteTraceDifferences']}));print('failures',len(failed),failed[:2])
    if failed:raise ValueError('509 provider-domain comparison failures retained in report')

if __name__=='__main__':run()
