import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json
from wave20261106_dwc_match_next_eighth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_match_next_eighth_build import build
from wave20261106_dwc_match_next_eighth_helpers import EXPECTED,validate,TYPE,MASK,WORD,STRLEN

MESSAGE,REFRESH,FRIEND_GLOBAL,CORE_GLOBAL,CTRL,FRIEND,ARG,REF,TEXT,STOP,SP=0x209c188,0x209d514,0x21d1b74,0x21d19e0,0x2171000,0x2173000,0x2175000,0x2176000,0x2177000,0x27e0000,0x2701000
PROVIDERS={0x201b248:'arm',0x209d134:'thumb'}


def vector(seed):return dict(type=seed%4,index=(seed//4)%4,messageOffset=seed%4,profile=42,parameter=0x12348899)


def run(image,row,body,v,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);friends=bytearray([0x63])*60
    for i in range(5):struct.pack_into('<I',friends,12*i,(0x76543210&~(3<<11))|(((i+v['type']-v['index'])%4)<<11))
    message=TEXT+v['messageOffset'];memory={FRIEND_GLOBAL:struct.pack('<IIII',0x11223344,0x22334455,0x33445566,CTRL),CORE_GLOBAL:struct.pack('<I',CTRL),CTRL:bytes([0x61])*2048,FRIEND:bytes(friends),ARG:struct.pack('<III',v['profile'],0x11223344,message),REF:bytes([0x62])*16,message:b'GPCM3vMATpayload\0'}
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==MESSAGE:args=[REF,ARG,v['parameter']];expected=dict(kind='provider',address=hex(0x201b248));frame=[message,0x20e0170,4];expected_counts={TYPE:0,MASK:0,WORD:0,STRLEN:1}
    else:
        args=[FRIEND,v['index'],v['profile']];expected=dict(kind='return',value=0) if v['type']==1 or v['index']==0 else dict(kind='provider',address=hex(0x209d134));frame=[0] if expected['kind']=='provider' else None;expected_counts={TYPE:1,MASK:1,WORD:1,STRLEN:0}
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;pcs=[];counts={k:0 for k in EXPECTED};checked=0;helper_return=None;saved=None;helper_kind=None
    def code(machine,at,size,user):
        nonlocal observed,interface,checked,helper_return,saved,helper_kind
        regs=[machine.reg_read(r) for r in C.REGISTERS]
        if helper_return is not None and at==helper_return:
            if regs[4:12]!=saved[0] or regs[13]!=saved[1]:raise ValueError('Actual original helper return ABI differs')
            interface=interface and regs[0]==(v['type'] if helper_kind==TYPE else 4);checked+=1;helper_return=None
        if at in EXPECTED:
            counts[at]+=1
            if at in [TYPE,STRLEN]:helper_kind=at;helper_return=regs[14]&~1;saved=(regs[4:12],regs[13]);interface=interface and regs[0]==(FRIEND+12*v['index'] if at==TYPE else 0x20e0170)
        for start,(mode,hexadecimal) in EXPECTED.items():
            if start<=at<start+len(bytes.fromhex(hexadecimal)):
                if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(mode=='thumb'):raise ValueError('Actual original helper mode differs')
                return
        if at==STOP:
            if regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual bounded caller return ABI differs')
            observed=dict(kind='return',value=regs[0]);machine.emu_stop();return
        if at in PROVIDERS:
            if bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)!=(PROVIDERS[at]=='thumb'):raise ValueError('Actual provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=interface and (frame is None or regs[:len(frame)]==frame);machine.emu_stop();return
        if not a<=at<a+len(body) or not machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Caller escaped genuine bounded helpers/body')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        raise ValueError('Unexpected caller/helper RAM write before provider')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=10000)
    if observed is None:raise ValueError('Caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==data for at,data in memory.items());initialized=a!=MESSAGE or bytes(cpu.mem_read(SP-32,12))==bytes(12);helper_ok=counts==expected_counts and checked==1
    return dict(address=row['address'],seed=seed,vector=v,observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',modelPassed=observed==expected and guards and interface and helper_ok and initialized,providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,versionBuffer12ByteInitializationPassed=initialized,actualOriginalHelperInvocations=sum(counts.values()),actualOriginalTypeVeneerInvocations=counts[TYPE],actualOriginalTypeLogicHelperInvocations=counts[MASK]+counts[WORD],actualOriginalStrlenHelperInvocations=counts[STRLEN],actualTopHelpersReturnedAndAbiPassed=helper_ok,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();validate(read_json(LANE/'helpers.json'),image,(ROOT/'config/arm9/symbols.txt').read_text(),(ROOT/'config/arm9/relocs.txt').read_text());proof=read_json(LANE/'helpers-proof.json')
    if proof['root']!=str(ROOT) or proof['status']!='passed' or proof['standaloneOriginalEntries']!=128:raise ValueError('Fresh original helper qualification absent')
    records=[];negative=[];variants={MESSAGE:('char * message = arg->message;','char * message = arg->message + 1;'),REFRESH:('DWC_GetFriendDataType(&friendList[index])','DWC_GetFriendDataType(&friendList[index+1])')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(128):
            v=vector(seed);left=run(image,row,native,v,seed);right=run(image,row,compiled,v,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent source-revision/helper model differs',left,right))
            records.append(left)
        directory=WORK/'wrong-c'/f'{a:08x}';directory.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],directory/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Meaningful source-revision wrong-C negative did not mutate')
        source=directory/'wrong.c';source.write_text(changed);bad,body=build(source,directory/'proof',negative=True);failed=sum(not run(image,row,body,vector(seed),seed)['modelPassed'] for seed in range(16))
        if not failed:raise ValueError('Genuine wrong whole C did not reject independent pointer/type-frame model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['256 paired actual original/source entries: complete type1/empty-prefix rejection returns, original type-word extraction/ABI and prefix strlen/frame/version-buffer initialization before first parse provider.0synthetic returns.','Each type call actually executes original8-byte canonical Thumb binding veneer plus12/16-byte original type extraction helpers; separate count fields retain the veneer/logic distinction. Message executes original28-byte ARM strlen.0new helper/veneer source credit.128 separate standalone original top-helper entries plus128 nested original helper entries and43negative contracts qualify them.','Message parsing stops before memcmp; later strchr/strncpy/strtoul/protocol/network paths and version-buffer overflow behavior remain unexecuted. Friend refresh stops before first profile lookup beyond its actual early rejection; later scans/deletions/callbacks unexecuted.0provider/device/game/nativeWindows execution and storage extent/authorship credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),actualOriginalTypeBindingVeneerExecutions=2*sum(r['actualOriginalTypeVeneerInvocations'] for r in records),standaloneOriginalHelperEntries=128,originalStandaloneNestedHelperEntries=128,wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',report);return report
