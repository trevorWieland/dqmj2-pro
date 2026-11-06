import os
import shutil
import subprocess
from project import ROOT,sha256
import match_runtime
from elftools.elf.elffile import ELFFile
WORK=ROOT/'work/w5sd-source'
GENERATED=ROOT/'generated/child-sdat-next'
COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
COMPILER_HASH='7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
LINKER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwldarm.exe'
LINKER_HASH='bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
FLAGS=['-O2','-proc','arm946e','-sym','on','-nolink','-lang','c99']


def compile_unit(source,directory,flags=None):
    if WORK!=ROOT/'work/w5sd-source' or GENERATED!=ROOT/'generated/child-sdat-next':raise ValueError('New static data build work/generated scope differs')
    if not directory.resolve().is_relative_to(WORK.resolve()) or not(source.resolve().is_relative_to(WORK.resolve()) or source.resolve().is_relative_to(GENERATED.resolve())):raise ValueError('New data compiler source/output escapes owned scope')
    if sha256(COMPILER)!=COMPILER_HASH:raise ValueError('Pinned actual C99 data compiler changed')
    directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';argv=[str(COMPILER),*(FLAGS if flags is None else flags),'-c',str(source),'-o',str(obj)];p=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    return obj,dict(command=argv,cwd=str(ROOT),exitCode=p.returncode,stdout=p.stdout,stderr=p.stderr)


def inspect_object(obj,symbol,expected):
    with obj.open('rb') as stream:
        elf=ELFFile(stream);table=elf.get_section_by_name('.symtab');entry=next((s for s in table.iter_symbols() if s.name==symbol),None)
        if entry is None or entry['st_info']['type']!='STT_OBJECT' or entry['st_info']['bind']!='STB_GLOBAL' or entry['st_size']!=len(expected):raise ValueError('Exact global STT_OBJECT symbol/type/complete size differs')
        section=elf.get_section(entry['st_shndx'])
        if section['sh_type']!='SHT_PROGBITS' or section['sh_flags']!=2:raise ValueError('Static asset must occupy immutable allocated nonexecutable data')
        if any(s['sh_flags']&4 and s['sh_size'] for s in elf.iter_sections()) or any(s['st_info']['type']=='STT_FUNC' and s['st_size'] for s in table.iter_symbols()):raise ValueError('Static data object contains executable instructions/function storage')
        debug=0
        for rel in elf.iter_sections():
            if rel['sh_type'] not in ['SHT_REL','SHT_RELA']:continue
            target=elf.get_section(rel['sh_info'])
            if target['sh_flags']&2:
                if rel.num_relocations():raise ValueError('Allocated static data must contain0relocations')
            elif not target.name.startswith('.debug'):raise ValueError('Unclassified nonallocated data-object relocation')
            else:debug+=rel.num_relocations()
        if sum(s['sh_size'] for s in elf.iter_sections() if s['sh_flags']&2)!=len(expected):raise ValueError('Data object allocates unselected extra storage')
        if section.data()[entry['st_value']:entry['st_value']+entry['st_size']]!=expected:raise ValueError('Complete static object bytes differ from semantic storage')
        return dict(section=section.name,sectionIndex=entry['st_shndx'],sectionOffset=entry['st_value'],nonAllocatedDebugRelocations=debug,executableSectionBytes=0,allocatedRelocations=0,allocatedZeroFillBytes=0)


def link_unit(obj,symbol,section,address,expected,directory):
    if not directory.resolve().is_relative_to(WORK.resolve()) or sha256(LINKER)!=LINKER_HASH:raise ValueError('New static data linker scope/tool differs')
    directory.mkdir(parents=True,exist_ok=True);local=directory/'input.o';shutil.copyfile(obj,local);before=sha256(obj);lcf=directory/'data.lcf';lcf.write_text('MEMORY { DATA: ORIGIN = '+hex(address)+' > data.bin }\nSECTIONS {\n'+section+': { input.o('+section+') } > DATA\n}\n');linked=directory/'linked.elf';argv=[str(LINKER),'-nostdlib','-nodeadstrip','-proc','arm946e','-main',symbol,str(lcf),str(local),'-o',str(linked)];p=subprocess.run(argv,cwd=directory,capture_output=True,text=True,timeout=60,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if p.returncode:raise ValueError(('Genuine original pinned data linker rejected object',p.stdout,p.stderr))
    if sha256(obj)!=before or sha256(local)!=before or (directory/'data.bin').read_bytes()!=expected:raise ValueError('Genuine data link changed object or complete storage bytes')
    with linked.open('rb') as stream:
        elf=ELFFile(stream);entry=next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name==symbol)
        if entry['st_info']['type']!='STT_OBJECT' or entry['st_value']!=address or entry['st_size']!=len(expected) or any(s['sh_flags']&4 and s['sh_size'] for s in elf.iter_sections()):raise ValueError('Actual linked data symbol/address/extent/executable flags differ')
    return dict(exactDataBytes=True,exactDataAddress=True,actualSymbolType='STT_OBJECT',objectUnmodified=True,objectSha256=before,linkedElf=linked.relative_to(ROOT).as_posix(),linkedElfSha256=sha256(linked),linkedDataSha256=sha256(directory/'data.bin'),lcf=lcf.relative_to(ROOT).as_posix(),lcfSha256=sha256(lcf),linkerSha256=LINKER_HASH,command=argv,executableSectionBytes=0,initializedDataRelocations=0,ordinaryFunctionCredit=0)
