import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_match_tail_next_fourth_build import build
from wave20261106_dwc_match_tail_next_fourth_bindings import negative_controls
from wave20261106_dwc_match_tail_next_fourth_controls import layouts,wrong_source
from wave20261106_dwc_match_tail_next_fourth_fixtures import prove
from wave20261106_dwc_match_tail_next_fourth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/fourth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mt/fourth/proof'


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
    if len(matches)!=7 or sum(row['bytes'] for row in matches)!=1026:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Seven complete ordinary C DWC cancellation/reservation-recovery/connection-control functions1026B reproduce full genuine MW-linked native extents,original relocations and typed main ARM/Thumb entry identities; source credit awaits shared acceptance.', 'Pinned comparative DWC C/header plus public DWC error/friend/main and GameSpy type declarations ground public enums,opaque connection pointers and the consumed MatchControl fields. Complete caller matching and28 independent layout checks qualify only consumed data views; imported bodies/storage remain uncredited.', 'Independent bounded caller models cover friend validation short-circuits,timeout exclusions,prior-profile resume paths,provided browser/command errors,NULL/present connection handles,0/1/3/31 connections,1/3/32 backup words,early send failures,own-versus-remote reservation ownership,cookie cancellation,match types0..3,server cancel retries,zero-connection restart,and64bit tick values.', 'Actual native and source caller executions compare all GPRs/CPSR,callee-saved/stack,ordered writes,exact typed provider tuples and output memory. Each function receives a genuine linked wrong-C returning model rejection,wrong layout and missing actual declaration controls.', 'Sibling caller bodies remain opaque entry contracts within another caller fixture; getters,status/error handlers,GT2/QR2/natneg/clock and close/retry providers execute zero real body instructions and add zero supplied source or execution credit. Provided SetMatchStatus and shutdown handlers are inert fixture boundaries; real state transitions,callback reentrancy,concurrent getters,network/device/game/Windows/Android execution are unqualified.', 'Payloads above32words,connection counts above31,invalid pointers,unbounded provider behavior and complete imported type correctness remain outside fixture coverage. Required-prototype diagnostics establish presence only. Full-size callback/coalescing residuals and the separate NNStartup592B remain unselected.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=7,matchedBytes=1026,ordinaryCBytes=1026,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
