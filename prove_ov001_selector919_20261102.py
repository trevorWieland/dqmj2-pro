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
import ov001_selector917_machine_20261102 as M
import ov001_selector917_model_20261102 as G

SOURCE = ROOT / 'nonmatching/overlay-lane/20261102-selector918/cached-state-quad-copy'
WORK = ROOT / 'work/ol919-proof'


def build(source, name, origin):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('902 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'} | dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('919 pinned runtime differs')
    for row in read_json(ROOT/'evidence/verification/ov001-selector919-inputs-20261102.json')['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('919 input differs',row['path']))
    mainInfo,main,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    candidate,image=build(SOURCE/'source.c','candidate',0x02650000)
    if candidate['canonicalComparison'].get('exactCallerBytes'):raise ValueError('919 unexpectedly exact; review separately')
    images={0x02650000:image}
    controls=[]
    template=(SOURCE/'source.c').read_text()
    for index,(name,text)in enumerate([('wrong-equality',template.replace('draw < state->field_26','draw <= state->field_26')),('wrong-wait-gate',template.replace('native_fn_0205fd60() == 0','native_fn_0205fd60() != 0'))]):
        if text==template:raise ValueError('919 wrong-C site absent')
        directory=ROOT/'nonmatching/overlay-lane/20261102-selector919'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('919 frozen control differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE/'context.h').read_bytes())
        origin=0x02652000+index*0x2000
        proof,wrong=build(source,name,origin)
        images[origin]=wrong
        controls.append(dict(name=name,origin=origin,proof=proof,actualTopReturns=0,rejected=0,positive=0))
    totals=dict(pairs=0,actualTopReturns=0,actualWaitGetterReturns=0,actualNativeRngReturns=0,actualNativeDivisionReturns=0,suppliedNotificationCalls=0,selector13Pairs=0,selector14Pairs=0,busyPairs=0)
    traces=[]
    pcs=set()
    for p in G.profiles():
        results=[]
        failures=[]
        for name,entry in [('native',M.SELECTOR),('candidate',0x02650000)]+[(r['name'],r['origin'])for r in controls]:
            vm=M.Machine(main,overlay,images,p)
            result=vm.run(entry)
            result['kind']=name
            results.append(result)
            failures.append(G.model(vm,result))
        original,hypothesis=results[:2]
        if failures[0]or failures[1]:
            write_json(ROOT/'evidence/attempts/ov001-selector919-model-rejected-20261102.json',dict(profile=p,failures=failures,results=list(map(compact,results))))
            raise ValueError(('919 model rejected',p['ordinal'],failures[:2]))
        differences=[k for k in ['stateHex','rngState','writes']if original[k]!=hypothesis[k]]
        if G.logical_providers(original)!=G.logical_providers(hypothesis):differences.append('consumed notification inputs')
        if differences or original['registers'][0]!=hypothesis['registers'][0]:raise ValueError(('919 own effects differ',p['ordinal'],differences))
        firstStack=min(original['privateStackStart'],hypothesis['privateStackStart'])
        if not M.SP-0x1000<=firstStack<=M.SP:raise ValueError('919 stack bound')
        memories=[]
        for result in results[:2]:
            memory=bytearray(result['memory'])
            memory[firstStack-0x02000000:M.SP-0x02000000]=bytes(M.SP-firstStack)
            memories.append(memory)
        if memories[0]!=memories[1]:raise ValueError('919 observable RAM outside private stack differs')
        totals['pairs']+=1
        totals['actualTopReturns']+=2
        if p['busy']!=0:totals['busyPairs']+=1
        elif p['firstDraw']<p['threshold']:totals['selector13Pairs']+=1
        else:totals['selector14Pairs']+=1
        for result in results[:2]:
            totals['actualWaitGetterReturns']+=sum(r['entry']=='0x205fd60'for r in result['nativePhysicalReturns'])
            totals['actualNativeRngReturns']+=sum(r['entry']=='0x203d294'for r in result['nativePhysicalReturns'])
            totals['actualNativeDivisionReturns']+=sum(r['entry']=='0x2026350'for r in result['nativePhysicalReturns'])
            totals['suppliedNotificationCalls']+=len(result['provided'])
        pcs.update(original['ownPcs'])
        for index,control in enumerate(controls):
            control['actualTopReturns']+=1
            control['rejected'if failures[index+2]else'positive']+=1
        traces.append(dict(profile=p,results=list(map(compact,results)),modelFailures=failures,observedPrivateStackStart=firstStack,observableRamSha256=hashlib.sha256(memories[0]).hexdigest(),scratchDifferences=[i for i in [1,2,3,12]if original['registers'][i]!=hypothesis['registers'][i]],cpsrDiffers=original['cpsr']!=hypothesis['cpsr']))
    if any(not r['rejected']for r in controls):raise ValueError('919 control did not reject')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-selector919-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,canonicalMatchedBytes=0,canonicalMatchedFunctions=0,romSha256=configuration()['romSha256'],module='ov001',processor='arm9',program='',mode='arm',address=hex(M.SELECTOR),nativeBytes=496,moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],candidate=candidate,totals=totals,negativeEvidence=controls,nativeOwnInstructionAddresses=sorted(pcs),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Complete ordinary496-byte source hypothesis genuinely compiles/links to504 bytes; canonical mismatch remains failure and zero source credit. Candidate and whole-C controls execute at nonoverlapping private origins, preserving neighboring FB1DC bytes.','Only raw subphase u8[02239A14+0x0F]==0x6E is behavior-qualified. Original0205FD60 reads supplied u32[021B8E84]; nonzero suppresses the RNG/state changes. When zero, actual RNG(1000)/division execute and signed32 result is compared with signed16[02239A14+0x26]. Selector u8+0x0A becomes13 for LT,14 for GE; notification(0,1) precedes clearing subphase+0x0F.','Synthetic inverse-LCG seeds cover all1000 outputs plus threshold boundaries across signed16 thresholds[-32768,-1,0,1,500,999,1000,32767], and two nonzero wait-word values. Seed/threshold/subphase/wait-word are initialized test state, not observed future scene state.','Only021E3544 notification is supplied, with exact two consumed caller words and legal caller-saved GPR/NZCV clobbers and no memory effects. Its original wrapper forwards those words with02238AD4 to021D9494; downstream behavior remains unqualified. Original wait getter/RNG/divider execute.','Full8MiB RAM outside only measured private-stack union, ordered writes, consumed inputs, raw return words and actual return opcodes/SP/callee-saved GPRs are checked. Raw unused service words/scratch/CPSR/LR remain in traces.','Other full-source states, actual scheduler reachability, service effects, record construction/persistence and role meanings of13/14 remain unproved. Separate912 proof covers later dispatcher/child RNG(256) under supplied selector14/child state30; this packet does not silently join those initialized conditions. No source/module/ROM completion or host/device claim.'])
    write_json(ROOT/'evidence/application/ov001-selector919-behavior-20261102.json',report)
    print(dict(totals=totals,controls=[{k:r[k]for k in ['name','actualTopReturns','rejected','positive']}for r in controls],sourceCredit=0),flush=True)

if __name__=='__main__':execute()
