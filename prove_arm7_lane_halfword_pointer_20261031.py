import json
import hashlib
import random
from collections import Counter
import match_runtime
import audit_arm7_bulk_20261030 as inventory
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from project import ROOT,sha256,write_json
BASE,WRAM,DATA,STACK,RETURN,HARDWARE=0x027e0000,0x037f8000,0x023c0000,0x023e0000,0x023ff000,0x04808000
POINTER=0x0380fff4
CONFIG={'':dict(constructor=0x027e89ec,stop=0x027e8a10,load=0x027e89f8,store=0x027e8a08,call=0x027e8a0c,fill=0x037fe014,fillBytes=92,descriptorReg='r4',pointerReg='r3',main='extract/arm7/runtime/arm7-main.bin',wram='extract/arm7/runtime/arm7-wram.bin',mainSha256='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416',wramSha256='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'),
    'dwc/utility.bin/move/child.srl':dict(constructor=0x027e8b78,stop=0x027e8b9c,load=0x027e8b84,store=0x027e8b8c,call=0x027e8b98,fill=0x037fe734,fillBytes=76,descriptorReg='r4',pointerReg='r0',main='extract/utility/runtime/utility-child-arm7-main.bin',wram='extract/utility/runtime/utility-child-arm7-wram.bin',mainSha256='a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a',wramSha256='13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6')}


def qualify_roles(main,config):
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM);decoder.detail=True
    code=list(decoder.disasm(main[config['constructor']-BASE:config['stop']-BASE],config['constructor']))
    by={i.address:i for i in code};load=by[config['load']];store=by[config['store']];call=by[config['call']]
    if load.mnemonic!='ldr' or load.op_str!='r1, [r4]' or store.mnemonic!='str' or store.op_str!='r1, ['+config['pointerReg']+']':raise ValueError('Descriptor-word0 producer/store role differs')
    literals=[]
    for instruction in code:
        if instruction.mnemonic=='ldr' and len(instruction.operands)==2 and instruction.operands[1].type==3 and instruction.reg_name(instruction.operands[1].mem.base)=='pc':
            location=instruction.address+8+instruction.operands[1].mem.disp;value=int.from_bytes(main[location-BASE:location-BASE+4],'little');literals.append((instruction.op_str.split(',')[0],value))
    if (config['pointerReg'],POINTER) not in literals or ('r2',0x694) not in literals:raise ValueError('Absolute runtime-word target/context-clear extent differs')
    if call.mnemonic!='bl' or call.operands[0].imm!=config['fill'] or call.address+4!=config['stop']:raise ValueError('Actual clear helper/natural prefix boundary differs')
    return dict(constructor=hex(config['constructor']),boundaryStop=hex(config['stop']),descriptorLoad=hex(config['load']),pointerStore=hex(config['store']),clearHelper=hex(config['fill']),clearBytes=0x694,storage=hex(POINTER),storageBytes=4,origin='incoming descriptor word0',outerReturnCredit=0)


