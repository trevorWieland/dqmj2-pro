import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_second_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_second_build import build
from wave20261106_dwc_match_next_second_error_helper import execute as qualify_error

INIT,ASYNC,PROCESS,STOPLOGIN,ERRORMAP,CONNECTED=0x209c4f0,0x209c538,0x209c55c,0x209c610,0x209c690,0x209c6e4
GLOBAL,ERROR,ERRWORD=0x21d1b68,0x209a9e4,0x21d19ac
CTRL,USER,REF,ARG,NAME,PARAM,STOP,SP,CALLBACK=0x2171000,0x2173000,0x2174000,0x2175000,0x2176000,0x2177000,0x27e0000,0x2701000,0x27e0200
FILL,REMOTE,REMOTE_PROCESS,GPPROCESS,TICK,SETERROR,STATUS,GETINFO=0x2008d78,0x209c81c,0x209c940,0x20a9f60,0x2007a9c,0x209a9f8,0x209d1c8,0x20aa100
PROVIDERS={FILL:'arm',REMOTE:'thumb',REMOTE_PROCESS:'thumb',GPPROCESS:'thumb',TICK:'arm',SETERROR:'thumb',STATUS:'thumb',GETINFO:'thumb',STOPLOGIN:'thumb',ERRORMAP:'thumb'}


