import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_fourteenth_build import build
from wave20261105_dwc_http_next_fourteenth_bindings import negative_controls
from wave20261105_dwc_http_next_fourteenth_controls import layouts,wrong_source
from wave20261105_dwc_http_next_fourteenth_fixtures import prove
from wave20261105_dwc_http_next_fourteenth_prototypes import verify as prototype_preflight
from wave20261105_dwc_http_next_fourteenth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/fourteenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/fourteenth/proof'


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
    if len(matches)!=4 or sum(row['bytes'] for row in matches)!=604:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    abi=verify_abi()
    limits=['Four complete ordinary C internet-control functions604B match full genuine MW-linked native extents,all original relocations/generated switches and strict original Thumb/ARM entries; shared acceptance pending.',
        'Published exact-commit C/headers provide comparison/type evidence without assuming original SDK authorship. Measured final100B control,80B WDS payload,12B AC config and8B grouped globals reproduce every native offset. Raw WDS state5 and result5 remain numeric; no newer named WDS meaning is inferred.',
        'Native GetStatus sets wontExecuteWDS before fatal callback and passes second startup word1. Public StartupGetWDSInfo header has one argument; original caller suppliesR1=1 and callee saves incomingR1 inR4 then stores it at context+0x790. Source preserves the measured two-word boundary,not the outdated declaration; flag meaning remains unknown.',
        'Caller models cover null/existing globals,valid16-bit initialization arguments,byte-truncated AC configuration,actual Thumb allocator/free callback pointers,raw WDS/phase/status branches,ordered state changes,cached fields,provided helper-induced global-pointer changes and full GPR/CPSR/callee-saved/stack/ordered-write/argument tuples.',
        'All imported AC/CPS/WCM/allocator/error bodies and original BSS/callback data remain provided zero-credit contracts,including calls to other independently selected functions. No network,device/service,combined family execution,game or nativeWindows/Android behavior is proven.',
        'Only bounded valid100B controls and12B AC config storage are modeled. Reentrant provider effects are explicit fixtures,not claims about real SDK callback timing. Unknown WDS5 semantics,unbounded/invalid memory and full imported type completeness remain unqualified. Private requireprotos diagnostics prove declaration presence only.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=4,matchedBytes=604,ordinaryCBytes=604,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,originalAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
