import match_runtime
import hashlib
import json
import re
import struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
from project import ROOT,read_json,write_json
from wave20261106_dwc_match_control_first_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_gpi_buddy_resume_first_fixtures import BASE,STACK,END,STATE,REGS,cstring

BUFFER=0x02302000
BROWSER=BUFFER+0x1000
QR=BUFFER+0x1100
OPTION=BUFFER+0x1200
SOCKETPTR=BUFFER+0x1300
SOCKET=BUFFER+0x1400
CONNECTION=BUFFER+0x1500
CONNSLOT=BUFFER+0x1600
CONINFO=BUFFER+0x1700
CALLBACKS=BUFFER+0x1800
GAMENAME=BUFFER+0x1900
SECRET=BUFFER+0x1a00
OLD=BUFFER+0x1b00
ALLOCATED=BUFFER+0x1c00
HELPMODE={0x020a3d70:(12,'thumb'),0x02008e0c:(304,'arm'),0x0201d69c:(28,'arm')}
SEND_CASES=[(-1,0,0),(0,1,1)]+[(t,s,0)for t in range(4)for s in[0,1,4,6,11,12]]
COUNTS={0x0209dfd8:6,0x0209e0fc:8,0x0209e258:12,0x0209e408:len(SEND_CASES),0x0209ed44:9,0x0209ef04:10}
LIMITS='Complete original/C caller returns on synthetic1156-byte MatchControl,QR2 minimum184-byte consumed view,8-byte connection info and bounded friend/filter buffers. Original GetMatchCnt12,copy304,strlen28 helpers actually execute; their source and imported storage receive0credit. Allocator,free,QR2,GT2,browser,clockless formatter,key-builder,protocol,state/common setters,error,connection-record lookup and callback services are supplied boundaries with0bodyinstructions; their response/output contracts are explicit. No real networking,SDK provider bodies,callback bodies,allocation,I/O,hardware,game scenes,concurrency or Windows/Android execution. QR2 retry count0..5;friend list length0..2;GT2 indices0/1 and bounded connection counts0/1;filter copy229 bytes includes initialized caller buffer tail. Invalid size/pointer domains and negative latency are not executed.'


def case_count(a):return COUNTS[a]


