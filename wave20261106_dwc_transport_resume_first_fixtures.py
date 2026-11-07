import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_dwc_transport_resume_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS

BUFFER=0x02303000
RECEIVE=BUFFER+0x1000
HEADER=BUFFER+0x2200
LINK=BUFFER+0x2300
AID=3
RECORD=STATE+48*AID
SENDCB=END+0x100
RECVCB=END+0x200
TIMECB=END+0x300
PINGCB=END+0x400
HELPERS={0x020a4378:(16,'thumb'),0x020a439c:(20,'thumb'),0x020a40f8:(28,'thumb'),0x020a4114:(48,'thumb'),0x02008e0c:(304,'arm'),0x0201b248:(64,'arm'),0x0201d780:(80,'arm')}
COUNTS={0x020a3f84:6,0x020a40a4:3,0x020a40c0:3,0x020a40dc:3,0x020a4114:4,0x020a4144:6,0x020a4158:3,0x020a41dc:3,0x020a431c:3,0x020a4404:8,0x020a449c:5,0x020a44f4:9,0x020a456c:8,0x020a45fc:4}
LIMITS='Complete original/C transport callers return on synthetic32x48 release connections,8-byte DT wire headers,bounded send/receive buffers and callback/provider interfaces. Actual original Thumb connection/state/header helpers and ARM copy304/memcmp64 bodies execute; imported helper/storage source credit remains0. Supplied sendability,send/free-space,protocol dispatch,clock,error,connection-to-AID and synthetic callback providers execute0bodyinstructions. No real GT2/network,allocator,clock,queue hook,I/O,callbacks,game scene,concurrency or Windows/Android execution. Receive sizes are nonnegative and all selected aids0..31. Native release Clear differs from public by unconditionally removing receive buffer/size/state; matched sendBuffer remains unchanged.'


def case_count(a):return COUNTS[a]


