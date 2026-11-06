import copy
import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_dwc_auth_next_fifth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_fifth_build import build

CLOSE,DISCONNECT,PROGRAM,ERROR,AROUND,STEALTH,USER=0x2095194,0x20951e4,0x20952d0,0x2095324,0x2095494,0x20954dc,0x209557c
HOLD,CTRL,PHASE,STOP,SP=0x2170000,0x2171000,0x2175000,0x27e0000,0x2701000
PROVIDERS={0x20951e4:'thumb',0x2095248:'thumb',0x20990f0:'thumb',0x208a268:'thumb',0x2089b64:'thumb',0x2008e0c:'arm'}
ERROR_CASES=[(0,3,0),(9,4,0),(9,0,0),(10,0,0),(12,0,0),*[(13,0,e) for e in [0,-1,-2,-3,-4,-5,-6,444]]]


def list_state(seed):
    work=bytearray([0xa5])*3352;connect=[0,1,2,3,4,6,7,8,15,0][seed%10];work[3340]=(work[3340]&240)|connect
    settings=[[255,255,255],[0,1,2],[1,1,1],[0,0,0],[1,255,1]][seed%5]
    for i in range(3):
        work[i*256+231]=settings[i]
        for slot in range(2):
            length=[0,1,31,32,4][(seed+i*2+slot)%5];value=bytes(((seed+i+slot+j)%126)+1 for j in range(length));start=i*256+64+slot*32;work[start:start+32]=value+bytes(32-length)
    return bytes(work),connect


def user_model(work):
    result=bytearray(work);connect=work[3340]&15;count=0
    for i in range(3):
        state=work[i*256+231]
        if connect not in [0,i+1] or state==255:continue
        for slot in [0,1] if state==1 else [0]:
            raw=work[i*256+64+slot*32:i*256+96+slot*32];value=raw.split(bytes(1),1)[0]
            if not value:continue
            start=768+count*36;result[start+1]=i+slot*3;result[start+3]=len(value);result[start+4:start+4+len(value)]=value;count+=1
    return bytes(result),count


def error_model(sequence,state,error,payload):
    if sequence<10:return ({3:-51100,4:-51200}.get(state,-51300)-payload)&0xffffffff
    if sequence<13:return (-52000-payload)&0xffffffff
    bases={0:-50000,-1:-52100,-2:-52200,-3:-52300,-4:-53000,-5:-53100,-6:-53200}
    return (bases[error]-payload if error in bases else error)&0xffffffff


