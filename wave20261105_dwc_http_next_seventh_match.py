import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_seventh_build import build
from wave20261105_dwc_http_next_seventh_bindings import negative_controls
from wave20261105_dwc_http_next_seventh_controls import layouts,wrong_source
from wave20261105_dwc_http_next_seventh_fixtures import prove
from wave20261105_dwc_http_next_seventh_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/seventh'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/seventh/proof'


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
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],actualNativeAndSourceCallerStops=model['actualNativeAndSourceCallerStops'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,
            boundaryReturnContract=item['boundaryReturnContract'])
        matches.append(row)
        print('proved GT2 C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=2 or sum(row['bytes'] for row in matches)!=756:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    abi=verify_abi(matches)
    limits=['Two complete ordinary C SVL request/result functions total756B reproduce genuine whole MW-linked native extents,original relocations and static modes/data. Shared acceptance remains pending.',
        'Constructor requires nonnull work,service and result. Its28B local Http parameter and148B Cal scratch are measured; real returned-word Cal tests and current-thread priority replace incorrect comparative void/hardcoded values. Native priority provider is read-only corroboration only,never executed or credited.',
        'Constructor fixtures cover failure stages,custom/default URL,raw thread ID,callback modes,priority decrement,provider pointer changes and result clearing. The existing active-thread OS_Terminate path is a declared stop at the actual ARM import entry. Stops are counted separately from caller returns; no supplied termination body executes.',
        'Parser fixtures preserve sticky errno34 before/after both integer conversions,signed return/status limits,negative/zero/positive decode boundaries,Date/time import and latest work/result pointers while retaining cached Http. Provided encoded-result payloads fit supplied bounds and terminate return-code scratch; arbitrary malformed strings/oversized payloads and signed error-arithmetic overflow remain unqualified.',
        'All GPRs/CPSR,returned callee-saved registers,stack,ordered writes,observed errno reads,external memory and provider tuples compare. Original initialized/BSS data and all allocation,HTTP,Cal,RTC,error/thread,network/game/Windows/Android provider implementation/execution credit remain zero.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=2,matchedBytes=756,ordinaryCBytes=756,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),actualNativeAndSourceCallerStops=sum(model['actualNativeAndSourceCallerStops'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