def setup(program,seed,offset,patch=None):
    config=CONFIG[program];main=(ROOT/config['main']).read_bytes();wram=(ROOT/config['wram']).read_bytes()
    if sha256(ROOT/config['main'])!=config['mainSha256'] or sha256(ROOT/config['wram'])!=config['wramSha256']:raise ValueError('Qualified original main/WRAM modules changed')
    roles=qualify_roles(main,config)
    main=bytearray(main+bytes(0x20000-len(main)))
    if patch:
        address,body,code=patch
        if not (BASE<=address and address+len(body)<=BASE+len(main)):raise ValueError('Owned source substitution escaped main module')
        main[address-BASE:address-BASE+len(body)]=body
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={BASE:bytes(main),WRAM:wram+bytes(0x18000-len(wram)),DATA:random.Random(seed+19).randbytes(0x4000),STACK:random.Random(seed+218).randbytes(0x4000),RETURN:bytes(0x1000),HARDWARE:random.Random(seed+219).randbytes(0x1000)}
    for first,data in regions.items():cpu.mem_map(first,len(data));cpu.mem_write(first,data)
    descriptor=DATA+0x3000;target=DATA+offset;cpu.mem_write(descriptor,target.to_bytes(4,'little'))
    before={first:bytearray(cpu.mem_read(first,len(data))) for first,data in regions.items()}
    reads,writes,visited=[],[],[];state=dict(phase='prefix',instructions=0)
    def code_hook(uc,pc,size,unused):
        state['instructions']+=1
        if uc.reg_read(UC_ARM_REG_CPSR)&32:raise ValueError('ARM-only pointer/halfword fixture switched instruction mode')
        if state['phase']=='prefix':allowed=config['constructor']<=pc<config['stop'] or config['fill']<=pc<config['fill']+config['fillBytes']
        else:allowed=patch[0]<=pc<patch[0]+patch[2]
        if not allowed:raise ValueError('Qualified pointer/owned halfword execution escaped instruction scope: '+hex(pc))
        visited.append(pc)
    def read(uc,access,address,size,value,unused):reads.append([address,size])
    def write(uc,access,address,size,value,unused):writes.append([address,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code_hook);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    initial=[random.Random(seed*19+i).getrandbits(32) for i in range(15)];initial[0]=descriptor;initial[-2:]=[STACK+0x3f00,RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR,(seed%16)<<28|0xd3)
    for register,value in zip(match_runtime.REGISTERS,initial):cpu.reg_write(register,value)
    cpu.emu_start(config['constructor'],config['stop'],timeout=200000,count=10000)
    if cpu.reg_read(UC_ARM_REG_PC)!=config['stop'] or cpu.reg_read(match_runtime.REGISTERS[14])!=config['stop'] or visited[-1]!=config['fill']+config['fillBytes']-4:raise ValueError('Producer did not reach actual original clear-helper return boundary')
    before[WRAM][POINTER-WRAM:POINTER-WRAM+4]=target.to_bytes(4,'little');before[DATA][offset:offset+0x694]=bytes(0x694)
    if any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in before.items() if first!=STACK):raise ValueError('Independent producer pointer/whole-context clear/outside-memory model differs')
    nonstack=[r for r in writes if not STACK<=r[0]<STACK+0x4000]
    if nonstack[0]!=[POINTER,4,target]:raise ValueError('Original producer did not store the full incoming descriptor pointer first')
    prefix=dict(roles,program=program,target=hex(target),descriptor=hex(descriptor),actualOriginalFillReturns=1,constructorActualReturn=False,constructorReturnCredit=0,
        instructions=len(visited),orderedNonstackWritesSha256=hashlib.sha256(repr(nonstack).encode()).hexdigest(),storeWidthCounts=dict(Counter(str(r[1]) for r in nonstack)))
    def invoke(address,arguments,budget=1000):
        reads.clear();writes.clear();visited.clear();state['phase']='caller';state['instructions']=0
        registers=[(seed*0x10203+i*0x1030507+0x7129)&0xffffffff for i in range(15)];registers[:len(arguments)]=arguments;registers[13:]=[STACK+0x3000,RETURN]
        cpsr=0x1f|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
        for register,value in zip(match_runtime.REGISTERS,registers):cpu.reg_write(register,value)
        guard=bytes(cpu.mem_read(STACK+0x3000,0x1000));fault=None
        try:cpu.emu_start(address,RETURN,timeout=200000,count=budget)
        except (UcError,ValueError) as error:fault=str(error)
        actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
        if not actual:return dict(actualReturn=False,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,instructions=state['instructions'],postFaultStateExcluded=True)
        result=[cpu.reg_read(register) for register in match_runtime.REGISTERS];flags=cpu.reg_read(UC_ARM_REG_CPSR)
        if result[4:12]!=registers[4:12] or result[13:]!=registers[13:] or flags&255!=cpsr&255 or bytes(cpu.mem_read(STACK+0x3000,0x1000))!=guard:raise ValueError('Actual halfword caller return/register/mode/stack contract differs')
        return dict(actualReturn=True,registers=result,cpsr=flags,pc=hex(RETURN),fault=None,instructions=state['instructions'])
    return dict(cpu=cpu,regions=regions,reads=reads,writes=writes,visited=visited,state=state,prefix=prefix,target=target,invoke=invoke)


def main():
    records=[];controls=[]
    for program,config in CONFIG.items():
        for offset in (0x40,0x800):
            for seed in range(4):records.append(setup(program,seed,offset)['prefix'])
        raw=(ROOT/config['main']).read_bytes();qualify_roles(raw,config)
        for name,pc,mask in [('descriptor-offset',config['load'],4),('store-offset',config['store'],4),('wrong-call',config['call'],1)]:
            changed=bytearray(raw);changed[pc-BASE]^=mask
            try:qualify_roles(changed,config)
            except ValueError:controls.append(dict(program=program,name=name,rejected=True))
            else:raise ValueError('Independent producer instruction-role mutation accepted')
    output=ROOT/'evidence/arm7/lane-halfword-runtime-pointer-20261031.json'
    write_json(output,dict(generator=__import__('pathlib').Path(__file__).name,generatorSha256=sha256(__file__),storage=hex(POINTER),storageBytes=4,moduleBssOwnership=False,originalDataSourceCredit=0,sourceCredit=0,constructorActualReturns=0,constructorReturnCredit=0,
        actualOriginalFillReturns=len(records),records=records,namespaceInputs=[dict(program=p,main=c['main'],mainSha256=c['mainSha256'],wram=c['wram'],wramSha256=c['wramSha256']) for p,c in CONFIG.items()],controls=controls,
        limits=['Explicit native constructor prefixes stop after actual clear-helper returns; no enclosing constructor/thread/game reachability claim','Only the four-byte descriptor-produced absolute pointer word is qualified; pointee32-bit views and module ownership are separate']))
    print(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),prefixes=len(records),actualFillReturns=len(records),constructorReturnCredit=0,controls=len(controls)))


if __name__=='__main__':main()