def run(image,row,body,seed,bound=250000,strict=True):
    a=int(row['address'],0)
    if(row.get('program')or'',row['processor'],row['module'],row['mode'])!=('','arm9','main','thumb')or a not in COUNTS:raise ValueError('Exact Match-control caller namespace differs')
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(BASE,0x400000);uc.mem_write(BASE,image);uc.mem_write(a,body);uc.mem_map(STACK,0x10000);uc.mem_map(END,0x1000);uc.mem_write(STACK,b'\xa5'*0x10000);sp=STACK+0xf000
    initial=[((i+1)*0x11223344^(seed*0x01010101))&0xffffffff for i in range(13)]
    for r,v in zip(REGS,initial):uc.reg_write(r,v)
    uc.reg_write(UC_ARM_REG_CPSR,0x30|((seed%4)<<28));uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,END|1)
    def sw(p,v):uc.mem_write(p,struct.pack('<I',v&0xffffffff))
    def sh(p,v):uc.mem_write(p,struct.pack('<H',v&65535))
    def sb(p,v):uc.mem_write(p,bytes([v&255]))
    def word(p):return struct.unpack('<I',uc.mem_read(p,4))[0]
    def text(p):return bytes.fromhex(cstring(uc,p)).decode('ascii')
    uc.mem_write(STATE,b'\x5a'*1156);uc.mem_write(QR,b'\0'*184);uc.mem_write(BUFFER,b'\x6d'*512);uc.mem_write(BUFFER,b'A=B\0');uc.mem_write(GAMENAME,b'Game\0');uc.mem_write(SECRET,b'Secret\0');uc.mem_write(CONINFO,b'\x7c'*8);sw(CONNSLOT,0xabcdef);sw(SOCKETPTR,SOCKET);sw(STATE+4,SOCKETPTR);sw(STATE+8,CALLBACKS);sw(STATE+16,QR);sw(STATE+228,BROWSER);sw(STATE+512,123456);sw(STATE+756,GAMENAME);sw(STATE+760,SECRET);sw(0x021d1b88,0);sw(0x021d1b8c,STATE);sw(0x021d1b90,0);sb(STATE+12,0);sb(STATE+13,0);sb(STATE+20,0);sb(STATE+21,0);sb(STATE+425,0);sw(STATE+416,7);sw(STATE+244,991);sw(STATE+248,992);sw(STATE+528,0x01020304);sw(STATE+532,0x11223344);sh(STATE+656,6500);sh(STATE+658,6600);uc.mem_write(STATE+720,bytes([3,7,9]));sw(STATE+396,17);sw(STATE+400,23);uc.mem_write(BUFFER+0x300,b'991\0');args=[];calls=[];sem=[];helpers={};providers={};failures=[];observed=set();returned=False;result=0;void=a!=0x0209dfd8;qr_errors=[0];qcount=0;new_browser=BROWSER;sb_error=0;gp_error=0;reservation_error=0;startup_error=0;index=0;accept=1;cancel=1;gt2_result=0;latency=128;remote_ip=0x01020304;remote_port=6500;message=BUFFER+0x300;count=0;sid=0;filter_arg=0;friendlen=2;distant=1;num_entry=4;expected_writes=[]
    def ew(p,data):expected_writes.append((p,bytes(data)))
    def eword(p,v):ew(p,struct.pack('<I',v&0xffffffff))
    def ehalf(p,v):ew(p,struct.pack('<H',v&65535))
    def ebyte(p,v):ew(p,bytes([v&255]))
    if a==0x0209dfd8:
        args=[234567];sw(STATE+16,QR if seed==0 else 0);qr_errors={0:[0],1:[0],2:[3,0],3:[1],4:[3]*5,5:[3,3,0]}[seed]
        if seed:
            eword(STATE+512,234567)
            for error in qr_errors:
                sem.extend([['socket',SOCKET],['port',SOCKET],['qr-init',77,6500]])
                if error:sem.append(['qr-shutdown',QR])
                else:break
            final=qr_errors[-1]
            if final:sem.append(['qr-error',final]);eword(STATE+16,0);result=final
            else:
                eword(STATE+16,QR);eword(STATE+28,0);ehalf(STATE+26,0);sem.extend([['register-public',QR,0x020a3909],['register-natneg',QR,0x020a391d],['register-message',QR,0x020a39b5],['state-change',QR]])
    elif a==0x0209e0fc:
        args=[4,0,END+0x100|1,0x112233,END+0x200|1,0x445566];filter_arg=BUFFER if seed in[2,3]else 0;args[1]=filter_arg;sw(0x021d1b90,OLD if seed in[1,2]else 0);sw(STATE+228,0 if seed in[4,5]else BROWSER);sw(STATE+16,0 if seed==7 else QR);new_browser=0 if seed==5 else BROWSER;sb_error=3 if seed==6 else 0;startup_error=3 if seed==7 else 0
        if seed in[1,2]:sem.append(['free',4,OLD,0]);eword(0x021d1b90,0)
        if filter_arg:
            sem.append(['default-filter',0xffffffff,32,3]);sem.append(['allocate',4,229]);eword(0x021d1b90,0 if seed==3 else ALLOCATED)
            if seed==3:sem.append(['stop',9,-80001])
            else:ew(ALLOCATED,uc.mem_read(BUFFER,229));ebyte(ALLOCATED+228,0)
        if seed!=3:
            sem.append(['set-common',0,4,args[2],args[3]]);eword(STATE+1140,args[4]);eword(STATE+1144,args[5]);sem.append(['set-state',2]);eword(STATE+416,2)
            if seed in[4,5]:sem.append(['new-browser']);eword(STATE+228,new_browser)
            if seed==5:sem.append(['sb-error',5])
            else:
                sem.extend([['gp-status',3,'',0],['sb-update',123456],['sb-error',sb_error]])
                if not sb_error:
                    if seed==7:sem.append(['startup',123456])
                    sem.append(['init-option',0])
    elif a==0x0209e258:
        friendlen=0 if seed==0 else 1 if seed in[1,3,4,5]else 2;distant=0 if seed in[1,3,4,5]else 1;args=[BUFFER,friendlen,num_entry,distant,END+0x100|1,0x112233,END+0x200|1,0x445566];uc.mem_write(BUFFER,bytes([3,7]));sw(STATE+228,0 if seed in[6,10]else BROWSER);new_browser=0 if seed==6 else BROWSER;gp_error=3 if seed==7 else 0;startup_error=3 if seed==8 else 0;reservation_error=1 if seed==9 else 0;sw(STATE+16,0 if seed==8 else QR)
        if seed in[3,4,5]:sw(0x021d1b88,OPTION);uc.mem_write(OPTION,bytes([0 if seed==4 else 1,4 if seed==5 else 2]))
        sem.append(['set-common',1,num_entry,args[4],args[5]]);ebyte(STATE+422,distant);eword(STATE+1140,args[6]);eword(STATE+1144,args[7]);ew(STATE+772,uc.mem_read(BUFFER,friendlen));eword(STATE+836,friendlen)
        if seed in[0,1,4,5]:sem.append(['stop',10,0])
        else:
            sem.append(['set-state',4]);eword(STATE+416,4)
            if seed in[6,10]:sem.append(['new-browser']);eword(STATE+228,new_browser)
            if seed==6:sem.append(['sb-error',5])
            else:
                value='FME=4;MDF='+('Y'if distant else'N')+';VER=3';sem.extend([['format',4],['key-set','FME','4',47],['key-add','MDF','Y'if distant else'N',47],['format',3],['key-add','VER','3',47],['gp-status',4,value,0],['gp-error',gp_error]])
                if not gp_error:
                    if seed==8:sem.append(['startup',123456])
                    if not startup_error:
                        sem.extend([['reservation',0,1,0],['command-error',reservation_error]])
                        if not reservation_error:sem.append(['init-option',0])
    elif a==0x0209e408:
        typ,state,flag=SEND_CASES[seed];args=[0 if typ==-1 else QR];sw(QR+180,flag);sb(STATE+21,typ);sw(STATE+416,state)
        if typ!=-1:
            sem.append(['qr-think',QR])
            if not flag and((typ in[0,1]and state in[1,2,3,4,6,11])or(typ==2 and state==11)):sem.append(['state-change',QR])
    elif a==0x0209ed44:
        if seed==0:sw(0x021d1b8c,0)
        if seed==1:sw(STATE+416,0)
        if seed==2:sb(STATE+425,1)
        index=-1 if seed==3 else 0;accept=0 if seed==4 else 1;count=1 if seed==6 else 0;sb(STATE+13,count);latency=300000 if seed==6 else 128;remote_ip=0xaabbccdd if seed in[7,8]else[0x01020304,0x11223344][count];remote_port=6500 if count==0 else 6600
        if seed==7:uc.mem_write(message,b'\0')
        args=[SOCKET,CONNECTION,remote_ip,remote_port,latency,message,4]
        if seed in[0,1,2]:sem.append(['reject',CONNECTION,'Init state',0xffffffff])
        else:
            sem.append(['connection-index'])
            if index==-1:sem.extend([['reject',CONNECTION,'Server full',0xffffffff],['stop',6,-87100]])
            else:
                if seed==7:sem.append(['reject',CONNECTION,'Unknown connect attempt',0xffffffff])
                else:
                    if seed==8:sem.append(['parse','991',0,10]);eword(STATE+528,remote_ip);ehalf(STATE+656,remote_port)
                    eword(STATE+396,0);eword(STATE+400,0);sem.append(['accept',CONNECTION,CALLBACKS])
                    if not accept:sem.append(['stop',6,-80410])
                    else:
                        sem.extend([['stop-resend'],['connection-slot',index],['connection-info',index],['connection-data',CONNECTION,CONINFO],['postprocess',2]]);eword(CONNSLOT,CONNECTION);ebyte(STATE+13,count+1);ebyte(CONINFO,index);ebyte(CONINFO+1,[3,7][count]);ehalf(CONINFO+2,0);eword(CONINFO+4,0)
                        if count==0:ehalf(STATE+432,min(latency>>1,65535))
    else:
        states=[0,7,7,7,7,7,12,7,7,7];results=[0,5,6,6,2,0,0,6,6,6];sw(STATE+416,states[seed]);sid=results[seed];count=5 if seed==2 else 1;sb(STATE+12,count);index=-1 if seed==5 else 0;gt2_result=1 if seed==8 else 2 if seed==9 else 0;cancel=0 if seed in[4,9]else 1;args=[CONNECTION,sid,message,4]
        if seed not in[0,1]:
            if sid==6:
                ebyte(STATE+12,count+1)
                if seed==2:ebyte(STATE+12,0);sem.append(['cancel',991])
                else:
                    ew(BUFFER+0x400,b'1.2.3.4:6500\0');sem.extend([['format',123456],['address',0x01020304,6500,0],['connect',SOCKET,'1.2.3.4:6500','123456',0xffffffff,5000,CALLBACKS,0]])
                    if seed==8:sem.append(['gt2-error',1])
                    elif seed==9:sem.append(['cancel',991])
            elif sid:sem.append(['cancel',992])
            else:
                sem.append(['connection-index'])
                if index==-1:sem.append(['stop',6,-87100])
                else:sem.extend([['connection-slot',0],['connection-info',0],['connection-data',CONNECTION,CONINFO],['postprocess',0 if seed==6 else 1]]);eword(CONNSLOT,CONNECTION);ebyte(STATE+13,1);ebyte(CONINFO,0);ebyte(CONINFO+1,7);ehalf(CONINFO+2,0);eword(CONINFO+4,0)
    for i,value in enumerate(args):
        if i<4:uc.reg_write(REGS[i],value&0xffffffff)
        else:sw(sp+4*(i-4),value)
    expected=bytearray(uc.mem_read(BASE,0x400000))
    for p,value in expected_writes:expected[p-BASE:p-BASE+len(value)]=value
    def finish(v=0):
        for r,x in zip([*REGS[:4],UC_ARM_REG_R12],[v&0xffffffff,0xa1a1a1a1,0xa2a2a2a2,0xa3a3a3a3,0xacacacac]):uc.reg_write(r,x)
        uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    imports=read_json(LANE/'original-imports.json')['mapping'];names={int(v['address'],0):name for name,v in imports.items()};qcallback=[0x20a37ad,0x20a388d,0x20a3891,0x20a3895,0x20a38fd,0x20a3901]
    def hook(machine,pc,size,user):
        nonlocal returned,qcount
        if pc==END:returned=True;machine.emu_stop();return
        if a<=pc<a+len(body):observed.add(pc);return
        for start,(length,mode)in HELPMODE.items():
            if start<=pc<start+length:
                if bool(machine.reg_read(UC_ARM_REG_CPSR)&0x20)!=(mode=='thumb'):failures.append('Original helper mode differs');machine.emu_stop();return
                if pc==start:helpers[hex(start)]=helpers.get(hex(start),0)+1
                return
        providers[hex(pc)]=providers.get(hex(pc),0)+1;r=[machine.reg_read(x)for x in REGS[:4]];stk=machine.reg_read(UC_ARM_REG_SP);stack=[word(stk+4*i)for i in range(12)];name=names.get(pc,'')
        if pc==0x020b7334:calls.append(['qr-think',r[0]]);finish();return
        if pc==0x020b748c:calls.append(['state-change',r[0]]);finish();return
        if name=='DWC_Free':calls.append(['free',*r[:3]]);finish();return
        if name=='DWCi_GetDefaultMatchFilter':calls.append(['default-filter',r[1],r[2],r[3]]);finish(20);return
        if name=='DWC_Alloc':calls.append(['allocate',r[0],r[1]]);finish(0 if a==0x0209e0fc and seed==3 else ALLOCATED);return
        if pc==0x0209f130:calls.append(['stop',r[0],r[1]if r[1]<0x80000000 else r[1]-0x100000000]);finish();return
        if name=='DWCi_SetMatchCommonParam':calls.append(['set-common',*r]);finish();return
        if pc==0x020a3d7c:calls.append(['set-state',r[0]]);sw(STATE+416,r[0]);finish();return
        if name=='ServerBrowserNew':
            if r!=[GAMENAME,GAMENAME,SECRET,0]or stack[:5]!=[20,1,0,0x020a3239,0]:failures.append('Actual nine-word ServerBrowser interface differs')
            calls.append(['new-browser']);finish(new_browser);return
        if name in['DWCi_HandleSBError','native_fn_020a304c']:calls.append(['sb-error',r[0]]);finish(r[0]);return
        if pc==0x0209d1c8:calls.append(['gp-status',r[0],text(r[1]),r[2]]);finish(gp_error);return
        if name=='DWCi_SBUpdateAsync':calls.append(['sb-update',r[0]]);finish(sb_error);return
        if pc==0x0209dfd8:calls.append(['startup',r[0]]);finish(startup_error);return
        if name=='DWCi_InitOptMinCompParam':calls.append(['init-option',r[0]]);finish();return
        if pc==0x020061ac:
            value=r[3];calls.append(['format',value]);data=str(value).encode()+b'\0'
            if text(r[2])!='%u'or len(data)>r[1]:failures.append('Actual bounded unsigned formatting contract differs')
            machine.mem_write(r[0],data);finish(len(data)-1);return
        if name in['DWC_SetCommonKeyValueString','DWC_AddCommonKeyValueString']:
            key,value=text(r[0]),text(r[1]);add=name.startswith('DWC_Add');calls.append(['key-add'if add else'key-set',key,value,r[3]]);old=text(r[2])+';'if add else'';machine.mem_write(r[2],(old+key+'='+value).encode()+b'\0');finish();return
        if name=='DWCi_HandleGPError':calls.append(['gp-error',r[0]]);finish(r[0]);return
        if name=='DWCi_SendResvCommandToFriend':calls.append(['reservation',*r[:3]]);finish(reservation_error);return
        if name=='DWCi_HandleMatchCommandError':calls.append(['command-error',r[0]]);finish(r[0]);return
        if name=='gt2GetSocketSOCKET':calls.append(['socket',r[0]]);finish(77);return
        if name=='gt2GetLocalPort':calls.append(['port',r[0]]);finish(6500);return
        if name=='qr2_init_socket':
            if r!=[STATE+16,77,6500,GAMENAME]or stack[:10]!=[SECRET,1,1,*qcallback,0]:failures.append('Actual fourteen-word QR2 initializer callback/tag interface differs')
            error=qr_errors[min(qcount,len(qr_errors)-1)];qcount+=1;sw(r[0],QR);calls.append(['qr-init',r[1],r[2]]);finish(error);return
        if name=='qr2_shutdown':calls.append(['qr-shutdown',r[0]]);finish();return
        if name=='DWCi_HandleQR2Error':calls.append(['qr-error',r[0]]);finish(r[0]);return
        if name.startswith('qr2_register_'):
            role={'qr2_register_publicaddress_callback':'public','qr2_register_natneg_callback':'natneg','qr2_register_clientmessage_callback':'message'}[name];calls.append(['register-'+role,r[0],r[1]]);finish();return
        if name=='DWCi_GT2GetConnectionListIdx':calls.append(['connection-index']);finish(index);return
        if name=='gt2Reject':calls.append(['reject',r[0],text(r[1]),r[2]]);finish();return
        if name=='gt2Accept':calls.append(['accept',r[0],r[1]]);finish(accept);return
        if name=='strtoul':calls.append(['parse',text(r[0]),r[1],r[2]]);finish(991);return
        if name=='DWCi_StopResendingMatchCommand':calls.append(['stop-resend']);finish();return
        if name in['DWCi_GetGT2ConnectionByIdx','DWCi_GetConnectionInfoByIdx']:
            calls.append(['connection-slot'if name=='DWCi_GetGT2ConnectionByIdx'else'connection-info',r[0]]);finish(CONNSLOT if name=='DWCi_GetGT2ConnectionByIdx'else CONINFO);return
        if name=='gt2SetConnectionData':calls.append(['connection-data',r[0],r[1]]);finish();return
        if name=='DWCi_PostProcessConnection':calls.append(['postprocess',r[0]]);finish();return
        if name in['DWCi_CancelPreConnectedServerProcess','native_fn_020a16e4']:calls.append(['cancel',r[0]]);finish(cancel);return
        if name=='gt2AddressToString':calls.append(['address',*r[:3]]);machine.mem_write(BUFFER+0x400,b'1.2.3.4:6500\0');finish(BUFFER+0x400);return
        if name=='gt2Connect':calls.append(['connect',r[0],text(r[2]),text(r[3]),*stack[:4]]);finish(gt2_result);return
        if name=='DWCi_HandleGT2Error':calls.append(['gt2-error',r[0]]);finish(r[0]);return
        failures.append('Execution escaped exact Match-control caller/helper/provider set:'+hex(pc)+'/'+name);machine.emu_stop()
    uc.hook_add(UC_HOOK_CODE,hook)
    try:uc.emu_start(a|1,END+4,count=bound)
    except Exception as error:raise ValueError(dict(address=row["address"],case=seed,pc=hex(uc.reg_read(UC_ARM_REG_PC)),cpsr=hex(uc.reg_read(UC_ARM_REG_CPSR)),calls=calls,expectedCalls=sem,failures=failures))from error
    if not returned or(not void and uc.reg_read(UC_ARM_REG_R0)!=(result&0xffffffff))or calls!=sem:failures.append('Independent full Match-control return/provider model differs')
    actual=bytes(uc.mem_read(BASE,0x400000))
    if actual!=expected:failures.append('Full protected Match/QR2/connection/BSS/native memory differs:'+str([hex(BASE+i)for i,(x,y)in enumerate(zip(actual,expected))if x!=y][:16]))
    if returned and(uc.reg_read(UC_ARM_REG_SP)!=sp or[uc.reg_read(r)for r in REGS[4:12]]!=initial[4:12]):failures.append('Complete caller stack/callee-save differs')
    if bytes(uc.mem_read(STACK,0xd000))!=b'\xa5'*0xd000:failures.append('Lower stack guard differs')
    value=dict(actualReturn=returned,modelPassed=not failures,failures=failures,returnWord=None if void else uc.reg_read(UC_ARM_REG_R0),calls=calls,expectedCalls=sem,helperEntries=helpers,suppliedProviderEntries=providers,callerInstructionAddresses=sorted(observed))
    if strict and failures:raise ValueError(dict(address=row['address'],case=seed,**value))
    return value


