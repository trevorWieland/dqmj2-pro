import gzip
import hashlib
import json
import struct
import arm7_lane_card_service_engine_20261031 as engine
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM,CS_MODE_THUMB,CS_GRP_JUMP,CS_GRP_CALL,CS_OP_IMM
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_ARM_REG_CPSR
from project import ROOT,sha256,write_json
MODULE='extract/arm7/runtime/arm7-wram.bin'
RUNTIME_PINS='provenance/arm7-lane-card-callback-scope-runtime-pins-20261031.json'
RUNTIME_PINS_SHA='c273862e55ef9e6b627b3853f9774ec271258bea057dd92959d8ac20f51fc1aa'
MODULE_HASH='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
BASE=0x037f8000
SCOPES=((0x038028e4,60),(0x03802924,76),(0x03802974,96))
IO,STATE,SOURCE,DESTINATION=0x040001a0,engine.DATA,engine.DATA+0x200,engine.DATA+0x400


def qualify(raw):
    if hashlib.sha256(raw).hexdigest()!=MODULE_HASH:raise ValueError('Callback source module differs')
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    rows=[]
    for address,code in SCOPES:
        body=raw[address-BASE:address-BASE+code+4]
        instructions=list(decoder.disasm(body[:code],address))
        if len(instructions)*4!=code or instructions[-1].mnemonic!='bx' or instructions[-1].op_str!='lr':
            raise ValueError('Callback code/return boundary differs')
        if struct.unpack_from('<I',body,code)[0]!=IO+2:raise ValueError('Callback pool is not SPI data register')
        edges=[]
        for insn in instructions:
            if CS_GRP_JUMP in insn.groups and insn.mnemonic!='bx':
                target=insn.operands[0].imm
                if not address<=target<address+code or target%4:raise ValueError('Callback branch enters another role')
                edges.append(dict(source=hex(insn.address),target=hex(target),kind=insn.mnemonic))
        rows.append(dict(program='',processor='arm7',module='arm7-wram',mode='arm',address=hex(address),
            bytes=code+4,instructionBytes=code,poolBytes=4,codeEnd=hex(address+code),end=hex(address+code+4),
            sourceSha256=hashlib.sha256(body).hexdigest(),codeSha256=hashlib.sha256(body[:code]).hexdigest(),
            poolSha256=hashlib.sha256(body[code:]).hexdigest(),poolWord=hex(IO+2),alignment=4,localBranches=edges,
            originalModuleSha256=MODULE_HASH,sourceCredit=0))
    return rows


def select(raw,address,mode,size):
    matches=[row for row in qualify(raw) if int(row['address'],0)==address and row['mode']==mode and row['bytes']==size]
    if len(matches)!=1:raise ValueError('Unqualified callback entry/mode/complete boundary')
    return matches[0]


def fixture(address,case,seed,mediated):
    raw=(ROOT/MODULE).read_bytes()
    body=raw[0x03802860-BASE:0x03802860-BASE+132]
    machine=engine.setup(0x03802860,body,seed);cpu=machine['cpu']
    cpu.mem_write(STATE,struct.pack('<IIII',case['count'],SOURCE,DESTINATION,case['flag']))
    cpu.mem_write(SOURCE,bytes([case['source']]))
    cpu.mem_write(IO,bytes(4))
    snapshots=engine.snapshot(machine)
    entered=[];reads=[];modes=[]
    read_pc={0x038028e4:0x03802908,0x03802924:0x0380295c,0x03802974:0x03802998}[address]
    pc_state=dict(pc=None)
    def code(uc,pc,size,unused):
        pc_state['pc']=pc
        if pc==address:
            entered.append(uc.reg_read(engine.match_runtime.REGISTERS[14]))
            modes.append(bool(uc.reg_read(UC_ARM_REG_CPSR)&32))
    def read(uc,access,target,size,value,unused):
        if pc_state['pc']==read_pc and target==IO+2:
            reads.append(case['response'])
            uc.mem_write(IO+2,case['response'].to_bytes(2,'little'))
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read)
    entry,args=(0x03802860,(SOURCE,DESTINATION,1,address)) if mediated else (address,(STATE,))
    if mediated:
        cpu.mem_write(0x038096c4,case['count'].to_bytes(4,'little'))
        state_address=0x038096c4
        snapshots=engine.snapshot(machine)
    else:state_address=STATE
    execution=machine['invoke'](entry,args,True,20000)
    if not execution['actualReturn'] or len(entered)!=1 or modes!=[False] or reads!=[case['response']]:
        raise ValueError('Callback actual ARM invocation/return/readback contract differs')
    if mediated and machine['helperReturns'][address]!=1:raise ValueError('Indirect callback did not actually return to transfer caller')
    def put(target,size,value):
        for first,data in snapshots.items():
            if first<=target and target+size<=first+len(data):
                data[target-first:target-first+size]=value.to_bytes(size,'little');return
        raise ValueError('Callback model write escaped backing')
    if mediated:
        put(state_address,4,(case['count']-1)&0xffffffff)
        put(state_address+4,4,SOURCE);put(state_address+8,4,DESTINATION)
        put(IO,2,0 if case['count']==1 else 0xa040)
    put(IO+2,2,case['response'])
    if address==0x038028e4:
        put(DESTINATION,1,case['response']&255);put(state_address+8,4,DESTINATION+1)
    elif address==0x03802924:put(state_address+4,4,SOURCE+1)
    else:
        if (case['response']&255)!=case['source']:
            put(state_address+12,4,0)
            current=(case['count']-1)&0xffffffff if mediated else case['count']
            if current>1:put(state_address,4,1)
        put(state_address+4,4,SOURCE+1)
    if any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in snapshots.items()):
        raise ValueError('Independent callback complete nonstack memory model differs')
    return dict(address=hex(address),case=case,seed=seed,callerMediated=mediated,execution=execution,
        actualReturn=True,callbackEntryMode='arm',callbackReturnLinks=[hex(value) for value in entered],
        actualNestedReturns={hex(key):value for key,value in machine['helperReturns'].items()},
        independentCompleteMappedMemoryModel=True,syntheticSpiReadback=case['response'],physicalHardwareCredit=0,
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()})


