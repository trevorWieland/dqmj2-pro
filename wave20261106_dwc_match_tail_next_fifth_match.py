import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_match_tail_next_fifth_build import build
from wave20261106_dwc_match_tail_next_fifth_bindings import negative_controls
from wave20261106_dwc_match_tail_next_fifth_controls import layouts,wrong_source
from wave20261106_dwc_match_tail_next_fifth_fixtures import prove
from wave20261106_dwc_match_tail_next_fifth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-match-tail-next/fifth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6mt/fifth/proof'


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
    if len(matches)!=7 or sum(row['bytes'] for row in matches)!=1106:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Seven complete ordinary C receive/host-list/server-status/handshake/closing functions1106B reproduce whole genuine MW-linked native extents and exact original ARM/Thumb import entries; source credit remains pending shared acceptance.', 'Pinned comparative DWC sources and explicit public transport/error/main/friend/common/SDK declarations ground consumed enums,fields and interfaces. Source-visible shared unsigned-format CString preserves native literal pooling under pinned noreuse compilation; original CString/storage bytes add zero authorship. All authored source remains C with no object/instruction patches.', 'Independent bounded models cover0..128 parsed numeric segments with15-byte temporary bounds,high-bit command/profile words,provided strtoul overflow behavior,missing/present host ids andNULL controller,close-state exclusions,SC status counts,handshake types2/3/4,indices0..31,bit31 Ack masks,latency comparison,ack completion loops,cancellation/cookie/close paths and64bit tick values.', 'The168-byte sender writes only one or three payload bytes for SYN,two for SYN_ACK,andnone for ACK,while passing4bytes. Only those defined prefixes have an independent semantic oracle. All four actual wire bytes,including indeterminate stack-tail bytes,compare between concrete native and rebuilt executions; their values and portable C/network meanings remain unqualified. Uninitialized outputs are not represented as initialized game semantics.', 'All GPRs/CPSR,callee-saved/stack,ordered writes,complete provider argument tuples and output memory compare. Phase-word read observation is not configured and adds no ordered phase-read proof. Required-prototype diagnostics prove declaration presence only; imported type completeness remains unqualified.', 'Numeric parsing,key/value constructors,clock,state/getter/error handlers,original sibling bodies,GT2/NN/GP/reliable-send providers are supplied opaque fixture boundaries. Synthetic key/value serialization is only a fixture effect. Their real bodies,callbacks/concurrency,network/devices/game/nativeWindows/Android execution and original storage receive zero source or execution credit.', 'Invalid pointers,host counts or Aid indices above31,segments exceeding15 bytes,signed/invalid numeric text,unbounded provider behavior,and unobserved state changes remain outside semantic fixtures. Coalescing residuals including388-byte deletion and124-byte valid-Aid list remain reserved/uncredited.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=7,matchedBytes=1106,ordinaryCBytes=1106,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
