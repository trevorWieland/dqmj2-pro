import hashlib
import random
from collections import Counter
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

MAIN,DATA,STACK,RETURN,MMIO=0x027E0000,0x023C0000,0x023E0000,0x023FF000,0x04000000
ADDRESS,SIZE,IO=0x027F6EC0,92,0x04000138
HELPERS={0x027F6F1C:64,0x027F6F5C:52,0x027F6F90:128,0x027F7010:184,0x027F70C8:200}
ARITIES={0x027F6F1C:0,0x027F6F5C:0,0x027F6F90:2,0x027F7010:2,0x027F70C8:2}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    result=[dict(command=command,qualifier=((command*0x1020305)^0x8000FF00)&0xFFFFFFFF,pointer=DATA+0x100+(command&1),
        count=1+command%3,initialIo=(command*257)^0xA551,pattern=command%4,passes=2) for command in range(256)]
    result.extend(dict(command=command,qualifier=qualifier,pointer=DATA+0x100+parity,count=count,
        initialIo=initial,pattern=(count+parity)%4,passes=2)
        for command in (6,0x86) for qualifier in (0,0xFFFFFFFF) for parity in (0,1)
        for count in (1,2,3,8) for initial in (0,1,0xFFFF,0x8000,0x5511))
    result.extend(dict(command=command,qualifier=0xFFFFFFFF,pointer=0x06000000,count=0xFFFFFFFF,
        initialIo=0xFFFF,pattern=3,passes=2) for command in (0x100,0x80000006,0xFFFFFF86,0xFFFFFFFF))
    return result


def model(io_value,data,case):
    data=bytearray(data)
    reads,writes=[],[]
    def read_io():
        reads.append([IO,2])
        return io_value
    def write_io(value):
        nonlocal io_value
        io_value=value&0xFFFF
        writes.append([IO,2,io_value])
    def read_half(pointer):
        reads.append([pointer,2])
        offset=pointer-DATA
        if offset<0 or offset+2>len(data):
            raise ValueError('Native word-dispatch model escaped its bounded buffer')
        return int.from_bytes(data[offset:offset+2],'little')
    def send_byte(value):
        working=(read_io()&~0x77)|0x74
        for index in range(8):
            working=(working&~3)|((value>>index)&1)
            write_io(working)
            working=(working&~2)|2
            write_io(working)
    working=(read_io()&~0x77)|0x72
    write_io(working)
    write_io(working|4)
    send_byte(case['command']|case['qualifier'])
    contracts=[[0x027F6F1C,[]],[0x027F6F90,[case['command'],case['qualifier']]]]
    if case['command'] in (6,0x86):
        if not 1<=case['count']<=8:
            raise ValueError('Native data-helper model only qualifies positive counts1..8')
        contracts.append([0x027F7010 if case['command']==6 else 0x027F70C8,[case['pointer'],case['count']]])
        for index in range(case['count']):
            pointer=case['pointer']+index
            if case['command']==6:
                half=read_half(pointer&~1)
                send_byte(half>>(8 if pointer&1 else 0))
            else:
                working=(read_io()&~0x77)|0x64
                received=0
                for unused in range(8):
                    working&=~3
                    write_io(working)
                    working=read_io()
                    received=(received>>1)|(0x80 if working&1 else 0)
                    working=(working&~2)|2
                    write_io(working)
                half=read_half(pointer&~1)
                half=((half&0xFF)|(received<<8)) if pointer&1 else ((half&0xFF00)|received)
                offset=(pointer&~1)-DATA
                data[offset:offset+2]=half.to_bytes(2,'little')
                writes.append([pointer&~1,2,half])
    write_io(read_io()&~4)
    contracts.append([0x027F6F5C,[]])
    return dict(io=io_value,data=bytes(data),nonstackReads=reads,nonstackWrites=writes,directCalls=contracts)


