import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_fourth_build import build
from wave20261105_gamespy_qr2_next_fourth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_fourth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_fourth_fixtures import prove

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/fourth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/fourth/proof'


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
    if len(matches)!=1 or sum(row['bytes'] for row in matches)!=248:raise ValueError('Selected immutable packet membership changed')
    layout=layouts(matches[0],WORK/'layout');wrong_layout=layouts(matches[0],WORK/'wrong-layout',True);bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    limits=['One complete248-byte ordinary C host ARM9/main/Thumb QR2 query-dispatch function matches through fresh source compilation and genuine MW linking; shared acceptance remains pending.',
        'The measured Nintendo8-byte socket-address interface replaces the provisional16-byte host layout in this separate source context. Every direct import retains its original same-program callsite, entry and Thumb mode; existing frozen headers remain unchanged.',
        'Bounded caller models cover three length-guarded byte-count lists, zero/all-key sentinels, exact true1 reply status, signed packet ordinal limit7,280-byte progress state and its initialized key count, output reset to5, and six/eight-word SDK call boundaries.',
        'Reply builders provide opaque bounded payloads and progress transitions. Sendto captures the8-byte sender and requested packet bytes. None of the original reply-builder/networking helper bodies executes or earns source/behavior credit.',
        'Invalid pointers, complete buffers/objects beyond their measured views, actual network operation, devices/scenes, and native Windows/Android game execution remain unproved.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=1,matchedBytes=248,ordinaryCBytes=248,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
