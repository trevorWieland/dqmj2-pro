import hashlib
import json
import shutil
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json
from wave20261106_itcm_reset_next_paths import SOURCE,WORK,EVIDENCE,assert_owned
from wave20261106_itcm_reset_next_build import build

ENTRY,READER,CACHE,HEADER,BASE,SP=0x1ff82c8,0x1ff8370,0x2007ff4,0x27ffe00,0x27ffc2c,0x2703000


def run(row,body,seed):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(0x1ff8000,0x8000);cpu.mem_write(0x1ff8000,(ROOT/'extract/arm9/itcm.bin').read_bytes());cpu.mem_write(ENTRY,body)
    cpu.mem_map(0x2000000,0x100000);cpu.mem_write(0x2000000,(ROOT/'extract/arm9/arm9.bin').read_bytes());cpu.mem_map(0x2700000,0x100000)
    base=[0,1,0x7fff,0x8000,0x10000,0x7fffffff,0xffff8000,0xffffffff][seed%8];cpu.mem_write(BASE,struct.pack('<I',base));fields=[(0x12345678*(i+1)+seed*0x10101)&0xffffffff for i in range(6)];offsets=[0x20,0x28,0x2c,0x30,0x38,0x3c]
    for off,value in zip(offsets,fields):cpu.mem_write(HEADER+off,struct.pack('<I',value))
    initial=[0x60000000+i*0x101+seed for i in range(15)];initial[-2:]=[SP,0x2600000];cpu.reg_write(ar.UC_ARM_REG_CPSR,((seed%16)<<28)|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    reads=[];observed=None;pcs=[]
    def read(machine,access,address,size,value,user):
        if BASE<=address<0x2800000:reads.append([address,size])
    def code(machine,address,size,user):
        nonlocal observed
        if address in (READER,CACHE):
            regs=[machine.reg_read(r)for r in C.REGISTERS];observed=dict(provider=hex(address),arguments=regs[:3]if address==READER else [],callerStackBytes=SP-regs[13],mode='thumb'if machine.reg_read(ar.UC_ARM_REG_CPSR)&32 else'arm');machine.emu_stop();return
        if not ENTRY<=address<ENTRY+row['compiledBytes'] or machine.reg_read(ar.UC_ARM_REG_CPSR)&32:raise ValueError('Reset fixture left exact ARM caller before provider stop')
        pcs.append(address)
    cpu.hook_add(un.UC_HOOK_MEM_READ,read);cpu.hook_add(un.UC_HOOK_CODE,code);cpu.emu_start(ENTRY,0,count=100)
    expected=dict(provider=hex(READER if base>=0x8000 else CACHE),arguments=[base,HEADER,0x160]if base>=0x8000 else [],callerStackBytes=40,mode='arm');expected_reads=[[BASE,4]]+([]if base>=0x8000 else [[HEADER+o,4]for o in offsets])
    passed=observed==expected and reads==expected_reads
    return dict(seed=seed,base=hex(base),observed=observed,expected=expected,actualReservedRamReads=reads,expectedReservedRamReads=expected_reads,passed=passed,actualCallerReturn=False,actualProviderInstructions=0,callerInstructions=len(pcs))


def execute(rows):
    assert_owned();row=rows[0];native=(ROOT/'extract/arm9/itcm.bin').read_bytes()[0x2c8:0x370];rebuilt=((ROOT/row['realLink']['linkedElf']).parent/'caller.bin').read_bytes();records=[]
    for seed in range(32):
        a=run(row,native,seed);b=run(row,rebuilt,seed)
        if not a['passed']or a!=b:raise ValueError('Original/source reset partial boundary differs from independent RAM/call model')
        records.append(a)
    negatives=[];text=(ROOT/row['source']).read_text();variants=[('wrong-initial-condition','rom_base>=0x8000','rom_base<0x8000'),('wrong-source-header-offset','p+0x20','p+0x24')]
    for name,before,after in variants:
        folder=WORK/'wrong-c'/name;folder.mkdir(parents=True,exist_ok=True);shutil.copyfile(SOURCE/'context.h',folder/'context.h');source=folder/'01ff82c8.c'
        if text.count(before)!=1:raise ValueError('Whole-C reset mutation is not unique')
        source.write_text(text.replace(before,after));wrong,body=build(source,folder/'link',negative=True);failures=[run(wrong,body,s)for s in range(32)];violations=sum(not x['passed']for x in failures)
        if not violations:raise ValueError('Genuinely linked wrong reset C admitted by independent model')
        negatives.append(dict(case=name,compiledBytes=wrong['compiledBytes'],genuineLink=True,exactCallerBytes=False,independentModelViolations=violations,object=wrong['object'],objectSha256=wrong['objectSha256'],records=failures))
    trace=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest();result=dict(status='passed',records=records,traceSha256=trace,actualPairedCallerEntries=32,nativeAndCompiledReturningCalls=0,actualNativeAndSourceCallerReturns=0,actualNativeAndSourcePartialStops=64,actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=2,negativeControls=negatives,limits=['Only caller entry through the first original cache or ROM-reader boundary is executed.','No provider return is invented. Caller return and every cache/ROM-reader body, cache operation, card-ROM I/O, reset, full image transfer and device/game/Windows execution remain unexecuted.','Reserved RAM/header and helper implementation source, storage and extent receive zero credit.'])
    write_json(EVIDENCE/'caller-fixtures.json',result);return result
