import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_eighteenth_build import build
from wave20261105_gamespy_qr2_next_eighteenth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_eighteenth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_eighteenth_fixtures import prove
from wave20261105_gamespy_qr2_next_eighteenth_abi import verify as verify_abi
from wave20261105_gamespy_qr2_next_eighteenth_helper import prove as prove_helper

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/eighteenth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/eighteenth/proof'


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
    if len(matches)!=10 or sum(row['bytes'] for row in matches)!=1366:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches);helper=prove_helper()
    closure=code_closure([Path(__file__).name])
    limits=['Ten complete ordinary C host ARM9/main/Thumb bodies total1366 bytes and match fresh source compilation, unchanged original relocations and genuine MW linking; shared acceptance pending.',
        'The coherent subset covers NAT packet dispatch194 and QR2 initialization364,think44,receive96,heartbeat204,statechange72,shutdown104,local-IP enumeration64,peer-address108 andpublic-address116. Exact source uses measured Nintendo peer8, scalar byte-order macros and exact socket-1 checks; no optimizer permutation or ASM substitution was used.',
        'The measured full QR2 C view is3476 bytes, with userdata268/backend byte272 and a3200-byte IP-verify array at276. The two newer public callback fields are absent. Original callers retain the IP-verify expiry and memset boundaries but omit NNThink/NNFree and newer connected-callback initialization. These are explicit measured source-context differences, not a claim that the entire comparison SDK revision is identified.',
        'Original initializer has14 incoming words: four registers and10 stack words at entry SP+0..36. Six incoming callback-pointer words are stored unchanged without invocation. The two selected indirect callback sites remain unresolved runtime inputs and are tested using synthetic ARM/Thumb targets only.',
        'The full original524-byte signed divide helper separately returns45 checked R0 quotient/R1 remainder pairs for positive nonzero divisors and signed numerators, including INT_MIN. Initializer7264 calls it and726e consumes R1 as a byte. Its separate ABI probe adds no helper reconstruction credit; caller fixtures provide this measured two-register contract.',
        'Bounded vectors compare all GPRs,CPSR,callee-saved registers,stack balance,ordered writes and original import entry modes. They cover initialized words and exact caller/helper boundaries, raw error/enum bits, timer equality/wrap, callback/helper side effects, packet prefix snapshots, receive ownership and allocator/static-record branches.',
        'Packet dispatch models assume at least21 accessible input bytes even for rejected lengths. QR2 initializer vectors use successful supplied allocation and bounded terminated names; allocation failure, overflowing names, scanner failure and real networking are unproved. A supplied receive-2 vector deliberately measures the native exact-1 branch and its neighboring hostname-byte write; it is not a claim that the OS normally returns-2.',
        'Original global storage, imported helper implementations, unresolved callback implementations, actual networking/devices/scenes, complete game and native Windows/Android execution receive zero added source/execution credit.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=10,matchedBytes=1366,ordinaryCBytes=1366,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,originalSignedDivisionHelperAbiProof=helper,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
