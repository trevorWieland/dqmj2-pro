import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x0200B97C
DATA=0x02520000
ARC=DATA+0x100
STACK=0x03030000
STOP=0x0F000000
INIT=0x0200BD04
FILL=0x02008D78
OPEN=0x0200BF2C
READ=0x0200C180
CLOSE=0x0200C02C
CALLBACK=0x0200B200
MASK=0xFFFFFFFF


def word(data,offset):return struct.unpack_from('<I',data,offset)[0]


def put(data,offset,value):struct.pack_into('<I',data,offset,value&MASK)


def cases():
    for shift in range(32):
        for a,b in [(0,0),(1,1),(3,5),(31,32),(32,33),(63,64)]:
            need=((a+b+63)&MASK)&~31
            for variant in range(8):
                capacity=[0,need-1,need,need+1,MASK,need,need,need][variant]
                opened=[(False,False),(True,False),(False,True),(True,True)][variant%4]
                results=[(0,0),(MASK,0),(1,0x80000000),(0x7FFFFFFF,MASK)][variant%4]
                yield dict(a=a,b=b,shift=shift,capacity=capacity,opened=opened,results=results,flags=[0,1,4,8,12,MASK,0x80000000,0xA5A5][variant])
    for a,b in [(MASK,0),(0xFFFFFF80,0x100),(0x80000000,0x80000100)]:
        need=((a+b+63)&MASK)&~31
        assert need
        yield dict(a=a,b=b,shift=31,capacity=need-1,opened=(False,False),results=(0,0),flags=0)


def arena(case,tag):
    data=bytearray((i*31+tag*7)&255 for i in range(4096))
    for offset,value in [(0x1C,case['flags']),(0x2C,0xF1234000+tag),(0x30,case['a']),(0x34,0xFEDC8000+tag),(0x38,case['b'])]:put(data,0x100+offset,value)
    return data


def written_bytes(index,length,tag):return bytes((0x31+index*53+tag*11+i)&255 for i in range(min(3,length)))


def model(case,tag,initial):
    data=bytearray(initial);events=[];fills=0
    size=((case['a']+case['b']+63)&MASK)&~31
    pointer=DATA+0x401+case['shift'];aligned=(pointer+31)&~31
    if size<=case['capacity']:
        for index,(offset,length,old) in enumerate([(0x2C,case['a'],word(initial,0x12C)),(0x34,case['b'],word(initial,0x134))]):
            destination=aligned if index==0 else aligned+case['a']
            events.append(('open',index,old,(old+length)&MASK,MASK))
            if case['opened'][index]:
                events.append(('read',index,destination,length,case['results'][index]))
                chunk=written_bytes(index,length,tag);data[destination-DATA:destination-DATA+len(chunk)]=chunk
                if case['results'][index]&0x80000000:
                    data[destination-DATA:destination-DATA+length]=bytes(length);fills+=1
                events.append(('close',index))
            put(data,0x100+offset,destination)
        put(data,0x144,pointer);put(data,0x150,CALLBACK);put(data,0x11C,case['flags']|4)
    return bytes(data),size,events,fills


