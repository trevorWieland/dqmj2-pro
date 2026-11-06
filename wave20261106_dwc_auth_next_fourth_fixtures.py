import copy
import hashlib
import json
import re
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261106_dwc_auth_next_fourth_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK
from wave20261106_dwc_auth_next_fourth_build import build

CREATE,SSID,INSERT,FREE,ALL,TYPE=0x2094284,0x2094530,0x20945bc,0x2094600,0x209463c,0x20947b4
GLOBAL,HOLD,CTRL,CONFIG,INFO,WCM,SOC,NET,FREEPTR=0x21d18cc,0x2170000,0x2171000,0x2174000,0x2175000,0x2178000,0x217b000,0x217b100,0x217b200
STOP,ALLOC_CB,FREE_CB,SP=0x27e0000,0x27e1000,0x27e2000,0x2701000
GETMEM,CONVERT=0x20946ec,0x2094818
PROVIDERS={0x2008d78:'arm',0x2008c28:'arm',0x208b524:'thumb'}


def helper_specs(image,inventory):
    result=[]
    for address,size in [(GETMEM,68),(CONVERT,12)]:
        canonical=next((x for x in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x%x\) addr:0x%08x'%(size,address),x)),None)
        if canonical is None:raise ValueError('Actual canonical pure AC helper absent')
        result.append(dict(program='',processor='arm9',module='main',mode='thumb',address=hex(address),bytes=size,canonicalInventoryRecord=canonical,targetSha256=hashlib.sha256(image[address-0x2000000:address-0x2000000+size]).hexdigest(),helperSourceCredit=0,helperExtentCredit=0))
    return result


def validate_helper(item,image,inventory):
    expected=next((x for x in helper_specs(image,inventory) if x['address']==item['address']),None)
    if expected is None or any(item.get(k)!=expected[k] for k in ['program','processor','module','mode','address','bytes','canonicalInventoryRecord','targetSha256']):raise ValueError('Actual pure helper namespace/mode/full original boundary/hash changed')


def run(image,row,body,seed):
    a=int(row['address'],0);cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_write(a,body);cpu.mem_map(STOP,0x3000);cpu.mem_map(SP-0x4000,0x5000);cpu.mem_write(SP-0x4000,bytes([0xa5])*0x4000)
    flags=[0,0,1,2,4,8,16,31][seed%8];name=[1,2,1,2,4,8,16,32][seed%8];present=a not in [FREE,ALL] or seed!=0;alloc=ALLOC_CB+(seed&1);free=FREE_CB+((seed>>1)&1);override=[0,1,0,4,8,0,99,255][seed%8];input_type=[0,1,2,3,5,6,127,255][seed%8];index=seed%3
    hold=bytearray([0x61])*36;struct.pack_into('<II',hold,0,alloc,free);hold[8]=flags;hold[34]=override;work=bytearray([0x62])*3352;work[3340]=[0,0xf0,0xff,0x21,0xc4,0x98,0x37,0xa6][seed%8];config=struct.pack('<IIBBBB',alloc,free,seed%4,seed%2,seed%9,seed%2);memory={GLOBAL:struct.pack('<5I',WCM,SOC,NET,HOLD if present else 0,CTRL),HOLD:bytes(hold),CTRL:bytes(work),CONFIG:config,INFO:bytes([0x63])*240,FREEPTR:bytes([0x64])*32};expected_memory=dict(memory)
    for at,data in memory.items():cpu.mem_write(at,data)
    if a==CREATE:args=[CONFIG];target=ALLOC_CB;frame=[1,36]
    elif a==SSID:
        args=[INFO,FREEPTR,seed%4];target=0x2008d78;frame=[CTRL,0,240];changed=bytearray(work);changed[3340]=(changed[3340]&240)|1;expected_memory[CTRL]=bytes(changed)
    elif a==INSERT:args=[index,INFO];target=0x2008c28;frame=[INFO,CTRL+index*256,240]
    elif a==FREE:
        args=[name,FREEPTR,seed*17];target=FREE_CB if present and flags&name else None;frame=[name,FREEPTR,seed*17]
        if target is not None:changed=bytearray(hold);changed[8]&=~name;expected_memory[HOLD]=bytes(changed)
    elif a==ALL:
        args=[];flag=next((v for v in [16,8,4,2,1] if flags&v),None);target=FREE_CB if present and flag else None
        if target is not None:
            ptr={16:CTRL,8:NET,4:SOC,2:WCM,1:HOLD}[flag];frame=[flag,ptr,{16:3352,8:12,4:88,2:8960,1:36}[flag]];changed=bytearray(hold);changed[8]&=~flag;expected_memory[HOLD]=bytes(changed)
        else:frame=[]
    elif a==TYPE:
        args=[input_type];target=0x208b524;frame=[0];changed=bytearray(hold);changed[23]=override if override else (input_type-3 if input_type>2 else input_type)&255;expected_memory[HOLD]=bytes(changed)
    else:raise ValueError('Unexpected owned AC caller')
    initial=[0x64d00000+i*0x101+seed for i in range(15)];initial[:len(args)]=args;initial[-2:]=[SP,STOP|1];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;interface=True;pcs=[];helper_active=None;helper_invocations=0;helper_returns=0
    def code(machine,at,size,user):
        nonlocal observed,interface,helper_active,helper_invocations,helper_returns
        regs=[machine.reg_read(r) for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if at==STOP:
            if target is not None or regs[4:12]!=initial[4:12] or regs[13]!=SP:raise ValueError('Actual complete AC return ABI or guard differs')
            observed=dict(kind='return');machine.emu_stop();return
        if at in [ALLOC_CB,FREE_CB] or at in PROVIDERS:
            mode='thumb' if at==ALLOC_CB and alloc&1 or at==FREE_CB and free&1 else 'arm' if at in [ALLOC_CB,FREE_CB] else PROVIDERS[at]
            if target!=at or thumb!=(mode=='thumb'):raise ValueError('Actual AC callback/provider entry or ARM/Thumb mode differs')
            observed=dict(kind='provider',address=hex(at));interface=regs[:len(frame)]==frame;machine.emu_stop();return
        for helper,length in [(GETMEM,68),(CONVERT,12)]:
            if helper<=at<helper+length:
                if not thumb:raise ValueError('Actual original AC helper mode differs')
                if at==helper:
                    if helper_active is not None:raise ValueError('Unexpected nested AC helper')
                    helper_active=helper;helper_invocations+=1
                pcs.append(at);return
        if not a<=at<a+len(body) or not thumb:raise ValueError('AC caller escaped original bounded body/helpers')
        if helper_active is not None:helper_returns+=1;helper_active=None
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if SP-0x4000<=at and at+size<=SP:return
        if a==SSID and at==CTRL+3340 and size==1:return
        if a in [FREE,ALL] and at==HOLD+8 and size==1:return
        if a==TYPE and at==HOLD+23 and size==1:return
        raise ValueError('Unexpected AC caller/helper RAM write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(a|1,STOP+4,count=20000)
    if observed is None:raise ValueError('AC caller did not reach bounded return/provider')
    guards=all(bytes(cpu.mem_read(at,len(data)))==expected_memory[at] for at,data in memory.items());expected=dict(kind='return') if target is None else dict(kind='provider',address=hex(target));model=observed==expected and interface and guards and helper_invocations==helper_returns
    return dict(address=row['address'],seed=seed,vector=dict(present=present,flags=flags,name=name,index=index,overrideType=override,inputType=input_type,alloc=hex(alloc),free=hex(free)),observed=observed,expected=expected,topReturned=observed['kind']=='return',partialProviderStopped=observed['kind']=='provider',providerInterfaceModelPassed=interface,independentMutationModelPassed=guards,modelPassed=model,actualOriginalHelperInvocations=helper_invocations,actualOriginalHelperReturns=helper_returns,providerInstructionExecutions=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();helpers=helper_specs(image,inventory);helper_negatives=[]
    for item in helpers:
        validate_helper(item,image,inventory)
        for key,value in [('program','child'),('processor','arm7'),('module','ov000'),('mode','arm'),('address',hex(int(item['address'],0)+2)),('bytes',item['bytes']-2),('targetSha256','0'*64)]:
            wrong=copy.deepcopy(item);wrong[key]=value
            try:validate_helper(wrong,image,inventory)
            except ValueError as error:helper_negatives.append(dict(address=item['address'],case=key,rejected=True,reason=str(error)))
            else:raise ValueError('Invalid original AC pure helper metadata admitted')
    records=[];negatives=[];variants={CREATE:('config->alloc(1,sizeof(tagACHOLD))','config->alloc(1,sizeof(tagACHOLD)+4)'),SSID:('work->connectType=1;','work->connectType=2;'),INSERT:('no*256','no*512'),FREE:('(*myAcHold->free)(name,ptr,size);','(*myAcHold->free)(name,ptr,size+4);'),ALL:('(*myAcHold->free)(0x10,ptr,0xd18);','(*myAcHold->free)(0x10,ptr,0xd1c);'),TYPE:('acHold->type=selected;','acHold->type=selected+1;')}
    for row in rows:
        a=int(row['address'],0);native=image[a-0x2000000:a-0x2000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(8):
            left=run(image,row,native,seed);right=run(image,row,compiled,seed)
            if left!=right or not left['modelPassed']:raise ValueError(('Independent complete AC guard/provider/state model differs',left,right))
            records.append(left)
        folder=WORK/'wrong-c'/f'{a:08x}';folder.mkdir(parents=True,exist_ok=True)
        for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
        before,after=variants[a];text=(ROOT/row['source']).read_text();changed=text.replace(before,after,1)
        if changed==text:raise ValueError('Meaningful complete AC wrong-C variant did not mutate')
        source=folder/'wrong.c';source.write_text(changed);bad,body=build(source,folder/'proof',negative=True);failed=sum(not run(image,row,body,seed)['modelPassed'] for seed in range(8))
        if not failed:raise ValueError('Genuine wrong whole AC C did not reject independent model')
        negatives.append(dict(address=row['address'],genuinelyLinked=True,matchedNative=False,independentModelFailures=failed,changedExpression=[before,after],realLink=bad['realLink']))
    limits=['48paired original/source full caller entries. Complete no-hold/no-allocation guards in Free/FreeAll return with actual callee-saved/SP checks; other paths stop before first allocator/free/clear/copy/ESSID provider instruction. Actual canonical Thumb GetMemPtr68B and ConvertAPType12B helpers execute/return without source or extent credit. Both ARM/Thumb indirect alloc/free targets checked.','Independent model verifies exact five global pointer slots, allocation-priority16/8/4/2/1 and sizes,pre-provider flag clearing,SSID connect-type nibble preservation,insertion256-byte stride/240-byte extent and override/conversion type writes. All other source caller/provider/RAM/device behavior remains unexecuted despite complete native-byte genuine link equality.','No allocation/free/memory-copy/cache/ESSID/postal/WiFi/flash/socket/network/device/timer/game/nativeWindows provider execution or synthetic returns. All original BSS/static/external data storage and imported source authorship remains0credit.']
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();result=dict(status='passed',records=records,pureHelperQualifications=helpers,pureHelperNegativeControls=helper_negatives,nativeAndCompiledReturningCalls=2*sum(r['topReturned'] for r in records),nativeAndCompiledPartialStops=2*sum(r['partialProviderStopped'] for r in records),actualNativeCalleeBodiesExecuted=2*sum(r['actualOriginalHelperInvocations'] for r in records),actualOriginalHelperReturns=2*sum(r['actualOriginalHelperReturns'] for r in records),wholeCNegativeControlsRejected=len(negatives),wrongC=negatives,nativeDevicesOrScenesExecuted=0,traceSha256=trace,limits=limits);write_json(LANE/'caller-fixtures.json',result);return result
