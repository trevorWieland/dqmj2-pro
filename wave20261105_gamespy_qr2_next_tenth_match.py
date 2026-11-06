import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_tenth_build import build
from wave20261105_gamespy_qr2_next_tenth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_tenth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_tenth_fixtures import prove

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/tenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/tenth/proof'


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
        wrong.append(wrong_source(row,directory/'wrong-C'))
        row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],
            matchingBytesScope='Complete genuine MW-linked native caller extent including original literal pool',
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,
            boundaryReturnContract=item['boundaryReturnContract'])
        matches.append(row)
        print('proved GT2 C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=4 or sum(row['bytes'] for row in matches)!=162:raise ValueError('Selected immutable packet membership changed')
    layout=layouts(matches[0],WORK/'layout');wrong_layout=layouts(matches[0],WORK/'wrong-layout',True);bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Four complete ordinary C host ARM9/main/Thumb NAT utility/record bodies162B match fresh source compilation and genuine MW links; shared acceptance pending.',
        'Two physical38-byte local-port reader functions retain their distinct original entry/callsite identities and measured Nintendo sockaddr8/family1/port2/address4 layout. The original failure predicate compares status exactly-1 and successful port forwarding retains the raw network-order halfword.',
        'One84-byte builder zeros the entire original allocation/append extent through a typed C initializer, retaining original ArrayNew/Append/Length/Nth calls. The published negotiation-record view is84 bytes with an8-byte remote address; no additional record semantics, padding/storage authorship or actual allocator execution is credited.',
        'The original2-byte OutputMapping body is a void no-op after published debug macros are disabled. Bounded native/source traces prove only unchanged caller state/registers and return, including null and nonnull mapping inputs.',
        'Independent bounded fixtures and genuinely linked wrong-source controls cover error-1 versus other negative statuses, raw port bits, existing/new list paths, full84-byte zero append payload and illegal no-op memory writes. Socket/array helper bodies remain supplied ABI contracts with zero execution/source credit.',
        'BSS list-pointer storage, actual networking/devices/scenes, debug-enabled builds and native Windows/Android execution remain unproved. Large NAT Think520 and local-IP60 shape mismatches remain uncredited.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=4,matchedBytes=162,ordinaryCBytes=162,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
