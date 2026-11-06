import gzip
import json
from pathlib import Path
import match_runtime
import arm7_host_sleep_callback32_native_20261101 as native
import link_arm7_bulk_20261030 as linker
from project import ROOT,sha256,write_json
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB

REPORT=ROOT/'evidence/attempts/arm7-host-sleep-callback32-scope-20261101.json'
ENTRY,SIZE,CODE=0x037FC50C,32,28
TARGET='d11759af4c00f6095ef8640029715d7105d6df2a035253e5de49d80c3b38331a'


def boundary():
    modules,functions=linker.namespace('');wram=(ROOT/modules['arm7-wram']['binary']).read_bytes()
    if sha256(ROOT/modules['arm7-wram']['binary'])!=native.engine.WRAM_SHA:
        raise ValueError('Host callback module input differs')
    body=wram[ENTRY-native.engine.BASE:ENTRY-native.engine.BASE+SIZE]
    if linker.digest(body)!=TARGET or int.from_bytes(body[28:32],'little')!=native.WAKE:
        raise ValueError('Complete callback instruction/tail-literal roles differ')
    if ENTRY in functions:raise ValueError('Original sleep callback gap unexpectedly configured')
    inventory=json.loads((ROOT/'evidence/arm7/ghidra-runtime-inventory.json').read_text())['functions']
    overlap=[row for row in inventory if row['module']=='arm7-wram'and any(int(a,0)<ENTRY+SIZE and ENTRY<int(b,0)for a,b in row['ranges'])]
    if overlap:raise ValueError('Unreconciled callback configured-code overlap')
    if int.from_bytes(wram[0x4508:0x450C],'little')!=ENTRY:raise ValueError('Actual Sleep callback-pointer producer literal differs')
    references=[];branches=[]
    for module in modules.values():
        raw=(ROOT/module['binary']).read_bytes();base=int(module['base'],0)
        for offset in range(0,len(raw)-3,4):
            target=int.from_bytes(raw[offset:offset+4],'little')
            if ENTRY<=target&~1<ENTRY+SIZE:
                references.append(dict(module=module['id'],address=hex(base+offset),value=hex(target),
                    completeEntryRoot=target==ENTRY,classification='bounded-aligned-initialized-word-not-all-proven-pointers'))
    for module in modules.values():
        raw=(ROOT/module['binary']).read_bytes();base=int(module['base'],0)
        for row in inventory:
            if row['module']!=module['id']:continue
            decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM if row['mode']=='arm'else CS_MODE_THUMB);decoder.detail=True
            for begin,end in row['ranges']:
                begin,end=int(begin,0),int(end,0)
                for instruction in decoder.disasm(raw[begin-base:end-base],begin):
                    if instruction.mnemonic.startswith('b')and instruction.operands and instruction.operands[0].type==2:
                        target=instruction.operands[0].imm&0xFFFFFFFF
                        if ENTRY<=target<ENTRY+SIZE:
                            branches.append(dict(module=module['id'],address=hex(instruction.address),target=hex(target),entryRoot=target==ENTRY))
    if any(not row['entryRoot']for row in branches):raise ValueError('Unreconciled callback direct branch into an interior')
    if references!=[dict(module='arm7-wram',address='0x37fc508',value='0x37fc50c',completeEntryRoot=True,
        classification='bounded-aligned-initialized-word-not-all-proven-pointers')]:
        raise ValueError('Callback outside-word/interior/mode references differ')
    wake=next(row for row in inventory if row['module']=='arm7-wram'and int(row['address'],0)==native.WAKE)
    if ['037fc524','COMPUTED_JUMP']not in wake['incomingReferences']:
        raise ValueError('Recorded native wake-tail destination/reference changed')
    return dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(ENTRY),bytes=SIZE,
        codeBytes=CODE,literalBytes=4,alignmentBytes=0,fullRangeSha256=TARGET,inputModuleSha256=native.engine.WRAM_SHA,
        previousConfiguredSourceExtent=dict(address='0x37fc468',codeEnd='0x37fc500',literalStart='0x37fc500',fullEnd='0x37fc50c',sourceCredit=0),
        followingConfiguredEntry='0x37fc52c',literalWords=[dict(address='0x37fc528',value=hex(native.WAKE),role='configured-ARM-wake-direct-tail')],
        nativeSlotAbi=dict(argumentRegister='r0',slotReadBytes=4,slotClearBytes=4,threadAlarmOffset=148,
            threadAlarmClearBytes=4,wakePointerRegister='r0',normalReturnThroughOriginalLr=True),
        actualCallerCallsite='0x37fc4cc',callerPointerLiteral='0x37fc508',boundedAlignedWordReferences=references,boundedConfiguredDirectBranchReferences=branches,
        configuredOverlap=[],originalNamespaceStillRefusesEntry=True,sourceCredit=0,initializedDenominatorDelta=0,
        limitations=['Aligned initialized words in three measured host ARM7 modules plus measured original caller-prefix ABI',
            'Computed/cross-processor/runtime-written references not exhaustively covered; no broad callback or malformed-pointer ABI',
            'Ordinary C draft matches nonrelocation bytes; no source admission or function bytes credited here'])


