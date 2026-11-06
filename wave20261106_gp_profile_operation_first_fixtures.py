import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_gp_profile_operation_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS,cstring

OP=0x02302000
SEARCH=OP+0x200
BUFFER=OP+0x1000
MESSAGE=OP+0x2400
HOST=OP+0x2600
ADDRLIST=HOST+0x40
IPADDRESS=HOST+0x80
OUT=HOST+0xc0
CALLBACK=0x13572469
PARAM=0x24681357
HELPERS={0x0201d914:52}
LIMITS='Complete original/C GP search-initialization,registration and stats-receive callers return on synthetic records. Actual original ARM strncmp52 executes. Allocator,memset,memmove,parser,DNS,socket,timer,callback-dispatch,error and close providers are supplied boundaries with zero body instructions. No actual network/I/O,callbacks,storage ownership,Windows/Android,concurrency or game scene execution. DS340-byte search layout omits the later public68-byte namespace-array/count feature; same-address initialized/BSS views are minimum consumed typed contracts only.'


def case_count(a):return{0x020b0cd4:10,0x020b0e04:3,0x020b2908:7,0x020b29a0:7,0x020b30c8:10}[a]


def run(image,row,body,seed,bound=100000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or a not in[0x020b0cd4,0x020b0e04,0x020b2908,0x020b29a0,0x020b30c8]:raise ValueError('Exact GP operation namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def setword(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    def word(p):return struct.unpack('<I',uc.mem_read(p,4))[0]
    def text(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    uc.mem_write(STATE,b'\x5a'*0x700);uc.mem_write(OP,b'\x4b'*64);uc.mem_write(SEARCH,b'\xa5'*340);uc.mem_write(BUFFER,b'Z'*4098);setword(CONNECTION,STATE);setword(OP+4,SEARCH);setword(OUT,0xabababab)
    uc.mem_write(HOST,b'\0'*16);setword(HOST+12,ADDRLIST);setword(ADDRLIST,IPADDRESS);uc.mem_write(IPADDRESS,b'\x01\x02\x03\x04')
    callback=0 if seed==2 else CALLBACK;setword(OP+12,callback);setword(OP+16,PARAM)
    prefix=b'\\rn\\'if a==0x020b2908 else b'\\rc\\';uc.mem_write(MESSAGE,(b'bad!'if seed==1 else prefix)+b'payload\0')
    stat=0x021d2514;slot=0x020e15f0
    if a==0x020b30c8:
        sock=-1 if seed in[0,9]else 7;state=4 if seed==1 else 5;length=4;maximum=100 if seed in[3,4]else 256
        if seed==5:length=200
        setword(slot+4,sock);setword(stat+8,length);setword(stat+24,maximum);setword(stat+40,BUFFER);setword(stat+44,state)
    arguments=[CONNECTION,OP,MESSAGE]
    if a==0x020b0e04:arguments=[CONNECTION,OUT,17]
    if a==0x020b30c8:arguments=[]
    for r,v in zip(REGS,arguments):uc.reg_write(r,v)
    before=bytes(uc.mem_read(BASE,0x400000));expected=bytearray(before);calls=[];expected_calls=[];helpers={};observed=set();failures=[];returned=False;allocations=0;readable=0
    def ew(p,v):struct.pack_into('<I',expected,p-BASE,v&0xffffffff)
    def eb(p,data):expected[p-BASE:p-BASE+len(data)]=data
    result=0
    if a==0x020b0e04:
        expected_calls=[['allocate',340]]
        if seed==0:result=1;expected_calls+=[['error-string','Out of memory.']]
        else:
            expected_calls+=[['zero',340],['allocate',4097]];eb(SEARCH,b'\0'*340);ew(SEARCH,17);ew(SEARCH+4,-1);ew(SEARCH+28,4096);ew(SEARCH+24,0 if seed==1 else BUFFER)
            if seed==1:result=1;expected_calls+=[['error-string','Out of memory.']]
            else:ew(OUT,SEARCH)
    elif a in[0x020b2908,0x020b29a0]:
        expected_calls=[['check-error',MESSAGE,1]]
        if seed==0:result=4
        elif seed==1:result=3;expected_calls+=[['set-error',1,'Unexpected data was received from the server.'],['error-callback',3,1]]
        else:
            if callback:
                expected_calls+=[['allocate',4]]
                if seed==3:result=1;expected_calls+=[['error-string','Out of memory.']]
                else:
                    ew(BUFFER,0);expected_calls+=[['add-callback',CALLBACK,PARAM,BUFFER,OP,0]]
                    if seed==4:result=7
            if not result:expected_calls+=[['remove-operation',OP]]
    elif a==0x020b0cd4:
        expected_calls=[['allocate',4097]];ew(SEARCH+12,4096);ew(SEARCH+8,0 if seed==0 else BUFFER)
        if seed==0:result=1;expected_calls+=[['error-string','Out of memory.']]
        else:
            socket=-1 if seed==1 else 7;ew(SEARCH+4,socket);expected_calls+=[['socket',2,1,0]]
            if seed==1:result=3;message='There was an error creating a socket.'
            else:
                expected_calls+=[['blocking',7,0]]
                if seed==2:result=3;message='There was an error making a socket non-blocking.'
                else:
                    expected_calls+=[['resolve','gpsp.gs.nintendowifi.net']]
                    if seed==3:result=3;message='Could not resolve search mananger host name.'
                    else:
                        expected_calls+=[['connect',7,'000274cd01020304',8]]
                        if seed in[4,5,6,7]:expected_calls+=[['last-error',7]]
                        if seed==7:result=3;message='There was an error connecting a socket.'
                        else:expected_calls+=[['time']];ew(OP+20,1);ew(SEARCH+328,0x12345678)
            if result==3:expected_calls+=[['set-error',5,message],['error-callback',3,1]]
    else:
        result=0 if sock==-1 or state!=5 else 1
        if result:
            expected_calls=[['readable',7]]
            if seed not in[2]:
                if maximum-length<128:
                    maximum=256 if maximum<256 else maximum*2;ew(stat+24,maximum);ew(stat+40,0 if seed==3 else BUFFER);expected_calls+=[['resize',BUFFER,maximum+1]]
                if seed==3:result=0
                else:
                    n=-1 if seed==6 else 0 if seed==7 else 5;expected_calls+=[['receive',7,BUFFER+length,maximum-length,0]]
                    if n<=0:expected_calls+=[['close']];ew(slot+4,-1);result=0
                    else:
                        eb(BUFFER+length,b'HELLO');length+=5;eb(BUFFER+length,b'\0');processed=length if seed==4 else 2;expected_calls+=[['process',BUFFER,length]]
                        if processed==length:length=0
                        else:
                            expected_calls+=[['move',BUFFER,BUFFER+processed,length-processed]];eb(BUFFER,bytes(expected[BUFFER-BASE+processed:BUFFER-BASE+length]));length-=processed
                        ew(stat+8,length);expected_calls+=[['readable',7]]
    def finish(value):
        for r,v in zip([*REGS[:4],UC_ARM_REG_R12],[value&0xffffffff,0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,v)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,data):
        nonlocal returned,allocations,readable
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        if pc in HELPERS:
            if machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Original strncmp ARM mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(p<=pc<p+n for p,n in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Supplied provider mode differs')
        if pc in[0x020b2a4c,0x020b2c88,0x020b2c6c,0x020acbcc,0x020afad8,0x020acc28]and r[0]!=CONNECTION:failures.append('Provider connection owner differs')
        if pc==0x020a927c:
            calls.append(['allocate',r[0]]);allocations+=1
            fail=(a==0x020b0e04 and(seed==0 or(seed==1 and allocations==2)))or(a==0x020b0cd4 and seed==0)or(a in[0x020b2908,0x020b29a0]and seed==3)
            finish(0 if fail else SEARCH if a==0x020b0e04 and allocations==1 else BUFFER);return
        if pc==0x0201b208:calls.append(['zero',r[2]]);machine.mem_write(r[0],bytes([r[1]&255])*r[2]);finish(r[0]);return
        if pc==0x020b2a4c:calls.append(['check-error',r[1],r[2]]);finish(int(seed==0));return
        if pc==0x020b2c88:calls.append(['error-string',text(r[1])]);finish(0);return
        if pc==0x020b2c6c:calls.append(['set-error',r[1],text(r[2])]);finish(0);return
        if pc==0x020acbcc:calls.append(['error-callback',r[1],r[2]]);finish(0);return
        if pc==0x020afad8:calls.append(['remove-operation',r[1]]);finish(0);return
        if pc==0x020acc28:
            tail=struct.unpack('<II',machine.mem_read(machine.reg_read(UC_ARM_REG_SP),8));calls.append(['add-callback',*r[1:],*tail]);finish(7 if seed==4 else 0);return
        if pc==0x020a8b5c:calls.append(['socket',*r[:3]]);finish(-1 if seed==1 else 7);return
        if pc==0x020a8d54:calls.append(['blocking',r[0],r[1]]);finish(0 if seed==2 else 1);return
        if pc==0x0209046c:calls.append(['resolve',text(r[0])]);finish(0 if seed==3 else HOST);return
        if pc==0x020a8bc4:calls.append(['connect',r[0],bytes(machine.mem_read(r[1],8)).hex(),r[2]]);finish(-1 if seed in[4,5,6,7]else -2 if seed==8 else 0);return
        if pc==0x020a8c9c:calls.append(['last-error',r[0]]);finish({4:-6,5:-26,6:-76,7:-1}[seed]);return
        if pc==0x020a8ef8:calls.append(['time']);finish(0x12345678);return
        if pc==0x020b3264:calls.append(['readable',r[0]]);finish(int(readable==0 and seed!=2));readable+=1;return
        if pc==0x020a928c:calls.append(['resize',r[0],r[1]]);finish(0 if seed==3 else BUFFER);return
        if pc==0x020a8bf0:
            calls.append(['receive',*r]);n=-1 if seed==6 else 0 if seed==7 else 5
            if n>0:machine.mem_write(r[1],b'HELLO')
            finish(n);return
        if pc==0x020b3068:calls.append(['close']);setword(slot+4,-1);finish(0);return
        if pc==0x020b3588:calls.append(['process',r[0],r[1]]);finish(r[1]if seed==4 else 2);return
        if pc==0x0201b1bc:calls.append(['move',*r[:3]]);machine.mem_write(r[0],bytes(machine.mem_read(r[1],r[2])));finish(r[0]);return
        failures.append('Unqualified execution escaped caller/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(a|1,END+4,count=bound)
    if not returned or uc.reg_read(UC_ARM_REG_R0)!=result or calls!=expected_calls:failures.append('Independent caller return/provider model differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected:failures.append('Full protected caller/data/heap memory differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Complete return stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=uc.reg_read(UC_ARM_REG_R0),calls=calls,expectedCalls=expected_calls,helperEntries=helpers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!={0x020b0cd4,0x020b0e04,0x020b2908,0x020b29a0,0x020b30c8}:raise ValueError('Exact five source identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=[];specs=[]
    for a,n in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        if line is None:raise ValueError('Original strncmp full boundary/mode differs')
        specs.append(dict(address=hex(a),bytes=n,mode='arm',nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Original/C whole caller observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['calls']),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete caller prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
