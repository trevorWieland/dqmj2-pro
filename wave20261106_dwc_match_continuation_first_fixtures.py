import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,write_json
from wave20261106_dwc_match_continuation_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,CONNECTION,STATE,REGS,cstring

BROWSER=0x02302000
SERVERS=[BROWSER+0x100+i*0x40 for i in range(6)]
FRIENDS=BROWSER+0x400
OUT=BROWSER+0x800
NUMBER=BROWSER+0x900
TEXT=BROWSER+0xa00
CALLBACK=END+0x100
PARAM=0x24681357
TABLE=0x021d1ba8
HELPERS={0x020a3d70:(12,'thumb'),0x02026144:(524,'arm')}
ADDRESSES={0x020a2afc,0x020a2b44,0x020a2b98,0x020a2c38,0x020a2c80,0x020a2cc8,0x020a2ff8,0x020a304c,0x020a30b4,0x020a3528,0x020a3694,0x020a37ac}
LIMITS='Complete original/C matched callers return on synthetic1156-byte MatchControl,friend/peer/browser records and supplied error/search/browser/QR2/clock/random/callback services. Actual original Thumb GetMatchCnt12 and ARM signed-divide524 bodies execute. Supplied browser,QR2,clock,profile lookup,error and dynamic evaluation callback bodies execute0instructions. Weighted selection is bounded to0..6 servers; list indices/aid shifts stay within declared32 entries and0..31 shift domain. No actual network,I/O,clock,RNG,callback bodies,game scene,concurrency,Windows/Android or imported initialized/BSS storage authorship execution. Error enum inputs stay inside defined handled domains.'


def case_count(a):return{0x020a2afc:4,0x020a2b44:5,0x020a2b98:8,0x020a2c38:6,0x020a2c80:5,0x020a2cc8:4,0x020a2ff8:5,0x020a304c:7,0x020a30b4:21,0x020a3528:8,0x020a3694:7,0x020a37ac:13}[a]


