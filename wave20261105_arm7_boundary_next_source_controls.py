import os
import subprocess
from project import ROOT,sha256,write_json
import match_runtime as C
from elftools.elf.elffile import ELFFile
from wave20261105_arm7_boundary_next_source_build import SOURCE,LANE,WORK,COMPILER,FLAGS
from wave20261105_arm7_boundary_next_source_bindings import controls as binding_controls
from wave20261105_arm7_boundary_next_source_callables import controls as callable_controls
EXPECTED=[5520,2000,720,20,40,88,5452,5456,194,48,0,2,8,8,0,2]


def compile_unit(source,output):
    process=subprocess.run([str(COMPILER),*FLAGS,'-c',str(source),'-o',str(output)],cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if process.returncode:raise ValueError(('Actual closed ARM7 layout/ABI compile failed',process.stdout,process.stderr))


def geometry(directory):
    text='\n'.join('#include "context%03d.h"'%i for i in range(5))+'\n#define OFF(T,F) ((u32)&((T*)0)->F)\nconst u32 geometry[]={sizeof(WMSPWork),sizeof(WMStatus),sizeof(WMArm7Buf),sizeof(WlCmdReq),OFF(WMSPWork,fromWLmsgQ),OFF(WMSPWork,confirmQ),OFF(WMSPWork,wm7buf),OFF(WMSPWork,status),OFF(WMStatus,beaconIndicateFlag),sizeof(WMStartParentCallback),OFF(WMStartParentCallback,apiid),OFF(WMStartParentCallback,errcode),OFF(WMStartParentCallback,state),WM_APIID_START_PARENT,WM_ERRCODE_SUCCESS,WM_STATECODE_BEACON_SENT};\n'
    source=directory/'geometry.c';source.write_text(text);output=directory/'geometry.o';compile_unit(source,output)
    with output.open('rb') as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name=='geometry');raw=elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value']+symbol['st_size']];values=[int.from_bytes(raw[i:i+4],'little') for i in range(0,len(raw),4)]
    if values!=EXPECTED:raise ValueError(('Actual source/compiler geometry differs from independently observed member-width/offset expectations',values,EXPECTED))
    return dict(sourceSha256=sha256(source),objectSha256=sha256(output),values=values,originalStorageExtentCredit=0,limits=['Complete SDK-comparison type sizes are compiler checks, not proof of original allocation extents; observed original member widths/offsets are independently required by exact whole native code.'])


def abi(directory):
    import unicorn
    from unicorn import arm_const as R
    text='\n'.join('#include "context%03d.h"'%i for i in range(5))+'\nu32 abi_beacon(WMStatus *p){return p->beaconIndicateFlag;}\nu32 abi_state(WMStatus *p){return p->state;}\nu32 abi_code(WlCmdReq *p){return p->header.code;}\nu32 abi_poll(void *p){return(u16)(u32)p;}\n';source=directory/'abi.c';output=directory/'abi.o'
    def evaluate(payload):
        source.write_text(payload);compile_unit(source,output);results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset in [('abi_beacon',194),('abi_state',0),('abi_code',12),('abi_poll',None)]:
                s=next(s for s in symbols if s.name==name);body=elf.get_section(s['st_shndx']).data()[s['st_value']:s['st_value']+s['st_size']]
                if s['st_info']['type']!='STT_FUNC' or not any(t.name=='$a' and t['st_value']==s['st_value'] and t['st_shndx']==s['st_shndx'] for t in symbols):raise ValueError('Fresh ARMv4T ABI mapping differs')
                for value in [0,1,32767,32768,65535]:
                    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_TI925T);vm.mem_map(0x02000000,0x10000);vm.mem_write(0x02000000,body);vm.reg_write(R.UC_ARM_REG_CPSR,0x10);argument=value|0xabcd0000 if offset is None else 0x02002000
                    if offset is not None:vm.mem_write(argument+offset,value.to_bytes(2,'little'))
                    vm.reg_write(R.UC_ARM_REG_R0,argument);vm.reg_write(R.UC_ARM_REG_SP,0x0200f000);vm.reg_write(R.UC_ARM_REG_LR,0x02001000);vm.emu_start(0x02000000,0x02001000,count=64);actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=value or vm.reg_read(R.UC_ARM_REG_PC)!=0x02001000:raise ValueError(('Actual fresh ARMv4T unsigned-field/callback-low16 ABI differs',name,value,actual))
                    results.append(dict(function=name,fieldInput=value,argument=argument,returned=actual))
        return dict(actualFreshAbiReturns=len(results),cases=results,sourceSha256=sha256(source),objectSha256=sha256(output))
    positive=evaluate(text);bad=[]
    for label,old,new in [('beacon-signed','return p->beaconIndicateFlag','return(s16)p->beaconIndicateFlag'),('command-truncated','return p->header.code','return(u8)p->header.code'),('poll-untruncated','return(u16)(u32)p','return(u32)p')]:
        if text.count(old)!=1:raise ValueError('ABI mutation ambiguous')
        try:evaluate(text.replace(old,new))
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong ARM7 ABI probe admitted')
    source.write_text(text);return dict(positive=positive,negative=bad,sourceCredit=0,originalImportedBodiesExecuted=0)


def execute(row):
    if SOURCE!=ROOT/'src/arm7/parallel_wave20261105/arm7-boundary-next' or LANE!=ROOT/'evidence/lanes/parallel-wave20261105/arm7-boundary-next/source' or WORK!=ROOT/'work/w5ab-source':raise ValueError('New ARM7 source/evidence controls materializer scope changed')
    directory=WORK/'controls';directory.mkdir(parents=True,exist_ok=True);headers={p.name:p.read_bytes() for p in SOURCE.glob('*.h')}
    for name,raw in headers.items():(directory/name).write_bytes(raw)
    positive=geometry(directory);bad=[]
    for label,name,old,new in [('message-queue-offset','context002.h','OSMessageQueue fromWLmsgQ;','u32 movedFromWL;OSMessageQueue fromWLmsgQ;'),('wm7buf-offset','context002.h','WMArm7Buf *wm7buf;','u32 movedWm7;WMArm7Buf *wm7buf;'),('beacon-flag-width','context001.h','u16 beaconIndicateFlag;','u32 beaconIndicateFlag;')]:
        text=headers[name].decode()
        if text.count(old)!=1:raise ValueError('Private ARM7 geometry mutation ambiguous')
        (directory/name).write_text(text.replace(old,new))
        try:geometry(directory)
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong private ARM7 geometry admitted')
        (directory/name).write_bytes(headers[name])
    from wave20261105_arm7_boundary_next_source_c99 import execute as c99
    return dict(status='passed',sourceCredit=0,geometry=positive,wrongGeometry=bad,fieldAbi=abi(directory),bindingControls=binding_controls(row),callableControls=callable_controls(),actualC99Frontend=c99(row))
