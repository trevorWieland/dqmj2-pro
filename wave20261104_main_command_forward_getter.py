import shutil
import json
import struct
import match_runtime as C
import unicorn as un
from unicorn import arm_const as ar
from project import ROOT,read_json,write_json,sha256
from wave20261104_main_command_forward_build import build

LANE=ROOT/'evidence/lanes/parallel-wave20261104/main-command-forward'
WORK=ROOT/'work/w4mcf/getter-fixture'
BASE,GLOBAL,STOP,SP=0x02000000,0x02102dc0,0x027e0000,0x02701000


def run(image,address,body,value,flags):
    cpu=un.Uc(un.UC_ARCH_ARM,un.UC_MODE_ARM);cpu.ctl_set_cpu_model(ar.UC_CPU_ARM_946)
    cpu.mem_map(BASE,0x200000);cpu.mem_write(BASE,image);cpu.mem_write(address,body)
    cpu.mem_map(STOP,0x1000);cpu.mem_map(SP-0x1000,0x1000)
    data=bytes([0x31,0x72,0xb4,0xf0,1,2,3,value^255,value]);cpu.mem_write(GLOBAL,data)
    initial=[0x11220000+i*0x101+value for i in range(15)];initial[-2:]=[SP,STOP]
    cpu.reg_write(ar.UC_ARM_REG_CPSR,flags)
    for reg,word in zip(C.REGISTERS,initial):cpu.reg_write(reg,word)
    reads=[];pcs=[];returned=False
    def code(machine,at,size,user):
        nonlocal returned
        if at==STOP:returned=True;machine.emu_stop()
        else:pcs.append(hex(at))
    cpu.hook_add(un.UC_HOOK_CODE,code)
    cpu.hook_add(un.UC_HOOK_MEM_READ,lambda machine,access,at,size,word,user:reads.append([hex(at),size]))
    cpu.emu_start(address,STOP+4,count=8)
    registers=[cpu.reg_read(reg) for reg in C.REGISTERS];state=bytes(cpu.mem_read(GLOBAL,9))
    if not returned or registers[1:13]!=initial[1:13] or registers[13]!=SP or cpu.reg_read(ar.UC_ARM_REG_CPSR)!=flags or state!=data:raise ValueError('Getter did not preserve independent ABI/memory/flags or return')
    return dict(actualTopReturn=True,r0=registers[0],registers=registers,cpsr=cpu.reg_read(ar.UC_ARM_REG_CPSR),globalBytes=state.hex(),reads=reads,pcs=pcs)


def execute(rows):
    row=next(r for r in rows if r['address']=='0x205be14');directory=WORK/'wrong-field';directory.mkdir(parents=True,exist_ok=True)
    source=ROOT/row['source'];text=source.read_text()
    if text.count('native_data_02102dc0.field8')!=1:raise ValueError('Typed getter expression not isolated')
    wrong=directory/'source.c';wrong.write_text(text.replace('native_data_02102dc0.field8','native_data_02102dc0.reserved[7]'))
    shutil.copyfile(source.with_name('context.h'),wrong.with_name('context.h'))
    bad,badbody=build(wrong,directory/'build',True)
    if bad['compiledBytes']!=16 or bad['realLink']['linkerAttempt']['exitCode']!=0 or bad['realLink']['exactCallerBytes']:raise ValueError('Wrong typed field must genuinely compile/link complete16B and fail bytes')
    image=(ROOT/'extract/arm9/arm9.bin').read_bytes();native=image[0x5be14:0x5be24];linked=(ROOT/row['realLink']['linkedElf']).with_name('caller.bin').read_bytes();records=[]
    for value in range(256):
        flags=(value&15)<<28|0x10
        original,rebuilt,negative=[run(image,0x0205be14,body,value,flags) for body in [native,linked,badbody]]
        if original!=rebuilt or original['r0']!=value or original['reads']!=[['0x205be20',4],['0x2102dc8',1]] or negative['r0']==value:raise ValueError('Independent unsigned-byte getter model/control failed')
        records.append(dict(value=value,original=original,recompiled=rebuilt,wrongFieldR0=negative['r0']))
    result=dict(traceSha256=C.sha(json.dumps(records,sort_keys=True,separators=(',',':')).encode()),status='passed',address=row['address'],supportedReturningVectors=256,nativeAndCompiledReturningCalls=512,wrongReturningControls=256,wrongFieldCasesRejected=256,actualNativeCalleeOrDeviceExecutions=0,originalObjectStorageCredit=0,unicornVersion=un.__version__,wrongC=dict(source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),compiledBytes=16,realLink=bad['realLink']),records=records,limits=['All256 unsigned-byte values execute the complete original and actual real-linked16B getter with independently supplied original-data bytes, preserved GPR/SP/CPSR/memory and actual top return.','Original storage extent/authorship, game invariants, hardware and other functions remain unproved; no imports execute.'])
    write_json(LANE/'getter-fixtures.json',result)
    return {k:v for k,v in result.items() if k not in ['records','wrongC']}
