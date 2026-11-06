import itertools
from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_seventh_bindings import negative_controls
from wave20261105_socket_thumb_next_seventh_callbacks import execute as callbacks

REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}]


def execute(rows):
    directory=ROOT/'work/w5st/seventh-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/seventh/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual shared command/queue geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),sourceSha256=sha256(source),objectSha256=sha256(output),word32=True,pointer32=True,threadQueue8=True,messageQueue32=True,commandHeader16=True,packet44=True,overlappingQueueState36=True,configPrefix32=True,resultSocketPrefix112=True)
    wrong=[]
    for label,old,new in [('thread-queue-size','ThreadView *tail;','ThreadView *tail[2];'),('response-offset','void *socket4;','void *socket4[2];'),('packet-stride','u8 bytes[44]','u8 bytes[40]'),('allocator-offset','u8 opaque0[24]','u8 opaque0[20]'),('result-offset','u8 opaque0[108]','u8 opaque0[104]')]:
        if original.count(old)!=1:raise ValueError('Actual command layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong command layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public command/type/reference text changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,callbackContract=callbacks(rows),signedAbi=signed_abi(header,directory),publicReferences=REFERENCES,limits=['Public SDK implementation/layout correspondence does not prove exact native library version or full original declarations. Production includes are the closed private context only; all reference/prefix/storage/provider bytes receive0credit.'])


def signed_abi(header,directory):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'abi.c';output=directory/'abi.o';source.write_text('#include "context.h"\ns32 abi_flag(CommandHeader *command){return command->blockD;}\ns32 abi_full(MessageQueue *queue){return queue->used1C>=queue->count14;}\n')
    values=[-0x80000000,-1,0,1,2,0x7fffffff]
    def probe(text):
        (directory/'context.h').write_text(text);process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual signed command ABI compile failed',process.stdout,process.stderr))
        results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name in ['abi_flag','abi_full']:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual signed command Thumb mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                cases=[(value,) for value in range(256)] if name=='abi_flag' else itertools.product(values,repeat=2)
                for args in cases:
                    vm.mem_write(0x02301000,bytes(32))
                    if name=='abi_flag':vm.mem_write(0x0230100d,bytes([args[0]]));expected=(args[0] if args[0]<128 else args[0]-256)&0xffffffff
                    else:
                        vm.mem_write(0x02301014,int(args[0]&0xffffffff).to_bytes(4,'little'));vm.mem_write(0x0230101c,int(args[1]&0xffffffff).to_bytes(4,'little'));expected=int(args[1]>=args[0])
                    vm.reg_write(R.UC_ARM_REG_R0,0x02301000);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100);actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual signed command projection differs',name,args,actual,expected))
                    results.append(dict(function=name,arguments=list(args),returned=actual))
        return dict(actualFreshAbiReturns=len(results),cases=results,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrImportedBodiesExecuted=0)
    original=header.read_text();positive=probe(original);wrong=[]
    for label,old,new in [('unsigned-flag','s8 blockD;','u8 blockD;'),('unsigned-used-count','s32 used1C;','u32 used1C;')]:
        if original.count(old)!=1:raise ValueError('Actual signed command ABI mutation ambiguous')
        try:probe(original.replace(old,new))
        except ValueError as error:wrong.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong signed command ABI admitted')
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,positive=positive,negative=wrong)
