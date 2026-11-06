import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_gp_profile_operation_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS,cstring

OP=0x02302000
NODES=[OP+i*0x100 for i in range(3)]
DATA=[OP+0x400+i*0x200 for i in range(3)]
BUFFER=OP+0x1000
MESSAGE=OP+0x3000
PEER=OP+0x3200
HELPERS={0x0201d780:80,0x0201d984:108}
LIMITS='Complete original/C manager callers return on empty-command receive buffers,including send/receive errors,closed/deleting state,blocking-loop retry and keepalive boundaries. Nonempty manager command parsing/dispatch and real network bodies are not executed. Complete search-list,NOFILE transfer and bounded terminated-copy callers execute on synthetic records. Actual original ARM strncpy80/strstr108 helpers execute; allocation,search processing/removal,format parser,transfer reply,timer,socket I/O,error,buffer append and sleep bodies are supplied boundaries with zero body instructions. No actual callbacks,file/network/I/O,storage authorship,game scene,concurrency or Windows/Android execution.'


def case_count(a):return{0x020aab70:11,0x020b27a0:10,0x020b28c0:5,0x020b2a38:6}[a]


def run(image,row,body,seed,bound=100000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or a not in[0x020aab70,0x020b27a0,0x020b28c0,0x020b2a38]:raise ValueError('Exact second caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def setword(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    def text(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    uc.mem_write(STATE,b'\x5a'*0x700);setword(CONNECTION,STATE);uc.mem_write(BUFFER,b'Z'*4096);uc.mem_write(MESSAGE,b'example header\0')
    for p,d in zip(NODES,DATA):uc.mem_write(p,b'\xa5'*36);uc.mem_write(d,b'\xa5'*340)
    args=[CONNECTION];selected=[];callbacks=0
    if a==0x020aab70:
        now=120001 if seed==6 else 120000 if seed==7 else 0 if seed==10 else 1000;oldtime=0xffffffff if seed==10 else 0
        setword(STATE+496,7);setword(STATE+500,5 if seed==5 else 0);setword(STATE+504,BUFFER);setword(STATE+512,0);setword(STATE+536,int(seed==8));setword(STATE+1584,oldtime);uc.mem_write(BUFFER,b'\0')
    elif a==0x020b27a0:
        setword(STATE+568,0 if seed==0 else 3);setword(STATE+1476,0 if seed==6 else NODES[0])
        for i,(p,d)in enumerate(zip(NODES,DATA)):
            kind=1 if seed==3 and i==1 else 3;state=5 if seed==4 and i==1 else 0;processing=1 if seed==5 and i==1 else 0
            setword(p,kind);setword(p+4,d);setword(p+20,state);setword(p+32,NODES[i+1]if i<2 else 0);setword(d+320,processing);setword(d+324,int(seed==8 and i==1))
            if seed!=6 and kind==3 and state!=5 and not processing:selected.append((i,p,d))
    elif a==0x020b28c0:args=[CONNECTION,PEER,77,MESSAGE];setword(sp,BUFFER);setword(sp+4,21)
    else:
        count=[1,2,5,8,31,5][seed];data=b''if seed==0 else b'Hi'if seed==5 else b'abcdefghijklmnopqrstuvwxyz0123456789';uc.mem_write(MESSAGE,data+b'\0');args=[BUFFER+16,MESSAGE,count]
    for r,v in zip(REGS,args):uc.reg_write(r,v)
    before=bytes(uc.mem_read(BASE,0x400000));expected=bytearray(before);calls=[];expected_calls=[];helpers={};observed=set();failures=[];returned=False;blocking_calls=0;retval=0
    def ew(p,v):struct.pack_into('<I',expected,p-BASE,v&0xffffffff)
    def eb(p,data):expected[p-BASE:p-BASE+len(data)]=data
    if a==0x020aab70:
        expected_calls=[['time']]
        for loop in range(2 if seed==9 else 1):
            expected_calls+=[['add-local',STATE+528],['send',7,STATE+528,1,'CM']]
            if seed==8:ew(STATE+1584,now)
            if seed==1:retval=1;break
            expected_calls+=[['receive',7,STATE+504,'CM']]
            if seed in[2,3]:
                retval=2 if seed==2 else 3
                if seed==3:expected_calls+=[['set-error',5,'There was an error reading from the server.'],['error-callback',3,1]]
                break
            if seed==4:expected_calls+=[['set-error',7,'The server has closed the connection.'],['error-callback',3,1]];break
            expected_calls+=[['blocking-operations']]
            if seed==9 and loop==0:expected_calls+=[['sleep',10]]
        if seed not in[1,2,3,4]and((now-(now if seed==8 else oldtime))&0xffffffff)>120000:expected_calls+=[['append',STATE+528,'\\ka\\\\final\\']];ew(STATE+1584,now)
    elif a==0x020b27a0:
        if seed!=0:
            expected_calls=[['allocate',12]]
            if seed==1:retval=1;expected_calls+=[['error-string','Out of memory.']]
            else:
                for n,(i,p,d)in enumerate(selected):ew(BUFFER+4*n,p);expected_calls+=[['process',p]];ew(p+28,7)if seed==7 else None
                expected_calls+=[['remove',p]for i,p,d in selected if seed==8 and i==1];expected_calls+=[['free',BUFFER]]
    elif a==0x020b28c0:
        expected_calls=[['value-key','example header','\\xfer\\',64]]
        if seed!=0:expected_calls+=[['scan','-1 4660 22136','%d %u %u']]
        if seed==3:expected_calls+=[['reply',[-1,0x1234,0x5678],PEER,2,0]]
    else:
        copied=data[:count]+b'\0'*max(0,count-len(data));copied=copied[:count];eb(BUFFER+16,copied);eb(BUFFER+16+count-1,b'\0')
    def finish(value):
        for r,v in zip([*REGS[:4],UC_ARM_REG_R12],[value&0xffffffff,0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,v)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,opaque):
        nonlocal returned,blocking_calls
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        if pc in HELPERS:
            if machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Original MSL helper mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(p<=pc<p+n for p,n in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];stack=machine.reg_read(UC_ARM_REG_SP);binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Supplied provider mode differs')
        connection_calls=[0x20ae834,0x20ac954,0x20ac880,0x20b2c6c,0x20acbcc,0x20afb40,0x20ac6f4,0x20b1044,0x20afad8,0x20b2860,0x20b2c88]
        if pc in connection_calls and r[0]!=CONNECTION:failures.append('Actual supplied connection owner differs')
        if pc==0x20a8ef8:calls.append(['time']);finish(now);return
        if pc==0x20ae834:calls.append(['add-local',r[1]]);finish(0);return
        if pc==0x20ac954:
            tail=struct.unpack('<II',machine.mem_read(stack,8));calls.append(['send',r[1],r[2],tail[0],text(tail[1])]);finish(1 if seed==1 else 0);return
        if pc==0x20ac880:
            tail=struct.unpack('<II',machine.mem_read(stack,8));calls.append(['receive',r[1],r[2],text(tail[1])]);setword(r[3],0);setword(tail[0],int(seed in[4,5]));finish(2 if seed==2 else 3 if seed==3 else 0);return
        if pc==0x20b2c6c:calls.append(['set-error',r[1],text(r[2])]);finish(0);return
        if pc==0x20acbcc:calls.append(['error-callback',r[1],r[2]]);finish(0);return
        if pc==0x20afb40:calls.append(['blocking-operations']);finish(int(seed==9 and blocking_calls==0));blocking_calls+=1;return
        if pc==0x20a8f14:calls.append(['sleep',r[0]]);finish(0);return
        if pc==0x20ac6f4:calls.append(['append',r[1],text(r[2])]);finish(0);return
        if pc==0x20a927c:calls.append(['allocate',r[0]]);finish(0 if seed==1 else BUFFER);return
        if pc==0x20b2c88:calls.append(['error-string',text(r[1])]);finish(0);return
        if pc==0x20b1044:
            calls.append(['process',r[1]]);d=struct.unpack('<I',machine.mem_read(r[1]+4,4))[0]
            if struct.unpack('<I',machine.mem_read(d+320,4))[0]!=1:failures.append('Selected search processing guard was not set')
            finish(7 if seed==7 else 0);return
        if pc==0x20afad8:
            calls.append(['remove',r[1]]);d=struct.unpack('<I',machine.mem_read(r[1]+4,4))[0]
            if struct.unpack('<I',machine.mem_read(d+320,4))[0]!=0:failures.append('Selected search processing flag not cleared before removal')
            finish(0);return
        if pc==0x20a929c:calls.append(['free',r[0]]);finish(0);return
        if pc==0x20b2ae0:calls.append(['value-key',text(r[0]),text(r[1]),r[3]]);machine.mem_write(r[2],b'-1 4660 22136\0');finish(int(seed!=0));return
        if pc==0x2019dd4:
            calls.append(['scan',text(r[0]),text(r[1])]);p=struct.unpack('<I',machine.mem_read(stack,4))[0];n={1:0,2:2,3:3,4:4}[seed]
            for target,value in zip([r[2],r[3],p],[-1,0x1234,0x5678]):setword(target,value)
            finish(n);return
        if pc==0x20b2860:
            fields=list(struct.unpack('<iII',machine.mem_read(r[1],12)));tail=struct.unpack('<I',machine.mem_read(stack,4))[0];calls.append(['reply',fields,r[2],r[3],tail]);finish(0);return
        failures.append('Execution escaped qualified caller/helper/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(a|1,END+4,count=bound)
    if not returned or calls!=expected_calls or(a in[0x020aab70,0x020b27a0]and uc.reg_read(UC_ARM_REG_R0)!=retval):failures.append('Independent full caller return/provider model differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected:failures.append('Full protected caller/record/heap memory differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Caller return stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=uc.reg_read(UC_ARM_REG_R0)if a in[0x020aab70,0x020b27a0]else None,calls=calls,expectedCalls=expected_calls,helperEntries=helpers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!={0x020aab70,0x020b27a0,0x020b28c0,0x020b2a38}:raise ValueError('Exact second subset differs')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=[];specs=[]
    for a,n in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        if line is None:raise ValueError('Original MSL helper full boundary/mode differs')
        specs.append(dict(address=hex(a),bytes=n,mode='arm',nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Original/C complete second caller observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['calls']),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
