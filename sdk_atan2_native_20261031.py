import hashlib
import struct
from project import ROOT,configuration,native_dependencies
native_dependencies(configuration())
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE,UC_PROT_READ,UC_PROT_EXEC
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY=0x020028D8
TABLE=0x020D7FE0
STACK=0x03020000
STOP=0x0F000000
HELPERS={0x0200235C:16,0x02002458:36,0x020023C4:48}


def cases():
    result=set()
    for index in range(129):
        for delta in [-1,0,1,31]:
            a=index*32+delta;b=4096
            if not 0<=a<=b:continue
            for sy,sx in [(1,1),(1,-1),(-1,1),(-1,-1)]:
                result.add((sy*a,sx*b));result.add((sy*b,sx*a))
    for a in [0,1,2,31,32,4095,8191,0x7FFFFFFE,0x7FFFFFFF]:
        for b in [0,1,2,4096,8192,0x7FFFFFFF]:
            for sy,sx in [(1,1),(1,-1),(-1,1),(-1,-1)]:result.add((sy*a,sx*b))
    return sorted(result)


def expected(y,x,table):
    if y==0:return (0 if x>=0 else 12868),None,None
    if x==0:return (6434 if y>0 else -6434),None,None
    ay,ax=abs(y),abs(x)
    if ay==ax:
        return ((3217 if x>0 else 9651)*(1 if y>0 else -1)),None,None
    numerator,denominator=min(ay,ax),max(ay,ax)
    quotient=((numerator<<32)//denominator+0x80000)>>20
    index=quotient>>5;angle=table[index]
    if ay>ax:angle=6434-angle
    if x<0:angle=12868-angle
    if y<0:angle=-angle
    return angle,(numerator,denominator),index


def execute(arm,table,y,x,tag,check=True):
    angle,ratio,index=expected(y,x,table)
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address,size in [(0x02002000,0x1000),(0x020D7000,0x2000),(STACK,0x2000),(0x04000000,0x1000),(STOP,0x1000)]:uc.mem_map(address,size)
    uc.mem_write(0x02002000,arm[0x2000:0x3000]);uc.mem_write(TABLE,struct.pack('<129h',*table));uc.mem_write(STACK,b'\xB7'*0x2000)
    uc.mem_protect(0x02002000,0x1000,UC_PROT_READ|UC_PROT_EXEC);uc.mem_protect(0x020D7000,0x2000,UC_PROT_READ)
    for i,reg in enumerate(REGISTERS):uc.reg_write(reg,(0xA0110000+i*0x101+tag)&0xFFFFFFFF)
    uc.reg_write(UC_ARM_REG_CPSR,((tag&15)<<28)|0x1F);uc.reg_write(REGISTERS[0],y&0xFFFFFFFF);uc.reg_write(REGISTERS[1],x&0xFFFFFFFF)
    uc.reg_write(UC_ARM_REG_SP,STACK+0x1F00);uc.reg_write(UC_ARM_REG_LR,STOP|(tag&1))
    saved=[uc.reg_read(reg) for reg in REGISTERS[4:12]]
    state={'actualReturn':0,'helperEntries':0,'helperReturns':0,'busyReads':0,'deviceCompletions':0,'instructions':0};pending=[];pcs=set();writes=[];reads=[];division=[];lookup=[]
    def code(machine,address,size,user):
        state['instructions']+=1
        if pending and address==pending[-1][1]:pending.pop();state['helperReturns']+=1
        if address==STOP:state['actualReturn']+=1;machine.emu_stop();return
        assert ENTRY<=address<ENTRY+408 or any(a<=address<a+n for a,n in HELPERS.items()),hex(address)
        pcs.add(address)
        if address in HELPERS:
            pending.append((address,machine.reg_read(UC_ARM_REG_LR)&~1));state['helperEntries']+=1
            if address==0x0200235C:
                args=(machine.reg_read(REGISTERS[0]),machine.reg_read(REGISTERS[1]));assert args==ratio;division.append(args)
    def read(machine,access,address,size,value,user):
        reads.append((address,size))
        if address==0x04000280:
            assert size==2;busy=state['busyReads']<tag%4;state['busyReads']+=1;machine.mem_write(address,struct.pack('<H',0x8001 if busy else 1))
        if TABLE<=address<TABLE+258:lookup.append((address,size));assert size==2
    def write(machine,access,address,size,value,user):
        writes.append((address,size,value&((1<<(size*8))-1)))
        assert STACK<=address and address+size<=STACK+0x2000 or 0x04000280<=address and address+size<=0x040002A0
        if address==0x0400029C:
            n=int.from_bytes(machine.mem_read(0x04000290,8),'little',signed=True);d=int.from_bytes(machine.mem_read(0x04000298,4),'little',signed=True)
            assert ratio is not None and n==ratio[0]<<32 and d==ratio[1] and d>0
            q=n//d;r=n-q*d;machine.mem_write(0x040002A0,struct.pack('<qq',q,r));state['deviceCompletions']+=1
    uc.hook_add(UC_HOOK_CODE,code);uc.hook_add(UC_HOOK_MEM_READ,read);uc.hook_add(UC_HOOK_MEM_WRITE,write)
    uc.emu_start(ENTRY,STOP+4,count=10000)
    assert state['actualReturn']==1 and uc.reg_read(UC_ARM_REG_PC)==STOP and uc.reg_read(UC_ARM_REG_SP)==STACK+0x1F00 and not pending
    assert [uc.reg_read(reg) for reg in REGISTERS[4:12]]==saved
    actual=uc.reg_read(REGISTERS[0]);passed=actual==angle&0xFFFFFFFF
    if check:assert passed,(y,x,angle,hex(actual))
    assert state['helperEntries']==state['helperReturns']==(3 if ratio else 0)
    assert state['deviceCompletions']==(1 if ratio else 0)
    if check:assert lookup==([] if ratio is None else [(TABLE+index*2,2)])
    mmio=[w for w in writes if w[0]<STACK or w[0]>=STACK+0x2000]
    assert mmio==([] if ratio is None else [(0x04000280,2,1),(0x04000290,4,0),(0x04000294,4,ratio[0]),(0x04000298,4,ratio[1]),(0x0400029C,4,0)])
    qreads=[r for r in reads if 0x040002A0<=r[0]<0x040002A8]
    assert qreads==([] if ratio is None else [(0x040002A0,4),(0x040002A4,4)])
    return {'input':[y,x],'actualReturn':True,'result':actual,'expected':angle&0xFFFFFFFF,'modelPassed':passed,'state':state,'pcs':sorted(pcs),'lookup':lookup,'writes':writes,'reads':reads,'registers':[uc.reg_read(reg) for reg in REGISTERS],'cpsr':uc.reg_read(UC_ARM_REG_CPSR),'stackSha256':hashlib.sha256(bytes(uc.mem_read(STACK,0x2000))).hexdigest(),'deviceSha256':hashlib.sha256(bytes(uc.mem_read(0x04000000,0x1000))).hexdigest()}
