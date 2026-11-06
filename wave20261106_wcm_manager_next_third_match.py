import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_third_build import build
from wave20261106_wcm_manager_next_third_bindings import negative_controls
from wave20261106_wcm_manager_next_third_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_third_fixtures import prove
from wave20261106_wcm_manager_next_third_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/third'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/third/proof'


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen runtime dependency changed',pin['path']))
    if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('Measured ROM identity changed')
    interface=read_json(LANE/'work-view-interface.json')
    if interface['portableCDeclarationResolved']or interface['sourceOrStorageCredit']!=0:raise ValueError('Unresolved WCM view ABI debt erased')
    for pin in interface['headers']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen WCM view evidence changed')
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
        print('proved WCM C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=1868:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Six complete ordinary C WCM callback/search functions1868B reproduce full genuine MW-linked native extents and every original branch/data/callback relocation. The common callback preserves its actual same-entry Thumb function pointer;no recursive or supplied callback body executes.', 'Forty-three typed layout checks ground consumed192B BSS descriptor fields,80B WEP key/mode/id positions,68B scan record,48B DCF receive header and12B callback. Game-information128B,OS alarm and other opaque work bytes remain unqualified. No source credit is granted to pointed storage.', 'Bounded models cover API/error dispatch,provider error classes,WEP/power/auth arguments,notice data selection,disconnect/auth reset,DCF data dispatch/RSSI byte/cache range,connection-loss/reset/camouflage-rate transitions,search phase gates and32bit scan-count wrap.', 'All real WM/cache/interrupt,phase,notification,scan-parameter,RSSI and receive providers remain opaque. Fixtures preserve work/configuration inputs across supplied calls unless explicit outputs are provided;real asynchronous effects,reentrancy,IRQ/cache/concurrency,wireless service/game and host behavior are unproved.', 'The mandatory work-view-interface receipt preserves different frozen opaque-prefix aggregate declarations from earlier packets. Matching native pointer representation and all consumed offsets does not prove ISO C compatible aggregate declarations across translation units. Portable shared Work declaration remains unresolved;future zero-byte migration must preserve every native match.', 'All GPRs/CPSR,callee-saved registers,stack,ordered writes,bounded external memory and exact provider tuples compare. Strict declaration checks establish presence only. No ordered observed-read addresses are configured;invalid pointers,oversized/uninitialized receive buffers,actual helper memory effects and unbounded asynchronous outcomes remain unqualified.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=1868,ordinaryCBytes=1868,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        abiInterfaceEvidence=[dict(path=(LANE/'work-view-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'work-view-interface.json'))],portableCWorkDeclarationResolved=False,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
