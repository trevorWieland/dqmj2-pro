import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_match_tail_next_third_build import build
from wave20261106_dwc_match_tail_next_third_bindings import negative_controls
from wave20261106_dwc_match_tail_next_third_controls import layouts,wrong_source
from wave20261106_dwc_match_tail_next_third_fixtures import prove
from wave20261106_dwc_match_tail_next_third_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/third'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mt/third/proof'


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
        print('proved DWC C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=1006:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Six complete ordinary C command routing,binary serialization,reservation,command stop,QR2 reset and valid-connection functions1006B reproduce full genuine MW-linked native extents and all original ARM/Thumb relocations; acceptance pending.', 'Pinned comparative DWC C/header and public GameSpy pointer/enum declarations ground independently checked consumed fields. Known SBCM literal copying is expressed as ordinary memcpy of five bytes via an actually consumed string.h,then version overwrites the terminating byte; original aliased CString is uncredited. Unsigned Aid shift retains native bytes and defines bit31 portably.', 'Bounded independent caller models cover commands1/2/6/8/9/255,routing across match types0..3/distant flag,NULL/empty/32word data,binary negative/oversize count clamp,20..148byte wire records,DNS error retry exhaustion,GP512byte message truncation,all-bit bitmap counts,deferred and server-derived reservations,prior request choice,and64bit tick carry/wrap. Source-specific wrong-C variants must genuinely link and return with observable model violations.', 'All GPRs,CPSR,callee-saved/stack,ordered writes,complete argument tuples and produced external memory compare between actual native and rebuilt caller. Incoming stack argument slots may be rewritten inside the caller own frame,as the original6argument sender does.', 'Selected sibling functions remain opaque imported entry contracts when testing another caller; each sibling is independently proved only in its own complete row. Getter,formatter,copies,clock,GameSpy server/address/network providers and imported literal/BSS bytes add zero supplied-body/storage execution or source credit; no real network,device,game,Windows or Android execution is established.', 'Invalid pointers,tracked commands with payloads over32words,negative text lengths,real concurrent getter changes,and unbounded provider behavior remain outside semantic coverage. Explicit required-prototype diagnostics prove declaration presence,not complete imported type correctness. NN startup592B stays unselected after a bounded register-allocation mismatch.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=1006,ordinaryCBytes=1006,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
