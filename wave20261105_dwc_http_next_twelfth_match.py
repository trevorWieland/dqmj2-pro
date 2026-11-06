import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_dwc_http_next_twelfth_build import build
from wave20261105_dwc_http_next_twelfth_bindings import negative_controls
from wave20261105_dwc_http_next_twelfth_controls import layouts,wrong_source
from wave20261105_dwc_http_next_twelfth_fixtures import prove
from wave20261105_dwc_http_next_twelfth_prototypes import verify as prototype_preflight

LANE=ROOT/'evidence/lanes/parallel-wave20261105/dwc-http-next/twelfth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5dh/twelfth/proof'


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
    if len(matches)!=1 or sum(row['bytes'] for row in matches)!=372:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    closure=code_closure([Path(__file__).name])
    prototypes=[prototype_preflight(row,WORK/format(int(row['address'],0),'08x')/'prototype-presence')for row in matches]
    limits=['One complete ordinary C NAS date conversion372B matches full genuine MW-linked native extent,all original literal words/relocations and strict original ARM callee/data namespaces; shared acceptance pending.',
        'The public comparative NAS-time C is reconstructed/decompiler-style and contains invalid overlapping locals,incorrect strncmp and undefined return. Actual native behavior is independently recovered with published SDK RTCDate16/RTCTime12 declarations,a32B local,strcmp and unsigned month<=12. Source is ordinary C only.',
        'Original month pointer table48B,12CString pointees,date-template30B,errno4B and NAS clock20B imports have exact original words/relocation records and add zero authored-data/scaffolding credit. NAS clock signed64 base/difference use measured alignment4 offsets4/12.',
        'Bounded caller models compare all GPRs/CPSR,callee-saved registers,stack,ordered writes,exact provider tuples,errno reads and state results for12months,unknown names,years1999/2000/2006/2099,delimiter/length failures,ignored weekday,provider failures,each errno34 stage and64-bit carry/borrow/sentinel inputs.',
        'RTC_GetDateTime and RTC_ConvertDateTimeToSecond are supplied typed entry contracts; the latter returns genuine low/high words inR0/R1. Their bodies and real calendar/device/timekeeping behavior are not executed or credited. The model verifies consumed/produced struct tuples and complete caller behavior only.',
        'atoi is bounded to signed32 input results and sticky errno is modeled explicitly; malformed pointers,unbounded strings,atoi overflow,signed64 subtraction overflow,hardware/network/game/nativeWindows/Android execution remain unqualified. Published SDK declarations do not establish complete imported ABI/type correctness beyond this measured boundary.',
        'Private appended-requireprotos/-w-error diagnostic retains full function bytes/relocations and rejects the actual64-bit RTC declaration removal; declaration presence alone does not prove types. All supplied callee/libc/RTC implementations receive zero source/execution credit.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=1,matchedBytes=372,ordinaryCBytes=372,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,prototypePresencePreflight=prototypes,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
