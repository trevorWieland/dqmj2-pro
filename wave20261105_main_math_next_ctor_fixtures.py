import hashlib
import json
import shutil
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,write_json,sha256
from wave20261105_main_math_next_ctor_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261105/main-math-next/ctor'
ADDRESS,TABLE,STOP,SP=0x2026a94,0x20dcb30,0x27e0000,0x2701000


def run(image,body,seed,nzcv):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x2000000,0x200000);cpu.mem_write(0x2000000,image);cpu.mem_write(ADDRESS,body);cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x2000);before=bytes(cpu.mem_read(TABLE,8));initial=[(0x11220000+i*0x101+seed)&0xffffffff for i in range(15)];initial[-2:]=[SP,STOP];cpu.reg_write(ar.UC_ARM_REG_CPSR,nzcv|0x10)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    returned=False;pcs=[];reads=[]
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop();return
        if not ADDRESS<=at<ADDRESS+40:raise ValueError('Empty-list fixture entered callback/another body/literal')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not (SP-0x1000<=at and at+size<=SP):raise ValueError('Constructor fixture wrote outside own stack')
    def read(machine,access,at,size,value,user):
        if TABLE<=at<TABLE+8:reads.append(dict(address=hex(at),bytes=size))
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.hook_add(un.UC_HOOK_MEM_READ,read);cpu.emu_start(ADDRESS,STOP+4,count=300);registers=[cpu.reg_read(r) for r in C.REGISTERS]
    if not returned or registers[4:12]!=initial[4:12] or registers[13]!=SP or bytes(cpu.mem_read(TABLE,8))!=before:raise ValueError('Constructor actual return/ABI/read-only table differs')
    return dict(address=hex(ADDRESS),seed=seed,nzcv=nzcv,topReturned=True,calleeSavedAbiPreserved=True,callerMemoryUnchanged=True,firstPointerRead=reads,modelPassed=reads==[dict(address=hex(TABLE),bytes=4)],pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest(),nativeCalleeExecutions=0)


def execute(rows):
    row=rows[0];image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[0x26a94:0x26ac0];linked=(ROOT/row['realLink']['lcf']).with_name('caller.bin').read_bytes();cases=[(seed,nzcv) for seed in range(8) for nzcv in [0,0x10000000,0x80000000,0xf0000000]];records=[]
    for seed,nzcv in cases:
        original=run(image,native,seed,nzcv);source=run(image,linked,seed,nzcv)
        if original!=source or not original['modelPassed']:raise ValueError('Original linker-start pointer read/return model differs')
        records.append(original)
    folder=ROOT/'work/w5mn/ctor/fixtures/wrong-C';folder.mkdir(parents=True,exist_ok=True);source=ROOT/row['source']
    for pin in row['sourceDependencies']:shutil.copyfile(ROOT/pin['path'],folder/(ROOT/pin['path']).name)
    text=source.read_text();changed=text.replace('p=native_data_020dcb30;','p=native_data_020dcb30+1;',1)
    if changed==text:raise ValueError('Wrong complete C did not shift original linker-start pointer')
    wrong=folder/source.name;wrong.write_text(changed);bad,body=build(wrong,folder/'genuine-link',negative=True)
    if bad['compiledBytes']!=44:raise ValueError('Wrong whole constructor C extent differs')
    negative=[]
    for seed,nzcv in cases[:16]:
        actual=run(image,body,seed,nzcv)
        if actual['modelPassed'] or not actual['topReturned']:raise ValueError('Wrong C did not actually return after wrong first-slot read')
        negative.append(actual)
    report=dict(status='passed',records=records,nativeAndCompiledReturningCalls=2*len(records),actualNativeCalleeBodiesExecuted=0,nativeDevicesOrScenesExecuted=0,traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True).encode()).hexdigest(),wholeCNegativeControlsRejected=1,wrongC=dict(sourceSha256=sha256(wrong),compiledBytes=44,genuineLink=bad['realLink'],actualReturningModelRejections=len(negative),records=negative),limits=['Only actual original empty-table-first-word behavior executes; no synthetic nonzero callbacks are installed. Caller loads exactly the original linker-start word, returns with callee-saved ABI and leaves table memory unchanged.','Whole wrong C skips the linker-start slot; it genuinely links at the same 44-byte extent and actually returns after reading the next original zero word. The independently declared first-slot address model rejects its observed read, even though both words currently contain zero.','Complete table extent/storage and all nonzero callback targets, modes, namespaces, returns and source credit remain unqualified. No hardware or scene execution.']);write_json(LANE/'caller-fixtures.json',report);return report
