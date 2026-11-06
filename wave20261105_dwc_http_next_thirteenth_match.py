import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_thirteenth_build import build
from wave20261105_dwc_http_next_thirteenth_bindings import negative_controls
from wave20261105_dwc_http_next_thirteenth_controls import layouts,wrong_source
from wave20261105_dwc_http_next_thirteenth_fixtures import prove
from wave20261105_dwc_http_next_thirteenth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/thirteenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/thirteenth/proof'


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
    if len(matches)!=1 or sum(row['bytes'] for row in matches)!=156:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['One complete ordinary C156B NAS clock-consuming date/time function matches full genuine MW-linked native extent,all original relocations,three separate canonical NAS BSS entries and exact ARM SDK helper modes; shared acceptance pending.',
        'Readable C is independently reconstructed from measured native control/data flow,published RTCDate16/RTCTime12 and64-bit SDK declarations. GetNasDateTime is a descriptive working name,not a recovered published symbol. Comparative NAS-time source supplies only the already measured global-variable roles.',
        'Valid flag,64-bit base and64-bit difference are original zero-credit BSS entries021d1990/021d1994/021d199c. No data/scaffolding/provider body is authored or credited.',
        'Bounded caller fixtures cover invalid/nonzero validity words,SDK read failures,-1 seconds sentinel,current/base equality and century rollover,negative/zero/exact3155759999/above-limit results,high/low64-bit words and source-level wrong-state/arithmetic/boundary mutations.',
        'The RTC read,seconds conversion and inverse conversion remain provided typed contracts. Original helper bodies and real calendar/hardware/timekeeping behavior are unexecuted and uncredited. Caller R0/R1 return andR2/R3 argument pairs,exact struct tuples,callee-saved registers,CPSR,stack,ordered writes and external memory compare.',
        'Only nonnull disjoint valid date/time output buffers are modeled. Arbitrary pointers,concurrent state mutation,signed64 addition/subtraction overflow,hardware/network/game/nativeWindows/Android execution remain unqualified. Required-prototype diagnostics prove declaration presence only.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=1,matchedBytes=156,ordinaryCBytes=156,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