def references(raw):
    result=[]
    targets={address for address,code in SCOPES}
    for path,base in ((MODULE,BASE),('extract/arm7/runtime/arm7-main.bin',0x027e0000)):
        data=(ROOT/path).read_bytes()
        for offset in range(0,len(data)-3,4):
            value=struct.unpack_from('<I',data,offset)[0]
            if value in targets:result.append(dict(modulePath=path,address=hex(base+offset),word=hex(value),
                evidence='Aligned literal identity; actual callsite qualification is separate'))
    return result


def branch_audit(raw):
    entries,ranges=engine.inventory()
    first,last=SCOPES[0][0],SCOPES[-1][0]+SCOPES[-1][1]+4
    decoders={False:Cs(CS_ARCH_ARM,CS_MODE_ARM),True:Cs(CS_ARCH_ARM,CS_MODE_THUMB)}
    for decoder in decoders.values():decoder.detail=True
    qualified=[];seen=set()
    for low,high,thumb in ranges:
        if not BASE<=low<=high<=BASE+len(raw):continue
        for insn in decoders[thumb].disasm(raw[low-BASE:high-BASE],low):
            if insn.address in seen:continue
            seen.add(insn.address)
            if not any(group in insn.groups for group in (CS_GRP_JUMP,CS_GRP_CALL)):continue
            if not insn.operands or insn.operands[0].type!=CS_OP_IMM:continue
            target=insn.operands[0].imm&~1
            if first<=target<last:
                qualified.append(dict(source=hex(insn.address),sourceMode='thumb' if thumb else 'arm',target=hex(target),opcode=insn.mnemonic))
    raw_aligned=[]
    for path,base in ((MODULE,BASE),('extract/arm7/runtime/arm7-main.bin',0x027e0000)):
        data=(ROOT/path).read_bytes()
        for offset in range(0,len(data)-3,4):
            word=struct.unpack_from('<I',data,offset)[0]
            if word&0x0e000000!=0x0a000000 or word>>28==15:continue
            displacement=word&0xffffff
            if displacement&0x800000:displacement-=0x1000000
            target=base+offset+8+displacement*4
            if first<=target<last:
                source=base+offset
                own=any(start<=source<start+size for start,size in SCOPES)
                raw_aligned.append(dict(source=hex(source),target=hex(target),withinProposedCode=own,
                    sourceModeQualified=own or any(low<=source and source+4<=high and not thumb for low,high,thumb in ranges),
                    category='Aligned ARM branch hypothesis; data/mode coincidence remains possible'))
    return dict(existingModeQualifiedDirectBranches=qualified,rawAlignedArmBranchHypotheses=raw_aligned,
        externalModeQualifiedInteriorEntries=[row for row in qualified if int(row['target'],0) not in {start for start,size in SCOPES}],
        limitation='The current mode-qualified function inventory plus proposed local CFG is audited; unknown indirect/global producers and unclassified bytes are not claimed closed')


