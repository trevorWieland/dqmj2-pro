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
TOP=0x027eff00

def run(main,wram,case,index,body=None,budget=100000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original TX host module bytes differ')
    if case['priority']not in range(3):raise ValueError('TX priority source-array contract0..2 required')
    if body is not None:
        if len(body)!=544:raise ValueError('Full TX ordinary C source extent differs')
        raw=bytearray(main);raw[TOP-MAIN:TOP-MAIN+544]=body;main=bytes(raw)
    rng=random.Random(0x205000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';returned=[False];visited=[];writes=[];owned_writes=[];entry_events=[];executions=[];callback=[None];callback_active=[];callback_returns=[]
    def code(machine,pc,size,user):
        if pc==STOP:
            if callback_active:raise ValueError('TX caller stopped with an unfinished real callback')
            returned[0]=True;machine.emu_stop();return
        if phase=='prefix'and not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Original TX descriptor prefix escaped')
        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('TX original execution escaped initialized host modules')
        if phase=='target':
            if TOP+532<=pc<TOP+544:raise ValueError('TX caller attempted to fetch its generated literal pool')
            while callback_active and pc==callback_active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==callback_active[-1]['sp']:
                item=callback_active.pop();item['actualReturn']=True;item['outgoingR0']=machine.reg_read(REGISTERS[0]);item['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved');callback_returns.append(item)
            if pc==callback[0]:callback_active.append(dict(entry=hex(pc),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
            visited.append(pc)
            if pc in(0x037fb928,0x037fb8f0,0x037f8a80,0x027f0288,0x027f0120,0x027e9cc0):entry_events.append(dict(entry=hex(pc),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],lr=hex(machine.reg_read(REGISTERS[-1])),sp=hex(machine.reg_read(REGISTERS[-2]))))
    def store(machine,access,address,width,value,user):
        if phase=='target':
            row=[address,width,value&((1<<(width*8))-1)];writes.append(row)
            if TOP<=machine.reg_read(UC_ARM_REG_PC)<TOP+544:owned_writes.append(row)
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
    priority=case['priority'];heap=context+0x194+priority*12;queue=context+0x42c+priority*20;kind=case['kind'];count=0 if kind=='empty'else 1;head=0xffffffff if kind in('empty','sentinel','busy')else DATA+0x3000;cpu.mem_write(heap,struct.pack('<IIH',head,head,count));cpu.mem_write(queue,struct.pack('<HH',1 if kind=='busy'else 0,case['inCount']));cpu.mem_write(HW+0x210,struct.pack('<I',case['irqMask']));cpu.mem_write(context+0x354,struct.pack('<H',case.get('powerState',2)));cpu.mem_write(context+0x3d0,struct.pack('<H',case.get('lifetime',65535)));cpu.mem_write(context+0x3ec,struct.pack('<H',case.get('interval',0)))
    if kind=='frame':
        cpu.mem_write(head,bytes(0x200));cpu.mem_write(head,struct.pack('<II',0xffffffff,0xffffffff));cpu.mem_write(head+0xc,struct.pack('<H',65535));cpu.mem_write(head+0x10+0x14,struct.pack('<H',case['frameControl']));cpu.mem_write(head+0x10+6,bytes(2));cpu.mem_write(head+0x10+0x12,struct.pack('<H',24))
    cpu.mem_write(DATA+0x6000,struct.pack('<H',case.get('camState',0)))
    if 'camActive'in case:
        flags=int.from_bytes(cpu.mem_read(context+0x530,2),'little');cpu.mem_write(context+0x530,struct.pack('<H',(flags&~1)|int(case['camActive'])))
    if 'camFrameCount'in case:cpu.mem_write(DATA+0x6016,struct.pack('<H',case['camFrameCount']))
    callback[0]=int.from_bytes(cpu.mem_read(queue+16,4),'little')
    cam_state=int.from_bytes(cpu.mem_read(DATA+0x6000,2),'little');cam_active=bool(int.from_bytes(cpu.mem_read(context+0x530,2),'little')&1);cam_frame_count=int.from_bytes(cpu.mem_read(DATA+0x6016,2),'little')
    before={address:bytes(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=priority;initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    if case.get('missingCamPointer'):cpu.mem_write(context+0x31c,bytes(4))
    if case.get('missingMessageQueue'):cpu.mem_write(context+0x304,bytes(4))
    phase='target';returned[0]=False
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',pc=hex(cpu.reg_read(UC_ARM_REG_PC)),events=entry_events,postFaultCredit=0,sourceCredit=0)
    nonstack=[r for r in writes if not STACK<=r[0]<STACK+0x4000];checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),irqMaskPreserved=int.from_bytes(cpu.mem_read(HW+0x210,4),'little')==case['irqMask'],returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1))
    if kind!='frame':expected_own=[]
    elif case.get('interval',0)>case.get('lifetime',65535)*8:
        expected_own=[[context+0x4da,2,1],[head+0x10+8,2,2],[queue+4,2,1]]
    elif(priority==0 or priority==1 and cam_state==0x40)and not cam_active:
        expected_own=[]
    elif(priority==0 or priority==1 and cam_state==0x40)and cam_state!=0x40:
        expected_own=[[head+0x10+8,2,2]]
    else:
        mac_frame=int.from_bytes(before[DATA][queue-DATA+8:queue-DATA+12],'little');control=0xa000 if case['frameControl']&12==4 else 0x9000 if case['frameControl']&0xfc==0x50 else 0x8000;control|=(mac_frame&0x3fff)//2;expected_own=[[queue,2,1],[queue+2,2,(case['inCount']+1)&65535],[queue+12,4,head+0x10]]+([[mac_frame+12,2,case['frameControl']|0x2000]]if case['mode']==1 and cam_frame_count>1 else[])+[[0x048080a0+priority*4,2,control]]
    direct_irq=[event for event in entry_events if event['entry']=='0x37fb928'and TOP<=int(event['lr'],0)<TOP+532]
    checks['directIrqMaskContract']=direct_irq==[]if kind=='empty'else len(direct_irq)==1 and direct_irq[0]['incoming'][0]==1<<24
    checks['callbackAbiAndReturn']=all(item['actualReturn']and item['calleeSavedPreserved']and item['arguments'][:2]==[head+0x10,0]for item in callback_returns)
    checks['callbackExpectedCount']=len(callback_returns)==int(case.get('interval',0)>case.get('lifetime',65535)*8)
    checks['independentOwnNonstackStores']=[row for row in owned_writes if not STACK<=row[0]<STACK+0x4000]==expected_own
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownedWrites=owned_writes,originalInitializedCamState=cam_state,originalInitializedCamActive=cam_active,actualCallbackReturns=callback_returns,syntheticCamState=case.get('camState',0),originalInitializedCamFrameCount=cam_frame_count,events=entry_events,visited=sorted(set(visited)),instructions=len(visited),actualSetupReturns=executions,memorySha256={hex(address):hashlib.sha256(cpu.mem_read(address,len(raw))).hexdigest()for address,raw in regions.items()},providerReplacements=[],sourceCredit=0,boundedNativeEvidence=True,frameBranchIndependentEffectsModelIncomplete=True,dmaLimitZeroCpuCopyFallbackPrerequisite=True,timeoutCamCallbackAndSceneContextUnproved=True)

def cases():
    vectors=[dict(mode=mode,priority=pri,kind='frame',contextOffset=0,irqMask=0xffffffff,inCount=count,frameControl=fc,lifetime=0 if expired else 65535,interval=1 if expired else 0,camState=camstate,powerState=power)for mode,pri,count,fc,expired,camstate,power in itertools.product((0,1,2,3),range(3),(0,65535),(0,4,0x50),(False,True),(0,0x40),(0,2))]
    vectors +=[dict(mode=mode,priority=pri,kind=kind,contextOffset=off,irqMask=irq,inCount=65535,frameControl=0,lifetime=65535,interval=0)for mode,pri,kind,off,irq in itertools.product(range(4),range(3),('empty','busy','sentinel'),(0,4),(0,0xffffffff))]
    vectors +=[dict(mode=mode,priority=pri,kind='frame',contextOffset=0,irqMask=0xffffffff,inCount=1,frameControl=0,lifetime=65535,interval=0,camState=0x40,camActive=False,powerState=2)for mode,pri in itertools.product(range(4),(0,1))]
    vectors +=[dict(mode=1,priority=pri,kind='frame',contextOffset=0,irqMask=0xffffffff,inCount=count,frameControl=0,lifetime=65535,interval=0,camState=0x40,camActive=True,camFrameCount=frames,powerState=2)for pri,count,frames in itertools.product(range(3),(0,65535),(0,2))]
    return vectors