def run(image,row,body,seed,bound=100000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or a not in COUNTS:raise ValueError('Exact transport caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def sw(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    def sh(p,v):uc.mem_write(p,struct.pack('<H',v&65535))
    uc.mem_write(STATE,b'\x5a'*1556);uc.mem_write(BUFFER,bytes(range(64)));uc.mem_write(RECEIVE,b'Z'*128);uc.mem_write(HEADER,struct.pack('<iH2s',8,1,b'DT'));sw(0x021d2308,STATE);sw(RECORD,BUFFER);sw(RECORD+4,RECEIVE);sw(RECORD+8,8);sw(RECORD+12,0);sw(RECORD+16,0);sw(RECORD+20,8);sw(RECORD+24,8);uc.mem_write(RECORD+28,b'\0\x02\x01');sh(RECORD+34,1);sw(RECORD+44,9);sw(STATE+1536,SENDCB|1);sw(STATE+1540,RECVCB|1);sw(STATE+1544,TIMECB|1);sw(STATE+1548,PINGCB|1);sh(STATE+1552,16);clock=0x12345678abcdef01;args=[];result=0;void=False;sem=[];selected_type=1;size=8
    if a in[0x020a40a4,0x020a40c0,0x020a40dc]:
        sw(0x021d2308,0 if seed==0 else STATE);args=[0 if seed==1 else RECVCB|1];result=int(seed!=0)
    elif a==0x020a4158:sw(0x021d2308,0 if seed==0 else STATE);args=[AID,0 if seed==1 else 0xffffffff];result=int(seed!=0)
    elif a==0x020a431c:void=True;sw(0x021d2308,0 if seed==0 else STATE);args=[AID]
    elif a==0x020a41dc:void=True;sw(STATE+1548,0 if seed==0 else PINGCB|1);latency=[0,123,-7][seed];args=[LINK,latency&0xffffffff]
    elif a==0x020a4114:
        kind=[1,3,65535,2][seed];uc.mem_write(HEADER,struct.pack('<iH2s',8,kind,b'XX'if seed==3 else b'DT'));args=[HEADER];result=0 if seed==3 else kind
    elif a==0x020a4144:args=[seed];result=12 if seed in[2,3,4]else 8
    elif a==0x020a3f84:
        selected_type=2 if seed==5 else 1;size=32 if seed in[2,3]else 8;sw(STATE+1536,0 if seed==4 else SENDCB|1);args=[selected_type,AID,BUFFER,size];result=int(seed!=0)
    elif a==0x020a4404:
        void=True;state=[0,0,1,2,3,4,5,0][seed];kind=2 if seed==0 else 1 if seed in[1,2]else 0 if seed==7 else 3;uc.mem_write(RECORD+29,bytes([state]));uc.mem_write(HEADER,struct.pack('<iH2s',8,kind,b'XX'if seed==7 else b'DT'));args=[LINK,HEADER,8]
    elif a==0x020a449c:
        void=True;sw(RECORD+4,0 if seed==0 else RECEIVE);sw(RECORD+8,4 if seed==1 else 8);sw(STATE+1540,0 if seed==3 else RECVCB|1);sw(STATE+1544,0 if seed==4 else TIMECB|1);args=[LINK,BUFFER,8]
    elif a==0x020a44f4:
        void=True;kind=[1,1,1,1,2,3,4,0,9][seed];size=7 if seed==3 else 8;uc.mem_write(HEADER,struct.pack('<iH2s',8,kind,b'XX'if seed==7 else b'DT'));sw(RECORD+8,4 if seed==1 else 8);sw(RECORD+4,0 if seed==2 else RECEIVE);uc.mem_write(RECORD+29,b'\x01');args=[AID,HEADER,size]
    elif a==0x020a456c:
        void=True;size=4 if seed in[0,3,4,5]else 8;sw(RECORD+16,4 if seed==3 else 6 if seed==4 else 0);uc.mem_write(RECORD+29,bytes([3 if seed==5 else 2]));sw(STATE+1540,0 if seed==2 else RECVCB|1);sw(STATE+1544,0 if seed==7 else TIMECB|1);sw(RECORD+44,0 if seed==6 else 9);args=[AID,BUFFER,size]
    else:void=True;sh(RECORD+34,[0,2,3,4][seed]);args=[AID,BUFFER,8]
    for r,v in zip(REGS,args):uc.reg_write(r,v&0xffffffff)
    before=bytes(uc.mem_read(BASE,0x400000));expected=bytearray(before);calls=[];helpers={};providers={};observed=set();failures=[];returned=False
    def ew(p,v):struct.pack_into('<I',expected,p-BASE,v&0xffffffff)
    def eh(p,v):struct.pack_into('<H',expected,p-BASE,v&65535)
    def eb(p,data):expected[p-BASE:p-BASE+len(data)]=data
    def tick():struct.pack_into('<Q',expected,RECORD-BASE+36,clock)
    if a in[0x020a40a4,0x020a40c0,0x020a40dc]and seed!=0:ew(STATE+{0x020a40a4:1536,0x020a40c0:1540,0x020a40dc:1544}[a],args[0])
    elif a==0x020a4158 and seed!=0:ew(RECORD+44,args[1]);tick();sem=[['clock']]
    elif a==0x020a431c and seed!=0:
        for p in[4,8,12,16,20,24]:ew(RECORD+p,0)
        eb(RECORD+28,b'\0\0');eh(RECORD+34,0)
    elif a==0x020a41dc:sem=[['connection-aid',LINK],['ping-callback',latency,AID]]if seed!=0 else[]
    elif a==0x020a3f84:
        sem=[['sendable',AID,selected_type]]
        if seed!=0:
            eb(RECORD+28,b'\x01');ew(RECORD,BUFFER);ew(RECORD+12,0);ew(RECORD+20,size);wire=struct.pack('<iH2s',size,selected_type,b'DT');sem+=[['send',AID,wire.hex(),8,1],['free-space',AID]]
            if seed!=3:
                amount=min(size,16);sem+=[['send',AID,bytes(uc.mem_read(BUFFER,amount)).hex(),amount,1]];ew(RECORD+12,amount)
                if amount==size:
                    eb(RECORD+28,b'\0');ew(RECORD,0);ew(RECORD+12,0);ew(RECORD+20,0)
                    if seed not in[4,5]:sem+=[['send-callback',size,AID]]
    elif a==0x020a4404:
        sem=[['connection-aid',LINK]]
        if state==0 and kind in[2,3,4]or state==1:sem+=[['receive-header',AID,HEADER,8]]
        elif state==2:sem+=[['receive-body',AID,HEADER,8]]
        elif state==3:sem+=[['receive-system',AID,HEADER,8]]
        elif state==4:eb(RECORD+29,b'\x01');ew(RECORD+16,0);ew(RECORD+24,0)
        elif state not in[0,1,2,3,4]:sem+=[['error',6,-97610]]
    elif a==0x020a449c:
        sem=[['connection-aid',LINK]]
        if seed not in[0,1]:
            if seed!=3:sem+=[['receive-callback',AID,BUFFER,8]]
            if seed!=4:sem+=[['clock']];tick()
    elif a==0x020a44f4:
        eb(RECORD+30,b'\x01')
        if not(seed==3 and kind==1):
            eh(RECORD+34,kind)
            if kind==1:ew(RECORD+24,8);ew(RECORD+16,0);eb(RECORD+29,bytes([4 if seed in[1,2]else 2]))
            elif kind in[2,3,4]:eb(RECORD+29,b'\x03')
    elif a==0x020a456c:
        received=4 if seed==3 else 6 if seed==4 else 0
        if seed==4:sem=[['error',6,-97620]]
        else:
            if seed!=5:eb(RECEIVE+received,bytes(uc.mem_read(BUFFER,size)))
            received+=size;ew(RECORD+16,received)
            if received==8:
                eb(RECORD+29,b'\x01');ew(RECORD+16,0);ew(RECORD+24,0)
                if seed!=2:sem+=[['receive-callback',AID,RECEIVE,8]]
            if seed not in[6,7]:sem+=[['clock']];tick()
    elif a==0x020a45fc:
        eb(RECORD+29,b'\x01')
        if seed!=0:sem=[['match-sync',AID,[0,2,3,4][seed],BUFFER]]
    def finish(v,wide=False):
        for r,x in zip([*REGS[:4],UC_ARM_REG_R12],[v&0xffffffff,(v>>32)&0xffffffff if wide else 0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,x)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,insn_size,opaque):
        nonlocal returned
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        if pc in HELPERS:
            n,mode=HELPERS[pc]
            if bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):failures.append('Original protocol/memory helper mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(p<=pc<p+n for p,(n,m)in HELPERS.items()):return
        r=[machine.reg_read(x)for x in REGS[:4]];binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Supplied transport provider mode differs')
        providers[hex(pc)]=providers.get(hex(pc),0)+1
        if pc==0x02007a9c:calls.append(['clock']);finish(clock,True);return
        if pc==0x020a3f10:calls.append(['sendable',r[0],r[1]]);finish(int(seed!=0));return
        if pc==0x020a4624:calls.append(['free-space',r[0]]);finish(8 if seed==3 else 16);return
        if pc==0x020a43b0:calls.append(['send',r[0],bytes(machine.mem_read(r[1],r[2])).hex(),r[2],r[3]]);finish(0);return
        if pc==0x0209bd60:calls.append(['connection-aid',r[0]]);finish(AID);return
        if pc in[0x020a44f4,0x020a456c,0x020a45fc]:calls.append([{0x020a44f4:'receive-header',0x020a456c:'receive-body',0x020a45fc:'receive-system'}[pc],*r[:3]]);finish(0);return
        if pc==0x0209a9f8:calls.append(['error',r[0],r[1]if r[1]<0x80000000 else r[1]-0x100000000]);finish(0);return
        if pc==0x0209f1e8:calls.append(['match-sync',*r[:3]]);finish(0);return
        if pc in[SENDCB,RECVCB,TIMECB,PINGCB]:
            if not machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Synthetic typed callback mode differs')
            if pc==SENDCB:calls.append(['send-callback',r[0],r[1]])
            elif pc==RECVCB:calls.append(['receive-callback',*r[:3]])
            elif pc==PINGCB:calls.append(['ping-callback',r[0]if r[0]<0x80000000 else r[0]-0x100000000,r[1]])
            else:calls.append(['timeout-callback',r[0]])
            finish(0);return
        failures.append('Execution escaped exact transport caller/helper/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(a|1,END+4,count=bound)
    if not returned or(not void and uc.reg_read(UC_ARM_REG_R0)!=(result&0xffffffff))or calls!=sem:failures.append('Independent full transport return/provider model differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected:failures.append('Full protected transport/header/receive/native memory differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Complete caller stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=None if void else uc.reg_read(UC_ARM_REG_R0),calls=calls,expectedCalls=sem,helperEntries=helpers,suppliedProviderEntries=providers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!=set(COUNTS):raise ValueError('Exact fourteen transport identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=[];specs=[]
    for a,(n,mode)in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),s)),None)
        if line is None:raise ValueError('Actual original transport helper mode/extent differs')
        specs.append(dict(address=hex(a),bytes=n,mode=mode,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Original/C complete transport observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=sum(left['suppliedProviderEntries'].values()),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete transport prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
