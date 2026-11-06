import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_first_build import build
from wave20261105_dwc_http_next_first_bindings import negative_controls
from wave20261105_dwc_http_next_first_controls import layouts,wrong_source
from wave20261105_dwc_http_next_first_fixtures import prove
from wave20261105_dwc_http_next_first_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/first'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/first/proof'


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
    if len(matches)!=9 or sum(row['bytes'] for row in matches)!=706:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Nine complete ordinary C ARM9/main/Thumb HTTP/runtime callers total706 bytes reproduce explicit-C99 compilation,original relocations and genuine full MW-linked native extents. Shared acceptance remains pending.',
        'Primary published DWCAuthAlloc/Free and buffer/result headers plus independently reconstructed comparative C guide source; comparative text is not original SDK C. Native callback preloads,early inclusive-index guard,unsigned32 address delta,readonly literal imports and complete target extents are independently checked. An opcode-matching cleanup draft used different tag text and failed immutable native-string preflight; that attempt remains uncredited.',
        'Buffer allocation/failure,growth/copy/cleanup,table insertion/search/destruction,decode/raw capacity boundaries and init-byte/abort/thread-state gates compare provided contracts. Inputs bound strings to127 bytes,table rows to32,nonnegative result indexes to supplied storage,buffer growth/copies to512-byte fixture spans; negative lengths qualify rejected paths only. Arbitrary malformed pointers/indexes,size overflow,concurrency and real provider progress remain unqualified.',
        'Synthetic allocator/free ARM/Thumb modes and callback field/base/index mutations exercise cached callback identity and reload timing. Original callback destinations remain unresolved. Provider bodies and original string/storage bytes add zero source/data/execution credit; the separate60-byte getter receives only its own independently rebuilt extent once.',
        'All GPRs,CPSR,callee-saved registers,stack,ordered writes,external memory,original static modes/entries/string bytes and supplied argument/return contracts compare. No actual alloc/free,mutex/join,base64,library IO,SSL,HTTP thread,network,game scenes,native Windows/Android or whole-game execution is established.']


    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=9,matchedBytes=706,ordinaryCBytes=706,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
