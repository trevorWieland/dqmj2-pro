import copy
from project import ROOT,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighteenth_bindings import negative_controls
from wave20261105_socket_thumb_next_eighteenth_callbacks import execute as callback_controls
from wave20261105_socket_thumb_next_eighth_controls import projection_abi
REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_cleanup.c', 'sha256': 'a44ba6e6407efb877eec5cce069cf199f417b9b27de5d4438733be86389e60f2'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_close.c', 'sha256': 'd5283509ab77a14a3eb96424652b6c3ce87e730690944212b2ca2c5648fa6725'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/libraries/soc/src/socl_shutdown.c', 'sha256': '4b646c03b7824210f878520b109a5945848b7f019818f4fc79718f2758660489'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-shutdown-close/reference-manifest.json', 'sha256': '30750198e39a2e303f7f6e2843345e1bf6938f146906fa0f8d128ad4c804c260'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-soc-list/include/nitroWiFi/soc.h', 'sha256': '5411d7f9d20b249e36e689730efd20a8bd5fa90ce2e2df0cee9b0aae15ce9dbe'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-soc-list/libraries/soc/src/soc.c', 'sha256': 'cca97021577811657a17add2123f3de9b9c258578f40fb93357dfe9ea5d06003'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-soc-list/libraries/soc/src/socl_list.c', 'sha256': '2cf98835d9a303c0d2f7b873fcdca6ee2890d08c5c6fbccfd9046902e5b3cfe5'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-soc-list/reference-manifest.json', 'sha256': 'c580501b37e91ffa5ca6d8888fb58bf73e91b7fc546580b069d0ae910ee0645b'}]

def literal_link(row,offset,callback,interface):
    address=int(row['address'],0);size=row['bytes'];name='native_fn_'+format(callback,'08x')
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
    return dict(status='passed',sourceCredit=0,originalPointerWord=hex(word),canonicalEntry=hex(callback),linkedFunctionValueEven=True,actualLinkedELFType='STT_FUNC',actualLinkedThumbMapping='$t',actualRelocatableELFType='STT_FUNC',actualRelocatableThumbMapping='$t',calleeInitializedCodeBytes=0,calleeSourceCredit=0,linkedElfSha256=sha256(linked),probe=probe,minimumInterface=interface,originalTargetIsSelectedSeparateCaller=callback in [0x02090608,0x02090624],limits=['Only exact original callable word/mode/entry and minimum caller-facing interface;0 imported bodies/storage/callee credit.'])


def execute(rows):
    sourceRoot=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth';evidenceRoot=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth'
    if sourceRoot!=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth' or evidenceRoot!=ROOT/'evidence/lanes/parallel-wave20261105/socket-thumb-next/eighteenth':raise ValueError('New eighteenth source/evidence materializer scope changed')
    directory=ROOT/'work/w5st/eighteenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/eighteenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o';(directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual lifecycle/address/startup private geometry failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,address8=True,configInput52=True,startup56=True,wrapperPrefix120=True,observedBSSAliasOffset64=True)
    wrong=[]
    for label,old,new in [('address-port-width','u16 port2;','u32 port2;'),('CPS-LAN-offset','u8 opaque0[28];void *lan1C','u8 opaque0[24];void *lan1C'),('wrapper-prefix-offset','u8 opaque10[48]','u8 opaque10[44]'),('SOC-MTU-offset','u8 opaque24[8];s32 mtu2C','u8 opaque24[4];s32 mtu2C'),('state-width','volatile s16 state70;','volatile s32 state70;')]:
        if original.count(old)!=1:raise ValueError('Actual lifecycle/address/startup layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong lifecycle/address/startup geometry admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    proofs=[];bad=[]
    for row in rows:
        for offset,callback,interface in {0x020902f0:[(28,0x0208ef98,'int(int,u16)')],0x0209063c:[(236,0x02090608,'void*(u32)'),(240,0x02090624,'void(void*)')]}.get(int(row['address'],0),[]):
            proof=literal_link(row,offset,callback,interface);proofs.append(proof);name='native_fn_'+format(callback,'08x')
            for label in ['even-pointer','wrong-symbol-name','ARM-binding','overlay-binding','ELF-sha']:
                changed=copy.deepcopy(row);rel=next(r for r in changed['relocations'] if r['symbol']==name)
                if label=='even-pointer':rel['target']=hex(callback)
                elif label=='wrong-symbol-name':rel['symbol']='native_fn_'+format(callback+2,'08x')
                elif label=='ARM-binding':changed['nativeSymbolEntries'][name]['mode']='arm'
                elif label=='overlay-binding':changed['nativeSymbolEntries'][name]['module']='ov000'
                else:changed['realLink']['linkedElfSha256']='0'*64
                try:literal_link(changed,offset,callback,interface)
                except (ValueError,KeyError) as error:bad.append(dict(caller=row['address'],callback=hex(callback),case=label,rejected=True,reason=str(error)))
                else:raise ValueError('Bad actual encoded SOC callable proof admitted')
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public SOC/list/lifecycle reference changed')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),encodedCallableProofs=proofs,wrongEncodedCallableProofs=bad,indirectInterfaces=callback_controls(rows),wrongRuntimeTags=runtime_tags(rows),publicReferences=REFERENCES)


def runtime_tags(rows):
    from wave20261105_socket_thumb_next_eighteenth_models import fixtures,scenario
    from wave20261105_socket_thumb_next_eighteenth_execution import run
    import link_runtime_unit as L
    unused,main,unused=L.measured_module('main');bad=[]
    for name in ['0208ff04','02090608','02090624']:
        row=next(r for r in rows if int(r['address'],0)==int(name,16));path=(ROOT/row['realLink']['linkedElf']).parent/'caller.bin';body=path.read_bytes()
        if sha256(path)!=row['outputSha256']:raise ValueError('Actual lifecycle/raw callback runtime-tag body changed')
        for mode in ['arm','thumb']:
            fixture=next(f for i,f in enumerate(fixtures(name)) if ((releases:=[a for a in scenario(name,f,i)['actions'] if a['kind']]) and releases[0]['mode']==mode and (name!='0208ff04' or (not f['mutate'] and f['requested'] and f['waits']==0))))
            result=run(row,body,dict(fixture,_wrongTag=True),main)
            if not result['modelFailures'] or result['actualTopReturn'] or not result['rejectedAtObservedProtocolBoundary'] or result['calls'][-1]['mode']==mode:raise ValueError('Wrong named allocator/free runtime tag not rejected')
            bad.append(dict(caller=row['address'],declaredFreshProviderMode=mode,actualMode=result['calls'][-1]['mode'],rejected=True,actualCallerReturn=False,originalCalleeBodiesExecuted=0,fixture=fixture,result=result))
    return bad
