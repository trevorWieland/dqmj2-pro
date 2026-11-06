import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
import ov003_config526_machine_20261101 as M
import ov003_config526_models_20261101 as P
WORK=ROOT/'work/ol526-proof'
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-config526/source.c'


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov003','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('526 candidate compilation failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];out=WORK/name/'linked'
    try:proof=validate(row,qualified_bindings(row),out)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(out/'caller.bin').read_bytes()



def regions(original,observed):
    native=original['overlay'];decoder=M.Cs(M.CS_ARCH_ARM,M.CS_MODE_ARM);missing=set(range(M.ENTRY,M.ENTRY+M.SIZE,4))-observed;literals={}
    for address in sorted(observed):
        ins=next(decoder.disasm(native[address-M.OVERLAY:address-M.OVERLAY+4],address));match=re.search(r'\[pc(?:, #(-?(?:0x[0-9a-f]+|[0-9]+)))?\]',ins.op_str)
        if not ins.mnemonic.startswith('ldr')or not match:continue
        target=address+8+(int(match[1],0)if match[1]else 0)
        if target in missing:literals.setdefault(target,[]).append(address)
    return dict(observedInstructionAddresses=[hex(a)for a in sorted(observed)],observedCodeBytes=len(observed)*4,unobservedWords=[hex(a)for a in sorted(missing)],referencedLiteralWords=[dict(address=hex(a),value=hex(int.from_bytes(native[a-M.OVERLAY:a-M.OVERLAY+4],'little')),fixedPcRelativeReadInstructions=[hex(v)for v in refs])for a,refs in sorted(literals.items())],classifiedLiteralBytes=len(literals)*4,unclassifiedBytes=len(missing-set(literals))*4,allNativeInstructionAddressesObserved=missing==set(literals),exhaustivePathCoverage=False)


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('526 runtime differs')
    for item in json.loads((ROOT/'evidence/verification/ov003-config526-inputs-20261101.json').read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('526 frozen input differs',item['path']))
    original=M.inputs()
    if original['main']['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or original['module']['sha256']!='efbcc417d3e4b22c11f87bb58ee9fbbf3df4b12c285122d322eb3f9257607260':raise ValueError('526 measured modules differ')
    row,link,body=compile_unit(SOURCE,'candidate');traces=[];cases=[];failed=[];observed=set();passed=0;nativeReturns=0;providers=0;rawDifferences=0;writeDifferences=0;extraDifferences=[]
    for p in P.profiles():
        try:
            a=M.Machine(original,p).run();b=M.Machine(original,p,body).run();ma=P.model(a,original);mb=P.model(b,original)
            if ma!=mb:raise ValueError('526 original/candidate independent models differ')
            observed.update(a['ownObserved']);passed+=1;nativeReturns+=len(a['nativeReturns'])+len(b['nativeReturns']);providers+=len(a['providedEvents'])+len(b['providedEvents']);raw=sum(x['rawCallerWords']!=y['rawCallerWords']for x,y in zip(a['providedEvents'],b['providedEvents']));rawDifferences+=raw;writes=a['nonstackWrites']!=b['nonstackWrites'];writeDifferences+=writes
            for x,y in zip(a['providedEvents'],b['providedEvents']):
                if x['rawCallerWords']!=y['rawCallerWords']:extraDifferences.append(dict(profile=p['name'],address=hex(x['address']),changedWords=[i for i in range(4)if x['rawCallerWords'][i]!=y['rawCallerWords'][i]]))
            trace=dict(profile=p,independentModel=ma,nativeInstructions=a['instructions'],candidateInstructions=b['instructions'],nativeProviders=a['providedEvents'],candidateProviders=b['providedEvents'],nativeReturns=a['nativeReturns'],candidateReturns=b['nativeReturns'],nativeWrites=a['nonstackWrites'],candidateWrites=b['nonstackWrites'],nativePhysicalR0=a['returnedR0'],candidatePhysicalR0=b['returnedR0'],rawCallerWordDifferences=raw,orderedNonstackWritesDiffer=writes);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=len(a['nativeReturns'])+len(b['nativeReturns']),providedCalls=len(a['providedEvents'])+len(b['providedEvents']),traceSha256=c.sha(encoded(trace)),orderedNonstackWritesDiffer=writes))
        except Exception as error:failed.append(dict(profile=p,error=str(error)))
    controls=[]
    for name,index in[('configuration',0),('key',6)]:
        source=ROOT/'nonmatching/overlay-lane/20261101-config526-controls'/name/'source.c';bad,bp,code=compile_unit(source,name);p=P.profiles()[index];result=M.Machine(original,p,code).run();rejection=None
        try:P.model(result,original)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('526 compiled returning control passed',name))
        controls.append(dict(name=name,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,genuineLink=bp,actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),providedCalls=len(result['providedEvents']),rejected=True,rejection=rejection))
    functions=[]
    for category,entries in[('actualNative',original['ranges']),('supplied',original['providers'])]:
        for address,meta in sorted(entries.items()):
            data,base=(original['arm'],M.BASE)if meta['module']=='main'else(original['overlay'],M.OVERLAY);functions.append(dict(category=category,address=hex(address),processor='arm9',program='',moduleSha256=original['main'if meta['module']=='main'else'module']['sha256'],**meta,sha256=c.sha(data[address-base:address-base+meta['bytes']]),sourceCredit=0))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov003-config526-provider-domain-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov003',moduleSha256=original['module']['sha256'],address=hex(M.ENTRY),mode='arm',nativeSpanSha256=c.sha(original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]),nativeBytes=M.SIZE,regionClassification=regions(original,observed),sourceCredit=0,exactBytes=0,matchedFunctions=0,draftedNativeBytes=M.SIZE,compiledNativeBytes=M.SIZE,candidate=row,genuineLink=link,nativeIdentities=functions,derivedAddresses={k:hex(original[k])for k in['keys','kind','config']},setterAddresses=[hex(a)for a in original['setters']],explicitPreparedWordCounts={hex(k):v for k,v in M.PROVIDERS.items()},oracle=dict(attemptedPairs=len(P.profiles()),passedFinalEffectPairs=passed,actualTopReturns=passed*2,actualNativeDependencyReturns=nativeReturns,providedCalls=providers,independentlyModeledPairs=passed,observedOwnCodeBytes=len(observed)*4,fullOwnFunctionCoverage=regions(original,observed)['allNativeInstructionAddressesObserved'],rawCallerWordViewDifferences=rawDifferences,rawDifferenceScope=extraDifferences,orderedNonstackWriteTraceDifferences=writeDifferences,orderedWriteEqualityClaim=False,cases=cases,failed=failed,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0,rejectedInitialByteTableModel=dict(path='evidence/attempts/ov003-config525-initial-model-20261101.json',sha256=sha256(ROOT/'evidence/attempts/ov003-config525-initial-model-20261101.json'),sourceAlreadyHadCorrectU16Table=True)),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov003_config526_machine_20261101.py'),modelSha256=sha256(ROOT/'ov003_config526_models_20261101.py'),limits=['Linked ordinary C is772 bytes against756 native bytes and545 same-offset matches; zero exact/source credit','Every positive case requires actual bounded ARM return,SP/callee-saved restoration and independently modeled complete nonstack RAM plusphysicalR0','Actual original key/kind/config getters andsix full-word setters execute; five rendering/notification/selection entries remain deterministic supplied services','Table021E038C isunsigned16 indexed bylow8 kind;initial independent byte model was wrong,whilefresh C declaration was alreadycorrect; failure is retained','Initial kind dispatch isfull32; confirm dispatch truncates tolow8; supplied renderer maymutate thekindword beforeconfirm reload','The supplied selection helper writes a declared synthetic nextword; tablelookup uses theoldlow8 kind; no original selection-cycle orscene behavior claim','Twelve cases have different ownRAM store order while final memory andall independent effect contracts agree; exact intermediate write-order equivalence isnot claimed','Twelve raw extra caller-word differences are retained; compared prepared-word views are caller-specific evidence,not complete callee formal types','The24-byte configuration stack object andsix values compare at theprovider boundary; raw stack addresses are retained without treating allocation identity as a semantic difference','Full32 kinds andlow8 tableindices beyond0..3 use explicitlymapped synthetic data,not valid-menu orsaved-record meaning','All classified own instruction addresses are observed across thecorpus; literal classification uses fixedPC-relative load references; no exhaustive path proof','No original lower rendering/audio/selection behavior,concurrency,game reachability orapplication policy is established; no app edits'],reproductionCommand='python prove_ov003_config526_20261101.py')
    write_json(ROOT/'evidence/attempts/ov003-config526-provider-domain-20261101.json',report);print(json.dumps({k:report['oracle'][k]for k in['attemptedPairs','passedFinalEffectPairs','actualTopReturns','actualNativeDependencyReturns','providedCalls','observedOwnCodeBytes','rawCallerWordViewDifferences','orderedNonstackWriteTraceDifferences']}));print('failed',len(failed),failed[:2])
    if failed:raise ValueError('526 candidate/model failures retained')

if __name__=='__main__':run()
