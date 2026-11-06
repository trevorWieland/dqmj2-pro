import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,sha256,write_json,configuration
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
COUNTS={0x02063F6C:0,0x02002C98:3,0x02008C58:3,0x0201D444:2,0x0203CC2C:2,0x020481B8:3,0x0202A8E0:1,0x02048308:0,0x0202A498:2,0x02004E58:3,0x02004B58:3,0x02004C18:3,0x02004CD8:3,0x021DDD60:2,0x021DA838:1,0x02048A94:2,0x02048A9C:2,0x02048A60:3,0x02048644:3,0x02084924:10,0x02049FFC:1,0x020633B0:0,0x02046AF4:6,0x021DDEC4:2,0x021DDDEC:4,0x020877BC:4,0x02048034:2,0x020BF218:0,0x021E5FF8:0}
import ov005_details516_machine_20261101 as M
import ov005_details516_models_20261101 as P
WORK=ROOT/'work/ol516-proof'
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-details516/source.c'


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov005','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('516 candidate did not compile')
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
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('516 pinned runtime differs')
    for item in json.loads((ROOT/'evidence/verification/ov005-details516-inputs-20261101.json').read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('516 frozen input differs',item['path']))
    original=M.inputs();row,link,body=compile_unit(SOURCE,'candidate');traces=[];cases=[];observed=set();passed=0;independent=0;providerCalls=0;rawDifferences=0;writeDifferences=0;nativeReturns=0;failed=[]
    for p in P.profiles():
        try:
            native=M.Machine(original,p).run();candidate=M.Machine(original,p,body).run();native['extent']=M.SIZE;candidate['extent']=len(body);nm=P.model(native);cm=P.model(candidate);nativeReturns+=len(native['nativeReturns'])+len(candidate['nativeReturns'])
            if nm!=cm:raise ValueError('516 independent original/candidate models differ')
            if not equal_effect(native,candidate):raise ValueError('516 original/candidate final effect orcall order differs')
            observed.update(native['ownObserved']);passed+=1;independent+=int(nm['independentlyModeled']);providerCalls+=len(native['providedEvents'])+len(candidate['providedEvents']);raw=sum(x['rawCallerWords']!=y['rawCallerWords']for x,y in zip(native['providedEvents'],candidate['providedEvents']));rawDifferences+=raw
            for x,y in zip(native['providedEvents'],candidate['providedEvents']):
                count=COUNTS[x['address']]
                if(x['rawCallerWords']+x['stackWords'])[:count]!=(y['rawCallerWords']+y['stackWords'])[:count]:raise ValueError(('516 prepared core words differ',hex(x['address'])))
            writes=native['nonstackWrites']!=candidate['nonstackWrites'];writeDifferences+=writes
            if writes:raise ValueError('516 complete ordered writes differ')
            result=dict(profile=p,independentModel=nm,nativeInstructions=native['instructions'],candidateInstructions=candidate['instructions'],nativeReturn=native['returnedR0'],candidateReturn=candidate['returnedR0'],nativeProviders=native['providedEvents'],candidateProviders=candidate['providedEvents'],nativeWrites=native['nonstackWrites'],candidateWrites=candidate['nonstackWrites'],nativeDependencyReturns=native['nativeReturns'],candidateDependencyReturns=candidate['nativeReturns'],nativeHelperInputViews=native['helperWords'],candidateHelperInputViews=candidate['helperWords'],rawProviderWordViewsDiffer=raw,orderedWriteViewsDiffer=writes);traces.append(result);cases.append(dict(profile=p['name'],actualTopReturns=2,independentlyModeled=nm['independentlyModeled'],traceSha256=c.sha(encoded(result))))
        except Exception as error:
            failed.append(dict(profile=p,error=str(error)));cases.append(dict(profile=p['name'],passed=False,error=str(error)))
    controls=[]
    for tag in ['state','cap']:
        wrong=ROOT/'nonmatching/overlay-lane/20261101-details516-controls'/tag/'source.c';bad,bp,code=compile_unit(wrong,tag);p=P.profiles()[1];result=M.Machine(original,p,code).run();rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError('516 wrong compiled returning control passed')
        controls.append(dict(tag=tag,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),compilation=bad,genuineLink=bp,actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),providedCalls=len(result['providedEvents']),rejected=True,rejection=rejection))
    services=[]
    for address,meta in sorted(original['providers'].items()):
        data,base=(original['arm'],M.BASE)if meta['module']=='main'else(original['overlay'],M.OVERLAY)
        services.append(dict(address=hex(address),processor='arm9',program='',moduleSha256=original['main'if meta['module']=='main'else'module']['sha256'],**meta,sha256=c.sha(data[address-base:address-base+meta['bytes']]),executedOriginalBody=address==0x02008C58,originalExecutionCondition='length4 native;length0x80000 supplied'if address==0x02008C58 else'not executed'))
    nativeFunctions=[]
    for address,meta in sorted(original['ranges'].items()):
        if address==M.ENTRY:continue
        data,base=(original['arm'],M.BASE)if meta['module']=='main'else(original['overlay'],M.OVERLAY)
        nativeFunctions.append(dict(address=hex(address),processor='arm9',program='',moduleSha256=original['main'if meta['module']=='main'else'module']['sha256'],**meta,sha256=c.sha(data[address-base:address-base+meta['bytes']]),sourceCredit=0))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov005-details516-provider-domain-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov005',moduleSha256=original['module']['sha256'],address=hex(M.ENTRY),mode='arm',nativeSpanSha256=c.sha(original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]),nativeBytes=M.SIZE,sourceCredit=0,exactBytes=0,matchedFunctions=0,draftedNativeBytes=M.SIZE,compiledNativeBytes=M.SIZE,candidate=row,genuineLink=link,explicitPreparedWordCounts={hex(k):v for k,v in COUNTS.items()},oracle=dict(attemptedPairs=len(P.profiles()),passedFinalEffectPairs=passed,actualTopReturns=passed*2,actualNativeDependencyReturns=nativeReturns,providedCalls=providerCalls,serviceCatalogue=services,executedOriginalFunctionCatalogue=nativeFunctions,actualReturnAndFrameRequired=True,independentlyModeledPairs=independent,independentlyModeledActualTopReturns=independent*2,observedOwnCodeBytes=len(observed)*4,fullOwnFunctionCoverage=False,rawCallerWordViewDifferences=rawDifferences,orderedNonstackWriteTraceDifferences=writeDifferences,cases=cases,failed=failed,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov005_details516_machine_20261101.py'),modelSha256=sha256(ROOT/'ov005_details516_models_20261101.py'),limits=['Zero accepted source credit: linked C is1612 bytes against1616 native bytes with438 matching,not exact','Three native4-byte clears andthe native633B0 literal getter execute percaller; VRAMclear andremaining lower effects are supplied,with no scene claim','Original/candidate final ownRAM andmapped MMIO storage,result andservice call order are compared outside substituted code/stack','Independent native-instruction model covers every supplied profile; lower provider behavior remains synthetic','Declared prepared core words,including sixstack words for84924 andtwo for46AF4,compare; extra raw registers remain qualified separately without formal-arity claims','Five32-byte descriptor writes,five load/size returns,nine mapped handle returns,64-byte formatting writes andclears are supplied contracts; other lower effects are absent','Mapped MMIO is ordinary Unicorn-backed storage; physical display/timing/hardware effects are not established','All cases require actual bounded return,stack andcallee-saved preservation,ARM mode andguarded own code extents','Generated source andGhidra exports remain hypotheses; no compiler object ororiginal binary is counted as reconstructed source'],reproductionCommand='python prove_ov005_details516_20261101.py')
    write_json(ROOT/'evidence/attempts/ov005-details516-provider-domain-20261101.json',report);print(json.dumps({k:report['oracle'][k]for k in['attemptedPairs','passedFinalEffectPairs','actualTopReturns','providedCalls','independentlyModeledPairs','observedOwnCodeBytes','rawCallerWordViewDifferences','orderedNonstackWriteTraceDifferences']}));print('nativeDependencyReturns',nativeReturns);print('failures',len(failed),failed[:2])
    if failed:raise ValueError('516 provider-domain comparison failures retained in report')

if __name__=='__main__':run()
