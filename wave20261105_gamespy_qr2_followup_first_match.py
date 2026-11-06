import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_first_build import build
from wave20261105_gamespy_qr2_followup_first_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_first_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_first_fixtures import prove
from wave20261105_gamespy_qr2_followup_first_abi import verify as verify_abi
from wave20261105_gamespy_qr2_followup_first_profile import prove as prove_wrong_profile

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/first/proof'


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
    if len(matches)!=3 or sum(row['bytes'] for row in matches)!=716:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches);profile=prove_wrong_profile(next(row for row in matches if row['address']=='0x20b8334'),WORK/'wrong-profile')
    closure=code_closure([Path(__file__).name])
    limits=['Three complete ordinary C host ARM9/main/Thumb QR2 bodies total716 bytes and match fresh explicit-C99 SP1p5 compilation, unchanged original relocations and genuine MW linking; shared acceptance pending.',
        'Verifier88 scans200 typed16-byte entries, matches raw endpoint/challenge words and clears only the matched address/port fields. Keepalive76 and heartbeat552 preserve the full1400-byte local buffer and len@1400, the qualified3476-byte QR2 record and Nintendo peer8.',
        'The pinned base compiler produces a64-byte keepalive with different large-stack member accesses. The same C source compiled with pinned SP1p5 produces exact native76; the base variant genuinely links but fails complete native comparison and returning-model controls. No source/instruction/object patch or optimizer-permutation search substitutes for compiler qualification.',
        'Bounded caller models cover array endpoints/challenge equality, heartbeat state classes, local-IP loop reads, raw callback-gate/NAT/port words, full-buffer server-only fallback, one-byte shutdown trailer, variable-length copies, send payloads, clock updates and helper mutations.',
        'Header/query/memory/format/address/buffer/socket/clock implementations are supplied contracts. Artificial large header/query lengths exercise caller capacity branches without claiming those helper implementations produce those values in the game. Callback pointers are unresolved incoming record data and no callback body executes.',
        'All GPRs,CPSR,callee-saved registers,stack,ordered writes and original import modes compare. Original storage, actual helpers/networking/devices/scenes, complete game and native Windows/Android execution receive zero added source or execution credit. Query-parser660 remains nonmatching640 in separate bounded diagnostics.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=3,matchedBytes=716,ordinaryCBytes=716,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,negativeCompilerProfileEvidence=profile,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
