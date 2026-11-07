import os
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,sha256
from goal_resume_ctype_ascii_data import SOURCE,LANE,WORK,COMPILER,COMPILER_SHA,LINKER,LINKER_SHA,FLAGS
sys.path.insert(0,str(ROOT/'deps/native'))
from elftools.elf.elffile import ELFFile


def inspect(path,row,expected=None):
    with path.open('rb')as stream:
        elf=ELFFile(stream)
        if elf['e_machine']!='EM_ARM'or elf.elfclass!=32 or not elf.little_endian:raise ValueError('Data object has another physical architecture')
        symbols=list(elf.get_section_by_name('.symtab').iter_symbols());name='native_data_'+f'{int(row["address"],0):08x}';symbol=next(s for s in symbols if s.name==name);section=elf.get_section(symbol['st_shndx'])
        if symbol['st_info']['type']!='STT_OBJECT'or symbol['st_size']!=row['bytes']or symbol['st_value']!=0:raise ValueError('Typed data symbol geometry differs')
        if section['sh_type']!='SHT_PROGBITS'or section['sh_size']!=row['bytes']or section['sh_flags']&5!=0 or not section['sh_flags']&2:raise ValueError('Data is not exact read-only initialized non-executable PROGBITS')
        executable=sum(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&2 and s['sh_flags']&4);zero=sum(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&2 and s['sh_type']=='SHT_NOBITS');allocated=sum(s['sh_size']for s in elf.iter_sections()if s['sh_flags']&2)
        if executable or zero or allocated!=row['bytes']or any(s['st_info']['type']=='STT_FUNC'and s['st_size']for s in symbols):raise ValueError('Data object contains code, BSS, padding or another allocated object')
        debug=0
        for rel in elf.iter_sections():
            if rel['sh_type']not in('SHT_REL','SHT_RELA'):continue
            if elf.get_section(rel['sh_info'])['sh_flags']&2 and rel.num_relocations():raise ValueError('Data object contains allocated relocations')
            debug+=rel.num_relocations()
        payload=section.data()
        if expected is not None and payload!=expected:raise ValueError('Actual typed compiler data differs from independent ASCII predicates')
        return payload,dict(symbol=name,section=section.name,sectionIndex=symbol['st_shndx'],sectionOffset=0,actualSourceSymbolType='STT_OBJECT',sourceSectionAlignment=section['sh_addralign'],allocatedBytes=allocated,executableSectionBytes=executable,allocatedZeroFillBytes=zero,sectionPaddingBytes=0,allocatedRelocations=0,nonAllocatedDebugRelocations=debug,objectUnmodified=True)


def build(source,row,folder,expected=None):
    if sha256(COMPILER)!=COMPILER_SHA or sha256(LINKER)!=LINKER_SHA:raise ValueError('Frozen data compiler/linker differs')
    folder.mkdir(parents=True,exist_ok=True);obj=folder/'data.o';environment=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'))
    command=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];process=subprocess.run(command,cwd=ROOT,capture_output=True,text=True,timeout=60,env=environment)
    if process.returncode:raise ValueError(('Actual semantic data compile failed',process.stdout,process.stderr))
    payload,geometry=inspect(obj,row,expected);copied=folder/'input.o';shutil.copyfile(obj,copied);object_sha=sha256(obj)
    lcf=folder/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = '+row['address']+' > data.bin }\nSECTIONS { '+geometry['section']+': { input.o('+geometry['section']+') } > DATA }\n')
    linked=folder/'data.elf';link_command=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',geometry['symbol'],str(lcf),str(copied),'-o',str(linked)]
    process=subprocess.run(link_command,cwd=folder,capture_output=True,text=True,timeout=60,env=environment)
    if process.returncode:raise ValueError(('Genuine native data link failed',process.stdout,process.stderr))
    actual=(folder/'data.bin').read_bytes()
    if actual!=payload or sha256(obj)!=object_sha or sha256(copied)!=object_sha:raise ValueError('Native data link changed the genuine object/payload')
    with linked.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==geometry['symbol'])
        if symbol['st_info']['type']!='STT_OBJECT'or symbol['st_value']!=int(row['address'],0)or symbol['st_size']!=row['bytes']:raise ValueError('Genuine native data symbol placement differs')
    result=dict(name=geometry['symbol'],nativeAlias='data_'+f'{int(row["address"],0):08x}',program='',processor='arm9',module='main',kind='data',mode='data',sourceLanguage='C',address=row['address'],bytes=row['bytes'],size=row['bytes'],initializedBytes=row['bytes'],compiledBytes=len(payload),elementBytes=row['width'],elements=128,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),sourceDependencies=[],object=obj.relative_to(ROOT).as_posix(),objectSha256=object_sha,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_SHA,compilerFlags=FLAGS,compileCommand=command,linkerSha256=LINKER_SHA,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedDataBinary=(folder/'data.bin').relative_to(ROOT).as_posix(),linkedDataBinarySha256=sha256(folder/'data.bin'),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),linkCommand=link_command,relocations=[],ordinaryFunctionCredit=0,executableByteCredit=0,encodedAssetBytes=0,measuredZeroAlignmentBytes=0,realLink=dict(exactDataBytes=True,exactDataAddress=True,objectUnmodified=True),**geometry)
    return payload,result