def setup(body,case,seed):
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if digest(raw)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or len(body)!=SIZE:
        raise ValueError('Measured host main/complete92-byte source entry differs')
    module=bytearray(raw+bytes(0x20000-len(raw)))
    module[ADDRESS-MAIN:ADDRESS-MAIN+SIZE]=body
    data=random.Random(seed+31).randbytes(0x2000)
    if case['pattern']<3:
        pattern=(b'\x00',b'\xff',b'\x00\x80\x7f\xff')[case['pattern']]
        data=pattern*(len(data)//len(pattern))
    regions={MAIN:bytes(module),DATA:data,STACK:random.Random(seed+79).randbytes(0x4000),RETURN:bytes(0x1000),MMIO:random.Random(seed+157).randbytes(0x1000)}
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,content in regions.items():
        cpu.mem_map(base,len(content))
        cpu.mem_write(base,content)
    cpu.mem_write(IO,(case['initialIo']&0xFFFF).to_bytes(2,'little'))
    writes,reads,visited,contracts,frames=[],[],set(),[],[]
    returns=Counter()
    state=dict(instructions=0)
    def code(machine,pc,size,unused):
        state['instructions']+=1
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not (ADDRESS<=pc<ADDRESS+SIZE or any(a<=pc<a+n for a,n in HELPERS.items())):
            raise ValueError('Word-dispatch execution escaped exact host ARM caller/helper bounds')
        while frames and pc==frames[-1][1]:
            returns[frames.pop()[0]]+=1
        if ADDRESS<=pc<ADDRESS+SIZE:
            visited.add(pc)
        if pc in HELPERS:
            contracts.append([pc,[machine.reg_read(register) for register in match_runtime.REGISTERS[:ARITIES[pc]]]])
            frames.append([pc,machine.reg_read(match_runtime.REGISTERS[14])])
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    return dict(cpu=cpu,regions=regions,case=case,seed=seed,state=state,writes=writes,reads=reads,visited=visited,
        contracts=contracts,frames=frames,helperReturns=returns)


def execute(prepared,budget=100000):
    cpu,case,seed=prepared['cpu'],prepared['case'],prepared['seed']
    records=[]
    for iteration in range(case['passes']):
        initial=[(seed*0x10203+index*0x1030507+0x7129)&0xFFFFFFFF for index in range(15)]
        initial[:4]=[case['command'],case['qualifier'],case['pointer'],case['count']]
        initial[13:]=[STACK+0x3000,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,0x1F|((seed&1)*128)|((seed&15)<<28))
        for register,value in zip(match_runtime.REGISTERS,initial):
            cpu.reg_write(register,value)
        before_io=int.from_bytes(cpu.mem_read(IO,2),'little')
        before_data=bytes(cpu.mem_read(DATA,0x2000))
        before_mmio=bytearray(cpu.mem_read(MMIO,0x1000))
        prepared['writes'].clear()
        prepared['reads'].clear()
        prepared['contracts'].clear()
        prepared['frames'].clear()
        prepared['helperReturns'].clear()
        first=prepared['state']['instructions']
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,timeout=100000,count=budget)
        except (UcError,ValueError) as error:
            fault=str(error)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not returned:
            records.append(dict(actualReturn=False,fault=fault,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),
                instructions=prepared['state']['instructions']-first,postFaultStateExcluded=True))
            break
        expected=model(before_io,before_data,case)
        before_mmio[IO-MMIO:IO-MMIO+2]=expected['io'].to_bytes(2,'little')
        nonstack_writes=[row for row in prepared['writes'] if not STACK<=row[0]<STACK+0x4000]
        nonstack_reads=[row for row in prepared['reads'] if not STACK<=row[0]<STACK+0x4000]
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS]
        if nonstack_writes!=expected['nonstackWrites'] or nonstack_reads!=expected['nonstackReads'] or prepared['contracts']!=expected['directCalls']:
            raise ValueError('Independent full-word dispatch, bit/byte transfer or ordered ABI/access model differs')
        if bytes(cpu.mem_read(DATA,0x2000))!=expected['data'] or bytes(cpu.mem_read(MMIO,0x1000))!=before_mmio:
            raise ValueError('Independent word-dispatch data/MMIO guard model differs')
        if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or registers[0]!=expected['io']:
            raise ValueError('Word-dispatch preserved-register/stack or incidental machine R0 differs')
        if cpu.reg_read(UC_ARM_REG_CPSR)!=0x6000001F|((seed&1)*128):
            raise ValueError('Word-dispatch final flags/mode/interrupt mask differ')
        if bytes(cpu.mem_read(STACK+0x3000,0x1000))!=prepared['regions'][STACK][0x3000:]:
            raise ValueError('Word-dispatch caller-visible stack guard changed')
        for base in (MAIN,RETURN):
            if bytes(cpu.mem_read(base,len(prepared['regions'][base])))!=prepared['regions'][base]:
                raise ValueError('Word-dispatch changed unrelated code/return memory')
        records.append(dict(actualReturn=True,fault=None,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            nonstackReads=nonstack_reads,nonstackWrites=nonstack_writes,directCalls=list(prepared['contracts']),
            memorySha256={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in prepared['regions'].items()},
            nestedReturns={hex(a):n for a,n in sorted(prepared['helperReturns'].items())},
            instructions=prepared['state']['instructions']-first,independentModel=True))
    return dict(case=case,states=records,visited=sorted(prepared['visited']))
