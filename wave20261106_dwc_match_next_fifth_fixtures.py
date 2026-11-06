import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_dwc_match_next_fifth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_fifth_build import build
from wave20261106_dwc_match_next_fifth_login_helper import execute as qualify_login

UPDATE,TICK,END,DELETE,STATUS=0x209cfe4,0x209d294,0x209d4c0,0x209d4e0,0x209d690
GLOBAL,LOGIN_GLOBAL,HELPER=0x21d1b74,0x21d1b68,0x209cba8
CTRL,LOGINCTRL,FRIEND,REF,OUTPUT,STOP,CALLBACK,SP=0x2171000,0x2172000,0x2173000,0x2174000,0x2178000,0x27e0000,0x27e1000,0x2701000
PROVIDERS={0x2007a9c:'arm',0x2008d78:'arm',0x209c5fc:'thumb',CALLBACK:'thumb'}


def vector(seed):
    return dict(present=seed%4!=0,loginPresent=seed%3!=0,loginState=[0,1,4,5,6,7,0xffffffff][seed%7],friendListPresent=seed%2!=0,index=seed%4,changed=[0,1,2,255][seed%4])


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x2000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    context=bytearray([0x61])*92;struct.pack_into('<I',context,4,REF);struct.pack_into('<I',context,24,FRIEND if v['friendListPresent'] else 0);context[29]=v['changed'];struct.pack_into('<II',context,44,CALLBACK|1,0x11224488);login=bytearray([0x62])*640;struct.pack_into('<I',login,4,v['loginState']);memory={GLOBAL:struct.pack('<IIII',0x33445566,0x44556677,0x55667788,CTRL if v['present'] or a in [UPDATE,TICK,END] else 0),LOGIN_GLOBAL:struct.pack('<III',0x66778899,LOGINCTRL if v['loginPresent'] else 0,0x778899aa),CTRL:bytes(context),LOGINCTRL:bytes(login),FRIEND:bytes([0x63])*48,REF:struct.pack('<I',0x2179000),OUTPUT:bytes([0x94])*532}
    for at,data in memory.items():cpu.mem_write(at,data)
    expected_memory=dict(memory);helpers=0;private=True
    if a==UPDATE:
        args=[0x12345678,0x23456789,0x34567891,0x45678912,0x56789123,0x67891234,0x78912345,0x89123456];updated=bytearray(context);struct.pack_into('<IIIIII',updated,44,*args[2:]);updated[28:32]=bytes([0,0,0,1 if v['friendListPresent'] else 2]);struct.pack_into('<I',updated,0,1);expected_memory[CTRL]=bytes(updated);expected=dict(kind='return');frame=None
    elif a==TICK:args=[];expected=dict(kind='provider',address=hex(0x2007a9c));frame=[]
    elif a==END:args=[];expected=dict(kind='provider',address=hex(CALLBACK));frame=[0,v['changed'],0x11224488]
    elif a==DELETE:
        args=[FRIEND,v['index'],3];expected=dict(kind='provider',address=hex(0x2008d78)) if v['present'] else dict(kind='return');frame=[FRIEND+12*v['index'],0,12] if v['present'] else None
    else:
        args=[FRIEND,OUTPUT];helpers=int(v['present']);expected=dict(kind='provider',address=hex(0x209c5fc)) if v['present'] and v['loginPresent'] and v['loginState']==5 else dict(kind='return',value=0);frame=[]
    initial=[(0x64d00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args[:4]):initial[i]=arg&0xffffffff
    for i,arg in enumerate(args[4:]):cpu.mem_write(SP+i*4,struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;count=0;checked=0;helper_return=None;helper_saved=None
    def code(machine,at,size,user):
        nonlocal observed,interface,count,checked,helper_return,helper_saved,private
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[0]!=int(v['loginPresent'] and v['loginState']==5) or regs[4:12]!=helper_saved[0] or regs[13]!=helper_saved[1]:raise ValueError('Actual login leaf ABI/predicate differs')
            checked+=1;helper_return=None
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual friend caller return ABI differs')
            observed=dict(kind='return')
            if a==STATUS:observed['value']=regs[0]
            machine.emu_stop();return
        if at==HELPER:count+=1;helper_return=regs[14]&~1;helper_saved=(regs[4:12],regs[13])
        if HELPER<=at<HELPER+22:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual login leaf mode differs')
            return
        if at in PROVIDERS:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame
            if a==TICK:private=regs[4]==0 and regs[5]==CTRL
            machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Caller escaped genuine bounded body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==UPDATE and CTRL<=at and at+size<=CTRL+92:return
        raise ValueError('Unexpected caller RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items());helper_model=count==checked==helpers
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface and helper_model and private,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,preTickAccumulatorAndControlPassed=private,actualOriginalHelperInvocations=count,originalHelperBooleanAndAbiPassed=helper_model,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);helper=qualify_login();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={UPDATE:('state = DWC_FRIEND_STATE_PERS_LOGIN','state = DWC_FRIEND_STATE_LOGON'),TICK:('result = GP_NO_ERROR','result = 1'),END:('DWC_ERROR_NONE,','1,'),DELETE:('sizeof(DWCFriendData)','sizeof(DWCFriendData)-1'),STATUS:('if (!stpFriendCnt || !DWCi_CheckLogin()) return FALSE;','if (!stpFriendCnt || !DWCi_CheckLogin()) return TRUE;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,compiled,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent caller/model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c'/f'{a:08x}';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if text==changed:raise ValueError('Meaningful whole-C negative did not mutate')
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,vector(seed),seed)['modelPassed'] for seed in range(16))
        if not failed:raise ValueError(('Wrong C did not reject independent observable model',row['address']))
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['128 paired actual original/source entries per caller. Complete update-state writes and null/login-state returns; exact provider frames and no-write guards. Only original28-byte CheckLogin helper executes as a callee.0synthetic provider returns.','GPProcess stops before first original OS_GetTick instruction; only prologue, captured control pointer and zero-initialized R4 result accumulator are executed/checked.0GPProcess returns, tick/time/counter/GP behavior execution.','EndUpdateServers stops before callback entry; its later state transition is byte/link validated but unexecuted. Delete stops before clear provider; later callback unexecuted. Buddy status stops before userdata provider on successful login.0storage extent/authorship/callee source credit.','No network/device/hardware/game/nativeWindows execution. All five whole genuinely linked wrong-C variants reject independent observed model states.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),standaloneOriginalLoginHelperEntries=helper['standaloneOriginalEntries'],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
