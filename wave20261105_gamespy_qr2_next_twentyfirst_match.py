import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_twentyfirst_build import build
from wave20261105_gamespy_qr2_next_twentyfirst_bindings import negative_controls
from wave20261105_gamespy_qr2_next_twentyfirst_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_twentyfirst_fixtures import prove
from wave20261105_gamespy_qr2_next_twentyfirst_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/twentyfirst'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/twentyfirst/proof'


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
    if len(matches)!=2 or sum(row['bytes'] for row in matches)!=338:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Two complete ordinary C host ARM9/main/Thumb GT2 receive/builder bodies total338 bytes and match fresh source compilation, unchanged original relocations and genuine MW linking; shared acceptance pending.',
        'Receiver264 uses the actual1500-byte stack buffer and eight-byte Nintendo peer view. Native error tests distinguish exact recv sentinel-1 and measured error words reset-15,unreachable-23,message-size-35; only this caller context is qualified.',
        'Outgoing builder74 uses ordinary typed-zero16-byte initialization, matching four original word stores before publishing start,length,serial and timestamp. Its padding10..11 is concretely zeroed and all16 forwarded bytes are compared by the supplied append contract.',
        'Independent bounded cases cover available/no data loops, repeated peer-length reset8, raw receive/error/boolean words, exact ignored message-size error, live socket mutation after handlers, array-count equality, serial/time/buffer words and clock side effects after start capture.',
        'Caller models compare all GPRs,CPSR,callee-saved registers,stack balance,ordered writes and original import modes. Successful receive contracts supply accessible payloads and all peer bytes even on modeled errors; this is not a claim about OS error-output initialization.',
        'Supplied receive/array/clock/handler implementations, original storage, all real networking/devices/scenes, complete game and native Windows/Android execution receive zero added source or execution credit. The separate sender336 remains338/346 in bounded private zero-context probes and is uncredited.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=2,matchedBytes=338,ordinaryCBytes=338,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
