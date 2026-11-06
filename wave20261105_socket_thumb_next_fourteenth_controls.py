import copy
from project import ROOT,sha256
import match_runtime as C
from elftools.elf.elffile import ELFFile
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_controls import projection_abi
from wave20261105_socket_thumb_next_fourteenth_bindings import negative_controls
REFERENCES=[{'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/manifest.json', 'sha256': 'ee84f2b3cd60b635fb08c123a9f54029375df0a2fcfe26ebc70562e0ed75dae4'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-read/libraries/soc/src/socl_read.c', 'sha256': 'cf7fb830b1232df2af32116e3b0a48df70185f31ad4e67ec07f2049f770fd929'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/reference-manifest.json', 'sha256': '9c31c2836e27e32a314603bc203eef37056bcbf665bb41ba654e3e1ae0f7a2f6'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/libraries/soc/src/socl_command.c', 'sha256': '2b023bcaeb5db6f66fdc81cefe768cbf2470d9b109edaa48c936f54f061f77a0'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-command/include/nitroWiFi/socl.h', 'sha256': '166b04e5fa97ead37797f6bf458b50805827450a6cae9300c1b00e69ccd08bb3'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/reference-manifest.json', 'sha256': 'a4fdd77f6d3273a05df3e699bb799314d37927c79df74e63d4a04f3354d2495a'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-types/include/nitro/types.h', 'sha256': 'a2d0f5265bdf17b543d88ae71c4d5aa9dbddd6e07a8c0ca0dbbca432aca2a2b7'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/reference-manifest.json', 'sha256': '6f06b4fd80ce55d40bb2472aeaf0c43110139d87d7f70bc602755469076d97c5'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-thumb-next/include/nitroWiFi/cps.h', 'sha256': 'a50f467431d9e3334b6c5d63428b3cf979f9373d84fb0b491de6bfbe75b1895d'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/reference-manifest.json', 'sha256': '24253dc196d195ee4f546c2f68a9d29918beaa838116e93e2f73ec7c5e430463'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/message.h', 'sha256': 'a478ca5e02f830554b8df9266d264b758c3eca4f8aee9e6ced15728e718c674c'}, {'path': 'deps/reference/nitrosdk-eaae40f199c0-socket-message/include/nitro/os/common/thread.h', 'sha256': '50c9abbb9f95c8eccb2ccddc2f01c46f682c241f4702d492fed35ad37fb24742'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/reference-manifest.json', 'sha256': '25503394ede91e8a3b316084373a56a9142383eb492cf7a726882ccf92d10a9b'}, {'path': 'deps/reference/nitrowifi-e6048fc29448-socket-socl-write/libraries/soc/src/socl_write.c', 'sha256': '37ec73c7b81978cc58a9d2db4491cb0540de5b5e3f9389526eb7b8e051655cb7'}]

def literal_link(row):
    address=int(row['address'],0);size=row['bytes'];offset,callback={0x0208f91c:(276,0x0208fa34)}[address];name='native_fn_'+format(callback,'08x')
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
    return dict(status='passed',sourceCredit=0,originalPointerWord=hex(word),canonicalEntry=hex(callback),linkedFunctionValueEven=True,actualLinkedELFType='STT_FUNC',actualLinkedThumbMapping='$t',actualRelocatableELFType='STT_FUNC',actualRelocatableThumbMapping='$t',calleeInitializedCodeBytes=0,calleeSourceCredit=0,linkedElfSha256=sha256(linked),probe=probe,minimumInterface='int32(voidPointer)',originalTargetIsSelectedSeparateCaller=True,limits=['Actual original encoded target identity and Thumb tag are proved. This binding supplies0callee source credit; this248B callback is credited only by its separate selected top-level full-function proof, never as an imported constructor callee.'])


def execute(rows):
    directory=ROOT/'work/w5st/fourteenth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/fourteenth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual private constructor layouts failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),word32=True,pointer32=True,socket128=True,recvPrefix276=True,writeCommand44=True,send272=True)
    wrong=[]
    for label,old,new in [('write-command-padding','u8 padE[2]','u8 padE[4]'),('write-command-word','s32 firstLength14;','s16 firstLength14;'),('write-ring-position-width','u16 after20;','u32 after20;'),('send-index-width','volatile u16 out102;','volatile u32 out102;')]:
        if original.count(old)!=1:raise ValueError('Actual constructor layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong private constructor layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    proofs=[];bad=[]
    for row in rows:
        if int(row['address'],0)!=0x0208f91c:continue
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
