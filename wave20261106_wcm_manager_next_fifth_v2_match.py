import re,hashlib
from pathlib import Path
from closed_c_compiler_inputs_20261105 import compiler_inputs
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_fifth_v2_build import build
from wave20261106_wcm_manager_next_fifth_v2_prototypes import function_bytes
from wave20261106_wcm_manager_next_fifth_v2_bindings import negative_controls
from wave20261106_wcm_manager_next_fifth_v2_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_fifth_v2_fixtures import prove
from wave20261106_wcm_manager_next_fifth_v2_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/fifth-v2'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/fifth-v2/proof'


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen runtime dependency changed',pin['path']))
    if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('Measured ROM identity changed')
    interface=read_json(LANE/'work-view-interface.json')
    if interface['portableCDeclarationResolved']or interface['sourceOrStorageCredit']!=0:raise ValueError('Unresolved WCM view ABI debt erased')
    for pin in interface['headers']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen WCM view evidence changed')
    subobject=read_json(LANE/'cpsif-subobject-provenance.json')
    if subobject['sourceOrStorageCredit']!=0 or not subobject['objectRelocationsUnmodified']or(subobject['fieldOffset'],subobject['fieldExtent'])!=(12,24):raise ValueError('CPSIF subobject provenance changed')
    correction=read_json(LANE/'directive-phase2-correction.json')
    if correction['sourceCredit']!=0 or not correction['genericSourceOnlyGateUnchanged']or not correction['unchangedGenericGateRejectsOriginalAndAcceptsAllNineNew']:raise ValueError('Directive correction qualification differs')
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
        change=next(x for x in correction['records']if x['address']==row['address']);old=change['oldSourceExactText'].encode()
        if hashlib.sha256(old).hexdigest()!=change['oldSourceSha256']or re.sub(rb'\\\r?\n',b'',old)!=source.read_bytes():raise ValueError('Only C phase2 continuation splicing is permitted')
        for pin in change['headerHashesUnchanged']:
            if sha256(source.parent/pin['name'])!=pin['sha256']:raise ValueError('Correction changed an original private header')
        for key,value in change['legacyContract'].items():
            if row[key]!=value:raise ValueError(('Pre-correction native/compiler/relocation contract changed',key))
        if hashlib.sha256(function_bytes(ROOT/row['object'],row['name'])).hexdigest()!=change['oldObjectFunctionSha256']:raise ValueError('Correction changed complete raw object function bytes')
        closed=compiler_inputs(row)
        model=prove(row,native,body);models.append(model)
        wrong.extend(wrong_source(row,directory/'wrong-C'))
        row.update(program='',sourceLanguage='C',ordinaryCOnly=True,ordinaryCBytes=row['bytes'],justifiedAssemblyBytes=0,justifiedAssemblyRanges=[],
            sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceProvenance=item['sourceProvenance'],
            matchingBytesScope='Complete genuine MW-linked native caller extent including original literal pool',
            actualNativeAndSourceCallerReturns=model['actualNativeAndSourceCallerReturns'],suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,
            boundaryReturnContract=item['boundaryReturnContract'],closedCCompilerInputs=closed,phase2OnlyPreprocessingCorrectionVerified=True)
        matches.append(row)
        print('proved WCM C',row['address'],row['bytes'],model['cases'],flush=True)
    if len(matches)!=9 or sum(row['bytes'] for row in matches)!=1056:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Nine complete ordinary C WCM connection/AP/CPSIF functions1056B reproduce all genuine MW-linked native bytes and original call/data/callback identities. No imported object,callee or pointer storage receives source credit.', 'Seventy typed layout assertions include26B connection callback,208B AP nodes,8B thread queue,24B mutex and44B CPSIF record. Null-send uses genuine ABS32 source addend12 from the canonical CPSIF base to its mutex;the original literal,effective address,source addend,field offset and all object relocation payloads remain unchanged.', 'Bounded models cover connection AID1/2007/invalid boundaries,state26 no-op and error/status flows;AP entry/allocator/search/reordering/count/occupied-slot outcomes;null-packet lock/error boundaries;MAC/SSID pointer/optional length results and receive-callback pointer storage.', 'SDK version macros follow the pinned public header only to qualify the consumed conditional. Matching the state26 branch does not identify the exact original SDK release. Work/OS/WM aggregate interoperability remains debt in mandatory interface evidence;no complete host ABI is claimed.', 'Fixture phase/notification,memory copy,allocator/search/table providers and IRQ mutex/transmit contracts are supplied without executing their real bodies. Caller allocator/search/append bodies execute only in their separate top-level cases. No actual IRQ/thread/sleep/concurrency,WM service/network/game or native host behavior is proved.', 'All GPRs/CPSR,stack,ordered writes,bounded external memory and exact provider tuples compare. Required declarations prove presence only;no ordered observed-read addresses are configured. AP tables have0..3 backed nodes and bounded counts/occupancy masks,including intentional inconsistent count cases where native returns an occupied last candidate. Cycles,unbounded/negative buffers,invalid narrow arguments and real provider sideeffects remain outside coverage.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=9,matchedBytes=1056,ordinaryCBytes=1056,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        abiInterfaceEvidence=[dict(path=(LANE/'work-view-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'work-view-interface.json'))],portableCWorkDeclarationResolved=False,
        preprocessingCorrectionEvidence=dict(path=(LANE/'directive-phase2-correction.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'directive-phase2-correction.json')),genericSourceOnlyGateUnchanged=True,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
