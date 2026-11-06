import match_runtime
import base64
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_gpi_buddy_resume_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,PEER,PROFILE,STATUS,OP,MESSAGE,REGS,cstring

ENTRY=0x020ac130
HELPERS={0x0201d800:276,0x0201d69c:28}
NEXT=OP+0x100
KEYS=OP+0x200
VALUES=OP+0x240
ARG=OP+0x280
DARRAY=OP+0x2c0
CALLBACK=0x12345001
USER=0xabcdef00
LIMITS='Complete724-byte original/C key-reply caller returns on synthetic profiles/peer queues and bounded0..2 keys. Original ARM strcmp276/strlen28 bodies execute; key parser/Base64/atoi/allocator/duplicate/check-add-set/callback/queue provider bodies are supplied and unexecuted. Binary decoded payloads are modeled only at those boundaries. No arbitrary malformed or negative counts,allocation failure handling,real network,I/O,callbacks,game scenes,concurrency,Windows/Android or imported storage authorship execution.'


def cases():
    base=dict(found=True,empty=False,count=0,header=True,queue='match',callback=True,existing=False,checkResult=0)
    changes=[dict(found=False),dict(empty=True,queue='none'),dict(empty=True,queue='wrong'),dict(empty=True,callback=False),dict(empty=True),dict(header=False),dict(queue='none'),dict(queue='wrong'),dict(callback=False),{},dict(count=1,queue='none'),dict(count=1),dict(count=2,existing=True),dict(count=2,checkResult=7),dict(count=2,queue='wrong'),dict(count=2,callback=False)]
    return [dict(base,**c)for c in changes]


