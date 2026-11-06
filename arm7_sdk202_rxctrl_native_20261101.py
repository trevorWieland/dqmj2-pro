import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS

MAIN,WRAM,DATA,STACK,MAC,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04804000,0x0f000000,0x0380fff4
TOP,FILL=0x037fb1e0,0x037fdfd0
MODE=0x027e8f3c
PRODUCER={MODE:116,0x027e9c58:96,0x027e91bc:168,0x027ead30:44}
STARTS={0:0x794,1:0x10c4,2:0xbfc,3:0x794}

def cases():return[dict(mode=m,contextOffset=c,rxFill=fill,ioPattern=p)for m,c,fill,p in itertools.product(range(4),(0,4,0x100),(0,0xff,0xa5),(0,0xffff))]

def run(main,wram,case,index,body=None,budget=20000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Current original RX module hashes differ')
    if case['mode']not in STARTS:raise ValueError('RX typed C contract requires original bounded mode0..3 producer')
    if body is not None:
        if len(body)!=288:raise ValueError('RX full source extent differs')
        changed=bytearray(wram);changed[TOP-WRAM:TOP-WRAM+288]=body;wram=bytes(changed)
    rng=random.Random(0x202000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),MAC:case['ioPattern'].to_bytes(2,'little')*0x2800,STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';prefix=[];producer_writes=[];reads=[];writes=[];visited=[];producer_visited=[];helpers=[];active=[];returned=[False];prefix_fills=[0]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('RX incoming descriptor prefix escaped')
            if pc==0x037fe014:prefix_fills[0]+=1
            return
        if pc==STOP:
            if active:raise ValueError('RX scope returned with unfinished native helper')
            returned[0]=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),abiPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved'));helpers.append(item)
        if phase=='mode':
            if size!=4 or not any(start<=pc<start+length for start,length in PRODUCER.items()):raise ValueError('Actual mode producer escaped its qualified ARM scopes')
            producer_visited.append(pc)
            if pc in PRODUCER and pc!=MODE:active.append(dict(entry=hex(pc),phase='mode',lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
            return
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not(TOP<=pc<TOP+248 or FILL<=pc<FILL+28):raise ValueError('RX source fetched outside own ARM code or actual28-byte fill')
        visited.append(pc)
        if pc==FILL:active.append(dict(entry=hex(pc),phase='rx',lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
    def write(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(8*width))-1)]
        if phase=='prefix':prefix.append(row);return
        if phase=='mode':producer_writes.append(row);return
        allowed=STACK<=address and address+width<=STACK+0x4000 and width==4 or context+0x4dc<=address and address+width<=context+0x52c and width in(2,4)or address==context+0x3de and width==2 or MAC<=address and address+width<=MAC+0x5000 and width==2
        if not allowed:raise ValueError('RX store outside measured receive state/size/static ports/private frame')
        writes.append(row)
    def read(machine,access,address,width,value,user):
        if phase!='rx':return
        reads.append([address,width])
        if address==WORD and width==4 or TOP+248<=address and address+width<=TOP+288 and width==4 or DATA<=address and address+width<=DATA+0x8000 and width in(2,4)or STACK<=address and address+width<=STACK+0x4000 and width==4:return
        raise ValueError('RX read outside measured word/mode/own pool/private frame')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or prefix_fills[0]!=1 or[r for r in prefix if not STACK<=r[0]<STACK+0x4000]!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]:raise ValueError('RX original descriptor/fill initialization differs')
    phase='mode';cpu.reg_write(REGISTERS[0],case['mode']);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(MODE,STOP+4,count=10000)
    if not returned[0]or cpu.reg_read(REGISTERS[0])!=0 or cpu.mem_read(context+0x32e,2)!=case['mode'].to_bytes(2,'little')or cpu.mem_read(context+0x350,2)!=case['mode'].to_bytes(2,'little'):raise ValueError('Actual bounded native mode setter did not return/produce the supported state')
    producer_helpers=helpers[:];helpers.clear();cpu.mem_write(context+0x4dc,bytes([case['rxFill']])*0x50);expected={address:bytearray(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};expected_writes=[]
    def effect(address,width,value):
        value&=(1<<(width*8))-1;expected_writes.append([address,width,value]);base=DATA if DATA<=address<DATA+0x8000 else MAC;expected[base][address-base:address-base+width]=value.to_bytes(width,'little')
    for offset in range(0,0x50,4):effect(context+0x4dc+offset,4,0)
    start=STARTS[case['mode']];io=0x04808000
    for address,value in[(io+0x30,0x8000),(io+0x50,0x4000+start),(io+0x56,start//2),(io+0x52,0x5f60),(io+0x5a,start//2),(context+0x4e0,start//2),(context+0x4dc,65535),(context+0x3de,0x1f60-start),(io+0x62,0x5f5e),(io+0x30,0x8001),(io+0x24c,65535),(io+0x24e,65535),(MAC+0x1f70,65535),(MAC+0x1f72,65535),(MAC+0x1f7e,65535),(MAC+0x1f76,65535)]:effect(address,2,value)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    phase='rx';returned[0]=False;cpu.emu_start(TOP,STOP+4,count=budget)
    if not returned[0]:raise ValueError('RX initializer failed actual return within instruction bound')
    checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),allNonstackMemory=all(cpu.mem_read(base,len(raw))==bytes(raw)for base,raw in expected.items()if base!=STACK),orderedNonstackWrites=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==expected_writes,actualFillContract=len(helpers)==1 and helpers[0]['entry']==hex(FILL)and helpers[0]['incoming'][:3]==[0,context+0x4dc,0x50],fillAbi=all(r['abiPreserved']for r in helpers),rawIncidentalR0=cpu.reg_read(REGISTERS[0])==MAC+0x1f70,returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1))
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,visited=sorted(set(visited)),instructions=len(visited),helpers=helpers,actualNestedFillReturns=len(helpers),producer=dict(actualPrefixFillReturns=1,constructorActualReturns=0,actualModeSetterReturns=1,modeSetterHelpers=producer_helpers,visited=sorted(set(producer_visited)),orderedWrites=producer_writes,supportedModeProduced=case['mode']),memorySha256={hex(base):hashlib.sha256(cpu.mem_read(base,len(raw))).hexdigest()for base,raw in regions.items()},providers=[],sourceModeOutside0To3UndefinedAndUnsupported=True,staticMappedWifiAndSyntheticDescriptorContext=True,physicalHardwareAndSceneReachabilityUnproved=True)
