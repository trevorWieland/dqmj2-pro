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
TOPS={0x027e9c58:(104,96),0x027e9d00:(136,104)}
FUNCTIONS={**TOPS,0x027e91bc:(176,168),0x027ead30:(44,44),0x027ea62c:(32,24),0x027ea5fc:(48,44),0x037fb420:(52,48),0x037fb454:(52,48)}
FRAMES={0x027e9c58:(3,14),0x027e9d00:(3,14),0x027e91bc:(3,4,5,14),0x027ea5fc:(3,14)}
NAMES={0x027e91bc:'main:ARM027E91BC',0x027ead30:'main:ARM027EAD30',0x027ea62c:'main:ARM027EA62C',0x027ea5fc:'main:ARM027EA5FC',0x037fb420:'wram:ARM037FB420',0x037fb454:'wram:ARM037FB454-gap-zero-credit'}


def cases(entry):
    if entry==0x027e9c58:
        return [dict(value=v,mode=m,payload=p,active=a,packetOffset=i&1,csr=(0,1,0x40,0x8000,0xffff)[i%5],contextOffset=(0x40,0x800)[i%2])for i,(v,m,p,a)in enumerate(itertools.product((0,1,2,65535,65536,0x80000000,0xffffffff,0x10001),(0,1,2,65535),(0,9,10,0x1234,65535),(0,1)))]
    pairs=((0,0),(1,3),(3,1),(None,0),(0,None),(None,None),(10239,10240))
    return [dict(state=s,ioData=v,waits=list(pair),gapBusy=(0,2,None,10239)[i%4],sticky=(0xfffe,0x8000,0x4000)[i%3],contextOffset=(0x40,0x800)[i%2])for i,(s,v,pair)in enumerate(itertools.product((0,1,2,65535),(0,1,0x3f,0x8000,65535,0x1234),pairs))]


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
    if entry==0x027e9c58:
        for off,value in((0x32e,case['mode']),(0x33c,case['payload']),(0x4a4,case['active']),(0x3da,case['packetOffset'])):cpu.mem_write(context+off,struct.pack('<H',value))
        cpu.mem_write(context+0x4ac,struct.pack('<I',DATA+0x2000));cpu.mem_write(IO+6,struct.pack('<H',case['csr']))
    else:cpu.mem_write(context+0x5f8,struct.pack('<H',case['state']));cpu.mem_write(IO+0x15c,struct.pack('<H',case['ioData']))
    expected={base:bytearray(cpu.mem_read(base,len(raw)))for base,raw in regions.items()};expected_stack=expected[STACK]
    if wrong_pointer:cpu.mem_write(DATA+0x3000,bytes(cpu.mem_read(context,0x694)));cpu.mem_write(POINTER,struct.pack('<I',DATA+0x3000))
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['value']if entry==0x027e9c58 else rng.getrandbits(32);initial[-2:]=[STACK+0x3800,STOP|(index&1)];mode=0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,((index%16)<<28)|mode)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase='target';cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:raise ValueError('State entry did not actually return within bounded supported native context')
    expected_nonstack=[];expected_helpers=[]
    def expect_store(address,width,value):
        expected_nonstack.append([address,width,value&((1<<(width*8))-1)])
        base=next(b for b,raw in expected.items()if b<=address and address+width<=b+len(raw));expected[base][address-base:address-base+width]=int(value&((1<<(width*8))-1)).to_bytes(width,'little')
    if entry==0x027e9c58:
        value=case['value'];low=value&65535;call=not(value!=0 and case['mode']!=1);expect_store(context+0x352,2,low);expect_store(IO+6,2,(case['csr']&~0x40)if call else(case['csr']|0x40));result=0
        if call:
            expected_helpers.append(0x027e91bc)
            if case['payload']>=10:
                expect_store(context+0x33c,2,case['payload'])
                if case['active']:
                    pair=[case['payload']&255,case['payload']>>8]if low==1 else[255,255];start=DATA+0x2024+case['packetOffset']+6
                    for i,byte in enumerate(pair):
                        address=start+i;aligned=address&~1;old=struct.unpack_from('<H',expected[DATA],aligned-DATA)[0];new=(old&255)|(byte<<8)if address&1 else(old&0xff00)|byte;expect_store(aligned,2,new);expected_helpers.append(0x027ead30)
                    flags=(2 if low>=1 else 0)|(4 if case['packetOffset']else 0)
                else:flags=6
            else:flags=8
        else:flags=8 if case['mode']==0 else 2
    else:
        def expected_wait(port,busy):
            clear=busy is not None and busy<10240;count=busy+1 if clear else 10240;values=[(case['sticky']&~1)|1]*(count-1)+[(case['sticky']&~1)if clear else(case['sticky']|1)];struct.pack_into('<H',expected[IO],port-IO,values[-1]);return values,0 if clear else 1
        expected_waits=[]
        if case['state']==2:expect_store(IO+0x17e,2,0xc008);expect_store(IO+0x17c,2,0);values,unused=expected_wait(IO+0x180,case['gapBusy']);expected_waits.append((IO+0x180,values));expected_helpers.extend((0x027ea62c,0x037fb454))
        expect_store(IO+0x158,2,0x601e);values,unused=expected_wait(IO+0x15e,case['waits'][0]);expected_waits.append((IO+0x15e,values));expected_helpers.append(0x037fb420);expect_store(IO+0x15a,2,case['ioData']|0x3f);expect_store(IO+0x158,2,0x501e);values,last_result=expected_wait(IO+0x15e,case['waits'][1]);expected_waits.append((IO+0x15e,values));expected_helpers.extend((0x027ea5fc,0x037fb420));expect_store(IO+0x168,2,0x800d);expect_store(IO+0x36,2,1);result=IO+0x36;flags=6 if last_result==0 else 2
    abi=all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;actual_nonstack=[x for x in writes if not STACK<=x[0]<STACK+0x4000];actual_frames=[x for x in writes if STACK<=x[0]<STACK+0x4000];helper_entries=sorted(int(x['entry'],0)for x in helpers);checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==result,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==flags,nonstackWrites=actual_nonstack==expected_nonstack,frames=actual_frames==frames,helpers=helper_entries==sorted(expected_helpers),helperAbi=all(x['abiPreserved']for x in helpers),memory=all(bytes(cpu.mem_read(base,len(raw)))==bytes(raw)for base,raw in expected.items()),producerPointerPreserved=struct.unpack('<I',cpu.mem_read(POINTER,4))[0]==context)
    if entry==0x027e9d00:checks['waitInputs']=[(x['port'],x['values'])for x in waits]==expected_waits
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedWrites=writes,orderedReads=reads,helpers=helpers,scopedHelperReturnEvents=len(helpers),overlappingTailHelperEvents=sum(x['tailOverlap']for x in helpers),waits=waits,visited=sorted(set(visited)),instructionCount=len(visited),regionHashes={hex(base):hashlib.sha256(cpu.mem_read(base,len(raw))).hexdigest()for base,raw in expected.items()},producer=dict(actualFillReturn=True,constructorActualReturn=False,descriptorWord0=context,storage=POINTER,clearBytes=0x694,prefixInstructions=len(prefix_visited),orderedNonstackWriteSha256=hashlib.sha256(repr(nonstack).encode()).hexdigest()),contextOverride=case,wrongPointerControl=wrong_pointer,providers=[],physicalHardwareOrSceneContextProven=False)