def execute(rows):
    assert_owned(LANE,SOURCE,WORK)
    if{int(r['address'],0)for r in rows}!=set(COUNTS):raise ValueError('Exact six Match-control identities differ')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text(encoding='utf-8');records=[];specs=[]
    for a,(n,mode)in HELPMODE.items():
        line=next((s for s in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(%s,size=0x%x\) addr:0x%08x'%(mode,n,a),s)),None)
        if line is None:raise ValueError('Actual original Match-control helper mode/extent differs')
        specs.append(dict(address=hex(a),bytes=n,mode=mode,nativeSha256=hashlib.sha256(image[a-BASE:a-BASE+n]).hexdigest(),canonicalInventoryRecord=line,sourceCredit=0))
    for row in rows:
        a=int(row['address'],0);native=image[a-BASE:a-BASE+row['bytes']];body=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(case_count(a)):
            left=run(image,row,native,seed);right=run(image,row,body,seed)
            if left!=right:raise ValueError('Original/C complete Match-control observations differ')
            records.append(dict(address=row['address'],case=seed,topReturned=True,partialProviderStopped=False,actualOriginalHelperInvocations=sum(left['helperEntries'].values()),suppliedServiceCalls=sum(left['suppliedProviderEntries'].values()),original=left,candidate=right))
    first=rows[0];a=int(first['address'],0)
    if run(image,first,image[a-BASE:a-BASE+first['bytes']],0,bound=1,strict=False)['modelPassed']:raise ValueError('Incomplete Match-control prefix admitted')
    result=dict(status='passed',records=records,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),actualQualifiedPureHelpers=specs,nativeAndCompiledReturningCalls=2*len(records),nativeAndCompiledPartialStops=0,actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations']for r in records),suppliedServiceCalls=2*sum(r['suppliedServiceCalls']for r in records),suppliedServiceBodyInstructionsExecuted=0,boundedPrefixRejected=True,helperSourceCodeCredit=0,limits=LIMITS)
    write_json(LANE/'caller-fixtures.json',result);return result
