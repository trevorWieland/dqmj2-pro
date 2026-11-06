import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_ninth_build import build
from wave20261105_gamespy_qr2_next_ninth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_ninth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_ninth_fixtures import prove
from wave20261105_gamespy_qr2_next_ninth_abi import verify as verify_dynamic_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/ninth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/ninth/proof'


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
    if len(matches)!=1 or sum(row['bytes'] for row in matches)!=424:raise ValueError('Selected immutable packet membership changed')
    layout=layouts(matches[0],WORK/'layout');wrong_layout=layouts(matches[0],WORK/'wrong-layout',True);bindings=negative_controls(matches)
    dynamic_abi=verify_dynamic_abi(matches[0])
    closure=code_closure([Path(__file__).name])
    limits=['One complete424-byte ordinary C host ARM9/main/Thumb QR2 partial-reply builder matches through fresh source compilation and genuine MW linking; shared acceptance pending.',
        'Published/measured record prefix ends after pa_callback168; bytes172..267 remain opaque and userdata word268 is measured. This272-byte view does not claim full original object layout or storage.',
        'Six original register-indirect BLX sites preserve unresolved runtime identities: one count, one keys, two server-value, one player-value and one team-value callsite. Synthetic ARM/Thumb/mixed callback contracts qualify caller ABI only; no static callback namespace or implementation execution credit.',
        'Ordinary C scalar endian expression plus source-visible fixed2 unsigned byte copy reproduces the measured count prefix. Two source empty literals bind the one actual original ABS32 address020e25b4; unknown-string020e25ac/table020e277c storage gets zero authorship credit.',
        'Bounded independent models cover count0/explicit/list255 queries, zero/negative row counts, ASCII names/missing-name fallback, no-output callbacks/empty placeholders,2/1/0-byte capacity boundaries and incoming fifth stack word preservation. Imported buffer-add/callback bodies remain supplied contracts.',
        'No real callbacks, networking/devices/scenes, invalid pointer behavior, full object storage or native Windows/Android execution is proved.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=1,matchedBytes=424,ordinaryCBytes=424,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalDynamicCallbackAbiProof=dynamic_abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
