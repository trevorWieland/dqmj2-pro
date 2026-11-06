import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_third_build import build
from wave20261105_dwc_http_next_third_bindings import negative_controls
from wave20261105_dwc_http_next_third_controls import layouts,wrong_source
from wave20261105_dwc_http_next_third_fixtures import prove
from wave20261105_dwc_http_next_third_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/third'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/third/proof'


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
    if len(matches)!=2 or sum(row['bytes'] for row in matches)!=504:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Two complete ordinary C ARM9/main/Thumb custom-base64 functions total504 bytes reproduce explicit-C99,pinned2.0sp1p5 compilation,original relocations and full genuine MW-linked native extents. Shared acceptance remains pending; no algorithm ASM or object edits.',
        'Pinned independent reconstructed C supplies comparison text; actual native zero-input decode no-write differs from that text.2.0sp1p5 naturally reproduces original signed local-byte reloads; base240B and volatile alternatives remain uncredited. Original64-symbol alphabet/pointer receive zero authored data credit.',
        'Independent stdlib-base64 translation and six-bit stream models cover query/exact/short capacities,residual triplets,custom.- alphabet,*padding,invalid signed bytes and length rejection. Decode allpadding query0/write1 and zero-input no-write quirks are preserved.256-byte provided physical output permits raw effects beyond advertised logical capacity; arbitrary pointers,huge lengths/overflow/aliasing,global safety and real service use remain unqualified.',
        'Ninety-six original bounded ARM support probes separately verify quotientR0/remainderR1,callee-saved/SP/LR,mode andno writes. Caller tests provide those arithmetic contracts plus copy/fill boundaries and compare all GPRs,CPSR,stack,ordered writes,external memory and tuples. Arithmetic/copy/fill bodies,original alphabet,hardware/network/game scenes,native Windows/Android and whole-game execution add zero additional credit.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=2,matchedBytes=504,ordinaryCBytes=504,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
