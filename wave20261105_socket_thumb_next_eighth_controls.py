from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_bindings import negative_controls

REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-poll-bind/reference-manifest.json', 'sha256': 'c6faca3b70ece2b9e46a1944179f86d82cf5c158321017440058d4f8bc345f18'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-poll-bind/libraries/soc/src/socl_poll.c', 'sha256': '5e4fe750111b30d4e6cd3fcd7d686591f2b479a9e5a866459897ee31180ab371'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-poll-bind/libraries/soc/src/socl_bind.c', 'sha256': 'c70b0d7dda64fa14aa24a4f317ba846bf6003774cb5e58f9a205e59d78abacd0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}]


def execute(rows):
    directory=ROOT/'work/w5st/eighth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual socket/status/receive geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,recvPrefix264=True,udpPrefix6=True,stateWord16=True,resultWord32=True)
    wrong=[]
    for label,old,new in [('receive-count-offset','u8 opaque9[59]','u8 opaque9[55]'),('consumed-offset','u8 opaque0[248]','u8 opaque0[244]'),('udp-halfword-width','u16 size4;','u32 size4;'),('state-width','volatile s16 state70;','volatile s32 state70;')]:
        if original.count(old)!=1:raise ValueError('Actual socket layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong socket layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public socket/source/type comparison changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),publicReferences=REFERENCES,limits=['Native source/private types are independently compiled/genuinely linked. Public implementation/layout correspondence does not prove exact SDK version, full original declarations/storage, network/thread/game/platform behavior. Controlled read-ordinal data updates are unit fixtures, not original hardware observations.'])


def projection_abi(header,directory):
    import unicorn
    from unicorn import arm_const as R
    from elftools.elf.elffile import ELFFile
    source=directory/'abi.c';output=directory/'abi.o';source.write_text('#include "context.h"\ns32 abi_mode(SocketView *socket){return socket->mode73;}\ns32 abi_state(SocketView *socket){return socket->state70;}\nu32 abi_size(UdpView *packet){return packet->size4;}\n')
    def probe(text):
        (directory/'context.h').write_text(text);process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual signed/unsigned socket ABI compilation failed',process.stdout,process.stderr))
        results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset,width,values,signed in [('abi_mode',115,1,range(256),True),('abi_state',112,2,[0,1,127,128,255,256,32767,32768,65534,65535],True),('abi_size',4,2,[0,1,127,128,255,32767,32768,65534,65535],False)]:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];body=elf.get_section(symbol['st_shndx']).data()[start:start+symbol['st_size']]
                if not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual socket ABI Thumb mapping absent')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                for value in values:
                    vm.mem_write(0x02301000,bytes(128));vm.mem_write(0x02301000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_R0,0x02301000);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100)
                    actual=vm.reg_read(R.UC_ARM_REG_R0);expected=(value-(1<<(width*8)) if signed and value&(1<<(width*8-1)) else value)&0xffffffff
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual socket sign/width projection differs',name,value,actual,expected))
                    results.append(dict(function=name,input=value,returned=actual))
        return dict(actualFreshAbiReturns=len(results),cases=results,sourceSha256=sha256(source),objectSha256=sha256(output),originalGameOrImportedBodiesExecuted=0)
    original=header.read_text();positive=probe(original);wrong=[]
    for label,old,new in [('unsigned-mode','s8 mode73;','u8 mode73;'),('unsigned-state','volatile s16 state70;','volatile u16 state70;'),('signed-size','u16 size4;','s16 size4;')]:
        if original.count(old)!=1:raise ValueError('Actual socket signed projection mutation ambiguous')
        try:probe(original.replace(old,new))
        except ValueError as error:wrong.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong socket signed projection admitted')
    (directory/'context.h').write_text(original)
    return dict(status='passed',sourceCredit=0,positive=positive,negative=wrong)
