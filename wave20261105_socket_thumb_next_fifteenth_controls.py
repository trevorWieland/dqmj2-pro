import copy
from project import ROOT,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_fifteenth_bindings import negative_controls
REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/reference-manifest.json', 'sha256': '30750198e39a2e303f7f6e2843345e1bf6938f146906fa0f8d128ad4c804c260'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_shutdown.c', 'sha256': '4b646c03b7824210f878520b109a5945848b7f019818f4fc79718f2758660489'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_close.c', 'sha256': 'd5283509ab77a14a3eb96424652b6c3ce87e730690944212b2ca2c5648fa6725'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_cleanup.c', 'sha256': 'a44ba6e6407efb877eec5cce069cf199f417b9b27de5d4438733be86389e60f2'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}]

def literal_link(row):
    address=int(row['address'],0);size=row['bytes'];offset,callback={0x0208fbe8:(132,0x0208fc70),0x0208fcb0:(152,0x0208fd4c)}[address];name='native_fn_'+format(callback,'08x')
    if (row['processor'],row['module'],row['mode'],row.get('program') or '')!=('arm9','main','thumb',''):raise ValueError('Actual encoded callable caller namespace differs')
    candidates=[r for r in row['relocations'] if r['symbol']==name]
    if len(candidates)!=1:raise ValueError('Original encoded callable symbol absent/ambiguous')
    relocation=candidates[0]
    if (relocation['offset'],relocation['type'],relocation['addend'],relocation['target'])!=(offset,2,0,hex(callback|1)):raise ValueError('Actual original odd callable relocation contract differs')
    binding=row['nativeSymbolEntries'][name]
    if (binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'],binding.get('program') or '')!=('arm9','main','thumb','function',hex(callback),''):raise ValueError('Exact encoded callable canonical identity differs')
    linked=ROOT/row['realLink']['linkedElf']
    if sha256(linked)!=row['realLink']['linkedElfSha256']:raise ValueError('Actual encoded callable linked ELF changed')
    with linked.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());target=next(s for s in symbols if s.name==name);caller=next(s for s in symbols if s.name==row['name'])
        if target['st_info']['type']!='STT_FUNC' or target['st_value']!=callback or target['st_size']!=0 or not any(s.name=='$t' and s['st_value']==target['st_value'] and s['st_shndx']==target['st_shndx'] for s in symbols):raise ValueError('Actual linked callable type/even-entry/Thumb mapping differs')
        targetSection=elf.get_section(target['st_shndx'])
        if targetSection['sh_size']!=0 or targetSection.data():raise ValueError('Mode-only callable unexpectedly initializes executable bytes')
        if caller['st_value']!=address or caller['st_size']!=size:raise ValueError('Actual linked caller symbol boundary differs')
        bodyPath=linked.parent/'caller.bin';body=bodyPath.read_bytes()
        if len(body)!=size or sha256(bodyPath)!=row['outputSha256'] or sha256(bodyPath)!=row['realLink']['linkedCallerSha256']:raise ValueError('Actual linked caller binary identity differs')
        word=int.from_bytes(body[offset:offset+4],'little')
        if word!=(callback|1) or C.sha(body)!=row['targetSha256']:raise ValueError('Full actual linked caller/original odd pointer differs')
    probe=next(p for p in row['realLink']['bindingOnlyProbes'] if p['name']==name)
    if sha256(ROOT/probe['object'])!=probe['objectSha256'] or any(probe[key]!=0 for key in ['initializedCodeBytes','nativeCalleeBytesUsed','calleeSourceCredit','functionSymbolSize','linkedInitializedOutputBytes']):raise ValueError('Actual encoded callable mode-only probe changed')
    with (ROOT/probe['object']).open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name==name)
        if symbol['st_info']['type']!='STT_FUNC' or symbol['st_size']!=0 or elf.get_section(symbol['st_shndx'])['sh_type']!='SHT_NOBITS' or not any(s.name=='$t' and s['st_value']==symbol['st_value'] and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual relocatable callable function/Thumb mapping differs')
    return dict(status='passed',sourceCredit=0,originalPointerWord=hex(word),canonicalEntry=hex(callback),linkedFunctionValueEven=True,actualLinkedELFType='STT_FUNC',actualLinkedThumbMapping='$t',actualRelocatableELFType='STT_FUNC',actualRelocatableThumbMapping='$t',calleeInitializedCodeBytes=0,calleeSourceCredit=0,linkedElfSha256=sha256(linked),probe=probe,minimumInterface='int32(voidPointer)',originalTargetIsSelectedSeparateCaller=callback==0x0208fc70,limits=['Actual original encoded target identity and Thumb tag are proved. This binding supplies0callee source credit; the32B shutdown callback is separately selected;124B close callback is not reconstructed here. Imported target credit always0.'])


def execute(rows):
    directory=ROOT/'work/w5st/fifteenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fifteenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual private constructor layouts failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,commandHeader16=True,send272=True)
    wrong=[]
    for label,old,new in [('CPS-prefix-size','u8 cps0[100]','u8 cps0[96]'),('executor-offset','u8 opaque0[268]','u8 opaque0[264]'),('response-word-width','void *response8;','u16 response8;'),('state-width','volatile s16 state70;','volatile s32 state70;')]:
        if original.count(old)!=1:raise ValueError('Actual constructor layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong private constructor layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    proofs=[];bad=[]
    for row in rows:
        if int(row['address'],0) not in [0x0208fbe8,0x0208fcb0]:continue
        proof=literal_link(row);proofs.append(proof)
        target=proof['canonicalEntry'];name='native_fn_'+format(int(target,0),'08x')
        for label in ['even-pointer','wrong-symbol-name','ARM-binding','overlay-binding','ELF-sha']:
            changed=copy.deepcopy(row);rel=next(r for r in changed['relocations'] if r['symbol']==name)
            if label=='even-pointer':rel['target']=target
            elif label=='wrong-symbol-name':rel['symbol']='native_fn_'+format(int(target,0)+2,'08x')
            elif label=='ARM-binding':changed['nativeSymbolEntries'][name]['mode']='arm'
            elif label=='overlay-binding':changed['nativeSymbolEntries'][name]['module']='ov000'
            else:changed['realLink']['linkedElfSha256']='0'*64
            try:literal_link(changed)
            except (ValueError,KeyError) as error:bad.append(dict(caller=row['address'],case=label,rejected=True,reason=str(error)))
            else:raise ValueError('Bad actual encoded callable proof admitted')
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public comparison input changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),encodedCallableProofs=proofs,wrongEncodedCallableProofs=bad,publicReferences=REFERENCES,limits=['Public source/private prefix types are comparison and minimum caller-access evidence only. No exact SDK version/full original declarations/storage, constructor-target execution, allocator/command/thread/game/platform behavior is inferred. All imported bodies/source credit0.'])

