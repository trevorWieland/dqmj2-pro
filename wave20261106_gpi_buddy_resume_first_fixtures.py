import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_gpi_buddy_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK

BASE=0x02000000
STACK=0x03000000
END=0x04000000
CONNECTION=0x02300000
STATE=CONNECTION+0x100
PEER=CONNECTION+0x1000
PROFILE=CONNECTION+0x1100
STATUS=CONNECTION+0x1200
OP=CONNECTION+0x1300
MESSAGE=CONNECTION+0x2000
EMPTY=0x020e0764
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]
HELPERS={0x020b2a38:('thumb',20),0x0201d780:('arm',80),0x0201d800:('arm',276)}
LIMITS='Complete original and C Thumb caller returns with synthetic connections/peers/messages and supplied named GP API boundaries. Original strzcpy20,strncpy80,strcmp276 helper bodies actually execute with mode checks; their source and storage receive0credit. Append/network/peer/allocator/key-save/free bodies are bypassed and only their supplied ABI words/results are modeled. No real network,I/O,allocation,game scenes,concurrency,Windows/Android or imported storage authorship execution.'


def route_cases():
    base=dict(hasPeer=False,found=False,hasInfo=True,port=7,signature=False,newPeer=True,state=100,option=0,kind=99,operation=False,sigResult=0,startResult=0,messageResult=0)
    changes=[{},dict(option=0xb00),dict(found=True,hasInfo=False),dict(found=True,port=0),dict(found=True,newPeer=False),dict(found=True),dict(found=True,sigResult=7),dict(found=True,signature=True),dict(found=True,signature=True,startResult=9),dict(hasPeer=True,operation=True),dict(hasPeer=True,messageResult=11),dict(hasPeer=True,state=106),dict(hasPeer=True,state=106,found=True),dict(hasPeer=True,state=106,found=True,option=0xb00),dict(hasPeer=True,state=106,found=True,kind=100),dict(hasPeer=True,state=106,found=True,kind=105,operation=True),dict(hasPeer=True,state=106,found=True,hasInfo=False),dict(hasPeer=True,state=106,found=True,hasInfo=False,option=0xb00)]
    return [dict(base,**c)for c in changes]


def cstring(machine,address,maximum=4096):
    raw=bytes(machine.mem_read(address,maximum));end=raw.find(b'\0')
    if end<0:raise ValueError('Unterminated supplied GP string')
    return raw[:end].hex()


def model_route(c,profile,kind,message):
    calls=[['find-peer',profile]];result=0;clear=False
    if not c['hasPeer']:
        calls.append(['get-profile',profile])
        if not c['found']or not c['hasInfo']or c['port']==0:
            if c['option']==0xb00:return 3,calls,clear
            return 0,calls+[['server',profile,kind,message]],clear
        calls.append(['add-peer',profile,1])
        if not c['newPeer']:return 1,calls,clear
        name='start'if c['signature']else'signature';calls.append([name])
        result=c['startResult']if c['signature']else c['sigResult']
        if result:return result,calls,clear
    elif c['state']==106:
        calls.append(['get-profile',profile])
        if c['found']:
            clear=c['hasInfo']
            if c['option']==0xb00:return 3,calls,clear
            if kind<100:return 0,calls+[['server',profile,kind,message]],clear
    if c['operation']:calls.append(['add-operation'])
    calls.append(['add-message',kind,message])
    return c['messageResult'],calls,clear


def helper_specs(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();values=[]
    for a,(mode,n)in HELPERS.items():
        line=next((l for l in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),l)),None)
        if line is None:raise ValueError('Actual original string helper mode/full extent differs')
        values.append(dict(address=hex(a),mode=mode,bytes=n,canonicalInventoryRecord=line,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),sourceCredit=0))
    return values


def case_count(address):return {0x020abf18:6,0x020abfe4:len(route_cases()),0x020ac0d8:8}[address]


