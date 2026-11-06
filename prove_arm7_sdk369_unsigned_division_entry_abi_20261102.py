import hashlib
import json
import random
from pathlib import Path
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
import arm7_lane_sdk_division_scope_20261031 as prior
import link_arm7_bulk_20261030 as strict
from project import ROOT,sha256,write_json

ENTRY,END,STOP,STACK=0x03806e44,0x03807028,0x0f000000,0x03010000

def boundary(raw):
    old=prior.validate_scope(raw);offset=ENTRY-prior.BASE
    if struct.unpack_from('<II',raw,offset)!=(0xe3510000,0x012fff1e):raise ValueError('Exact denominator-zero CMP/BX prefix changed')
    modules,functions=strict.namespace('');binding=functions.get(ENTRY)
    if not binding or binding['program']!=''or binding['module']!='arm7-wram'or binding['mode']!='arm':raise ValueError('Actual helper must already be the canonical hostWRAM ARM entry')
    return dict(processor='arm7',program='',module='arm7-wram',mode='arm',address=hex(ENTRY),fullSpanBytes=END-ENTRY,fullSpanSha256=hashlib.sha256(raw[offset:END-prior.BASE]).hexdigest(),prefixBytes=8,prefixSha256=hashlib.sha256(raw[offset:offset+8]).hexdigest(),moduleSha256=prior.MODULE_SHA,canonicalEntryAlreadyPresent=True,priorComputedTailScope=old,sourceCredit=0,denominatorIncrease=0)

def execute(raw,n,d,index):
    if not 0<=n<=0xffffffff or not 0<=d<=0xffffffff:raise ValueError('Raw unsigned32 inputs required')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);image=raw+bytes(0x10000-len(raw));cpu.mem_map(prior.BASE,len(image));cpu.mem_write(prior.BASE,image);cpu.mem_map(STACK,0x1000);cpu.mem_map(STOP,0x1000);rng=random.Random(0x369000+index);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:2]=[n,d];initial[-2:]=[STACK+0xff0,STOP];cpsr=0x13|((index%4)<<6)|((index&15)<<28);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for r,v in zip(REGISTERS,initial):cpu.reg_write(r,v)
    visited=[];stores=[];returned=[False]
    def code(machine,pc,size,user):
        if pc==STOP:returned[0]=True;machine.emu_stop();return
        if not ENTRY<=pc<END or pc==prior.FIRST or size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('Helper escaped exact original ARM code or executed skippedNOP')
        visited.append(pc)
    def write(machine,access,a,width,v,user):stores.append([a,width,v])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.emu_start(ENTRY,STOP+4,count=10000);regs=[cpu.reg_read(r)for r in REGISTERS];expected=list(divmod(n,d))if d else[n,0];checks=dict(actualReturn=returned[0],quotientAndRemainder=regs[:2]==expected,calleeSaved=regs[4:12]+regs[13:]==initial[4:12]+initial[13:],modeAndControl=(cpu.reg_read(UC_ARM_REG_CPSR)&255)==(cpsr&255),noStores=not stores,wholeMappedMemoryUnchanged=bytes(cpu.mem_read(prior.BASE,len(image)))==image and bytes(cpu.mem_read(STACK,0x1000))==bytes(0x1000)and bytes(cpu.mem_read(STOP,0x1000))==bytes(0x1000))
    if not all(checks.values()):raise ValueError(dict(n=n,d=d,checks=checks))
    return dict(numerator=n,denominator=d,actualReturn=True,checks=checks,registers=regs,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),visited=sorted(set(visited)),instructions=len(visited),denominatorZeroCharacterizationOnly=d==0,sourceCredit=0)

def main():
    path=ROOT/'extract/arm7/runtime/arm7-wram.bin';raw=path.read_bytes();scope=boundary(raw);edges=(0,1,2,255,65535,0x7fffffff,0x80000000,0xffffffff);cases=[(n,d)for n in edges for d in edges if d];cases.extend((1<<s,1)for s in range(32));rng=random.Random(0x369fff);cases.extend((rng.getrandbits(32),rng.getrandbits(32)|1)for unused in range(64));rows=[execute(raw,n,d,i)for i,(n,d)in enumerate(cases)];zeros=[execute(raw,n,0,1000+i)for i,n in enumerate(edges)];visited={pc for r in rows for pc in r['visited']}
    if set(range(0x03806ea0,END,4))-visited:raise ValueError('Original computed division tail not fully visited')
    main_image=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();framing=main_image[0xd9d8:0xda08];expected_words=[0xe5951004,0xe1a04000,0xe3510000,0x15950008,0xe3a02000,0x13500000,0x0a000003]
    if list(struct.unpack('<7I',framing[:28]))!=expected_words or list(struct.unpack('<4I',main_image[0xd9f8:0xda08]))!=[0xe2802001,0xe3520064,0x83a02064,0xe595101c]:raise ValueError('Actual zero guard/quotient-only use/flags and remainder overwrite differs')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),scope=scope,priorScopeGenerator=dict(path=Path(prior.__file__).name,sha256=sha256(prior.__file__)),actualNonzeroDenominatorReturns=len(rows),actualZeroCharacterizationReturns=len(zeros),records=rows,zeroCharacterization= zeros,callerFraming=dict(range=['0x27ed9d8','0x27eda08'],sha256=hashlib.sha256(framing).hexdigest(),postCallQuotientOnlyUseAndRemainderFlagsKilled=True),callerContract=dict(caller='0x27ed864',relocationOffset=400,relocationType=1,compilerSymbol='_u32_div_f',inputRegisters=['r0:u32 numerator','r1:u32 nonzero denominator'],usedReturnRegisters=['r0:u32 quotient'],alsoObservedButNotUsedReturn='r1:u32 remainder',sourceOperator='pMLME->Work.Measure.CCA / pMLME->Work.Measure.Counter',sourceGuardSkipsZeroCounter=True,postCallR1AndFlagsNotConsumed=True),sourceCredit=0,originalAssemblyProvenanceCredit=0,newNamespaceOrConfigurationChanges=False,limitations=['Zero behavior is original-helper characterization and never makes C division byzero supported','Only the pinned compiler/caller/relocation/expression can consume this contract','No reconstructed helper source or assembly credit','No general compiler alias or alternate-entry guard is relaxed']);write_json(ROOT/'evidence/attempts/arm7-sdk369-unsigned-division-entry-abi-20261102.json',report);print(json.dumps(dict(nonzeroReturns=len(rows),zeroCharacterizationReturns=len(zeros),fullSpanSha256=scope['fullSpanSha256'],sourceCredit=0)),flush=True)

if __name__=='__main__':main()
