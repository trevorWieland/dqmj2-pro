import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_followup_sixth_build import build
from wave20261105_gamespy_qr2_followup_sixth_bindings import negative_controls
from wave20261105_gamespy_qr2_followup_sixth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_followup_sixth_fixtures import prove
from wave20261105_gamespy_qr2_followup_sixth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-followup/sixth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qf/sixth/proof'


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
    if len(matches)!=7 or sum(row['bytes'] for row in matches)!=530:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Seven complete ordinary C ARM9/main/Thumb runtime callers total530 bytes reproduce explicit-C99 compilation, original relocations and full genuine MW-linked native extents. Shared acceptance remains pending.',
        'The actual initializer clears72-byte status then carves96-byte rounded header and supplied child views using unsigned shift rounding. Both132-byte initializer and32-byte budget preserve LSR/LSL expression and32-bit overflow; previous BIC-mask drafts remain uncredited. Allocation failure, provider base changes and exact tag/size/alignment tuples are modeled without allocating through original SDK code.',
        'A112-byte resolver preserves Nintendo peer8, signed port byte order, nullable direct/fallback results,16-byte host entry and signed16 host length. Provided host data is bounded to0/4 copied bytes; malformed larger/negative lengths and actual DNS/network providers remain unqualified. The46-byte predicate only establishes measured length3..64/interior-dot behavior, with one shared failure return block.',
        'The84-byte consumer loads a function pointer at status64 and forwards raw words at52/56/68 through BLX. Native callsite99e2 separately qualifies this three-word callback view; earlier frozen producers remain raw-word views and are not migrated. Both synthetic ARM/Thumb modes, word order and caller clearing/base changes are compared; no callback body executes.',
        'All GPRs,CPSR,callee-saved registers,stack,ordered writes,external memory,original modes and provided argument/return contracts compare. Provided entropy/seed,status,error,allocation/getter/constructor,resolve/copy/mutex,wakeup/callback implementations add zero source or execution credit. No real randomness,threads,hardware,networks,game scenes,native Windows/Android or whole-game execution is established.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=7,matchedBytes=530,ordinaryCBytes=530,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
