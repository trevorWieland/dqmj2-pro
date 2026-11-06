import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261106_dwc_match_next_third_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_third_build import build

REMOTE,PROCESS,INFO=0x209c81c,0x209c940,0x209caa0
GLOBAL,CTRL,USER,REF,ARG,PARAM,STOP,SP,CALLBACK=0x21d1b68,0x2171000,0x2173000,0x2174000,0x2175000,0x2177000,0x27e0000,0x2701000,0x27e0200
FILL,AUTHENTIC,GETERROR,DESTROY,USERNAME,DISCONNECT=0x2008d78,0x209718c,0x2097674,0x2097618,0x2096ffc,0x20aa068
PROVIDERS={FILL:'arm',AUTHENTIC:'thumb',GETERROR:'thumb',DESTROY:'thumb',USERNAME:'thumb',DISCONNECT:'thumb'}


def vector(seed):
    return dict(state=[0,1,2,3,4,5,7][seed%7],result=seed%5,profile=[0,1,-1,0x7fffffff][seed%4],lastByte=[0,65,128,255][seed%4],gamecode=(0x12340000+seed)&0xffffffff)


def run(image,row,body,v,seed,fragment=False):
    a=int(row['address'],0)
    if fragment and a!=REMOTE:raise ValueError('Only original remote post-clear block may have an internal entry')
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    context=bytearray([0x75])*640;struct.pack_into('<I',context,4,v['state']);struct.pack_into('<I',context,12,v['gamecode']);struct.pack_into('<I',context,0x1c,USER)
    userdata=bytes([0x7b])*64;argument=bytearray((seed+i)&255 for i in range(516));struct.pack_into('<Ii',argument,0,v['result'],v['profile']);argument[142]=v['lastByte']
    global_words=[PARAM+4,CTRL,CALLBACK+5];memory={GLOBAL:struct.pack('<III',*global_words),CTRL:bytes(context),USER:userdata,ARG:bytes(argument),REF:struct.pack('<I',PARAM+8)};expected_memory=dict(memory)
    for at,data in memory.items():cpu.mem_write(at,data)
    expected=dict(kind='return');frame=None
    if a==REMOTE:
        args=[CALLBACK|1,PARAM]
        if fragment:expected=dict(kind='provider',address=hex(AUTHENTIC));frame=[USER];expected_memory[GLOBAL]=struct.pack('<III',PARAM,CTRL,CALLBACK|1)
        else:expected=dict(kind='provider',address=hex(FILL));frame=[SP-88,0,72]
    elif a==PROCESS:args=[];expected=dict(kind='provider',address=hex(GETERROR))
    else:
        args=[REF,ARG,PARAM+4]
        if v['result']==0 and v['state'] in [3,4]:
            if v['state']==3 and v['lastByte']!=0:expected=dict(kind='provider',address=hex(DISCONNECT));frame=[REF]
            else:expected=dict(kind='provider',address=hex(USERNAME));frame=[USER+4,v['gamecode'],SP-38 if v['state']==3 else SP-59]
    initial=[(0x63c00000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP-88 if fragment else SP,STOP|1]
    for i,arg in enumerate(args):initial[i]=arg&0xffffffff
    if fragment:initial[4]=PARAM;initial[5]=CALLBACK|1
    cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[];interface=True
    def code(machine,at,size,user):
        nonlocal observed,interface
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if at==STOP:
            if fragment:raise ValueError('Internal remote block unexpectedly returned')
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual GP callback return ABI differs')
            observed=dict(kind='return');machine.emu_stop();return
        if at in PROVIDERS:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual auth provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=frame is None or regs[:len(frame)]==frame;machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Auth caller escaped bounded genuine body/mode')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if GLOBAL<=at and at+size<=GLOBAL+12:return
        raise ValueError('Unexpected auth caller write outside scoped RAM/stack')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start((a+18 if fragment else a)|1,STOP+4,count=20000)
    if observed is None:raise ValueError('Auth caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in expected_memory.items())
    return dict(address=row['address'],seed=seed,vector=v,entryKind='internal-after-unexecuted-clear' if fragment else 'function',actualFunctionEntry=not fragment,observed=observed,expected=expected,topReturned=observed['kind']=='return' and not fragment,partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,actualOriginalHelperInvocations=0,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[];fragments=[];negative=[]
    original=image[REMOTE-0x2000000:REMOTE-0x2000000+292]
    if original[4:8].hex()!='051c0c1c' or original[20:24].hex()!='85600460':raise ValueError('Original prologue role/global8/global0 stores differ')
    variants={REMOTE:('sizeof(auth)','(sizeof(auth)+4)'),PROCESS:('DWC_Auth_GetError()','(DWC_Auth_Destroy(),DWC_Auth_GetError())'),INFO:('&stpLoginCnt->userdata->pseudo','&stpLoginCnt->userdata->authentic')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,linked,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent auth/GP provider model differs',left,right))
            records.append(left)
            if a==REMOTE:
                left=run(image,row,native,v,seed,True);right=run(image,row,linked,v,seed,True)
                if left!=right or not left['modelPassed']:raise ValueError(('Actual internal remote slot store model differs',left,right))
                fragments.append(left)
        folder=WORK/'fixtures'/format(a,'08x')/'wrong-C';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        wrong=folder/'match.c';text=(ROOT/row['source']).read_text();old,new=variants[a];changed=text.replace(old,new,1)
        if changed==text:raise ValueError('Whole auth wrong-C did not mutate')
        wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True);failures=[]
        for seed in range(16):
            v=vector(seed);v.update(result=0,state=3,lastByte=0);r=run(image,row,body,v,seed)
            if r['modelPassed']:raise ValueError('Whole auth wrong-C accepted independent provider model')
            failures.append(r)
        negative.append(dict(address=row['address'],sourceSha256=sha256(wrong),compiledBytes=bad['compiledBytes'],genuineLink=bad['realLink'],records=failures))
    row=next(r for r in rows if int(r['address'],0)==REMOTE);folder=WORK/'fixtures/wrong-global-order';folder.mkdir(parents=True,exist_ok=True)
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    header=folder/'context.h';text=header.read_text();correct='typedef struct{void*remoteParam;DWCLoginControl*control;DWCRemoteAuthCallback remoteCallback;}DWCLoginGlobals;';wrong='typedef struct{DWCRemoteAuthCallback remoteCallback;DWCLoginControl*control;void*remoteParam;}DWCLoginGlobals;'
    if correct not in text:raise ValueError('Correct new remote global slot declaration absent')
    header.write_text(text.replace(correct,wrong));source=folder/'match.c';shutil.copyfile(ROOT/row['source'],source);bad,body=build(source,folder/'genuine-link',negative=True);wrong_fragments=[]
    for seed in range(16):
        r=run(image,row,body,vector(seed),seed,True)
        if r['modelPassed']:raise ValueError('Wrong remote global slot order accepted actual internal-store model')
        wrong_fragments.append(r)
    limits=['Three complete ordinary C auth/GP callers908B genuinely link every original native extent/branch/data/Thumb-tagged callback, measured inline SDK64-bit LCG and scoped_ll_udiv/_ull_mul helpers. AuthParam72/callbacks64/68, opaque allocated Http7188 at explicit alignment4, auth result452 and GP info516/lastname142/selector1797 compiler-qualified.0external storage extent/authorship credit.','384paired actual full function entries independently model72-byte clear frame, auth polling first provider, GP-info result/state returns and user-pseudo/gamecode/local21-byte buffer or disconnect provider frames.0callee/provider/callback/time/random/heap/network body execution and0synthetic returns; full ordinary C remains byte/link evidence for later paths.','Separately128paired internal starts at0209c82e after the UNEXECUTED clear call, with original prologue-established R5callback/R4parameter/SP-88, prove actual slot8callback/slot0parameter stores and preserved control4 before account-auth provider. These256internal starts are NOTfunction entries/returns, helper executions or proof of prefix/clear reachability. Three whole genuinely linked wrong-C variants reject48independent models; a genuinely linked wrong global-slot layout rejects16internal models; wrong layouts/prototypes/native bindings qualify separately.0device/game/nativeWindows execution.']
    trace=hashlib.sha256(json.dumps(dict(functionEntries=records,internalBlocks=fragments),sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,separateInternalBlockRecords=fragments,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=len(negative),wrongC=negative,wrongGlobalLayoutGenuineLink=bad['realLink'],wrongGlobalLayoutInternalModels=wrong_fragments,actualSeparateNativeAndSourceInternalStarts=2*len(fragments),actualSeparateInternalTopReturns=0,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