def vector(seed):
    return dict(present=seed%4!=0,error=[0,0,1,0xffffffff][seed%4],state=[0,1,2,3,4,5,7][seed%7],argError=[0,1,6,9][seed%4],code=[-61001,-60000,-2147483648,2147483647][seed%4],result=seed%5,profile=[0,1,-1,0x7fffffff][seed%4],sameProfile=seed%2!=0,gpPointer=seed%3!=0,gpValue=seed%4!=0,connectFlag=seed%2)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    present=v['present'] if a in [PROCESS,STOPLOGIN] else True
    context=bytearray([0x71])*640
    for off,value in [(0,REF if v['gpPointer'] else 0),(4,v['state']),(0x14,CALLBACK|1),(0x18,PARAM),(0x1c,USER),(0x30,v['connectFlag'])]:struct.pack_into('<I',context,off,value&0xffffffff)
    userdata=bytearray([0x6a])*64;struct.pack_into('<I',userdata,0x1c,(v['profile'] if v['sameProfile'] else v['profile']^1)&0xffffffff)
    argument=bytearray((seed+i)&255 for i in range(32));struct.pack_into('<Ii',argument,0,v['result'],v['profile'])
    globals=struct.pack('<III',CALLBACK|1,CTRL if present else 0,PARAM+4)
    memory={GLOBAL:globals,ERRWORD:struct.pack('<I',v['error']&0xffffffff),CTRL:bytes(context),USER:bytes(userdata),ARG:bytes(argument),REF:struct.pack('<I',PARAM+8 if v['gpValue'] else 0),NAME:bytes([65,0])*26};expected_memory=dict(memory)
    for at,data in memory.items():cpu.mem_write(at,data)
    changed=bytearray(context);expected=dict(kind='return');frame=None;stack_frame=None;helpers=0
    if a==INIT:
        args=[CTRL,USER,REF,seed+1000,0x12340000+seed,NAME,CALLBACK|1,PARAM];expected_memory[GLOBAL]=struct.pack('<III',CALLBACK|1,CTRL,PARAM+4);expected=dict(kind='provider',address=hex(FILL));frame=[CTRL,0,640]
    elif a==ASYNC:args=[];expected=dict(kind='provider',address=hex(REMOTE));frame=[0x209c7a1,0]
    elif a==PROCESS:
        args=[];helpers=int(present)
        if present and not v['error']:
            if v['state']==1:expected=dict(kind='provider',address=hex(REMOTE_PROCESS))
            elif v['state'] in [2,3,4]:
                if v['gpPointer'] and v['gpValue']:expected=dict(kind='provider',address=hex(GPPROCESS));frame=[REF]
                elif v['connectFlag']:expected=dict(kind='provider',address=hex(TICK))
    elif a==STOPLOGIN:
        args=[v['argError'],v['code']]
        if present and v['argError']!=0:expected=dict(kind='provider',address=hex(SETERROR));frame=[v['argError'],v['code']&0xffffffff]
    elif a==ERRORMAP:
        args=[v['result']]
        if v['result']==0:expected=dict(kind='return',value=0)
        else:expected=dict(kind='provider',address=hex(STOPLOGIN));frame=[9 if v['result'] in [1,2] else 6,(-61000-{1:1,2:2,3:10,4:20}[v['result']])&0xffffffff]
    else:
        args=[REF,ARG,PARAM+4];struct.pack_into('<I',changed,0x30,0)
        if v['result']!=0:expected=dict(kind='provider',address=hex(ERRORMAP));frame=[v['result']]
        else:
            changed[0x260:0x280]=argument
            if v['state']==2:
                if v['sameProfile']:struct.pack_into('<I',changed,4,5);expected=dict(kind='provider',address=hex(STATUS));frame=[1,0x20e017c,0]
                else:expected=dict(kind='provider',address=hex(STOPLOGIN));frame=[6,(-60000)&0xffffffff]
            elif v['state']==3:expected=dict(kind='provider',address=hex(GETINFO));frame=[REF,v['profile']&0xffffffff,0,0];stack_frame=[0x209caa1,0]
    expected_memory[CTRL]=bytes(changed);initial=[(0x62b00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP|1]
    for i,arg in enumerate(args[:4]):initial[i]=arg&0xffffffff
    for i,arg in enumerate(args[4:]):cpu.mem_write(SP+i*4,struct.pack('<I',arg&0xffffffff))
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True;helper_count=0;helper_return=None;helper_saved=None;checked=0
    def code(machine,at,size,user):
        nonlocal observed,interface,helper_count,helper_return,helper_saved,checked
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[0]!=int(v['error']!=0) or regs[4:12]!=helper_saved[0] or regs[13]!=helper_saved[1]:raise ValueError('Actual original error helper predicate/ABI differs')
            checked+=1;helper_return=None
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual login caller return ABI differs')
            observed=dict(kind='return',value=regs[0]) if a==ERRORMAP else dict(kind='return');machine.emu_stop();return
        if at==ERROR:helper_count+=1;helper_return=regs[14]&~1;helper_saved=(regs[4:12],regs[13])
        if ERROR<=at<ERROR+16:
            if not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Actual original error helper mode differs')
            return
        if at in PROVIDERS and at!=a:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual login provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame
            if stack_frame is not None:interface=interface and list(struct.unpack('<II',bytes(machine.mem_read(regs[13],8))))==stack_frame
            machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Login caller escaped bounded genuine body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if CTRL<=at and at+size<=CTRL+len(context):return
        if GLOBAL<=at and at+size<=GLOBAL+12:return
        raise ValueError('Unexpected login caller write outside scoped RAM/stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000)
    if observed is None:raise ValueError('Login caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items());helper_model=helper_count==checked==helpers
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and interface and guards and helper_model,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=helper_count,originalHelperBooleanAndAbiPassed=helper_model,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);helper=qualify_error();image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];negative=[]
    variants={INIT:('sizeof(DWCLoginControl)','(sizeof(DWCLoginControl)+4)'),ASYNC:('DWCi_RemoteAuthCallback, NULL','DWCi_RemoteAuthCallback, (void*)4'),PROCESS:('!stpLoginCnt ||','stpLoginCnt ||'),STOPLOGIN:('error == DWC_ERROR_NONE','error != DWC_ERROR_NONE'),ERRORMAP:('errorCode = DWC_ECODE_TYPE_ALLOC;','errorCode = (DWC_ECODE_TYPE_ALLOC-1);'),CONNECTED:('connectFlag = FALSE','connectFlag = TRUE')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);original=run(image,row,native,v,seed);source=run(image,row,linked,v,seed)
            if original!=source or not original['modelPassed']:raise ValueError(('Independent login state/copy/error/provider model differs',original,source))
            records.append(original)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole login wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True);failures=[]
        for seed in range(16):
            v=vector(seed);v.update(present=True,error=0,state=1,argError=1,result=1,connectFlag=1);result=run(image,row,body,v,seed)
            if result['modelPassed']:raise ValueError(('Whole login wrong-C accepted independent model',row['address'],result))
            failures.append(result)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    limits=['Six complete ordinary C login/control callers588B genuinely link all original native extents/relocations/ARM-Thumb targets and original callback literals0209c7a1/0209caa1.640-byte login control,64-byte account data,32-byte GP response,12-byte external global callback/control/parameter group and all used field widths/offsets are actual compiler-qualified;0external storage extent/authorship credit.','768paired actual entries independently model null/error/state returns,640-byte clear and remote callback provider frames, login process state/provider selection, error-code translation and GP callback32-byte response copies/connectFlag reset/profile/state mutations before actual provider transfers. Only canonical original20-byte error predicate executes as a callee;32 standalone original helper entries and12 negatives qualify it separately.0synthetic returns.','Memory clear/authentication/remote/GP processing/status/error/state/callback/time/division/Internet/provider bodies and following paths remain unexecuted; provider instructions execute0. Thus timeout conversion is full native-link evidence only, without elapsed-time or network behavior execution.6whole genuinely linked wrong-C variants reject96independent models; wrong layouts and unchanged original binding negatives qualify separately.0network/device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),standaloneOriginalErrorHelperEntries=helper['standaloneOriginalEntries'],wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
