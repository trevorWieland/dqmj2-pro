import gzip
import hashlib
import json
import sys

import match_runtime as C
import unicorn
from project import ROOT, read_json, write_json, sha256, configuration
from link_runtime_unit import measured_module, validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import wave20261102_battle_fifth_fixture01 as F

LANE=ROOT/'evidence/lanes/parallel-wave20261102/battle-fifth'
WORK=ROOT/'work/parallel-wave20261102/battle-fifth/packet01'
SOURCE=ROOT/'src/ov001/parallel_wave20261102/battle-fifth/packet01/021dff00/native_ov001_021dff00.c'


def build(source,label,origin=None):
    directory=WORK/label
    C.WORK=directory/'compile'
    rows,unused=C.compare(source,'ov001','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):
        raise ValueError(('Battle fifth compiler refused',rows))
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    bindings=qualified_bindings(row)
    if origin is None:
        proof=validate(row,bindings,directory/'canonical')
        row.update(realLink=proof,nativeSymbolEntries=bindings)
        return row,(directory/'canonical/caller.bin').read_bytes()
    try:
        comparison=validate(row,bindings,directory/'canonical')
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],dict):
            raise
        comparison=error.args[0]
    if comparison.get('exactCallerBytes'):
        raise ValueError('Whole-source negative control unexpectedly exact')
    proof,body=link_private(row,bindings,directory/'canonical',directory/'private',origin)
    return dict(source=row,canonicalComparison=comparison,privateLink=proof),body


def compact(result):
    return{key:value for key,value in result.items()if key!='memory'}|dict(completeRamSha256=hashlib.sha256(result['memory']).hexdigest())


def main():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':
        raise ValueError('Battle fifth pinned runtime differs')
    inputs=LANE/'packet01-inputs.json'
    for pin in read_json(inputs)['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:
            raise ValueError(('Battle fifth frozen input changed',pin['path']))
    match,body=build(SOURCE,'source')
    template=SOURCE.read_text()
    actor_line=next(line for line in template.splitlines()if 'native_fn_ov001_021d7e80('in line)
    bad_actor_line=actor_line.replace('(void *) ','(void *) (255U & ').replace(');','));')
    changes=[('wrong-return',template.replace('return 0U;','return 1U;')),('wrong-actor-word',template.replace(actor_line,bad_actor_line)),('wrong-label-signedness',template.replace('(s8) native_fn_0205d790','(u8) native_fn_0205d790'))]
    images={}
    controls=[]
    for ordinal,(label,text)in enumerate(changes):
        if text==template:
            raise ValueError('Battle fifth negative source site missing')
        directory=WORK/'controls'/label
        directory.mkdir(parents=True,exist_ok=True)
        source=directory/SOURCE.name
        source.write_text(text)
        source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        origin=0x02650000+ordinal*0x2000
        proof,image=build(source,label,origin)
        images[origin]=image
        controls.append(dict(label=label,origin=origin,proof=proof,rejected=0,positive=0,actualTopReturns=0))
    main_info,main,unused=measured_module('main')
    module_info,overlay,unused=measured_module('ov001')
    traces=[]
    pcs=set()
    calls=0
    for profile in F.profiles():
        original_vm=F.Machine(main,overlay,images,profile)
        original=original_vm.run(F.ENTRY)
        source_vm=F.Machine(main,overlay,images|{F.ENTRY:body},profile)
        source=source_vm.run(F.ENTRY)
        model_errors=[F.model(original_vm,original),F.model(source_vm,source)]
        differences=[key for key in ['registers','cpsr','stateHex','writes','provided','memory','rngState','nativeEntries','nativePhysicalReturns','topReturn']if original[key]!=source[key]]
        if any(model_errors)or differences:
            write_json(LANE/'packet01-failure.json',dict(profile=profile,modelErrors=model_errors,differences=differences,original=compact(original),source=compact(source)))
            raise ValueError(('Battle fifth original/source/model difference',profile['ordinal'],differences,model_errors))
        results=[dict(kind='native',**compact(original)),dict(kind='source',**compact(source))]
        for control in controls:
            vm=F.Machine(main,overlay,images,profile)
            result=vm.run(control['origin'])
            errors=F.model(vm,result)
            control['actualTopReturns']+=1
            control['rejected'if errors else'positive']+=1
            results.append(dict(kind=control['label'],modelErrors=errors,**compact(result)))
        pcs.update(original['ownPcs'])
        calls+=len(original['provided'])+len(source['provided'])
        traces.append(dict(profile=profile,results=results,originalAndSourceCompletePhysicalStateEqual=True,independentModelPassed=True))
        if len(traces)%64==0:
            print('battle fifth pairs',len(traces),flush=True)
    if any(not row['rejected']for row in controls):
        raise ValueError('Battle fifth negative control was never rejected')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    trace=LANE/'packet01-traces.json.gz'
    trace.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=module_info['sha256'],mainSha256=main_info['sha256'],allPassed=True,matches=[match],canonicalMatchedFunctions=1,canonicalMatchedBytes=436,sourceCreditPendingIntegrator=436,sourceCreditPendingSharedAcceptance=True,producer='wave20261102_battle_fifth_packet01.py',producerSha256=sha256(__file__),inputs=dict(path=inputs.relative_to(ROOT).as_posix(),sha256=sha256(inputs)),cases=len(traces),actualNativeAndSourceCallerReturns=len(traces)*2,actualTopReturnsIncludingControls=len(traces)*5,actualNativeHelperReturns=0,suppliedBoundaryCalls=calls,completePhysicalRegistersCpsrRawCallsOrderedWritesAndAll8MiBRamEqual=True,independentRawPhaseWordModelPassed=True,nativeInstructionAddresses=sorted(pcs),negativeEvidence=controls,generatedTrace=dict(path=trace.relative_to(ROOT).as_posix(),sha256=sha256(trace),uncompressedSha256=hashlib.sha256(raw).hexdigest()),abiDebt=dict(path=(LANE/'callee-0205d790-abi-debt.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'callee-0205d790-abi-debt.json')),limits=['Ordinary C complete436-byte original extent, original compiler relocations and genuine pinned MW linkage. Qualified nativeSymbolEntries retain CPU/module/mode/address identity for host global interworking.', 'All256 raw phase bytes, bounded signed-byte cursors0/1/5, high-word actor pointers, raw low-byte handle truncation and signed label promotion are checked against an independent instruction-level model.', 'All12 external targets are supplied word boundaries with no memory effects and adversarial caller-saved/NZCV clobbers; zero actual original callee returns, source credit or arbitrary downstream behavior claim.', 'Legacy0205d790(void) prototype omits a live incoming/forwarded R0 word. The caller explicitly supplies the measured0x5c word; the accepted source remains unchanged and separately recorded ABI debt.', 'Raw field, phase, handle and label values carry no inferred battle/game meaning. No scene reachability, arbitrary alias domain, native Windows/Android or source-only ROM claim. Shared module/ROM acceptance remains coordinator-owned.'])
    write_json(LANE/'packet01-match.json',report)
    print(dict(functions=1,bytes=436,pairs=len(traces),actualTopReturns=len(traces)*5,controls=[{key:row[key]for key in ['label','rejected','positive']}for row in controls]),flush=True)


if __name__=='__main__':
    main()
