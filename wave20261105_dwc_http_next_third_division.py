import hashlib,json,re,struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,sha256
ENTRIES={0x2026144:524,0x2026350:484}
STOP,SP=0x27e0000,0x2701000
def signed(n):return n-(1<<32)if n&0x80000000 else n
def result(at,n,d):
    if not d:raise ValueError('Zero divisor outside qualified support domain')
    if at==0x2026144:
        a,b=signed(n),signed(d);q=abs(a)//abs(b);q=-q if(a<0)!=(b<0)else q;r=a-q*b
    elif at==0x2026350:q,r=divmod(n,d)
    else:raise ValueError('Unqualified arithmetic entry')
    return q&0xffffffff,r&0xffffffff
def run(at,n,d,seed,image):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x100000);cpu.mem_write(0x2000000,image);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000)
    before=[(0x11220000+seed*0x101+i*0x110011)&0xffffffff for i in range(15)];before[:2]=[n,d];before[13:]=[SP,STOP];cpsr=[0x10,0x10000010,0x80000010,0xf0000010][seed%4];cpu.reg_write(ar.UC_ARM_REG_CPSR,cpsr)
    for reg,value in zip(C.REGISTERS,before):cpu.reg_write(reg,value)
    returned=False;pcs=[];writes=[]
    def code(machine,pc,size,unused):
        nonlocal returned
        if pc==STOP:returned=True;machine.emu_stop();return
        if not at<=pc<at+ENTRIES[at]or machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Native arithmetic escaped exact canonical ARM extent')
        pcs.append(pc)
    def write(machine,access,address,size,value,unused):writes.append((address,size,value))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(at,STOP+4,count=10000);after=[cpu.reg_read(reg)for reg in C.REGISTERS]
    if not returned or after[:2]!=list(result(at,n,d))or after[4:12]!=before[4:12]or after[13:]!=before[13:]or writes:raise ValueError(('Native arithmetic ABI differs',hex(at),hex(n),hex(d),after[:2],result(at,n,d)))
    record=dict(entry=hex(at),numerator=hex(n),denominator=hex(d),registersBefore=before,registersAfter=after,cpsrBefore=cpsr,cpsrAfter=cpu.reg_read(ar.UC_ARM_REG_CPSR),pcs=pcs,writes=writes)
    return dict(entry=hex(at),numerator=hex(n),denominator=hex(d),quotient=hex(after[0]),remainder=hex(after[1]),traceSha256=hashlib.sha256(json.dumps(record,sort_keys=True).encode()).hexdigest(),calleeSavedStackArmModeAndNoWritesPassed=True)
def verify():
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();rows=[];providers=[]
    values=[0,1,2,3,4,5,6,7,8,15,16,63,255,0x7fffffff,0x80000000,0xffffffff]
    for at,size in ENTRIES.items():
        canonical=next((line for line in inventory.splitlines()if re.fullmatch(r'\S+ kind:function\(arm,size=0x%x\) addr:0x%08x'%(size,at),line)),None)
        if canonical is None:raise ValueError('Canonical arithmetic support changed')
        providers.append(dict(entry=hex(at),mode='arm',bytes=size,bodySha256=hashlib.sha256(image[at-0x2000000:at-0x2000000+size]).hexdigest(),canonicalInventoryRecord=canonical))
        for seed,(n,d)in enumerate((n,d)for n in values for d in [3,6,0xffffffff]):rows.append(run(at,n,d,seed,image))
    return dict(status='passed',cases=rows,providers=providers,actualOriginalArithmeticReturns=len(rows),GprR0QuotientR1RemainderVerified=True,calleeSavedStackArmEntryAndNoWritesVerified=True,callerSavedR2R3R12AndCpsrNotPreservedByCallerContract=True,zeroDivisorQualified=False,originalCompilerSupportSourceOrAdditionalExecutionCredit=0,scope='Actual original support bodies execute only in these bounded arithmetic qualification probes; caller fixtures use supplied verified quotient/remainder contracts with caller-saved/CPSR stress')
