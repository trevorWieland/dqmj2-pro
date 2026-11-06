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
import ov001_phase960_fixture_20261102 as F

SOURCE = ROOT / 'src/overlays/ov001_20261102_battle_phase959'
WORK = ROOT / 'work/ol961-proof'


def build(source, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('961 compiler failed', rows))
    row = rows[0]
    row['sourceDependencies'] = [dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(), sha256=sha256(source.with_name('context.h')))]
    directory = WORK / name / 'canonical'
    bindings = qualified_bindings(row)
    if origin is None:
        proof = validate(row, bindings, directory)
        return dict(**row, realLink=proof), (directory / 'caller.bin').read_bytes()
    try:
        comparison = validate(row, bindings, directory)
    except ValueError as error:
        if not error.args or not isinstance(error.args[0], dict):
            raise
        comparison = error.args[0]
    proof, body = link_private(row, bindings, directory, WORK / name / 'private', origin)
    return dict(source=row, canonicalComparison=comparison, privateLink=proof), body


def compact(result):
    return {key: value for key, value in result.items() if key != 'memory'}


def main():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('961 pinned runtime differs')
    pins=read_json(ROOT/'evidence/verification/ov001-nextstage961-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('961 input differs',row['path']))
    selected=read_json(ROOT/pins['acceptedSnapshot'])['functions']
    if any(r['processor']=='arm9'and r['program']==''and r['module']=='ov001'and max(r['address'],F.ENTRY)<min(r['address']+r['bytes'],F.ENTRY+624)for r in selected):raise ValueError('961 accepted overlap')
    mainInfo,arm,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    match,body=build(SOURCE/'source.c','source')
    template=(SOURCE/'source.c').read_text()
    controls=[]
    images={}
    variants=[('wrong-return',template.replace('    return 0U;', '    return 1U;')),('missing-default-domain',template.replace('else if (M2C_FIELD(native_data_ov001_02239a14, u8 *, 3) < 50) {','else {')),('wrong-byte-predicate',template.replace('native_fn_02041800() != 1','native_fn_02041800() == 0'))]
    for index,(name,text)in enumerate(variants):
        if text==template:raise ValueError('961 control site absent')
        directory=ROOT/'nonmatching/overlay-lane/20261102-nextstage961-controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('961 frozen control differs')
        source.write_text(text)
        source.with_name('context.h').write_bytes((SOURCE/'context.h').read_bytes())
        origin=0x02650000+index*0x2000
        proof,image=build(source,name,origin)
        images[origin]=image
        controls.append(dict(name=name,origin=origin,proof=proof,actualTopReturns=0,rejected=0,positive=0))
    traces=[]
    cases=[]
    pcs=set()
    supplied=0
    nativeReturns=0
    nativeLogicalEntries=0
    for p in F.profiles():
        results=[]
        failures=[]
        for kind,start in [('native',F.ENTRY),('source',F.ENTRY)]+[(r['name'],r['origin'])for r in controls]:
            installed=images|({F.ENTRY:body}if kind=='source'else{})
            vm=F.Machine(arm,overlay,installed,p)
            result=vm.run(start)
            result['kind']=kind
            results.append(result)
            failures.append(F.model(vm,result))
        if failures[0]or failures[1]:
            write_json(ROOT/'evidence/attempts/ov001-nextstage961-model-rejected-20261102.json',dict(profile=p,failures=failures,results=list(map(compact,results))))
            raise ValueError(('961 independent model',p['ordinal'],failures[:2]))
        fields=['registers','cpsr','memory','stateHex','rngState','provided','writes','nativeEntries','nativePhysicalReturns','topReturn','ownPcs','steps','tailEntries','actorHex']
        differences=[key for key in fields if results[0][key]!=results[1][key]]
        if differences:raise ValueError(('961 full physical state differs',p['ordinal'],differences))
        pcs.update(results[0]['ownPcs'])
        supplied+=sum(len(r['provided'])for r in results[:2])
        nativeReturns+=sum(len(r['nativePhysicalReturns'])for r in results[:2])
        nativeLogicalEntries+=sum(len(r['nativeEntries'])+len(r['tailEntries'])for r in results[:2])
        for index,control in enumerate(controls):
            control['actualTopReturns']+=1
            control['rejected'if failures[index+2]else'positive']+=1
        trace=dict(profile=p,results=[compact(r)|dict(completeRamSha256=hashlib.sha256(r['memory']).hexdigest())for r in results],modelFailures=failures,physicalDifferences=differences)
        raw=json.dumps(trace,sort_keys=True,separators=(',',':')).encode()
        cases.append(dict(ordinal=p['ordinal'],actualTopReturns=2,traceSha256=hashlib.sha256(raw).hexdigest()))
        traces.append(trace)
    if pcs!=set(range(F.ENTRY,F.ENTRY+616,4))or any(not r['rejected']for r in controls):raise ValueError('961 coverage/controls incomplete')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-nextstage961-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],matches=[match],canonicalMatchedFunctions=1,canonicalMatchedBytes=624,sourceCreditPendingIntegrator=624,allPassed=True,totals=dict(pairs=len(cases),actualTopReturns=len(cases)*2,actualNativeHelperReturns=nativeReturns,actualLogicalNativeEntries=nativeLogicalEntries,suppliedCalls=supplied,independentModelPairs=len(cases)),allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allOrderedWritesEqual=True,allOwnCodeObserved=dict(codeBytes=616,literalBytes=8,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Ordinary C624-byte complete-span genuine match, pending integrator admission. No callee/module/ROM credit.','Native default phase increment applies only below50; the historical unconditional default incorrectly changed inactive phases and phase55 count flow. Assignment-in-condition preserves the original unsigned-byte increment/store/narrowed comparison using ordinary C; prefix/wide-temporary/debug/space alternatives remain failures.','Raw phase+03 and flag+04 each cover all256 bytes; count+00 covers all256 values in phases40/55. Unsigned byte increments wrap modulo256 before comparisons. Context selector+0A becomes raw4 on this function closing path. Actor+324 and+358 byte writes and supplied resolver full-word slot arguments are independently modeled.','Actual main41800 wrapper and417F8 leaf read raw u8[020F6100+02] for0/1/255. A tail leaf entry is logged without a duplicate frame; its actual BX LR at417FC is counted once physically for the wrapper path. Logical wrapper+leaf entries are separate from physical returns. No RNG executes.','All other lower services/resolver/UI functions are supplied with legal caller-saved/NZCV clobbers and no memory effects. The synthetic actor is writable0x400bytes; no ordinary scene, actor membership, UI/resource/handle legality, complete original formal arity, persistence or record33 claim is made.','All616 own instruction bytes are observed, plus8 measured literal bytes. Complete registers/CPSR/RAM including stack, raw calls and writes agree; independent state/actor/call/nonstackRAM model passes. Whole wrong-C controls genuinely link at private nonoverlapping origins and properly return; inactive-path positives are retained.','No accepted/shared/application edits; zero source credit before integrator full-module/regression gates.'])
    write_json(ROOT/'evidence/matches/ov001-20261102-battle-state961.json',report)
    print(dict(pairs=len(cases),actualTopReturns=len(cases)*2,matchedBytes=624,suppliedCalls=supplied,controls=[{k:r[k]for k in ['name','actualTopReturns','rejected','positive']}for r in controls]),flush=True)

if __name__=='__main__':main()
