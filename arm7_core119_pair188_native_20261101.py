import hashlib
import itertools
import random
import struct
import match_runtime
import arm7_lane_sdk_division_scope_20261031 as division_scope
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
TOPS={0x027e96ec:(88,80),0x027e9e3c:(100,92)}
FUNCTIONS={**TOPS,0x03806e44:(484,484)}
FRAMES={0x027e96ec:(3,14),0x027e9e3c:(4,5,6,14)}
NAMES={0x027e9e3c:'main:ARM027E9E3C',0x03806e44:'wram:ARM03806E44-u32-division'}


def cases(entry):
    values=(0,1,9,10,11,99,100,127,128,129,999,1000,1001,65535,65536,0x80000000,0xffffffff)if entry==0x027e96ec else(0,1,9,10,6553,6554,65535,65536,65537,0x80000000,0xffffffff)
    others=(0,1,100,6553,6554,51199,51200,51201,65534,65535)if entry==0x027e96ec else(0,1,10,99,100,101,1000,65535)
    result=[dict(value=value,sourceValue=other if entry==0x027e96ec else(0x1111+i)&65535,rate=other if entry==0x027e9e3c else(0,1,100,65535)[i%4],oldOutput=(0x4321+i)&65535,port=(0,1,0x8000,65535)[i%4],contextOffset=(0x40,0x800)[i%2])for i,(value,other)in enumerate(itertools.product(values,others))]
    if entry==0x027e9e3c:
        rng=random.Random(0x9e3c)
        for i in range(64):result.append(dict(value=rng.getrandbits(32),sourceValue=rng.getrandbits(16),rate=rng.getrandbits(16),oldOutput=rng.getrandbits(16),port=rng.getrandbits(16),contextOffset=0x40))
    return result


def cmp_flags(left,right):
    value=(left-right)&0xffffffff
    return ((value>>31)<<3)|(4 if value==0 else 0)|(2 if left>=right else 0)|(1 if((left^right)&(left^value)&0x80000000)else 0)


