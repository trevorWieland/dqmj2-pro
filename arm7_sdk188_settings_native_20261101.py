import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS

MAIN,WRAM,DATA,STACK,IO,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04808000,0x0f000000,0x0380fff4
WEP,PREAMBLE=0x027e8ff0,0x027e929c
FUNCTIONS={WEP:(160,148),PREAMBLE:(168,160),0x027e9bd8:(128,116),0x027f4e1c:(96,92),0x027ea584:(76,72),0x027ead30:(44,44),0x027ead5c:(28,28)}

def cases(entry):
    if entry==WEP:
        raw=[dict(argument=a,sta=s,cap=c,frame=f,io=v)for a,s,c,f,v in itertools.product((0,1,2,3,4,65535),(0,0x40,0xffff),(0,65535,0xa5a5),(0,65535),(0,65535))]
    elif entry==PREAMBLE:
        raw=[dict(argument=a,sta=s,configMode=m,cap=c,io=v,rateMode=r,rateBits=b)for a,s,m,c,v,r,b in itertools.product((0,1,2,65535),(0,0x40,0xffff),(0,1,3),(0,65535),(0,65535),(0,1,2),(0,1))]
    else:raise ValueError('Unknown settings entry')
    for bit in range(16):
        for argument in(0,1):raw.append(dict(argument=argument,sta=0x40,configMode=1,cap=1<<bit,frame=1<<bit,io=1<<bit,rateMode=0,rateBits=1<<bit))
    for index,row in enumerate(raw):row.update(contextOffset=(0,4,0x100)[index%3],sourceEnabled=index%2,inputHalfword=(0,1,0xffff,0x1234)[index%4],beaconInitial=(index*37)&65535)
    return raw

