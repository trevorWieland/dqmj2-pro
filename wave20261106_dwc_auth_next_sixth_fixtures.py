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
from wave20261106_dwc_auth_next_sixth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_sixth_build import build

DIFF,FREESPOT,CHANNEL=0x2094ab0,0x209545c,0x2095630
DESC,CTRL,GLOBAL,STOP,SP=0x2170000,0x2171000,0x21d18cc,0x27e0000,0x2701000
GETMEM,STRNCMP,NINTENDO=0x20946ec,0x201d914,0x20949e4


def helpers(image,inventory):
    result=[]
    for a,size,mode in [(GETMEM,68,'thumb'),(STRNCMP,52,'arm')]:
        canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\('+mode+r',size=0x%x\) addr:0x%08x'%(size,a),x)),None)
        if canonical is None:raise ValueError('Actual pure helper canonical entry/range/mode absent')
        result.append(dict(program='',processor='arm9',module='main',mode=mode,address=hex(a),bytes=size,canonicalInventoryRecord=canonical,targetSha256=hashlib.sha256(image[a-0x2000000:a-0x2000000+size]).hexdigest(),sourceCredit=0,extentCredit=0))
    return result


def validate_helper(item,image,inventory):
    expected=next((x for x in helpers(image,inventory) if x['address']==item['address']),None)
    if expected is None or item!=expected:raise ValueError('Exact pure helper namespace/mode/full boundary/body differs')


def equal_string(left,right,n):
    for a,b in zip(left[:n],right[:n]):
        if a!=b:return False
        if a==0:return True
    return True


