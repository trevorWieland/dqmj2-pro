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
import ov001_nextstage924_fixture_20261102 as F

SOURCE = ROOT / 'src/overlays/ov001_20261102_nextstage924'
WORK = ROOT / 'work/ol924-proof'


def build(source, name, origin=None):
    C.WORK = WORK / name / 'compile'
    rows, unused = C.compare(source, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compileFailed'):
        raise ValueError(('924 compiler failed', rows))
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
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('924 pinned runtime differs')
    pins=read_json(ROOT/'evidence/verification/ov001-nextstage924-inputs-20261102.json')
    for row in pins['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('924 input differs',row['path']))
    selected=read_json(ROOT/pins['acceptedSnapshot'])['functions']
    if any(r['processor']=='arm9'and r['program']==''and r['module']=='ov001'and max(r['address'],F.ENTRY)<min(r['address']+r['bytes'],F.ENTRY+296)for r in selected):raise ValueError('924 accepted overlap')
    mainInfo,arm,unused=measured_module('main')
    moduleInfo,overlay,unused=measured_module('ov001')
    match,body=build(SOURCE/'source.c','source')
    template=(SOURCE/'source.c').read_text()
    controls=[]
    images={}
    variants=[('wrong-return',template.replace('    return 0;', '    return 1;')),('wrong-counter-boundaries',template.replace('[1] < 40)', '[1] <= 40)').replace('[1] < 90)', '[1] <= 90)')),('wrong-builder-word',template.replace('native_fn_ov001_021fb214(*(u32 *)(native_data_ov001_02239a14 + 0x40));', 'native_fn_ov001_021fb214(*(u32 *)(native_data_ov001_02239a14 + 0x40) ^ 1U);'))]
    for index,(name,text)in enumerate(variants):
        if text==template:raise ValueError('924 control site absent')
        directory=ROOT/'nonmatching/overlay-lane/20261102-nextstage924-controls'/name
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('924 frozen control differs')
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
            write_json(ROOT/'evidence/attempts/ov001-nextstage924-model-rejected-20261102.json',dict(profile=p,failures=failures,results=list(map(compact,results))))
            raise ValueError(('924 independent model',p['ordinal'],failures[:2]))
        fields=['registers','cpsr','memory','stateHex','rngState','provided','writes','nativeEntries','nativePhysicalReturns','topReturn','ownPcs','steps']
        differences=[key for key in fields if results[0][key]!=results[1][key]]
        if differences:raise ValueError(('924 full physical state differs',p['ordinal'],differences))
        pcs.update(results[0]['ownPcs'])
        supplied+=sum(len(r['provided'])for r in results[:2])
        for index,control in enumerate(controls):
            control['actualTopReturns']+=1
            control['rejected'if failures[index+2]else'positive']+=1
        trace=dict(profile=p,results=[compact(r)|dict(completeRamSha256=hashlib.sha256(r['memory']).hexdigest())for r in results],modelFailures=failures,physicalDifferences=differences)
        raw=json.dumps(trace,sort_keys=True,separators=(',',':')).encode()
        cases.append(dict(ordinal=p['ordinal'],actualTopReturns=2,traceSha256=hashlib.sha256(raw).hexdigest()))
        traces.append(trace)
    if pcs!=set(range(F.ENTRY,F.ENTRY+292,4))or any(not r['rejected']for r in controls):raise ValueError('924 coverage/controls incomplete')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    artifact=ROOT/'evidence/generated/ov001-nextstage924-traces-20261102.json.gz'
    artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],matches=[match],canonicalMatchedFunctions=1,canonicalMatchedBytes=296,sourceCreditPendingIntegrator=296,allPassed=True,totals=dict(pairs=len(cases),actualTopReturns=len(cases)*2,actualNativeHelperReturns=0,suppliedCalls=supplied,independentModelPairs=len(cases)),allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allOrderedWritesEqual=True,allOwnCodeObserved=dict(codeBytes=292,literalBytes=4,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Readable ordinary C296-byte complete-span genuine match, pending integrator admission. No callee source or module/ROM credit.','Raw u8 state[02239A14+1] covers all256 values; wait status0/1/FFFFFFFF and actor raw words0/02540000/FFFFFFFF are supplied. Timer bounds, wait gate, exact ordered initialization/notification/actor-builder calls, selector15 write and unchanged RNG are independently modeled.','All lower services including FB214 are explicitly supplied with no memory effects and legal caller-saved/NZCV clobbers. This does not establish their full behavior or ordinary scene reachability. Every raw R0..R3 provider-entry word is retained and equal between original/C, including unconsumed words; no complete original formal arity is inferred from the selected contract subset.','All292 own instruction bytes observed; literal4 is a normal measured relocation. Full GPR/CPSR/RAM including stack, raw calls, writes, proper return opcode/SP/callee-saved state agree. Three whole-C controls properly return and reject independently.','Actual FB214 scratch prefix922 remains separate and is not falsely supplied as a complete returning constructor. No complete-record, persistence, role meaning, host/device or application claim.'])
    write_json(ROOT/'evidence/matches/ov001-20261102-nextstage924.json',report)
    print(dict(pairs=len(cases),actualTopReturns=len(cases)*2,matchedBytes=296,suppliedCalls=supplied,controls=[{k:r[k]for k in ['name','actualTopReturns','rejected','positive']}for r in controls]),flush=True)

if __name__=='__main__':main()
