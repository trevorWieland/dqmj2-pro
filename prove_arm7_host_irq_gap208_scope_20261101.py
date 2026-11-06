import hashlib
import json
from pathlib import Path
import match_runtime
import arm7_host_irq_gap208_native_20261101 as native
import link_arm7_bulk_20261030 as linker
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB
from project import ROOT,sha256,write_json

REPORT=ROOT/'evidence/attempts/arm7-host-irq-gap208-scope-20261101.json'
WRAM_SHA='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
GAP_SHA='be91eb7ca24e0a1d7fee1cea28f46ded6bd0e4f754b3970779ecdb50a8feb118'
START,END,BASE=0x037FB6C8,0x037FB798,0x037F8000


def boundary():
    modules,functions=linker.namespace('')
    path=ROOT/modules['arm7-wram']['binary'];raw=path.read_bytes()
    if sha256(path)!=WRAM_SHA or linker.digest(raw[START-BASE:END-BASE])!=GAP_SHA:
        raise ValueError('Qualified host IRQ initialized input changed')
    if any(address in functions for address in range(START,END,4)):
        raise ValueError('Historical host IRQ gap unexpectedly has configured entries')
    inventory=json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    overlaps=[dict(parent=row['address'],mode=row['mode'],begin=begin,end=end)for row in inventory
        if row['module']=='arm7-wram'for begin,end in row['ranges']if int(begin,0)<END and START<int(end,0)]
    if overlaps!=[dict(parent='0x37fb488',mode='arm',begin='0x37fb748',end='0x37fb78c')]:
        raise ValueError('Historical host IRQ discontiguous shared-body association changed')
    entries=[]
    for index in range(8):
        address=START+16*index;body=raw[address-BASE:address-BASE+16]
        if body[:4]!=bytes.fromhex('04c09fe5') or body[4:8]!=(0xE3A00000|index).to_bytes(4,'little') or body[8:12]!=bytes.fromhex('1cff2fe1') or int.from_bytes(body[12:16],'little')!=0x037FB63C:
            raise ValueError('Host IRQ wrapper instruction/literal role changed')
        entries.append(dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(address),
            bytes=16,codeBytes=12,literalBytes=4,alignmentBytes=0,fullRangeSha256=linker.digest(body),
            literalWords=[dict(address=hex(address+12),value='0x37fb63c',role='qualified-configured-ARM-tail-dispatcher')],
            callbackIndex=index,normalReturnViaOriginalIncomingLr=True))
    address=0x037FB748;body=raw[address-BASE:END-BASE]
    pools=[int.from_bytes(body[offset:offset+4],'little')for offset in(68,72,76)]
    if pools!=[0x027FFC3C,0x03807680,0x0380FFF8]:
        raise ValueError('Host IRQ counter-handler literal roles changed')
    entries.append(dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(address),
        bytes=80,codeBytes=68,literalBytes=12,alignmentBytes=0,fullRangeSha256=linker.digest(body),
        literalWords=[dict(address=hex(address+68+4*index),value=hex(value),role=role)for index,(value,role)in enumerate(zip(pools,
            ['absolute-shared-counter-word-not-module-BSS','initialized-callback-record-base','reserved-interrupt-check-word']))],
        callbackIndex=8,normalReturnViaOriginalIncomingLr=True))
    table=[int.from_bytes(raw[0xF564+4*i:0xF568+4*i],'little')for i in range(25)]
    expected={0:0x037FB748,3:0x037FB708,4:0x037FB718,5:0x037FB728,6:0x037FB738,
        8:0x037FB6C8,9:0x037FB6D8,10:0x037FB6E8,11:0x037FB6F8}
    if table!=[expected.get(i,0x037FB638)for i in range(25)]:
        raise ValueError('Initialized host IRQ table/root mappings changed')
    index_table=[int.from_bytes(raw[0xF550+2*i:0xF552+2*i],'little')for i in range(9)]
    if index_table!=list(native.BITS):raise ValueError('Initialized host callback-index to IRQ-bit mapping changed')
    roots={int(row['address'],0)for row in entries};references=[];branches=[]
    for module in modules.values():
        binary=(ROOT/module['binary']).read_bytes();base=int(module['base'],0)
        for offset in range(0,len(binary)-3,4):
            value=int.from_bytes(binary[offset:offset+4],'little')
            if START<=value&~1<END:
                references.append(dict(module=module['id'],address=hex(base+offset),value=hex(value),
                    entryRoot=(value&~1)in roots,thumbTagged=bool(value&1),classification='bounded-aligned-word-reference-not-all-words-proven-pointers'))
        for row in inventory:
            if row['module']!=module['id']:continue
            decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM if row['mode']=='arm'else CS_MODE_THUMB);decoder.detail=True
            for begin,end in row['ranges']:
                begin,end=int(begin,0),int(end,0)
                for instruction in decoder.disasm(binary[begin-base:end-base],begin):
                    if instruction.mnemonic.startswith('b')and instruction.operands and instruction.operands[0].type==2:
                        target=instruction.operands[0].imm&0xFFFFFFFF
                        if START<=target<END:
                            branches.append(dict(module=module['id'],address=hex(instruction.address),target=hex(target),mnemonic=instruction.mnemonic,entryRoot=target in roots,
                                sourceInsideSameUnit=any(int(unit['address'],0)<=instruction.address<int(unit['address'],0)+unit['codeBytes']and int(unit['address'],0)<=target<int(unit['address'],0)+unit['codeBytes']for unit in entries)))
    if any(not row['entryRoot']or row['thumbTagged']for row in references)or any(not row['entryRoot']and not row['sourceInsideSameUnit']for row in branches):
        raise ValueError('Unreconciled host IRQ interior/mode reference')
    data_refusals=[]
    for target in(0x027FFC3C,0x0380FFF8):
        try:linker.data_binding({'program':''},target,modules)
        except ValueError as error:
            if str(error)!='Unqualified external ARM7 data target: '+hex(target):raise
            data_refusals.append(dict(address=hex(target),originalRefusal=str(error)))
        else:raise ValueError('Original external-word data guard was loosened')
    inputs=[dict(path=module['binary'],sha256=sha256(ROOT/module['binary']))for module in modules.values()]
    inputs.append(dict(path='evidence/arm7/ghidra-runtime-inventory.json',sha256=sha256(ROOT/'evidence/arm7/ghidra-runtime-inventory.json')))
    return dict(program='',processor='arm7',module='arm7-wram',mode='arm',initializedModuleSha256=WRAM_SHA,
        start=hex(START),end=hex(END),bytes=208,codeBytes=164,literalBytes=44,alignmentBytes=0,rangeSha256=GAP_SHA,
        entries=entries,inputs=inputs,initializedDenominatorDelta=0,sourceCredit=0,
        historicalGhidraDiscontiguousCodeAssociation=overlaps,whollyUnconfiguredWrapperBytes=128,
        separatelyCallableHandlerContainingExistingIsrCode=dict(bytes=80,existingGhidraCodeBytes=68,literalBytes=12,
            canonicalEntryMissing=True,configuredParent='0x37fb488',sourceCredit=0),
        irqVectorTable=dict(address='0x3807564',words=[hex(value)for value in table],bytes=100,sourceCredit=0),
        irqBitIndexTable=dict(address='0x3807550',halfwords=index_table,bytes=18,followingAlignmentBytes=2,sourceCredit=0),
        boundedAlignedWordReferences=references,boundedConfiguredDirectBranchReferences=branches,
        unresolvedOpaqueIndirectReferenceCoverage=True,originalDataGuardRefusals=data_refusals,
        originalNamespaceUnchanged=not any(address in linker.namespace('')[1]for address in roots),
        platformWordSourceBindingApproved=False,assemblyJustificationAdopted=False,
        staticConsumer=dict(address='0x37fb488',tableLiteral='0x37fb4ec',table='0x3807564',
            observedInstructions=[dict(address='0x37fb4dc',operation='LDR table literal'),dict(address='0x37fb4e0',operation='LDR target by interrupt bit'),
                dict(address='0x37fb4e8',operation='BX target')],actualHardwareExceptionEntryClaim=False),
        existingDispatcher=dict(address='0x37fb63c',bytes=140,codeBytes=120,literalBytes=20,scopeCredit=0),
        boundsLimitations=['Configured direct branches and aligned initialized words across the three measured host ARM7 modules only',
            'No exhaustive computed pointer, runtime-mutated vector, cross-processor or arbitrary malformed-index proof',
            'Nine callable gap entries are inventory evidence only; original objects/gap bytes remain zero-credit scaffolding'])


