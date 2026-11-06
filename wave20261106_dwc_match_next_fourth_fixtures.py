import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_fourth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_fourth_build import build
from wave20261106_dwc_match_next_fourth_login_helper import execute as qualify_login

STATUS,DATA,SETDATA,DELETE=0x209cbd4,0x209cc98,0x209ccf4,0x209cd4c
HELPER,LOGIN_GLOBAL,GLOBAL=0x209cba8,0x21d1b68,0x21d1b74
CTRL,LOGINCTRL,FRIEND,REF,TEXT,MAX,NUM,SIZE,OUTPUT,STOP,SP=0x2171000,0x2172000,0x2173000,0x2174000,0x2176000,0x2177000,0x2177010,0x2177020,0x2178000,0x27e0000,0x2701000
GETSTATUS,ENCODE,FILL,GETUSER=0x209d690,0x209a738,0x2008d78,0x209c5fc
PROVIDERS={GETSTATUS:'thumb',STATUS:'thumb',ENCODE:'thumb',FILL:'arm',GETUSER:'thumb'}


def vector(seed):
    return dict(friendPresent=seed%4!=0,loginPresent=seed%3!=0,loginState=[0,1,4,5,6,7,0xffffffff][seed%7],size=[0,1,255,0xffffffff][seed%4],maxPresent=seed%2!=0,numPresent=seed%3!=0,outputPresent=seed%4!=0)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    context=bytearray([0x61])*96;struct.pack_into('<I',context,4,REF);login=bytearray([0x62])*640;struct.pack_into('<I',login,4,v['loginState']);memory={GLOBAL:struct.pack('<IIII',0x11223344,0x22334455,0x33445566,CTRL if v['friendPresent'] else 0),LOGIN_GLOBAL:struct.pack('<III',0x44556677,LOGINCTRL if v['loginPresent'] else 0,0x55667788),CTRL:bytes(context),LOGINCTRL:bytes(login),FRIEND:bytes([0x63])*12,REF:struct.pack('<I',TEXT),TEXT:b'status-payload\0',MAX:b'\x91',NUM:b'\x92',SIZE:struct.pack('<I',0x93748121),OUTPUT:bytes([0x94])*256}
    for at,data in memory.items():cpu.mem_write(at,data)
    maximum=MAX if v['maxPresent'] else 0;number=NUM if v['numPresent'] else 0;output=OUTPUT if v['outputPresent'] else 0;expected=dict(kind='provider');helpers=0
    if a==STATUS:args=[FRIEND,maximum,number,output];expected['address']=hex(GETSTATUS);frame=[FRIEND,SP-548]
    elif a==DATA:args=[FRIEND,maximum,number,output,SIZE];expected['address']=hex(STATUS);frame=[FRIEND,maximum,number,SP-272]
    elif a==SETDATA:
        args=[TEXT,v['size']];helpers=int(v['friendPresent'])
        if v['friendPresent'] and v['loginPresent'] and v['loginState']==5:expected['address']=hex(ENCODE);frame=[TEXT,v['size'],SP-272,255]
        else:expected=dict(kind='return',value=0);frame=None
    else:
        args=[FRIEND];helpers=int(v['friendPresent'])
        if v['friendPresent'] and v['loginPresent'] and v['loginState']==5:expected['address']=hex(GETUSER);frame=None
        else:expected['address']=hex(FILL);frame=[FRIEND,0,12]
    initial=[(0x64d00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args[:4]):initial[i]=arg&0xffffffff
    for i,arg in enumerate(args[4:]):cpu.mem_write(SP+i*4,struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;count=0;checked=0;helper_return=None;helper_saved=None
    def code(machine,at,size,user):
        nonlocal observed,interface,count,checked,helper_return,helper_saved
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[0]!=int(v['loginPresent'] and v['loginState']==5) or regs[4:12]!=helper_saved[0] or regs[13]!=helper_saved[1]:raise ValueError('Actual login leaf predicate/ABI differs in friend caller')
            checked+=1;helper_return=None
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual friend caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at==HELPER:count+=1;helper_return=regs[14]&~1;helper_saved=(regs[4:12],regs[13])
        if HELPER<=at<HELPER+22:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual login leaf mode differs')
            return
        if at in PROVIDERS and at!=a:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual friend provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame;machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Friend caller escaped bounded genuine body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        raise ValueError('Unexpected friend caller RAM write before provider')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Friend caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items());helper_model=count==checked==helpers
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface and helper_model,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=count,originalHelperBooleanAndAbiPassed=helper_model,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);helper=qualify_login();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={STATUS:('DWCi_GetFriendBuddyStatus(friendData, &status)','DWCi_GetFriendBuddyStatus(friendData, (GPBuddyStatus*)0)'),DATA:('DWC_GetFriendStatusSC(friendData, maxEntry, numEntry, statusString)','DWC_GetFriendStatusSC(friendData, numEntry, maxEntry, statusString)'),SETDATA:('DWC_GS_STATUS_STRING_LEN - 1','DWC_GS_STATUS_STRING_LEN - 2'),DELETE:('sizeof(DWCFriendData)','(sizeof(DWCFriendData)+4)')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,linked,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent friend status/null/login/provider model differs',left,right))
            records.append(left)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole friend wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True);failures=[]
        for seed in range(16):
            v=vector(seed);v.update(friendPresent=a!=DELETE,loginPresent=True,loginState=5,maxPresent=True,numPresent=True,outputPresent=True);r=run(image,row,body,v,seed)
            if r['modelPassed']:raise ValueError('Whole friend wrong-C accepted independent provider model')
            failures.append(r)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    coverage={hex(target):sum(r['observed']==dict(kind='provider',address=hex(target)) for r in records) for target in [GETSTATUS,STATUS,ENCODE,FILL,GETUSER]}
    if not all(coverage.values()) or not any(r['topReturned'] for r in records):raise ValueError('Friend vectors omitted a required return/provider branch')
    limits=['Four complete ordinary C status/data/friend callers456B genuinely link exact original full extents/relocations and actualARMstdlib imports. Native GPBuddyStatus532/quietModeFlags528 is grounded in frozen genuine writer020aa3e0 and original DWC helper0209d6ee call to it; public SDK528 lacks that tail. The measured type fixes original stack allocation without a compiler allocation search.12B friend data and only used friend-control pointer+12/pGpObj4 are qualified; other control/global fields remain prefix/comparison evidence and0storage credit.','512paired actual entries independently cover nullable max/num/output forwarding, actual local532B status/256B data buffer provider frames, complete null/login-state returns, encode capacity255 and invalidation12B clear/provider selection. Only original canonical28-byte CheckLogin leaf executes as a callee;64 standalone native entries/13negative contracts qualify it separately.0synthetic returns.','All buddy status/query/string/conversion/base64/clear/userdata/GP provider bodies and later paths remain unexecuted; provider instructions execute0.4whole genuinely linked wrong-C variants reject64independent argument/buffer/size models; actual wrong typed layouts/prototypes/original binding negatives qualify separately.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,requiredProviderBranchCoverage=coverage,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),standaloneOriginalLoginHelperEntries=helper['standaloneOriginalEntries'],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