def projection_abi(header,directory):
    import unicorn
    from unicorn import arm_const as R
    source=directory/'abi.c';output=directory/'abi.o';source.write_text('#include "context.h"\ns32 abi_mode(SocketView *socket){return socket->mode73;}\ns32 abi_block(SocketView *socket){return socket->block72;}\ns32 abi_state(SocketView *socket){return socket->state70;}\n')
    def evaluate():
        process=compile_source(source,output,'thumb')
        if process.returncode:raise ValueError(('Actual signed borrowed-field ABI compile failed',process.stdout,process.stderr))
        rows=[]
        with output.open('rb') as stream:
            elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols())
            for name,offset,width,values in [('abi_mode',115,1,range(256)),('abi_block',114,1,range(256)),('abi_state',112,2,[0,1,32767,32768,32769,65534,65535])]:
                symbol=next(s for s in symbols if s.name==name);start=symbol['st_value'];section=symbol['st_shndx'];body=elf.get_section(section).data()[start:start+symbol['st_size']]
                if symbol['st_info']['type']!='STT_FUNC' or start&1 or not any(s.name=='$t' and s['st_shndx']==section and s['st_value']==start for s in symbols):raise ValueError('Actual signed field getter Thumb mapping differs')
                vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_THUMB);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02300000,0x2000);vm.mem_write(0x02300000,body)
                for value in values:
                    vm.reg_write(R.UC_ARM_REG_CPSR,0x30);vm.mem_write(0x02301000+offset,value.to_bytes(width,'little'));vm.reg_write(R.UC_ARM_REG_R0,0x02301000);vm.reg_write(R.UC_ARM_REG_LR,0x02300801);vm.reg_write(R.UC_ARM_REG_SP,0x02301f00);vm.reg_write(R.UC_ARM_REG_CPSR,0x30);vm.emu_start(0x02300001,0x02300800,count=100)
                    expected=(value if value<1<<(width*8-1) else value-(1<<(width*8)))&0xffffffff;actual=vm.reg_read(R.UC_ARM_REG_R0)
                    if actual!=expected or vm.reg_read(R.UC_ARM_REG_PC)!=0x02300800:raise ValueError(('Actual signed field ABI differs',name,value,actual,expected))
                    rows.append(dict(function=name,input=value,returned=actual))
        return dict(status='passed',actualFreshAbiReturns=len(rows),sourceSha256=sha256(source),objectSha256=sha256(output),cases=rows)
    original=header.read_text();(directory/'context.h').write_text(original);positive=evaluate();bad=[]
    for label,old,new in [('mode-signed','s8 mode73;','u8 mode73;'),('block-signed','s8 block72;','u8 block72;'),('state-signed','volatile s16 state70;','volatile u16 state70;')]:
        if original.count(old)!=1:raise ValueError('Actual signed field ABI mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new))
        try:evaluate()
        except ValueError as error:bad.append(dict(case=label,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong signed field getter admitted')
    (directory/'context.h').write_text(original)
    return dict(positive=positive,negative=bad,sourceCredit=0,originalNativeBodiesExecuted=0)
