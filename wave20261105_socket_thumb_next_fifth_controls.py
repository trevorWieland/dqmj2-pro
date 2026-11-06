import itertools
import re
from project import ROOT,sha256,read_json
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_fifth_bindings import negative_controls,inputs
from elftools.elf.elffile import ELFFile

REFERENCE='deps/reference/nitrosdk-eaae40f199c0-socket-random'
HEADER_SHA='519901610b2d0f0908b8eb62eb348ffe7b2395245b110764ddd3ddb9703962e0'
MANIFEST_SHA='ce400f855c47b8be362fbf6ef95affb7ae9435f99dc984476e976c4a43e8f336'


def execute(rows):
    directory=ROOT/'work/w5st/fifth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fifth/context.h';original=header.read_text();source=directory/'layout.c';output=directory/'layout.o';source.write_text('#include "context.h"\n')
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual128-byte/64-bit source geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,word64=True,privatePrefix128=True,seed104=True,multiplier112=True,increment120=True)
    negative=[]
    for label,old,new in [('context-offset','u8 opaque0[104]','u8 opaque0[96]'),('seed-width','u64 seed68;','u32 seed68;'),('multiplier-width','u64 multiplier70;','u32 multiplier70;'),('increment-width','u64 increment78;','u32 increment78;')]:
        if original.count(old)!=1:raise ValueError('Actual128-byte context mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong64-bit context geometry admitted',label,process.stdout,process.stderr))
        negative.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    reference=ROOT/REFERENCE;public=reference/'include/nitro/math/rand.h';manifest=reference/'reference-manifest.json'
    if sha256(public)!=HEADER_SHA or sha256(manifest)!=MANIFEST_SHA:raise ValueError('Immutable public64-bit comparison changed')
    if read_json(manifest)['commit']!='eaae40f199c0a8827947afbc33227b6ba2f9d45c':raise ValueError('Public64-bit comparison commit differs')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=negative,pairAbi=pair_abi(directory),originalPrimitiveAbi=original_primitive(),publicReference=dict(header=dict(path=public.relative_to(ROOT).as_posix(),sha256=HEADER_SHA),manifest=dict(path=manifest.relative_to(ROOT).as_posix(),sha256=MANIFEST_SHA),productionCompilerInclude=False,exactNativeVersionOrNamesClaimed=False))


def pair_abi(directory):
    import unicorn
    from unicorn import arm_const as R
    source=directory/'pair.c';output=directory/'pair.o'
    original='#include "context.h"\nu64 abi_add(u64 first,u64 second){return first+second;}\nu32 abi_range(u64 value){return (u32)(((value>>32)*65536)>>32);}\n'
    values=[0,1,0xffffffff,0x100000000,0x8000000000000000,0x89abcdef01234567,0xffffffffffffffff]
    def probe(text):
        source.write_text(text);process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual unsigned64 ABI compile failed',process.stdout,process.stderr))
        results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name in ['abi_add','abi_range']:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual unsigned64 Thumb mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                pairs=itertools.product(values,repeat=2) if name=='abi_add' else [(value,0) for value in values]
                for first,second in pairs:
                    args=[first&0xffffffff,first>>32,second&0xffffffff,second>>32]
                    for reg,value in zip(C.REGISTERS,args):vm.reg_write(reg,value)
                    vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    actual=vm.reg_read(R.UC_ARM_REG_R0)|(vm.reg_read(R.UC_ARM_REG_R1)<<32) if name=='abi_add' else vm.reg_read(R.UC_ARM_REG_R0)
                    expected=(first+second)&((1<<64)-1) if name=='abi_add' else first>>48
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual unsigned64 carry/range ABI differs',name,first,second,actual,expected))
                    results.append(dict(function=name,arguments=args,returned=actual))
        return dict(actualFreshProbeReturns=len(results),cases=results,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrImportedBodiesExecuted=0)
    positive=probe(original);negative=[]
    for label,old,new in [('lost-carry','return first+second','return (u32)first+(u32)second'),('wrong-range-scale','*65536','*32768')]:
        try:probe(original.replace(old,new))
        except ValueError as error:negative.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong unsigned64 arithmetic ABI admitted')
    return dict(status='passed',sourceCredit=0,positive=positive,negative=negative)


def original_primitive():
    import unicorn
    from unicorn import arm_const as R
    value,image,inventory,records,imports=inputs();address=0x02026124;size=32
    canonical=next((line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(arm,size=0x20\) addr:0x02026124',line)),None)
    if canonical is None:raise ValueError('Actual original two64-word primitive entry absent')
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,image)
    stop=0x027e0000;stack=0x027f0000
    def code(uc,at,width,user):
        if at==stop:uc.emu_stop();return
        if not address<=at<address+size:raise ValueError('Unexpected original primitive/callee execution')
    vm.hook_add(unicorn.UC_HOOK_CODE,code);cases=[];values=[0,1,0xffffffff,0x100000000,0x8000000000000000,0x89abcdef01234567,0xffffffffffffffff]
    for first,second in itertools.product(values,repeat=2):
        initial=[first&0xffffffff,first>>32,second&0xffffffff,second>>32]+[0x11220000+i for i in range(4,13)]+[stack,stop]
        vm.reg_write(R.UC_ARM_REG_CPSR,0x10)
        for reg,number in zip(C.REGISTERS,initial):vm.reg_write(reg,number)
        vm.emu_start(address,stop+4,count=100)
        regs=[vm.reg_read(reg) for reg in C.REGISTERS];actual=regs[0]|regs[1]<<32;expected=first*second&((1<<64)-1)
        if actual!=expected or regs[4:12]!=initial[4:12] or regs[13]!=stack or vm.reg_read(R.UC_ARM_REG_PC)!=stop:raise ValueError(('Actual original primitive ABI/result differs',first,second,actual,expected))
        cases.append(dict(arguments=[first,second],returned=actual))
    return dict(status='passed',sourceCredit=0,originalHelperBody=hex(address),mode='arm',bytes=size,nativeSha256=C.sha(image[address-0x02000000:address-0x02000000+size]),canonicalInventoryRecord=canonical,actualOriginalHelperReturns=len(cases),distinctOriginalHelpersExecuted=1,actualGameCallerExecutions=0,calleeSourceCredit=0,cases=cases,limits=['Separate bounded49-case ABI qualification executes the existing original32-byte primitive only. It supplies no reconstructed primitive source credit or general game/platform execution claim; caller fixtures continue to intercept it.'])
