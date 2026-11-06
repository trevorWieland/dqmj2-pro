import hashlib
import json
import match_runtime as C
import unicorn as un
import unicorn.arm_const as ar
from project import ROOT,write_json
from wave20261106_auth_resume_next_third_paths import assert_owned,EVIDENCE as LANE,SOURCE,WORK


def helper_specs(image,inventory):return []


def run(image,row,body,seed,specs):
    address=int(row['address'],0);stack=0x027e0000;work=0x03005000;cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_THUMB);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946);cpu.mem_map(0x02000000,0x400000);cpu.mem_write(0x02000000,image);cpu.mem_write(address,body);cpu.mem_map(stack-0x4000,0x5000);cpu.mem_write(stack-0x4000,bytes([0xa5])*0x4000);cpu.mem_map(work,0x1000);initial=[0x6c000000+i*0x101+seed for i in range(15)];initial[0]=work;initial[-2:]=[stack,0x04000001];cpu.reg_write(ar.UC_ARM_REG_CPSR,[0,0x10000000,0x80000000,0xf0000000][seed%4]|0x30)
    for reg,value in zip(C.REGISTERS,initial):cpu.reg_write(reg,value)
    observed=None;pcs=[]
    def code(machine,at,size,user):
        nonlocal observed
        regs=[machine.reg_read(r)for r in C.REGISTERS];thumb=bool(machine.reg_read(ar.UC_ARM_REG_CPSR)&32)
        if at==0x02007a9c:
            if thumb or regs[4]!=work or regs[13]!=stack-24:raise ValueError('Actual original clock-entry/work/frame ABI differs')
            observed=dict(kind='provider-stop',address=hex(at),providerInstructionsExecuted=0);machine.emu_stop();return
        if not address<=at<address+len(body)or not thumb:raise ValueError('Caller escaped before its actual opaque clock boundary')
        pcs.append(at)
    def write(machine,access,at,size,value,user):
        if not stack-0x4000<=at<=at+size<=stack:raise ValueError('Unexpected pre-provider caller memory write')
    cpu.hook_add(un.UC_HOOK_CODE,code);cpu.hook_add(un.UC_HOOK_MEM_WRITE,write);cpu.emu_start(address|1,0x04000004,count=1000)
    if observed is None or bytes(cpu.mem_read(work,3352))!=bytes(3352):raise ValueError('Original clock entry was not reached with caller RAM intact')
    return dict(address=row['address'],seed=seed,observed=observed,topReturned=False,partialProviderStopped=True,modelPassed=True,actualOriginalHelperInvocations=0,actualOriginalHelperReturns=0,pcSha256=hashlib.sha256(json.dumps(pcs).encode()).hexdigest())


def execute(rows):
    assert_owned(LANE,SOURCE,WORK);image=(ROOT/'extract/arm9/arm9.bin').read_bytes();records=[]
    for row in rows:
        address=int(row['address'],0);native=image[address-0x02000000:address-0x02000000+row['bytes']];compiled=(ROOT/row['realLink']['linkedElf']).parent.joinpath('caller.bin').read_bytes()
        for seed in range(4):
            left=run(image,row,native,seed,[]);right=run(image,row,compiled,seed,[])
            if left!=right:raise ValueError('Actual original/C provider-entry traces differ')
            records.append(left)
    result=dict(status='passed',traceSha256=hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':')).encode()).hexdigest(),records=records,nativeAndCompiledReturningCalls=0,nativeAndCompiledPartialStops=2*len(records),actualNativeCalleeBodiesExecuted=0,wholeCNegativeControlsRejected=0,limits='Four original/C calls stop BEFORE first actual hardware-clock provider instruction, with measured ARM BLX/work pointer/frame and untouched work RAM. No caller returns, timer/division/scan/next-phase/provider bodies, hardware/network/game/Windows execution or imported storage/source credit. Full post-clock caller semantics are justified by complete original-C byte/link equality and native field/branch witnesses, not claimed executed here.')
    write_json(LANE/'caller-fixtures.json',result);return result