def run(main,wram,entry,body,case,index,wrong_pointer=False,wrong_descriptor=False,budget=250000):
    division_scope.validate_scope(wram)
    if wram[0x03806e44-WRAM:0x03806e4c-WRAM]!=bytes.fromhex('000051e31eff2f01'):raise ValueError('Original u32 division zero-prefix differs')
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
            item=active.pop();item.update(actualReturn=True,result=machine.reg_read(REGISTERS[0]),secondaryResult=machine.reg_read(REGISTERS[1]),abiPreserved=[machine.reg_read(r)for r in REGISTERS[4:12]]==item['saved']);helpers.append(item)
        matched=[start for start,(size,code_bytes)in FUNCTIONS.items()if start<=pc<start+code_bytes]
        if pc==0x03806e9c or len(matched)!=1 or pc%4 or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('State routine fetched outside complete original/owned ARM code or into pool')
        start=matched[0];visited.append(pc)
        if pc==start and start in FRAMES:
            sp=machine.reg_read(REGISTERS[-2]);saved=FRAMES[start];base=sp-4*len(saved)
            for i,register in enumerate(saved):
                value=machine.reg_read(REGISTERS[register]);frames.append([base+4*i,4,value]);struct.pack_into('<I',expected_stack,base-STACK+4*i,value)
        if pc in NAMES and pc!=entry:
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
        if False:return
        if False:return
        raise ValueError('State routine read outside measured original pools/context/frame/ports')
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,store);cpu.hook_add(UC_HOOK_MEM_READ,load);cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],descriptor);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(CTOR,PREFIX_STOP,count=10000)
    expected_prefix=[[POINTER,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)];nonstack=[x for x in prefix_writes if not STACK<=x[0]<STACK+0x4000]
    if nonstack!=expected_prefix or cpu.reg_read(UC_ARM_REG_PC)!=PREFIX_STOP or prefix_visited[-1]!=FILL+88 or cpu.reg_read(REGISTERS[-1])!=PREFIX_STOP or struct.unpack('<I',cpu.mem_read(POINTER,4))[0]!=context:raise ValueError('Actual descriptor/producer pointer write, clear or natural fill-return boundary differs')
    for off,value in((0x338,case['sourceValue']),(0x3b2,case['rate']),(0x3d0,case['oldOutput'])):cpu.mem_write(context+off,struct.pack('<H',value))
    cpu.mem_write(IO+0x8c,struct.pack('<H',case['port']))
    expected={base:bytearray(cpu.mem_read(base,len(raw)))for base,raw in regions.items()};expected_stack=expected[STACK]
    if wrong_pointer:cpu.mem_write(DATA+0x3000,bytes(cpu.mem_read(context,0x694)));cpu.mem_write(POINTER,struct.pack('<I',DATA+0x3000))
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['value'];initial[-2:]=[STACK+0x3800,STOP|(index&1)];mode=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase='target';cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:raise ValueError('State entry did not actually return within bounded supported native context')
    expected_nonstack=[];expected_helpers=[]
    def expect_store(address,width,value):
        expected_nonstack.append([address,width,value&((1<<(width*8))-1)])
        base=next(b for b,raw in expected.items()if b<=address and address+width<=b+len(raw));expected[base][address-base:address-base+width]=int(value&((1<<(width*8))-1)).to_bytes(width,'little')
    def expected_update(value,rate):
        if value==65535:expect_store(context+0x338,2,65535);expect_store(context+0x3d0,2,65535);return 0,6
        numerator=(value*rate)&0xffffffff;quotient,remainder=divmod(numerator,100);expected_helpers.append(0x03806e44);division=[x for x in helpers if x['entry']=='0x3806e44']
        if len(division)!=1 or division[0]['incoming'][:2]!=[numerator,100]or division[0]['result']!=quotient or division[0]['secondaryResult']!=remainder:raise ValueError('Actual original division arguments/results differ from independent wrap/u32 quotient/remainder')
        flags=cmp_flags(quotient,65536)
        if quotient>65536:return 5,flags
        expect_store(context+0x338,2,value);expect_store(context+0x3d0,2,quotient);return 0,flags
    value=case['value']
    if entry==0x027e96ec:
        if value<10:result=5;flags=cmp_flags(value,10)
        elif value>1000:result=5;flags=cmp_flags(value,1000)
        else:
            expect_store(context+0x3b2,2,value);expect_store(IO+0x8c,2,value);expected_helpers.append(0x027e9e3c);nested,flags=expected_update(case['sourceValue'],value);result=0
            nested_events=[x for x in helpers if x['entry']=='0x27e9e3c']
            if len(nested_events)!=1 or nested_events[0]['incoming'][0]!=case['sourceValue']or nested_events[0]['result']!=nested:raise ValueError('Native nested update raw argument/result differs')
    else:result,flags=expected_update(value,case['rate'])
    abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;actual_nonstack=[x for x in writes if not STACK<=x[0]<STACK+0x4000];actual_frames=[x for x in writes if STACK<=x[0]<STACK+0x4000];helper_entries=sorted(int(x['entry'],0)for x in helpers);checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==flags,nonstackWrites=actual_nonstack==expected_nonstack,frames=actual_frames==frames,helpers=helper_entries==sorted(expected_helpers),helperAbi=all(x['abiPreserved']for x in helpers),memory=all(bytes(cpu.mem_read(base,len(raw)))==bytes(raw)for base,raw in expected.items()),producerPointerPreserved=struct.unpack('<I',cpu.mem_read(POINTER,4))[0]==context)
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,orderedReads=reads,helpers=helpers,scopedHelperReturnEvents=len(helpers),overlappingTailHelperEvents=sum(x['tailOverlap']for x in helpers),waits=waits,visited=sorted(set(visited)),instructionCount=len(visited),regionHashes={hex(base):hashlib.sha256(cpu.mem_read(base,len(raw))).hexdigest()for base,raw in expected.items()},producer=dict(actualFillReturn=True,constructorActualReturn=False,descriptorWord0=context,storage=POINTER,clearBytes=0x694,prefixInstructions=len(prefix_visited),orderedNonstackWriteSha256=hashlib.sha256(repr(nonstack).encode()).hexdigest()),contextOverride=case,wrongPointerControl=wrong_pointer,providers=[],physicalHardwareOrSceneContextProven=False)