def run(image,row,body,seed,bound=100000,strict=True):
    address=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or address not in[0x020abf18,0x020abfe4,0x020ac0d8]:raise ValueError('Actual GP buddy caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000)
    sp=STACK+0xf000;uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for reg,value in zip(REGS,initial):uc.reg_write(reg,value)
    uc.mem_write(CONNECTION,struct.pack('<I',STATE));uc.mem_write(STATE,b'\0'*0xa00)
    sess=[0,1,0xffffffff,0x80000000,0x7fffffff,0x12345678][seed%6];uc.mem_write(STATE+0x198,struct.pack('<I',sess))
    for p,n in[(PEER,80),(PROFILE,32),(STATUS,60),(OP,24)]:uc.mem_write(p,b'\0'*n)
    profile=300+seed;kind=[99,100,105,0xffffffff][seed%4];text=b'Q'*([0,1,3499,3500,3501,3510][seed%6]if address==0x020abf18 else seed%5);uc.mem_write(MESSAGE,text+b'\0'+b'Z'*8)
    uc.mem_write(PEER+16,struct.pack('<I',profile));arguments=[CONNECTION,profile,kind,MESSAGE];calls=[];helpers={};observed=set();returned=False;failures=[];c={};expected_clear=False
    if address==0x020abfe4:
        c=route_cases()[seed];kind=c['kind'];arguments[2]=kind;uc.mem_write(PEER,struct.pack('<I',c['state']));uc.mem_write(PROFILE+12,struct.pack('<I',STATUS if c['hasInfo']else 0));uc.mem_write(PROFILE+28,struct.pack('<I',MESSAGE if c['signature']else 0));uc.mem_write(STATUS+32,struct.pack('<H',c['port']));uc.mem_write(sp,struct.pack('<II',c['option'],OP if c['operation']else 0));expected_result,expected_calls,expected_clear=model_route(c,profile,kind,text.hex())
    elif address==0x020abf18:
        expected_result=0;expected_calls=[['append-string',(b'\\bm\\').hex()],['append-int',kind],['append-string',(b'\\sesskey\\').hex()],['append-int',sess],['append-string',(b'\\t\\').hex()],['append-int',profile],['append-string',(b'\\msg\\').hex()],['append-string',text[:3500].hex()],['append-string',(b'\\final\\').hex()]]
    else:
        arguments=[CONNECTION,PEER];save_error=7 if seed==0 else 0;send_error=9 if seed==1 else 0;null=seed in[2,3];empty=seed in[4,5];text=b''if empty else b'key-value';uc.mem_write(MESSAGE,text+b'\0');chosen=EMPTY if null else MESSAGE;expected_calls=[['save-keys']];expected_result=save_error
        if not save_error:
            expected_calls.append(['send',profile,105,text.hex()if not null else'',0xb00,0]);expected_result=send_error
            if not send_error and not null and text:expected_calls.append(['free',MESSAGE])
    for reg,value in zip(REGS,arguments):uc.reg_write(reg,value)
    before=bytes(uc.mem_read(BASE,0x400000))
    def finish(machine,result):
        machine.reg_write(UC_ARM_REG_R0,result&0xffffffff);machine.reg_write(UC_ARM_REG_R1,0xa1a1a1a1);machine.reg_write(UC_ARM_REG_R2,0xa2a2a2a2);machine.reg_write(UC_ARM_REG_R3,0xa3a3a3a3);machine.reg_write(UC_ARM_REG_R12,0xacacacac);machine.reg_write(UC_ARM_REG_PC,machine.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,data):
        nonlocal returned
        if pc==END:returned=True;machine.emu_stop();return
        if address<=pc<address+len(body):observed.add(pc);return
        if pc in HELPERS:
            mode,n=HELPERS[pc]
            if bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):failures.append('Actual string helper entry mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(a<=pc<a+n for a,(mode,n)in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];stack=machine.reg_read(UC_ARM_REG_SP)
        if pc in[0x020ac6f4,0x020ac710]and address==0x020abf18:
            if r[:2]!=[CONNECTION,STATE+0x210]:failures.append('Actual output-buffer/provider ABI differs')
            calls.append(['append-string',cstring(machine,r[2])]if pc==0x020ac6f4 else['append-int',r[2]]);finish(machine,19);return
        if address==0x020abfe4:
            if pc==0x020b03a4:calls.append(['find-peer',r[1]]);finish(machine,PEER if c['hasPeer']else 0);return
            if pc==0x020b0a50:
                calls.append(['get-profile',r[1]])
                if not STACK<=r[2]<sp:failures.append('Actual profile out-pointer is not caller stack')
                machine.mem_write(r[2],struct.pack('<I',PROFILE if c['found']else 0));finish(machine,int(c['found']));return
            if pc==0x020b0404:calls.append(['add-peer',r[1],r[2]]);finish(machine,PEER if c['newPeer']else 0);return
            if pc==0x020abf18:calls.append(['server',r[1],r[2],cstring(machine,r[3])]);finish(machine,0);return
            if pc in[0x020b0464,0x020b049c]:calls.append(['signature'if pc==0x020b0464 else'start']);finish(machine,c['sigResult']if pc==0x020b0464 else c['startResult']);return
            if pc==0x020b0794:
                if r[:2]!=[PEER,OP]:failures.append('Actual peer-operation ABI differs')
                calls.append(['add-operation']);finish(machine,0);return
            if pc==0x020b0534:
                if r[:2]!=[CONNECTION,PEER]:failures.append('Actual peer-message ABI differs')
                calls.append(['add-message',r[2],cstring(machine,r[3])]);finish(machine,c['messageResult']);return
        if address==0x020ac0d8:
            if pc==0x020af5d4:calls.append(['save-keys']);machine.mem_write(r[1],struct.pack('<I',0 if null else MESSAGE));finish(machine,save_error);return
            if pc==0x020abfe4:
                option,operation=struct.unpack('<II',machine.mem_read(stack,8));calls.append(['send',r[1],r[2],cstring(machine,r[3]),option,operation]);finish(machine,send_error);return
            if pc==0x020a929c:calls.append(['free',r[0]]);finish(machine,0);return
        failures.append('Execution escaped actual original caller/string-helper/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address|1,END+4,count=bound)
    if not returned or calls!=expected_calls or uc.reg_read(UC_ARM_REG_R0)!=expected_result:failures.append('Independent ordered protocol/route/result model differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Actual complete caller stack/callee-save contract differs')
    expected_memory=bytearray(before)
    if expected_clear:expected_memory[STATUS+32-BASE:STATUS+34-BASE]=b'\0\0'
    if bytes(uc.mem_read(BASE,0x400000))!=expected_memory:failures.append('Full protected main RAM differs outside declared buddy-port store')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Stack lower guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=uc.reg_read(UC_ARM_REG_R0),calls=calls,helperEntries=helpers,callerInstructionAddresses=sorted(observed),portCleared=expected_clear)
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!={0x020abf18,0x020abfe4,0x020ac0d8}:raise ValueError('Exact coherent GP buddy subset differs')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image);records=[]
    for row in rows:
        a=int(row['address'],0);original=image[a-BASE:a-BASE+row['bytes']];candidate=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,original,seed);right=run(image,row,candidate,seed)
            if left!=right:raise ValueError('Actual original/C complete GP traces differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['calls']),original=left,candidate=right))
    if run(image,rows[0],image[int(rows[0]['address'],0)-BASE:int(rows[0]['address'],0)-BASE+rows[0]['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete bounded prefix admitted as complete GP return')
    value=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',value);return value
