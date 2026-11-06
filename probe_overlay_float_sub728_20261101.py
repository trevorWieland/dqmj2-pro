import itertools
import sys
import math
import struct
import match_runtime as c
import unicorn
from project import ROOT,write_json,sha256,configuration
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE,ENTRY,STACK,STOP=0x02000000,0x02025CA4,0x027F0000,0x027FF800
REGS=c.REGISTERS[:13]


def number(word):return struct.unpack('<f',struct.pack('<I',word))[0]


def bits(value):
    try:return struct.unpack('<I',struct.pack('<f',value))[0]
    except OverflowError:return 0xFF800000 if value<0 else 0x7F800000


def ranges(addresses):
    result=[]
    for address in sorted(addresses):
        if result and result[-1]['end']==address:result[-1]['end']=address+4
        else:result.append(dict(start=address,end=address+4))
    return result


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!="2.1.4":raise ValueError("728 pinned runtime differs")
    module,image,unused=measured_module('main')
    if module['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f':raise ValueError('728 main image differs')
    values=[0,1,0x007FFFFF,0x00800000,0x3EAAAAAB,0x3F000000,0x3F800000,0x3F800001,0x3F7FFFFF,0x40000000,0x4B000000,0x4B800000,0x7F7FFFFF];words=sorted(set(values+[v|0x80000000 for v in values]));cases=[];observed=set();failures=[];wrong_add,wrong_reverse=0,0
    for a,b in itertools.product(words,repeat=2):
        u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(BASE,image);u.reg_write(UC_ARM_REG_CPSR,0xA0000010);initial=[0xA7280000+i*256 for i in range(13)]
        for register,value in zip(REGS,initial):u.reg_write(register,value)
        u.reg_write(UC_ARM_REG_R0,a);u.reg_write(UC_ARM_REG_R1,b);u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);seen=set();writes=[]
        def code(vm,address,size,data):
            if not BASE<=address<BASE+len(image):raise ValueError(('728 unexpected native code',hex(address)))
            seen.add(address)
        def write(vm,access,address,size,value,data):writes.append([address,size,value])
        u.hook_add(UC_HOOK_CODE,code);u.hook_add(UC_HOOK_MEM_WRITE,write);u.emu_start(ENTRY,STOP,count=10000)
        if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[u.reg_read(r)for r in REGS[4:12]]!=initial[4:12]:raise ValueError('728 did not actually return preserving frame')
        if writes:raise ValueError(('728 unexpected memory writes',writes))
        actual=u.reg_read(UC_ARM_REG_R0);expected=bits(number(a)-number(b));wrong_add+=actual!=bits(number(a)+number(b));wrong_reverse+=actual!=bits(number(b)-number(a));observed.update(seen)
        row=dict(inputRawR0=a,inputRawR1=b,actualRawR0=actual,expectedF32Subtraction=expected,matches=actual==expected,actuallyReturned=True,finalR1Scratch=u.reg_read(UC_ARM_REG_R1),cpsr=u.reg_read(UC_ARM_REG_CPSR),memoryWrites=0,nativeCodeSha256=c.sha(b''.join(struct.pack('<II',pc,int.from_bytes(image[pc-BASE:pc-BASE+4],'little'))for pc in sorted(seen))))
        cases.append(row)
        if actual!=expected:failures.append(row)
        u=None
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=module['sha256'],mode='arm',entry=hex(ENTRY),sourceCredit=0,actualTopReturns=len(cases),providedCalls=0,observedNativeCodeRanges=ranges(observed),finiteRawWordValues=len(words),allFinitePairs=len(cases),matchingF32Subtraction=len(cases)-len(failures),failedF32Subtraction=failures,wrongModelsOnly=dict(additionRejected=wrong_add,reverseSubtractionRejected=wrong_reverse,extraExecutions=0,compiledWrongSource=False),cases=cases,limits=['Original native-only finite raw-word contract, not a selected C caller/source/boundary proof.','R0/R1 input words are interpreted as IEEE754 binary32 and R0 output compared to once-rounded subtraction of two finite binary32 operands. R1 and flags are retained as scratch facts, not semantic outputs.','Signed zeros, subnormals, adjacent mantissas, large finite values and overflow-to-infinity results are recorded. NaN/infinity inputs remain unsupported.','Existing heuristic ledger entry02025CA4/632 is not promoted to a verified isolated function boundary; branches into shared float code remain measured native execution. The preceding XOR-swap entry02025C98 is not rebound or accepted.','No providers, hardware/device/emulator scene, inferred SDK identity or source credit.'])
    write_json(ROOT/'evidence/abi/overlay-main25ca4-f32-sub728-20261101.json',report);print(dict(actualTopReturns=len(cases),matches=len(cases)-len(failures),failed=len(failures),nativeCodeRanges=ranges(observed),wrong_add=wrong_add,wrong_reverse=wrong_reverse),flush=True)


if __name__=='__main__':execute()
