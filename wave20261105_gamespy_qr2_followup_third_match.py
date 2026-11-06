import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_third_build import build
from wave20261105_gamespy_qr2_followup_third_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_third_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_third_fixtures import prove
from wave20261105_gamespy_qr2_followup_third_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/third'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/third/proof'


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
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=544:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Six complete ordinary C ARM9/main/Thumb callers total544 bytes, including104/240-byte initializers and116-byte phase worker, match fresh explicit-C99 pinned base compiler, original object relocations and genuine MW links. Shared acceptance remains pending.',
        'Caller views initialize2292/4816 bytes and describe192-byte thread/2048-byte stack spans, fixed field offsets and the six-word thread-creation boundary. They establish these observed views, not complete foreign owner allocation or all OS/type semantics.',
        'The two shared phase/status words retain native volatile guard/switch reads and explicit old-word transition reads. Independent ordered-read oracles compare each selected load as well as all GPRs,CPSR,callee-saved registers,stack,ordered writes,external memory,provider tuples and returns. Wrong C removing those reads/qualifiers must return and fail the oracle.',
        'The worker model uses finite supplied handler progression through codes1..7. Unknown/default nonzero phases preserve native looping behavior, but have no scheduler or termination proof. Native thread entries receive one opaque ignored argument; no original OS/thread/provider body is executed.',
        'Published allocation/free word declarations come from the exact-commit narrow NitroDWC header snapshot. Incoming allocator pointers are only stored; qualified original mask/thread function pointers are preserved with exact native entries/modes. The five-byte bounded string helper receives the original empty string, with NUL padding modeled; supplied providers add zero implementation credit.',
        'Filled storage, original data/BSS, callbacks, OS queues/mutexes/threads, devices, networks, game scenes and native Windows/Android execution add zero source or execution credit. Larger message-builder and RC4 shape probes remain separate and uncredited.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=544,ordinaryCBytes=544,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
