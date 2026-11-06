import hashlib
import itertools
import json
import random
import struct
from pathlib import Path
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
from project import ROOT,sha256,write_json

MAIN,WRAM,DATA,STACK,MAC,HW,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x04000000,0x0f000000,0x0380fff4
SIZES={0x027edc6c:248,0x027edd64:236}
CODES={0x027edc6c:240,0x027edd64:232}

def run(main,wram,case,index,body=None,budget=100000):
    TOP=case['entry'];SIZE=SIZES[TOP]
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original TX host module bytes differ')
    if body is not None:
        if len(body)!=SIZE:raise ValueError('Full TX ordinary C source extent differs')
        raw=bytearray(main);raw[TOP-MAIN:TOP-MAIN+SIZE]=body;main=bytes(raw)
    rng=random.Random(0x205000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];visited=[];writes=[];owned_writes=[];entry_events=[];executions=[];callback=[None];callback_active=[];callback_returns=[];helper_active=[];helper_returns=[];watched={0x037f886c,0x027eb078,0x027ea0ec,0x027ead5c,0x027ead30,0x037f8d58}
    def code(machine,pc,size,user):
        if pc==STOP:
            if callback_active or helper_active:raise ValueError('MLME caller stopped with unfinished native helper')
            returned[0]=True;machine.emu_stop();return
        if phase=='prefix'and not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Original TX descriptor prefix escaped')
        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('TX original execution escaped initialized host modules')
        if phase=='target':
            if TOP+CODES[TOP]<=pc<TOP+SIZE:raise ValueError('Copy caller attempted to fetch its generated literal pool')
            while callback_active and pc==callback_active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==callback_active[-1]['sp']:
                item=callback_active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');callback_returns.append(item)
            if pc==callback[0]:callback_active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
            while helper_active and pc==helper_active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==helper_active[-1]['sp']:
                item=helper_active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');helper_returns.append(item)
            if pc in watched:helper_active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
            visited.append(pc)
            if pc in(0x037fb928,0x037fb8f0,0x037f8a80,0x027f0288,0x027f0120,0x027e9cc0):entry_events.append(dict(entry=hex(pc),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],lr=hex(machine.reg_read(REGISTERS[-1])),sp=hex(machine.reg_read(REGISTERS[-2]))))
    def store(machine,access,address,width,value,user):
        if phase=='target':
            row=[address,width,value&((1<<(width*8))-1)];writes.append(row)
            if TOP<=machine.reg_read(UC_ARM_REG_PC)<TOP+SIZE:owned_writes.append(row)
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or int.from_bytes(cpu.mem_read(WORD,4),'little')!=context or cpu.mem_read(context,0x694)!=bytes(0x694):raise ValueError('Actual TX incoming descriptor clear differs')
    cpu.mem_write(context+0x31c,struct.pack('<I',DATA+0x6000));cpu.mem_write(context+0x320,struct.pack('<HH',2,2));cpu.mem_write(context+0x304,struct.pack('<I',DATA+0x6400))
    for name,entry,argument in[('queue-init',0x037fc6ac,(DATA+0x6400,DATA+0x6800,16)),('mode',0x027e8f3c,case['mode']),('cam-init',0x027ec51c,None),('tx-init',0x037faec0,None)]:
        phase=name;returned[0]=False;cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
        if isinstance(argument,tuple):
            for register,value in zip(REGISTERS,argument):cpu.reg_write(register,value)
        elif argument is not None:cpu.reg_write(REGISTERS[0],argument)
        cpu.emu_start(entry,STOP+4,count=100000)
        if not returned[0]:raise ValueError('Original TX setup failed actual return:'+name)
        executions.append(dict(name=name,entry=hex(entry),actualReturn=True,sourceCredit=0))
    for off in range(0x188,0x23c,12):cpu.mem_write(context+off,struct.pack('<IIH',0xffffffff,0xffffffff,0))
    for name,entry,args in [('os-heap-init',0x037fce24,[0,DATA+0x7400,DATA+0x8000,1]),('os-heap-create',0x037fcecc,[0,DATA+0x7800,DATA+(0x7820 if case.get('heapFailure')else 0x8000)]),('os-heap-current',0x037fcdf0,[0,0])]:
        phase=name;returned[0]=False;cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
        for reg,value in zip(REGISTERS,args):cpu.reg_write(reg,value)
        cpu.emu_start(entry,STOP+4,count=100000)
        if not returned[0]:raise ValueError('Actual OS heap prerequisite did not return:'+name)
        executions.append(dict(name=name,entry=hex(entry),actualReturn=True,outgoingR0=cpu.reg_read(REGISTERS[0]),sourceCredit=0))
    cpu.mem_write(context+0x17c,bytes(12));cpu.mem_write(HW+0x210,struct.pack('<I',case['irqMask']));mac=DATA+0x5100;ssid=DATA+0x5200+case['ssidAlignment'];cpu.mem_write(mac,bytes.fromhex('123456789abc'));cpu.mem_write(ssid,bytes([0,case['ssidLength']])+bytes((i*17+index)&255 for i in range(32)));expected_buffer=DATA+0x7820
    before={address:bytes(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0:3]=[0 if case.get('nullMac')else mac,case['aid'],0 if case.get('nullSsid')else ssid];initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    if case.get('missingMessageQueue'):cpu.mem_write(context+0x304,bytes(4))
    phase='target';returned[0]=False
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    nonstack=[r for r in writes if not STACK<=r[0]<STACK+0x4000];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),irqMaskPreserved=int.from_bytes(cpu.mem_read(HW+0x210,4),'little')==case['irqMask'],returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1))
    actual_pointer=int.from_bytes(cpu.mem_read(DATA+0x6800,4),'little');buffer=cpu.mem_read(expected_buffer,58)
    if case.get('heapFailure'):
        checks['independentOriginalFatalFlag']=int.from_bytes(cpu.mem_read(context+0x3f4,2),'little')==1;checks['returnAllocationFailure']=cpu.reg_read(REGISTERS[0])==0;checks['noOwnIndicationStores']=[w for w in owned_writes if not STACK<=w[0]<STACK+0x4000]==[];checks['originalFatalHelperActuallyReturned']=any(r['entry']=='0x27eb078'for r in helper_returns)
    else:
        checks['actualAllocatedMessageQueued']=actual_pointer==expected_buffer;checks['returnSuccess']=cpu.reg_read(REGISTERS[0])==1;expected_payload=bytes.fromhex('123456789abc')+struct.pack('<HH',case['aid']&0xfff if TOP==0x027edc6c else case['aid'],case['ssidLength'])+bytes((i*17+index)&255 if i<min(32,case['ssidLength'])else 0 for i in range(32));checks['independentIndicationFields']=buffer[16:58]==expected_payload;checks['independentHeader']=buffer[12:16]==struct.pack('<HH',0x86 if TOP==0x027edc6c else 0x87,21);expected_own=[[expected_buffer+12,2,0x86 if TOP==0x027edc6c else 0x87],[expected_buffer+14,2,21],[expected_buffer+22,2,case['aid']&0xfff if TOP==0x027edc6c else case['aid']],[expected_buffer+24,2,case['ssidLength']]];checks['independentOwnOrderedStores']=[w for w in owned_writes if not STACK<=w[0]<STACK+0x4000]==expected_own
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownedWrites=owned_writes,events=entry_events,actualNativeHelperReturns=helper_returns,visited=sorted(set(visited)),instructions=len(visited),actualSetupReturns=executions,queuedPointer=hex(actual_pointer),indicationBytes=bytes(buffer).hex(),memorySha256={hex(address):hashlib.sha256(cpu.mem_read(address,len(raw))).hexdigest()for address,raw in regions.items()},providerReplacements=[],sourceCredit=0,allLowerAllocQueueAndByteHelpersOriginal=True,sceneNetworkConcurrencyAndProducerUnproved=True)

def cases():
    positive=[dict(entry=entry,mode=mode,contextOffset=off,irqMask=0xffffffff,ssidLength=length,ssidAlignment=align,aid=aid)for entry,mode,off,length,align,aid in itertools.product(SIZES,(0,1),(0,4),(0,1,31,32,33,255),(0,1),(0,1,4095,4096,65535))]
    return positive+[dict(entry=entry,mode=mode,contextOffset=off,irqMask=0xffffffff,ssidLength=length,ssidAlignment=align,aid=aid,heapFailure=True)for entry,mode,off,length,align,aid in itertools.product(SIZES,(0,1),(0,4),(0,255),(0,1),(0,65535))]
