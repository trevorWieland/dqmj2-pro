import json
import match_runtime
import crossreuse_utility_c
from elftools.elf.elffile import ELFFile
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_PC,UC_ARM_REG_CPSR
from project import ROOT,sha256,write_json
WORK=ROOT/'work/arm7-bulk-20261030/lane-card-abi16-layout-probe'
SOURCE=ROOT/'nonmatching/arm7-bulk/20261031/lane-card-abi16-layout-probe/layout_probe.c'
HEADER=ROOT/'src/arm7/lane_20261031_card_abi16/native_card_types.h'
EXPECTED=[16,0,4,8,12,4,12,16,72,240,164]


def measure(name,header):
    directory=WORK/name;directory.mkdir(parents=True,exist_ok=True)
    source=directory/SOURCE.name;source.write_bytes(SOURCE.read_bytes())
    include=directory/HEADER.name;include.write_text(header,encoding='utf-8')
    pin=json.loads((ROOT/'nonmatching/arm7-bulk/20261031/lane-card-abi16-1252-final/closure.json').read_text())['matches'][0]
    origin=dict(name='card_layout_probe',source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source))
    attempt,compiled=crossreuse_utility_c.compile_origin(origin,ROOT/pin['compiler'],pin['compilerFlags'],directory)
    if compiled is None:return dict(compilerRejected=True,attempt=attempt,sourceCredit=0)
    derived,masks,body=compiled
    if derived['relocations']:raise ValueError('ABI probe unexpectedly needs unqualified linking')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base in (0x02000000,0x02100000,0x02200000,0x02300000):cpu.mem_map(base,0x1000)
    cpu.mem_write(0x02000000,body);cpu.mem_write(0x02100000,bytes(44))
    cpu.reg_write(UC_ARM_REG_CPSR,0x1f)
    for i,register in enumerate(match_runtime.REGISTERS):cpu.reg_write(register,0x200+i)
    cpu.reg_write(match_runtime.REGISTERS[0],0x02100000);cpu.reg_write(match_runtime.REGISTERS[13],0x02200800);cpu.reg_write(match_runtime.REGISTERS[14],0x02300000)
    cpu.emu_start(0x02000000,0x02300000,count=1000,timeout=500000)
    if cpu.reg_read(UC_ARM_REG_PC)!=0x02300000:raise ValueError('ABI compiler probe did not actually return')
    values=[int.from_bytes(cpu.mem_read(0x02100000+4*i,4),'little') for i in range(11)]
    return dict(compilerRejected=False,actualProbeReturn=True,layout=values,expected=EXPECTED,matchesNativeMeasuredOffsets=values==EXPECTED,
        headerSha256=sha256(include),sourceSha256=sha256(source),objectSha256=derived['probeObjectSha256'],compiler=pin['compiler'],compilerSha256=pin['compilerSha256'],compilerFlags=pin['compilerFlags'],sourceCredit=0)


def main():
    header=HEADER.read_text();positive=measure('full16',header)
    if not positive.get('matchesNativeMeasuredOffsets'):raise ValueError('Shared complete ABI does not match measured native offsets')
    results=[]
    for name,old,new in (('missing-word','    u32 matched;',''),('narrow-word','    u32 matched;','    u16 matched;'),('short-thread','contextAndThreadWords[41]','contextAndThreadWords[40]')):
        changed=header.replace(old,new)
        if changed==header:raise ValueError('Expected ABI mutant token missing')
        result=measure(name,changed)
        if not result.get('compilerRejected') and result.get('matchesNativeMeasuredOffsets'):raise ValueError('Incorrect ABI layout accepted')
        results.append(dict(name=name,rejected=True,result=result))
    report=ROOT/'evidence/verification/arm7-card-shared-layout-20261031.json'
    write_json(report,dict(generator='prove_arm7_card_shared_layout_20261031.py',generatorSha256=sha256(__file__),
        sharedDeclaration=dict(path=HEADER.relative_to(ROOT).as_posix(),sha256=sha256(HEADER)),positive=positive,controls=results,
        acceptedSourcesChanged=False,newSourceCredit=0,hardwareCredit=0,
        limitations='Auxiliary ordinary C compiler-layout probe only; no original executable region or decompilation bytes are credited. Member offsets are independently measured native ABI requirements.'))
    print(dict(report=report.relative_to(ROOT).as_posix(),sha256=sha256(report),layout=positive['layout'],negativeControls=len(results),sourceCredit=0))


if __name__=='__main__':main()
