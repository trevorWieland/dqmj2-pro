from pathlib import Path
import json
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
from project import ROOT,sha256,write_json
MAIN=0x027e0000
WRAM=0x037f8000
DATA=0x023c0000
STACK=0x03030000
IO=0x04808000
STOP=0x0f000000
REPORT=ROOT/'evidence/attempts/arm7-core124-helper128-native-probe-20261101.json'


def main():
    arm_main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();results=[]
    for seed in range(4):
        cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        for base,raw in[(MAIN,arm_main+bytes(0x20000-len(arm_main))),(WRAM,wram+bytes(0x18000-len(wram))),(DATA,bytes(0x8000)),(STACK,bytes(0x4000)),(IO,bytes(0x1000)),(STOP,bytes(0x1000))]:cpu.mem_map(base,len(raw));cpu.mem_write(base,raw)
        cpu.mem_write(DATA+0x7000,struct.pack('<I',DATA+0x40));cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP);cpu.emu_start(0x27e89ec,0x27e8a10,count=10000)
        if cpu.reg_read(UC_ARM_REG_PC)!=0x27e8a10 or int.from_bytes(cpu.mem_read(0x380fff4,4),'little')!=DATA+0x40:raise ValueError('Real original prefix/clear did not reach bound')
        for i,value in enumerate([0x11223344+j*0x10203+seed for j in range(15)]):cpu.reg_write(REGISTERS[i],value&0xffffffff)
        cpu.reg_write(REGISTERS[-2],STACK+0x3800);cpu.reg_write(REGISTERS[-1],STOP);visited=[];invalid=[];returned=[False]
        def code(machine,pc,size,user):
            if pc==STOP:returned[0]=True;machine.emu_stop();return
            if not(MAIN<=pc<MAIN+len(arm_main)or WRAM<=pc<WRAM+len(wram)):raise ValueError('Exploratory fetch left measured initialized ARM7 images')
            visited.append(pc)
        def bad(machine,access,address,size,value,user):invalid.append(dict(access=access,address=hex(address),bytes=size,value=value));return False
        cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_INVALID,bad);error=None
        try:cpu.emu_start(0x27e9bd8,STOP+4,count=100000)
        except Exception as exception:error=type(exception).__name__+': '+str(exception)
        results.append(dict(seed=seed,observedStopReturn=returned[0],returnR0=cpu.reg_read(REGISTERS[0])if returned[0]else None,pc=hex(cpu.reg_read(UC_ARM_REG_PC)),instructions=len(visited),uniqueVisited=[hex(x)for x in sorted(set(visited))],invalidMemory=invalid,error=error,rawRegisters=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),sourceCredit=0,validatedReturnOrPostStateCredit=0,broadExploratoryFetchMapNotFullBoundaryProof=True))
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),results=results,mainSha256=sha256(ROOT/'extract/arm7/runtime/arm7-main.bin'),wramSha256=sha256(ROOT/'extract/arm7/runtime/arm7-wram.bin'),codePoolBoundariesNotYetQualified=True,sourceCredit=0);write_json(REPORT,report);print(json.dumps([dict(seed=r['seed'],stop=r['observedStopReturn'],pc=r['pc'],instructions=r['instructions'],error=r['error'],invalid=r['invalidMemory'])for r in results]),flush=True)
if __name__=='__main__':main()
