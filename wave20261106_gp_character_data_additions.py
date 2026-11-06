import hashlib
import os
import shutil
import subprocess
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,configuration
from qualify_child_message_data_additions_20261106 import selected_data,identity
from replay_sdk_data_registration_v2_20261106 import qualify as qualify_row
from closed_c_compiler_inputs_20261105 import compiler_inputs
from wave20261106_gp_character_data_paths import EVIDENCE,SOURCE
from wave20261106_gp_character_data_codec import encode,render
from wave20261106_gp_character_data_validate import validate_reference,validate_native
from wave20261106_gp_character_data_build import inspect_object,COMPILER,COMPILER_HASH,LINKER,LINKER_HASH,FLAGS,ELFFile

CLAIM=EVIDENCE/'data-claim.json'
CLAIM_HASH='9d9fb10cf08ed3cc5a0fd44b61a40267dbb2e2f5e07b5a02a21c8a32c7b990a6'
LAYOUT=SOURCE/'layout.json'
LAYOUT_HASH='724eb9edc05afd24d62f5d51be8c39afd8b07b8b6045a22a5da043fa5b4b3f88'
HEADER=SOURCE/'characters.h'
HEADER_HASH='2e8f74072ec4c0ce6ab9b0c257dabb83e11025c94c9fdef2ea021cf1a52517f8'


def require(value,message):
    if not value:raise ValueError(message)


def membership(before,after,expected,functions):
    require(sha256(CLAIM)==CLAIM_HASH and sha256(LAYOUT)==LAYOUT_HASH and sha256(HEADER)==HEADER_HASH,'Admitted GP claim/layout/header changed')
    admitted={identity(row):row for row in read_json(CLAIM)['claimedStorage']}
    assets={identity(row):row for row in read_json(LAYOUT)['assets']}
    wanted={identity(row):row['bytes']for row in expected};added=set(after)-set(before)
    require(len(expected)==len(wanted)==259 and sum(wanted.values())==3696,'Exact259/3696 GP addition membership differs')
    require(added==set(wanted)==set(admitted)==set(assets),'GP additions differ from exact admitted complete character objects')
    require(wanted=={key:row['bytes']for key,row in admitted.items()},'GP complete character sizes changed')
    require(all(identity(row)==key for key,row in after.items()),'Selected data identity differs from its key')
    for key,row in before.items():require(key in after and after[key]==row,'Earlier selected data row changed')
    occupied=[]
    for key,row in before.items():occupied.append((key[:3],key[4],key[4]+row.get('bytes',row.get('size'))))
    for row in functions.values():
        key=identity(dict(row,kind='data'));occupied.append((key[:3],key[4],key[4]+row['size']))
    for key in sorted(added):
        require(key[:4]==('','arm9','main','data'),'GP addition crossed admitted program/CPU/module/kind')
        end=key[4]+wanted[key]
        require(not any(scope==key[:3]and max(key[4],start)<min(end,stop)for scope,start,stop in occupied),'GP data overlaps earlier data/function or another addition')
        occupied.append((key[:3],key[4],end))
    return admitted,assets


def validate(row,asset,admitted,image):
    require(row['mode']==row['kind']=='data'and row['exactBytes']is True,'GP row is not exact typed data')
    require(all(row[key]==0 for key in ['ordinaryFunctionCredit','executableSectionBytes','allocatedZeroFillBytes','encodedAssetBytes','measuredZeroAlignmentBytes']),'GP data claims executable/BSS/gap/alignment credit')
    require(row['sourceLanguage']=='C'and row['relocations']==[],'GP source language or allocated relocations differ')
    require(row['compiler']==COMPILER.relative_to(ROOT).as_posix()and row['compilerSha256']==COMPILER_HASH and row['compilerFlags']==FLAGS,'GP ordinary-C compiler profile changed')
    require(row['source']==asset['source']and row['sourceSha256']==asset['sourceSha256']==sha256(ROOT/row['source']),'GP original C source/hash changed')
    require(row['semanticSource']==asset['semanticSource']==admitted['semanticSource'],'GP semantic source identity changed')
    require(sha256(ROOT/row['semanticSource'])==asset['semanticSourceSha256']==admitted['semanticSourceSha256'],'GP complete character semantics changed')
    require(row['sourceDependencies']==[dict(path=HEADER.relative_to(ROOT).as_posix(),sha256=HEADER_HASH)],'GP actual typed C header dependency differs')
    generation={p['path']:p['sha256']for p in row['dataSourceDependencies']}
    require(len(row['dataSourceDependencies'])==2 and generation=={LAYOUT.relative_to(ROOT).as_posix():LAYOUT_HASH,asset['semanticSource']:asset['semanticSourceSha256']},'GP semantic/layout generation dependencies differ')
    for path,digest in generation.items():require(sha256(ROOT/path)==digest,'GP generation dependency changed')
    document=read_json(ROOT/row['semanticSource']);payload,_=encode(document);code,_=render(document,row['nativeSymbol'])
    require((ROOT/row['source']).read_text(encoding='utf-8')==code,'GP readable character C initializer changed')
    require(row['bytes']==row['size']==row['initializedBytes']==row['compiledBytes']==len(payload)==admitted['bytes'],'GP complete character extent changed')
    require(row['targetSha256']==row['outputSha256']==asset['targetSha256']==admitted['targetSha256']==hashlib.sha256(payload).hexdigest(),'GP complete character payload digest differs')
    address=int(row['address'],0)
    require(row['nativeAlias']==f'data_{address:08x}'and row['nativeSymbol']==asset['nativeSymbol']and row['section']=='.rodata'and row['targetSection']=='.data','GP genuine configured alias/placement differs')
    require(f"{row['nativeAlias']} kind:data(any) addr:0x{address:08x}"in(ROOT/'config/arm9/symbols.txt').read_text().splitlines(),'GP alias is not an existing configured native data entry')
    validate_reference(document);validate_native(row,payload,image);compiler_inputs(row);qualify_row(row)
    require(sha256(ROOT/row['realLink']['lcf'])==row['realLink']['lcfSha256'],'GP sealed genuine-link placement input changed')
    inspect_object(ROOT/row['object'],row['nativeSymbol'],payload)
    return payload


