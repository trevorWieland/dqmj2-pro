import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_eleventh_build import build
from wave20261105_gamespy_qr2_next_eleventh_bindings import negative_controls
from wave20261105_gamespy_qr2_next_eleventh_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_eleventh_fixtures import prove
from wave20261105_gamespy_qr2_next_eleventh_abi import verify as verify_dynamic_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/eleventh'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/eleventh/proof'


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
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=782:raise ValueError('Selected immutable packet membership changed')
    layout=layouts(matches[0],WORK/'layout');wrong_layout=layouts(matches[0],WORK/'wrong-layout',True);bindings=negative_controls(matches)
    dynamic_abi=verify_dynamic_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Six complete ordinary C host ARM9/main/Thumb NAT protocol/controller bodies782B match fresh source compilation and genuine MW links; shared acceptance pending.',
        'The published84-byte negotiation record and measured Nintendo peer8 view explain word/signed-state/byte/halfword accesses. Known global views cover BSS active flag+28 and initialized sockets+4/+8; unknown preceding words stay opaque and all storage earns zero authorship credit.',
        'Independent bounded models cover all selected state transitions, strict unsigned timer/equality/wrap boundaries, retry limits, canceled/null states, two-step active-NAT publication, receive-loop error/close/cancel exits and callback side effects. Opaque helpers are supplied ABI contracts, not real network executions.',
        'Original completed-callback(slot60) and progress-callback(slot56) BLX sites retain unresolved runtime target identities. Synthetic ARM/Thumb/mixed contracts qualify caller argument/return preservation only; no static callback namespace or implementation execution is inferred.',
        'Hostname resolution tests check bounded snprintf capacity64, format/game/default forwarding and truncation before opaque NameToIp. Original ARM formatter entry/mode and fifth stacked argument are independently measured; no formatter or resolver body executes.',
        'Peer checks cover initialized family/port/IP fields only; the untouched length byte is not authored. Unselected default-domain macros, original global/string/buffer storage, imported code, complete game/network/device behavior and native Windows/Android execution receive zero extra credit. NAT Think520 remains uncredited.']
    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=782,ordinaryCBytes=782,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalDynamicCallbackAbiProof=dynamic_abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