def execute(arm,helper_sizes,case,tag,check=True):
    initial=arena(case,tag);expected,result,expected_events,expected_fills=model(case,tag,initial)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base in [0x02008000,0x0200B000,0x0200C000]:
        uc.mem_map(base,4096);uc.mem_write(base,arm[base-0x02000000:base-0x02000000+4096]);uc.mem_protect(base,4096,UC_PROT_READ|UC_PROT_EXEC)
    for base in [DATA,STACK,STOP]:uc.mem_map(base,4096)
    uc.mem_write(DATA,bytes(initial));uc.mem_write(STACK,b'\xB7'*4096)
    sp=STACK+0xF00;frame=sp-96;file=frame+4
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA1000000+tag*131+i*0x101)&MASK)
    for reg,value in zip(REGISTERS[:3],[ARC,DATA+0x401+case['shift'],case['capacity']]):uc.reg_write(reg,value)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(UC_ARM_REG_SP,sp);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]];pcs=set();pending=[];events=[];reads=[];writes=[];current=-1
    state=dict(actualTopReturns=0,originalInitializerReturns=0,originalFillReturns=0,providedCompletions=0,instructions=0)
    def code(machine,address,size,user):
        nonlocal current
        state['instructions']+=1
        if pending and address==pending[-1][0]:
            _,kind=pending.pop();state[kind]+=1
        if address==STOP:state['actualTopReturns']+=1;machine.emu_stop();return
        assert not machine.reg_read(UC_ARM_REG_CPSR)&32 and size==4
        if address in [OPEN,READ,CLOSE]:
            regs=[machine.reg_read(reg) for reg in REGISTERS[:4]];assert regs[0]==file
            if address==OPEN:
                current+=1;assert current in [0,1] and regs[1]==ARC and machine.reg_read(UC_ARM_REG_SP)==frame
                fifth=word(bytes(machine.mem_read(frame,4)),0);events.append(('open',current,regs[2],regs[3],fifth))
                if current==0:
                    for offset,value in [(0,0),(4,0),(8,0),(12,0),(16,14),(24,0),(28,0)]:assert word(bytes(machine.mem_read(file+offset,4)),0)==value
                machine.mem_write(file,bytes((i*13+current*17+tag)&255 for i in range(72)));value=MASK if case['opened'][current] else 0
            elif address==READ:
                value=case['results'][current];events.append(('read',current,regs[1],regs[2],value))
                chunk=written_bytes(current,regs[2],tag)
                if chunk:machine.mem_write(regs[1],chunk)
            else:events.append(('close',current));value=0xC105E000+current
            lr=machine.reg_read(UC_ARM_REG_LR)
            for reg in [1,2,3,12]:machine.reg_write(REGISTERS[reg],(0xE1000000+reg*0x100+tag)&MASK)
            machine.reg_write(UC_ARM_REG_CPSR,((tag*3&15)<<28)|0x1F);machine.reg_write(REGISTERS[0],value);machine.reg_write(UC_ARM_REG_PC,lr);state['providedCompletions']+=1;return
        assert ENTRY<=address<ENTRY+288 or any(start<=address<start+length for start,length in helper_sizes.items()),hex(address)
        if ENTRY<=address<ENTRY+288:pcs.add(address)
        if address in [INIT,FILL]:
            if address==INIT:assert machine.reg_read(REGISTERS[0])==file
            pending.append((machine.reg_read(UC_ARM_REG_LR)&~1,'originalInitializerReturns' if address==INIT else 'originalFillReturns'))
    def read(machine,access,address,size,value,user):
        if DATA<=address<DATA+4096:reads.append((address,size))
    def write(machine,access,address,size,value,user):
        assert frame<=address and address+size<=sp or DATA<=address and address+size<=DATA+4096
        writes.append((address,size,value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write);uc.emu_start(ENTRY,STOP+4,count=4000)
    assert state['actualTopReturns']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==sp and not pending
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved
    assert bytes(uc.mem_read(STACK,frame-STACK))==b'\xB7'*(frame-STACK) and bytes(uc.mem_read(sp,STACK+4096-sp))==b'\xB7'*(STACK+4096-sp)
    memory=bytes(uc.mem_read(DATA,4096));passed=memory==expected and uc.reg_read(REGISTERS[0])==result and events==expected_events and state['originalFillReturns']==expected_fills
    assert state['originalInitializerReturns']==int(result<=case['capacity'])
    if check:assert passed,(case,events,expected_events,hex(uc.reg_read(REGISTERS[0])),hex(result))
    return dict(actualReturn=True,modelPassed=passed,state=state,events=events,pcs=sorted(pcs),reads=reads,writes=writes,memorySha256=hashlib.sha256(memory).hexdigest(),stackSha256=hashlib.sha256(bytes(uc.mem_read(STACK,4096))).hexdigest(),registers=[uc.reg_read(reg) for reg in REGISTERS],cpsr=uc.reg_read(UC_ARM_REG_CPSR))