def main():
    pins=ROOT/RUNTIME_PINS
    if sha256(pins)!=RUNTIME_PINS_SHA:raise ValueError('Frozen runtime pin manifest differs')
    for row in json.loads(pins.read_text())['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen runtime source/input dependency differs: '+row['path'])
    if sha256(ROOT/'extract/arm7/runtime/arm7-main.bin')!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416':
        raise ValueError('Measured host ARM7 main namespace differs')
    import platform,unicorn,elftools
    if platform.python_version()!='3.13.5' or unicorn.__version__!='2.1.4' or elftools.__version__!='0.33':
        raise ValueError('Pinned Python/native-test dependency versions differ')
    raw=(ROOT/MODULE).read_bytes();rows=qualify(raw)
    entries,_=engine.inventory()
    if any(address in entries for address,unused in SCOPES):raise ValueError('Gap entries unexpectedly entered old inventory')
    records=[]
    for address,code in SCOPES:
        for count in (0,1,2,0xffffffff):
            for flag in (0,1,0x80000000):
                for source,response in ((0,0),(1,1),(0x80,0xff80),(0xff,0xffff),(1,0)):
                    for seed in (0,15):
                        case=dict(count=count,flag=flag,source=source,response=response)
                        records.append(fixture(address,case,seed,False))
        for source,response in ((0,0),(1,1),(0xff,0xffff),(1,0)):
            records.append(fixture(address,dict(count=1,flag=1,source=source,response=response),0,True))
    failed=[]
    for address,code in SCOPES:
        altered=bytearray(raw);altered[address-BASE]^=1
        try:qualify(bytes(altered))
        except ValueError:failed.append(dict(kind='changed-owned-code',address=hex(address),rejected=True))
        else:raise ValueError('Changed original callback code accepted')
    for address,code in SCOPES:
        for entry,mode,size in ((address+4,'arm',code),(address,'thumb',code+4),
            (address,'arm',code),(address,'arm',code+8),(address+code,'arm',4),(address+1,'arm',code+4)):
            try:select(raw,entry,mode,size)
            except ValueError:failed.append(dict(kind='entry-mode-boundary-role',address=hex(entry),mode=mode,bytes=size,rejected=True))
            else:raise ValueError('Invalid callback entry/mode/boundary accepted')
    stopped=[]
    for address,code in SCOPES:
        for entry,budget,kind in ((address,1,'instruction-cap'),(address+code,100,'literal-pool')):
            machine=engine.setup(0x03802860,raw[0x03802860-BASE:0x03802860-BASE+132],0)
            execution=machine['invoke'](entry,(STATE,),True,budget)
            if execution['actualReturn']:raise ValueError('Stopped/pool execution gained return')
            stopped.append(dict(kind=kind,entry=hex(entry),execution=execution,returnCredit=0))
    payload=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode()
    product=ROOT/'work/arm7-bulk-20261030/lane-card-callback-scope/callback-records.json.gz';product.parent.mkdir(parents=True,exist_ok=True)
    product.write_bytes(gzip.compress(payload,compresslevel=9,mtime=0))
    report=ROOT/'evidence/arm7/lane-card-callback-scope-20261031.json'
    write_json(report,dict(generator=__import__('pathlib').Path(__file__).name,generatorSha256=sha256(__file__),
        runtimePins=dict(path=RUNTIME_PINS,sha256=RUNTIME_PINS_SHA),
        engine=dict(path='arm7_lane_card_service_engine_20261031.py',sha256=sha256(ROOT/'arm7_lane_card_service_engine_20261031.py')),
        originalModule=dict(path=MODULE,sha256=sha256(ROOT/MODULE)),candidateRanges=rows,literalReferences=references(raw),branchInteriorAudit=branch_audit(raw),
        actualDirectCallbackReturns=sum(not row['callerMediated'] for row in records),
        actualTransferCallerReturns=sum(row['callerMediated'] for row in records),
        actualIndirectCallbackReturns=sum(row['callerMediated'] for row in records),
        actualOwnSourceReturnCredit=0,newSourceCredit=0,initializedDenominatorBytesAdded=0,
        runtimeVersions=dict(python=platform.python_version(),unicorn=unicorn.__version__,pyelftools=elftools.__version__,cpu='TI925T ARMv4T surrogate'),
        oldConfiguredInventoryUnchanged=True,linkerUnknownSymbolRefusalUnchanged=True,mutationControls=failed,unsupportedControls=stopped,
        indirectCallInstruction=dict(address='0x038028AC',opcode='BX r6',returnAddress='0x038028B0',argumentWords=1,argumentMeaning='State pointer'),
        traceProduct=dict(path=product.relative_to(ROOT).as_posix(),sha256=sha256(product),rawSha256=hashlib.sha256(payload).hexdigest(),bytes=product.stat().st_size,rawBytes=len(payload),records=len(records),gzipMtime=0),
        limitations=['Proposed callable boundaries only; integrator owns inventory/configuration decisions',
            'All244 bytes already lie in measured initialized WRAM; no denominator expansion',
            'Every callback has one finalBX LR and only internal direct branches; pool words are040001A2 data-register addresses',
            'Original transfer caller executes actualBX and callbackRET; standalone entries also actually return with full-register/caller guards',
            'SPI readback is an explicit synthetic peripheral contract; no physical storage, timing, ownership, game-save or source reconstruction credit',
            'Literal scans are aligned word identities and can include data coincidence; executable caller/entry links are scoped separately']))
    print(json.dumps(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),directReturns=360,indirectReturns=12,bytes=244,sourceCredit=0)))


if __name__=='__main__':main()
