import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_match_tail_next_seventh_build import build
from wave20261106_dwc_match_tail_next_seventh_bindings import negative_controls
from wave20261106_dwc_match_tail_next_seventh_controls import layouts,wrong_source
from wave20261106_dwc_match_tail_next_seventh_fixtures import prove
from wave20261106_dwc_match_tail_next_seventh_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/seventh'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mt/seventh/proof'


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen runtime dependency changed',pin['path']))
    if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('Measured ROM identity changed')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();matches=[];models=[];wrong=[]
    for item in inputs['entries']:
        source=ROOT/item['source']
        for path in [source,*[ROOT/pin['path'] for pin in item['sourceDependencies']]]:
            text=path.read_text()
            if len(text.splitlines())>500 or re.search(r'/\*|//|\b(?:asm|__asm|__asm__)\b',text):raise ValueError(('Ordinary authored C source policy differs',str(path)))
        directory=WORK/format(int(item['address'],0),'08x');row,body=build(source,directory/'source')
        for key in ['address','bytes','source','sourceSha256','sourceDependencies','targetSha256','compilerPath','compilerSha256','compilerFlags','relocations','nativeSymbolEntries']:
            if row[key]!=item[key]:raise ValueError(('Frozen whole source/compiler/interface contract changed',item['address'],key))
        if row['compiledBytes']!=item['bytes'] or not row['realLink']['exactCallerBytes']:raise ValueError('Complete genuine linked extent differs')
        start=int(row['address'],0)-0x2000000;native=image[start:start+row['bytes']]
        if body!=native:raise ValueError('Complete native caller bytes differ')
        model=prove(row,native,body);models.append(model)
        wrong.extend(wrong_source(row,directory/'wrong-C'))
        row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],
            matchingBytesScope='Complete genuine MW-linked native caller extent including original literal pool',
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,
            boundaryReturnContract=item['boundaryReturnContract'])
        matches.append(row)
        print('proved DWC C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=1 or sum(row['bytes'] for row in matches)!=2796:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['One complete2796B ordinary C receive-command dispatcher matches full genuine MW-linked native extent and all208 original relocation origins,target modes and addends. Source acceptance remains pending.', 'Pinned public DWC text and independently measured SDK/Nintendo context qualify actual explicit call declarations,8B sockaddr layout,the source-visible ordinary network-order macro,and a4B optional-control pointer slot at main BSS021d1b88. Other QR2 layout and original storage authorship remain unqualified.', 'Independent models cover only commands0/3/4/5/6/9/12/13/14/15/16/17/18/19/64/65/255: NULL/INIT gates,selected reservation-deny/wait/cancel paths,address forwarding,link-success,cancel delegation,SC close-list filtering,optional timeout/poll Ack,connection-block and keepalive. Commands1/2/7/8/10/11/32 and their branches have full static byte evidence but no independent dynamic model here.', 'Address fixtures independently verify only initialized sockaddr port/IP bytes2..7. All8 actual bytes including uninitialized length/family slots compare native-versus-rebuilt concrete runs; portable meaning or required values for those first2bytes are unqualified.', 'All GPRs/CPSR,callee-saved/stack,ordered writes,exact provider tuples and output memory compare. Two meaningful wrong-C variants independently reject byte-order and wait-count changes; layout,prototype-presence and original binding controls remain strict. No nonempty phase-read observation is configured.', 'Getters,SDK timer/division/state/errors,original sibling/provider bodies,callbacks and network services are supplied opaque contracts and receive zero source/execution credit. No device/game/nativeWindows/Android behavior is established. Fixture option pointees guarantee a32B published prefix and valid indices; real allocation/concurrency/failure behavior and complete imported type correctness remain unqualified.', 'The optional pointer at BSS group+0 and older12B group/addFilter+8 view use separate partial C declarations. Their DS link/offset evidence does not establish a unified portable object declaration; the separately pinned zero-byte interface receipt preserves this debt for later migration.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=1,matchedBytes=2796,ordinaryCBytes=2796,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
