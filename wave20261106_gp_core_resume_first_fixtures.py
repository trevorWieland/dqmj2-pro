import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_gp_core_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS,cstring

OP=0x02302000
OP2=OP+0x100
HOST=OP+0x200
ADDRLIST=OP+0x240
IPADDRESS=OP+0x280
BUFFER=OP+0x300
HELPERS={0x0201d780:80,0x02026350:484}
TABLE=b'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
LIMITS='Complete original/C caller returns on synthetic GP connections,operations and supplied network/allocator/key services. Original ARM strncpy80 and signed-divide484 helper bodies execute; RNG,UDP,socket,DNS,free,key-state,profile-map and callback bodies do not. Startup retries model0..100 increments and explicit failure/allowed-error boundaries. Opaque48-byte context tail is preserved,not interpreted or credited. No actual network/I/O/random engine,callbacks,allocation,save/game scenes,concurrency,Windows/Android or imported storage authorship execution.'


def startup_cases():
    base=dict(initialized=False,failures=0,localPort=7777,firewall=False,handler=0,socket=7,blocking=1,direct=False,dns=True,connect=0,error=0)
    changes=[{},dict(failures=1),dict(failures=100),dict(failures=101),dict(initialized=True),dict(initialized=True,firewall=True),dict(firewall=True),dict(handler=7),dict(socket=-1),dict(blocking=0),dict(direct=True),dict(dns=False),dict(connect=-1,error=-6),dict(connect=-1,error=-26),dict(connect=-1,error=-76),dict(connect=-1,error=-1),dict(connect=-2)]
    return[dict(base,**change)for change in changes]


def case_count(address):return {0x020aa9b4:4,0x020aced4:6,0x020acf00:len(startup_cases())}[address]


def startup_model(c):
    calls=[['udp-initialized']];port=0x5a5a;socket=0x5a5a5a5a;success=False
    if not c['initialized']:
        tries=min(c['failures']+1,101)
        calls.extend(['udp-initialize',6500+i]for i in range(tries))
        if c['failures']>=101:return 3,calls+[['set-error',8,'There was error starting the UDP layer.'],['error-callback',3,1]],port,socket,success
        if not c['firewall']:port=6500+c['failures']
    else:calls.append(['udp-port']);port=c['localPort']
    calls.append(['register-handler'])
    if c['handler']:return 3,calls+[['set-error',8,'There was an error starting the UDP Layer.'],['error-callback',3,1]],port,socket,success
    if c['firewall']:port=0
    calls.append(['socket',2,1,0]);socket=c['socket']
    if socket==-1:return 3,calls+[['set-error',5,'There was an error creating a socket.'],['error-callback',3,1]],port,socket,success
    calls.append(['blocking',socket,0])
    if not c['blocking']:return 3,calls+[['set-error',5,'There was an error making a socket non-blocking.'],['error-callback',3,1]],port,socket,success
    calls.append(['inet','gpcm.gs.nintendowifi.net'])
    if not c['direct']:
        calls.append(['resolve','gpcm.gs.nintendowifi.net'])
        if not c['dns']:return 3,calls+[['set-error',5,'Could not resolve connection mananger host name.'],['error-callback',3,1]],port,socket,success
    else:calls.append(['inet','gpcm.gs.nintendowifi.net'])
    calls.append(['connect',socket,'000274cc01020304',8])
    if c['connect']==-1:
        calls.append(['last-error',socket])
        if c['error']not in[-6,-26,-76]:return 3,calls+[['set-error',5,'There was an error connecting a socket.'],['error-callback',3,1]],port,socket,success
    return 0,calls,port,socket,True


