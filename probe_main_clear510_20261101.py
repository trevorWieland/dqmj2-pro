import json
import struct
import match_runtime as c
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE
from unicorn.arm_const import *
BASE,ENTRY,SIZE,DEST,STACK,STOP=0x02000000,0x02008C58,76,0x02600000,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12]


def execute(image,fill,count,r3):
    u=Uc(UC_ARCH_ARM,UC_MODE_ARM);u.ctl_set_cpu_model(UC_CPU_ARM_946);u.mem_map(BASE,0x800000);u.mem_write(BASE,image);u.mem_write(DEST,bytes([0xA5])*512);initial=[0xC5100000+i*0x10101 for i in range(13)];u.reg_write(UC_ARM_REG_CPSR,0x10)
    for reg,value in zip(REGS,initial):u.reg_write(reg,value)
    for reg,value in zip(REGS[:4],[fill,DEST,count,r3]):u.reg_write(reg,value)
    u.reg_write(UC_ARM_REG_SP,STACK);u.reg_write(UC_ARM_REG_LR,STOP);observed=set();instructions=0
    def watch(engine,pc,size,data):
        nonlocal instructions
        instructions+=1
        if not ENTRY<=pc<ENTRY+SIZE:raise ValueError('510 escaped native helper')
        observed.add(pc)
    u.hook_add(UC_HOOK_CODE,watch);u.emu_start(ENTRY,STOP,count=300)
    if u.reg_read(UC_ARM_REG_PC)!=STOP or u.reg_read(UC_ARM_REG_SP)!=STACK or u.reg_read(UC_ARM_REG_CPSR)&63!=16 or[u.reg_read(x)for x in REGS[4:12]]!=initial[4:12]:raise ValueError('510 actual native return failed')
    wanted=struct.pack('<I',fill)*(count//4)+bytes([0xA5])*(512-count)
    if bytes(u.mem_read(DEST,512))!=wanted:raise ValueError('510 independent native fill model differs')
    output=[u.reg_read(reg)for reg in REGS]
    if output[:4]!=[fill,DEST+count,fill,fill]:raise ValueError('510 native volatile output registers differ')
    return dict(fill=fill,count=count,incomingR3=r3,returnedRegisters=output,destinationSha256=c.sha(wanted),instructions=instructions,observedOwnCodeBytes=len(observed)*4,actualNativeReturns=1)


def run():
    meta,image,unused=measured_module('main');cases=[]
    for fill in[0,0x12345678]:
        for count in[0,4,32,36,256]:
            group=[execute(image,fill,count,r3)for r3 in[0,0xFFFFFFFF,0x021E9BD8,0x00020404]]
            if any(x['returnedRegisters']!=group[0]['returnedRegisters']or x['destinationSha256']!=group[0]['destinationSha256']for x in group):raise ValueError('510 incoming R3 changed native outputs')
            cases+=group
    span=image[ENTRY-BASE:ENTRY-BASE+SIZE]
    if span[0x14:0x18]!=bytes.fromhex('0230a0e1'):raise ValueError('510 unconditional MOV R3,R2 opcode differs')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=meta['sha256'],address=hex(ENTRY),mode='arm',bytes=SIZE,nativeSpanSha256=c.sha(span),sourceCredit=0,evidenceClass='original native execution plus independent fill/register model',actualNativeReturns=len(cases),providedCalls=0,comparedGroupCount=10,cases=cases,staticEvidence=dict(firstIncomingR3WritePc='0x02008C6C',instruction='MOV R3,R2',earlierInstructionsDoNotReadR3=True),generatorSha256=sha256(__file__),reproductionCommand='python probe_main_clear510_20261101.py',limits=['Only this hash-qualified ARM9 main helper and aligned lengths0/4/32/36/256 are exercised','Constructor509 differences occur at a4-byte clear call; original R3 is overwritten before any use','This does not declare fourth words unused in any other helper orchange accepted C prototypes','No original assembly provenance ornew reconstructed source is credited','Final physical registers,memory effects,mode,stack andcallee-saved registers are checked on every native return'])
    write_json(ROOT/'evidence/verification/main-clear510-r3-consumption-20261101.json',report);print(json.dumps(dict(actualNativeReturns=len(cases),providedCalls=0,independentGroups=10)))

if __name__=='__main__':run()