def run(main,wram,entry,case,index,bodies=None,budget=20000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original settings module hashes differ')
    main=bytearray(main)
    for address,body in(bodies or{}).items():
        if address not in(WEP,PREAMBLE)or len(body)!=FUNCTIONS[address][0]:raise ValueError('Settings source-linked extent differs')
        main[address-MAIN:address-MAIN+len(body)]=body
    rng=random.Random(0x188000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:bytes(main)+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),IO:rng.randbytes(0x1000),STOP:bytes(0x1000)}
    for base,raw in regions.items():cpu.mem_map(base,len(raw));cpu.mem_write(base,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';prefix=[];reads=[];writes=[];visited=[];active=[];helpers=[];returned=[False];fills=[0]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Settings native descriptor prefix escaped')
            if pc==0x037fe014:fills[0]+=1
            return
        if pc==STOP:
            if active:raise ValueError('Settings returned with unfinished native callees')
            returned[0]=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),abiPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item.pop('saved'));helpers.append(item)
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not any(start<=pc<start+length for start,(extent,length)in FUNCTIONS.items()):raise ValueError('Settings fetched outside exact ARM code scopes')
        visited.append(pc)
        if pc in FUNCTIONS and pc!=entry:active.append(dict(entry=hex(pc),lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),incoming=[machine.reg_read(r)for r in REGISTERS[:4]],saved=[machine.reg_read(r)for r in REGISTERS[4:12]],sourceCredit=0))
    def write(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(8*width))-1)]
        if phase=='prefix':prefix.append(row);return
        allowed=STACK<=address and address+width<=STACK+0x4000 and width in(2,4)or address in(context+0x334,context+0x33a,context+0x3c0,context+0x3ce,DATA+0x402e,IO+6,IO+0xbc,IO+0x140)and width==2
        if not allowed:raise ValueError('Settings store outside measured fields/beacon/ports/private frames')
        writes.append(row)
    def read(machine,access,address,width,value,user):
        if phase=='prefix':return
        reads.append([address,width])
        if address==WORD and width==4:return
        if any(start+length<=address and address+width<=start+extent and width==4 for start,(extent,length)in FUNCTIONS.items()):return
        if DATA<=address and address+width<=DATA+0x8000 and width in(1,2,4):return
        if STACK<=address and address+width<=STACK+0x4000 and width in(2,4):return
        if address in(IO+6,IO+0xbc)and width==2:return
        raise ValueError('Settings read outside measured source state/pools/ports/frame')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    nonstack=[r for r in prefix if not STACK<=r[0]<STACK+0x4000]
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or fills[0]!=1 or nonstack!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]:raise ValueError('Actual settings descriptor producer/fill differs')
    halfwords={0x32e:case.get('configMode',0),0x330:case.get('rateMode',0),0x334:0x55aa,0x33a:0xa5a5,0x34c:case['sta'],0x3c0:case['cap'],0x3ce:case.get('frame',0),0x3a4:case.get('rateBits',0)}
    for offset,value in halfwords.items():cpu.mem_write(context+offset,struct.pack('<H',value))
    cpu.mem_write(context+0x4ac,struct.pack('<I',0 if case.get('missingBeacon')else DATA+0x4000));cpu.mem_write(DATA+0x402e,struct.pack('<H',case['beaconInitial']));cpu.mem_write(IO+6,struct.pack('<H',case['io']));cpu.mem_write(IO+0xbc,struct.pack('<H',case['io']));cpu.mem_write(context+0x318,struct.pack('<I',DATA+0x2000 if case['sourceEnabled']else 0));cpu.mem_write(DATA+0x202e,struct.pack('<H',case['inputHalfword']))
    expected={base:bytearray(cpu.mem_read(base,len(raw)))for base,raw in regions.items()};expected_writes=[];argument=case['argument'];valid=argument<=(3 if entry==WEP else 1)
    def effect(address,value):
        value&=65535;expected_writes.append([address,2,value]);base=DATA if DATA<=address<DATA+0x8000 else IO;struct.pack_into('<H',expected[base],address-base,value)
    if valid:
        if entry==WEP:
            cap=(case['cap']|16)if argument else(case['cap']&~16);effect(context+0x334,argument);effect(context+0x3c0,cap);effect(context+0x3ce,(case.get('frame',0)|0x4000)if argument else(case.get('frame',0)&~0x4000))
            if case['sta']==0x40 and argument==1:effect(DATA+0x402e,cap)
            effect(IO+6,(case['io']&~0x38)|((argument or 1)<<3))
        else:
            effect(context+0x33a,(0xa5a5&~4)|(argument<<2));cap=(case['cap']|32)if argument else(case['cap']&~32);effect(context+0x3c0,cap)
            if case['sta']==0x40 and case.get('configMode',0)==1:effect(DATA+0x402e,cap)
            preamble=(case['io']|6)if argument else(case['io']&~6);effect(IO+0xbc,preamble);timestamp=(case['inputHalfword']if case['sourceEnabled']else 0xe2e2)+0x202;rate=10 if case.get('rateMode',0)==1 or case.get('rateMode',0)==0 and case.get('rateBits',0)&1 else 20
            if rate==20:
                timestamp-=0x6161
                if preamble&2:timestamp-=0x6060
            effect(IO+0x140,timestamp)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=argument;initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpsr=((index%16)<<28)|0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    phase='target';cpu.emu_start(entry,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Settings source entry failed to return within instruction bound')
    checks=dict(returnValue=cpu.reg_read(REGISTERS[0])==(0 if valid else 5),calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),armThumbReturn=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1),orderedNonstackWrites=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==expected_writes,allNonstackMemory=all(cpu.mem_read(base,len(raw))==bytes(raw)for base,raw in expected.items()if base!=STACK),helperAbi=all(h['abiPreserved']for h in helpers),helperEntry=(len(helpers)==0)if entry==WEP or not valid else(any(h['entry']=='0x27e9bd8'for h in helpers)),runtimeWord=int.from_bytes(cpu.mem_read(WORD,4),'little')==context)
    return dict(case=case,entry=hex(entry),actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,rawReturn=cpu.reg_read(REGISTERS[0]),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,helpers=helpers,actualNativeHelperReturns=len(helpers),visited=sorted(set(visited)),instructions=len(visited),producer=dict(actualFillReturns=1,constructorActualReturns=0,descriptorWord0=context,clearBytes=0x694),memorySha256={hex(base):hashlib.sha256(cpu.mem_read(base,len(raw))).hexdigest()for base,raw in regions.items()},providers=[],syntheticBeaconAndMappedRegisterPrerequisites=True,physicalHardwareConcurrencyFrameValidityAndSceneReachabilityUnproved=True)
