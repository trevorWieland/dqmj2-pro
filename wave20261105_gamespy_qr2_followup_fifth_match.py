import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_fifth_build import build
from wave20261105_gamespy_qr2_followup_fifth_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_fifth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_fifth_fixtures import prove
from wave20261105_gamespy_qr2_followup_fifth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/fifth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/fifth/proof'


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
    if len(matches)!=7 or sum(row['bytes'] for row in matches)!=536:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Seven complete ordinary C ARM9/main/Thumb callers total536 bytes, including120-byte send/208-byte receive, preserve explicit-C99 compilation, complete native spans, original relocation payloads and genuine MW links. Shared acceptance pending.',
        'Signed progress counters and unsigned sizeof/length comparisons preserve native signed BGT versus unsigned BLO behavior.1044-byte caller view has length@0,magic@4 and12-byte minimum header. Finite provider scripts cover partial IO, initial/partial zero and negative reads, bounded write retries, length overflow, bad magic, exact frame edge and global-base mutations.',
        'The40-byte sender forwards its original result pointer as queue message after three word clears; its earlier NULL-forwarding draft remains uncredited diagnostic evidence. Both60/68-byte thread waits preserve measured16-bit register read/disable/current-read/restore order and the52/2576-byte thread offsets.',
        'Register04000208 is mapped only as a bounded two-byte fixture word. No actual interrupts, scheduler, thread, queue or DS hardware executes. All GPRs,CPSR,callee-saved registers,stack,ordered reads/writes,external memory,provider argument/result contracts and actual original modes compare.',
        'Provided scheduler, queues, IO, errors, cleanup/status and output-pointer implementations add zero source or execution credit. Positive IO counts are bounded by request; scripts supply finite progress. Persistent zero writes, out-of-contract returns, real networking/game behavior, full foreign allocations and native Windows/Android execution remain unproven. All source is ordinary C; no authored algorithm assembly or object/instruction patch.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=7,matchedBytes=536,ordinaryCBytes=536,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
