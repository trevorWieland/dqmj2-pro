import re
from pathlib import Path
from project import ROOT,configuration,read_json,write_json,sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261105_gamespy_qr2_next_twentieth_build import build
from wave20261105_gamespy_qr2_next_twentieth_bindings import negative_controls
from wave20261105_gamespy_qr2_next_twentieth_controls import layouts,wrong_source
from wave20261105_gamespy_qr2_next_twentieth_fixtures import prove
from wave20261105_gamespy_qr2_next_twentieth_abi import verify as verify_abi

LANE=ROOT/'evidence/lanes/parallel-wave20261105/gamespy-qr2-next/twentieth'
INPUT=LANE/'inputs.json'
WORK=ROOT/'work/w5qr/twentieth/proof'


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
    if len(matches)!=13 or sum(row['bytes'] for row in matches)!=1518:raise ValueError('Selected immutable packet membership changed')
    layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'layout')for row in matches];wrong_layout=[layouts(row,WORK/format(int(row['address'],0),'08x')/'wrong-layout',True)for row in matches];bindings=negative_controls(matches)
    abi=verify_abi(matches)
    closure=code_closure([Path(__file__).name])
    limits=['Thirteen complete ordinary C host ARM9/main/Thumb GT2 receive/delivery bodies total1518 bytes and match fresh source compilation, unchanged original relocations and genuine MW linking; shared acceptance pending.',
        'Published handler definitions were exposed in private diagnostic compilation because omitting the unknown platform receiver had allowed the compiler to delete its entire unused static handler graph. Final source is split into13 ordinary C units with complete typed prototypes; no algorithm ASM, patched instructions or allocation permutation search was used.',
        'Measured typed context is160-byte connection,76-byte socket,12-byte buffers and16-byte incoming/outgoing message records. Cases cover phase/error forwarding, reliable/unreliable type dispatch, 16-bit serial wrap and signed differences, buffer capacity equality, duplicate/overflow behavior, held-message restart, sequence advancement, challenge buffers and ping elapsed-time wrap.',
        'Buffering caller passes original comparator pointer020b4ac9 with actual canonical host ARM9/main/Thumb entry020b4ac8,size12. The original pointer load/addend/tag/callee namespace is checked separately from actual Thumb call opcodes. The comparator body is neither authored nor executed by caller fixtures.',
        'Original buffer caller re-stores the unchanged sixth incoming overflow-pointer word at entrySP+4, instruction020b4ade. Only this new fixture permits that exact caller/address/width/value idempotent spill; original prologue/load/store evidence is retained. All other write bounds and old frozen fixtures remain unchanged.',
        'The16-byte incoming-message local initializes14 bytes and leaves padding14..15 unspecified. Independent ArrayInsertSorted projection reads only the initialized14-byte prefix; source/native caller machine traces still compare all GPRs,CPSR,callee-saved registers,stack and ordered writes completely.',
        'Array/auth/filter/error/delivery/clock/buffer implementations are supplied ABI contracts and receive no extra source/execution credit. Packet lengths with rejected/negative values still have accessible fixture buffers; no unsafe network input handling, actual service/device/scenes, complete game or native Windows/Android execution is inferred.']

    write_json(LANE/'match.json',dict(schemaVersion=1,romSha256=inputs['romSha256'],moduleSha256=inputs['moduleSha256'],program='',processor='arm9',module='main',allPassed=True,
        matches=matches,matchedFunctions=13,matchedBytes=1518,ordinaryCBytes=1518,justifiedAssemblyBytes=0,sourceOnlyCompilerInputs=True,
        actualNativeAndSourceCallerReturns=sum(model['actualNativeAndSourceCallerReturns'] for model in models),boundedCallerModels=models,
        suppliedCalleeSourceOrExecutionCredit=0,hardwareOrGameExecutionCredit=0,typedLayoutChecks=layout,negativeLayoutEvidence=wrong_layout,
        negativeEvidence=wrong,negativeOriginalBindingEvidence=bindings,sourceOnlyCanonicalReplayRequired=True,originalCallerAbiProof=abi,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),generatorSources=[dict(path=name,sha256=sha256(ROOT/name)) for name in closure],
        replayDependencies=[dict(path=INPUT.relative_to(ROOT).as_posix(),sha256=sha256(INPUT))],freshCompileObjectsAndLinkedReportsEveryRun=True,limits=limits))


if __name__=='__main__':main()
