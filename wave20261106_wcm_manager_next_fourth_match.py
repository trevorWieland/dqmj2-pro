import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_wcm_manager_next_fourth_build import build
from wave20261106_wcm_manager_next_fourth_bindings import negative_controls
from wave20261106_wcm_manager_next_fourth_controls import layouts,wrong_source
from wave20261106_wcm_manager_next_fourth_fixtures import prove
from wave20261106_wcm_manager_next_fourth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/wcm-manager-next/fourth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w6wc/fourth/proof'


def main():
    inputs=read_json(INPUT)
    for pin in inputs['files']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError(('Frozen runtime dependency changed',pin['path']))
    if inputs['romSha256']!=configuration()['romSha256']:raise ValueError('Measured ROM identity changed')
    interface=read_json(LANE/'work-view-interface.json')
    if interface['portableCDeclarationResolved']or interface['sourceOrStorageCredit']!=0:raise ValueError('Unresolved WCM view ABI debt erased')
    for pin in interface['headers']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Frozen WCM view evidence changed')
    qualification=read_json(LANE/'helper-contract-qualification.json')
    if qualification['sourceCredit']!=0 or not qualification['earlierFrozenReportsUnchanged']:raise ValueError('Legacy helper qualification differs')
    arrays=read_json(LANE/'imported-array-provenance.json')
    if arrays['sourceOrStorageCredit']!=0 or not arrays['actualNativeAndPublicCInitializersAgree']:raise ValueError('Imported arrays improperly credited')
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
    if len(matches)!=6 or sum(row['bytes'] for row in matches)!=1300:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['Six complete ordinary C WCM connection/scan/AP callers1300B reproduce genuine MW-linked native full extents and original branch/data/callback identities. Every object and canonical report rebuilds freshly from source.', 'Fifty-seven typed layout checks cover192B BSS,82B WEP input,208B AP node,112B scan callback,68B scan record and measured work buffer offsets. Game-information128B and other documented opaque internals remain unqualified;no pointed storage receives source credit.', 'Bounded models cover connection phase/BSS/game-info/WEP validation,82-byte or80-byte clear/copy distinctions,support-rate update,scan-filter/string and SSID32-byte boundaries,scan callback arrays0..2,round-scan divisors/count wrap,AP lock/clear/point outcomes and original typed mode boundaries.', 'Original ARM CountBits0208a66c and CLZ0208a690 primitives,plus unsigned division02026350,are supplied opaque arithmetic contracts. No helper implementation,inline assembly,original code object or patched instruction is supplied;all authored caller algorithm bytes remain ordinary C. Real helper bodies execute zero times and receive zero source credit.', 'Fixtures supply phase-word,notification-id and option-provider effects and byte copy/fill contracts without executing real callees. Real alarm/IRQ/cache/asynchronous provider effects,wireless service/concurrency/game and host behavior remain unproved. Static BSSID6/ESSID32 all-ones wildcard arrays match public/native bytes but remain imported zero-credit storage.', 'The mandatory work-view interface receipt retains incompatible private aggregate declarations across frozen TUs and the typed getter pointer boundary as portable-interface debt. No complete host ABI or shared Work declaration is claimed. All GPRs/CPSR,stack,ordered writes,output memory and provider tuples compare;no ordered observed-read addresses are configured.', 'Fixtures use valid fixed-size32-byte SSID backing,receive buffers and0..2 callback entries. Invalid/unbounded pointers/counts,reentrant provider changes,actual AP storage management and complete network lifecycle are outside dynamic coverage. Whole native/link equality independently covers every static branch.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=6,matchedBytes=1300,ordinaryCBytes=1300,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        abiInterfaceEvidence=[dict(path=(LANE/'work-view-interface.json').relative_to(ROOT).as_posix(),sha256=sha256(LANE/'work-view-interface.json'))],portableCWorkDeclarationResolved=False,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
