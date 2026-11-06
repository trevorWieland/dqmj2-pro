import hashlib
import os
import shutil
import subprocess
from project import ROOT,configuration,native_dependencies,sha256
from wave20261106_gp_character_data_paths import SOURCE,WORK,assert_owned,assert_work

native_dependencies(configuration())
from elftools.elf.elffile import ELFFile

COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
LINKER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
COMPILER_HASH='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER_HASH='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
FLAGS=['-O2','-proc','arm946e','-char','signed','-str','noreuse','-sym','on','-gccinc','-nolink','-lang','c99']


def inspect_object(path,symbol,payload):
    with path.open('rb')as stream:
        elf=ELFFile(stream);symbols=list(elf.get_section_by_name('.symtab').iter_symbols());entry=next(s for s in symbols if s.name==symbol);section=elf.get_section(entry['st_shndx'])
        if entry['st_info']['type']!='STT_OBJECT'or entry['st_info']['bind']!='STB_GLOBAL'or entry['st_size']!=len(payload)or entry['st_value']!=0:raise ValueError('Complete typed character STT_OBJECT extent differs')
        if section['sh_type']!='SHT_PROGBITS'or section['sh_flags']!=2 or section['sh_size']!=len(payload)or section.data()!=payload:raise ValueError('Complete read-only character section/payload differs')
        if any(s['sh_size']and s['sh_flags']&2 and s.name!=section.name for s in elf.iter_sections()):raise ValueError('Unowned extra allocated code/data/BSS emitted')
        definitions=[s.name for s in symbols if s['st_info']['type']in('STT_OBJECT','STT_FUNC')and isinstance(s['st_shndx'],int)and s['st_size']and elf.get_section(s['st_shndx'])['sh_flags']&2]
        if definitions!=[symbol]:raise ValueError('Character compilation defines another object/function')
        debug=0
        for s in elf.iter_sections():
            if s['sh_type']not in('SHT_REL','SHT_RELA'):continue
            target=elf.get_section(s['sh_info'])
            if target['sh_flags']&2 and s.num_relocations():raise ValueError('Character initializer has an allocated relocation')
            if not target['sh_flags']&2:
                if not target.name.startswith('.debug'):raise ValueError('Unexpected character nonallocated relocation')
                debug+=s.num_relocations()
        return section.name,entry['st_shndx'],debug


def compile_link(row,source,payload,directory):
    assert_owned();assert_work(directory)
    if not any(source.resolve().is_relative_to(p.resolve())for p in [SOURCE,WORK]):raise ValueError('Character C compile escaped ownership')
    if sha256(COMPILER)!=COMPILER_HASH or sha256(LINKER)!=LINKER_HASH:raise ValueError('Pinned data compiler/linker changed')
    directory.mkdir(parents=True,exist_ok=True);obj=directory/'data.o';env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat'));command=[str(COMPILER),*FLAGS,'-c',str(source),'-o',str(obj)];run=subprocess.run(command,cwd=ROOT,env=env,capture_output=True,text=True,timeout=60)
    if run.returncode:raise ValueError(('Character C compilation failed',run.stdout,run.stderr))
    symbol=row['nativeSymbol'];section,index,debug=inspect_object(obj,symbol,payload);before=sha256(obj);linkdir=directory/'link';linkdir.mkdir(parents=True,exist_ok=True);local=linkdir/'input.o';shutil.copyfile(obj,local);lcf=linkdir/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = '+row['address']+' > data.bin }\nSECTIONS {\n'+section+': { input.o('+section+') } > DATA\n}\n',encoding='utf-8');linked=linkdir/'linked.elf';link_command=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',symbol,str(lcf),str(local),'-o',str(linked)];result=subprocess.run(link_command,cwd=linkdir,env=env,capture_output=True,text=True,timeout=60)
    if result.returncode:raise ValueError(('Character genuine MW link failed',result.stdout,result.stderr))
    output=linkdir/'data.bin'
    if output.read_bytes()!=payload or sha256(obj)!=before or sha256(local)!=before:raise ValueError('Original character object changed or full linked payload differs')
    with linked.open('rb')as stream:
        elf=ELFFile(stream);entry=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==symbol)
        if (entry['st_info']['type'],entry['st_size'],entry['st_value'])!=('STT_OBJECT',len(payload),int(row['address'],0)):raise ValueError('Genuine complete character native placement differs')
        if any(s['sh_flags']&4 and s['sh_size']for s in elf.iter_sections()):raise ValueError('Character link emitted executable code')
    proof=dict(exactDataBytes=True,exactDataAddress=True,objectUnmodified=True,actualSymbolType='STT_OBJECT',linkerSha256=LINKER_HASH,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedData=output.relative_to(ROOT).as_posix(),linkedDataSha256=sha256(output),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),command=link_command)
    return dict(object=obj.relative_to(ROOT).as_posix(),objectSha256=before,compiler=COMPILER.relative_to(ROOT).as_posix(),compilerSha256=COMPILER_HASH,compilerFlags=FLAGS,compilerCommand=command,section=section,sectionIndex=index,sectionOffset=0,nonAllocatedDebugRelocations=debug,realLink=proof,outputSha256=hashlib.sha256(payload).hexdigest())
