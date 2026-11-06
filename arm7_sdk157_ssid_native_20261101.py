import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
MAIN,WRAM,DATA,STACK,IO,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04808000,0x0f000000,0x0380fff4
TOP,READ,WRITE=0x027ea3b0,0x027ead5c,0x027ead30
FUNCTIONS={TOP:(208,204),READ:(28,28),WRITE:(44,44)}
def cases():
    base=[dict(length=length,storedLength=stored,mlme=state,mismatch=mode,alias=alias,contextOffset=(0,4,0x100)[(length+stored)%3])for length,stored,state,mode,alias in itertools.product((0,1,2,15,31,32,33,65535),(0,1,2,31,32,33,65535),(0,0x13),('none','first','last','masked'),('external','stored'))]
    extra=[dict(length=32,storedLength=32,mlme=0x13,mismatch='first',alias='external',contextOffset=(i%2)*4,maskValue=i)for i in range(256)]
    return base+extra+[dict(length=33,storedLength=1,mlme=0,mismatch='none',alias='external',contextOffset=0,invalidInputPointer=True),dict(length=0,storedLength=0,mlme=0,mismatch='none',alias='external',contextOffset=0,invalidInputPointer=True)]
def run(main,wram,case,index,bodies=None,budget=20000):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original host ARM7 main/WRAM input hashes differ')
    main=bytearray(main)
    for address,body in(bodies or{}).items():
        if address not in FUNCTIONS or len(body)!=FUNCTIONS[address][0]:raise ValueError('SSID compiled closure extent differs')
        main[address-MAIN:address-MAIN+len(body)]=body
    main=bytes(main);rng=random.Random(0x157000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),IO:rng.randbytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';prefix=[];reads=[];writes=[];visited=[];active=[];helpers=[];returned=[False];fill=[0]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('SSID producer escaped original prefix/fill')
            if pc==0x037fe014:fill[0]+=1
            return
        if pc==STOP:
            if active:raise ValueError('SSID returned with unfinished byte helper')
            returned[0]=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            helper=active.pop();helper.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]));helpers.append(helper)
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not any(a<=pc<a+size for a,(extent,size)in FUNCTIONS.items()if a!=WRITE):raise ValueError('SSID fetched outside qualified ARM code')
        visited.append(pc)
        if pc==READ:active.append(dict(entry=hex(READ),lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),argument=machine.reg_read(REGISTERS[0])))
    def write(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(8*width))-1)]
        if phase=='prefix':prefix.append(row);return
        if not STACK<=address<STACK+0x4000 or width!=4:raise ValueError('SSID predicate wrote outside its private frame')
        writes.append(row)
    def read(machine,access,address,width,value,user):
        if phase=='prefix':return
        if not(address==WORD and width==4 or address==TOP+204 and width==4 or DATA<=address and address+width<=DATA+0x8000 and width in(1,2,4)or STACK<=address and address+width<=STACK+0x4000 and width==4):raise ValueError('SSID read outside qualified word/pool/fields/buffers/frame')
        reads.append([address,width])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    outside=[r for r in prefix if not STACK<=r[0]<STACK+0x4000]
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or outside!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]or fill[0]!=1:raise ValueError('SSID actual pointer producer/fill/clear differs')
    cpu.mem_write(context+0x362,struct.pack('<H',case['storedLength']));cpu.mem_write(context+0x404,struct.pack('<H',case['mlme']))
    stored=bytearray((i*37+index)&255 for i in range(32));mask=bytearray([case.get('maskValue',0)]*32);requested=bytearray(stored)
    if case['mismatch']in('first','masked'):requested[0]^=0x40
    if case['mismatch']=='last':requested[31]^=0x40
    if case['mismatch']=='masked':mask[0]|=0x40
    cpu.mem_write(context+0x364,bytes(stored));cpu.mem_write(context+0x384,bytes(mask));cpu.mem_write(DATA+0x5000+(index&1),bytes(requested))
    pointer=context+0x364 if case['alias']=='stored'else DATA+0x5000+(index&1)
    if case.get('invalidInputPointer'):pointer=0
    expected_memory={address:bytes(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};length=case['length'];stored_length=case['storedLength'];expected=0
    if length<=32:
        if stored_length==0:expected=1
        elif case['mlme']==0x13 and length>=stored_length or case['mlme']!=0x13 and length==stored_length:
            count=stored_length if case['mlme']==0x13 else length
            a=bytes(cpu.mem_read(pointer,count))if pointer else bytes(count);b=bytes(cpu.mem_read(context+0x364,count));m=bytes(cpu.mem_read(context+0x384,count));expected=int(all((x|z)==(y|z)for x,y,z in zip(a,b,m)))
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0:2]=[length,pointer];initial[-2:]=[STACK+0x3800,STOP|(index&1)]
    cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|0x13|((index%4)<<6))
    for reg,value in zip(REGISTERS,initial):cpu.reg_write(reg,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    phase='target';cpu.emu_start(TOP,STOP+4,count=budget)
    if not returned[0]:raise ValueError('SSID entry did not actually return within budget')
    checks=dict(returnValue=cpu.reg_read(REGISTERS[0])==expected,nonstackPreserved=all(bytes(cpu.mem_read(address,len(raw)))==expected_memory[address]for address,raw in regions.items()if address!=STACK),calleeSaved=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in list(range(4,12))+[13,14]),helperReturnValues=all(h['result']==cpu.mem_read(h['argument'],1)[0]for h in helpers),noProviders=True)
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,expectedReturn=expected,rawReturn=cpu.reg_read(REGISTERS[0]),registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,visited=sorted(set(visited)),instructions=len(visited),helpers=helpers,actualHelperReturns=len(helpers),producer=dict(actualFillReturns=1,constructorActualReturns=0,incomingDescriptor=context,clearBytes=0x694),providers=[],memorySha256={hex(address):hashlib.sha256(cpu.mem_read(address,len(raw))).hexdigest()for address,raw in regions.items()},formalLengthDomain='u16',physicalSceneAndNetworkMeaningUnproved=True)