def run(image,row,body,seed,bound=200000,strict=True):
    address=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or address not in[0x020aa9b4,0x020aced4,0x020acf00]:raise ValueError('Exact GP core caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(address,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1);initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.mem_write(CONNECTION,struct.pack('<I',STATE));uc.mem_write(STATE,b'\x5a'*0x700);uc.mem_write(OP,b'\x4b'*64);uc.mem_write(OP2,b'\x6c'*64);uc.mem_write(BUFFER,b'\xa5'*128);calls=[];helpers={};observed=set();returned=False;failures=[];ports=[];random_words=[0,1,61,62,63,32767,12345];random_calls=0;init_calls=0;remove_calls=0;expected_result=0;expected_calls=[];expected_ram=None;c={}
    def word(offset,value):uc.mem_write(STATE+offset,struct.pack('<I',value&0xffffffff))
    if address==0x020aa9b4:
        free_ptrs=[0 if seed==0 else BUFFER+8*i for i in range(5)]
        for offset,pointer in zip([504,520,528,1504,1520],free_ptrs):word(offset,pointer)
        nodes=0 if seed in[0,1]else 2;word(1476,OP if nodes else 0);expected_calls=[['free',p]for p in free_ptrs]+[['destroy-keys'],['initialize-keys',STATE]];status=7 if seed==1 else 0;expected_result=status
        if status:expected_calls.append(['destroy-local-connection',STATE])
        else:expected_calls.extend([['remove-operation',OP],['remove-operation',OP2]]if nodes else[]);expected_calls.append(['profile-map',0x020aa9a5,0])
        arguments=[CONNECTION]
    elif address==0x020aced4:
        count=[-1,0,1,4,7,63][seed];arguments=[BUFFER,count&0xffffffff]
    else:
        c=startup_cases()[seed];word(268,int(c['firewall']));uc.mem_write(STATE+560,b'\x5a\x5a');uc.mem_write(HOST,b'\0'*16);uc.mem_write(HOST+12,struct.pack('<I',ADDRLIST));uc.mem_write(ADDRLIST,struct.pack('<I',IPADDRESS));uc.mem_write(IPADDRESS,b'\x01\x02\x03\x04');arguments=[CONNECTION,OP];expected_result,expected_calls,expected_port,expected_socket,success=startup_model(c)
    for r,v in zip(REGS,arguments):uc.reg_write(r,v)
    before=bytes(uc.mem_read(BASE,0x400000))
    def getstr(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    def finish(result):
        for r,v in zip([*REGS[:4],UC_ARM_REG_R12],[result&0xffffffff,0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,v)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,data):
        nonlocal returned,random_calls,init_calls,remove_calls
        if pc==END:returned=True;machine.emu_stop();return
        if address<=pc<address+len(body):observed.add(pc);return
        if pc in HELPERS:
            if machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Actual original string/division helper ARM mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(a<=pc<a+n for a,n in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];stack=machine.reg_read(UC_ARM_REG_SP);binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Actual original provider/callback mode differs')
        if address==0x020aa9b4:
            if pc==0x020a929c:calls.append(['free',r[0]]);finish(0);return
            if pc==0x020af494:
                if r[0]!=CONNECTION:failures.append('Actual key destroy owner differs')
                calls.append(['destroy-keys']);finish(0);return
            if pc in[0x020af460,0x020aa978]:
                if not STACK<=r[0]<sp:failures.append('Actual local connection out-pointer differs')
                actual=struct.unpack('<I',machine.mem_read(r[0],4))[0];calls.append(['initialize-keys'if pc==0x020af460 else'destroy-local-connection',actual]);finish(status if pc==0x020af460 else 0);return
            if pc==0x020afad8:
                if r[0]!=CONNECTION:failures.append('Actual operation owner differs')
                calls.append(['remove-operation',r[1]]);remove_calls+=1;machine.mem_write(STATE+1476,struct.pack('<I',OP2 if remove_calls==1 else 0));finish(0);return
            if pc==0x020b0bd0:
                if r[0]!=CONNECTION:failures.append('Actual profile-map owner differs')
                calls.append(['profile-map',r[1],r[2]]);finish(1);return
        if address==0x020aced4 and pc==0x0201d5d4:
            calls.append(['random-word']);finish(random_words[random_calls%len(random_words)]);random_calls+=1;return
        if address==0x020acf00:
            if pc==0x020a99c0:calls.append(['udp-initialized']);finish(int(c['initialized']));return
            if pc==0x020a99cc:
                trailing=list(struct.unpack('<IIIIIII',machine.mem_read(stack,28)))
                if r[1:]!=[0,0,0]or trailing!=[0]*7:failures.append('Actual11-word UDP initialization ABI differs')
                calls.append(['udp-initialize',r[0]]);ports.append(r[0]);result=7 if init_calls<c['failures']else 0;init_calls+=1;finish(result);return
            if pc==0x020a9d64:calls.append(['udp-port']);finish(c['localPort']);return
            if pc==0x020a9d78:
                trailing=list(struct.unpack('<IIII',machine.mem_read(stack,16)))
                if r!=[STATE+544,STATE+544,0,0x020b0771]or trailing!=[0x020b06b9,0x020b0791,0x020b06d1,CONNECTION]:failures.append('Actual original typed callback pointer/owner words differ')
                calls.append(['register-handler']);finish(c['handler']);return
            if pc==0x020a8b5c:calls.append(['socket',*r[:3]]);finish(c['socket']);return
            if pc==0x020a8d54:calls.append(['blocking',r[0],r[1]]);finish(c['blocking']);return
            if pc==0x020a8c84:calls.append(['inet',getstr(r[0])]);finish(0x04030201 if c['direct']else 0xffffffff);return
            if pc==0x0209046c:calls.append(['resolve',getstr(r[0])]);finish(HOST if c['dns']else 0);return
            if pc==0x020a8bc4:calls.append(['connect',r[0],bytes(machine.mem_read(r[1],8)).hex(),r[2]]);finish(c['connect']);return
            if pc==0x020a8c9c:calls.append(['last-error',r[0]]);finish(c['error']);return
            if pc==0x020b2c6c:
                if r[0]!=CONNECTION:failures.append('Actual network error owner differs')
                calls.append(['set-error',r[1],getstr(r[2])]);finish(0);return
            if pc==0x020acbcc:
                if r[0]!=CONNECTION:failures.append('Actual error callback owner differs')
                calls.append(['error-callback',r[1],r[2]]);finish(0);return
        failures.append('Execution escaped actual GP core caller/helpers/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(address|1,END+4,count=bound)
    expected_ram=bytearray(before)
    def write(offset,value):struct.pack_into('<I',expected_ram,STATE-BASE+offset,value&0xffffffff)
    if address==0x020aa9b4:
        for offset in[272,303,324]:expected_ram[STATE-BASE+offset]=0
        write(496,-1);write(500,0)
        for offset in[504,508,512,516,520,524,528,532,536,540,1504,1508,1512,1516,1520,1524,1528,1532]:write(offset,0)
        if not status:
            for offset in[1476,1488,412,416,408,568,1468,1492,1584]:write(offset,0)
            write(564,2);write(572,-1)
            for offset in[952,1208]:expected_ram[STATE-BASE+offset]=0
    elif address==0x020aced4:
        n=max(0,count);text=bytes(TABLE[random_words[i%len(random_words)]%62]for i in range(n))+b'\0';expected_ram[BUFFER-BASE:BUFFER-BASE+len(text)]=text;expected_calls=[['random-word']]*n
    else:
        expected_ram[STATE-BASE+544:STATE-BASE+560]=b'gamespygp'+b'\0'*7;struct.pack_into('<H',expected_ram,STATE-BASE+560,expected_port);write(496,expected_socket)
        if success:write(500,1);struct.pack_into('<I',expected_ram,OP-BASE+20,1)
    if not returned or calls!=expected_calls or(address!=0x020aced4 and uc.reg_read(UC_ARM_REG_R0)!=expected_result):failures.append('Independent full reset/random/startup boundary model differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Actual complete caller stack/callee-save contract differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected_ram:failures.append('Full protected RAM differs outside declared caller/operation writes')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=uc.reg_read(UC_ARM_REG_R0)if address!=0x020aced4 else None,calls=calls,helperEntries=helpers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!={0x020aa9b4,0x020aced4,0x020acf00}:raise ValueError('Exact GP core moderate subset differs')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();specs=[];records=[]
    for a,n in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        if line is None:raise ValueError('Actual full original helper entry/extent/mode differs')
        specs.append(dict(address=hex(a),bytes=n,mode='arm',canonicalInventoryRecord=line,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Actual original/C whole GP core observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['calls']),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete GP core prefix admitted as complete return')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