def state(a,seed):
    work=bytearray([0xa5])*3352;desc=bytearray([0x63])*192;connect=[0,6,1,15][seed%4];work[3340]=(work[3340]&240)|connect;count=[0,1,2,3,5,10,11,4,2,1,3,5][seed%12] if a==CHANNEL else seed%6;work[3346]=count;length=[0,1,8,31,32,3][seed%6];struct.pack_into('<H',desc,10,length);ssid=b'FREESPOT'+bytes(24) if seed%3 else b'FREExPOT'+bytes(24);desc[12:44]=ssid;expected=bytearray(work)
    if a==CHANNEL:
        changed=0
        for i in range(11):
            at=1092+i*4;work[at]=(seed+i)%3;work[at+3]=(i*11+seed)&255;channel=[0,1,14,128,65535][(seed+i)%5];struct.pack_into('<H',work,1136+i*192+54,channel)
        expected=bytearray(work)
        for i in range(count):
            at=1092+i*4;channel=struct.unpack_from('<H',work,1136+i*192+54)[0]
            if work[at]==0 and channel-1!=(work[at+3]&127):expected[at+3]&=127;changed+=1
            else:expected[at+3]|=128
        answer=changed
    elif a==FREESPOT:answer=8 if connect in [0,6] and equal_string(desc[12:44],b'FREESPOT',8) else 0
    else:
        answer=0xffffffff
        for i in range(count):
            at=1136+i*192;item_length=length if (i+seed)%2==0 else (length+1)%33;struct.pack_into('<H',work,at+10,item_length);work[at+12:at+44]=ssid if i==seed%max(count,1) else b'OTHER'+bytes(27);work[1092+i*4+1]=10+i
        expected=bytearray(work)
        for i in range(count):
            at=1136+i*192
            if length==struct.unpack_from('<H',work,at+10)[0] and equal_string(desc[12:44],work[at+12:at+44],length):answer=work[1092+i*4+1];break
    return bytes(work),bytes(desc),bytes(expected),answer,length,connect,count


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000);work,desc,expected_work,answer,length,connect,count=state(a,seed);global_bytes=struct.pack('<5I',0,0,0,0,CTRL);memory={CTRL:work,DESC:desc,GLOBAL:global_bytes}
    for at,data in memory.items():cpu.mem_write(at,data)
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[0]=CTRL if a==CHANNEL else DESC
    if a==DIFF:initial[1]=CTRL
    initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;pcs=[];active=None;invocations=0;returns=0
    def code(machine,at,size,user):
        nonlocal observed,interface,active,invocations,returns
        regs=[machine.reg_read(r) for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if at==STOP:
            observed=dict(kind='return',value=regs[0]);interface=regs[4:12]==initial[4:12] and regs[13]==SP;machine.emu_stop();return
        if at==NINTENDO:
            if not thumb:raise ValueError('Actual Nintendo-SSID provider mode differs')
            observed=dict(kind='provider',address=hex(at));interface=a==DIFF and length==32 and regs[0]==DESC;machine.emu_stop();return
        for helper,size,mode in [(GETMEM,68,'thumb'),(STRNCMP,52,'arm')]:
            if helper<=at<helper+size:
                if thumb!=(mode=='thumb'):raise ValueError('Actual original pure helper mode differs')
                if at==helper:
                    if active is not None:raise ValueError('Unexpected nested pure helper')
                    invocations+=1;active=helper
                pcs.append(at);return
        if not a<=at<a+len(body) or not thumb:raise ValueError('Caller escaped original bounded body/helpers')
        if active is not None:returns+=1;active=None
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==CHANNEL and size==1 and any(at==CTRL+1092+i*4+3 for i in range(11)):return
        raise ValueError('Unexpected caller/helper RAM mutation')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=50000)
    if observed is None:raise ValueError('Caller did not reach original bounded return/provider')
    expected=dict(kind='provider',address=hex(NINTENDO)) if a==DIFF and length==32 else dict(kind='return',value=answer);guards=all(bytes(cpu.mem_read(at,len(data)))==(expected_work if at==CTRL else data) for at,data in memory.items());model=observed==expected and interface and guards and invocations==returns
    return dict(address=row['address'],seed=seed,vector=dict(length=length,connectType=connect,count=count),observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,modelPassed=model,actualOriginalHelperInvocations=invocations,actualOriginalHelperReturns=returns,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();specs=helpers(image,inventory);neg_helpers=[]
    for item in specs:
        validate_helper(item,image,inventory)
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','data'),('address',hex(int(item['address'],0)+2)),('bytes',item['bytes']-2),('targetSha256','0'*64)]:
            bad=copy.deepcopy(item);bad[key]=value
            try:validate_helper(bad,image,inventory)
            except ValueError as error:neg_helpers.append(dict(address=item['address'],case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Wrong pure helper metadata admitted')
    records=[];negative=[];variants={DIFF:('found=0xffffffff;','found=0;'),FREESPOT:('return 8;','return 7;'),CHANNEL:('work->findList[i].find=0;','work->findList[i].find=1;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(12):
            left=run(image,row,native,seed);right=run(image,row,compiled,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent real channel/SSID/descriptor model differs',left,right))
            records.append(left)
        folder=WORK/'wrong-c'/f'{a:08x}';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Meaningful whole C negative did not mutate')
        source=folder/'wrong.c';source.write_text(changed);bad,body=build(source,folder/'proof',negative=True);failed=sum(not run(image,row,body,seed)['modelPassed'] for seed in range(12))
        if not failed:raise ValueError('Wrong complete C passed independent channel/SSID model')
        negative.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['36paired full original/source entries. Full channel-marking/count returns,exact eight-byte Freespot checks and descriptor-list lookup return with actual R0/callee-saved/SP/full RAM guards;32-byte Nintendo-SSID cases stop before the actual provider entry.','Actual canonical original GetMemPtr68Thumb and strncmp52ARM helpers execute/return under bounded image/namespace/mode/body witnesses,0source/extent credit. No synthetic returns. Channel logic preserves low7channel bits and reads actual16-bit BSSchannel+54;3independent complete C negatives reject.','No Nintendo-SSID provider/network/socket/WCM/WiFi/flash/cache/timer/device/game/nativeWindows execution or BSS/static/external data authorship credit. Correct5630ABI u8(ACWORK*) is independent of the explicitly rejected older unused iCopySSID declaration.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();result=dict(status='passed',records=records,pureHelperQualifications=specs,pureHelperNegativeControls=neg_helpers,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),actualOriginalHelperReturns=2*sum(r['actualOriginalHelperReturns'] for r in records),wholeCNegativeControlsRejected=len(negative),wrongC=negative,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',result);return result