def produce():
    evidence=boundary();execution=native.run()
    generators=[Path(__file__).name,'arm7_host_irq_gap208_native_20261101.py','arm7_host_irq_gap208_native_engine_20261101.py']
    return dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),
        generators=[dict(path=path,sha256=sha256(ROOT/path))for path in generators],boundary=evidence,native=execution,
        sourceCredit=0,nativeCodeCredit=0,initializedDataCredit=0,initializedDenominatorDelta=0,
        ordinarySourceReconstructionPending=True,completeImageClaim=False)


def validate(report):
    if report.get('boundary')!=boundary():raise ValueError('Current qualified boundary/reference/data-guard evidence differs')
    if any(report.get(key)!=0 for key in('sourceCredit','nativeCodeCredit','initializedDataCredit','initializedDenominatorDelta')):
        raise ValueError('Read-only host gap witness cannot grant source or denominator credit')
    if not report.get('ordinarySourceReconstructionPending')or report.get('completeImageClaim'):
        raise ValueError('Host gap completeness/evidence class differs')
    expected_generators=[dict(path=path,sha256=sha256(ROOT/path))for path in(Path(__file__).name,'arm7_host_irq_gap208_native_20261101.py','arm7_host_irq_gap208_native_engine_20261101.py')]
    if report.get('schemaVersion')!=1 or report.get('generator')!=Path(__file__).name or report.get('generatorSha256')!=sha256(__file__)or report.get('generators')!=expected_generators:
        raise ValueError('Complete host gap generator closure differs')
    for pin in report['generators']:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Host gap proof generator changed')
    evidence=report['native'];trace=evidence['trace'];path=ROOT/trace['path']
    if sha256(path)!=trace['compressedSha256']:raise ValueError('Host gap native compressed trace unavailable or changed')
    import gzip
    raw=gzip.decompress(path.read_bytes())
    if linker.digest(raw)!=trace['rawSha256']:raise ValueError('Host gap native raw trace changed')
    records=json.loads(raw);counts={hex(0x037FB63C):96,hex(0x037FB748):12}
    counts.update({hex(START+16*i):12 for i in range(8)})
    actual={key:0 for key in counts}
    for seed,(case,row)in enumerate(zip(native.cases(),records)):
        if row['case']!=case or row['entry']not in actual or not row['execution']['actualReturn']or not row['allCompleteMemoryAndOrderedEffectsValidated']or row['providerReplacements']or row['sourceCredit']!=0:
            raise ValueError('Host gap original native case/actual-return evidence differs')
        if len(row['prefixes'])!=2 or not all(prefix['actualReturn']for prefix in row['prefixes'])or row['execution']['error']is not None or int(row['execution']['pc'],0)!=native.engine.RETURN:
            raise ValueError('Host gap actual initializer/installer/entry termination differs')
        actual[row['entry']]+=1
    if len(records)!=204 or actual!=counts or evidence['actualOwnedNativeReturns']!=204 or evidence['actualInitializerAndInstallerReturnsSeparate']!=408:
        raise ValueError('Host gap original own/prefix return counts differ')
    callbacks=sum(sum(int(frame['entry'],0)in(native.CALLBACK,0x037FB638)for frame in row['execution']['nestedReturns'])for row in records)
    tails=sum(len(row['execution']['tailTransfers'])for row in records)
    if any(evidence.get(key)!=0 for key in('sourceCredit','nativeCodeCredit','dataCredit')):
        raise ValueError('Native-only execution cannot grant source/data credit')
    if callbacks!=102 or tails!=96 or evidence['actualCallbackReturnsSeparate']!=102 or evidence['actualTailWriterTransfersSeparate']!=96 or evidence['fullOwnCodeCoverageBytes']!=284 or evidence['unvisitedCode']:
        raise ValueError('Host gap original nested/tail/code coverage differs')
    if evidence['unsupportedReturnCredit']!=0 or evidence['unsupportedControls'][0]['execution']['actualReturn']:
        raise ValueError('Host gap exhausted execution acquired return credit')
    return dict(qualifiedGapEntries=9,qualifiedGapInitializedBytes=208,actualGapEntryReturns=108,existingDispatcherReturnsSeparate=96,
        sourceCredit=0,initializedDenominatorDelta=0)


def main():
    report=produce();validate(report);write_json(REPORT,report)
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),validation=validate(report))),flush=True)


if __name__=='__main__':main()