def run(image,row,body,seed,bound=200000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or a not in ADDRESSES:raise ValueError('Exact DWC Match caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def sw(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    def word(p):return struct.unpack('<I',uc.mem_read(p,4))[0]
    def text(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    uc.mem_write(STATE,b'\x5a'*1156);sw(0x021d1b8c,STATE);uc.mem_write(FRIENDS,b'\x7c'*384);uc.mem_write(TABLE,b'\0'*1848);sw(NUMBER,23);sw(NUMBER+4,-7);uc.mem_write(TEXT,b'CustomValue\0');sw(TABLE,1);sw(TABLE+8,NUMBER);uc.mem_write(TABLE+12,b'\x01\x01');sw(TABLE+20,TEXT);sw(TABLE+153*12,1);sw(TABLE+153*12+8,NUMBER+4)
    uc.mem_write(STATE+720,bytes(range(32)));sw(STATE+228,BROWSER);sw(STATE+512,123456);uc.mem_write(STATE+20,b'\x03\x01\x06\x01');sw(STATE+32,-1);args=[];result=0;void=False;sem=[];calls=[];providers={};helpers={};observed=set();failures=[];returned=False;last_server=SERVERS[0];active=[];evals={};server_pids={};server_values={};randword=7;clock=0;qrstate=0
    if a==0x020a2afc:
        ids=[[0,1,2],[0,0],[1,2],list(range(32))][seed];uc.mem_write(STATE+20,bytes([len(ids)-1]));uc.mem_write(STATE+720,bytes(ids));result=next((i for i in range(32)if i not in ids),32)
    elif a==0x020a2b44:
        profiles=[[-1,77,88],[-1,88,99],[77],[77],[77]][seed];sw(STATE+764,0 if seed==3 else FRIENDS);sw(STATE+836,len(profiles));uc.mem_write(STATE+772,bytes(range(len(profiles))));args=[77];result=int(seed not in[1,3])
    elif a==0x020a2b98:
        args=[SERVERS[0]];values=dict(numplayers=4,maxplayers=6,dwc_mtype=1,dwc_mresv=1,dwc_mver=3,dwc_pid=1234)
        if seed in[0,1,2]:values[['numplayers','maxplayers','dwc_mtype'][seed]]=-1
        if seed in[3,4]:values['dwc_mresv']=-1
        if seed==5:values['dwc_mver']=-1
        if seed==6:values['dwc_pid']=0
        result=0 if seed in[0,1,2,3,5,6]else 1234
    elif a==0x020a2c38:
        ids=[100,200,300,400];n=0 if seed==5 else 3;uc.mem_write(STATE+13,bytes([n]));uc.mem_write(STATE+720,bytes([9,8,7,6]));
        for i,v in enumerate(ids):sw(STATE+244+4*i,v)
        target=[100,100,300,400,777,100][seed];idx0=seed!=0;args=[target,int(idx0)];indices=range(0 if idx0 else 1,n+1);result=next(([9,8,7,6][i]for i in indices if ids[i]==target),255)
    elif a==0x020a2c80:
        ids=[0,31]if seed==4 else[0,1,3,5]if seed!=2 else[0,2,2,2];n=0 if seed==3 else 1 if seed==4 else 3;uc.mem_write(STATE+13,bytes([n]));uc.mem_write(STATE+720,bytes(ids));sw(STATE+752,0xf0f0f0f3);args=[int(seed==0)];result=0xf0f0f0f2 if seed==0 else sum(1<<i for i in set(ids[1:n+1]))
    elif a==0x020a2cc8:void=True;clock=[0,1,0x12345678abcdef01,0xffffffffffffffff][seed]
    elif a==0x020a2ff8:
        args=[seed];result=seed
        if seed:sem=[['stop-match',9 if seed in[1,2]else 6,-81000-{1:1,2:2,3:10,4:20}[seed]]]
    elif a==0x020a304c:
        args=[seed];result=seed
        if seed:sem=[['stop-match',9 if seed in[5,6]else 6,-85000-{1:50,2:30,3:20,4:40,5:1,6:2}[seed]]]
    elif a==0x020a30b4:
        error=0 if seed==0 else 1+(seed-1)//4;qrstate=[2,4,5,0][0 if seed==0 else(seed-1)%4];args=[error];result=error
        if error:sem=[[{2:'stop-login',4:'stop-friend',5:'stop-match',0:'set-error'}[qrstate],6,{2:-64000,4:-74000,5:-84000,0:-94000}[qrstate]-{1:50,2:60,3:30,4:80,5:20}[error]]]
    elif a==0x020a3528:
        active=[]if seed==0 else SERVERS[:2]if seed in[2,3,7]else SERVERS[:1];server_pids={p:100+i for i,p in enumerate(active)};uc.mem_write(STATE+13,b'\x02');uc.mem_write(STATE+21,bytes([0 if seed in[2,3]else 1]));sw(STATE+248,100);sw(STATE+252,101 if seed==3 else 999);sw(STATE+1140,CALLBACK|1 if seed in[4,5,6,7]else 0);sw(STATE+1144,PARAM);evals={p:(-1 if seed==7 and i==0 else 10 if seed==4 or seed==7 else 0x800000 if seed==5 else 0)for i,p in enumerate(active)};args=[int(seed%2)];items=list(active);deleted=False;result=1
        for p in list(items):
            if seed in[2,3]and server_pids[p]in[100,101 if seed==3 else 999]:sem.append(['remove',p]);items.remove(p);continue
            if seed in[4,5,6,7]:
                value=evals[p];sem.append(['evaluate',items.index(p),PARAM])
                if value<=0:sem.append(['remove',p]);items.remove(p);deleted=True;continue
                sem.extend([['random',256],['add-key',p,'dwc_eval',min(value,0x7fffff)*256+7]])
            else:sem.extend([['random',128],['add-key',p,'dwc_eval',7]])
        if seed%2 and items:sem.append(['sort',0,'dwc_eval',0])
        result=int(not(deleted and not items))
    elif a==0x020a3694:
        void=True;n=[0,1,3,3,3,6,3][seed];active=SERVERS[:n];server_values={p:([0x7fffffff]*6 if seed==6 else[-1,10,20,4,5,6])[i]for i,p in enumerate(active)};randword=[0,0,0,37,99,99,75][seed]
        if n>1:
            weights=[3,3,2,2,1,1][:n];total=sum(weights);cumulative=0;chosen=n-1
            for i,w in enumerate(weights):
                cumulative+=100*w//total
                if i==n-1 or randword<cumulative:chosen=i;break
            score=min(max([0,*server_values.values()])+1,0x7fffffff);sem=[['random',100],['add-key',active[chosen],'dwc_eval',score],['sort',0,'dwc_eval',0]]
    else:
        void=True;key=[8,10,50,51,52,53,54,99,100,101,253,254,102][seed];args=[key,OUT,0xabcdef];v={8:3,10:6,50:123456,51:1,52:-1,53:3,54:1,100:23,253:-7}
        if key in v:sem=[['qr-int',OUT,v[key]]]
        elif key==101:sem=[['qr-text',OUT,'CustomValue']]
    for r,v in zip(REGS,args):uc.reg_write(r,v&0xffffffff)
    before=bytes(uc.mem_read(BASE,0x400000));expected=bytearray(before)
    if a==0x020a2cc8:expected[STATE-BASE+429]=0;struct.pack_into('<Q',expected,STATE-BASE+504,clock)
    def finish(v,wide=False):
        for r,x in zip([*REGS[:4],UC_ARM_REG_R12],[v&0xffffffff,(v>>32)&0xffffffff if wide else 0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,x)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def hook(machine,pc,size,opaque):
        nonlocal returned,last_server
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        if pc in HELPERS:
            if bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(HELPERS[pc][1]=='thumb'):failures.append('Actual getter/divide mode differs');machine.emu_stop();return
            helpers[hex(pc)]=helpers.get(hex(pc),0)+1
        if any(p<=pc<p+n for p,(n,m)in HELPERS.items()):return
        providers[hex(pc)]=providers.get(hex(pc),0)+1
        r=[machine.reg_read(x)for x in REGS[:4]];binding=next((b for b in row['nativeSymbolEntries'].values()if b['kind']=='function'and int(b['address'],0)==pc),None)
        if binding and bool(machine.reg_read(UC_ARM_REG_CPSR)&32)!=(binding['mode']=='thumb'):failures.append('Supplied provider mode differs')
        if pc==0x02007a9c:calls.append(['clock']);finish(clock,True);return
        if pc in[0x0209f130,0x0209c610,0x0209d03c,0x0209a9f8]:calls.append([{0x0209f130:'stop-match',0x0209c610:'stop-login',0x0209d03c:'stop-friend',0x0209a9f8:'set-error'}[pc],r[0],r[1]if r[1]<0x80000000 else r[1]-0x100000000]);finish(0);return
        if pc==0x0209bc88:finish(qrstate);return
        if pc==0x020a601c:
            key=text(r[1])
            if a==0x020a2b98:
                value=(8 if seed==4 else 0)if key=='dwc_mresv'and r[2]==0 else values[key]
            else:value=server_values[r[0]]if a==0x020a3694 else server_pids[r[0]]
            finish(value);return
        if pc==0x020a69a8:
            if r[0]!=BROWSER:failures.append('Actual browser owner differs')
            finish(len(active));return
        if pc==0x020a699c:
            if r[0]!=BROWSER or r[1]>=len(active):failures.append('Actual browser/index bounds differ');machine.emu_stop();return
            last_server=active[r[1]];finish(last_server);return
        if pc==0x020a691c:
            if r[0]!=BROWSER or r[1]not in active:failures.append('Actual browser removal differs');machine.emu_stop();return
            calls.append(['remove',r[1]]);active.remove(r[1]);finish(0);return
        if pc==0x0209b368:calls.append(['random',r[0]]);finish(randword);return
        if pc==0x020a5fc0:calls.append(['add-key',r[0],text(r[1]),r[2]]);finish(0);return
        if pc==0x020a69b4:
            if r[0]!=BROWSER:failures.append('Actual sort browser owner differs')
            calls.append(['sort',r[1],text(r[2]),r[3]]);finish(0);return
        if pc==CALLBACK:
            if not machine.reg_read(UC_ARM_REG_CPSR)&32:failures.append('Synthetic evaluation callback Thumb entry differs')
            calls.append(['evaluate',r[0],r[1]]);finish(evals[last_server]);return
        if pc==0x020b7568:calls.append(['qr-int',r[0],r[1]if r[1]<0x80000000 else r[1]-0x100000000]);finish(0);return
        if pc==0x020b7588:calls.append(['qr-text',r[0],text(r[1])]);finish(0);return
        if a==0x020a2b44:
            expected_address=int(next(b['address']for n,b in row['nativeSymbolEntries'].items()if n=='DWCi_GetProfileIDFromList'),0)
            if pc==expected_address:
                if r[0]>=len(profiles):failures.append('Actual friend-index bound differs');machine.emu_stop();return
                finish(profiles[r[0]]);return
        failures.append('Execution escaped exact Match caller/helper/provider set:'+hex(pc));machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook);uc.emu_start(a|1,END+4,count=bound)
    if not returned or(not void and uc.reg_read(UC_ARM_REG_R0)!=(result&0xffffffff)):failures.append('Independent full caller return model differs')
    if a not in[0x020a2b44,0x020a2b98,0x020a2cc8]and calls!=sem:failures.append('Independent supplied service/callback contract differs')
    if a==0x020a2cc8 and calls!=[['clock']]:failures.append('Actual two-word clock boundary differs')
    if bytes(uc.mem_read(BASE,0x400000))!=expected:failures.append('Full protected Match/heap/BSS/native memory differs')
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Complete caller stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=None if void else uc.reg_read(UC_ARM_REG_R0),calls=calls,expectedCalls=sem,helperEntries=helpers,suppliedProviderEntries=providers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(value)
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!=ADDRESSES:raise ValueError('Exact twelve Match identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();records=[];specs=[]
    for a,(n,mode)in HELPERS.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),s)),None)
        if line is None:raise ValueError('Actual getter/divide canonical extent/mode differs')
        specs.append(dict(address=hex(a),bytes=n,mode=mode,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Original/C complete Match caller observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=sum(left['suppliedProviderEntries'].values()),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete Match caller prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