def produce():
    return dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),boundary=boundary(),native=native.run(),
        generators=[dict(path=path,sha256=sha256(ROOT/path))for path in(Path(__file__).name,
            'arm7_host_sleep_callback32_native_20261101.py','arm7_host_sleep_callback32_native_engine_20261101.py')],
        sourceCredit=0,initializedDenominatorDelta=0,sleepCallerCompleteSourceCredit=0)


def validate(report):
    if report['boundary']!=boundary()or any(report[key]!=0 for key in('sourceCredit','initializedDenominatorDelta','sleepCallerCompleteSourceCredit')):
        raise ValueError('Current callback identity/boundary/zero-credit profile differs')
    pins=[dict(path=path,sha256=sha256(ROOT/path))for path in(Path(__file__).name,'arm7_host_sleep_callback32_native_20261101.py','arm7_host_sleep_callback32_native_engine_20261101.py')]
    if report.get('schemaVersion')!=1 or report.get('generator')!=Path(__file__).name or report.get('generatorSha256')!=sha256(__file__)or report.get('generators')!=pins:
        raise ValueError('Complete callback generator closure differs')
    evidence=report['native'];trace=evidence['trace'];path=ROOT/trace['path']
    if not path.is_file():raise ValueError('Required current callback native trace is missing')
    if sha256(path)!=trace['compressedSha256']:raise ValueError('Current callback trace compressed hash differs')
    raw=gzip.decompress(path.read_bytes())
    if linker.digest(raw)!=trace['rawSha256']:raise ValueError('Current callback raw trace differs')
    payload=json.loads(raw);records=payload['records'];prefixes=payload['prefixes']
    if len(records)!=72 or evidence['actualCallbackReturns']!=72 or evidence['actualWakeTailTransfersSeparate']!=72 or evidence['callbackCodeCoverageBytes']!=28:
        raise ValueError('Callback actual-return/tail/whole-code evidence differs')
    for case,row in zip(native.cases(),records):
        if row['case']!=case or not row['execution']['actualReturn']or row['execution']['error']or not row['completeMemoryAndOrderedEffects']or row['sourceCredit']or row['providerReplacements']:
            raise ValueError('Callback native case/return/state/provider evidence differs')
        if len(row['execution']['wakeDirectTailEntries'])!=1:raise ValueError('Callback actual tail transfer missing')
    if len(prefixes)!=7 or evidence['sleepCallerPrefixBoundaryStops']!=7 or evidence['actualPrefixAlarmCreateAndIrqDisableReturnsSeparate']!=14:
        raise ValueError('Caller producer-prefix counts differ')
    if evidence['sleepCallerActualOuterReturns']or evidence['sleepCallerReturnCredit']or evidence['sourceCredit']or evidence['nativeCodeCredit']:
        raise ValueError('Boundary-only caller prefix acquired source/return credit')
    for row in prefixes:
        if row['execution']['actualReturn']or not row['producerBoundaryOnly']or row['outerReturnCredit']or row['actualCallArguments']!=row['expectedCallArguments']:
            raise ValueError('Caller boundary/ABI semantics differ')
    if evidence['unsupportedReturnCredit']or evidence['unsupportedControls'][0]['execution']['actualReturn']:
        raise ValueError('Exhausted callback acquired normal return credit')
    return dict(callbackBytes=32,actualNativeCallbackReturns=72,wakeTailTransfersSeparate=72,
        callerPrefixBoundaryStops=7,callerActualOuterReturns=0,sourceCredit=0,initializedDenominatorDelta=0)


def main():
    report=produce();validate(report);write_json(REPORT,report)
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),validation=validate(report))),flush=True)


if __name__=='__main__':main()
