import hashlib
import json
import random
import struct
from collections import deque
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_INVALID,UC_HOOK_INTR
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
from project import ROOT
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
MAIN,WRAM,DATA,STACK,MAC,HW,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x04000000,0x0f000000,0x0380fff4
TOP,SIZE,CODE=0x037f8de0,952,876
DIRECT={0x037f9198:'WStop',0x027ead78:'RND_init',0x027ec51c:'InitCAM',0x027f4ccc:'InitApList',0x037faec0:'InitTxCtrl',0x037fb1e0:'InitRxCtrl',0x03806bf0:'_ll_udiv',0x037f9238:'WSetStaState',0x027f11a8:'StartBeaconFrame',0x027e9ea0:'WDisableTmpttPowerSave',0x027e9cc0:'WSetPowerState',0x037fb300:'WaitLoop_Rxpe'}
def run(main,wram,case,index,body=None,budget=200000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original WStart main/WRAM input changed')
    if body is not None:
        if len(body)!=SIZE:raise ValueError('WStart compiled C extent differs')
        wram=wram[:TOP-WRAM]+body+wram[TOP-WRAM+SIZE:]
    callsites={}
    for instruction in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(wram[TOP-WRAM:TOP-WRAM+CODE],TOP):
        if instruction.mnemonic=='bl':callsites[instruction.address+4]=int(instruction.op_str.lstrip('#'),0)
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);rng=random.Random(0x168000+index)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:bytes(0x10000),STACK:rng.randbytes(0x4000),MAC:bytes(0x5000),HW:bytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case.get('contextOffset',0);cpu.mem_write(DATA+0xf000,struct.pack('<I',context));phase='prefix';prefix=[];reads=[];writes=[];pcs=[];tail=deque(maxlen=48);faults=[];returned=[False];prefix_fill=[0];active=[];direct=[]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('WStart original producer prefix escaped')
            if pc==0x037fe014:prefix_fill[0]+=1
            return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            frame=active.pop();frame.update(actualReturn=True,result=[machine.reg_read(r)for r in REGISTERS[:4]],calleeSavedPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==frame['saved']);direct.append(frame)
        if pc==STOP:
            if active:raise ValueError('Startup returned with unfinished direct native callee')
            returned[0]=True;machine.emu_stop();return
        if TOP+CODE<=pc<TOP+SIZE:raise ValueError('Startup fetched its verified literal suffix')
        if pc in DIRECT:
            lr=machine.reg_read(REGISTERS[-1])&~1
            if callsites.get(lr)==pc:
                active.append(dict(name=DIRECT[pc],entry=hex(pc),lr=lr,sp=machine.reg_read(REGISTERS[-2]),arguments=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))

        if not(MAIN<=pc<MAIN+len(main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('WStart diagnostic execution escaped original native images')
        row=[pc,size,machine.reg_read(UC_ARM_REG_CPSR)&32];pcs.append(row);tail.append(row)
    def read(machine,access,address,width,value,user):
        if phase!='prefix':reads.append([address,width])
    def write(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(width*8))-1)]
        if phase=='prefix':prefix.append(row)
        else:writes.append([machine.reg_read(UC_ARM_REG_PC),*row])
    def invalid(machine,access,address,width,value,user):
        faults.append(dict(kind=access,address=hex(address),width=width,pc=hex(machine.reg_read(UC_ARM_REG_PC))));return False
    def interrupt(machine,number,user):raise ValueError('WStart reached unsupported BIOS/exception interrupt '+str(number))
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_INVALID,invalid);cpu.hook_add(UC_HOOK_INTR,interrupt);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0xf000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    outside=[r for r in prefix if not STACK<=r[0]<STACK+0x4000]
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or prefix_fill[0]!=1 or outside!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]:raise ValueError('WStart actual incoming-pointer producer/clear changed')
    for off,value in[(0x350,case['mode']),(0x352,case.get('power',0)),(0x3b2,case.get('beaconPeriod',100)),(0x334,case.get('wep',0)),(0x33a,4 if case.get('shortPreamble')else 0),(0x690,case.get('operation',0)),(0x322,case.get('maxSta',1)),(0x3a8,case.get('bssid',0))]:cpu.mem_write(context+off,struct.pack('<H',value))
    for off,value in[(0x30c,case.get('dmaChannel',4)),(0x310,case.get('dmaMaxCount',0x400)),(0x31c,DATA+0x2000)]:cpu.mem_write(context+off,struct.pack('<I',value))
    if case.get('initializeLists'):
        for offset in range(392,572,12):cpu.mem_write(context+offset,struct.pack('<IIHH',0xffffffff,0xffffffff,0,0))
    cpu.mem_write(0x0480819c,struct.pack('<H',case.get('signal',0x80)));cpu.mem_write(0x04808044,struct.pack('<H',case.get('sequence',0x1234)));cpu.mem_write(0x048080f8,struct.pack('<Q',case.get('tsf',0)))
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x3800,STOP|(index&1)]
    cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|0x13|((index%4)<<6))
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    phase='target';error=None
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except(UcError,ValueError)as exc:error=dict(type=type(exc).__name__,message=str(exc))
    if not returned[0]:
        return dict(case=case,actualOwnReturn=False,actualOwnReturnCredit=0,unsupported=True,error=error,instructions=len(pcs),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),faults=faults,tail=[(hex(a),b,c)for a,b,c in tail],providers=[],postFaultStateCredit=0,sourceCredit=0)
    own=[r for r in writes if TOP<=r[0]<TOP+CODE];own_hardware=[r[1:]for r in own if 0x04808000<=r[1]<0x04809000];expected_hardware=hardware_model(case)
    cap=[r for r in own if r[1]==context+0x3c0];sync=[r for r in own if r[1]==context+0x356];expected_cap=1|(0x20 if case.get('shortPreamble')else 0)|(0x10 if case.get('wep',0)else 0)
    sequence=['WStop','RND_init','InitCAM','InitApList','InitTxCtrl','InitRxCtrl']
    mode=case['mode']
    if mode==1:sequence+=['_ll_udiv','WSetStaState','StartBeaconFrame']
    elif mode in(2,3,4):sequence+=['WSetStaState']
    sequence+=['WDisableTmpttPowerSave']
    if case.get('power',0)==1:sequence+=['WSetPowerState']
    sequence+=['WaitLoop_Rxpe']
    argument_checks=[]
    for frame in direct:
        name=frame['name'];args=frame['arguments']
        if name=='RND_init':
            value=case.get('sequence',0x1234);argument_checks.append(args[:2]==[(value+(value<<8))&0xffffffff,value])
        elif name=='WSetStaState':argument_checks.append(args[0]==(0x40 if mode==1 else 0x20))
        elif name=='WSetPowerState':argument_checks.append(args[0]==2)
        elif name=='_ll_udiv':
            divisor=case.get('beaconPeriod',100)*1024;value=case.get('tsf',0);quotient=unsigned_quotient(value,divisor)
            argument_checks.append(args==[value&0xffffffff,value>>32,divisor,0]and frame['result'][:2]==[quotient&0xffffffff,quotient>>32])
    checks=dict(orderedOwnHardware=own_hardware==expected_hardware,ownCapability=bool(cap)and cap[-1][2:]==[2,expected_cap],ownSynchronization=bool(sync)and all(r[2:]==[2,0]for r in sync),directCallOrder=[r['name']for r in direct]==sequence,directAbi=all(r['calleeSavedPreserved']and r['actualReturn']for r in direct),specifiedCallArguments=all(argument_checks),ownContextStores=all(r[1]in(context+0x3c0,context+0x356)for r in own if DATA<=r[1]<DATA+0x10000))
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,directNativeReturns=direct,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),instructions=len(pcs),visited=sorted({r[0]for r in pcs}),orderedReads=reads,orderedWrites=writes,ownWrites=[r for r in writes if TOP<=r[0]<TOP+SIZE],memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providers=[],actualOriginalFillReturns=1,constructorActualReturnCredit=0,staticMappedHardwareNoTransferSemantics=True,sceneAndDeviceReachabilityUnproved=True,sourceCredit=0)


