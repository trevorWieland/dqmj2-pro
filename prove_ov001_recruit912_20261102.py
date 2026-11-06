import gzip
import hashlib
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import match_runtime as C
import unicorn
from project import ROOT, configuration, read_json, write_json, sha256
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov001_recruit911_machine_20261102 as M
import ov001_recruit911_model_20261102 as G

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-recruit910/candidate'
WORK = ROOT / 'work/ol912-proof'


def build(source,name):
    C.WORK=WORK/name/'compile'
    rows,unused=C.compare(source,'ov001','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError(('912 compile failed',rows))
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'genuine'
    try:
        comparison=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],dict):raise
        comparison=error.args[0]
    body=(directory/'caller.bin').read_bytes()
    if len(body)!=904:raise ValueError('912 candidate would cross measured native extent')
    return dict(source=row,genuineLink=comparison,bodySha256=hashlib.sha256(body).hexdigest()),body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'} | dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3]!=(3,13,5) or unicorn.__version__!='2.1.4':raise ValueError('912 pinned runtime differs')
    for row in read_json(ROOT/'evidence/verification/ov001-recruit912-inputs-20261102.json')['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('912 input differs',row['path']))
    mainInfo,main,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    candidate,image=build(SOURCE/'source.c','candidate')
    if candidate['genuineLink'].get('exactCallerBytes'):raise ValueError('912 unexpected match; review separately')
    template=(SOURCE/'source.c').read_text()
    controls=[]
    for name,text in [('wrong-rng-threshold',template.replace(' < 0x80)', ' < 0x81)')),('wrong-counter-threshold',template.replace(' > 0x3CU)', ' > 0x3BU)'))]:
        if text==template:raise ValueError('912 wrong-C site absent')
        directory=ROOT/'nonmatching/overlay-lane/20261102-recruit912'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('912 frozen control differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE/'context.h').read_bytes())
        proof,wrong=build(source,name)
        controls.append(dict(name=name,proof=proof,image=wrong,actualDispatcherReturns=0,actualGetterReturns=0,rejected=0,positive=0))
    totals=dict(pairs=0,actualTopReturns=0,actualDispatcherReturns=0,actualGetterReturns=0,actualOriginalChildReturns=0,actualCandidateChildReturns=0,actualNativeRngReturns=0,actualNativeDivisionReturns=0,suppliedCalls=0)
    traces=[]
    pcs=set()
    for p in G.profiles():
        results=[]
        getterResults=[]
        failures=[]
        for name,body in [('native',None),('candidate',image)]+[(r['name'],r['image'])for r in controls]:
            vm=M.Machine(main,overlay,body,p)
            result=vm.run(M.ENTRY)
            getter=vm.run(M.GETTER)
            result['kind']=name
            getter['kind']=name
            results.append(result)
            getterResults.append(getter)
            failures.append(G.model(vm,result,getter))
        original,hypothesis=results[:2]
        if failures[0]or failures[1]:
            write_json(ROOT/'evidence/attempts/ov001-recruit912-model-rejected-20261102.json',dict(profile=p,failures=failures,results=list(map(compact,results)),getterResults=list(map(compact,getterResults))))
            raise ValueError(('912 model rejected',p['ordinal'],failures[:2]))
        differences=[k for k in ['stateHex','rngState','writes']if original[k]!=hypothesis[k]]
        if differences or original['registers'][0]!=hypothesis['registers'][0]:raise ValueError(('912 own effects differ',p['ordinal'],differences))
        firstStack=min(original['privateStackStart'],hypothesis['privateStackStart'])
        if not M.SP-0x1000<=firstStack<=M.SP:raise ValueError('912 stack bound')
        memories=[]
        for result in results[:2]:
            memory=bytearray(result['memory'])
            memory[firstStack-0x02000000:M.SP-0x02000000]=bytes(M.SP-firstStack)
            memory[M.CHILD-0x02000000:M.CHILD-0x02000000+904]=bytes(904)
            memories.append(memory)
            if any(M.CHILD<=row[0]<M.CHILD+904 for row in result['writes']):raise ValueError('912 writable substituted code storage')
        if memories[0]!=memories[1]:raise ValueError('912 observable RAM differs outside stack and immutable substituted code')
        totals['pairs']+=1
        totals['actualTopReturns']+=4
        totals['actualDispatcherReturns']+=2
        totals['actualGetterReturns']+=2
        totals['actualOriginalChildReturns']+=sum(row['entry']==hex(M.CHILD)for row in original['nativePhysicalReturns'])
        totals['actualCandidateChildReturns']+=sum(row['entry']==hex(M.CHILD)for row in hypothesis['nativePhysicalReturns'])
        for result in results[:2]:
            totals['actualNativeRngReturns']+=sum(row['entry']=='0x203d294'for row in result['nativePhysicalReturns'])
            totals['actualNativeDivisionReturns']+=sum(row['entry']=='0x2026350'for row in result['nativePhysicalReturns'])
        pcs.update(original['ownPcs'])
        for index,control in enumerate(controls):
            control['actualDispatcherReturns']+=1
            control['actualGetterReturns']+=1
            control['rejected'if failures[index+2]else'positive']+=1
        traces.append(dict(profile=p,results=list(map(compact,results)),getterResults=list(map(compact,getterResults)),modelFailures=failures,observableRamSha256=hashlib.sha256(memories[0]).hexdigest(),observedPrivateStackStart=firstStack,ignoredImmutableSubstitutedCode=dict(address=hex(M.CHILD),bytes=904),scratchDifferences=[i for i in [1,2,3,12]if original['registers'][i]!=hypothesis['registers'][i]],cpsrDiffers=original['cpsr']!=hypothesis['cpsr']))
    if any(not r['rejected']for r in controls):raise ValueError('912 no returning wrong-C rejection')
    for row in controls:del row['image']
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-recruit912-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,sourceCredit=0,canonicalMatchedBytes=0,canonicalMatchedFunctions=0,allPassed=True,romSha256=configuration()['romSha256'],module='ov001',processor='arm9',program='',mode='arm',address=hex(M.CHILD),nativeBytes=904,moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],candidate=candidate,totals=totals,negativeEvidence=controls,nativeOwnInstructionAddresses=sorted(pcs),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Nonmatching complete904-byte C body; canonical genuine match888/904. Only raw states10,30,42,60 and two fallback states of the child are behavior-qualified. No exact source/module/ROM credit.','Unmodified original260-byte dispatcher021FBD6C selects the child only through supplied u8[02239A14+0x0A]==14. Original parent calls original or independently linked C child at its904-byte canonical slot without changing the parent branch. No neighboring bytes are overwritten.','Original RNG0203D294 and division02026350 execute. Synthetic seeds cover every bounded RNG(256) result0..255, including threshold127/128; one advance and exact state write precedes child-state40/50 selection. All256 counter-byte representations are checked for each supported counter state. No services are provided.','Original24-byte021FBE70 getter is invoked afterward by the test driver as a separate bounded entry, not by the dispatcher. It returns02239ABC iff supplied raw u8+0x67 is nonzero; all256 byte values are covered. Child leaves this supplied gate unchanged. No automatic ordinary caller/recruitment or scene-validity chain is inferred from the driver order.','All4104 positive top returns are actual dispatcher/getter executions;2052 child completions are nested returns and counted separately as1026 original plus1026 candidate. RNG and division actual native returns512 each are separate dependencies; they are not added again to top counts. Wrong-control returns are separate.','Full8MiB RAM outside only measured private-stack union and the immutable substituted904-byte executable storage is compared. Any write to that code storage is rejected. Ordered writes, independent state/RNG model, actual return opcodes/SP/callee-saved GPRs and consumed input words are verified. Raw scratch/CPSR/LR remain in traces.','Selector initialization, other child states/service effects, scratch record construction/persistence, ordinary scene reachability and validity of future RNG state remain unresolved. Initial seed and selector/counter/gate fields are supplied test state. No Windows/Android execution or application edits.'])
    write_json(ROOT/'evidence/application/ov001-recruit912-behavior-20261102.json',report)
    print(dict(totals=totals,controls=[{k:r[k]for k in ['name','actualDispatcherReturns','actualGetterReturns','rejected','positive']}for r in controls],sourceCredit=0),flush=True)

if __name__=='__main__':execute()
