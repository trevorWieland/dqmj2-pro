import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_second_build import build
from wave20261105_gamespy_qr2_followup_second_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_second_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_second_fixtures import prove
from wave20261105_gamespy_qr2_followup_second_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/second'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/second/proof'


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
        print('proved GT2 C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=11 or sum(row['bytes'] for row in matches)!=580:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Eleven complete ordinary C host ARM9/main/Thumb bodies total580 bytes; fresh explicit-C99 base compiler, unchanged original relocations and genuine MW links prove whole extents. Shared acceptance remains pending.',
        'Ten control/callback/dispatch bodies total560 bytes use raw names and measured48-byte control,40-byte result and20-byte event prefixes. The full backing containers and higher-level middleware meaning remain unqualified. QR2 key registration20 derives from the pinned published definition with the measured50..254 signed range.',
        'The148-byte worker dispatches measured codes1..9 and preserves default/null, dequeue/clear order and finite supplied poll progress. OS queue/thread, registration, dispatch handlers and sleep providers are bounded contracts; no original provider body is executed by these fixtures.',
        'User callback is one Event* word and both synthetic ARM/Thumb modes, returned words and helper mutations are tested. The registered boundary callback is two words int/Event*, with original pointer020b8d15 and exact canonical Thumb entry020b8d14. Static namespaces and original instruction/data words remain independently qualified.',
        'Caller model compares all GPRs,CPSR,callee-saved registers,stack,ordered writes,external memory,helper argument tuples and returns. Finite poll fixtures establish caller behavior only; real scheduler/hardware progress and full network/game behavior remain unproven.',
        'The registry1020-byte minimum indexed span and control global pointer add zero original-storage/allocation credit. Every supplied helper, dynamic callback, original provider, device, scene and native Windows/Android execution receives zero added source or execution credit. Separate QR2 parser/RC4 probes remain uncredited.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=11,matchedBytes=580,ordinaryCBytes=580,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