def hardware_model(case):
    result=[]
    def store(offset,value):result.append([0x04808000+offset,2,value&65535])
    for off,value in[(0x32,0x8000),(0x134,65535),(0x2a,0),(0x28,0),(0x38,15),(0x30,0x8000),(0x10,65535),(0x1ae,0x1fff),(0x1aa,0x400 if case.get('operation',0)&8 else 0),(8,0),(10,0)]:store(off,value)
    mode=case['mode']
    if mode==0:
        for off,value in[(0x12,0x3f),(0xd0,65535),(0xe0,8),(8,0),(10,0),(0xe8,0),(4,1)]:store(off,value)
    elif mode==1:
        for off,value in[(0x12,0x703f),(0x1ae,0x1fff),(0xd0,0x301),(0xe0,0xd),(8,0xe000),(4,1)]:store(off,value)
        period=case.get('beaconPeriod',100)*1024;value=((unsigned_quotient(case.get('tsf',0),period)+1)*period)&0xffffffffffffffff
        for off,shift in[(0xf6,48),(0xf4,32),(0xf2,16),(0xf0,0)]:store(off,(value>>shift)|(1 if off==0xf0 else 0))
        store(0xe8,1);store(0xea,1);store(0xae,2)
    elif mode==2:
        store(0x12,0xe0bf)
        if case.get('operation',0)&0x20:store(0x12,0xe0ff);store(0x1aa,(0x400 if case.get('operation',0)&8 else 0)|0x68)
        for off,value in[(0xd0,0x181|(0x400 if case.get('bssid',0)&1 else 0)),(0xe0,0xb),(4,1),(0xe8,1),(0xea,1)]:store(off,value)
    elif mode==3:
        for off,value in[(0x10,65535),(0x12,0xc03f),(0xd0,1|(0x400 if case.get('bssid',0)&1 else 0)),(0xe0,0xb),(4,1),(0xe8,1),(0xea,1),(0x48,0)]:store(off,value)
    elif mode==4:
        for off,value in[(0x12,0),(0x1ae,0),(4,1)]:store(off,value)
    store(0x48,0);store(0xae,2);return result


def unsigned_quotient(numerator,denominator):
    return numerator//denominator if denominator else numerator
