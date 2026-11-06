import hashlib
import re
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json
from wave20261105_gamespy_qr2_next_nineteenth_models import DIV,SP,STOP,s32,mod


def prove():
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();inventory=(ROOT/'config/arm9/symbols.txt').read_text();originals=(ROOT/'config/arm9/relocs.txt').read_text().splitlines()
    record=next(line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(arm,size=0x[0-9a-f]+\) addr:0x02026144',line));size=int(re.search(r'size=(0x[0-9a-f]+)',record)[1],0)
    origin='from:0x020b7ed2 kind:thumb_call_arm to:0x02026144 module:main'
    assert origin in originals
    outputs=[]
    vectors=[(a,b)for a in [0,1,254,255,256,0x7fffffff,0xffffffff,0xffffff00,0x80000000]for b in [1,2,9,10,255,256,0x7fffffff]]
    for seed,(numerator,denominator)in enumerate(vectors):
        unused=0;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
        cpu.mem_map(0x2000000,0x400000);cpu.mem_write(0x2000000,image);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x4000,0x5000)
        initial=[(0x33660000+index*0x101+seed)&0xffffffff for index in range(15)];initial[:2]=[numerator,denominator];initial[-2:]=[SP,STOP|1]
        cpu.reg_write(ar.UC_ARM_REG_CPSR,[0x10,0x10000010,0x80000010,0xf0000010][seed%4])
        for register,value in zip(C.REGISTERS,initial):cpu.reg_write(register,value)
        returned=[];trace=[];writes=[]
        def instruction(machine,address,width,user):
            if address==STOP:returned.append(address);machine.emu_stop();return
            if not DIV<=address<DIV+size or machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError(('Signed helper escaped its actual full ARM function',hex(address)))
            trace.append(address)
        def store(machine,access,address,width,value,user):
            if not SP-0x4000<=address or address+width>SP:raise ValueError('Signed helper wrote beyond bounded stack')
            writes.append((address,width,value))
        cpu.hook_add(un.UC_HOOK_CODE,instruction);cpu.hook_add(un.UC_HOOK_MEM_WRITE,store);cpu.emu_start(DIV,STOP+4,count=20000)
        regs=[cpu.reg_read(register) for register in C.REGISTERS]
        assert returned==[STOP] and regs[:2]==[((s32(numerator)-mod(s32(numerator),s32(denominator)))//s32(denominator))&0xffffffff,mod(s32(numerator),s32(denominator))&0xffffffff] and regs[4:12]==initial[4:12] and regs[13]==SP
        outputs.append(dict(numerator=hex(numerator),denominator=hex(denominator),quotient=hex(regs[0]),remainder=hex(regs[1]),seed=seed,cpsr=hex(cpu.reg_read(ar.UC_ARM_REG_CPSR)),traceSha256=hashlib.sha256(repr((trace,writes,regs)).encode()).hexdigest()))
    return dict(status='passed',address=hex(DIV),program='',processor='arm9',module='main',mode='arm',bytes=size,nativeSha256=hashlib.sha256(image[DIV-0x2000000:DIV-0x2000000+size]).hexdigest(),
        canonicalInventoryRecord=record,actualOriginalCallerRelocationRecord=origin,callerReadsR1At='0x20b7eda',callerInstruction='str r1,[r5,r0] stores measured modulo remainder into current-index word',actualOriginalHelperReturns=len(outputs),records=outputs,
        quotientRegister='R0',remainderRegister='R1',calleeSavedAndStackChecked=True,entryAndCompleteInstructionRangeChecked=True,helperSourceCredit=0,hardwareOrGameExecutionCredit=0,
        limits=['Only this full original arithmetic helper executes without a substitute. Signed numerators including INT_MIN and nonzero positive divisors are checked; divide-by-zero and every possible uint32 pair are unproved.','Helper source/object reconstruction is outside this caller packet and earns zero additional source credit. Caller fixture records separately use its now-measured two-register ABI.'])
