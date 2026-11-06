import os
import shutil
import subprocess
from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_compiler import COMPILER
from wave20261105_socket_thumb_next_second_bindings import negative_controls


def execute(rows):
    binding=negative_controls(rows)
    directory=ROOT/'work/w5st/second-controls'
    directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/second/context.h'
    source=directory/'layout.c';source.write_text('#include "context.h"\n')
    output=directory/'layout.o'
    flags=C.FLAGS[:];flags[0]='-O4,p';flags[flags.index('-inline')+1]='on,noauto';flags+=['-ipa','file','-lang','c99','-thumb']
    command=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)]
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    original=header.read_text();(directory/'context.h').write_text(original)
    result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if result.returncode:raise ValueError(('Actual Thumb geometry assertions failed',result.stdout,result.stderr))
    positive=dict(compilerSha256=sha256(COMPILER),headerSha256=sha256(header),objectSha256=sha256(output),nativeLayoutAssertions=5,exitCode=0,word32=True,pointer32=True,SocketPrefix100=True,ThreadPrefix168=True,SingletonPrefix8=True,AddressPrefix84=True)
    failures=[]
    for label,old,new in [('socket-halfword-offset','u8 opaque14[4]','u8 opaque14[2]'),('thread-pointer-offset','u8 opaque0[0xa4]','u8 opaque0[0xa0]'),('singleton-pointer-offset','Singleton { u32 opaque0;','Singleton { u32 opaque0[2];'),('address-offset','opaque0[0x50]','opaque0[0x4c]'),('buffer-pointer-offset','u32 capacity3C;','u32 capacity3C[2];')]:
        if original.count(old)!=1:raise ValueError('Actual Thumb layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new))
        result=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
        if result.returncode==0 or 'illegal constant expression' not in result.stdout:raise ValueError(('Wrong Thumb field layout accepted',label,result.stdout,result.stderr))
        failures.append(dict(case=label,rejected=True,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    return dict(status='passed',sourceCredit=0,bindingControls=binding,nativeCompilerLayout=positive,wrongLayouts=failures,projectionAbi=projection_abi(header,directory,flags),returnPairAbi=return_pair_abi(header,directory,flags))


def projection_abi(header,directory,flags):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'abi.c';source.write_text('#include "context.h"\nu32 abi_state(SocketView *p){return p->state8;}\nu32 abi_port(SocketView *p){return p->portA;}\n')
    output=directory/'abi.o'
    command=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)]
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))

    def probe(text):
        (directory/'context.h').write_text(text)
        process=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
        if process.returncode:raise ValueError(('Actual Thumb ABI compile failed',process.stdout,process.stderr))
        records=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset,width,values in [('abi_state',8,1,range(256)),('abi_port',10,2,[0,1,127,128,255,32767,32768,65534,65535])]:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value']&~1;body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Fresh Thumb ABI mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                for value in values:
                    vm.mem_write(0x02301000,bytes(100));vm.mem_write(0x02301000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_R0,0x02301000);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=value or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual unsigned Thumb byte/halfword ABI differs',name,value,actual))
                    records.append(dict(field=name,input=value,returned=actual))
        return dict(sourceSha256=sha256(source),objectSha256=sha256(output),actualNativeAbiProbeReturns=len(records),cases=records,originalGameOrProviderBodiesExecuted=0)

    original=header.read_text();positive=probe(original);failures=[]
    for label,old,new in [('signed-state','u8 state8;','signed char state8;'),('signed-port','u16 portA;','signed short portA;')]:
        if original.count(old)!=1:raise ValueError('Actual Thumb projection mutation ambiguous')
        try:probe(original.replace(old,new))
        except ValueError as error:failures.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong signed Thumb ABI accepted')
    return dict(status='passed',sourceCredit=0,positive=positive,negative=failures)


def return_pair_abi(header,directory,flags):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'pair.c';output=directory/'pair.o'
    original='#include "context.h"\nu64 abi_pair(u32 low,u32 high){return ((u64)high<<32)|low;}\nu32 abi_tick(u64 value){return (u32)(value>>16);}\n'
    command=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)]
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    values=[(0,0),(0xffffffff,0),(0,0xffffffff),(0x89abcdef,0x12345678),(0x80000000,0x7fffffff)]

    def probe(text):
        source.write_text(text);(directory/'context.h').write_text(header.read_text())
        process=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
        if process.returncode:raise ValueError(('Actual two-word Thumb ABI compile failed',process.stdout,process.stderr))
        records=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name in ['abi_pair','abi_tick']:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value']&~1;body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x1000);vm.mem_write(0x02300000,body)
                for low,high in values:
                    vm.reg_write(R.UC_ARM_REG_R0,low);vm.reg_write(R.UC_ARM_REG_R1,high);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02300f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    words=[vm.reg_read(R.UC_ARM_REG_R0),vm.reg_read(R.UC_ARM_REG_R1)]
                    expected=[low,high] if name=='abi_pair' else [(low>>16|high<<16)&0xffffffff]
                    if words[:len(expected)]!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual two-word/tick projection ABI differs',name,low,high,words,expected))
                    records.append(dict(function=name,input=[low,high],returned=words[:len(expected)]))
        return dict(actualNativeAbiProbeReturns=len(records),cases=records,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrProviderBodiesExecuted=0)

    positive=probe(original);negative=[]
    for label,old,new in [('swapped-return-words','((u64)high<<32)|low','((u64)low<<32)|high'),('wrong-tick-shift','value>>16','value>>15')]:
        try:probe(original.replace(old,new))
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong two-word ABI accepted')
    return dict(status='passed',sourceCredit=0,positive=positive,negative=negative)
