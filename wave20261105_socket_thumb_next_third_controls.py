import os
import subprocess
from project import ROOT,sha256,read_json
import match_runtime as C
from wave20261105_socket_thumb_next_compiler import COMPILER
from wave20261105_socket_thumb_next_third_bindings import negative_controls

REFERENCE='deps/reference/nitrowifi-e6048fc29448-socket-thumb-next'
HEADER_SHA='a50f467431d9e3334b6c5d63428b3cf979f9373d84fb0b491de6bfbe75b1895d'
MANIFEST_SHA='6f06b4fd80ce55d40bb2472aeaf0c43110139d87d7f70bc602755469076d97c5'


def execute(rows):
    directory=ROOT/'work/w5st/third-controls';directory.mkdir(parents=True,exist_ok=True)
    flags=C.FLAGS[:];flags[0]='-O4,p';flags[flags.index('-inline')+1]='on,noauto';flags+=['-ipa','file','-lang','c99','-thumb']
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/third/context.h'
    original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    def compile_text(text):
        (directory/'context.h').write_text(text)
        return compile_source(source,output,flags)
    result=compile_text(original)
    if result.returncode:raise ValueError(('Actual private Thumb layouts failed',result.stdout,result.stderr))
    positive=dict(sourceSha256=sha256(source),headerSha256=sha256(header),objectSha256=sha256(output),packetPrefix14=True,addressPrefix84=True,word32=True,pointer32=True)
    failures=[]
    for label,old,new in [('packet-byte-offset','u8 opaque0[12]','u8 opaque0[13]'),('server-offset','u8 opaque0[32]','u8 opaque0[28]'),('lease-offset','u8 opaque3C[16]','u8 opaque3C[12]')]:
        if original.count(old)!=1:raise ValueError('Actual private layout mutation ambiguous')
        result=compile_text(original.replace(old,new))
        if result.returncode==0 or 'illegal constant expression' not in result.stdout:raise ValueError(('Wrong private Thumb layout admitted',label,result.stdout,result.stderr))
        failures.append(dict(case=label,rejected=True,stdout=result.stdout,stderr=result.stderr,exitCode=result.returncode))
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=failures,projectionAbi=projection_abi(header,directory,flags),publicComparison=public_reference(directory,flags))


def compile_source(source,output,flags):
    command=[str(COMPILER),*flags,'-c',str(source),'-o',str(output)]
    env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    return subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)


def projection_abi(header,directory,flags):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'abi.c';output=directory/'abi.o'
    source.write_text('#include "context.h"\nu32 abi_header(TransportHeader *p){return p->dataOffset12;}\nu32 abi_flags(TransportHeader *p){return p->flags13;}\nu32 abi_timer(AddressState *p){return p->timer38>>1;}\n')
    def probe(text):
        (directory/'context.h').write_text(text);process=compile_source(source,output,flags)
        if process.returncode:raise ValueError(('Actual Thumb ABI compile failed',process.stdout,process.stderr))
        records=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset,width,values in [('abi_header',12,1,range(256)),('abi_flags',13,1,range(256)),('abi_timer',56,4,[0,1,119,120,0x80000000,0xfffffffe,0xffffffff])]:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value']&~1;body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Fresh Thumb ABI mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                for value in values:
                    vm.mem_write(0x02301000,bytes(84));vm.mem_write(0x02301000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_R0,0x02301000);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    actual=vm.reg_read(R.UC_ARM_REG_R0);expected=value>>1 if name=='abi_timer' else value
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual unsigned Thumb projection differs',name,value,actual,expected))
                    records.append(dict(function=name,input=value,returned=actual))
        return dict(sourceSha256=sha256(source),objectSha256=sha256(output),actualNativeAbiProbeReturns=len(records),cases=records,originalGameOrProviderBodiesExecuted=0)
    original=header.read_text();positive=probe(original);failures=[]
    for label,old,new in [('signed-header','u8 dataOffset12;','signed char dataOffset12;'),('signed-flags','u8 flags13;','signed char flags13;'),('signed-timer','u32 timer38;','s32 timer38;')]:
        if original.count(old)!=1:raise ValueError('Actual Thumb signed projection mutation ambiguous')
        try:probe(original.replace(old,new))
        except ValueError as error:failures.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong signed Thumb projection accepted')
    return dict(status='passed',sourceCredit=0,positive=positive,negative=failures)


def public_reference(directory,flags):
    reference=ROOT/REFERENCE;header=reference/'include/nitroWiFi/cps.h';manifest=reference/'reference-manifest.json'
    if sha256(header)!=HEADER_SHA or sha256(manifest)!=MANIFEST_SHA:raise ValueError('Immutable public comparison reference changed')
    meta=read_json(manifest)
    if meta['commit']!='e6048fc294480831e154b3d53205d6cbda1775cd' or meta['files'][0]['sha256']!=HEADER_SHA:raise ValueError('Public comparison reference lineage differs')
    source=directory/'public-layout.c';output=directory/'public-layout.o'
    prelude='typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef signed int s32;typedef unsigned long long u64;typedef int BOOL;typedef struct OSThread OSThread;typedef struct MATHRandContext32 MATHRandContext32;extern u64 OS_GetTick(void);\n'
    fields={'thread':0,'block_type':4,'state':8,'ssl':9,'local_port':10,'con':12,'when':16,'local_ip_real':20,'remote_port':24,'remote_port_bound':26,'remote_ip':28,'remote_ip_bound':32,'ackno':36,'seqno':40,'remote_win':44,'remote_mss':46,'remote_ackno':48,'ackrcvd':52,'udpread_callback':56,'rcvbuf':60,'rcvbufp':68,'sndbuf':72,'linbuf':80,'outbuf':88,'outbufp':96}
    assertions=' && '.join('(u32)&((CPSSoc *)0)->'+field+'=='+str(offset) for field,offset in fields.items())
    text=prelude+'#include "'+header.as_posix()+'"\ntypedef char SocketLayout[(sizeof(CPSSoc)==100 && '+assertions+')?1:-1];\ntypedef char BufferLayout[(sizeof(CPSSocBuf)==8 && (u32)&((CPSSocBuf *)0)->data==4)?1:-1];\ntypedef char StateValues[(CPS_STT_CLOSED==0 && CPS_STT_SYN_SENT==2 && CPS_STT_ESTABLISHED==4 && CPS_STT_DATAGRAM==10 && CPS_STT_PING==11 && CPS_BLOCK_UDPREAD==3)?1:-1];\n'
    source.write_text(text);result=compile_source(source,output,flags)
    if result.returncode:raise ValueError(('Actual public comparison ABI layout failed',result.stdout,result.stderr))
    negative=text.replace('sizeof(CPSSoc)==100','sizeof(CPSSoc)==104');wrong=directory/'public-wrong-layout.c';wrong.write_text(negative);process=compile_source(wrong,directory/'public-wrong-layout.o',flags)
    if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError('Wrong public ABI size admitted')
    return dict(status='passed',sourceCredit=0,header=dict(path=header.relative_to(ROOT).as_posix(),sha256=HEADER_SHA),manifest=dict(path=manifest.relative_to(ROOT).as_posix(),sha256=MANIFEST_SHA),sourceSha256=sha256(source),objectSha256=sha256(output),all25PublicFields=fields,publicStructBytes=100,nativeCompilerExitCode=0,wrongSizeRejected=True,productionCompilerInput=False,originalGameOrProviderBodiesExecuted=0,limits=['This public header layout/enumeration comparison does not establish the exact native library version, routine names, complete original storage ownership or original public declarations. Production units remain closed independently measured private C/header inputs.'])
