import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,sha256,write_json,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov005_controller500_machine_20261101 as M
import ov005_controller500_models_20261101 as P
WORK=ROOT/'work/ol500-proof'
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-controller500/source.c'


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov005','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('500 candidate did not compile')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];out=WORK/name/'linked'
    try:proof=validate(row,qualified_bindings(row),out)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(out/'caller.bin').read_bytes()


def equal_effect(a,b):
    cut=M.STACK-M.BASE;begin=M.ENTRY-M.BASE;end=begin+max(M.SIZE,a['extent'],b['extent'])
    return a['after'][:begin]==b['after'][:begin]and a['after'][end:cut-65536]==b['after'][end:cut-65536]and a['after'][cut+4096:]==b['after'][cut+4096:]and a['ioAfter']==b['ioAfter']and a['returnedR0']==b['returnedR0']and[a['address']for a in a['providedEvents']]==[b['address']for b in b['providedEvents']]


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('500 pinned runtime differs')
    for item in json.loads((ROOT/'evidence/verification/ov005-controller500-inputs-20261101.json').read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('500 frozen input differs',item['path']))
    original=M.inputs();row,link,body=compile_unit(SOURCE,'candidate');traces=[];cases=[];observed=set();passed=0;independent=0;providerCalls=0;rawDifferences=0;writeDifferences=0;failed=[]
    for p in P.profiles():
        try:
            native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();native['extent']=M.SIZE;candidate['extent']=len(body);nm=P.model(native);cm=P.model(candidate)
            if nm!=cm:raise ValueError('500 independent original/candidate models differ')
            if not equal_effect(native,candidate):raise ValueError('500 original/candidate final effect orcall order differs')
            observed.update(native['ownObserved']);passed+=1;independent+=int(nm['independentlyModeled']);providerCalls+=len(native['providedEvents'])+len(candidate['providedEvents']);raw=sum(x['rawCallerWords']!=y['rawCallerWords']for x,y in zip(native['providedEvents'],candidate['providedEvents']));rawDifferences+=raw
            if raw:raise ValueError('500 complete raw caller word views differ')
            writes=native['nonstackWrites']!=candidate['nonstackWrites'];writeDifferences+=writes
            if writes:raise ValueError('500 complete ordered writes differ')
            result=dict(profile=p,independentModel=nm,nativeInstructions=native['instructions'],candidateInstructions=candidate['instructions'],nativeReturn=native['returnedR0'],candidateReturn=candidate['returnedR0'],nativeProviders=native['providedEvents'],candidateProviders=candidate['providedEvents'],nativeWrites=native['nonstackWrites'],candidateWrites=candidate['nonstackWrites'],rawProviderWordViewsDiffer=raw,orderedWriteViewsDiffer=writes);traces.append(result);cases.append(dict(profile=p['name'],actualTopReturns=2,independentlyModeled=nm['independentlyModeled'],traceSha256=c.sha(encoded(result))))
        except Exception as error:
            failed.append(dict(profile=p,error=str(error)));cases.append(dict(profile=p['name'],passed=False,error=str(error)))
    controls=[]
    for tag in ['footer','mmio']:
        wrong=ROOT/'nonmatching/overlay-lane/20261101-controller500-controls'/tag/'source.c';bad,bp,code=compile_unit(wrong,tag);p=next(p for p in P.profiles()if p['state']==(19 if tag=='footer'else 25)and p['name'].endswith('inputs2'));result=M.Machine(original,p,code).run();rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError('500 wrong compiled returning control passed')
        controls.append(dict(tag=tag,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),compilation=bad,genuineLink=bp,actualTopReturns=1,actualNativeDependencyReturns=0,providedCalls=len(result['providedEvents']),rejected=True,rejection=rejection))
    services=[]
    for address,meta in sorted(original['providers'].items()):
        data,base=(original['arm'],M.BASE)if meta['module']=='main'else(original['overlay'],M.OVERLAY)
        services.append(dict(address=hex(address),processor='arm9',program='',moduleSha256=original['main'if meta['module']=='main'else'module']['sha256'],**meta,sha256=c.sha(data[address-base:address-base+meta['bytes']]),executedOriginalBody=False))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov005-controller500-provider-domain-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],address=hex(M.ENTRY),mode='arm',nativeSpanSha256=c.sha(original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]),nativeBytes=M.SIZE,sourceCredit=0,exactBytes=0,matchedFunctions=0,draftedNativeBytes=M.SIZE,compiledNativeBytes=M.SIZE,candidate=row,genuineLink=link,oracle=dict(attemptedPairs=len(P.profiles()),passedFinalEffectPairs=passed,actualTopReturns=passed*2,actualNativeDependencyReturns=0,providedCalls=providerCalls,serviceCatalogue=services,independentlyModeledPairs=independent,independentlyModeledActualTopReturns=independent*2,observedOwnCodeBytes=len(observed)*4,fullOwnFunctionCoverage=False,rawCallerWordViewDifferences=rawDifferences,orderedNonstackWriteTraceDifferences=writeDifferences,cases=cases,failed=failed,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov005_controller500_machine_20261101.py'),modelSha256=sha256(ROOT/'ov005_controller500_models_20261101.py'),limits=['Zero accepted source credit: linked C is2324 bytes against2328 native bytes,not exact','All45 external entry points are supplied deterministic service providers; no original callee orwhole-scene behavior is claimed','Original/candidate final ownRAM andmapped MMIO storage,result andservice call order are compared outside substituted code/stack','Independent native-instruction models cover selected states only; other cases are original/candidate effect comparisons','Complete raw R0-R3 service-word views and ordered writes must equal in every passed pair; this does not establish native callee formal arity orlower behavior','Service pointer returns,busy/raw-mode/progress/kind results andno lower side effects are explicit synthetic contracts','Mapped MMIO is ordinary Unicorn-backed storage; physical display/timing/hardware effects are not established','All cases require actual bounded return,stack andcallee-saved preservation,ARM mode andguarded own code extents','Generated source andGhidra exports remain hypotheses; no compiler object ororiginal binary is counted as reconstructed source'],reproductionCommand='python prove_ov005_controller500_20261101.py')
    write_json(ROOT/'evidence/attempts/ov005-controller500-provider-domain-20261101.json',report);print(json.dumps({k:report['oracle'][k]for k in['attemptedPairs','passedFinalEffectPairs','actualTopReturns','providedCalls','independentlyModeledPairs','observedOwnCodeBytes','rawCallerWordViewDifferences','orderedNonstackWriteTraceDifferences']}));print('failures',len(failed),failed[:2])
    if failed:raise ValueError('500 provider-domain comparison failures retained in report')

if __name__=='__main__':run()
