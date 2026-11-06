import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_eighth_build import build
from wave20261105_gamespy_qr2_followup_eighth_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_eighth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_eighth_fixtures import prove
from wave20261105_gamespy_qr2_followup_eighth_v2_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/eighth'
INPUT=LANE/'inputs-v2.json'
WORK=ROOT/'work/w5qf/eighth/proof'


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
    if len(matches)!=8 or sum(row['bytes'] for row in matches)!=884:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Eight complete ordinary C ARM9/main/Thumb message callers total884 bytes reproduce explicit-C99 compilation,original relocations and full genuine MW-linked native extents. Shared acceptance remains pending.',
        'The actual1044-byte backing array and typed20-byte header view preserve native SP recomputation at provider calls. Two104-byte consumers read a raw32-bit control word at48; this new scalar view replaces only an unused function-pointer spelling in their private header. Earlier frozen contexts remain unchanged and no callback meaning is inferred for that word.',
        'The252-byte sender preserves unsigned1024-byte clamp,205 first-fragment total,207 continuation flag/length,copy andprogress updates,short-circuit failure,final wait/count comparison and cleanup. Fixtures bound payloads to0..3073 bytes and finite supplied success/failure scripts; actual IO/queue/provider progress and concurrency remain unqualified.',
        'Original literal8ab0+88 is exactly Thumb20b8dd9. A prior diagnostic draft named another callback with the same prototype and passed masked-opcode comparison, but failed strict native-binding preflight; it remains uncredited. Selected source names the genuine target and the materializer rejects every address-named API alias that differs from original metadata.',
        'Only defined header/payload bytes are consumed. Unused1044-byte stack tails are uninitialized and add no data-authorship or read-safety claim. All GPRs,CPSR,callee-saved registers,stack,ordered writes,external memory,original modes and supplied argument/return contracts compare. Callback,queue,copy,wait,send/setup/cleanup provider bodies add zero source or execution credit. No hardware,network,game scenes,native Windows/Android or whole-game execution is established.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=8,matchedBytes=884,ordinaryCBytes=884,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
