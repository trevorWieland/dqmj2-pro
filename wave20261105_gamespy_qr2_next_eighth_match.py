import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_eighth_build import build
from wave20261105_gamespy_qr2_next_eighth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_eighth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_eighth_fixtures import prove

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/eighth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/eighth/proof'


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
    if len(matches)!=3 or sum(row['bytes'] for row in matches)!=324:raise ValueError('Selected immutable packet membership changed')
    layout=layouts(matches[0],WORK/'layout');wrong_layout=layouts(matches[0],WORK/'wrong-layout',True);bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Three complete ordinary C host ARM9/main/Thumb control-packet builder bodies324B match through fresh source compilation and genuine MW linking; shared acceptance pending.',
        'Source-visible ordinary C byte-view copy specializes constant2/4 lengths without alignment assumptions; actual selected paths use fixed2. No assembly/intrinsic/object rewrite or callee body substitute is used. The copied reference spelling is pinned independently.',
        'Bounded caller models independently check UDP/VDP/other protocol words, little-endian payload prefixes, big-endian serial fields/equal NACK ranges, packet discriminators and successful-only pending-ACK clearing. Bytewise-copy source mutation and individual caller mutations genuinely compile/link and fail returning models.',
        'The imported ushort writer and sender routines remain explicit supplied ABI contracts; no helper source/body or real networking execution credit. Original function entries/modes are independently qualified from actual branch opcodes and canonical complete boundaries.',
        'The original3-byte magic view is immutable input with zero storage authorship credit. Invalid pointers, overlapping copies, other record fields, actual network/device/scene behavior and native Windows/Android game execution remain unproved.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=3,matchedBytes=324,ordinaryCBytes=324,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