def helper_contract(image,inventory):
    canonical=next((s for s in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0xb4\) addr:0x0209557c',s)),None)
    if canonical is None:raise ValueError('Original selected user-list helper full Thumb boundary absent')
    return dict(program='',processor='arm9',module='main',mode='thumb',address=hex(USER),bytes=180,canonicalInventoryRecord=canonical,targetSha256=hashlib.sha256(image[USER-0x2000000:USER-0x2000000+180]).hexdigest(),additionalHelperSourceCredit=0,additionalHelperExtentCredit=0)


def validate_selected_helper(item,image,inventory):
    expected=helper_contract(image,inventory)
    if item!=expected:raise ValueError('Selected original helper namespace/mode/full boundary/hash differs')


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);work,connect=list_state(seed);hold=bytearray([0x61])*36;sequence,state,error=ERROR_CASES[seed%len(ERROR_CASES)];override=0 if seed<len(ERROR_CASES) else 99;payload=[0,1,99,255][seed%4];hold[20]=state;hold[21]=payload;hold[22]=sequence;hold[34]=override;struct.pack_into('<I',hold,16,error&0xffffffff);phase=[0,10,11,12,13,14,15,17,18,255][seed%10];phase_bytes=bytes([phase])+bytes([0x62])*63;memory={HOLD:bytes(hold),CTRL:work,PHASE:phase_bytes};expected_memory=dict(memory)
    for at,data in memory.items():cpu.mem_write(at,data)
    target=None;frame=[];return_value=None
    if a==PROGRAM:
        value=[-1,0,1,2,3,4,-0x80000000,0x7fffffff][seed%8];args=[value&0xffffffff];return_value=({0:-10,1:-9,2:-8,3:-7}.get(value,0))&0xffffffff
    elif a==ERROR:args=[HOLD];return_value=error_model(sequence,state,error,override or payload)
    elif a==CLOSE:
        args=[PHASE]
        if phase<=10:target=0x20951e4
        elif phase==14:target=0x20990f0
        elif phase<18:target=0x2095248
        else:return_value=0
    elif a==DISCONNECT:args=[];target=0x208a268
    elif a in [USER,AROUND,STEALTH]:
        args=[CTRL];expected_memory[CTRL],count=user_model(work);return_value=count
        if a==AROUND and connect in [0,6]:target=0x2008e0c;frame=[0x20dc400,CTRL+768+count*36+4,8];return_value=None
        if a==STEALTH:
            selection=next(((kind,address,length) for kind,address,length in [(4,0x20dea58,8),(7,0x20dc3f8,8),(8,0x20dc408,11)] if connect in [0,kind]),None)
            if selection is not None:target=0x2008e0c;frame=[selection[1],CTRL+768+count*36+4,selection[2]];return_value=None
    else:raise ValueError('Wrong selected AC caller')
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;pcs=[];helper_active=False;helper_invocations=0;helper_returns=0
    def code(machine,at,size,user):
        nonlocal observed,interface,helper_active,helper_invocations,helper_returns
        regs=[machine.reg_read(r) for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if at==STOP:
            observed=dict(kind='return',value=regs[0]);interface=regs[4:12]==initial[4:12] and regs[13]==SP;machine.emu_stop();return
        if at in PROVIDERS and at!=a:
            if thumb!=(PROVIDERS[at]=='thumb'):raise ValueError('Original AC provider ARM/Thumb mode differs')
            observed=dict(kind='provider',address=hex(at));interface=at==target and regs[:len(frame)]==frame;machine.emu_stop();return
        if a in [AROUND,STEALTH] and USER<=at<USER+180:
            if not thumb:raise ValueError('Actual selected user-list helper lost Thumb mode')
            if at==USER:helper_invocations+=1;helper_active=True
            pcs.append(at);return
        if not a<=at<a+len(body) or not thumb:raise ValueError('AC caller escaped actual complete body/helper')
        if helper_active:helper_returns+=1;helper_active=False
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a in [USER,AROUND,STEALTH] and CTRL+768<=at and at+size<=CTRL+1092:return
        raise ValueError('Unexpected original/source AC state mutation')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=50000)
    if observed is None:raise ValueError('AC caller failed bounded completion/provider stop')
    expected=dict(kind='provider',address=hex(target)) if target is not None else dict(kind='return',value=return_value);guards=all(bytes(cpu.mem_read(at,len(data)))==expected_memory[at] for at,data in memory.items());model=observed==expected and interface and guards and helper_invocations==helper_returns
    return dict(address=row['address'],seed=seed,vector=dict(connectType=connect,phase=phase,sequence=sequence,endState=state,errorTest=error,overrideType=override,endType=payload),observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,modelPassed=model,actualOriginalHelperInvocations=helper_invocations,actualOriginalHelperReturns=helper_returns,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();helper=helper_contract(image,inventory);owned=next(r for r in rows if int(r['address'],0)==USER)
    if not owned['realLink']['exactCallerBytes']:raise ValueError('Selected C user-list helper not fully linked exact')
    helper_negatives=[]
    for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('address',hex(USER+2)),('bytes',178),('targetSha256','0'*64)]:
        bad=copy.deepcopy(helper);bad[key]=value
        try:validate_selected_helper(bad,image,inventory)
        except ValueError as error:helper_negatives.append(dict(case=key,rejected=True,reason=str(error)))
        else:raise ValueError('Invalid selected helper metadata admitted')
    records=[];negative=[];variants={CLOSE:('  return 0;','  return 1;'),DISCONNECT:('native_fn_0208a268()','native_fn_02089b64()'),PROGRAM:('= DWC_AC_STATE_ERROR_FATAL;','= DWC_AC_STATE_ERROR_FATAL-1;'),ERROR:('hd->endSequence < 10','hd->endSequence < 9'),AROUND:('MI_CpuCopy8( FREESPOT_SSID, list->ssid, FREESPOT_SSID_LENGTH )','MI_CpuCopy8( FREESPOT_SSID, list->ssid, 7 )'),STEALTH:('MI_CpuCopy8( NINTENDO_USB_SSID, list->ssid, NINTENDO_USB_SSID_LENGTH )','MI_CpuCopy8( NINTENDO_USB_SSID, list->ssid, 7 )'),USER:('i < 3','i < 2')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes();count=26 if a==ERROR else 8 if a in [PROGRAM,DISCONNECT] else 10
        for seed in range(count):
            left=run(image,row,native,seed);right=run(image,row,compiled,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent actual AC return/state/provider model differs',left,right))
            records.append(left)
        folder=WORK/'wrong-c'/f'{a:08x}';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError(('Meaningful whole AC C negative did not mutate',row['address'],before))
        source=folder/'wrong.c';source.write_text(changed);bad,body=build(source,folder/'proof',negative=True);failed=sum(not run(image,row,body,seed)['modelPassed'] for seed in range(count))
        if not failed:raise ValueError('Genuine wrong complete C passed independent AC return/state/provider model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['82paired original/source full entries: complete signed error maps,user-profile search-list construction and no-close/copy-needed guards return with actual R0/callee-saved/SP/RAM checks. Wrapper paths execute selected original canonical180B user-list helper,0additional source/extent credit,then stop before first copy provider where required.','Netcheck abort/destroy,disconnect/cleanup/socket/WCM phases and MI copy provider bodies are not executed; no synthetic returns. Close phase14 abort/destroy calls and missing source operations restored solely from exact original call records. Error switch case-body ordering follows original ordinary compiler layout.','No network/socket/WiFi/flash/device/cache/timer/game/nativeWindows execution or initialized/BSS/static data authorship credit. SSID arrays remain original external storage; macro/source labels derive primary comparison and measured bytes/interfaces.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();result=dict(status='passed',records=records,selectedOriginalHelperQualification=helper,selectedOriginalHelperNegatives=helper_negatives,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),actualOriginalHelperReturns=2*sum(r['actualOriginalHelperReturns'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',result);return result
