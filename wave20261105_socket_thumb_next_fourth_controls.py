from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_bindings import negative_controls
from wave20261105_socket_thumb_next_fourth_callbacks import execute as callbacks,compile_source
from wave20261105_socket_thumb_next_third_controls import public_reference


def execute(rows):
    directory=ROOT/'work/w5st/fourth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fourth/context.h';original=header.read_text()
    source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);result=compile_source(source,output,'thumb')
    if result.returncode:raise ValueError(('Actual datagram geometry failed',result.stdout,result.stderr))
    positive=dict(headerSha256=sha256(header),sourceSha256=sha256(source),objectSha256=sha256(output),socketPrefix100=True,threadPrefix168=True,singletonPrefix12=True,IPPrefix20=True,datagramPrefix8=True)
    failures=[]
    for label,old,new in [('callback-offset','u8 opaque2C[12]','u8 opaque2C[16]'),('thread-list-offset','u8 opaque0[104]','u8 opaque0[100]'),('global-list-offset','u32 opaque0;','u32 opaque0[2];'),('packet-halfword-offset','u16 source0;','u32 source0;')]:
        if original.count(old)!=1:raise ValueError('Actual datagram layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));result=compile_source(source,output,'thumb')
        if result.returncode==0 or 'illegal constant expression' not in result.stdout:raise ValueError(('Wrong datagram layout admitted',label,result.stdout,result.stderr))
        failures.append(dict(case=label,rejected=True,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr))
    (directory/'context.h').write_text(original)
    flags=C.FLAGS[:];flags[0]='-O4,p';flags[flags.index('-inline')+1]='on,noauto';flags+=['-ipa','file','-lang','c99','-thumb']
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=failures,callbackContract=callbacks(rows[0]),publicComparison=public_reference(directory,flags),byteOrderAbi=byte_order(header,directory))


def byte_order(header,directory):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'byte-order.c';output=directory/'byte-order.o'
    source.write_text('#include "context.h"\nu32 abi_half(u16 value){return host16(value);}\nu32 abi_word(u16 *data){return host32(data);}\n')
    original=header.read_text()
    def probe(text):
        (directory/'context.h').write_text(text);process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual byte-order ABI compilation failed',process.stdout,process.stderr))
        results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,values in [('abi_half',[0,1,127,128,255,256,32767,32768,0x1234,0x80ff,0xff80,65535]),('abi_word',[(0,0),(0x0102,0x0304),(0xffff,0xffff),(0x8000,0x7fff),(0x89ab,0xcdef)])]:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual byte-order Thumb mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                for value in values:
                    if name=='abi_half':expected=int.from_bytes(value.to_bytes(2,'little'),'big');argument=value
                    else:
                        raw=value[0].to_bytes(2,'little')+value[1].to_bytes(2,'little');vm.mem_write(0x02301000,raw);expected=int.from_bytes(raw,'big');argument=0x02301000
                    vm.reg_write(R.UC_ARM_REG_R0,argument);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual byte-order ABI differs',name,value,actual,expected))
                    results.append(dict(function=name,input=value,returned=actual))
        return dict(actualFreshByteOrderReturns=len(results),cases=results,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrImportedBodiesExecuted=0)
    positive=probe(original);negative=[]
    for label,old,new in [('signed-half','host16(u16 value)','host16(signed short value)'),('wrong-word-order','((u32)host16(p[0])<<16)|host16(p[1])','((u32)host16(p[1])<<16)|host16(p[0])')]:
        if original.count(old)!=1:raise ValueError('Actual byte-order mutation ambiguous')
        try:probe(original.replace(old,new))
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong byte-order ABI admitted')
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,positive=positive,negative=negative)
