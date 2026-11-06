import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_second_build import build
from wave20261106_wcm_manager_next_second_bindings import negative_controls
from wave20261106_wcm_manager_next_second_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_second_fixtures import prove
from wave20261106_wcm_manager_next_second_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/second'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/second/proof'


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
        print('proved WCM C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=1184:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Six complete ordinary C WCM lifecycle/callback functions1184B reproduce full genuine MW-linked native extents and all original function/data/callback relocation identities. Shared source acceptance remains pending.', 'Twenty-eight typed layout assertions cover consumed work offsets,callback8B fields,WMStatus2B state prefix and exact native initialization-buffer base. WMStatusPrefix names only the consumed state word;no complete WMStatus size/type or opaque work/alarm/scan internals are inferred.', 'Bounded models cover initialized/NULL work,all phases0..14,startup WM initialization/channel/finish/indication/enable errors,cleanup/disconnect returns and reset states,termination status READY/STOP/IDLE/other,all tested provider error classes,and indication/scan callback gates.', 'Configure,phase,notification,WM,cache and interrupt callees are opaque supplied provider contracts. Models leave their real memory/interrupt effects unqualified;no original provider body executes and none receives source credit. No real WiFi,asynchronous timing,IRQ/cache/concurrency/game or host behavior is established.', 'All GPRs/CPSR,callee-saved registers,stack,ordered writes,full bounded output memory and exact provider tuples compare. Required-prototype checks establish declaration presence only. No ordered observed-read addresses are configured;no phase-read/concurrency proof is claimed.', 'Status fixtures supply only a valid2B state prefix;callback fixtures supply valid8B public records. Invalid pointers,provider-reentrant/global changes,supplied caller configurations whose actual Configure helper would rewrite the preinitialized DMA value,and unbounded errors or lifecycle effects remain outside execution coverage. Source/native whole bytes independently cover all static branches.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=1184,ordinaryCBytes=1184,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
