import os
import shutil
import subprocess
from project import ROOT,sha256
from wave20261106_aes_table_data_paths import SOURCE,WORK,assert_owned,assert_work
from wave20261106_gp_character_data_build import inspect_object,COMPILER,COMPILER_HASH,LINKER,LINKER_HASH,FLAGS,ELFFile


def compile_link(row,source,payload,directory):
    assert_owned();assert_work(directory)
    if not any(source.resolve().is_relative_to(root.resolve())for root in [SOURCE,WORK]):raise ValueError('AES actual compiler input escaped owned paths')
    if sha256(COMPILER)!=COMPILER_HASH or sha256(LINKER)!=LINKER_HASH:raise ValueError('AES pinned genuine compiler/linker changed')
    directory.mkdir(parents=True,exist_ok=True);obj=directory/'data.o';env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));command=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];run=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if run.returncode:raise ValueError(('AES actual ordinary C compile failed',run.stdout,run.stderr))
    section,index,debug=inspect_object(obj,row['nativeSymbol'],payload)
    with obj.open('rb')as stream:
        elf=ELFFile(stream)
        if elf.get_section(index)['sh_addralign']!=4:raise ValueError('AES actual uint32 table alignment differs')
    before=sha256(obj);linkdir=directory/'link';linkdir.mkdir(parents=True,exist_ok=True);local=linkdir/'input.o';shutil.copyfile(obj,local);lcf=linkdir/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = '+row['address']+' > data.bin }\nSECTIONS {\n'+section+': { input.o('+section+') } > DATA\n}\n',encoding='utf-8');linked=linkdir/'linked.elf';link_command=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',row['nativeSymbol'],str(lcf),str(local),'-o',str(linked)];run=subprocess.run(link_command,cwd=linkdir,env=env,capture_output=True,text=True,timeout=60)
    if run.returncode:raise ValueError(('AES genuine whole-object placement failed',run.stdout,run.stderr))
    output=linkdir/'data.bin'
    if output.read_bytes()!=payload or sha256(obj)!=before or sha256(local)!=before:raise ValueError('AES original compiler object or complete linked payload changed')
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbols=[s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==row['nativeSymbol']]
        if len(symbols)!=1 or(symbols[0]['st_info']['type'],symbols[0]['st_size'],symbols[0]['st_value'])!=('STT_OBJECT',len(payload),int(row['address'],0)):raise ValueError('AES whole typed object native placement differs')
        memory=elf.get_section(symbols[0]['st_shndx']);segments=list(elf.iter_segments())
        if(memory.name,memory['sh_type'],memory['sh_flags'],memory['sh_addr'],memory['sh_size'])!=('DATA','SHT_PROGBITS',0x10000000,int(row['address'],0),0)or len(segments)!=1 or(segments[0]['p_type'],segments[0]['p_flags'],segments[0]['p_vaddr'],segments[0]['p_filesz'],segments[0]['p_memsz'])!=('PT_LOAD',0x80000000,int(row['address'],0),0,len(payload)):raise ValueError('AES genuine external-image ELF memory extent differs')
        if any(s['sh_size']and(s['sh_flags']&6 or s['sh_type']=='SHT_NOBITS')for s in elf.iter_sections()):raise ValueError('AES genuine placement emitted executable/BSS/extraallocated storage')
    proof=dict(exactDataBytes=True,exactDataAddress=True,objectUnmodified=True,actualSymbolType='STT_OBJECT',linkerSha256=LINKER_HASH,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedData=output.relative_to(ROOT).as_posix(),linkedDataSha256=sha256(output),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),command=link_command)
    return dict(object=obj.relative_to(ROOT).as_posix(),objectSha256=before,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_HASH,compilerFlags=FLAGS,compilerCommand=command,section=section,sectionIndex=index,sectionOffset=0,nonAllocatedDebugRelocations=debug,realLink=proof,outputSha256=sha256(output))
