import copy
from project import ROOT,sha256
import match_runtime as C
from wave20261105_socket_thumb_next_fourth_callbacks import compile_source
from wave20261105_socket_thumb_next_eighth_controls import projection_abi,REFERENCES
from wave20261105_socket_thumb_next_ninth_bindings import negative_controls
from elftools.elf.elffile import ELFFile


def literal_link(row):
    if int(row['address'],0)!=0x0208f0a0 or (row['processor'],row['module'],row['mode'],row.get('program') or '')!=('arm9','main','thumb',''):raise ValueError('Actual encoded callable caller namespace differs')
    candidates=[r for r in row['relocations'] if r['symbol']=='native_fn_0208f0e8']
    if len(candidates)!=1:raise ValueError('Original encoded callable symbol absent/ambiguous')
    relocation=candidates[0]
    if (relocation['offset'],relocation['type'],relocation['addend'],relocation['target'])!=(68,2,0,'0x208f0e9'):raise ValueError('Actual original odd callable relocation contract differs')
    binding=row['nativeSymbolEntries']['native_fn_0208f0e8']
    if (binding['processor'],binding['module'],binding['mode'],binding['kind'],binding['address'],binding.get('program') or '')!=('arm9','main','thumb','function','0x208f0e8',''):raise ValueError('Exact encoded callable canonical identity differs')
    linked=ROOT/row['realLink']['linkedElf']
    if sha256(linked)!=row['realLink']['linkedElfSha256']:raise ValueError('Actual encoded callable linked ELF changed')
    with linked.open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());target=next(s for s in symbols if s.name=='native_fn_0208f0e8');caller=next(s for s in symbols if s.name==row['name'])
        if target['st_info']['type']!='STT_FUNC' or target['st_value']!=0x0208f0e8 or target['st_size']!=0 or not any(s.name=='$t' and s['st_value']==target['st_value'] and s['st_shndx']==target['st_shndx'] for s in symbols):raise ValueError('Actual linked callable type/even-entry/Thumb mapping differs')
        targetSection=elf.get_section(target['st_shndx'])
        if targetSection['sh_size']!=0 or targetSection.data():raise ValueError('Mode-only callable unexpectedly initializes executable bytes')
        if caller['st_value']!=0x0208f0a0 or caller['st_size']!=72:raise ValueError('Actual linked caller symbol boundary differs')
        bodyPath=linked.parent/'caller.bin';body=bodyPath.read_bytes()
        if len(body)!=72 or sha256(bodyPath)!=row['outputSha256'] or sha256(bodyPath)!=row['realLink']['linkedCallerSha256']:raise ValueError('Actual linked caller binary identity differs')
        word=int.from_bytes(body[68:72],'little')
        if word!=0x0208f0e9 or C.sha(body)!=row['targetSha256']:raise ValueError('Full actual linked caller/original odd pointer differs')
    probe=next(p for p in row['realLink']['bindingOnlyProbes'] if p['name']=='native_fn_0208f0e8')
    if sha256(ROOT/probe['object'])!=probe['objectSha256'] or any(probe[key]!=0 for key in ['initializedCodeBytes','nativeCalleeBytesUsed','calleeSourceCredit','functionSymbolSize','linkedInitializedOutputBytes']):raise ValueError('Actual encoded callable mode-only probe changed')
    with (ROOT/probe['object']).open('rb') as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name=='native_fn_0208f0e8')
        if symbol['st_info']['type']!='STT_FUNC' or symbol['st_size']!=0 or elf.get_section(symbol['st_shndx'])['sh_type']!='SHT_NOBITS' or not any(s.name=='$t' and s['st_value']==symbol['st_value'] and s['st_shndx']==symbol['st_shndx'] for s in symbols):raise ValueError('Actual relocatable callable function/Thumb mapping differs')
    return dict(status='passed',sourceCredit=0,originalPointerWord=hex(word),canonicalEntry='0x208f0e8',linkedFunctionValueEven=True,actualLinkedELFType='STT_FUNC',actualLinkedThumbMapping='$t',actualRelocatableELFType='STT_FUNC',actualRelocatableThumbMapping='$t',calleeInitializedCodeBytes=0,calleeSourceCredit=0,linkedElfSha256=sha256(linked),probe=probe,minimumInterface='int32(voidPointer)',originalTargetIsSelectedSeparateCaller=True,limits=['Actual original encoded target identity and Thumb tag are proved. This binding supplies0callee source credit; the98B callback is credited only by its own independent selected whole-function proof.'])


def execute(rows):
    directory=ROOT/'work/w5st/ninth-controls';directory.mkdir(parents=True,exist_ok=True)
    header=ROOT/'src/runtime/parallel_wave20261105/socket-thumb-next/ninth/context.h';original=header.read_text();source=directory/'layout.c';source.write_text('#include "context.h"\n');output=directory/'layout.o'
    (directory/'context.h').write_text(original);process=compile_source(source,output,'thumb')
    if process.returncode:raise ValueError(('Actual bind/mutex/socket layouts failed',process.stdout,process.stderr))
    positive=dict(headerSha256=sha256(header),objectSha256=sha256(output),bind24=True,socket128=True,recvPrefix264=True,mutexOffset224=True,consumed248=True,pointer32=True,word32=True)
    wrong=[]
    for label,old,new in [('bind-local-offset','u8 paddingE[2]','u8 paddingE[4]'),('bind-port-width','u16 local10;','u32 local10;'),('mutex-offset','u8 opaque0[224]','u8 opaque0[220]')]:
        if original.count(old)!=1:raise ValueError('Actual bind layout mutation ambiguous')
        (directory/'context.h').write_text(original.replace(old,new));process=compile_source(source,output,'thumb')
        if process.returncode==0 or 'illegal constant expression' not in process.stdout:raise ValueError(('Wrong bind layout admitted',label,process.stdout,process.stderr))
        wrong.append(dict(case=label,rejected=True,exitCode=process.returncode,stdout=process.stdout,stderr=process.stderr))
    (directory/'context.h').write_text(original)
    for pin in REFERENCES:
        if sha256(ROOT/pin['path'])!=pin['sha256']:raise ValueError('Immutable public bind/type comparison changed')
    caller=next(r for r in rows if int(r['address'],0)==0x0208f0a0);literal=literal_link(caller);bad=[]
    for case in ['even-pointer','wrong-symbol','wrong-binding-mode','wrong-binding-module','wrong-ELF-hash']:
        row=copy.deepcopy(caller);rel=next(r for r in row['relocations'] if r['symbol']=='native_fn_0208f0e8')
        if case=='even-pointer':rel['target']='0x208f0e8'
        elif case=='wrong-symbol':rel['symbol']='native_fn_0208f0f0'
        elif case=='wrong-binding-mode':row['nativeSymbolEntries']['native_fn_0208f0e8']['mode']='arm'
        elif case=='wrong-binding-module':row['nativeSymbolEntries']['native_fn_0208f0e8']['module']='ov000'
        else:row['realLink']['linkedElfSha256']='0'*64
        try:literal_link(row)
        except ValueError as error:bad.append(dict(case=case,rejected=True,reason=str(error)))
        else:raise ValueError('Wrong original encoded callable proof admitted')
    return dict(status='passed',sourceCredit=0,bindingControls=negative_controls(rows),nativeCompilerLayout=positive,wrongLayouts=wrong,projectionAbi=projection_abi(header,directory),originalEncodedCallable=literal,wrongEncodedCallableProofs=bad,publicReferences=REFERENCES)
