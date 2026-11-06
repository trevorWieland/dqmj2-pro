import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_fourth_build import build
from wave20261105_gamespy_qr2_followup_fourth_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_fourth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_fourth_fixtures import prove
from wave20261105_gamespy_qr2_followup_fourth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/fourth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/fourth/proof'


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
    if len(matches)!=11 or sum(row['bytes'] for row in matches)!=740:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Eleven complete ordinary C ARM9/main/Thumb state/status/request callers total740 bytes, including three112/108/100-byte request producers, match explicit-C99 pinned base compilation, unchanged object relocations and genuine MW linking. Shared acceptance remains pending.',
        'Measured72-byte status prefix embeds40-byte request at20; validator preserves unsigned id1..255/nonzero-mode and1..15/zero-mode, protected phase2 and zero busy word. Producer1 adds1024 to numeric id. Five-word boundaries preserve word5 at entrySP+0; opaque words4/5 are stored only and have no inferred callback/userdata meaning.',
        'Signed shared error field at440 is loaded before locking, rechecked after provider side effects and read separately for the two-word shutdown boundary. Ordered-read oracle and wrong volatile-qualifier control preserve these independent loads. Protected status forwarding, dense switch cases, sticky error9, cleanup provider order and one-word synthetic ARM/Thumb callbacks are independently modeled.',
        'All GPRs,CPSR,callee-saved registers,stack,ordered reads/writes,external memory,provider tuple/return contracts and original static modes are compared. Request caller contracts deliberately include artificial validator acceptance and helper global-base mutations to exercise caller forwarding; this adds no reachability or provider implementation claim.',
        'Original queues, mutexes, shutdown, error forwarding, allocator/free, validator/send implementations, dynamic callbacks, source-provided storage, devices, networks, scenes, native Windows/Android and full game execution receive zero added source or execution credit. Full foreign object allocation and the separate nonmatching32-byte size calculator remain unproven.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=11,matchedBytes=740,ordinaryCBytes=740,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