def helper_specs(image):
    inventory=(ROOT/'config/arm9/symbols.txt').read_text();values=[]
    for a,n in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(n,a),s)),None)
        if line is None:raise ValueError('Actual key-reply string helper boundary/mode differs')
        values.append(dict(address=hex(a),mode='arm',bytes=n,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    return values


def expected(c):
    calls=[['get-profile',123]];payload=None
    if not c['found']:return 2,calls+[['error-string','Invalid profile.']],payload
    if not c['empty']:
        calls.append(['read-pair',0])
        if not c['header']:return 3,calls+[['set-error',1,'Error reading keys reply message'],['error-callback',3,0]],payload
        calls.append(['atoi',str(c['count'])])
    if not c['empty']and c['count']>0:
        calls.extend([['allocate',4*c['count']],['allocate',4*c['count']]])
        for i in range(c['count']):
            key=('key'+str(i)).encode();value=('value'+str(i)).encode();calls.append(['read-pair',i+1]);calls.extend([['decode',base64.b64encode(key).decode(),2],['decode',base64.b64encode(value).decode(),2],['duplicate',key.decode()],['duplicate',value.decode()],['check-key',key.decode()]])
            calls.append(['set-key'if c['existing']or c['checkResult']else'add-key',key.decode(),value.decode()])
    if c['queue']=='match'and c['callback']:
        calls.append(['allocate',16]);payload=[123,KEYS if c['count']and not c['empty']else 0,VALUES if c['count']and not c['empty']else 0,c['count']if not c['empty']else 0];calls.extend([['add-callback',CALLBACK,USER,payload,14 if c['count']and not c['empty']else 0],['remove-operation',NEXT]])
    return 0,calls,payload


def run(image,row,body,seed,bound=20000,strict=True):
    if(row.get('program')or'',row['processor'],row['module'],row['mode'],int(row['address'],0))!=('','arm9','main','thumb',ENTRY):raise ValueError('Actual full key-reply namespace differs')
    c=cases()[seed];uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(ENTRY,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1);initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    for p,n in[(PEER,80),(PROFILE,32),(STATUS,60),(OP,24),(NEXT,24),(KEYS,32),(VALUES,32),(ARG,16),(DARRAY,16)]:uc.mem_write(p,b'\0'*n)
    uc.mem_write(CONNECTION,struct.pack('<I',STATE));uc.mem_write(PEER+16,struct.pack('<I',123));uc.mem_write(PEER+68,struct.pack('<I',0 if c['queue']=='none'else OP));uc.mem_write(OP+12,struct.pack('<I',NEXT if c['queue']=='match'else 0));uc.mem_write(OP+16,struct.pack('<I',103));uc.mem_write(NEXT,struct.pack('<IIIIII',0,USER,CALLBACK if c['callback']else 0,0,104,0));uc.mem_write(PROFILE+12,struct.pack('<I',STATUS));uc.mem_write(STATUS+56,struct.pack('<I',DARRAY));uc.mem_write(MESSAGE,(b''if c['empty']else b'encoded-key-message')+b'\0')
    for r,v in zip(REGS,[CONNECTION,PEER,MESSAGE]):uc.reg_write(r,v)
    before=bytes(uc.mem_read(BASE,0x400000));expected_result,expected_calls,payload=expected(c);calls=[];helpers={};observed=set();allocations=[];duplicates=[];read_index=0;returned=False;failures=[]
    def getstr(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    def finish(result):
        for r,v in zip([*REGS[:4],UC_ARM_REG_R12],[result&0xffffffff,0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,v)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,data):
        nonlocal returned,read_index
        if pc==END:returned=True;machine.emu_stop();return
        if ENTRY<=pc<ENTRY+len(body):observed.add(pc);return
        if pc in HELPERS:
            if machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Actual original string helper ARM mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(a<=pc<a+n for a,n in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];stack=machine.reg_read(UC_ARM_REG_SP)
        if pc in[0x020b0a50,0x020b2c88,0x020b2c6c,0x020acbcc,0x020b2b90,0x020af578,0x020af4bc,0x020af510,0x020acc28]and r[0]!=CONNECTION:failures.append('Actual original connection argument word differs')
        binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Actual original provider entry mode differs')
        if pc==0x020b0a50:calls.append(['get-profile',r[1]]);machine.mem_write(r[2],struct.pack('<I',PROFILE if c['found']else 0));finish(int(c['found']));return
        if pc==0x020b2c88:calls.append(['error-string',getstr(r[1])]);finish(0);return
        if pc==0x020b2c6c:calls.append(['set-error',r[1],getstr(r[2])]);finish(0);return
        if pc==0x020acbcc:calls.append(['error-callback',r[1],r[2]]);finish(0);return
        if pc==0x020b2b90:
            key_value=struct.unpack('<I',machine.mem_read(stack,4))[0];calls.append(['read-pair',read_index]);offset=struct.unpack('<i',machine.mem_read(r[2],4))[0]
            if offset!=read_index:failures.append('Actual native read-pair index pointer/flow differs')
            if read_index==0:key=b'keys'if c['header']else b'wrong';value=str(c['count']).encode()
            else:key=base64.b64encode(('key'+str(read_index-1)).encode());value=base64.b64encode(('value'+str(read_index-1)).encode())
            machine.mem_write(r[3],key+b'\0');machine.mem_write(key_value,value+b'\0');read_index+=1;machine.mem_write(r[2],struct.pack('<I',read_index));finish(0);return
        if pc==0x0201f274:calls.append(['atoi',getstr(r[0])]);finish(int(getstr(r[0])));return
        if pc==0x020a927c:
            calls.append(['allocate',r[0]]);result=ARG if r[0]==16 else KEYS if not allocations else VALUES;allocations.append((result,r[0]));finish(result);return
        if pc==0x020a9040:
            mode=struct.unpack('<I',machine.mem_read(stack,4))[0];encoded=bytes(machine.mem_read(r[0],r[2]));decoded=base64.b64decode(encoded);calls.append(['decode',encoded.decode(),mode]);machine.mem_write(r[1],decoded);machine.mem_write(r[3],struct.pack('<i',len(decoded)));finish(0);return
        if pc==0x020a8ea0:
            text=getstr(r[0]);calls.append(['duplicate',text]);target=DARRAY+0x100+len(duplicates)*0x40;machine.mem_write(target,text.encode()+b'\0');duplicates.append((target,text));finish(target);return
        if pc==0x020af578:
            if r[1]!=DARRAY:failures.append('Actual extended-key array view differs')
            calls.append(['check-key',getstr(r[2])]);machine.mem_write(r[3],struct.pack('<I',DARRAY if c['existing']else 0));finish(c['checkResult']);return
        if pc in[0x020af4bc,0x020af510]:calls.append(['add-key'if pc==0x020af4bc else'set-key',getstr(r[2]),getstr(r[3])]);finish(0);return
        if pc==0x020acc28:
            operation,flag=struct.unpack('<II',machine.mem_read(stack,8));actual=list(struct.unpack('<IIII',machine.mem_read(r[3],16)));calls.append(['add-callback',r[1],r[2],actual,flag])
            if r[0]!=CONNECTION or operation:failures.append('Actual callback aggregate/operation ABI differs')
            finish(0);return
        if pc==0x020b07c0:
            calls.append(['remove-operation',r[1]])
            if r[0]!=PEER:failures.append('Actual peer-operation owner differs')
            finish(0);return
        failures.append('Execution escaped actual native key caller/helpers/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(ENTRY|1,END+4,count=bound)
    if not returned or calls!=expected_calls or uc.reg_read(UC_ARM_REG_R0)!=expected_result:failures.append('Independent whole key/queue/callback model differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Actual complete key caller callee-save/stack differs')
    expected_ram=bytearray(before)
    for target,text in duplicates:expected_ram[target-BASE:target-BASE+len(text)+1]=text.encode()+b'\0'
    if c['found']and not c['empty']and c['header']and c['count']>0:
        for i in range(c['count']):
            struct.pack_into('<I',expected_ram,KEYS-BASE+4*i,DARRAY+0x100+2*i*0x40);struct.pack_into('<I',expected_ram,VALUES-BASE+4*i,DARRAY+0x100+(2*i+1)*0x40)
    if payload is not None:struct.pack_into('<IIII',expected_ram,ARG-BASE,*payload)
    if bytes(uc.mem_read(BASE,0x400000))!=expected_ram:failures.append('Full protected main RAM differs outside explicit supplied duplicate/caller array/response writes')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=uc.reg_read(UC_ARM_REG_R0),calls=calls,helperEntries=helpers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if len(rows)!=1 or int(rows[0]['address'],0)!=ENTRY:raise ValueError('Exact key-reply singleton differs')
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();specs=helper_specs(image);native=image[ENTRY-BASE:ENTRY-BASE+724];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();records=[]
    for seed in range(len(cases())):
        left=run(image,row,native,seed);right=run(image,row,body,seed)
        if left!=right:raise ValueError('Actual original/C whole key caller traces differ')
        records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=len(left['calls']),original=left,candidate=right))
    if run(image,row,native,0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete key caller prefix counted as complete return')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