def link(row,payload,directory):
    directory=Path(directory).resolve()
    require(directory.is_relative_to((ROOT/'work').resolve()),'Private GP placement proof escaped repository work directory')
    directory.mkdir(parents=True,exist_ok=True);original=ROOT/row['object'];before=sha256(original);obj=directory/'input.o';shutil.copyfile(original,obj)
    section=row['section'];lcf=directory/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = '+row['address']+' > data.bin }\nSECTIONS {\n'+section+': { input.o('+section+') } > DATA\n}\n',encoding='utf-8');linked=directory/'linked.elf';command=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',row['nativeSymbol'],str(lcf),str(obj),'-o',str(linked)]
    run=subprocess.run(command,cwd=directory,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')),capture_output=True,text=True,timeout=60)
    require(run.returncode==0,'GP fresh genuine placement failed: '+run.stdout+run.stderr)
    require((directory/'data.bin').read_bytes()==payload and sha256(original)==before==sha256(obj),'GP original object or fresh complete linked payload changed')
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==row['nativeSymbol']);memory=elf.get_section(symbol['st_shndx']);segments=list(elf.iter_segments())
        require((symbol['st_info']['type'],symbol['st_size'],symbol['st_value'])==('STT_OBJECT',len(payload),int(row['address'],0)),'GP fresh complete native typed-object placement differs')
        require((memory.name,memory['sh_type'],memory['sh_flags'],memory['sh_addr'],memory['sh_size'])==('DATA','SHT_PROGBITS',0x10000000,int(row['address'],0),0),'GP MW external-image DATA memory section differs')
        require(len(segments)==1 and (segments[0]['p_type'],segments[0]['p_flags'],segments[0]['p_vaddr'],segments[0]['p_filesz'],segments[0]['p_memsz'])==('PT_LOAD',0x80000000,int(row['address'],0),0,len(payload)),'GP MW external-image full memory extent differs')
        require(not any(s['sh_size']and(s['sh_flags']&6 or s['sh_type']=='SHT_NOBITS')for s in elf.iter_sections()),'GP external-image ELF emitted extra executable/BSS/allocated sections')
    return dict(exactDataBytes=True,exactDataAddress=True,originalObjectUnmodified=True,actualSymbolType='STT_OBJECT',initializedBytes=len(payload),linkerSha256=LINKER_HASH,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedDataSha256=sha256(directory/'data.bin'),lcfSha256=sha256(lcf),mwExternalImageDataMemorySection=True,completeRawImageChecked=True,zeroBssAndCodeEstablishedFromCompleteOriginalObject=True,command=command)


def qualify(before,after,expected,functions,directory):
    require(sha256(COMPILER)==COMPILER_HASH and sha256(LINKER)==LINKER_HASH,'Pinned GP C compiler/linker changed')
    admitted,assets=membership(before,after,expected,functions)
    first=next(iter(assets.values()));image=(ROOT/first['binary']).read_bytes()
    require(hashlib.sha256(image).hexdigest()==first['inputModuleSha256'],'Full original GP native image changed')
    proofs=[]
    for key in sorted(admitted):
        row=after[key];payload=validate(row,assets[key],admitted[key],image);actual=link(row,payload,Path(directory)/f'main-{key[4]:08x}')
        proofs.append(dict(program='',processor='arm9',module='main',address=hex(key[4]),initializedBytes=len(payload),realLink=actual))
    result=dict(passed=True,newInitializedDataObjects=259,newInitializedDataBytes=3696,newTypedConstantDataBytes=3696,newEncodedAssetBytes=0,newDataAlignmentBytes=0,newSourceFunctions=0,newExecutableBytes=0,newBssBytes=0,newGapBytes=0,earlierDataPreserved=len(before),proofs=proofs,sourceCreditPendingSharedAcceptance=True)
    write_json(Path(directory)/'qualification.json',result)
    return result
