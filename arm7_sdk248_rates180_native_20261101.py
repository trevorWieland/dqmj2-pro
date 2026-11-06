import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
MAIN,WRAM,DATA,STACK,STOP,TOP=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x0f000000,0x027ea4d0
RATES=(2,4,11,12,18,22,24,36,48,72,96,108)
EXPECTED_TABLE=tuple(RATES.index(i)if i in RATES else 255 for i in range(1,121))

def run(main,wram,case,index,body=None,budget=20000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Measured ARM7 rate-conversion modules differ')
    if case['length']not in range(3):raise ValueError('Declared two-byte SUP_RATE_ELEMENT backing domain0..2 required')
    if struct.unpack_from('<120H',main,0x173c0)!=EXPECTED_TABLE:raise ValueError('Measured entire rate lookup differs from independent twelve-rate map')
    if body is not None:
        if len(body)!=180:raise ValueError('Complete rate-conversion C extent differs')
        main=main[:TOP-MAIN]+body+main[TOP-MAIN+180:]
    rng=random.Random(0x248000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    source=DATA+0x100+case['sourceAlignment'];output=DATA+0x400+case['outputAlignment'];cpu.mem_write(source,bytes([1,case['length'],case['rates'][0],case['rates'][1]]));initial=[rng.getrandbits(32)for r in REGISTERS];initial[0:2]=[0 if case.get('nullSource')else source,0 if case.get('nullOutput')else output];initial[-2:]=[STACK+0x3800,STOP|(index&1)]
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    cpu.reg_write(UC_ARM_REG_CPSR,0x13|((index%4)<<6));before={a:bytes(cpu.mem_read(a,len(raw)))for a,raw in regions.items()};visited=[];writes=[];owned=[];returned=[False];active=[];helpers=[]
    def code(machine,pc,size,user):
        if pc==STOP:
            if active:raise ValueError('Rate converter returned with unfinished native byte reader')
            returned[0]=True;machine.emu_stop();return
        if not MAIN<=pc<MAIN+len(main):raise ValueError('Rate converter escaped measured initialized code')
        if TOP+176<=pc<TOP+180:raise ValueError('Rate converter fetched its lookup literal')
        while active and pc==active[-1]['returnPc']and machine.reg_read(REGISTERS[-2])==active[-1]['sp']:
            row=active.pop();row['actualReturn']=True;row['outgoingR0']=machine.reg_read(REGISTERS[0]);row['calleeSavedPreserved']=[machine.reg_read(r)for r in REGISTERS[4:12]]==row.pop('saved');helpers.append(row)
        if pc==0x027ead5c:active.append(dict(entry=hex(pc),argument=machine.reg_read(REGISTERS[0]),returnPc=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]]))
        visited.append(pc)
    def store(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(width*8))-1)];writes.append(row)
        if TOP<=machine.reg_read(UC_ARM_REG_PC)<TOP+180:owned.append(row)
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store)
    try:cpu.emu_start(TOP,STOP+4,count=budget)
    except Exception as error:return dict(case=case,actualOwnReturn=False,error=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)),postFaultCredit=0,sourceCredit=0)
    if not returned[0]:return dict(case=case,actualOwnReturn=False,error='instruction bound exhausted',postFaultCredit=0,sourceCredit=0)
    basic=support=0;expected=[[output,2,0],[output+2,2,0]]
    for rate in case['rates'][:case['length']]:
        low=rate&127;bit=1<<RATES.index(low)if low in RATES else 0x8000;support|=bit;expected.append([output+2,2,support])
        if rate&128:basic|=bit;expected.append([output,2,basic])
    modeled=bytearray(before[DATA]);modeled[output-DATA:output-DATA+4]=struct.pack('<HH',basic,support);checks=dict(calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),returnMode=bool(cpu.reg_read(UC_ARM_REG_CPSR)&32)==bool(initial[-1]&1),independentFullDataMemory=cpu.mem_read(DATA,len(modeled))==bytes(modeled),independentOrderedNonstackStores=[r for r in writes if not STACK<=r[0]<STACK+0x4000]==expected,actualNativeReaderReturns=len(helpers)==case['length']+1,helperRegisterContracts=all(r['calleeSavedPreserved']for r in helpers))
    return dict(case=case,actualOwnReturn=True,modelChecks=checks,modelPassed=all(checks.values()),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,ownedWrites=owned,visited=sorted(set(visited)),actualNativeHelperReturns=helpers,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providerReplacements=[],sourceCredit=0,originalLookupDataCredit=0,sourceArrayCapacityTwoOnly=True)

def cases():
    vectors=[dict(length=0,rates=[0,255],sourceAlignment=a,outputAlignment=b)for a,b in itertools.product((0,1),(0,2))]
    vectors +=[dict(length=length,rates=[rate,(rate*17+31)&255],sourceAlignment=a,outputAlignment=b)for length,rate,a,b in itertools.product((1,2),range(256),(0,1),(0,2))]
    vectors +=[dict(length=2,rates=list(pair),sourceAlignment=a,outputAlignment=b)for pair,a,b in itertools.product(((2,2),(130,2),(2,130),(0,255),(1,128)),(0,1),(0,2))]
    return vectors
