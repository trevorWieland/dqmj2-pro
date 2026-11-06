import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_match_tail_next_sixth_build import build
from wave20261106_dwc_match_tail_next_sixth_bindings import negative_controls
from wave20261106_dwc_match_tail_next_sixth_controls import layouts,wrong_source
from wave20261106_dwc_match_tail_next_sixth_fixtures import prove
from wave20261106_dwc_match_tail_next_sixth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/sixth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mt/sixth/proof'


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
    if len(matches)!=4 or sum(row['bytes'] for row in matches)!=1608:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Four complete ordinary C reservation/retry/synchronization functions1608B reproduce full genuine MW-linked native extents and original ARM/Thumb entries; shared source acceptance remains pending.', 'Public DWC/SDK definitions and independently frozen GameSpy context ground the532B GPBuddyStatus record including its quiet-mode word at528,12B friend records,consumed MatchControl fields,and SDK33514000-clock conversion. Thirty-four typed layout checks include a wrong528-byte status-size rejection for the560B caller.', 'Bounded caller models cover friend-index start/wrap/empty candidate cycles,provided invalid/valid profiles and friend flags,buddy errors/status/version/entry filters,resend delay,all match types,retry failures,counter255 wrap,strict6000ms boundaries,CL/SV synchronization states,bit31 masks,Ack transitions,cancellation latency and64bit elapsed wrap/multiply/floor arithmetic.', 'The actual compiler-generated unsigned64 helper is bound to original ARM main020260dc with complete original callsite/entry/mode contracts. It is supplied as an opaque arithmetic fixture returning quotient inR0/R1; its real body has zero execution/source credit. SDK clock/getter/state,GP status/profile/parser,connection/cancel/error/sibling providers are also opaque; no real network,device,game or host-platform behavior is established.', 'All GPRs/CPSR,callee-saved/stack,ordered writes,exact provider tuples and output memory compare. Clock/division return high words are explicitly supplied; private required-prototype checks prove presence only. No ordered phase-read addresses are configured; no phase-read or concurrent-provider proof is claimed.', 'Friend fixtures use1..3 entries with valid12B backing records and fields fitting declared12/4/2byte temporary strings. Buddy index/status fixtures always initialize their outputs even on supplied errors; real provider failure output initialization remains unqualified. Invalid pointers,empty-invalid friend backing,oversized statuses/strings,Aids outside0..31 except255 sentinel,unbounded providers and complete imported type correctness remain outside coverage.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=4,matchedBytes=1608,ordinaryCBytes=1608,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
