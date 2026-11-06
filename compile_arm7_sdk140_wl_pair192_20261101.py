import hashlib
import json
import os
from pathlib import Path
import subprocess
import match_runtime
import link_arm7_bulk_20261030 as base_linker
import link_arm7_sdk140_wl_rate64_20261101 as qualified_linker
from elftools.elf.elffile import ELFFile
from project import ROOT,sha256
class Dispatch:
    def validate(self,row,directory):
        if int(row['address'],0)==0x027e9b98:return qualified_linker.validate(row,directory)
        return base_linker.validate(row,directory)
linker=Dispatch()

def compile_unit(seed,source,directory,strict=True):
    directory.mkdir(parents=True,exist_ok=True);obj=directory/'compiled.o';compiler=ROOT/seed['compiler']
    if sha256(compiler)!=seed['compilerSha256']:raise ValueError('Compiler differs')
    for dep in seed['sourceDependencies']:
        if sha256(ROOT/dep['path'])!=dep['sha256']:raise ValueError('Complete declared header differs')
    flags=seed['compilerFlags'];argv=[str(compiler),*flags,'-c',str(source),'-o',str(obj)]
    result=subprocess.run(argv,cwd=ROOT,capture_output=True,text=True,timeout=30,env=dict(os.environ,LM_LICENSE_FILE=str(ROOT/'tools/mwccarm/mwccarm/license.dat')))
    if result.returncode:raise ValueError(result.stdout+result.stderr)
    with obj.open('rb')as stream:
        elf=ELFFile(stream);symbol=next(s for s in elf.get_section_by_name('.symtab').iter_symbols()if s.name==seed['name']);start=symbol['st_value']&~1;size=symbol['st_size'];body=elf.get_section(symbol['st_shndx']).data()[start:start+size];relocations=[]
        for section in elf.iter_sections():
            if section['sh_type']not in('SHT_REL','SHT_RELA')or section['sh_info']!=symbol['st_shndx']:continue
            symbols=elf.get_section(section['sh_link'])
            for rel in section.iter_relocations():
                offset=rel['r_offset']-start
                if 0<=offset<size:relocations.append(dict(offset=offset,type=rel['r_info_type'],symbol=symbols.get_symbol(rel['r_info_sym']).name,format=section['sh_type'],explicitAddend=rel['r_addend']if section['sh_type']=='SHT_RELA'else None,originalEncodedWord=body[offset:offset+4].hex()))
    row=dict(seed,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compiledBytes=size,relocations=relocations,object=obj.relative_to(ROOT).as_posix(),objectSha256=sha256(obj),sectionIndex=symbol['st_shndx'],sectionOffset=start,command=argv,cwd=str(ROOT),exitCode=0,stdout=result.stdout,stderr=result.stderr)
    try:link=linker.validate(row,directory/'real-link')
    except ValueError as error:
        import ast
        if strict:raise
        link=ast.literal_eval(str(error))
        if not isinstance(link,dict)or not all(k in link for k in('nativeBytes','linkedBytes','matchingBytes')):raise ValueError('Unqualified wrong-source linker failure')
    return row,link,(directory/'real-link/caller.bin').read_bytes()
