import os
import shutil
import subprocess
from project import ROOT,sha256
from goal_resume_material_pivot import SOURCE,LANE,WORK,guarded_render
from goal_resume_ctype_ascii_data import COMPILER,COMPILER_SHA,LINKER,LINKER_SHA,FLAGS
from elftools.elf.elffile import ELFFile


def build(source,folder,expected=None):
    if sha256(COMPILER)!=COMPILER_SHA or sha256(LINKER)!=LINKER_SHA:raise ValueError('Frozen data compiler/linker differs')
    folder.mkdir(parents=True,exist_ok=True);obj=folder/'data.o';env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));command=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)]
    process=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if process.returncode:raise ValueError(('Material/pivot semantic data compile failed',process.stdout,process.stderr))
    name='native_data_main_020d9068';debug=0
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());symbol=next(s for s in symbols if s.name==name);section=elf.get_section(symbol['st_shndx']);payload=section.data()
        if elf['e_machine']!='EM_ARM'or elf.elfclass!=32 or not elf.little_endian:raise ValueError('Material data architecture differs')
        if symbol['st_info']['type']!='STT_OBJECT'or symbol['st_size']!=68 or symbol['st_value']!=0 or section['sh_size']!=68 or section['sh_type']!='SHT_PROGBITS'or section['sh_flags']!=2:raise ValueError('Material data object is not exact read-only68B initialized storage')
        if sum(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&2)!=68 or any(s['st_info']['type']=='STT_FUNC'and s['st_size']for s in symbols):raise ValueError('Material data includes code, BSS or padding')
        for rel in elf.iter_sections():
            if rel['sh_type']not in('SHT_REL','SHT_RELA'):continue
            if elf.get_section(rel['sh_info'])['sh_flags']&2 and rel.num_relocations():raise ValueError('Material data has allocated relocations')
            debug+=rel.num_relocations()
        alignment=section['sh_addralign'];section_name=section.name
    if expected is not None and payload!=expected:raise ValueError('Compiled material data differs from independent equations')
    before=sha256(obj);local=folder/'input.o';shutil.copyfile(obj,local);lcf=folder/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = 0x020d9068 > data.bin }\nSECTIONS { '+section_name+': { input.o('+section_name+') } > DATA }\n');elf_path=folder/'linked.elf'
    link=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',name,str(lcf),str(local),'-o',str(elf_path)];process=subprocess.run(link,cwd=folder,env=env,capture_output=True,text=True,timeout=60)
    if process.returncode:raise ValueError(('Genuine material data placement failed',process.stdout,process.stderr))
    actual=(folder/'data.bin').read_bytes()
    if actual!=payload or sha256(obj)!=before or sha256(local)!=before:raise ValueError('Genuine data link changed source object or bytes')
    with elf_path.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==name)
        if symbol['st_value']!=0x020d9068 or symbol['st_size']!=68 or symbol['st_info']['type']!='STT_OBJECT':raise ValueError('Genuine material data symbol address/extent changed')
    return payload,dict(name=name,symbol=name,nativeAlias='data_020d9068',program='',processor='arm9',module='main',kind='data',mode='data',address='0x020d9068',bytes=68,size=68,initializedBytes=68,compiledBytes=68,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=[],sourceLanguage='C',sourceSymbolType='STT_OBJECT',section=section_name,targetSection='.rodata',sourceSectionAlignment=alignment,sectionOffset=0,sectionPaddingBytes=0,object=obj.relative_to(ROOT).as_posix(),objectSha256=before,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_SHA,compilerFlags=FLAGS,compileCommand=command,linkerSha256=LINKER_SHA,linkCommand=link,linkedElf=elf_path.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(elf_path),linkedDataBinary=(folder/'data.bin').relative_to(ROOT).as_posix(),linkedDataBinarySha256=sha256(folder/'data.bin'),relocations=[],ordinaryFunctionCredit=0,executableSectionBytes=0,allocatedZeroFillBytes=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,nonAllocatedDebugRelocations=debug,realLink=dict(exactDataBytes=True,exactDataAddress=True,objectUnmodified=True))
