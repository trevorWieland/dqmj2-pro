import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_tenth_build import build
from wave20261105_dwc_http_next_tenth_bindings import negative_controls
from wave20261105_dwc_http_next_tenth_controls import layouts,wrong_source
from wave20261105_dwc_http_next_tenth_fixtures import prove
from wave20261105_dwc_http_next_tenth_prototypes import verify as prototype_preflight
from wave20261105_dwc_http_next_tenth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/tenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/tenth/proof'


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
    if len(matches)!=8 or sum(row['bytes'] for row in matches)!=522:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    abi=verify_abi(matches)
    limits=['Eight complete ordinary C common-string/error/memory functions total522B reproduce full genuine MW-linked native extents,original relocations/static modes and natural22-case generated switch table. Shared acceptance remains pending.',
        'Exact-commit published C/headers are comparison/declaration evidence; original SDK authorship is not assumed. Measured8B error and reversed free/alloc storage are typed zero-credit BSS imports. Additional native error codes20/21 retain raw numeric labels and actual type2 table targets.',
        'Source retains standard strlen/strchr/strncmp/strncpy spellings in consumed private string.h; a new scoped mapper binds only their exact original ARM entries. The rejected alias-spelling attempt remains diagnostic evidence. No shared helper map or compiler flags changed.',
        'Error fixtures cover fatal9 preservation,output-pointer null/alias behavior and raw code mapping. Memory fixtures cover null/failed/success callbacks,both ARM/Thumb callback modes,32B imported allocation headers,forwarded alignment,ignored old-size argument and minimum-length copying within supplied512B backing. Original header/callback bodies remain supplied contracts.',
        'Common fixtures cover signed separators,prefix/nonmatching keys,empty/last values,formatter4096 capacity and an independent split-pair output oracle. Getter separators are nonzero; all strings/outputs valid and bounded. Arbitrary malformed pointers/strings,oversize/overflow,real allocation safety,game/network/native Windows/Android behavior remain unqualified.',
        'Private appended-requireprotos/-w-error positive checks preserve complete function bytes/relocations; removing actual declarations rejects six calling functions. The two call-free error routines have no imported-call removal case. Declaration presence alone does not prove types.',
        'All GPRs/CPSR,callee-saved registers,stack,ordered writes,external memory and provider tuples compare. Original strings/BSS/allocation-header data and all supplied callback/libc/header/free implementations or executions add zero source credit.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=8,matchedBytes=522,ordinaryCBytes=522,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalAbiProof=abi,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
