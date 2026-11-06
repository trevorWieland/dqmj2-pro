from project import ROOT,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_seventeenth_bindings import negative_controls
REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/reference-manifest.json', 'sha256': '30750198e39a2e303f7f6e2843345e1bf6938f146906fa0f8d128ad4c804c260'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_shutdown.c', 'sha256': '4b646c03b7824210f878520b109a5945848b7f019818f4fc79718f2758660489'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_close.c', 'sha256': 'd5283509ab77a14a3eb96424652b6c3ce87e730690944212b2ca2c5648fa6725'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_cleanup.c', 'sha256': 'a44ba6e6407efb877eec5cce069cf199f417b9b27de5d4438733be86389e60f2'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/reference-manifest.json', 'sha256': '25503394ede91e8a3b316084373a56a9142383eb492cf7a726882ccf92d10a9b'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/libraries/soc/src/socl_write.c', 'sha256': '37ec73c7b81978cc58a9d2db4491cb0540de5b5e3f9389526eb7b8e051655cb7'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/reference-manifest.json', 'sha256': '6f06b4fd80ce55d40bb2472aeaf0c43110139d87d7f70bc602755469076d97c5'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/include/nitroWiFi/cps.h', 'sha256': 'a50f467431d9e3334b6c5d63428b3cf979f9373d84fb0b491de6bfbe75b1895d'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-math-min/reference-manifest.json', 'sha256': '16ca9cbcd7e5ce57b6f6102123ddc1aa1fec311f2a973c2299a5dabc0a06d556'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-math-min/include/nitro/math/math.h', 'sha256': 'dc9b769a2abef51ed02f6c36f48818b37133bd8644bc5d1549bec732b61df164'}]


def execute(rows):
    directory=ROOT/'work/w5st/seventeenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/seventeenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o';(directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual kernel/thread/SOC/config minimum layout failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),int32=True,pointer32=True,kernel8=True,thread168=True,soc48=True,config40=True)
    bad=[]
    for label,old,new in [('remote-window-offset','u8 opaque0[44]','u8 opaque0[40]'),('specific-offset','u8 opaque0[164]','u8 opaque0[160]'),('current-thread-offset','u32 opaque0;ThreadView','u32 opaque0[2];ThreadView'),('config-word-width','u32 mss24;','u16 mss24;')]:
        if original.count(old)!=1:raise ValueError('Actual getter geometry mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong getter geometry admitted',label,process.stdout,process.stderr))
        bad.append(dict(case=label,rejected=True,stdout=process.stdout,stderr=process.stderr,exitCode=process.returncode))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public math/header context changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=bad,fieldAbi=field_abi(header,directory),publicReferences=REFERENCES,originalImportedOrDivideBodiesExecuted=0)


def field_abi(header,directory):
    import unicorn
    from unicorn import arm_const as R
    source=directory/'abi.c';output=directory/'abi.o';text='#include "context.h"\nu32 abi_window(SocView *p){return p->window2C;}\nu32 abi_mss(SocView *p){return p->mss2E;}\nu32 abi_config(CpsConfigView *p){return p->mss24;}\nint abi_min(int a,int b){return minimum(a,b); }\n';source.write_text(text)
    values=[0,1,32767,32768,65535];signedValues=[0x80000000,0xffffffff,0,1,65535,0x7fffffff]
    def signed(v):return v if v<0x80000000 else v-0x100000000
    def evaluate():
        process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual field/minimum ABI compile failed',process.stdout,process.stderr))
        results=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name in ['abi_window','abi_mss','abi_config','abi_min']:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];section=symbol['st_shndx'];body=elf.get_section(section).data()[start:start+symbol['st_size']]
                if symbol['st_info']['type']!='STT_FUNC' or start&1 or not any(s.name=='$t' and s['st_value']==start and s['st_shndx']==section for s in symbols):raise ValueError('Actual field/minimum Thumb mapping differs')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                cases=[(a,b) for a in signedValues for b in signedValues] if name=='abi_min' else [(v,0) for v in signedValues] if name=='abi_config' else [(v,0) for v in values]
                for a,b in cases:
                    vm.reg_write(R.UC_ARM_REG_CPSR,0x30)
                    if name=='abi_min':vm.reg_write(R.UC_ARM_REG_R0,a);vm.reg_write(R.UC_ARM_REG_R1,b);expected=min(signed(a),signed(b))&0xffffffff
                    else:
                        offset=44 if name=='abi_window' else 46 if name=='abi_mss' else 36;width=4 if name=='abi_config' else 2;vm.mem_write(0x02301000+offset,a.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_R0,0x02301000);expected=a
                    vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.emu_start(0x02300001,0x02300800,count=100);actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual field/min ABI differs',name,a,b,actual,expected))
                    results.append(dict(function=name,a=a,b=b,returned=actual))
        return dict(status='passed',actualFreshAbiReturns=len(results),sourceSha256=sha256(source),objectSha256=sha256(output),cases=results)
    positive=evaluate();bad=[]
    for label,old,new in [('window-signed','return p->window2C','return (short)p->window2C'),('config-truncated','return p->mss24','return (u16)p->mss24'),('minimum-unsigned','minimum(a,b)','(u32)a<=(u32)b?a:b')]:
        if text.count(old)!=1:raise ValueError('Actual field ABI bad source ambiguous')
        source.write_text(text.replace(old,new))
        try:evaluate()
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong field/minimum ABI admitted')
    source.write_text(text)
    return dict(positive=positive,negative=bad,originalNativeBodiesExecuted=0,sourceCredit=0)
