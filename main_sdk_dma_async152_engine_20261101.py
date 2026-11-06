import hashlib
import random
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT

BASE,DATA,STACK,RETURN=0x02000000,0x023C0000,0x023E0000,0x023FF000
MODULE=ROOT/'extract/arm9/arm9.bin'
MODULE_SHA='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
ITCM=ROOT/'extract/arm9/itcm.bin'
ITCM_SHA='69b4ab1dc8c4f9c05388bbcc456ba6037fd8f09ab774d65a3eb8adc130e1c1fb'
SIZES={0x0200867C:152}
CODE=SIZES|{0x020088A4:84,0x02008714:100,0x02005C64:60,0x02005D20:44,
    0x02007FF4:20,0x02008008:24,0x01FF8448:64,0x02008430:16,0x02008440:12}



def digest(data):
    return hashlib.sha256(data).hexdigest()


def setup(bodies,seed,control=0):
    raw=MODULE.read_bytes()
    if digest(raw)!=MODULE_SHA:
        raise ValueError('Original measured ARM9 module differs')
    if bodies and bodies!={a:raw[a-BASE:a-BASE+n]for a,n in SIZES.items()}:
        raise ValueError('Only the complete freshly linked native-equal DMA C body may be installed')
    regions={BASE:bytearray(0x3E0000),STACK:bytearray(random.Random(seed+8701).randbytes(0x4000)),
        STACK+0x4000:bytearray(0x1C000)}
    itcm=ITCM.read_bytes()
    if digest(itcm)!=ITCM_SHA:raise ValueError('Measured original ITCM module differs')
    regions[0x01FF8000]=bytearray(itcm+bytes(0x8000-len(itcm)))
    regions[0x04000000]=bytearray(0x1000)
    regions[BASE][:len(raw)]=raw
    for address,body in bodies.items():regions[BASE][address-BASE:address-BASE+len(body)]=body
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base,data in regions.items():cpu.mem_map(base,len(data));cpu.mem_write(base,bytes(data))
    reads,writes,visited,frames,nested,events=[],[],[],[],[],[]
    def code(machine,pc,width,unused):
        if machine.reg_read(UC_ARM_REG_CPSR)&32 or not any(a<=pc and pc+width<=a+n for a,n in CODE.items()):
            raise ValueError('DMA setup fixture escaped exact original ARM caller/helper instruction scope: '+hex(pc))
        if frames and pc==frames[-1][1]:
            frame=frames.pop();nested.append({'entry':hex(frame[0]),'returnPc':hex(frame[1])})
        if pc in CODE:
            lr=machine.reg_read(match_runtime.REGISTERS[14])
            events.append({'entry':hex(pc),'lr':hex(lr),'arguments':[machine.reg_read(r)for r in match_runtime.REGISTERS[:4]],
                'sp':machine.reg_read(match_runtime.REGISTERS[13]),'cpsr':machine.reg_read(UC_ARM_REG_CPSR),
                'recordBytes':bytes(machine.mem_read(DATA+0x800,8)).hex()})
            if lr!=RETURN:frames.append([pc,lr])
        visited.append(pc)
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda m,a,p,n,v,u:reads.append([p,n]))
    cpu.hook_add(UC_HOOK_MEM_WRITE,lambda m,a,p,n,v,u:writes.append([p,n,v&((1<<(n*8))-1)]))
    def snapshot():
        return {base:bytearray(cpu.mem_read(base,len(data)))for base,data in regions.items()if base!=STACK}
    def invoke(address,arguments,budget=100000):
        initial=[random.Random(seed*37+i).getrandbits(32)for i in range(15)]
        initial[:min(4,len(arguments))]=arguments[:4]
        initial[-2:]=[STACK+0x3000,RETURN]
        if len(arguments)>4:cpu.mem_write(STACK+0x3000,b''.join(v.to_bytes(4,'little')for v in arguments[4:]))
        guard=bytes(cpu.mem_read(STACK+0x3000,0x1000))
        cpu.reg_write(UC_ARM_REG_CPSR,(seed%16<<28)|0x13|control)
        for r,v in zip(match_runtime.REGISTERS,initial):cpu.reg_write(r,v)
        reads.clear();writes.clear();visited.clear();frames.clear();nested.clear();events.clear()
        error=None
        try:cpu.emu_start(address,RETURN,count=budget,timeout=1000000)
        except(UcError,ValueError)as failure:error=str(failure)
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN and error is None
        registers=[cpu.reg_read(r)for r in match_runtime.REGISTERS]
        if returned and(registers[4:12]!=initial[4:12]or registers[13]!=initial[13]or frames or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard):
            raise ValueError('Actual DMA setup callee-save/SP/return-frame/upper-stack guard differs')
        return {'actualReturn':returned,'error':error,'pc':hex(cpu.reg_read(UC_ARM_REG_PC)),'registers':registers,
            'cpsr':cpu.reg_read(UC_ARM_REG_CPSR),'reads':reads[:],'writes':writes[:],'visited':sorted(set(visited)),
            'nestedReturns':nested[:],'entryEvents':events[:],'completeMemorySha256':{hex(b):digest(bytes(cpu.mem_read(b,len(d))))for b,d in regions.items()},
            'postFaultOrBoundaryStateExcluded':not returned}
    return {'cpu':cpu,'snapshot':snapshot,'invoke':invoke,'regions':regions}
