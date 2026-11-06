import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
MAIN=0x027e0000
WRAM=0x037f8000
DATA=0x023c0000
STACK=0x03030000
IO=0x04808000
STOP=0x0f000000
POINTER=0x0380fff4
CTOR=0x027e89ec
PREFIX_STOP=0x027e8a10
FILL=0x037fe014
TOPS={0x027ea584:(76,72)}
FUNCTIONS=dict(TOPS)
FRAMES={}
NAMES={}


def cases(entry=0x027ea584):
    result=[dict(mode=mode,flags=flags,contextOffset=(0x40,0x800)[i%2])for i,(mode,flags)in enumerate(itertools.product((0,1,2,32767,32768,65535),(0,1,2,3,32767,32768,32769,65535)))]
    rng=random.Random(0xa584)
    for i in range(128):result.append(dict(mode=rng.getrandbits(16),flags=rng.getrandbits(16),contextOffset=(0x40,0x800)[i%2]))
    return result


def run(main,wram,entry,body,case,index,wrong_pointer=False,wrong_descriptor=False,budget=250000):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),IO:rng.randbytes(4096),STOP:bytes(4096)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    cpu.mem_write(entry,body);context=DATA+case['contextOffset'];descriptor=DATA+0x7000;cpu.mem_write(descriptor,struct.pack('<I',context+(0x3000 if wrong_descriptor else 0)));phase='prefix';visited=[];writes=[];reads=[];prefix_visited=[];returned=False;helpers=[];active=[];frames=[];expected_stack=None;wait_call=-1;waits=[];current_wait=None;prefix_writes=[]
    def code(machine,pc,width,user):
        nonlocal returned,wait_call,current_wait
        if phase=='prefix':
            if not(CTOR<=pc<PREFIX_STOP or FILL<=pc<FILL+92)or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('Producer prefix escaped original ARM constructor/fill bounds')
            prefix_visited.append(pc);return
        if pc==STOP:
            if active:raise ValueError('Owned return retained unfinished native helper')
            returned=True;machine.emu_stop();return
        while active and active[-1]['lr']==pc and active[-1]['sp']==machine.reg_read(REGISTERS[-2]):
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),abiPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item['saved']);helpers.append(item)
        matched=[start for start,(size,code_bytes)in FUNCTIONS.items()if start<=pc<start+code_bytes]
        if len(matched)!=1 or pc%4 or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('State routine fetched outside complete original/owned ARM code or into pool')
        start=matched[0];visited.append(pc)
        if pc==start and start in FRAMES:
            sp=machine.reg_read(REGISTERS[-2]);saved=FRAMES[start];base=sp-4*len(saved)
            for i,register in enumerate(saved):
                value=machine.reg_read(REGISTERS[register]);frames.append([base+4*i,4,value]);struct.pack_into('<I',expected_stack,base-STACK+4*i,value)
        if pc in NAMES:
            item=dict(entry=hex(pc),identity=NAMES[pc],lr=machine.reg_read(REGISTERS[-1])&~1,sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(r)for r in REGISTERS[4:12]],incoming=[machine.reg_read(r)for r in REGISTERS[:4]],sourceCredit=0,tailOverlap=pc==0x037fb454);active.append(item)
        if pc in(0x037fb420,0x037fb454):
            if pc==0x037fb420:wait_call+=1;busy=case['waits'][wait_call];port=IO+0x15e
            else:busy=case['gapBusy'];port=IO+0x180
            current_wait=dict(entry=hex(pc),port=port,busy=busy,values=[]);waits.append(current_wait)
    def store(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(8*width))-1)]
        if phase=='prefix':prefix_writes.append(row);return
        if not(any(base<=address and address+width<=base+len(raw)for base,raw in regions.items()if base in(DATA,STACK,IO))):raise ValueError('State routine wrote outside bounded context/frame/ports')
        writes.append(row)
    def load(machine,access,address,width,value,user):
        if phase=='prefix':return
        reads.append([address,width])
        if current_wait is not None and address==current_wait['port']and width==2:
            busy=current_wait['busy'];values=current_wait['values'];word=(case['sticky']&~1)|(1 if busy is None or len(values)<busy else 0);values.append(word);machine.mem_write(address,struct.pack('<H',word));return
        if address==POINTER and width==4:return
        if any(start+code_bytes<=address and address+width<=start+size and width==4 for start,(size,code_bytes)in FUNCTIONS.items()):return
        if DATA<=address and address+width<=DATA+0x8000 and width in(1,2,4):return
        if STACK<=address and address+width<=STACK+0x4000 and width==4:return
        if entry==0x027e9c58 and address==IO+6 and width==2:return
        if entry==0x027e9d00 and address==IO+0x15c and width==2:return
        raise ValueError('State routine read outside measured original pools/context/frame/ports')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.hook_add(UC_HOOK_MEM_READ,load);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],descriptor);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(CTOR,PREFIX_STOP,count=10000)
    expected_prefix=[[POINTER,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)];nonstack=[x for x in prefix_writes if not STACK<=x[0]<STACK+0x4000]
    if nonstack!=expected_prefix or cpu.reg_read(UC_ARM_REG_PC)!=PREFIX_STOP or prefix_visited[-1]!=FILL+88 or cpu.reg_read(REGISTERS[-1])!=PREFIX_STOP or struct.unpack('<I',cpu.mem_read(POINTER,4))[0]!=context:raise ValueError('Actual descriptor/producer pointer write, clear or natural fill-return boundary differs')
    for off,value in((0x330,case['mode']),(0x3a4,case['flags'])):cpu.mem_write(context+off,struct.pack('<H',value))
    expected={base:bytearray(cpu.mem_read(base,len(raw)))for base,raw in regions.items()};expected_stack=expected[STACK]
    if wrong_pointer:cpu.mem_write(DATA+0x3000,bytes(cpu.mem_read(context,0x694)));cpu.mem_write(POINTER,struct.pack('<I',DATA+0x3000))
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x3800,STOP|(index&1)];mode=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase='target';cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:raise ValueError('State entry did not actually return within bounded supported native context')
    expected_nonstack=[];expected_helpers=[]
    def expect_store(address,width,value):
        expected_nonstack.append([address,width,value&((1<<(width*8))-1)])
        base=next(b for b,raw in expected.items()if b<=address and address+width<=b+len(raw));expected[base][address-base:address-base+width]=int(value&((1<<(width*8))-1)).to_bytes(width,'little')
    result=10 if case['mode']==1 or(case['mode']==0 and case['flags']&1)else 20
    flags=(2 if case['flags']&1 else 6)if case['mode']==0 else 6 if case['mode']==1 else 2
    abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;actual_nonstack=[x for x in writes if not STACK<=x[0]<STACK+0x4000];actual_frames=[x for x in writes if STACK<=x[0]<STACK+0x4000];helper_entries=sorted(int(x['entry'],0)for x in helpers);checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==flags,nonstackWrites=actual_nonstack==expected_nonstack,frames=actual_frames==frames,helpers=helper_entries==sorted(expected_helpers),helperAbi=all(x['abiPreserved']for x in helpers),memory=all(bytes(cpu.mem_read(base,len(raw)))==bytes(raw)for base,raw in expected.items()),producerPointerPreserved=struct.unpack('<I',cpu.mem_read(POINTER,4))[0]==context)
    checks['leafScratchContract']=cpu.reg_read(REGISTERS[1])==case['mode']and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(2,13))
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,orderedReads=reads,helpers=helpers,scopedHelperReturnEvents=len(helpers),overlappingTailHelperEvents=sum(x['tailOverlap']for x in helpers),waits=waits,visited=sorted(set(visited)),instructionCount=len(visited),regionHashes={hex(base):hashlib.sha256(cpu.mem_read(base,len(raw))).hexdigest()for base,raw in expected.items()},producer=dict(actualFillReturn=True,constructorActualReturn=False,descriptorWord0=context,storage=POINTER,clearBytes=0x694,prefixInstructions=len(prefix_visited),orderedNonstackWriteSha256=hashlib.sha256(repr(nonstack).encode()).hexdigest()),contextOverride=case,wrongPointerControl=wrong_pointer,providers=[],physicalHardwareOrSceneContextProven=False)
