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
SIZES={0x027f2450:380}
CODES={0x027f2450:364}

def run(main,wram,case,index,body=None,budget=100000):
    TOP=case['entry'];SIZE=SIZES[TOP]
    if case['aid']not in range(32):raise ValueError('Unsigned32 AID shift domain0..31 required')
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original TX host module bytes differ')
    if body is not None:
        if len(body)!=SIZE:raise ValueError('Full TX ordinary C source extent differs')
        raw=bytearray(main);raw[TOP-MAIN:TOP-MAIN+SIZE]=body;main=bytes(raw)
    rng=random.Random(0x205000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];visited=[];writes=[];owned_writes=[];entry_events=[];executions=[];callback=[None];callback_active=[];callback_returns=[];helper_active=[];helper_returns=[];watched={0x027ea480,0x027ebe98,0x037f8d58}
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
    cpu.mem_write(context+0x17c,bytes(12));phase='incoming-frame-allocation';returned[0]=False;cpu.reg_write(REGISTERS[0],context+0x188);cpu.reg_write(REGISTERS[1],256);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x037f886c,STOP+4,count=100000)
    if not returned[0]or cpu.reg_read(REGISTERS[0])!=DATA+0x7820:raise ValueError('Original incoming receive-frame allocation did not return expected backing')
    packet=DATA+0x7820;frame=packet+16;executions.append(dict(name='incoming-frame-allocation',entry='0x37f886c',actualReturn=True,sourceCredit=0));cpu.mem_write(frame,bytes(80));cpu.mem_write(packet+12,struct.pack('<HH',0xa55a,0x5aa5));cpu.mem_write(frame+6,struct.pack('<H',0xabcd));cpu.mem_write(frame+8,struct.pack('<H',case['oldKeyStatus']));cpu.mem_write(frame+10,struct.pack('<H',0x1234));cpu.mem_write(frame+12,struct.pack('<H',case['timestamp']));cpu.mem_write(frame+16,struct.pack('<H',case['mpdu']));cpu.mem_write(frame+44,struct.pack('<HH',case['txop'],case['bitmap']));cpu.mem_write(context+844,struct.pack('<H',case['sta']));cpu.mem_write(context+942,struct.pack('<H',case['aid']));cpu.mem_write(context+972,bytes(2));bssid=bytes.fromhex('123456789abc');link=bytes.fromhex('a1b2c3d4e5f6');cpu.mem_write(context+936,bssid);cpu.mem_write(context+966,link);cpu.mem_write(frame+30,bssid if case['bssidMatches']else bytes([bssid[0]^1])+bssid[1:]);cpu.mem_write(frame+36,link if case['linkMatches']else bytes([link[0]^1])+link[1:]);cpu.mem_write(context+1250,struct.pack('<H',0x55aa));cpu.mem_write(MAC+0x4098,struct.pack('<H',0x100|case['out98']));cpu.mem_write(MAC+0x4094,struct.pack('<H',case['out94']));cpu.mem_write(MAC+0x204,struct.pack('<H',case['retry']));cpu.mem_write(HW+0x210,struct.pack('<I',case['irqMask']))
    before={address:bytes(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=0 if case.get('nullFrame')else frame;initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    if case.get('missingMessageQueue'):cpu.mem_write(context+0x304,bytes(4))
    phase='target';returned[0]=False
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    nonstack=[r for r in writes if not STACK<=r[0]<STACK+0x4000];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),irqMaskPreserved=int.from_bytes(cpu.mem_read(HW+0x210,4),'little')==case['irqMask'],returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1))
    early=case['sta']!=0x40 or not case['bssidMatches']or not case['linkMatches'];actual_pointer=int.from_bytes(cpu.mem_read(DATA+0x6800,4),'little');buffer=cpu.mem_read(packet,66);expected_own=[]
    if early:
        checks['earlyReturn']=cpu.reg_read(REGISTERS[0])==1;checks['earlyNonstackPreserved']=all(cpu.mem_read(address,len(raw))==raw for address,raw in before.items()if address!=STACK)
    else:
        key=0x2000 if case['bitmap']&((1<<case['aid'])&65535)else 0;expected_own.append([context+1250,2,key])
        if case['out98']&0x8000 and case['retry']!=0:key|=0x4000;expected_own.append([context+1250,2,key])
        length=(case['mpdu']-28)&65535;header_length=(length+49)//2;status=case['oldKeyStatus']|key|((case['out98']&0x8000)>>4)|((case['out94']&0x8000)>>3);ack=(case['timestamp']+((case['bitmap'].bit_count()*(case['txop']+10)+252)>>4))&65535;expected_own +=[[frame+6,2,length],[packet+12,2,0x182],[packet+14,2,header_length],[frame+8,2,status],[frame+10,2,ack]];checks['acceptedReturn']=cpu.reg_read(REGISTERS[0])==0;checks['originalPointerQueued']=actual_pointer==packet;checks['independentHeaderAndFields']=cpu.mem_read(packet+12,4)==struct.pack('<HH',0x182,header_length)and cpu.mem_read(frame+6,8)==struct.pack('<HHHH',length,status,ack,case['timestamp']);checks['independentKeyRegister']=int.from_bytes(cpu.mem_read(context+1250,2),'little')==key
    checks['independentOwnOrderedStores']=[w for w in owned_writes if not STACK<=w[0]<STACK+0x4000]==expected_own
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownedWrites=owned_writes,events=entry_events,actualNativeHelperReturns=helper_returns,visited=sorted(set(visited)),instructions=len(visited),actualSetupReturns=executions,queuedPointer=hex(actual_pointer),packetBytes=bytes(buffer).hex(),memorySha256={hex(address):hashlib.sha256(cpu.mem_read(address,len(raw))).hexdigest()for address,raw in regions.items()},providerReplacements=[],sourceCredit=0,allLowerAllocQueueAndByteHelpersOriginal=True,sceneNetworkConcurrencyAndProducerUnproved=True)

def cases():
    base=dict(entry=0x027f2450,mode=0,contextOffset=0,irqMask=0xffffffff,sta=0x40,bssidMatches=True,linkMatches=True,aid=0,bitmap=1,oldKeyStatus=0xa000,timestamp=65535,txop=65535,mpdu=28,out98=0x8000,out94=0x8000,retry=1)
    cases=[dict(base,sta=sta,bssidMatches=bssid,linkMatches=link)for sta,bssid,link in itertools.product((0,0x40),(False,True),(False,True))]
    cases +=[dict(base,aid=aid,bitmap=bitmap,oldKeyStatus=old,timestamp=time,txop=op,mpdu=length,out98=out98,out94=out94,retry=retry)for aid,bitmap,old,time,op,length,out98,out94,retry in itertools.product((0,1,15,16,31),(0,1,0x8000,0xffff),(0,0xa000),(0,65535),(0,65535),(28,29,90),(0,0x8000),(0,0x8000),(0,1))]
    return cases
