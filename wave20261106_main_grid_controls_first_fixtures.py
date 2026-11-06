import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_main_grid_controls_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

LIMITS='Complete124-byte original/C callers execute supplied drawing services with real original coordinate88 helper.360-byte original/C callers stop BEFORE the540-byte input provider; no360 return or post-provider clamp execution credit. Synthetic records/handles/pages only; no real graphics/input/game scene,provider-body,I/O,concurrency,Windows/Android or storage authorship execution.'
HELPERS={0x020cfa78:88,0x020629e0:48,0x020d0a24:36}
BASE=0x02000000
STACK=0x03000000
END=0x04000000
HANDLE=0x02300000
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def specs(image,inventory):
    result=[]
    for a,n in HELPERS.items():
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),line)),None)
        if canonical is None:raise ValueError('Actual pure helper canonical full ARM extent differs')
        result.append(dict(address=hex(a),bytes=n,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=canonical,sourceCredit=0))
    return result


def run(image,row,body,seed,bound=16000,strict=True):
    address=int(row['address'],0)
    if (row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','arm')or address not in[0x020d0bfc,0x020d0844]:raise ValueError('Actual grid controller caller namespace differs')
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.mem_map(BASE,0x400000);machine.mem_write(BASE,image);machine.mem_write(address,body);machine.mem_map(STACK,0x10000);machine.mem_map(END,0x1000)
    machine.mem_write(STACK,b'\xA5'*0x10000);sp=STACK+0xf000
    initial=[((0x11223344*(i+1))^(seed*0x01010101))&0xffffffff for i in range(13)]
    for reg,value in zip(REGS,initial):machine.reg_write(reg,value)
    machine.reg_write(UC_ARM_REG_CPSR,0x10|((seed%4)<<28));machine.reg_write(UC_ARM_REG_SP,sp);machine.reg_write(UC_ARM_REG_LR,END)
    handle=bytes([(seed*17+i*13)&255 for i in range(16)]);machine.mem_write(HANDLE,handle)
    page=[0,1,8,255][seed%4];count=[0,1,12,13,99,100][seed%6]
    state=bytes([0x5a,page,0x73,0x84,0,0,0,0,0xfd,0x7f,0xa6,0x55]);machine.mem_write(0x021d6b5c,state)
    records=bytearray(13200)
    for i in range(count):struct.pack_into('<I',records,i*132+20,0x10000+i)
    machine.mem_write(0x021bd674,bytes(records))
    arguments=[HANDLE,0,0]if address==0x020d0bfc else[0x12345678,0x89abcdef,0xfedcba98]
    for reg,value in zip(REGS,arguments):machine.reg_write(reg,value)
    before=bytes(machine.mem_read(BASE,0x400000));supplied=[];helper_entries={};observed=set();returned=False;partial=False;failures=[];input_observation=None
    def hook(uc,pc,size,data):
        nonlocal returned,partial,input_observation
        if pc==END:returned=True;uc.emu_stop();return
        if address<=pc<address+len(body):observed.add(pc);return
        if pc in HELPERS:helper_entries[hex(pc)]=helper_entries.get(hex(pc),0)+1
        if any(a<=pc<a+n for a,n in HELPERS.items()):return
        if pc==0x02045dc4 and address==0x020d0bfc:
            stack=uc.reg_read(UC_ARM_REG_SP);words=[uc.reg_read(r)for r in REGS[:4]]+list(struct.unpack('<II',uc.mem_read(stack,8)));supplied.append(words)
            for reg,value in zip([*REGS[:4],UC_ARM_REG_R12],[0xdecafbad,0x11111111,0x22222222,0x33333333,0xcccccccc]):uc.reg_write(reg,value)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR));return
        if pc==0x020c1a04 and address==0x020d0844:
            pointer=uc.reg_read(UC_ARM_REG_R2);input_observation=dict(words=[uc.reg_read(r)for r in REGS[:4]],page=struct.unpack('<i',uc.mem_read(pointer,4))[0],stackRelative=pointer-sp);partial=True;uc.emu_stop();return
        failures.append('Execution escaped actually qualified caller/helpers/service boundary:'+hex(pc));uc.emu_stop()
    machine.hook_add(UC_HOOK_CODE,hook);machine.emu_start(address,END+4,count=bound)
    if address==0x020d0bfc:
        expected=[[handle[10],handle[11],(48+(i%4)*40)//8,((i//4+1)*40)//8,2,2]for i in range(12)]
        if not returned or partial or supplied!=expected:failures.append('Complete twelve-cell ordered six-word model differs')
        if machine.reg_read(UC_ARM_REG_SP)!=sp or[machine.reg_read(r)for r in REGS[4:12]]!=initial[4:12]:failures.append('Complete caller callee-saved/stack restoration differs')
    else:
        if not partial or returned or input_observation is None:failures.append('Actual input provider prefix did not stop at entry')
        elif input_observation['words'][:2]!=[208,40]or input_observation['words'][3]!=(count+11)//12 or input_observation['page']!=page or input_observation['stackRelative']!=-32:failures.append('Measured input prefix/count/page argument model differs')
    after=bytearray(machine.mem_read(BASE,0x400000));expected_memory=bytearray(before)
    if address==0x020d0844:expected_memory[0x021d6b5c-BASE]=page
    if after!=expected_memory:failures.append('Full protected main RAM differs outside declared old-page store')
    if bytes(machine.mem_read(STACK,0xe000))!=b'\xA5'*0xe000 or bytes(machine.mem_read(sp,0x1000))!=b'\xA5'*0x1000:failures.append('Stack guards differ')
    value=dict(topReturned=returned,partialProviderStopped=partial,modelPassed=not failures,failures=failures,suppliedCalls=supplied,helperEntries=helper_entries,inputObservation=input_observation,observedCallerInstructions=sorted(observed),protectedMainRamMatched=after==expected_memory)
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if {int(r['address'],0)for r in rows}!={0x020d0bfc,0x020d0844}:raise ValueError('Exact two controller packet identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();helper_specs=specs(image,(ROOT/'config/arm9/symbols.txt').read_text());records=[]
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(24):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Actual original/C caller observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=left['topReturned'],partialProviderStopped=left['partialProviderStopped'],actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['suppliedCalls']),original=left,candidate=right))
    if run(image,rows[0],image[int(rows[0]['address'],0)-BASE:int(rows[0]['address'],0)-BASE+rows[0]['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Bounded incomplete caller admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=helper_specs,nativeAndCompiledReturningCalls=2*sum(r['topReturned']for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped']for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
